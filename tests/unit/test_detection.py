"""Tests unitaires de détection (T013) : fusion, seuil, ids stables (FR-002, FR-005, D3)."""

from md_cleaner.detection import detecter
from md_cleaner.normalisation import normaliser_ligne
from md_cleaner.segmentation import Page

NAV = ["Aller au contenu", "[CORSEN](</fr/>)", "[Insights](</fr/insights/>)"]


def _pages(contenus: list[list[str]]) -> list[Page]:
    return [Page(i + 1, None, lignes) for i, lignes in enumerate(contenus)]


MOTS = [
    "alpha",
    "bravo",
    "charlie",
    "delta",
    "echo",
    "fox-trot",
    "golf",
    "hotel",
    "india",
    "juliett",
]


def test_motif_supprime_au_dessus_du_seuil() -> None:
    contenus = [f"Contenu propre a la page {MOTS[i]}" for i in range(5)]
    pages = _pages([NAV + [contenus[i]] for i in range(5)])
    motifs = detecter(pages)
    cible = [normaliser_ligne(l) for l in NAV]
    trouves = [m for m in motifs if m.lignes_norm == cible]
    assert len(trouves) == 1
    assert trouves[0].action == "supprimer"
    assert trouves[0].frequence == 1.0
    assert trouves[0].pages == [1, 2, 3, 4, 5]


def test_sous_le_seuil_conserve() -> None:
    contenus = []
    for i in range(10):
        page = [f"Contenu unique mot {MOTS[i]}"]
        if i in (0, 1):
            page = NAV + page
        contenus.append(page)
    motifs = detecter(_pages(contenus))
    cible = [normaliser_ligne(l) for l in NAV]
    trouves = [m for m in motifs if m.lignes_norm == cible]
    assert len(trouves) == 1
    assert trouves[0].action == "conserver"
    assert trouves[0].frequence == 0.2


def test_plancher_frequence() -> None:
    """Un motif vu sur moins de 20 % des pages n'entre pas dans la suggestion."""
    contenus = []
    for i in range(10):
        page = [f"Contenu unique {i}"]
        if i == 0:
            page = NAV + page
        contenus.append(page)
    motifs = detecter(_pages(contenus))
    cible = [normaliser_ligne(l) for l in NAV]
    assert not [m for m in motifs if m.lignes_norm == cible]


def test_page_unique_aucun_motif() -> None:
    assert detecter(_pages([NAV + ["Contenu"]])) == []


def test_partie_variable_reconnue() -> None:
    contenus = [
        NAV + [f"[Lecon {i}](</fr/formations/le-chat-mcp/{i}/>)", f"Corps {i}"]
        for i in range(1, 6)
    ]
    motifs = detecter(_pages(contenus))
    assert any(m.frequence == 1.0 and m.nb_lignes >= 4 for m in motifs)


def test_fusion_des_fenetres() -> None:
    nav = [f"Ligne de navigation {i} du menu" for i in range(20)]
    pages = _pages([nav + [f"Contenu propre a {mot}"] for mot in MOTS[:3]])
    motifs = detecter(pages)
    supprimes = [m for m in motifs if m.action == "supprimer" and m.frequence == 1.0]
    assert len(supprimes) == 1
    assert supprimes[0].nb_lignes == 20


def test_ids_stables() -> None:
    pages = _pages([NAV + [f"Contenu {i}"] for i in range(4)])
    premier = [(m.id, m.extrait) for m in detecter(pages)]
    second = [(m.id, m.extrait) for m in detecter(pages)]
    assert premier == second


def test_seuil_reglable() -> None:
    contenus = []
    for i in range(10):
        page = [f"Contenu unique mot {MOTS[i]}"]
        if i < 8:
            page = NAV + page
        contenus.append(page)
    pages = _pages(contenus)
    assert detecter(pages, seuil=80)[0].action == "supprimer"
    assert detecter(pages, seuil=95)[0].action == "conserver"


# --- Feature 002 : frontière majoritaire stricte (FR-001, T001) ---

NAV = ["NAV_A", "NAV_B"]
MID = ["MID_1", "MID_2"]


def _pages_frontiere(placement_adjacent: list[int]) -> list:
    """4 pages : NAV et MID récurrents sur toutes les pages.

    Sur les pages listées dans placement_adjacent, MID colle à NAV
    (intervalles touchants = chevauchement) ; sur les autres, MID est
    séparé de NAV par du contenu unique (aucun chevauchement)."""
    pages: list[list[str]] = []
    noms = ["alpha", "bravo", "charlie", "delta", "echo", "fox-trot"]
    for numero in range(1, 5):
        if numero in placement_adjacent:
            pages.append(NAV + MID + [f"contenu propre {noms[numero]}"])
        else:
            pages.append(
                MID
                + [f"texte seul {noms[numero]}"]
                + NAV
                + [f"suite {noms[numero + 1]}"]
            )
    return _pages(pages)


def _norm(lignes: list[str]) -> list[str]:
    return [normaliser_ligne(ligne) for ligne in lignes]


def test_frontiere_moitie_exacte_pas_de_fusion() -> None:
    """FR-001 : chevauchement sur exactement la moitié des pages de la
    candidate → refus de fusion : deux motifs distincts là où l'ancienne
    règle (≥ 1 page) n'en produisait qu'un seul."""
    motifs = detecter(_pages_frontiere([1, 2]))
    assert len(motifs) == 2, (
        "à la moitié exacte des pages chevauchantes, la candidate MID doit "
        "former son propre bloc (2 motifs), pas fusionner avec NAV"
    )
    pages_motifs = {tuple(m.pages) for m in motifs}
    assert pages_motifs == {(1, 2, 3, 4)}


def test_plus_de_la_moitie_fusion() -> None:
    """FR-001 : chevauchement sur strictement plus de la moitié → fusion."""
    motifs = detecter(_pages_frontiere([1, 2, 3]))
    touches = [
        m for m in motifs if m.lignes_norm and m.lignes_norm[0] in _norm(NAV + MID)
    ]
    assert len(touches) == 1, (
        "à 3 pages chevauchantes sur 4, NAV et MID fusionnent en un seul motif"
    )
    assert touches[0].pages == [1, 2, 3, 4]
