"""Tests d'intégration features 004/005 : destinations de liens (T002-T005).

SC-001 à SC-005, FR-003 à FR-005, FR-007 : run standard sans destination
résiduelle (relatives et absolues), --conserver-liens réversible octet par
octet, garde-fou des URLs nues (corps du texte, blocs de code), neutralité
sur corpus sans liens absolus conservés, sortie paginée nettoyée avec
marqueurs et cartographie intacts, dry-run non affecté.
"""

import re
from pathlib import Path

from md_cleaner.cli import CODE_OK, main

RACINE = Path(__file__).parents[2]
EXEMPLE_1 = RACINE / "Examples" / "Exemple_1" / "2.Input" / "consolidated.md"
EXEMPLE_2 = RACINE / "Examples" / "Exemple_2" / "2.Input" / "consolidated.md"
EXEMPLE_3 = RACINE / "Examples" / "Exemple_3" / "2.Input" / "retry-failed-records.md"

# Règle unifiée de la feature 005 : toute destination ](<...>), titre éventuel
# compris (contracts/nettoyage-liens-absolus.md).
_RE_DESTINATION = re.compile(r'(?<=\])\(<[^>]*>(?: "[^"]*")?\)')

# Règle de la feature 004 (référence pour la neutralité : sur les corpus où
# aucune destination absolue ne survit à la détection, les deux règles
# produisent le même résultat).
_RE_RELATIVE_004 = re.compile(r"(?<=\])\(</[^>]*>\)")


def _corpus_sans_liens(tmp_path) -> Path:
    """Corpus multi-pages sans aucune destination ](</...>) (SC-003)."""
    lignes: list[str] = []
    for page in range(1, 4):
        lignes.append(f"## Page {page}: https://exemple.fr/{page}")
        lignes += ["", f"# Titre du contenu numéro {page}", ""]
        lignes += [f"Paragraphe unique de la page {page} alpha bêta.", ""]
    chemin = tmp_path / "sans-liens.md"
    chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    return chemin


def _nettoye(racine, run: str = "001", nom: str = "consolidated-nettoye.md") -> str:
    """Lecture du fichier nettoyé, nommé d'après l'entrée (feature 006)."""
    return (racine / run / nom).read_text(encoding="utf-8")


def test_run_standard_sans_destination(tmp_path) -> None:
    """SC-001 (T002) : aucune ligne du nettoye.md ne contient ](</...>)."""
    assert main([str(EXEMPLE_2), "--sortie", str(tmp_path)]) == CODE_OK
    nettoye = _nettoye(tmp_path)
    assert "](<" not in nettoye
    assert nettoye.strip()
    assert "[Famille, handicap, sport et jeunesse]" in nettoye


def test_lignes_et_ordre_inchanges_vs_conserver(tmp_path) -> None:
    """SC-002 (T002) : même nombre et ordre de lignes que le run conservé."""
    assert main([str(EXEMPLE_2), "--sortie", str(tmp_path / "defaut")]) == CODE_OK
    assert (
        main([str(EXEMPLE_2), "--conserver-liens", "--sortie", str(tmp_path / "brut")])
        == CODE_OK
    )
    propre = _nettoye(tmp_path / "defaut").splitlines()
    brut = _nettoye(tmp_path / "brut").splitlines()
    assert len(propre) == len(brut)
    assert propre == [_RE_DESTINATION.sub("", ligne) for ligne in brut]


def test_conserver_liens_garde_les_destinations(tmp_path) -> None:
    """SC-004 (T003) : avec le drapeau, les destinations restent intactes."""
    assert (
        main([str(EXEMPLE_2), "--conserver-liens", "--sortie", str(tmp_path)])
        == CODE_OK
    )
    brut = _nettoye(tmp_path)
    assert "](<" in brut
    assert _RE_DESTINATION.search(brut)


def test_corpus_sans_liens_sorties_identiques(tmp_path) -> None:
    """SC-003 (T003) : sans ](</...>) en entrée, les deux modes sont
    identiques octet par octet."""
    entree = _corpus_sans_liens(tmp_path)
    assert main([str(entree), "--sortie", str(tmp_path / "defaut")]) == CODE_OK
    assert (
        main([str(entree), "--conserver-liens", "--sortie", str(tmp_path / "brut")])
        == CODE_OK
    )
    assert (tmp_path / "defaut" / "001" / "sans-liens-nettoye.md").read_bytes() == (
        tmp_path / "brut" / "001" / "sans-liens-nettoye.md"
    ).read_bytes()


def test_paginer_marqueurs_et_cartographie_intacts(tmp_path) -> None:
    """FR-004, FR-005, SC-004 (T004) : contenu paginé nettoyé, marqueurs et
    cartographie identiques entre les deux modes."""
    assert (
        main([str(EXEMPLE_2), "--pagine", "--sortie", str(tmp_path / "defaut")])
        == CODE_OK
    )
    assert (
        main(
            [
                str(EXEMPLE_2),
                "--pagine",
                "--conserver-liens",
                "--sortie",
                str(tmp_path / "brut"),
            ]
        )
        == CODE_OK
    )
    pagine_defaut = (tmp_path / "defaut" / "001" / "nettoye-pagine.md").read_text(
        encoding="utf-8"
    )
    pagine_brut = (tmp_path / "brut" / "001" / "nettoye-pagine.md").read_text(
        encoding="utf-8"
    )

    assert "](<" not in pagine_defaut
    assert "](<" in pagine_brut

    def marqueurs(texte: str) -> list[str]:
        return [ligne for ligne in texte.splitlines() if ligne.startswith("<!-- page:")]

    assert marqueurs(pagine_defaut) == marqueurs(pagine_brut)
    assert marqueurs(pagine_defaut)

    assert (tmp_path / "defaut" / "001" / "cartographie.json").read_bytes() == (
        tmp_path / "brut" / "001" / "cartographie.json"
    ).read_bytes()


def _document_garde_fou(tmp_path) -> Path:
    """Document avec URLs nues (bloc de code, corps du texte) et un lien
    absolu : le garde-fou ne doit toucher que la syntaxe de lien (SC-005)."""
    lignes = [
        "## Doc garde-fou",
        "",
        "```python",
        'client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])',
        "# endpoint : https://api.mistral.ai",
        "```",
        "",
        "La documentation officielle est sur https://docs.mistral.ai/api.",
        "",
        "[Try Studio ](<https://console.mistral.ai?utm_source=docs>) propose un essai.",
    ]
    chemin = tmp_path / "garde-fou.md"
    chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    return chemin


def test_urls_nues_intactes_et_lien_absolu_retire(tmp_path) -> None:
    """FR-007, SC-005 (T003) : URLs nues intactes octet par octet, lien
    absolu nettoyé."""
    entree = _document_garde_fou(tmp_path)
    assert main([str(entree), "--sortie", str(tmp_path / "run")]) == CODE_OK
    nettoye = _nettoye(tmp_path / "run", nom="garde-fou-nettoye.md")
    assert "https://api.mistral.ai" in nettoye
    assert "La documentation officielle est sur https://docs.mistral.ai/api." in nettoye
    assert "[Try Studio ](<" not in nettoye
    assert "[Try Studio ] propose un essai." in nettoye


def test_run_exemple_3_sans_destination(tmp_path) -> None:
    """SC-001 (T004) : aucune ligne du nettoye.md ne contient ](<, les
    libellés absolus restent en place."""
    assert main([str(EXEMPLE_3), "--sortie", str(tmp_path)]) == CODE_OK
    nettoye = _nettoye(tmp_path, nom="retry-failed-records-nettoye.md")
    assert "](<" not in nettoye
    assert "[Reach out]" in nettoye
    assert "[Try Studio ]" in nettoye
    assert "[Discord↗]" in nettoye


def test_exemple_3_lignes_et_ordre_inchanges_vs_conserver(tmp_path) -> None:
    """SC-002 (T004) : même nombre et ordre de lignes que le run conservé ;
    le diff se limite aux destinations (et titres) retirées."""
    assert main([str(EXEMPLE_3), "--sortie", str(tmp_path / "defaut")]) == CODE_OK
    assert (
        main([str(EXEMPLE_3), "--conserver-liens", "--sortie", str(tmp_path / "brut")])
        == CODE_OK
    )
    propre = _nettoye(
        tmp_path / "defaut", nom="retry-failed-records-nettoye.md"
    ).splitlines()
    brut = _nettoye(
        tmp_path / "brut", nom="retry-failed-records-nettoye.md"
    ).splitlines()
    assert len(propre) == len(brut)
    assert propre == [_RE_DESTINATION.sub("", ligne) for ligne in brut]


def test_neutralite_exemple_1_et_2(tmp_path) -> None:
    """SC-003 (T005) : aucune destination absolue ne survit à la détection
    sur Exemple_1/Exemple_2 ; le run par défaut y égale le run conservé
    nettoyé par la seule règle 004."""
    for exemple in (EXEMPLE_1, EXEMPLE_2):
        assert (
            main(
                [str(exemple), "--conserver-liens", "--sortie", str(tmp_path / "brut")]
            )
            == CODE_OK
        )
        brut = _nettoye(tmp_path / "brut")
        assert "](<http" not in brut
        assert main([str(exemple), "--sortie", str(tmp_path / "defaut")]) == CODE_OK
        propre = _nettoye(tmp_path / "defaut")
        assert propre.splitlines() == [
            _RE_RELATIVE_004.sub("", ligne) for ligne in brut.splitlines()
        ]


def test_conserver_liens_garde_les_destinations_absolues(tmp_path) -> None:
    """SC-004 (T005) : avec le drapeau, destinations absolues intactes sur
    Exemple_3, identiques à une sortie produite sans la feature."""
    assert (
        main([str(EXEMPLE_3), "--conserver-liens", "--sortie", str(tmp_path / "brut")])
        == CODE_OK
    )
    brut = _nettoye(tmp_path / "brut", nom="retry-failed-records-nettoye.md")
    assert "](<https://mistral.ai/about>)" in brut
    assert "](<https://console.mistral.ai?utm_source=docs" in brut


def test_dry_run_inchange_par_la_passe(tmp_path) -> None:
    """FR-005 (T005) : suggestion.json et rapport-dry-run.md identiques que
    la passe soit active ou désactivée (aucun effet observable en dry-run).
    Le rapport embarque le chemin de la suggestion : les chemins des deux
    dossiers sont normalisés avant comparaison."""
    assert (
        main([str(EXEMPLE_3), "--dry-run", "--sortie", str(tmp_path / "actif")])
        == CODE_OK
    )
    assert (
        main(
            [
                str(EXEMPLE_3),
                "--dry-run",
                "--conserver-liens",
                "--sortie",
                str(tmp_path / "brut"),
            ]
        )
        == CODE_OK
    )
    assert (tmp_path / "actif" / "001" / "suggestion.json").read_bytes() == (
        tmp_path / "brut" / "001" / "suggestion.json"
    ).read_bytes()

    rapports = {}
    for mode in ("actif", "brut"):
        texte = (tmp_path / mode / "001" / "rapport-dry-run.md").read_text(
            encoding="utf-8"
        )
        rapports[mode] = texte.replace(str(tmp_path / mode), "<sortie>")
    assert rapports["actif"] == rapports["brut"]
