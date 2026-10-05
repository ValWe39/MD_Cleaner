"""Tests unitaires de normalisation (T007) : parties variables et slug (FR-003, D3, D8).

Feature 006 (T001) : nommage du fichier nettoyé dérivé de la source
(FR-001 à FR-003, contrat nommage-sortie).
"""

from md_cleaner.normalisation import nom_sortie_nettoye, normaliser_ligne, slug_titre


def test_url_normalisee() -> None:
    assert normaliser_ligne("Voir https://example.com/page-12?x=1 maintenant") == (
        "Voir <URL> maintenant"
    )
    # Un lien relatif varying par numero de page est egalise par le jeton <N>
    a = normaliser_ligne("[Lecon](</fr/formations/le-chat-mcp/1/>)")
    b = normaliser_ligne("[Lecon](</fr/formations/le-chat-mcp/7/>)")
    assert a == b


def test_nombre_normalise() -> None:
    assert normaliser_ligne("Lecon 12 du module 3") == "Lecon <N> du module <N>"
    assert normaliser_ligne("Taux de 3,14 points") == "Taux de <N> points"


def test_date_textuelle_normalisee() -> None:
    assert (
        normaliser_ligne("Mis a jour le 29 juillet 2026 ici")
        == "Mis a jour le <DATE> ici"
    )


def test_date_iso_et_numerique() -> None:
    assert normaliser_ligne("Publie le 2026-09-29.") == "Publie le <DATE>."
    assert normaliser_ligne("Le 29/07/2026 et 07.29.26 ok") == "Le <DATE> et <DATE> ok"


def test_parties_variables_egalisent_les_pages() -> None:
    """FR-003 : un fil d'Ariane variant par numero de lecon est reconnu identique."""
    a = normaliser_ligne("[Formations](</fr/)>/Lecon 1")
    b = normaliser_ligne("[Formations](</fr/)>/Lecon 7")
    assert a == b


def test_espaces_plies() -> None:
    assert normaliser_ligne("a   b \t c") == "a b c"


def test_ligne_vide() -> None:
    assert normaliser_ligne("   ") == ""


def test_slug_titre() -> None:
    assert slug_titre("Le Chat et MCP - Automatisez", 10) == "le-chat-et"


def test_slug_titre_accents() -> None:
    assert slug_titre("Écosystème à l'épreuve", 9) == "ecosystem"


def test_slug_titre_ponctuation() -> None:
    assert slug_titre("Qu'est-ce que le MCP ?", 30) == "qu-est-ce-que-le-mcp"


# --- Feature 006 : nom de sortie dérivé du document source (T001) ---


def test_nom_sortie_nominal() -> None:
    """FR-001 : nom exact de l'exemple utilisateur (20 caractères, aucun retrait)."""
    assert nom_sortie_nettoye("retry-failed-records") == "retry-failed-records-nettoye"


def test_nom_sortie_court() -> None:
    """FR-001 : sous 20 caractères, ni troncature ni remplissage."""
    assert nom_sortie_nettoye("rapport") == "rapport-nettoye"


def test_nom_sortie_espaces_et_tabulations() -> None:
    """FR-002 : espace U+0020 et tabulation U+0009, chacune un _."""
    assert nom_sortie_nettoye("rapport annuel") == "rapport_annuel-nettoye"
    assert nom_sortie_nettoye("rapport\tannuel") == "rapport_annuel-nettoye"


def test_nom_sortie_sans_compression() -> None:
    """FR-002 : chaque blanc → un _, pas de compression des séquences."""
    assert nom_sortie_nettoye("rapport  annuel") == "rapport__annuel-nettoye"


def test_nom_sortie_blancs_aux_extremites() -> None:
    """FR-002 : blancs en tête et en fin remplacés, pas de décapage (cas limite)."""
    assert nom_sortie_nettoye(" rapport") == "_rapport-nettoye"
    assert nom_sortie_nettoye("rapport ") == "rapport_-nettoye"


def test_nom_sortie_accents_et_casse_conserves() -> None:
    """FR-002 : accents et casse conservés, seul le blanc devient _."""
    assert nom_sortie_nettoye("éco développement") == "éco_développement-nettoye"


def test_nom_sortie_troncature_brute() -> None:
    """FR-003 : troncature brute à 20 points de code, sans frontière de mot."""
    attendu = "comptes-rendus-conse"
    assert nom_sortie_nettoye("comptes-rendus-conseil-municipal-session-octobre") == (
        attendu + "-nettoye"
    )
    assert len(attendu) == 20


def test_nom_sortie_stem_de_blancs_uniquement() -> None:
    """Cas limite spec : un stem uniquement de blancs devient ___ (D2)."""
    assert nom_sortie_nettoye("   ") == "___-nettoye"
