"""Normalisation de lignes et slug de titre (research.md D3 et D8).

La normalisation remplace par des jetons les parties variables des lignes
(URL, dates, nombres) afin qu'un motif répétitif soit reconnu identique
d'une page à l'autre malgré ses parties changeantes (FR-003).
"""

import re
import unicodedata

_RE_URL = re.compile(r"https?://\S+|www\.\S+")
_MOIS = (
    "janvier|février|mars|avril|mai|juin|juillet|août|"
    "septembre|octobre|novembre|décembre|"
    "january|february|march|april|may|june|july|august|"
    "september|october|november|december"
)
_RE_DATE_MOIS = re.compile(rf"\b\d{{1,2}}\s+(?:{_MOIS})\s+\d{{4}}\b", re.IGNORECASE)
_RE_DATE_ISO = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
_RE_DATE_NUM = re.compile(r"\b\d{1,2}[/.]\d{1,2}[/.]\d{2,4}\b")
_RE_NOMBRE = re.compile(r"\d+(?:[.,]\d+)?")
_RE_ESPACES = re.compile(r"\s+")


def normaliser_ligne(ligne: str) -> str:
    """Normalise une ligne : URL, dates et nombres remplacés par des jetons."""
    s = ligne.strip()
    s = _RE_URL.sub("<URL>", s)
    s = _RE_DATE_MOIS.sub("<DATE>", s)
    s = _RE_DATE_ISO.sub("<DATE>", s)
    s = _RE_DATE_NUM.sub("<DATE>", s)
    s = _RE_NOMBRE.sub("<N>", s)
    s = _RE_ESPACES.sub(" ", s)
    return s


def slug_titre(texte: str, x: int) -> str:
    """Slug ASCII des x premiers caractères significatifs du titre (D8)."""
    s = unicodedata.normalize("NFKD", texte)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:x]
