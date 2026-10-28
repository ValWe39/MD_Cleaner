"""Nettoyage des pages et écriture des sorties (FR-004, FR-009, FR-016, D6)."""

import re
from dataclasses import dataclass

from md_cleaner.detection import Motif
from md_cleaner.segmentation import Page

SEUIL_QUASI_VIDE = 0.05

RE_DESTINATION_LIEN = re.compile(r'(?<=\])\(<[^>]*>(?: "[^"]*")?\)')

RE_IMAGE_INLINE = re.compile(r"!\[[^\]]*\]\([^)]*\)")

RE_DESTINATION_SANS_CHEVRONS = re.compile(
    r'(?<=\])\((?!<)(?=[^)\s])[^)\s]*(?: "[^"]*")?\)'
)

RE_SENTINELLE_IMAGE = re.compile(r"\x00(\d+)\x00")


def _masquer_images(ligne: str, images: list[str]) -> str:
    """Remplace chaque image par une sentinelle invisible aux passes (009).

    Les sentinelles ne contiennent ni crochet fermant ni parenthèse :
    les deux règles de destinations leur sont aveugles ; la restauration
    réintroduit chaque construct à l'identique (FR-003, D2).
    """

    def remplacer(correspondance) -> str:
        images.append(correspondance.group(0))
        return f"\x00{len(images) - 1}\x00"

    return RE_IMAGE_INLINE.sub(remplacer, ligne)


def _restaurer_images(ligne: str, images: list[str]) -> str:
    """Réintroduit chaque image masquée à l'identique (FR-003, D2, D4)."""
    return RE_SENTINELLE_IMAGE.sub(
        lambda correspondance: images[int(correspondance.group(1))], ligne
    )


def nettoyer_destinations(lignes: list[str]) -> list[str]:
    """Retire les destinations de liens inline ](<...>) et ](...) (004/005/009).

    Deux règles distinctes, sans distinction de schéma (FR-001, D1) :
    la règle 004/005 cible la sous-chaîne `](<...>)` entre chevrons,
    titre éventuel emporté (premier `>` refermant, sans décodage) ; la
    règle 009 cible la sous-chaîne `](...)` sans chevrons qui suit le
    crochet fermant du libellé — destination sans espace ne commençant
    pas par `<` (chevrons réservés à la première règle, D3), ancre et
    destination vide `(#)` couvertes, titre `](url "titre")` emporté
    avec la destination. Seuls les libellés survivent ; libellés et
    reste de la ligne sont inchangés (FR-002).

    Les images `![alt](destination)` sont masquées avant les passes et
    restaurées après : aucune destination d'image n'est retirée ; dans
    un lien contenant une image, seule la destination du lien externe
    est retirée (FR-003, D2, D4).

    Limites documentées : un titre contenant un guillemet interne
    échappé (\\") arrête le match avant la parenthèse fermante, sans
    corruption (limite 005) ; un alt d'image contenant un crochet
    fermant n'est pas protégé et la règle lien standard s'applique
    alors à sa destination (limite 009). La passe est idempotente
    (FR-008) : aucune forme cible ne subsiste après un passage.
    """
    resultat: list[str] = []
    for ligne in lignes:
        images: list[str] = []
        masquee = _masquer_images(ligne, images)
        nettoyee = RE_DESTINATION_LIEN.sub("", masquee)
        nettoyee = RE_DESTINATION_SANS_CHEVRONS.sub("", nettoyee)
        resultat.append(_restaurer_images(nettoyee, images))
    return resultat


@dataclass
class Bloc:
    """Segment de contenu de valeur conservé (data-model.md)."""

    id: str
    page: int
    texte: list[str]
    debut: int
    fin: int


def _occurrences_supprimees(page: Page, motifs: list[Motif]) -> list[bool]:
    supprime = [False] * len(page.lignes)
    for motif in motifs:
        if motif.action != "supprimer":
            continue
        for debut, fin in motif.emplacements.get(page.numero, []):
            for i in range(debut, min(fin, len(supprime))):
                supprime[i] = True
    return supprime


def nettoyer(pages: list[Page], motifs: list[Motif]) -> tuple[list[Bloc], list[str]]:
    """Supprime les lignes des motifs action=supprimer ; renvoie blocs et
    avertissements (FR-016)."""
    avertissements: list[str] = []
    if len(pages) < 2:
        avertissements.append(
            "document trop court : une seule page détectée, aucun nettoyage appliqué"
        )
    blocs: list[Bloc] = []
    total = sum(len(p.lignes) for p in pages)
    gardees = 0
    for page in pages:
        supprime = _occurrences_supprimees(page, motifs)
        debut = None
        for i, est_supprime in enumerate(supprime + [True]):
            if not est_supprime and debut is None:
                debut = i
            elif est_supprime and debut is not None:
                texte = page.lignes[debut:i]
                if any(ligne.strip() for ligne in texte):
                    blocs.append(Bloc("", page.numero, texte, debut, i - 1))
                    gardees += len(texte)
                debut = None
    compteurs: dict[int, int] = {}
    for bloc in blocs:
        compteurs[bloc.page] = compteurs.get(bloc.page, 0) + 1
        bloc.id = f"P{bloc.page}-B{compteurs[bloc.page]}"
    if total and gardees / total < SEUIL_QUASI_VIDE:
        avertissements.append(
            "sortie quasi vide : moins de 5 % des lignes sont conservées"
        )
    return blocs, avertissements


def _compacter(lignes: list[str]) -> list[str]:
    """Plie les suites de lignes vides en une seule, sans vides aux bords."""
    resultat: list[str] = []
    for ligne in lignes:
        if not ligne.strip() and (not resultat or not resultat[-1].strip()):
            continue
        if not ligne.strip():
            resultat.append("")
        else:
            resultat.append(ligne.rstrip())
    while resultat and not resultat[-1].strip():
        resultat.pop()
    return resultat


def ecrire_nettoye(chemin, blocs: list[Bloc], conserver_liens: bool = False) -> None:
    """Écrit le .md nettoyé simple, sans marqueur de page (FR-004).

    Sans conserver_liens, retire les destinations ](</...>) du texte
    écrit ; les Blocs ne sont pas mutés (FR-002, FR-005).
    """
    lignes: list[str] = []
    for bloc in blocs:
        texte = bloc.texte if conserver_liens else nettoyer_destinations(bloc.texte)
        lignes.extend(texte)
    lignes = _compacter(lignes)
    from pathlib import Path

    Path(chemin).write_text("\n".join(lignes) + "\n", encoding="utf-8")


def ecrire_nettoye_pagine(
    chemin, pages: list[Page], blocs: list[Bloc], conserver_liens: bool = False
) -> None:
    """Écrit le .md paginé : --- + <!-- page: N --> par page (D6, FR-009).

    Sans conserver_liens, retire les destinations ](</...>) du contenu
    des pages ; les marqueurs sont générés après la passe et restent
    strictement inchangés (FR-004, D5).
    """
    from pathlib import Path

    par_page: dict[int, list[str]] = {}
    for bloc in blocs:
        par_page.setdefault(bloc.page, []).extend(bloc.texte)
    morceaux: list[str] = []
    for page in pages:
        contenu = par_page.get(page.numero, [])
        if not conserver_liens:
            contenu = nettoyer_destinations(contenu)
        contenu = _compacter(contenu)
        if not contenu:
            continue
        morceaux.append(f"---\n\n<!-- page: {page.numero} -->\n\n")
        morceaux.append("\n".join(contenu) + "\n")
    Path(chemin).write_text("".join(morceaux), encoding="utf-8")
