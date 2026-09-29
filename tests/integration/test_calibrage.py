"""Tests d'intégration US4 (T027) : calibrage sur Exemple_2 (FR-012, FR-013, D7)."""

from pathlib import Path

from md_cleaner.cli import CODE_OK, main

RACINE = Path(__file__).parents[2]
ENTREE = RACINE / "Examples" / "Exemple_2" / "2.Input" / "consolidated.md"
ECHANTILLON = RACINE / "Examples" / "Exemple_2" / "1.Sample"


def _lignes_supprimees(sortie: Path) -> set[str]:
    """Lignes de l'entrée absentes de la sortie nettoyée."""
    from tests.integration.test_nettoyage_simple import _lignes_non_vides

    nettoye = (sortie / "001" / "nettoye.md").read_text(encoding="utf-8")
    return _lignes_non_vides(ENTREE.read_text(encoding="utf-8")) - _lignes_non_vides(
        nettoye
    )


def test_echantillon_au_moins_autocalibrage(tmp_path) -> None:
    """L'échantillon fourni supprime au moins les lignes que l'auto-calibrage
    supprime (comparaison des lignes retirées, pas des extraits)."""
    assert main([str(ENTREE), "--sortie", str(tmp_path / "auto")]) == CODE_OK
    assert (
        main(
            [
                str(ENTREE),
                "--echantillon",
                str(ECHANTILLON),
                "--sortie",
                str(tmp_path / "echantillon"),
            ]
        )
        == CODE_OK
    )
    supprimees_auto = _lignes_supprimees(tmp_path / "auto")
    supprimees_echantillon = _lignes_supprimees(tmp_path / "echantillon")
    assert supprimees_auto, "l'auto-calibrage doit supprimer du boilerplate"
    assert supprimees_echantillon >= supprimees_auto


def test_echantillon_invalide(tmp_path) -> None:
    from md_cleaner.cli import CODE_ARTEFACT

    dossier_vide = tmp_path / "vide"
    dossier_vide.mkdir()
    code = main([str(ENTREE), "--echantillon", str(dossier_vide)])
    assert code == CODE_ARTEFACT
