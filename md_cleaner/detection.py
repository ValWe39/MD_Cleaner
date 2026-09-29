"""Détection des motifs répétitifs (research.md D3, FR-002, FR-003, FR-005).

Pipeline déterministe : fenêtres glissantes de lignes normalisées
(w = 25 à 1), fusion des fenêtres chevauchantes en blocs maximaux
(union d'intervalles par page), seuil de fréquence réglable
(80 % par défaut), ids stables M01, M02, ...
"""

from dataclasses import dataclass, field

W_MAX = 25
FREQ_PLANCHER = 0.2
MIN_PAGES = 2


@dataclass
class Motif:
    """Bloc récurrent détecté (data-model.md)."""

    id: str
    action: str
    lignes_norm: list[str]
    extrait: str
    frequence: float
    pages: list[int]
    nb_lignes: int
    emplacements: dict[int, list[tuple[int, int]]] = field(default_factory=dict)


class ErreurEchantillon(Exception):
    """Échantillon de calibrage invalide (code retour 2)."""


def charger_echantillon(dossier) -> list:
    """Charge l'échantillon fourni : ≤ 5 fichiers .md triés par nom (FR-012)."""
    from pathlib import Path

    dossier = Path(dossier)
    if not dossier.is_dir():
        raise ErreurEchantillon(f"dossier d'échantillon introuvable : {dossier}")
    fichiers = sorted(
        (f for f in dossier.iterdir() if f.suffix.lower() == ".md"),
        key=lambda f: f.name,
    )
    if not fichiers:
        raise ErreurEchantillon(f"aucun fichier .md dans {dossier}")
    if len(fichiers) > 5:
        raise ErreurEchantillon("l'échantillon doit contenir au plus 5 fichiers .md")
    from md_cleaner.segmentation import segmenter

    pages = []
    for fichier in fichiers:
        lignes = fichier.read_text(encoding="utf-8-sig").splitlines()
        pages.extend(segmenter(lignes)[0])
    return pages


def _chevauche(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[1] and b[0] <= a[1]


def _ajoute_intervalles(
    intervalles: list[tuple[int, int]], nouveau: tuple[int, int]
) -> list[tuple[int, int]]:
    """Fusionne le nouvel intervalle aux existants seulement s'ils se
    chevauchent ou se touchent ; les intervalles disjoints restent
    séparés (jamais d'union min-max qui avalerait les lignes entre)."""
    resultat = sorted(intervalles + [nouveau])
    fusionnes: list[tuple[int, int]] = []
    for debut, fin in resultat:
        if fusionnes and debut <= fusionnes[-1][1]:
            fusionnes[-1] = (fusionnes[-1][0], max(fusionnes[-1][1], fin))
        else:
            fusionnes.append((debut, fin))
    return fusionnes


def detecter(
    pages: list, seuil: int = 80, pages_calibrage: list | None = None
) -> list[Motif]:
    """Détecte les motifs répétitifs sur les pages (déterministe)."""
    total = len(pages)
    if total < MIN_PAGES:
        return []

    calib = pages if pages_calibrage is None else pages_calibrage
    numeros_calib = {p.numero for p in calib}
    position = {p.numero: i for i, p in enumerate(pages)}

    blocs: list[dict] = []
    w_max = min(W_MAX, max((len(p.lignes_norm) for p in pages), default=1))

    for w in range(w_max, 0, -1):
        index: dict[tuple, dict[int, int]] = {}
        for page in pages:
            normales = page.lignes_norm
            n = len(normales)
            # Sommes préfixées de lignes non vides : test O(1) par fenêtre
            non_vides = [0] * (n + 1)
            for i, ligne in enumerate(normales):
                non_vides[i + 1] = non_vides[i] + (1 if ligne else 0)
            for debut in range(n - w + 1):
                if non_vides[debut + w] == non_vides[debut]:
                    continue
                cles = index.setdefault(tuple(normales[debut : debut + w]), {})
                cles.setdefault(page.numero, debut)

        for pages_cles in index.values():
            if len(pages_cles) < MIN_PAGES:
                continue
            if len(pages_cles) / total < FREQ_PLANCHER:
                continue
            if not any(num in numeros_calib for num in pages_cles):
                continue
            spans = {
                num: [(pages_cles[num], pages_cles[num] + w)] for num in pages_cles
            }
            touches = []
            for bloc in blocs:
                chevauchantes = sum(
                    1
                    for num in pages_cles
                    if num in bloc["emplacements"]
                    and any(
                        _chevauche(interval, spans[num][0])
                        for interval in bloc["emplacements"][num]
                    )
                )
                # FR-001 : la fusion n'est admise que si le chevauchement
                # se vérifie sur strictement plus de la moitié des pages
                # de la candidate (clarification du 2026-09-29, D1/D6 de
                # la feature 002) ; à la moitié exacte ou moins, la
                # candidate crée son propre bloc.
                if 2 * chevauchantes > len(pages_cles):
                    touches.append(bloc)
            if touches:
                cible = touches[0]
                for autre in touches[1:]:
                    for num, liste in autre["emplacements"].items():
                        for interval in liste:
                            cible["emplacements"][num] = _ajoute_intervalles(
                                cible["emplacements"].get(num, []), interval
                            )
                    blocs.remove(autre)
                for num, liste in spans.items():
                    for interval in liste:
                        cible["emplacements"][num] = _ajoute_intervalles(
                            cible["emplacements"].get(num, []), interval
                        )
            else:
                blocs.append({"emplacements": spans})

    def cle_tri(bloc: dict) -> tuple:
        num0 = min(
            bloc["emplacements"],
            key=lambda n: (position[n], bloc["emplacements"][n][0][0]),
        )
        return (
            position[num0],
            bloc["emplacements"][num0][0][0],
            -len(bloc["emplacements"]),
            -max(f - d for liste in bloc["emplacements"].values() for d, f in liste),
        )

    blocs.sort(key=cle_tri)

    motifs: list[Motif] = []
    for numero, bloc in enumerate(blocs, start=1):
        emplacements = {num: list(liste) for num, liste in bloc["emplacements"].items()}
        pages_motif = sorted(emplacements)
        num_long = max(
            emplacements,
            key=lambda n: (
                max(f - d for d, f in emplacements[n]),
                -position[n],
            ),
        )
        debut, fin = max(emplacements[num_long], key=lambda iv: iv[1] - iv[0])
        page_long = pages[position[num_long]]
        lignes_norm = page_long.lignes_norm[debut:fin]
        extrait = " / ".join(page_long.lignes[debut : debut + min(3, fin - debut)])
        motifs.append(
            Motif(
                id=f"M{numero:02d}",
                action=(
                    "supprimer"
                    if len(pages_motif) / total >= seuil / 100
                    else "conserver"
                ),
                lignes_norm=lignes_norm,
                extrait=extrait,
                frequence=round(len(pages_motif) / total, 2),
                pages=pages_motif,
                nb_lignes=fin - debut,
                emplacements=emplacements,
            )
        )
    return motifs
