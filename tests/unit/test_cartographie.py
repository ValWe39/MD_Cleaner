"""Tests unitaires de cartographie (T020) : ids, mode, cohérence (FR-010, D6)."""

import json

from md_cleaner.cartographie import (
    construire_cartographie,
    ecrire_cartographie,
    marqueur_page,
)
from md_cleaner.nettoyage import Bloc
from md_cleaner.segmentation import Page


def _pages() -> list[Page]:
    return [
        Page(1, "https://exemple.fr/1", ["Titre", "Corps"]),
        Page(2, None, ["Corps 2"]),
        Page(3, None, []),
    ]


def _blocs() -> list[Bloc]:
    return [
        Bloc("P1-B1", 1, ["Titre", "Corps"], 0, 1),
        Bloc("P2-B1", 2, ["Corps 2"], 0, 0),
    ]


def test_ids_uniques_et_sequence() -> None:
    carto = construire_cartographie("doc.md", "explicite", _pages(), _blocs())
    ids = [b["id"] for b in carto["blocs"]]
    assert ids == ["P1-B1", "P2-B1"]
    assert len(set(ids)) == len(ids)


def test_mode_pagination_reporte() -> None:
    carto = construire_cartographie("doc.md", "heuristique", _pages(), _blocs())
    assert carto["mode_pagination"] == "heuristique"


def test_url_source_absente_si_null() -> None:
    carto = construire_cartographie("doc.md", "explicite", _pages(), _blocs())
    pages = {p["page"]: p for p in carto["pages"]}
    assert "url_source" in pages[1]
    assert "url_source" not in pages[2]


def test_coherence_marqueurs_et_blocs() -> None:
    carto = construire_cartographie("doc.md", "explicite", _pages(), _blocs())
    references = {bid for p in carto["pages"] for bid in p["blocs"]}
    declares = {b["id"] for b in carto["blocs"]}
    assert references == declares
    for page in carto["pages"]:
        assert page["marqueur"] == marqueur_page(page["page"])


def test_page_sans_contenu_absente() -> None:
    carto = construire_cartographie("doc.md", "explicite", _pages(), _blocs())
    assert [p["page"] for p in carto["pages"]] == [1, 2]


def test_serialisation_deterministe(tmp_path) -> None:
    carto = construire_cartographie("doc.md", "explicite", _pages(), _blocs())
    ecrire_cartographie(tmp_path / "a.json", carto)
    ecrire_cartographie(tmp_path / "b.json", carto)
    assert (tmp_path / "a.json").read_bytes() == (tmp_path / "b.json").read_bytes()
    lue = json.loads((tmp_path / "a.json").read_text(encoding="utf-8"))
    assert lue == carto
