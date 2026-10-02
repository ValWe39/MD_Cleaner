"""Tests d'intégration feature 004 : destinations de liens (T002-T004).

SC-001 à SC-004, FR-001 à FR-005 : run standard sans destination résiduelle,
--conserver-liens réversible octet par octet, neutralité sur corpus sans
liens, sortie paginée nettoyée avec marqueurs et cartographie intacts.
"""

import re
from pathlib import Path

from md_cleaner.cli import CODE_OK, main

RACINE = Path(__file__).parents[2]
EXEMPLE_2 = RACINE / "Examples" / "Exemple_2" / "2.Input" / "consolidated.md"

_RE_DESTINATION = re.compile(r"(?<=\])\(</[^>]*>\)")


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


def _nettoye(racine, run: str = "001") -> str:
    return (racine / run / "nettoye.md").read_text(encoding="utf-8")


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
    assert (tmp_path / "defaut" / "001" / "nettoye.md").read_bytes() == (
        tmp_path / "brut" / "001" / "nettoye.md"
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
