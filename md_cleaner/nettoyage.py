"""Nettoyage des pages et écriture des sorties (FR-004, FR-009, FR-016, D6)."""

from dataclasses import dataclass

from md_cleaner.detection import Motif
from md_cleaner.segmentation import Page

SEUIL_QUASI_VIDE = 0.05


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


def ecrire_nettoye(chemin, blocs: list[Bloc]) -> None:
    """Écrit le .md nettoyé simple, sans marqueur de page (FR-004)."""
    lignes: list[str] = []
    for bloc in blocs:
        lignes.extend(bloc.texte)
    lignes = _compacter(lignes)
    from pathlib import Path

    Path(chemin).write_text("\n".join(lignes) + "\n", encoding="utf-8")


def ecrire_nettoye_pagine(chemin, pages: list[Page], blocs: list[Bloc]) -> None:
    """Écrit le .md paginé : --- + <!-- page: N --> par page (D6, FR-009)."""
    from pathlib import Path

    par_page: dict[int, list[str]] = {}
    for bloc in blocs:
        par_page.setdefault(bloc.page, []).extend(bloc.texte)
    morceaux: list[str] = []
    for page in pages:
        contenu = _compacter(par_page.get(page.numero, []))
        if not contenu:
            continue
        morceaux.append(f"---\n\n<!-- page: {page.numero} -->\n\n")
        morceaux.append("\n".join(contenu) + "\n")
    Path(chemin).write_text("".join(morceaux), encoding="utf-8")
