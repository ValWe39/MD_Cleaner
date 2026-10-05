"""Tests d'intégration US3 (T024) : pagination et cartographie (FR-009 à FR-011, SC-006)."""

import json
from pathlib import Path

from md_cleaner.cli import CODE_OK, main

RACINE = Path(__file__).parents[2]
ENTREE = RACINE / "Examples" / "Exemple_1" / "2.Input" / "consolidated.md"


def test_marqueurs_et_cartographie_coherents(tmp_path) -> None:
    code = main([str(ENTREE), "--pagine", "--sortie", str(tmp_path)])
    assert code == CODE_OK
    dossier = tmp_path / "001"
    pagine = (dossier / "nettoye-pagine.md").read_text(encoding="utf-8")
    simple = (dossier / "consolidated-nettoye.md").read_text(encoding="utf-8")
    carto = json.loads((dossier / "cartographie.json").read_text(encoding="utf-8"))

    assert carto["version"] == 1
    assert carto["source"] == "consolidated.md"
    assert carto["mode_pagination"] == "explicite"

    # Chaque marqueur apparaît exactement une fois (contrat de cohérence)
    for page in carto["pages"]:
        assert pagine.count(page["marqueur"]) == 1
    references = {bid for p in carto["pages"] for bid in p["blocs"]}
    declares = {b["id"] for b in carto["blocs"]}
    assert references == declares

    # La sortie simple ne porte ni marqueur ni séparateur d'origine (Q2 → A)
    assert "<!-- page:" not in simple
    assert "## Page 1:" not in simple
    assert "## Page 1:" not in pagine

    # Les URL sources sont conservées dans la cartographie
    assert any("url_source" in p for p in carto["pages"])


def test_document_sans_separateurs(tmp_path) -> None:
    """Sans séparateurs explicites : heuristique signalée ou mode unique,
    jamais de pagination silencieuse (FR-011)."""
    lignes = ENTREE.read_text(encoding="utf-8").splitlines()
    sans_separateurs = [
        ligne
        for ligne in lignes
        if not ligne.lstrip("# ").startswith("Page ")
        or not ligne.strip().startswith("#")
    ]
    entree = tmp_path / "sans-separateurs.md"
    entree.write_text("\n".join(sans_separateurs), encoding="utf-8")
    code = main([str(entree), "--pagine", "--sortie", str(tmp_path / "sortie")])
    assert code == CODE_OK
    carto = json.loads(
        (tmp_path / "sortie" / "001" / "cartographie.json").read_text(encoding="utf-8")
    )
    assert carto["mode_pagination"] in {"heuristique", "unique"}
