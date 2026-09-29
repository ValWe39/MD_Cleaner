"""Point d'entrée CLI (contracts/cli.md) : commandes, options, codes retour.

Codes retour : 0 succès, 1 entrée invalide, 2 artefact fourni invalide,
3 usage invalide.
"""

import argparse
import sys
from pathlib import Path

from md_cleaner.cartographie import construire_cartographie, ecrire_cartographie
from md_cleaner.detection import ErreurEchantillon, charger_echantillon, detecter
from md_cleaner.nettoyage import ecrire_nettoye, ecrire_nettoye_pagine, nettoyer
from md_cleaner.segmentation import segmenter
from md_cleaner.sortie import creer_dossier_run
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
    analyseur.add_argument("fichier", type=Path, help="fichier .md à nettoyer")
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


def main(argv: list[str] | None = None) -> int:
    args = construire_analyseur().parse_args(argv)

    if args.dry_run and args.suggestion:
        print("erreur : --dry-run et --suggestion sont incompatibles", file=sys.stderr)
        return CODE_USAGE

    fichier: Path = args.fichier
    if not fichier.is_file() or fichier.suffix.lower() != ".md":
        print(
            f"entrée invalide : {fichier} (fichier .md existant et lisible attendu)",
            file=sys.stderr,
        )
        return CODE_ENTREE
    try:
        texte = fichier.read_text(encoding="utf-8-sig")
    except OSError as erreur:
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

    pages_calibrage = pages[: args.calibrage]
    if args.echantillon is not None:
        try:
            pages_calibrage = charger_echantillon(args.echantillon)
        except ErreurEchantillon as erreur:
            print(f"échantillon invalide : {erreur}", file=sys.stderr)
            return CODE_ARTEFACT

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
            fichier.name, args.seuil, mode, len(pages), motifs
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
    ecrire_nettoye(dossier / "nettoye.md", blocs)
    if args.pagine:
        ecrire_nettoye_pagine(dossier / "nettoye-pagine.md", pages, blocs)
        ecrire_cartographie(
            dossier / "cartographie.json",
            construire_cartographie(fichier.name, mode, pages, blocs),
        )
    print(f"Sortie : {dossier / 'nettoye.md'}")
    if args.pagine:
        print(f"Sortie paginée : {dossier / 'nettoye-pagine.md'}")
        print(f"Cartographie : {dossier / 'cartographie.json'}")
    for message in avertissements:
        print(f"AVERTISSEMENT : {message}", file=sys.stderr)
    return CODE_OK
