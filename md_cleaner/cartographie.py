"""Cartographie JSON bloc → page (FR-010, contracts/formats.md, D6)."""

import json
from pathlib import Path

from md_cleaner.nettoyage import Bloc
from md_cleaner.segmentation import Page


def marqueur_page(numero: int) -> str:
    """Chaîne exacte insérée dans le .md paginé (contrat de cohérence)."""
    return f"<!-- page: {numero} -->"


def construire_cartographie(
    source: str, mode_pagination: str, pages: list[Page], blocs: list[Bloc]
) -> dict:
    """Construit la cartographie conforme à contracts/formats.md."""
    par_page: dict[int, list[str]] = {}
    for bloc in blocs:
        par_page.setdefault(bloc.page, []).append(bloc.id)
    entrees_pages = []
    for page in pages:
        if page.numero not in par_page:
            continue
        entree: dict = {
            "page": page.numero,
            "marqueur": marqueur_page(page.numero),
            "blocs": par_page[page.numero],
        }
        if page.url_source is not None:
            entree["url_source"] = page.url_source
        entrees_pages.append(entree)
    return {
        "version": 1,
        "source": source,
        "mode_pagination": mode_pagination,
        "pages": entrees_pages,
        "blocs": [
            {"id": b.id, "page": b.page, "debut": b.debut, "fin": b.fin} for b in blocs
        ],
    }


def ecrire_cartographie(chemin: Path, cartographie: dict) -> None:
    """Sérialisation déterministe : clés triées, indentation 2 (D9)."""
    Path(chemin).write_text(
        json.dumps(cartographie, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
