"""Tests d'intégration feature 007 : invocation multi-entrées (US1-US4).

US1 (T003) : lot de fichiers listés — FR-001, FR-003, FR-004, FR-005,
SC-002 (parité), SC-005 (rétrocompatibilité mono-document).
"""

from pathlib import Path

from md_cleaner.cli import CODE_ENTREE, CODE_OK, main

RACINE = Path(__file__).parents[2]
ENTREES = [
    RACINE / "Examples" / "Exemple_1" / "2.Input" / "consolidated.md",
    RACINE / "Examples" / "Exemple_2" / "2.Input" / "consolidated.md",
    RACINE / "Examples" / "Exemple_3" / "2.Input" / "retry-failed-records.md",
]


def _petit_doc(titre: str) -> str:
    """Document multi-pages minimal : 4 pages, un motif répété (menu)."""
    lignes: list[str] = []
    for n in range(1, 5):
        lignes.append(f"## Page {n}: https://exemple.test/{titre}/{n}")
        lignes.append(f"# {titre}")
        lignes.append("Menu | Accueil | Contact")
        lignes.append(f"Contenu unique {titre} page {n}")
    return "\n".join(lignes) + "\n"


def test_lot_de_trois_fichiers(tmp_path) -> None:
    """N documents -> N dossiers de run, un par document, code 0."""
    code = main([str(e) for e in ENTREES] + ["--sortie", str(tmp_path)])
    assert code == CODE_OK
    assert (tmp_path / "001" / "consolidated-nettoye.md").is_file()
    assert (tmp_path / "002" / "consolidated-nettoye.md").is_file()
    assert (tmp_path / "003" / "retry-failed-records-nettoye.md").is_file()


def test_parite_lot_individuel(tmp_path) -> None:
    """SC-002 : chaque sortie du lot est identique octet par octet à la
    sortie obtenue en invoquant le document seul avec les mêmes options."""
    for entree in ENTREES:
        assert main([str(entree), "--sortie", str(tmp_path / "indiv")]) == CODE_OK
    assert (
        main([str(e) for e in ENTREES] + ["--sortie", str(tmp_path / "lot")]) == CODE_OK
    )
    attendus = [
        "consolidated-nettoye.md",
        "consolidated-nettoye.md",
        "retry-failed-records-nettoye.md",
    ]
    for numero, attendu in enumerate(attendus, start=1):
        individuel = (tmp_path / "indiv" / f"{numero:03d}" / attendu).read_bytes()
        en_lot = (tmp_path / "lot" / f"{numero:03d}" / attendu).read_bytes()
        assert individuel == en_lot, f"parité rompue pour {attendu} (run {numero})"


def test_ordre_d_apparition(tmp_path) -> None:
    """FR-004 : les documents sont traités dans l'ordre des arguments."""
    doc_a = tmp_path / "aaa.md"
    doc_b = tmp_path / "bbb.md"
    doc_a.write_text(_petit_doc("Alpha"), encoding="utf-8")
    doc_b.write_text(_petit_doc("Beta"), encoding="utf-8")

    assert main([str(doc_a), str(doc_b), "--sortie", str(tmp_path / "sorties")]) == (
        CODE_OK
    )
    assert (tmp_path / "sorties" / "001" / "aaa-nettoye.md").is_file()
    assert (tmp_path / "sorties" / "002" / "bbb-nettoye.md").is_file()

    assert main([str(doc_b), str(doc_a), "--sortie", str(tmp_path / "inverse")]) == (
        CODE_OK
    )
    assert (tmp_path / "inverse" / "001" / "bbb-nettoye.md").is_file()
    assert (tmp_path / "inverse" / "002" / "aaa-nettoye.md").is_file()


def test_doublon_traite_deux_fois_sans_ecrasement(tmp_path) -> None:
    """FR-010 : chaque occurrence est traitée ; collision suffixée -1."""
    doc = tmp_path / "doc.md"
    doc.write_text(_petit_doc("Gamma"), encoding="utf-8")

    assert main([str(doc), str(doc), "--sortie", str(tmp_path / "sorties")]) == CODE_OK
    premiere = tmp_path / "sorties" / "001" / "doc-nettoye.md"
    seconde = tmp_path / "sorties" / "002" / "doc-nettoye.md"
    assert premiere.is_file()
    assert seconde.is_file()
    assert premiere.read_bytes() == seconde.read_bytes()


def test_mono_document_inchange(tmp_path) -> None:
    """SC-005 : une seule entrée positionnelle se comporte comme avant."""
    doc = tmp_path / "solo.md"
    doc.write_text(_petit_doc("Solo"), encoding="utf-8")
    assert main([str(doc), "--sortie", str(tmp_path)]) == CODE_OK
    assert (tmp_path / "001" / "solo-nettoye.md").is_file()


def test_zero_argument_usage_invalide(tmp_path) -> None:
    """FR-001 : aucune entrée reste un usage invalide (code 3)."""
    import pytest

    with pytest.raises(SystemExit) as sortie:
        main([])
    assert sortie.value.code == 3


# --- US2 (T007) : dossier en entrée (FR-002, FR-008) ---


def test_dossier_seuls_les_md_premier_niveau(tmp_path, capsys) -> None:
    """FR-002 : seuls les .md du premier niveau, triés par nom ; les
    autres fichiers sont ignorés sans message ; les sous-dossiers ne
    sont pas descendus."""
    dossier = tmp_path / "corpus"
    dossier.mkdir()
    (dossier / "b-histoire.md").write_text(_petit_doc("Histoire"), encoding="utf-8")
    (dossier / "a-intro.md").write_text(_petit_doc("Intro"), encoding="utf-8")
    (dossier / "ignore.txt").write_text("pas du markdown", encoding="utf-8")
    sous = dossier / "sous-dossier"
    sous.mkdir()
    (sous / "c-cache.md").write_text(_petit_doc("Cache"), encoding="utf-8")

    assert main([str(dossier), "--sortie", str(tmp_path / "sorties")]) == CODE_OK
    assert (tmp_path / "sorties" / "001" / "a-intro-nettoye.md").is_file()
    assert (tmp_path / "sorties" / "002" / "b-histoire-nettoye.md").is_file()
    sorties = list((tmp_path / "sorties").iterdir())
    assert len(sorties) == 2, "les non-.md et sous-dossiers ne sont pas traités"
    capturées = capsys.readouterr()
    assert "entrée ignorée" not in capturées.err + capturées.out


def test_melange_fichier_et_dossier(tmp_path) -> None:
    """FR-001 : union des fichiers listés et des .md du dossier, dans
    l'ordre d'apparition."""
    seul = tmp_path / "seul.md"
    seul.write_text(_petit_doc("Seul"), encoding="utf-8")
    dossier = tmp_path / "corpus"
    dossier.mkdir()
    (dossier / "dans.md").write_text(_petit_doc("Dans"), encoding="utf-8")

    code = main([str(seul), str(dossier), "--sortie", str(tmp_path / "sorties")])
    assert code == CODE_OK
    assert (tmp_path / "sorties" / "001" / "seul-nettoye.md").is_file()
    assert (tmp_path / "sorties" / "002" / "dans-nettoye.md").is_file()


def test_dossier_sans_md_seul_erreur_1(tmp_path, capsys) -> None:
    """FR-008 : dossier sans .md -> entrée ignorée avec message ; lot
    vide -> erreur d'entrée code 1, aucun traitement."""
    dossier = tmp_path / "vide-de-md"
    dossier.mkdir()
    (dossier / "note.txt").write_text("rien", encoding="utf-8")

    assert main([str(dossier), "--sortie", str(tmp_path / "sorties")]) == CODE_ENTREE
    assert not (tmp_path / "sorties").exists() or not list(
        (tmp_path / "sorties").iterdir()
    )
    capturées = capsys.readouterr()
    assert "entrée ignorée" in capturées.err
    assert str(dossier) in capturées.err


def test_dossier_sans_md_en_lot_mixte(tmp_path, capsys) -> None:
    """FR-008 : entrée ignorée avec message, le reste du lot est traité."""
    doc = tmp_path / "valide.md"
    doc.write_text(_petit_doc("Valide"), encoding="utf-8")
    dossier = tmp_path / "que-des-sous-dossiers"
    (dossier / "enfant").mkdir(parents=True)

    code = main([str(doc), str(dossier), "--sortie", str(tmp_path / "sorties")])
    assert code == CODE_OK
    assert (tmp_path / "sorties" / "001" / "valide-nettoye.md").is_file()
    capturées = capsys.readouterr()
    assert "entrée ignorée" in capturées.err


# --- US3 (T010) : options non applicables en lot (FR-006, SC-004) ---


def test_dry_run_neutralisee_en_lot(tmp_path, capsys) -> None:
    """FR-006 : --dry-run en lot de 2 -> avertissement explicite, option
    neutralisée, lot traité en nettoyage complet (aucun artefact dry-run)."""
    doc_a = tmp_path / "a.md"
    doc_b = tmp_path / "b.md"
    doc_a.write_text(_petit_doc("Alpha"), encoding="utf-8")
    doc_b.write_text(_petit_doc("Beta"), encoding="utf-8")

    code = main([str(doc_a), str(doc_b), "--dry-run", "--sortie", str(tmp_path / "s")])
    assert code == CODE_OK
    assert (tmp_path / "s" / "001" / "a-nettoye.md").is_file()
    assert (tmp_path / "s" / "002" / "b-nettoye.md").is_file()
    assert not (tmp_path / "s" / "001" / "rapport-dry-run.md").exists()
    assert not (tmp_path / "s" / "001" / "suggestion.json").exists()
    capturées = capsys.readouterr()
    assert "AVERTISSEMENT" in capturées.err
    assert "--dry-run ignorée en lot" in capturées.err


def test_suggestion_neutralisee_en_lot(tmp_path, capsys) -> None:
    """FR-006 : --suggestion en lot -> avertissement, suggestion
    neutralisée (re-calcul par document), lot nettoyé."""
    doc_a = tmp_path / "a.md"
    doc_b = tmp_path / "b.md"
    doc_a.write_text(_petit_doc("Alpha"), encoding="utf-8")
    doc_b.write_text(_petit_doc("Beta"), encoding="utf-8")
    suggestion = tmp_path / "suggestion.json"
    suggestion.write_text("{}", encoding="utf-8")

    code = main(
        [
            str(doc_a),
            str(doc_b),
            "--suggestion",
            str(suggestion),
            "--sortie",
            str(tmp_path / "s"),
        ]
    )
    assert code == CODE_OK
    assert (tmp_path / "s" / "001" / "a-nettoye.md").is_file()
    assert (tmp_path / "s" / "002" / "b-nettoye.md").is_file()
    capturées = capsys.readouterr()
    assert "--suggestion ignorée en lot" in capturées.err


def test_lot_d_un_seul_document_dry_run_fonctionnel(tmp_path) -> None:
    """FR-005 : un lot d'exactement un document garde le comportement
    actuel — dry-run et suggestion pleinement applicables."""
    doc = tmp_path / "solo.md"
    doc.write_text(_petit_doc("Solo"), encoding="utf-8")

    assert main([str(doc), "--dry-run", "--sortie", str(tmp_path / "s")]) == CODE_OK
    assert (tmp_path / "s" / "001" / "rapport-dry-run.md").is_file()
    assert (tmp_path / "s" / "001" / "suggestion.json").is_file()
    assert not (tmp_path / "s" / "001" / "solo-nettoye.md").exists()


def test_dossier_d_un_seul_md_dry_run_fonctionnel(tmp_path) -> None:
    """FR-005 : un dossier contenant un seul .md est un lot d'un
    document — le dry-run s'applique (US2 + US3 conjoints)."""
    dossier = tmp_path / "corpus"
    dossier.mkdir()
    (dossier / "unique.md").write_text(_petit_doc("Unique"), encoding="utf-8")

    assert main([str(dossier), "--dry-run", "--sortie", str(tmp_path / "s")]) == CODE_OK
    assert (tmp_path / "s" / "001" / "rapport-dry-run.md").is_file()
    assert (tmp_path / "s" / "001" / "suggestion.json").is_file()


# --- US4 (T012) : échecs en lot (FR-007) ---


def test_echec_isole_le_lot_poursuit(tmp_path, capsys) -> None:
    """FR-007 : un échec est signalé, le lot poursuit, les sorties des
    documents valides sont conservées, code 1."""
    doc_a = tmp_path / "a.md"
    doc_c = tmp_path / "c.md"
    doc_a.write_text(_petit_doc("Alpha"), encoding="utf-8")
    doc_c.write_text(_petit_doc("Gamma"), encoding="utf-8")
    absent = tmp_path / "absent.md"

    code = main([str(doc_a), str(absent), str(doc_c), "--sortie", str(tmp_path / "s")])
    assert code == CODE_ENTREE
    assert (tmp_path / "s" / "001" / "a-nettoye.md").is_file()
    assert (tmp_path / "s" / "002" / "c-nettoye.md").is_file()
    capturées = capsys.readouterr()
    assert f"ERREUR : {absent}" in capturées.err


def test_trois_echecs_consecutifs_arretent_le_lot(tmp_path, capsys) -> None:
    """FR-007 : au troisième échec consécutif, le lot s'arrête net —
    le document suivant n'est pas traité."""
    doc_valide = tmp_path / "valide.md"
    doc_valide.write_text(_petit_doc("Valide"), encoding="utf-8")
    absents = [tmp_path / f"absent{n}.md" for n in (1, 2, 3)]

    code = main(
        [str(a) for a in absents] + [str(doc_valide), "--sortie", str(tmp_path / "s")]
    )
    assert code == CODE_ENTREE
    assert not (tmp_path / "s").exists() or not list((tmp_path / "s").iterdir())
    capturées = capsys.readouterr()
    for absent in absents:
        assert f"ERREUR : {absent}" in capturées.err
    assert "valide" not in capturées.out


def test_echecs_non_consecutifs_lot_complet(tmp_path, capsys) -> None:
    """FR-007 : un succès remet le compteur d'échecs consécutifs à
    zéro ; deux échecs non consécutifs n'arrêtent pas le lot."""
    doc_b = tmp_path / "b.md"
    doc_b.write_text(_petit_doc("Beta"), encoding="utf-8")
    abs1 = tmp_path / "absent1.md"
    abs2 = tmp_path / "absent2.md"

    code = main([str(abs1), str(doc_b), str(abs2), "--sortie", str(tmp_path / "s")])
    assert code == CODE_ENTREE
    assert (tmp_path / "s" / "001" / "b-nettoye.md").is_file()
    capturées = capsys.readouterr()
    assert f"ERREUR : {abs1}" in capturées.err
    assert f"ERREUR : {abs2}" in capturées.err


def test_lot_entierement_invalide_aucune_sortie(tmp_path, capsys) -> None:
    """FR-007 : aucun document traitable -> aucune sortie, chaque échec
    signalé, code 1."""
    absents = [tmp_path / f"absent{n}.md" for n in (1, 2)]

    code = main([str(a) for a in absents] + ["--sortie", str(tmp_path / "s")])
    assert code == CODE_ENTREE
    assert not (tmp_path / "s").exists() or not list((tmp_path / "s").iterdir())
    capturées = capsys.readouterr()
    for absent in absents:
        assert f"ERREUR : {absent}" in capturées.err
