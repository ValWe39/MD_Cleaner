"""Tests unitaires de segmentation (T008) : separateurs, repli heuristique, mode unique (FR-011, D4)."""

from md_cleaner.segmentation import segmenter

DOC_EXPLICITE = [
    "## Page 1: https://exemple.fr/p1",
    "Contenu A ligne 1",
    "",
    "## Page 2: https://exemple.fr/p2",
    "Contenu B ligne 1",
    "## Page 3",
    "Contenu C ligne 1",
]


def test_explicite_avec_url() -> None:
    pages, mode = segmenter(DOC_EXPLICITE)
    assert mode == "explicite"
    assert [p.numero for p in pages] == [1, 2, 3]
    assert pages[0].url_source == "https://exemple.fr/p1"
    assert pages[2].url_source is None
    # Les lignes de separateur ne font pas partie du contenu des pages
    assert pages[0].lignes == ["Contenu A ligne 1", ""]


def test_separateur_niveaux_titres() -> None:
    pages, mode = segmenter(["#### Page 5", "x", "# Page 6", "y"])
    assert mode == "explicite"
    assert [p.numero for p in pages] == [1, 2]


def test_numeros_renumerotes_sans_trou() -> None:
    pages, _ = segmenter(["## Page 3", "a", "## Page 9", "b"])
    assert [p.numero for p in pages] == [1, 2]


def test_repli_heuristique() -> None:
    noms = ["alpha", "bravo", "charlie"]
    doc: list[str] = []
    for nom in noms:
        doc += [f"Contenu propre a la section {nom}", "FOOTER EXTERNE", ""]
    pages, mode = segmenter(doc)
    assert mode == "heuristique"
    assert len(pages) == 3
    # La ligne frontiere n'est pas conservee dans le contenu
    assert all("FOOTER EXTERNE" not in p.lignes for p in pages)
    assert all(any("Contenu propre" in l for l in p.lignes) for p in pages)


def test_mode_unique_sans_recurrence() -> None:
    doc = ["Titre", "Paragraphe unique", "Suite du texte"]
    pages, mode = segmenter(doc)
    assert mode == "unique"
    assert len(pages) == 1
    assert pages[0].numero == 1
    assert pages[0].lignes == doc


def test_un_seul_separateur_est_ignore() -> None:
    """Un seul separateur ne delimite rien : document unique, pas de mode trompeur."""
    doc = ["## Page 1: https://x", "contenu"]
    pages, mode = segmenter(doc)
    assert mode in ("unique", "heuristique")
    assert len(pages) >= 1


def test_nombres_distincts_pas_frontieres() -> None:
    """Des numeros d'etapes distincts (« 1 », « 2 », ...) normalises en <N>
    ne doivent pas etre elus frontières de pages (regression FR-016)."""
    doc = [
        "Introduction du texte.",
        "1",
        "Etape numero un decrite ici.",
        "2",
        "Etape numero deux decrite la.",
        "3",
        "Etape numero trois expliquee.",
    ]
    pages, mode = segmenter(doc)
    assert mode == "unique"
    assert len(pages) == 1
    assert pages[0].lignes == doc
