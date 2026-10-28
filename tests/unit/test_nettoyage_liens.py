"""Tests unitaires de la passe de retrait des destinations (004/005/009).

FR-001, FR-002, FR-006, FR-007, D1, D2, D5 : règle unifiée ](<...>) sans
distinction de schéma (option A), titre retiré avec la destination,
premier > refermant, sans décodage, libellés et crochets conservés,
URLs nues et marqueurs de page non matchés, idempotence.
Feature 009 : extension aux destinations sans chevrons ](...) (ancres,
relatifs, absolus, titres), images épargnées par protection (D2, D4),
neutralité des formes chevrons (D1, FR-005).
"""

from md_cleaner.nettoyage import Bloc, ecrire_nettoye, nettoyer_destinations


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


def test_destination_absolue_retiree() -> None:
    """FR-001 (009) : ](https://...) sans chevrons retirée, libellé conservé."""
    assert nettoyer_destinations(["[X](https://exemple.fr/page)"]) == ["[X]"]


def test_destination_relative_sans_chevrons_retiree() -> None:
    """FR-001 (009) : ](chemin/relatif) sans chevrons retirée."""
    assert nettoyer_destinations(["[X](chemin/relatif)"]) == ["[X]"]


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


# --- Feature 009 : destinations sans chevrons ---


def test_ancre_retiree() -> None:
    """FR-001 (009, T004) : ](#haut) retirée, libellé conservé."""
    assert nettoyer_destinations(["[Revenir en haut de page](#haut)"]) == [
        "[Revenir en haut de page]"
    ]


def test_ancre_vide_retiree() -> None:
    """Cas limite (009, T004) : ](#) retirée."""
    assert nettoyer_destinations(["[Ressources](#)"]) == ["[Ressources]"]


def test_relatif_racine_retire() -> None:
    """FR-001 (009, T004) : ](/commentaire/...) retirée sans décodage."""
    assert nettoyer_destinations(
        ["[Lire →](/commentaire/Le%20patrimoine%20des%20...%20fin%202025)"]
    ) == ["[Lire →]"]


def test_relatif_sans_slash_retire() -> None:
    """FR-001 (009, T004) : ](Les-crédits-dimp...) retirée, libellé avec
    ses crochets et son italique conservés (comportement 004/005)."""
    assert nettoyer_destinations(
        ["« [*crédit d'impôt*](Les-crédits-dimp%C3%B4t) »"]
    ) == ["« [*crédit d'impôt*] »"]


def test_plusieurs_liens_sans_chevrons_sur_une_ligne() -> None:
    """US1 scénario (009, T004) : chaque occurrence retirée, ordre conservé."""
    assert nettoyer_destinations(["[A](/a) et [B](https://b.fr)"]) == ["[A] et [B]"]


def test_note_de_bas_de_page() -> None:
    """Cas limite (009, T004) : ](#_ftn1) retirée, [[1]] conservé (D7)."""
    assert nettoyer_destinations(["en comptabilité nationale[[1]](#_ftn1)."]) == [
        "en comptabilité nationale[[1]]."
    ]


def test_titre_sans_chevrons_emporte() -> None:
    """FR-007 (009, T004) : destination et titre retirés (arbitrage 005)."""
    assert nettoyer_destinations(['[A](https://exemple.fr "titre")']) == ["[A]"]


def test_destination_vide_sans_titre_intacte() -> None:
    """Cas limite (009, T004) : ]() et ]( "titre") ne matchent pas."""
    assert nettoyer_destinations(["[A]() fin"]) == ["[A]() fin"]
    assert nettoyer_destinations(['[A]( "titre") fin']) == ['[A]( "titre") fin']


def test_ligne_entierement_constituee_dun_lien_sans_chevrons() -> None:
    """Précédent 004 (009, T004) : ligne conservée, libellé seul."""
    assert nettoyer_destinations(["[Libellé](/chemin)"]) == ["[Libellé]"]


def test_idempotence_sans_chevrons() -> None:
    """FR-008 (009, T004) : deux passes = une passe sur les deux règles."""
    lignes = ["[A](/a) et [B](https://b.fr) fin"]
    une = nettoyer_destinations(lignes)
    assert nettoyer_destinations(une) == une


def test_conserver_liens_desactive_les_deux_regles(tmp_path) -> None:
    """FR-004 (009, T008) : le drapeau laisse intactes les deux formes."""
    bloc = Bloc("P1-B1", 1, ["[A](</a>) [B](/b)"], 0, 0)
    chemin = tmp_path / "sortie.md"
    ecrire_nettoye(chemin, [bloc], conserver_liens=True)
    assert chemin.read_text(encoding="utf-8") == "[A](</a>) [B](/b)\n"
    ecrire_nettoye(chemin, [bloc], conserver_liens=False)
    assert chemin.read_text(encoding="utf-8") == "[A] [B]\n"


def test_image_simple_intacte() -> None:
    """FR-003 (009, T011) : figure épargnée, destination comprise."""
    ligne = "![](/images/FIV11a.png)Sources : rapports annexés."
    assert nettoyer_destinations([ligne]) == [ligne]


def test_logo_imbrique_reduit_a_image() -> None:
    """FR-003, D7 (009, T011) : destination externe retirée, image conservée."""
    assert nettoyer_destinations(["[![FIPECO](/images/logo.jpg)](/)"]) == [
        "[![FIPECO](/images/logo.jpg)]"
    ]


def test_image_alt_avec_crochet_fermant_non_protegee() -> None:
    """Limite D2 (009, T011) : construct non protégé, la règle lien
    standard s'applique à la sous-chaîne suivant le crochet fermant."""
    assert nettoyer_destinations(["![a]b](/img) fin"]) == ["![a]b] fin"]


def test_image_au_milieu_de_liens() -> None:
    """FR-003 (009, T011) : image intacte entre des liens nettoyés."""
    lignes = ["[A](/a) ![](/img.png) [B](https://b.fr)"]
    assert nettoyer_destinations(lignes) == ["[A] ![](/img.png) [B]"]


def test_formes_chevrons_inchangees_par_la_regle_009() -> None:
    """FR-005 (009, T014) : les formes ](<...>) gardent le traitement 004/005."""
    ligne = '[A](</a>) et [B](<https://b.fr> "t") fin'
    assert nettoyer_destinations([ligne]) == ["[A] et [B] fin"]


def test_idempotence_mixte() -> None:
    """FR-008 (009, T014) : idempotence sur les deux formes et une image."""
    lignes = ["[A](</a>) [B](/b) ![](/img.png)"]
    une = nettoyer_destinations(lignes)
    assert nettoyer_destinations(une) == une


# --- Bug nettoyage-balises2 : footnotes à titre échappé, espaces ---


def test_footnote_titre_echappe_emporte() -> None:
    """Bug nettoyage-balises2 : destination, titre et HTML embarqué
    (guillemets échappés) emportés ensemble, libellé conservé."""
    ligne = (
        "…politique des politiques [1](#easy-footnote-bottom-1-138905 "
        '"Emmanuel Macron, <a href=\\"https://avecvous.fr/publications/'
        'emmanuel-macron-avec-vous-a-marseille\\">Discours au Pharo</a>, '
        '16 avril 2022"). Le Président…'
    )
    assert nettoyer_destinations([ligne]) == [
        "…politique des politiques [1]. Le Président…"
    ]


def test_destination_avec_espaces_retiree() -> None:
    """Bug nettoyage-balises2 : destination non encodée avec espaces
    retirée quand aucun titre ne suit (Markdown invalide du convertisseur)."""
    assert nettoyer_destinations(
        ["[Histoire en images](https://exemple.fr/fr/Histoire en images)"]
    ) == ["[Histoire en images]"]


def test_destination_espaces_avec_titre_intacte() -> None:
    """Limite documentée (bug nettoyage-balises2) : destination à espaces
    suivie d'un titre — non couverte, ligne inchangée sans corruption."""
    ligne = '[A](chemin relatif "titre") fin'
    assert nettoyer_destinations([ligne]) == [ligne]


def test_footnote_et_image_sur_la_meme_ligne() -> None:
    """Bug nettoyage-balises2 : footnote emportée, image épargnée sur la
    même ligne (FR-003)."""
    ligne = (
        "Texte ![](/images/figure.jpg) puis [2](#easy-footnote-bottom-2-1 "
        '"<a href=\\"https://exemple.fr/rapport\\">Rapport</a>") suite'
    )
    assert nettoyer_destinations([ligne]) == [
        "Texte ![](/images/figure.jpg) puis [2] suite"
    ]


def test_idempotence_formes_bug() -> None:
    """FR-008 (bug nettoyage-balises2) : deux passes = une passe."""
    lignes = [
        '[A](/a) [B](https://exemple.fr/x y) [C](#ancre "titre \\"echappe\\"") fin'
    ]
    une = nettoyer_destinations(lignes)
    assert nettoyer_destinations(une) == une


def test_autolink_retire() -> None:
    """Quick fix 2026-10-27 : l'autolink <https://...> est retiré,
    sans libellé ni crochet — la référence devient vide (l'espace
    résiduel est décapé par le writer, cf. _compacter)."""
    ligne = (
        "13. <https://www.eea.europa.eu/data-and-maps/dashboards"
        "/emissions-trading-viewer-1>"
    )
    assert nettoyer_destinations([ligne]) == ["13. "]


def test_autolink_chevron_limite_non_corrompu() -> None:
    """Limite 004/005 préservée : une destination chevron dont le
    titre échoue (guillemets échappés) reste en place — l'autolink
    interne n'est pas retiré, aucune corruption."""
    ligne = '[A](<https://exemple.fr> "titre " interne") fin'
    assert nettoyer_destinations([ligne]) == [ligne]


def test_autolink_image_protegee() -> None:
    """FR-003 : une image à destination chevron est épargnée,
    l'autolink ne touche pas sa destination protégée."""
    ligne = "![](<https://exemple.fr/img.png>) légende"
    assert nettoyer_destinations([ligne]) == [ligne]


def test_url_nue_et_autolink_distincts() -> None:
    """Garde-fou 005 : URL nue intacte, autolink retiré — les deux
    formes cohabitent sans confusion."""
    lignes = ["voir https://exemple.fr/a puis <https://exemple.fr/b> fin"]
    assert nettoyer_destinations(lignes) == ["voir https://exemple.fr/a puis  fin"]
