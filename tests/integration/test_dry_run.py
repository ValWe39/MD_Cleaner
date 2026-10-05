"""Tests d'intégration US2 (T019) : dry-run et suggestion éditable (FR-007, FR-008, SC-004)."""

import json
from pathlib import Path

from md_cleaner.cli import CODE_ARTEFACT, CODE_OK, main

RACINE = Path(__file__).parents[2]
ENTREE = RACINE / "Examples" / "Exemple_1" / "2.Input" / "consolidated.md"


def test_dry_run_sans_nettoye(tmp_path) -> None:
    code = main([str(ENTREE), "--dry-run", "--sortie", str(tmp_path)])
    assert code == CODE_OK
    dossier = tmp_path / "001"
    assert (dossier / "rapport-dry-run.md").is_file()
    assert (dossier / "suggestion.json").is_file()
    assert not list(tmp_path.rglob("*-nettoye.md"))


def test_suggestion_conforme_au_contrat(tmp_path) -> None:
    main([str(ENTREE), "--dry-run", "--sortie", str(tmp_path)])
    suggestion = json.loads(
        (tmp_path / "001" / "suggestion.json").read_text(encoding="utf-8")
    )
    assert suggestion["version"] == 1
    assert suggestion["source"] == "consolidated.md"
    assert suggestion["seuil"] == 80
    assert suggestion["mode_segmentation"] == "explicite"
    assert suggestion["nb_pages"] == 14
    assert suggestion["motifs"], "au moins un motif attendu"
    for motif in suggestion["motifs"]:
        assert motif["id"].startswith("M")
        assert motif["action"] in {"supprimer", "conserver"}
        assert 0 <= motif["frequence"] <= 1
        assert motif["pages"] == sorted(motif["pages"])


def test_bascule_action_appliquee(tmp_path) -> None:
    """L'édition supprimer → conserver d'un motif est respectée au run suivant."""
    main([str(ENTREE), "--dry-run", "--sortie", str(tmp_path / "dry")])
    suggestion = json.loads(
        (tmp_path / "dry" / "001" / "suggestion.json").read_text(encoding="utf-8")
    )
    motif = next(m for m in suggestion["motifs"] if m["action"] == "supprimer")
    motif["action"] = "conserver"
    chemin_edité = tmp_path / "suggestion-editee.json"
    chemin_edité.write_text(
        json.dumps(suggestion, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    main([str(ENTREE), "--sortie", str(tmp_path / "defaut")])
    main(
        [
            str(ENTREE),
            "--suggestion",
            str(chemin_edité),
            "--sortie",
            str(tmp_path / "edite"),
        ]
    )
    defaut = (tmp_path / "defaut" / "001" / "consolidated-nettoye.md").read_text(
        encoding="utf-8"
    )
    edite = (tmp_path / "edite" / "001" / "consolidated-nettoye.md").read_text(
        encoding="utf-8"
    )
    premiere_ligne = next(
        morceau.strip() for morceau in motif["extrait"].split("\n") if morceau.strip()
    )
    assert premiere_ligne not in defaut
    assert premiere_ligne in edite


def test_id_inconnu_code_2(tmp_path) -> None:
    main([str(ENTREE), "--dry-run", "--sortie", str(tmp_path / "dry")])
    suggestion = json.loads(
        (tmp_path / "dry" / "001" / "suggestion.json").read_text(encoding="utf-8")
    )
    suggestion["motifs"].append(
        {
            "id": "M99",
            "action": "supprimer",
            "nb_lignes": 1,
            "frequence": 1.0,
            "pages": [1],
            "extrait": "ajouté à la main",
        }
    )
    chemin = tmp_path / "suggestion-m99.json"
    chemin.write_text(json.dumps(suggestion), encoding="utf-8")
    code = main([str(ENTREE), "--suggestion", str(chemin), "--sortie", str(tmp_path)])
    assert code == CODE_ARTEFACT


def test_dry_run_avec_suggestion_refuse(tmp_path) -> None:
    from md_cleaner.cli import CODE_USAGE

    code = main([str(ENTREE), "--dry-run", "--suggestion", "x.json"])
    assert code == CODE_USAGE


# --- Feature 002 : lisibilité du rapport (FR-004, SC-003, T005) ---


def test_rapport_exemple_1_sans_section_secondaire_superflue(tmp_path) -> None:
    """US2 scénario 3 : Exemple_1 (tous motifs supprimer) — la section
    secondaire affiche « aucun », pas de bruit."""
    main([str(ENTREE), "--dry-run", "--sortie", str(tmp_path)])
    rapport = (tmp_path / "001" / "rapport-dry-run.md").read_text(encoding="utf-8")
    assert "## Décisions requises" in rapport
    lignes_conservees = rapport.split("## Motifs conservés par défaut")[1]
    assert "aucun" in lignes_conservees.split("##")[0]


def test_rapport_exemple_2_decisions_bornees(tmp_path) -> None:
    """SC-003 : le tableau des décisions requises énumère au plus 5 motifs
    sur un document riche ; les conservés sont en section secondaire."""
    entree = RACINE / "Examples" / "Exemple_2" / "2.Input" / "consolidated.md"
    main([str(entree), "--dry-run", "--sortie", str(tmp_path)])
    rapport = (tmp_path / "001" / "rapport-dry-run.md").read_text(encoding="utf-8")
    tableau = rapport.split("## Motifs conservés par défaut")[0]
    lignes_decision = [
        ligne for ligne in tableau.splitlines() if ligne.startswith("| M")
    ]
    assert 1 <= len(lignes_decision) <= 5
    assert "## Motifs conservés par défaut" in rapport
