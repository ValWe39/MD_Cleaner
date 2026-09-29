"""Tests d'intégration feature 002 : décidabilité des motifs (T002, T003).

SC-001 : séparation filtres / métadonnées sur Exemple_2.
SC-002 : non-régression Exemple_1 (motifs identiques à la version précédente).
SC-003 : au plus 5 motifs supprimer sur le corpus.
SC-005 : déterminisme octet par octet.
"""

import json
from pathlib import Path

from md_cleaner.cli import CODE_OK, main
from md_cleaner.detection import detecter
from md_cleaner.segmentation import segmenter

RACINE = Path(__file__).parents[2]
EXEMPLE_1 = RACINE / "Examples" / "Exemple_1" / "2.Input" / "consolidated.md"
EXEMPLE_2 = RACINE / "Examples" / "Exemple_2" / "2.Input" / "consolidated.md"

# Références de la version précédente (mesurées avant la feature 002)
EMPLACEMENTS_EX1_P1 = [(0, 54), (55, 58), (113, 116), (125, 136)]


def _detecter(entree: Path):
    pages, _mode = segmenter(entree.read_text(encoding="utf-8").splitlines())
    return detecter(pages), pages


def _motif_couvrant(motifs, page_numero: int, index: int):
    """Le premier motif dont un emplacement couvre la ligne index de la page."""
    for motif in motifs:
        for debut, fin in motif.emplacements.get(page_numero, []):
            if debut <= index < fin:
                return motif
    return None


def test_separation_filtres_et_metadata() -> None:
    """SC-001 : la zone filtres et les métadonnées de publications
    appartiennent à des motifs distincts sur Exemple_2."""
    motifs, pages = _detecter(EXEMPLE_2)
    p1 = pages[0].lignes
    index_titre = next(
        i for i, ligne in enumerate(p1) if ligne.strip().startswith("* ## [")
    )
    index_meta = next(
        i for i in range(index_titre, len(p1)) if p1[i].strip() == "COUR DES COMPTES"
    )
    index_filtres = next(
        i for i, ligne in enumerate(p1) if ligne.strip() == "## Filtres actifs"
    )
    motif_meta = _motif_couvrant(motifs, 1, index_meta)
    motif_filtres = _motif_couvrant(motifs, 1, index_filtres)
    assert motif_meta is not None, "les métadonnées doivent être couvertes"
    assert motif_filtres is not None, "la zone filtres doit être couverte"
    assert motif_meta.id != motif_filtres.id, (
        "filtres et métadonnées ne doivent pas être soudés dans un seul motif"
    )


def test_au_plus_cinq_motifs_supprimer() -> None:
    """SC-003, FR-005 : au plus 5 motifs proposés à supprimer."""
    motifs, _ = _detecter(EXEMPLE_2)
    supprimer = [m for m in motifs if m.action == "supprimer"]
    assert 1 <= len(supprimer) <= 5
    motifs1, _ = _detecter(EXEMPLE_1)
    assert len([m for m in motifs1 if m.action == "supprimer"]) <= 5


def test_bascule_ciblee_filtres_supprimes_metadata_conservees(tmp_path) -> None:
    """US1 scénario 2 : « supprimer l'interface, garder les métadonnées »
    devient exprimable en n'éditant que les actions."""
    code = main([str(EXEMPLE_2), "--dry-run", "--sortie", str(tmp_path / "dry")])
    assert code == CODE_OK
    suggestion = json.loads(
        (tmp_path / "dry" / "001" / "suggestion.json").read_text(encoding="utf-8")
    )
    motifs, pages = _detecter(EXEMPLE_2)
    p1 = pages[0].lignes
    index_titre = next(
        i for i, ligne in enumerate(p1) if ligne.strip().startswith("* ## [")
    )
    index_meta = next(
        i for i in range(index_titre, len(p1)) if p1[i].strip() == "COUR DES COMPTES"
    )
    motif_meta = _motif_couvrant(motifs, 1, index_meta)
    for motif in suggestion["motifs"]:
        motif["action"] = (
            "conserver" if motif["id"] == motif_meta.id else motif["action"]
        )
    chemin = tmp_path / "suggestion-editee.json"
    chemin.write_text(
        json.dumps(suggestion, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    code = main(
        [str(EXEMPLE_2), "--suggestion", str(chemin), "--sortie", str(tmp_path / "net")]
    )
    assert code == CODE_OK
    nettoye = (tmp_path / "net" / "001" / "nettoye.md").read_text(encoding="utf-8")
    assert "Filtres actifs" not in nettoye, "les filtres doivent être supprimés"
    assert "COUR DES COMPTES" in nettoye, (
        "le marqueur d'institution des publications doit être conservé"
    )


def test_non_regression_exemple_1() -> None:
    """SC-002, FR-003 : les motifs d'Exemple_1 sont identiques à la
    version précédente (ids, zones, actions)."""
    motifs, _ = _detecter(EXEMPLE_1)
    assert [(m.id, m.action, m.emplacements[1]) for m in motifs] == [
        ("M01", "supprimer", [EMPLACEMENTS_EX1_P1[0]]),
        ("M02", "supprimer", [EMPLACEMENTS_EX1_P1[1]]),
        ("M03", "supprimer", [EMPLACEMENTS_EX1_P1[2]]),
        ("M04", "supprimer", [EMPLACEMENTS_EX1_P1[3]]),
    ]


def test_determinisme_octet_par_octet(tmp_path) -> None:
    """SC-005 : deux dry-run identiques produisent des suggestion.json
    identiques octet par octet (contenu sans chemin embarqué)."""
    main([str(EXEMPLE_2), "--dry-run", "--sortie", str(tmp_path / "run1")])
    main([str(EXEMPLE_2), "--dry-run", "--sortie", str(tmp_path / "run2")])
    premier = (tmp_path / "run1" / "001" / "suggestion.json").read_bytes()
    second = (tmp_path / "run2" / "001" / "suggestion.json").read_bytes()
    assert premier == second
