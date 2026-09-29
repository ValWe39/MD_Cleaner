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
