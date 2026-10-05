"""Tests unitaires feature 007 : résolution du lot (US1, T005).

Périmètre US1 : fichiers uniquement. Le développement des dossiers est
couvert par US2 (T008) dans ce même fichier.
"""

from pathlib import Path

from md_cleaner.lot import resoudre_lot


def test_fichiers_retenus_dans_l_ordre(tmp_path) -> None:
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    documents, avertissements = resoudre_lot([a, b])
    assert documents == [a, b]
    assert avertissements == []


def test_doublons_conserves(tmp_path) -> None:
    a = tmp_path / "a.md"
    documents, _ = resoudre_lot([a, a])
    assert documents == [a, a]


def test_chemin_inexistant_conserve(tmp_path) -> None:
    """Un chemin invalide transite jusqu'au traitement documentaire (D2)."""
    absent = tmp_path / "absent.md"
    documents, _ = resoudre_lot([absent])
    assert documents == [absent]


def test_liste_vide_donne_lot_vide() -> None:
    documents, avertissements = resoudre_lot([])
    assert documents == []
    assert avertissements == []


# --- US2 (T008) : développement des dossiers (FR-002, FR-008) ---


def test_dossier_developpe_en_md_premier_niveau(tmp_path) -> None:
    dossier = tmp_path / "corpus"
    dossier.mkdir()
    (dossier / "b.md").write_text("b", encoding="utf-8")
    (dossier / "a.md").write_text("a", encoding="utf-8")
    (dossier / "c.txt").write_text("c", encoding="utf-8")
    (dossier / "d.PNG.md").write_text("d", encoding="utf-8")

    documents, avertissements = resoudre_lot([dossier])
    assert [f.name for f in documents] == ["a.md", "b.md", "d.PNG.md"]
    assert avertissements == [], "les non-.md sont ignorés sans message"


def test_dossier_tri_alphabetique(tmp_path) -> None:
    dossier = tmp_path / "corpus"
    dossier.mkdir()
    for nom in ["z.md", "m.md", "a.md"]:
        (dossier / nom).write_text(nom, encoding="utf-8")

    documents, _ = resoudre_lot([dossier])
    assert [f.name for f in documents] == ["a.md", "m.md", "z.md"]


def test_dossier_non_recursif(tmp_path) -> None:
    """FR-002 : premier niveau uniquement ; les sous-dossiers ne sont
    jamais descendus (Out of Scope de la spec 007)."""
    dossier = tmp_path / "corpus"
    sous = dossier / "sous"
    sous.mkdir(parents=True)
    (sous / "profond.md").write_text("p", encoding="utf-8")

    documents, avertissements = resoudre_lot([dossier])
    assert documents == []
    assert len(avertissements) == 1


def test_dossier_sans_md_averti(tmp_path) -> None:
    """FR-008 : dossier sans .md -> message d'entrée ignorée explicite."""
    dossier = tmp_path / "vide"
    dossier.mkdir()

    documents, avertissements = resoudre_lot([dossier])
    assert documents == []
    assert len(avertissements) == 1
    assert str(dossier) in avertissements[0]
    assert "entrée ignorée" in avertissements[0]


def test_melange_fichier_dossier_ordre_apparition(tmp_path) -> None:
    seul = tmp_path / "seul.md"
    seul.write_text("s", encoding="utf-8")
    dossier = tmp_path / "corpus"
    dossier.mkdir()
    (dossier / "dans.md").write_text("d", encoding="utf-8")

    documents, _ = resoudre_lot([seul, dossier])
    assert [f.name for f in documents] == ["seul.md", "dans.md"]


def test_suffixe_md_insensible_a_la_casse(tmp_path) -> None:
    dossier = tmp_path / "corpus"
    dossier.mkdir()
    (dossier / "HISTOIRE.MD").write_text("h", encoding="utf-8")

    documents, _ = resoudre_lot([dossier])
    assert [f.name for f in documents] == ["HISTOIRE.MD"]


def test_types_normalises_en_path(tmp_path) -> None:
    documents, _ = resoudre_lot([tmp_path / "a.md"])
    assert all(isinstance(d, Path) for d in documents)
