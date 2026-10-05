"""Dossier de sortie et sous-dossiers de run (research.md D8, FR-006)."""

import re
from pathlib import Path

from md_cleaner.normalisation import slug_titre


def creer_dossier_run(racine: Path, titre: str, nom_titre: int | None) -> Path:
    """Crée le sous-dossier du run : numérotation séquentielle par défaut,
    ou slug des X premiers caractères du titre (option --nom-titre).
    Collision → suffixe -2, -3, ... (D8)."""
    racine = Path(racine)
    racine.mkdir(parents=True, exist_ok=True)
    if nom_titre is not None:
        base = slug_titre(titre, nom_titre) or "sans-titre"
        candidat = base
        indice = 2
        while (racine / candidat).exists():
            candidat = f"{base}-{indice}"
            indice += 1
    else:
        existants = {p.name for p in racine.iterdir() if p.is_dir()}
        numeros = [int(n) for n in existants if re.fullmatch(r"\d{3}", n)]
        candidat = f"{max(numeros) + 1 if numeros else 1:03d}"
    dossier = racine / candidat
    dossier.mkdir(parents=True)
    return dossier


def resoudre_chemin_libre(dossier: Path, base: str, extension: str) -> Path:
    """Premier chemin libre pour ``<base><suffixe><extension>`` (008, D4).

    Essaie ``<base><extension>``, puis ``<base>-1<extension>``,
    ``<base>-2<extension>``, ... — le suffixe de collision est inséré
    avant l'extension, de même forme que la règle 006. Retourne un
    chemin libre sans jamais écraser un fichier existant.
    """
    candidat = dossier / f"{base}{extension}"
    indice = 1
    while candidat.exists():
        candidat = dossier / f"{base}-{indice}{extension}"
        indice += 1
    return candidat


def resoudre_chemin_nettoye(dossier: Path, nom: str) -> Path:
    """Premier chemin libre pour le fichier nettoyé (006, D4, FR-004).

    Délègue à ``resoudre_chemin_libre`` (008, D4) : ``<nom>.md``, puis
    ``<nom>-1.md``, ``<nom>-2.md``, ... par ordre de traitement ; le
    suffixe de collision est ajouté à la fin du nom, avant
    l'extension. Retourne un chemin libre sans jamais écraser un
    fichier existant (SC-003).
    """
    return resoudre_chemin_libre(dossier, nom, ".md")
