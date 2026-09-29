"""Tests unitaires de suggestion (T015) : validation stricte, code 2 (FR-008, D5)."""

import json

import pytest

from md_cleaner.detection import Motif
from md_cleaner.suggestion import (
    ErreurSuggestion,
    appliquer_actions,
    construire_suggestion,
    ecrire_suggestion,
    generer_rapport,
    lire_suggestion,
)


def _motif(**surcharges) -> Motif:
    valeurs = {
        "id": "M01",
        "action": "supprimer",
        "lignes_norm": ["a", "b"],
        "extrait": "a / b",
        "frequence": 1.0,
        "pages": [1, 2],
        "nb_lignes": 2,
        "emplacements": {1: (0, 2), 2: (0, 2)},
    }
    valeurs.update(surcharges)
    return Motif(**valeurs)


def _ecrire(tmp_path, donnees) -> object:
    chemin = tmp_path / "suggestion.json"
    chemin.write_text(json.dumps(donnees, ensure_ascii=False), encoding="utf-8")
    return chemin


def test_roundtrip(tmp_path) -> None:
    motifs = [_motif()]
    suggestion = construire_suggestion("doc.md", 80, "explicite", 3, motifs)
    ecrire_suggestion(tmp_path / "suggestion.json", suggestion)
    lue = lire_suggestion(tmp_path / "suggestion.json", "doc.md")
    assert lue == suggestion


def test_serialisation_deterministe(tmp_path) -> None:
    suggestion = construire_suggestion("doc.md", 80, "explicite", 3, [_motif()])
    ecrire_suggestion(tmp_path / "a.json", suggestion)
    ecrire_suggestion(tmp_path / "b.json", suggestion)
    assert (tmp_path / "a.json").read_bytes() == (tmp_path / "b.json").read_bytes()


def test_version_invalide(tmp_path) -> None:
    chemin = _ecrire(tmp_path, {"version": 2, "source": "doc.md", "motifs": []})
    with pytest.raises(ErreurSuggestion, match="version"):
        lire_suggestion(chemin, "doc.md")


def test_source_differente(tmp_path) -> None:
    chemin = _ecrire(
        tmp_path,
        {"version": 1, "source": "autre.md", "seuil": 80, "motifs": []},
    )
    with pytest.raises(ErreurSuggestion, match="source"):
        lire_suggestion(chemin, "doc.md")


def test_action_invalide(tmp_path) -> None:
    chemin = _ecrire(
        tmp_path,
        {
            "version": 1,
            "source": "doc.md",
            "seuil": 80,
            "mode_segmentation": "explicite",
            "nb_pages": 2,
            "motifs": [
                {
                    "id": "M01",
                    "action": "peut-etre",
                    "nb_lignes": 2,
                    "frequence": 1.0,
                    "pages": [1],
                    "extrait": "a",
                }
            ],
        },
    )
    with pytest.raises(ErreurSuggestion, match="action"):
        lire_suggestion(chemin, "doc.md")


def test_id_duplique(tmp_path) -> None:
    motif = {
        "id": "M01",
        "action": "supprimer",
        "nb_lignes": 2,
        "frequence": 1.0,
        "pages": [1],
        "extrait": "a",
    }
    chemin = _ecrire(
        tmp_path,
        {
            "version": 1,
            "source": "doc.md",
            "seuil": 80,
            "mode_segmentation": "explicite",
            "nb_pages": 2,
            "motifs": [motif, dict(motif)],
        },
    )
    with pytest.raises(ErreurSuggestion, match="dupliqu"):
        lire_suggestion(chemin, "doc.md")


def test_json_invalide(tmp_path) -> None:
    chemin = tmp_path / "suggestion.json"
    chemin.write_text("{ pas du json", encoding="utf-8")
    with pytest.raises(ErreurSuggestion, match="illisible"):
        lire_suggestion(chemin, "doc.md")


def test_appliquer_actions_bascule() -> None:
    motifs = [_motif(id="M01"), _motif(id="M02", action="conserver")]
    suggestion = {
        "motifs": [
            {"id": "M01", "action": "conserver"},
            {"id": "M02", "action": "supprimer"},
        ]
    }
    appliquer_actions(motifs, suggestion)
    assert motifs[0].action == "conserver"
    assert motifs[1].action == "supprimer"


def test_appliquer_actions_id_inconnu() -> None:
    motifs = [_motif(id="M01")]
    suggestion = {"motifs": [{"id": "M99", "action": "supprimer"}]}
    with pytest.raises(ErreurSuggestion, match="M99"):
        appliquer_actions(motifs, suggestion)


# --- Feature 002 : rapport en deux sections (FR-004, T004) ---


def _rapport(tmp_path, motifs: list) -> str:
    suggestion = {
        "version": 1,
        "source": "doc.md",
        "seuil": 80,
        "mode_segmentation": "explicite",
        "nb_pages": 4,
        "motifs": motifs,
    }
    generer_rapport(tmp_path / "rapport.md", suggestion, [])
    return (tmp_path / "rapport.md").read_text(encoding="utf-8")


def _motif_json(id: str, action: str) -> dict:
    return {
        "id": id,
        "action": action,
        "nb_lignes": 2,
        "frequence": 0.5,
        "pages": [1, 2],
        "extrait": "ligne extra",
    }


def test_rapport_deux_sections(tmp_path) -> None:
    """FR-004 : décisions requises (supprimer) séparées des motifs
    conservés par défaut, sans action requise."""
    texte = _rapport(
        tmp_path,
        [_motif_json("M01", "supprimer"), _motif_json("M02", "conserver")],
    )
    assert "## Décisions requises" in texte
    assert "| M01 | supprimer" in texte
    assert "## Motifs conservés par défaut — aucune action requise" in texte
    assert "- M02 (0.5) : ligne extra" in texte
    # Le motif conservé ne doit pas figurer dans le tableau des décisions
    tableau = texte.split("## Motifs conservés par défaut")[0]
    assert "M02 |" not in tableau


def test_rapport_sections_vides(tmp_path) -> None:
    """Contrat rapport : une section vide affiche « aucun »."""
    texte = _rapport(tmp_path, [])
    assert "## Décisions requises" in texte
    assert "## Motifs conservés par défaut — aucune action requise" in texte
    assert texte.count("aucun") >= 2
