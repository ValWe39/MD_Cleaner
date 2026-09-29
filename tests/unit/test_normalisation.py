"""Tests unitaires de normalisation (T007) : parties variables et slug (FR-003, D3, D8)."""

from md_cleaner.normalisation import normaliser_ligne, slug_titre


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
