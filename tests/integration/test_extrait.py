"""Tests d'intégration feature 003 : extrait lisible et position (T003).

CLI --extrait (bornes, effet, no-op hors dry-run) et critères de corpus :
SC-001 (doublons), SC-002 (N exact), SC-003 (position réelle),
SC-004 (taille), SC-005 (déterminisme).
"""

import json
from collections import Counter
from pathlib import Path

from md_cleaner.cli import CODE_OK, CODE_USAGE, main
from md_cleaner.detection import detecter
from md_cleaner.segmentation import segmenter

RACINE = Path(__file__).parents[2]
EXEMPLE_1 = RACINE / "Examples" / "Exemple_1" / "2.Input" / "consolidated.md"
EXEMPLE_2 = RACINE / "Examples" / "Exemple_2" / "2.Input" / "consolidated.md"


def _suggestion_depuis_run(tmp_path, dossier: str) -> dict:
    return json.loads(
        (tmp_path / dossier / "001" / "suggestion.json").read_text(encoding="utf-8")
    )


def test_extrait_option_hors_bornes(tmp_path) -> None:
    """FR-003 : --extrait 1 et --extrait 40 → code retour 3."""
    assert (
        main([str(EXEMPLE_1), "--dry-run", "--extrait", "1", "--sortie", str(tmp_path)])
        == CODE_USAGE
    )
    assert (
        main(
            [str(EXEMPLE_1), "--dry-run", "--extrait", "40", "--sortie", str(tmp_path)]
        )
        == CODE_USAGE
    )


def test_extrait_sans_dry_run_sans_effet(tmp_path) -> None:
    """Clarification 2026-09-29 (Option A) : --extrait sans --dry-run
    → code 0, aucune suggestion générée, nettoyage normal."""
    code = main([str(EXEMPLE_1), "--extrait", "12", "--sortie", str(tmp_path)])
    assert code == CODE_OK
    assert not list(tmp_path.rglob("suggestion.json"))
    assert (tmp_path / "001" / "nettoye.md").is_file()


def test_extrait_n_exact(tmp_path) -> None:
    """SC-002 : N demandé → exactement N lignes pour les motifs à
    intervalle suffisant."""
    for n in (2, 12):
        main(
            [
                str(EXEMPLE_2),
                "--dry-run",
                "--extrait",
                str(n),
                "--sortie",
                str(tmp_path / f"n{n}"),
            ]
        )
        suggestion = _suggestion_depuis_run(tmp_path, f"n{n}")
        longs = [m for m in suggestion["motifs"] if m["nb_lignes"] >= n]
        assert longs, "des motifs à intervalle suffisant sont attendus"
        for motif in longs:
            assert len(motif["extrait"].split("\n")) == n


def test_doublons_extrait_au_plus_deux(tmp_path) -> None:
    """SC-001 : à la valeur par défaut, au plus 2 motifs partagent le
    même extrait sur Exemple_2 (baseline : 12 en doublon à 3 lignes)."""
    main([str(EXEMPLE_2), "--dry-run", "--sortie", str(tmp_path)])
    suggestion = json.loads(
        (tmp_path / "001" / "suggestion.json").read_text(encoding="utf-8")
    )
    extraits = [m["extrait"] for m in suggestion["motifs"]]
    en_doublon = sum(n for e, n in Counter(extraits).items() if n > 1)
    assert en_doublon <= 2


def test_position_couvre_ligne_reelle(tmp_path) -> None:
    """SC-003 : pour chaque motif, la ligne position.debut de la page
    position.page est couverte par une occurrence réelle du motif."""
    main([str(EXEMPLE_2), "--dry-run", "--sortie", str(tmp_path)])
    suggestion = json.loads(
        (tmp_path / "001" / "suggestion.json").read_text(encoding="utf-8")
    )
    pages, _mode = segmenter(EXEMPLE_2.read_text(encoding="utf-8").splitlines())
    motifs = detecter(pages, pages_calibrage=pages[:5])
    par_id = {m.id: m for m in motifs}
    numero_vs_index = {p.numero: i for i, p in enumerate(pages)}
    for motif in suggestion["motifs"]:
        position = motif["position"]
        detecte = par_id[motif["id"]]
        debut, fin = position["debut"], position["fin"]
        couvert = any(
            d <= debut < f for d, f in detecte.emplacements.get(position["page"], [])
        )
        assert couvert, (
            f"{motif['id']} : ligne {debut} non couverte en page {position['page']}"
        )
        assert numero_vs_index[position["page"]] >= 0
        page = pages[numero_vs_index[position["page"]]]
        assert page.lignes[debut] == motif["extrait"].split("\n")[0]
        assert fin > debut


def test_taille_sous_1_mo_a_la_borne(tmp_path) -> None:
    """SC-004 : suggestion.json < 1 Mo sur le corpus à N = 25."""
    main([str(EXEMPLE_2), "--dry-run", "--extrait", "25", "--sortie", str(tmp_path)])
    taille = (tmp_path / "001" / "suggestion.json").stat().st_size
    assert taille < 1024 * 1024


def test_determinisme_octet_par_octet(tmp_path) -> None:
    """SC-005 : deux dry-run identiques → suggestion.json identiques."""
    main(
        [
            str(EXEMPLE_2),
            "--dry-run",
            "--extrait",
            "12",
            "--sortie",
            str(tmp_path / "r1"),
        ]
    )
    main(
        [
            str(EXEMPLE_2),
            "--dry-run",
            "--extrait",
            "12",
            "--sortie",
            str(tmp_path / "r2"),
        ]
    )
    premier = (tmp_path / "r1" / "001" / "suggestion.json").read_bytes()
    second = (tmp_path / "r2" / "001" / "suggestion.json").read_bytes()
    assert premier == second


def test_rapport_sans_saut_de_ligne_dans_les_cellules(tmp_path) -> None:
    """SC-006, FR-004 : les cellules du tableau du rapport neutralisent
    les sauts de ligne de l'extrait (la rangée markdown reste intacte)."""
    main([str(EXEMPLE_2), "--dry-run", "--sortie", str(tmp_path)])
    rapport = (tmp_path / "001" / "rapport-dry-run.md").read_text(encoding="utf-8")
    cellules = [ligne for ligne in rapport.splitlines() if ligne.startswith("| M")]
    assert cellules, "le tableau des décisions requises doit être peuplé"
    for cellule in cellules:
        assert "\n" not in cellule
        assert len(cellule) <= 400  # troncature à 120 caractères de l'extrait respectée


def test_suggestion_sans_position_consommable(tmp_path) -> None:
    """FR-005, quickstart Scénario 5 : une suggestion d'avant-feature
    (sans champ position) se consomme avec le code 0."""
    main([str(EXEMPLE_2), "--dry-run", "--sortie", str(tmp_path / "dry")])
    suggestion = _suggestion_depuis_run(tmp_path, "dry")
    for motif in suggestion["motifs"]:
        motif.pop("position", None)  # simule une suggestion d'avant-feature
    chemin = tmp_path / "suggestion-ancienne.json"
    chemin.write_text(
        json.dumps(suggestion, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    code = main(
        [str(EXEMPLE_2), "--suggestion", str(chemin), "--sortie", str(tmp_path / "net")]
    )
    assert code == CODE_OK
    assert (tmp_path / "net" / "001" / "nettoye.md").is_file()
