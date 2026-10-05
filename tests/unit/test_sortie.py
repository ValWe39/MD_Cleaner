"""Tests unitaires de sortie (T002) : résolution de collision du nom nettoyé.

Feature 006 (D4, FR-004, SC-003) : le suffixe de collision est ajouté à la
fin du nom, avant l'extension (clarification du 2026-10-05) ; jamais
d'écrasement d'un fichier existant.
"""

from pathlib import Path

from md_cleaner.sortie import resoudre_chemin_nettoye


def test_nom_libre_sans_collision(tmp_path: Path) -> None:
    """Dossier vide → nom dérivé tel quel (FR-004)."""
    chemin = resoudre_chemin_nettoye(tmp_path, "retry-failed-records-nettoye")
    assert chemin == tmp_path / "retry-failed-records-nettoye.md"


def test_premiere_collision_suffixe_1(tmp_path: Path) -> None:
    """Premier conflit → -1, à la fin du nom avant .md (FR-004)."""
    (tmp_path / "retry-failed-records-nettoye.md").write_text(
        "existant", encoding="utf-8"
    )
    chemin = resoudre_chemin_nettoye(tmp_path, "retry-failed-records-nettoye")
    assert chemin == tmp_path / "retry-failed-records-nettoye-1.md"


def test_collisions_successives(tmp_path: Path) -> None:
    """Deuxième conflit → -2, par ordre de traitement (FR-004)."""
    (tmp_path / "x-nettoye.md").write_text("a", encoding="utf-8")
    (tmp_path / "x-nettoye-1.md").write_text("b", encoding="utf-8")
    chemin = resoudre_chemin_nettoye(tmp_path, "x-nettoye")
    assert chemin == tmp_path / "x-nettoye-2.md"


def test_fichiers_existants_intacts(tmp_path: Path) -> None:
    """SC-003 : la résolution ne modifie ni ne supprime aucun existant."""
    (tmp_path / "x-nettoye.md").write_text("contenu initial", encoding="utf-8")
    resoudre_chemin_nettoye(tmp_path, "x-nettoye")
    assert (tmp_path / "x-nettoye.md").read_text(encoding="utf-8") == (
        "contenu initial"
    )
