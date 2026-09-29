"""Suggestion éditable et rapport dry-run (FR-007, FR-008, contracts/formats.md)."""

import json
import re
from pathlib import Path

from md_cleaner.detection import Motif

ACTIONS = {"supprimer", "conserver"}
RE_ID = re.compile(r"^M\d{2,}$")
MODES = {"explicite", "heuristique", "unique"}


class ErreurSuggestion(Exception):
    """Suggestion invalide ou incohérente (code retour 2)."""


def construire_suggestion(
    source: str, seuil: int, mode_segmentation: str, nb_pages: int, motifs: list[Motif]
) -> dict:
    """Suggestion par défaut consommable et éditable (D5)."""
    return {
        "version": 1,
        "source": source,
        "seuil": seuil,
        "mode_segmentation": mode_segmentation,
        "nb_pages": nb_pages,
        "motifs": [
            {
                "id": m.id,
                "action": m.action,
                "nb_lignes": m.nb_lignes,
                "frequence": m.frequence,
                "pages": list(m.pages),
                "extrait": m.extrait,
            }
            for m in motifs
        ],
    }


def ecrire_suggestion(chemin: Path, suggestion: dict) -> None:
    """Sérialisation déterministe : clés triées, indentation 2 (D9)."""
    Path(chemin).write_text(
        json.dumps(suggestion, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def lire_suggestion(chemin: Path, source: str) -> dict:
    """Charge et valide strictement un suggestion.json (contracts/formats.md)."""
    try:
        donnees = json.loads(Path(chemin).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as erreur:
        raise ErreurSuggestion(f"suggestion illisible : {erreur}") from erreur
    if not isinstance(donnees, dict):
        raise ErreurSuggestion("suggestion invalide : objet JSON attendu")
    if donnees.get("version") != 1:
        raise ErreurSuggestion("suggestion invalide : version doit valoir 1")
    if donnees.get("source") != source:
        raise ErreurSuggestion(
            f"suggestion incohérente : source {donnees.get('source')!r} "
            f"attend {source!r}"
        )
    seuil = donnees.get("seuil")
    if not isinstance(seuil, int) or not 2 <= seuil <= 100:
        raise ErreurSuggestion("suggestion invalide : seuil entier 2-100 attendu")
    if donnees.get("mode_segmentation") not in MODES:
        raise ErreurSuggestion("suggestion invalide : mode_segmentation inconnu")
    if not isinstance(donnees.get("nb_pages"), int) or donnees["nb_pages"] < 1:
        raise ErreurSuggestion("suggestion invalide : nb_pages entier >= 1 attendu")
    motifs = donnees.get("motifs")
    if not isinstance(motifs, list):
        raise ErreurSuggestion("suggestion invalide : liste de motifs attendue")
    vus: set[str] = set()
    for motif in motifs:
        if not isinstance(motif, dict):
            raise ErreurSuggestion("suggestion invalide : motif objet attendu")
        identifiant = motif.get("id")
        if not isinstance(identifiant, str) or not RE_ID.match(identifiant):
            raise ErreurSuggestion(f"suggestion invalide : id {identifiant!r}")
        if identifiant in vus:
            raise ErreurSuggestion(f"suggestion invalide : id dupliqué {identifiant}")
        vus.add(identifiant)
        if motif.get("action") not in ACTIONS:
            raise ErreurSuggestion(
                f"suggestion invalide : action {motif.get('action')!r} pour {identifiant}"
            )
        frequence = motif.get("frequence")
        if not isinstance(frequence, (int, float)) or not 0 <= frequence <= 1:
            raise ErreurSuggestion(
                f"suggestion invalide : fréquence pour {identifiant}"
            )
        pages = motif.get("pages")
        if (
            not isinstance(pages, list)
            or not all(isinstance(p, int) for p in pages)
            or pages != sorted(pages)
        ):
            raise ErreurSuggestion(
                f"suggestion invalide : pages triées pour {identifiant}"
            )
        nb_lignes = motif.get("nb_lignes")
        if not isinstance(nb_lignes, int) or nb_lignes < 1:
            raise ErreurSuggestion(
                f"suggestion invalide : nb_lignes pour {identifiant}"
            )
        if not isinstance(motif.get("extrait"), str):
            raise ErreurSuggestion(f"suggestion invalide : extrait pour {identifiant}")
    return donnees


def appliquer_actions(motifs: list[Motif], suggestion: dict) -> None:
    """Applique les actions éditées aux motifs détectés (ids déterministes).

    Un id inconnu est une erreur bloquante (contracts/formats.md)."""
    detectes = {motif.id: motif for motif in motifs}
    for motif in suggestion["motifs"]:
        if motif["id"] not in detectes:
            raise ErreurSuggestion(
                f"id inconnu dans la suggestion : {motif['id']} "
                "(aucune correspondance dans le document)"
            )
        detectes[motif["id"]].action = motif["action"]


def generer_rapport(chemin: Path, suggestion: dict, avertissements: list[str]) -> None:
    """Rapport dry-run lisible : motifs, motifs sous le seuil, cas limites."""
    seuil = suggestion["seuil"]
    lignes = [
        "# Rapport dry-run",
        "",
        f"Source : {suggestion['source']}",
        f"Seuil : {seuil} % des {suggestion['nb_pages']} pages",
        f"Mode de segmentation : {suggestion['mode_segmentation']}",
        "",
        "## Motifs détectés",
        "",
        "| Id | Action suggérée | Fréquence | Pages | Extrait |",
        "| -- | --------------- | --------- | ----- | ------- |",
    ]
    for motif in suggestion["motifs"]:
        extrait = motif["extrait"].replace("|", "\\|")[:120]
        lignes.append(
            f"| {motif['id']} | {motif['action']} | {motif['frequence']} "
            f"| {len(motif['pages'])} pages | {extrait} |"
        )
    sous_seuil = [m for m in suggestion["motifs"] if m["frequence"] < seuil / 100]
    lignes.append("")
    lignes.append("## Motifs sous le seuil (conservés par défaut)")
    for motif in sous_seuil:
        lignes.append(f"- {motif['id']} ({motif['frequence']}) : {motif['extrait']}")
    if not sous_seuil:
        lignes.append("- aucun")
    lignes.append("")
    lignes.append("## Cas limites")
    for message in avertissements:
        lignes.append(f"- {message}")
    if not avertissements:
        lignes.append("- aucun")
    lignes.append("")
    lignes.append("## Appliquer la suggestion (éditable puis relancer)")
    lignes.append("")
    lignes.append("```bash")
    lignes.append(
        f"md-cleaner {suggestion['source']} --suggestion {chemin.parent / 'suggestion.json'}"
    )
    lignes.append("```")
    Path(chemin).write_text("\n".join(lignes) + "\n", encoding="utf-8")
