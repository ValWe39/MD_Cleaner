"""Tests d'intégration US1 (T014) : nettoyage simple sur Exemple_1 (SC-001, SC-002, SC-005)."""

from pathlib import Path

from md_cleaner.cli import CODE_ENTREE, CODE_OK, main

RACINE = Path(__file__).parents[2]
ENTREE = RACINE / "Examples" / "Exemple_1" / "2.Input" / "consolidated.md"


def _lignes_non_vides(texte: str) -> set[str]:
    return {ligne.strip() for ligne in texte.splitlines() if ligne.strip()}


def _occurrences(texte: str) -> dict[str, int]:
    compteur: dict[str, int] = {}
    for ligne in texte.splitlines():
        propre = ligne.strip()
        if propre:
            compteur[propre] = compteur.get(propre, 0) + 1
    return compteur


def test_nettoyage_supprime_le_boilerplate(tmp_path) -> None:
    code = main([str(ENTREE), "--sortie", str(tmp_path)])
    assert code == CODE_OK
    nettoye = (tmp_path / "001" / "nettoye.md").read_text(encoding="utf-8")
    assert "Aller au contenu principal" not in nettoye
    assert "[CORSEN AI](</fr/>)" not in nettoye
    assert "SASU · Paris, France" not in nettoye


def test_contenu_unique_conserve_a_100_pourcents(tmp_path) -> None:
    """SC-005 : toute ligne de contenu unique figure dans la sortie.

    Sont exclus les séparateurs de pages (supprimés par conception,
    clarification Q2 → A) et les lignes uniques uniquement par leurs
    parties variables (FR-003 : leur forme normalisée est récurrente)."""
    main([str(ENTREE), "--sortie", str(tmp_path)])
    nettoye = (tmp_path / "001" / "nettoye.md").read_text(encoding="utf-8")
    occurrences = _occurrences(ENTREE.read_text(encoding="utf-8"))
    from md_cleaner.normalisation import normaliser_ligne
    from md_cleaner.segmentation import RE_SEPARATEUR

    occurrences_norm: dict[str, int] = {}
    for ligne in occurrences:
        occurrences_norm[normaliser_ligne(ligne)] = (
            occurrences_norm.get(normaliser_ligne(ligne), 0) + 1
        )
    uniques = {
        ligne
        for ligne, n in occurrences.items()
        if n == 1
        and not RE_SEPARATEUR.match(ligne)
        and occurrences_norm[normaliser_ligne(ligne)] == 1
    }
    assert uniques <= _lignes_non_vides(nettoye)


def test_boilerplate_supprime_a_90_pourcents(tmp_path) -> None:
    """SC-001 : au moins 90 % des lignes répétées (12+ occurrences) sont supprimées."""
    main([str(ENTREE), "--sortie", str(tmp_path)])
    nettoye = (tmp_path / "001" / "nettoye.md").read_text(encoding="utf-8")
    lignes_nettoye = _lignes_non_vides(nettoye)
    occurrences = _occurrences(ENTREE.read_text(encoding="utf-8"))
    boilerplate = {ligne for ligne, n in occurrences.items() if n >= 12}
    supprimees = {ligne for ligne in boilerplate if ligne not in lignes_nettoye}
    assert len(supprimees) >= 0.9 * len(boilerplate)


def test_determinisme_octet_par_octet(tmp_path) -> None:
    """SC-002 : deux exécutions identiques produisent des sorties identiques."""
    main([str(ENTREE), "--sortie", str(tmp_path / "run1")])
    main([str(ENTREE), "--sortie", str(tmp_path / "run2")])
    premier = (tmp_path / "run1" / "001" / "nettoye.md").read_bytes()
    second = (tmp_path / "run2" / "001" / "nettoye.md").read_bytes()
    assert premier == second


def test_entree_invalide(tmp_path) -> None:
    assert main([str(tmp_path / "absent.md")]) == CODE_ENTREE
    (tmp_path / "fichier.txt").write_text("x", encoding="utf-8")
    assert main([str(tmp_path / "fichier.txt")]) == CODE_ENTREE
