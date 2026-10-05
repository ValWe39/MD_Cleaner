"""Point d'entrée CLI (contracts/cli.md) : commandes, options, codes retour.

Codes retour : 0 succès, 1 entrée invalide, 2 artefact fourni invalide,
3 usage invalide.
"""

import argparse
import sys
from pathlib import Path

from md_cleaner.cartographie import construire_cartographie, ecrire_cartographie
from md_cleaner.detection import ErreurEchantillon, charger_echantillon, detecter
from md_cleaner.lot import resoudre_lot
from md_cleaner.nettoyage import ecrire_nettoye, ecrire_nettoye_pagine, nettoyer
from md_cleaner.normalisation import nom_sortie_nettoye
from md_cleaner.segmentation import segmenter
from md_cleaner.sortie import creer_dossier_run, resoudre_chemin_nettoye
from md_cleaner.suggestion import (
    ErreurSuggestion,
    appliquer_actions,
    construire_suggestion,
    ecrire_suggestion,
    generer_rapport,
    lire_suggestion,
)

CODE_OK = 0
CODE_ENTREE = 1
CODE_ARTEFACT = 2
CODE_USAGE = 3


def _entier_bornes(nom: str, mini: int, maxi: int) -> callable:
    def convertit(valeur: str) -> int:
        try:
            nombre = int(valeur)
        except ValueError:
            raise argparse.ArgumentTypeError(f"{nom} : entier attendu") from None
        if not mini <= nombre <= maxi:
            raise argparse.ArgumentTypeError(
                f"{nom} : doit être entre {mini} et {maxi}"
            )
        return nombre

    return convertit


class _Analyseur(argparse.ArgumentParser):
    """Usage invalide → code retour 3 (contracts/cli.md)."""

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(CODE_USAGE, f"erreur : {message}\n")


def construire_analyseur() -> _Analyseur:
    analyseur = _Analyseur(
        prog="md-cleaner",
        description=(
            "Nettoie un fichier Markdown multi-pages de ses motifs répétitifs "
            "(navigation, fils d'Ariane, pieds de page)."
        ),
    )
    analyseur.add_argument(
        "entrees",
        nargs="+",
        type=Path,
        help="fichiers .md et/ou dossiers à nettoyer",
    )
    analyseur.add_argument(
        "--dry-run",
        action="store_true",
        help="produit rapport-dry-run.md et suggestion.json sans écrire de nettoyé",
    )
    analyseur.add_argument(
        "--suggestion",
        type=Path,
        help="consomme un suggestion.json (édité ou non)",
    )
    analyseur.add_argument(
        "--pagine",
        action="store_true",
        help="produit en plus nettoye-pagine.md et cartographie.json",
    )
    analyseur.add_argument(
        "--conserver-liens",
        action="store_true",
        help="conserve les destinations de liens inline ](<...>) dans les sorties .md",
    )
    analyseur.add_argument(
        "--seuil",
        type=_entier_bornes("--seuil", 2, 100),
        default=80,
        help="seuil de fréquence en %% des pages (défaut : 80)",
    )
    analyseur.add_argument(
        "--echantillon",
        type=Path,
        help="calibrage sur un échantillon fourni (au plus 5 fichiers .md)",
    )
    analyseur.add_argument(
        "--calibrage",
        type=_entier_bornes("--calibrage", 2, 50),
        default=5,
        help="nombre de premières pages pour l'auto-calibrage (défaut : 5)",
    )
    analyseur.add_argument(
        "--extrait",
        type=int,
        default=5,
        help=(
            "nombre de lignes d'extrait dans suggestion.json (2-25, défaut 5) ; "
            "effet limité au dry-run, sans effet observable sinon"
        ),
    )
    analyseur.add_argument(
        "--sortie",
        type=Path,
        default=Path("output"),
        help="dossier racine des sorties (défaut : ./output)",
    )
    analyseur.add_argument(
        "--nom-titre",
        type=_entier_bornes("--nom-titre", 5, 100),
        default=None,
        help="nomme le run d'après les X premiers caractères du titre",
    )
    return analyseur


def _titre_du_document(lignes: list[str], defaut: str) -> str:
    for ligne in lignes:
        if ligne.startswith("# "):
            return ligne[2:].strip()
    return defaut


def _traiter_document(
    args: argparse.Namespace,
    fichier: Path,
    pages_echantillon: list | None,
    en_lot: bool,
) -> int:
    """Traite un document par le chemin de la feature 001 (007, D4).

    ``en_lot`` adapte les messages d'erreur d'entrée au format ERREUR
    (FR-007) ; False conserve les messages actuels du mono-document
    (SC-005). ``pages_echantillon`` déjà chargée (calibrage global du lot)
    ou None : l'échantillon est alors chargé ici, à la position actuelle
    du mono-document.
    """
    if not fichier.is_file() or fichier.suffix.lower() != ".md":
        raison = "fichier .md existant et lisible attendu"
        if en_lot:
            print(f"ERREUR : {fichier} : {raison}", file=sys.stderr)
        else:
            print(f"entrée invalide : {fichier} ({raison})", file=sys.stderr)
        return CODE_ENTREE
    try:
        texte = fichier.read_text(encoding="utf-8-sig")
    except OSError as erreur:
        if en_lot:
            print(f"ERREUR : {fichier} : {erreur}", file=sys.stderr)
        else:
            print(f"entrée illisible : {erreur}", file=sys.stderr)
        return CODE_ENTREE

    lignes = texte.splitlines()
    titre = _titre_du_document(lignes, fichier.stem)

    pages, mode = segmenter(lignes)
    avertissements: list[str] = []
    if mode == "heuristique":
        avertissements.append(
            "pagination recréée par heuristique (aucun séparateur explicite)"
        )
    elif mode == "unique":
        avertissements.append(
            "aucune frontière de pages fiable : document traité comme section unique"
        )

    if args.echantillon is not None:
        if pages_echantillon is None:
            try:
                pages_echantillon = charger_echantillon(args.echantillon)
            except ErreurEchantillon as erreur:
                print(f"échantillon invalide : {erreur}", file=sys.stderr)
                return CODE_ARTEFACT
        pages_calibrage = pages_echantillon
    else:
        pages_calibrage = pages[: args.calibrage]

    motifs = detecter(pages, seuil=args.seuil, pages_calibrage=pages_calibrage)

    if args.suggestion is not None:
        try:
            suggestion = lire_suggestion(args.suggestion, fichier.name)
            appliquer_actions(motifs, suggestion)
        except ErreurSuggestion as erreur:
            print(f"suggestion invalide : {erreur}", file=sys.stderr)
            return CODE_ARTEFACT
    else:
        suggestion = construire_suggestion(
            fichier.name,
            args.seuil,
            mode,
            len(pages),
            motifs,
            pages=pages,
            extrait_n=args.extrait,
        )

    dossier = creer_dossier_run(args.sortie, titre, args.nom_titre)

    if args.dry_run:
        ecrire_suggestion(dossier / "suggestion.json", suggestion)
        generer_rapport(dossier / "rapport-dry-run.md", suggestion, avertissements)
        print(f"Rapport : {dossier / 'rapport-dry-run.md'}")
        print(f"Suggestion : {dossier / 'suggestion.json'}")
        for message in avertissements:
            print(f"AVERTISSEMENT : {message}", file=sys.stderr)
        return CODE_OK

    blocs, avertissements_nettoyage = nettoyer(pages, motifs)
    avertissements.extend(avertissements_nettoyage)
    # Nom de sortie dérivé du document d'entrée (feature 006, FR-001, FR-006) ;
    # collision résolue par suffixe -1, -2, ... jamais d'écrasement (FR-004)
    chemin_nettoye = resoudre_chemin_nettoye(dossier, nom_sortie_nettoye(fichier.stem))
    ecrire_nettoye(chemin_nettoye, blocs, conserver_liens=args.conserver_liens)
    if args.pagine:
        ecrire_nettoye_pagine(
            dossier / "nettoye-pagine.md",
            pages,
            blocs,
            conserver_liens=args.conserver_liens,
        )
        ecrire_cartographie(
            dossier / "cartographie.json",
            construire_cartographie(fichier.name, mode, pages, blocs),
        )
    print(f"Sortie : {chemin_nettoye}")
    if args.pagine:
        print(f"Sortie paginée : {dossier / 'nettoye-pagine.md'}")
        print(f"Cartographie : {dossier / 'cartographie.json'}")
    for message in avertissements:
        print(f"AVERTISSEMENT : {message}", file=sys.stderr)
    return CODE_OK


def main(argv: list[str] | None = None) -> int:
    args = construire_analyseur().parse_args(argv)

    if not 2 <= args.extrait <= 25:
        print("erreur : --extrait doit être entre 2 et 25", file=sys.stderr)
        return CODE_USAGE

    if args.dry_run and args.suggestion:
        print("erreur : --dry-run et --suggestion sont incompatibles", file=sys.stderr)
        return CODE_USAGE

    documents, avertissements_entrees = resoudre_lot(args.entrees)
    for message in avertissements_entrees:
        print(message, file=sys.stderr)
    if not documents:
        print("erreur : aucun document .md à traiter", file=sys.stderr)
        return CODE_ENTREE

    en_lot = len(documents) > 1
    if en_lot:
        if args.dry_run:
            print(
                "AVERTISSEMENT : --dry-run ignorée en lot : "
                "applicable à un seul document",
                file=sys.stderr,
            )
            args.dry_run = False
        if args.suggestion is not None:
            print(
                "AVERTISSEMENT : --suggestion ignorée en lot : "
                "applicable à un seul document",
                file=sys.stderr,
            )
            args.suggestion = None
    pages_echantillon: list | None = None
    if en_lot and args.echantillon is not None:
        try:
            pages_echantillon = charger_echantillon(args.echantillon)
        except ErreurEchantillon as erreur:
            print(f"échantillon invalide : {erreur}", file=sys.stderr)
            return CODE_ARTEFACT

    if not en_lot:
        return _traiter_document(args, documents[0], pages_echantillon, en_lot)

    code_final = CODE_OK
    echecs_consecutifs = 0
    for fichier in documents:
        if _traiter_document(args, fichier, pages_echantillon, en_lot) == CODE_OK:
            echecs_consecutifs = 0
            continue
        code_final = CODE_ENTREE
        echecs_consecutifs += 1
        if echecs_consecutifs >= 3:
            break
    return code_final
