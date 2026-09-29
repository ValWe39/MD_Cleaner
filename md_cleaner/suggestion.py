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
    source: str,
    seuil: int,
    mode_segmentation: str,
    nb_pages: int,
    motifs: list[Motif],
    pages: list | None = None,
    extrait_n: int = 5,
) -> dict:
    """Suggestion par défaut consommable et éditable (D5 feature 001).

    Feature 003 : avec `pages`, chaque motif est enrichi — l'extrait
    devient les `extrait_n` premières lignes du premier intervalle de
    sa page de première occurrence, rendues en vrais sauts de ligne,
    et un champ position (fin inclue, même ancrage) est ajouté
    (FR-001, FR-002, D1/D3)."""
    motifs_json = []
    for m in motifs:
        entree: dict = {
            "id": m.id,
            "action": m.action,
            "nb_lignes": m.nb_lignes,
            "frequence": m.frequence,
            "pages": list(m.pages),
            "extrait": m.extrait,
        }
        if pages is not None:
            extrait, position = _enrichir_motif(pages, m, extrait_n)
            entree["extrait"] = extrait
            entree["position"] = position
        motifs_json.append(entree)
    return {
        "version": 1,
        "source": source,
        "seuil": seuil,
        "mode_segmentation": mode_segmentation,
        "nb_pages": nb_pages,
        "motifs": motifs_json,
    }


def _enrichir_motif(pages: list, motif: Motif, extrait_n: int) -> tuple:
    """Extrait multi-lignes et position du motif, ancrés sur sa
    première occurrence (page la plus ancienne, premier intervalle).

    `fin` de la position est incluse : conversion depuis l'intervalle
    interne demi-ouvert (D3)."""
    position = {p.numero: i for i, p in enumerate(pages)}
    num0 = min(
        motif.emplacements, key=lambda n: (position[n], motif.emplacements[n][0][0])
    )
    debut, fin = motif.emplacements[num0][0]
    lignes = pages[position[num0]].lignes[debut : min(debut + extrait_n, fin)]
    extrait = "\n".join(lignes)
    return extrait, {"page": num0, "debut": debut, "fin": fin - 1}


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
        if "position" in motif and not _position_valide(motif["position"]):
            raise ErreurSuggestion(
                f"suggestion invalide : position pour {identifiant} "
                "(objet {page, debut, fin} avec page >= 1, debut >= 0, fin > debut attendu)"
            )
    return donnees


def _position_valide(position: object) -> bool:
    """FR-005 : position optionnelle mais, si présente, bien formée."""
    if not isinstance(position, dict):
        return False
    cles = ("page", "debut", "fin")
    if any(cle not in position for cle in cles):
        return False

    def entier(valeur: object) -> bool:
        return isinstance(valeur, int) and not isinstance(valeur, bool)

    return (
        entier(position["page"])
        and position["page"] >= 1
        and entier(position["debut"])
        and position["debut"] >= 0
        and entier(position["fin"])
        and position["fin"] > position["debut"]
    )


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
    """Rapport dry-run en deux sections (FR-004, contracts/rapport-dry-run.md) :
    décisions requises (motifs supprimer) et motifs conservés par défaut
    (aucune action requise)."""
    lignes = [
        "# Rapport dry-run",
        "",
        f"Source : {suggestion['source']}",
        f"Seuil : {suggestion['seuil']} % des {suggestion['nb_pages']} pages",
        f"Mode de segmentation : {suggestion['mode_segmentation']}",
        "",
        "## Décisions requises",
        "",
        "| Id | Action suggérée | Fréquence | Pages | Extrait |",
        "| -- | --------------- | --------- | ----- | ------- |",
    ]
    supprimer = [m for m in suggestion["motifs"] if m["action"] == "supprimer"]
    conserver = [m for m in suggestion["motifs"] if m["action"] == "conserver"]
    for motif in supprimer:
        # FR-004 : les sauts de ligne sont neutralisés dans les cellules
        # du tableau (un \n y terminerait la rangée markdown) ;
        # troncature à 120 caractères inchangée.
        extrait = motif["extrait"].replace("|", "\\|").replace("\n", " / ")[:120]
        lignes.append(
            f"| {motif['id']} | {motif['action']} | {motif['frequence']} "
            f"| {len(motif['pages'])} pages | {extrait} |"
        )
    if not supprimer:
        lignes.append("aucun")
    lignes.append("")
    lignes.append("## Motifs conservés par défaut — aucune action requise")
    for motif in conserver:
        lignes.append(f"- {motif['id']} ({motif['frequence']}) : {motif['extrait']}")
    if not conserver:
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
