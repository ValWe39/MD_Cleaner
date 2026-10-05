"""Tests unitaires de la passe de retrait des destinations (T001, T002).

FR-001, FR-002, FR-006, FR-007, D1, D2, D5 : règle unifiée ](<...>) sans
distinction de schéma (option A), titre retiré avec la destination,
premier > refermant, sans décodage, libellés et crochets conservés,
URLs nues et marqueurs de page non matchés, idempotence.
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


def test_https_avec_parametres_de_suivi_retiree() -> None:
    """FR-001 (T001) : [Try Studio ](<https://console...?utm_...>) → libellé seul."""
    ligne = (
        "[Try Studio ](<https://console.mistral.ai?utm_source=docs"
        "&utm_medium=header_cta&utm_campaign=studio_trial>)"
    )
    assert nettoyer_destinations([ligne]) == ["[Try Studio ]"]


def test_http_retire() -> None:
    """FR-001 (T001) : destination http entre chevrons retirée."""
    assert nettoyer_destinations(["[About us](<http://www.exemple.fr/a>)"]) == [
        "[About us]"
    ]


def test_mailto_et_tel_retires() -> None:
    """Clarification 2026-10-05 option A (T001) : tout schéma, même règle."""
    assert nettoyer_destinations(["[Contact](<mailto:contact@exemple.fr>)"]) == [
        "[Contact]"
    ]
    assert nettoyer_destinations(["[Tél](<tel:+33123456789>)"]) == ["[Tél]"]


def test_plusieurs_liens_absolus_sur_une_ligne() -> None:
    """US1 scénario 3 (T001) : chaque destination d'un pied de page est retirée."""
    ligne = (
        "[About us](<https://mistral.ai/about>)"
        "[Our customers](<https://mistral.ai/customers>)"
        "[Careers](<https://mistral.ai/careers>)"
    )
    assert nettoyer_destinations([ligne]) == ["[About us][Our customers][Careers]"]


def test_libelle_vide_absolu() -> None:
    """Cas limite (T001) : crochets vides conservés, destination retirée."""
    assert nettoyer_destinations(["[](<https://exemple.fr>)"]) == ["[]"]


def test_url_nue_dans_le_texte_intacte() -> None:
    """FR-007 (T001) : URL nue hors syntaxe de lien non touchée."""
    ligne = "voir https://docs.mistral.ai/api pour la suite"
    assert nettoyer_destinations([ligne]) == [ligne]


def test_titre_emporte_avec_la_destination() -> None:
    """FR-002 (T002) : destination et titre retirés, libellé seul conservé."""
    ligne = (
        "[Haut Conseil des finances publiques (HCFP)]"
        '(<http://www.hcfp.fr/> "Haut Conseil des finances publiques '
        '\\(HCFP\\)\\(nouvelle fenêtre\\)")'
    )
    assert nettoyer_destinations([ligne]) == [
        "[Haut Conseil des finances publiques (HCFP)]"
    ]


def test_titre_court_emporte() -> None:
    """FR-002 (T002) : guillemets et espace du titre emportés."""
    assert nettoyer_destinations(['[A](<https://exemple.fr> "titre")']) == ["[A]"]


def test_titre_sur_lien_relatif_emporte() -> None:
    """US3 scénario 2 (T002) : même règle sur la forme 004 avec titre."""
    assert nettoyer_destinations(['[A](</chemin> "titre")']) == ["[A]"]


def test_titre_avec_guillemet_interne_non_matche() -> None:
    """Limite D2 (T002) : guillemet interne échappé → ligne inchangée, sans
    corruption (la parenthèse fermante n'est pas atteinte)."""
    ligne = '[A](<https://exemple.fr> "titre \\" interne") fin'
    assert nettoyer_destinations([ligne]) == [ligne]


def test_titre_sans_destination_intact() -> None:
    """Cas limite (T002) : ]( "titre") sans chevrons ne matche pas."""
    ligne = '[A]( "titre") fin'
    assert nettoyer_destinations([ligne]) == [ligne]
