"""Résolution du lot d'une invocation multi-entrées (feature 007, D2/D3).

Chaque entrée positionnelle est développée en documents à traiter :

- un fichier est retenu tel quel à sa position, doublons compris ; un
  chemin invalide transite jusqu'au traitement documentaire (il y
  échoue avec l'erreur d'entrée actuelle) ;
- un dossier est développé en ses fichiers ``.md`` de premier niveau,
  triés par nom, non récursif (FR-002, précédent ``charger_echantillon``) ;
  les autres fichiers sont ignorés sans message ;
- un dossier sans aucun fichier ``.md`` est ignoré avec un message
  explicite (FR-008).
"""

from pathlib import Path


def resoudre_lot(entrees: list[Path]) -> tuple[list[Path], list[str]]:
    """Développe les entrées positionnelles en lot de documents.

    Retourne (documents, avertissements) : les documents dans l'ordre
    d'apparition des arguments, doublons conservés (jamais dédupliqués
    silencieusement) ; les avertissements signalent les entrées ignorées.
    """
    documents: list[Path] = []
    avertissements: list[str] = []
    for entree in entrees:
        entree = Path(entree)
        if entree.is_dir():
            fichiers = sorted(
                (
                    f
                    for f in entree.iterdir()
                    if f.is_file() and f.suffix.lower() == ".md"
                ),
                key=lambda f: f.name,
            )
            if fichiers:
                documents.extend(fichiers)
            else:
                avertissements.append(f"entrée ignorée : {entree} (aucun fichier .md)")
        else:
            documents.append(entree)
    return documents, avertissements
