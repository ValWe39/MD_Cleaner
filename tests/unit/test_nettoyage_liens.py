"""Tests unitaires de la passe de retrait des destinations (T001).

FR-001, FR-006, D1, D3, D5 : règle bornée à ](</...>), premier > refermant,
sans décodage, libellés et crochets conservés, marqueurs de page non matchés,
idempotence.
"""

from md_cleaner.nettoyage import nettoyer_destinations


def test_destination_seule_retiree() -> None:
    """FR-001 : ](</...>) retiré, libellé et crochets conservés, reste intact."""
    lignes = [
        (
            "[Famille, handicap, sport et jeunesse"
            "](</publications?f%5B1%5D=thematic%3A17182>) -"
        )
    ]
    assert nettoyer_destinations(lignes) == ["[Famille, handicap, sport et jeunesse] -"]


def test_plusieurs_liens_sur_une_ligne() -> None:
    """US1 scénario 3 : toutes les occurrences sont retirées."""
    assert nettoyer_destinations(["[A](</a>) et [B](</b>)"]) == ["[A] et [B]"]


def test_libelle_vide() -> None:
    """Cas limite : destination retirée, crochets vides conservés."""
    assert nettoyer_destinations(["[](</chemin>)"]) == ["[]"]


def test_caracteres_encodes_non_decodes() -> None:
    """FR-006 : %5B / %3A retirés tels quels avec la destination."""
    assert nettoyer_destinations(["[X](</p?f%5B1%5D=thematic%3A17182>)"]) == ["[X]"]


def test_destination_absolue_intacte() -> None:
    """Hors périmètre : ](https://...) n'est pas retirée."""
    ligne = "[X](https://exemple.fr/page)"
    assert nettoyer_destinations([ligne]) == [ligne]


def test_destination_nue_intacte() -> None:
    """Hors périmètre : ](chemin) sans chevrons n'est pas retirée."""
    ligne = "[X](chemin/relatif)"
    assert nettoyer_destinations([ligne]) == [ligne]


def test_chevron_non_referme_intact() -> None:
    """Cas limite : ](</a>b>) (pas de >) juste après le premier >) inchangé."""
    ligne = "[X](</a>b>) suite"
    assert nettoyer_destinations([ligne]) == [ligne]


def test_marqueur_page_intact() -> None:
    """D5, FR-004 : <!-- page: N --> ne matche pas la règle."""
    for marqueur in ("<!-- page: 3 -->", "<!-- page: 12 -->"):
        assert nettoyer_destinations([marqueur]) == [marqueur]


def test_ligne_sans_lien_inchangee_octet_par_octet() -> None:
    """SC-002/SC-003 : sans ](</...>), la ligne est inchangée."""
    lignes = ["Titre sans lien", "", "  Texte indenté  avec  espaces  "]
    assert nettoyer_destinations(lignes) == lignes


def test_idempotence() -> None:
    """Deux passes = une passe : aucune ](</ restante après la première."""
    lignes = ["[A](</a>) et [B](</b?x%5B1%5D=y>) fin"]
    une = nettoyer_destinations(lignes)
    assert nettoyer_destinations(une) == une


def test_ligne_entierement_constituee_dun_lien_conservee() -> None:
    """Cas limite : la ligne reste présente, aucune ligne supprimée."""
    assert nettoyer_destinations(["[Libellé](</chemin>)"]) == ["[Libellé]"]
