"""Découpage du document en pages (research.md D4, FR-011).

Priorité aux séparateurs explicites « ## Page N: URL » ; à défaut, repli
heuristique déterministe sur des lignes frontières récurrentes ; si rien
de fiable n'est trouvé, le document reste une section unique — jamais de
pagination silencieuse et trompeuse.
"""

import re
from collections import Counter
from dataclasses import dataclass, field

from md_cleaner.normalisation import normaliser_ligne

RE_SEPARATEUR = re.compile(r"^#{1,6}\s*[Pp]age\s+(\d+)\s*(?::\s*(\S+))?\s*$")
MIN_FRONTIERES = 3


@dataclass
class Page:
    """Subdivision du document source (data-model.md)."""

    numero: int
    url_source: str | None
    lignes: list[str]
    lignes_norm: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.lignes_norm = [normaliser_ligne(ligne) for ligne in self.lignes]


def _sans_pages_vides_aux_bords(pages: list[Page]) -> list[Page]:
    """Retire les pages entièrement vides en tête et en queue."""
    debut = 0
    while debut < len(pages) and not any(
        ligne.strip() for ligne in pages[debut].lignes
    ):
        debut += 1
    fin = len(pages)
    while fin > debut and not any(ligne.strip() for ligne in pages[fin - 1].lignes):
        fin -= 1
    pages = pages[debut:fin]
    for position, page in enumerate(pages, start=1):
        page.numero = position
    return pages


def _decouper_explicite(
    lignes: list[str], coupures: list[tuple[int, str | None]]
) -> list[Page]:
    """Le contenu suivant le séparateur « Page N » appartient à la page N."""
    pages: list[Page] = []
    if coupures[0][0] > 0 and any(ligne.strip() for ligne in lignes[: coupures[0][0]]):
        pages.append(Page(1, None, list(lignes[: coupures[0][0]])))
    for position, (index, url) in enumerate(coupures):
        debut = index + 1
        fin = coupures[position + 1][0] if position + 1 < len(coupures) else len(lignes)
        pages.append(Page(len(pages) + 1, url, lignes[debut:fin]))
    return _sans_pages_vides_aux_bords(pages)


def _frontiere_heuristique(lignes: list[str]) -> int | None:
    """Ligne brute récurrente servant de frontière, ou None (D4).

    Déterministe : meilleure candidate par (nombre d'occurrences
    décroissant, première occurrence croissante). La candidate est
    comparée sur la forme brute (espaces de fin ignorés) : une vraie
    frontière de page se répète à l'identique, alors que des contenus
    distincts ne doivent pas être confondus par la normalisation
    (ex. les numéros d'étapes « 1 », « 2 », ... normalisés en <N>)."""
    compte: Counter[str] = Counter()
    premiere: dict[str, int] = {}
    for index, ligne in enumerate(lignes):
        cle = ligne.strip()
        if not cle:
            continue
        compte[cle] += 1
        premiere.setdefault(cle, index)
    candidates = [
        (nb, premiere[cle], cle) for cle, nb in compte.items() if nb >= MIN_FRONTIERES
    ]
    if not candidates:
        return None
    candidates.sort(key=lambda c: (-c[0], c[1], c[2]))
    cle = candidates[0][2]
    return premiere[cle]


def segmenter(lignes: list[str]) -> tuple[list[Page], str]:
    """Segmente le document ; renvoie (pages, mode de segmentation)."""
    coupures: list[tuple[int, str | None]] = []
    for index, ligne in enumerate(lignes):
        match = RE_SEPARATEUR.match(ligne.strip())
        if match:
            coupures.append((index, match.group(2)))

    if len(coupures) >= 2:
        return _decouper_explicite(lignes, coupures), "explicite"

    index_frontiere = _frontiere_heuristique(lignes)
    if index_frontiere is not None:
        cle = lignes[index_frontiere].strip()
        positions = [i for i, ligne in enumerate(lignes) if ligne.strip() == cle]
        contour: list[str] = []
        pages: list[Page] = []
        debut = 0
        for position in positions:
            pages.append(Page(len(pages) + 1, None, contour + lignes[debut:position]))
            contour = []
            debut = position + 1
        pages.append(Page(len(pages) + 1, None, contour + lignes[debut:]))
        return _sans_pages_vides_aux_bords(pages), "heuristique"

    return [Page(1, None, list(lignes))], "unique"
