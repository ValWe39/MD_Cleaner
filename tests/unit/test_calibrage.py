"""Tests unitaires de calibrage (T025) : échantillon, auto-calibrage N=5 (FR-012, FR-013, D7)."""

import pytest

from md_cleaner.detection import (
    ErreurEchantillon,
    charger_echantillon,
    detecter,
)
from md_cleaner.normalisation import normaliser_ligne
from md_cleaner.segmentation import Page

NAV = ["Aller au contenu", "[CORSEN](</fr/>)", "[Insights](</fr/insights/>)"]


def _pages(contenus: list[list[str]]) -> list[Page]:
    return [Page(i + 1, None, lignes) for i, lignes in enumerate(contenus)]


def _ecrire_echantillon(tmp_path, noms: list[str]) -> None:
    for nom in noms:
        (tmp_path / nom).write_text(f"# Page {nom}\n", encoding="utf-8")


def test_echantillon_trie_par_nom(tmp_path) -> None:
    _ecrire_echantillon(tmp_path, ["c.md", "a.md", "b.md"])
    pages = charger_echantillon(tmp_path)
    assert [p.lignes[0] for p in pages] == [
        "# Page a.md",
        "# Page b.md",
        "# Page c.md",
    ]


def test_echantillon_vide(tmp_path) -> None:
    with pytest.raises(ErreurEchantillon, match="aucun fichier"):
        charger_echantillon(tmp_path)


def test_echantillon_trop_grand(tmp_path) -> None:
    _ecrire_echantillon(tmp_path, [f"p{i}.md" for i in range(6)])
    with pytest.raises(ErreurEchantillon, match="au plus 5"):
        charger_echantillon(tmp_path)


def test_dossier_introuvable(tmp_path) -> None:
    with pytest.raises(ErreurEchantillon, match="introuvable"):
        charger_echantillon(tmp_path / "absent")


def test_auto_calibrage_cinq_premieres_pages() -> None:
    """Un motif absent des 5 premières pages n'est pas calibré par défaut."""
    contenus = []
    for i in range(10):
        page = [f"Contenu mot {chr(97 + i)}"]
        if i >= 5:
            page = ["BANDEAU TARDIF"] + page
        contenus.append(page)
    pages = _pages(contenus)
    motifs_auto = detecter(pages, pages_calibrage=pages[:5])
    cible = [normaliser_ligne(l) for l in ["BANDEAU TARDIF"]]
    assert not [m for m in motifs_auto if m.lignes_norm == cible]
    motifs_complet = detecter(pages)
    assert any(m.lignes_norm == cible for m in motifs_complet)
