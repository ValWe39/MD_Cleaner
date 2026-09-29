# MD_Cleaner

Outil de nettoyage de fichiers Markdown multi-pages : il détecte les
éléments répétitifs (menus de navigation, fils d'Ariane, pieds de page,
filtres, pagination d'interface) et ne conserve que le contenu textuel
de valeur. 100 % local, déterministe, zéro dépendance runtime.

## Installation

Python 3.12 ou supérieur requis.

    pip install -e .
    pip install -r requirements.txt   # dépendances de développement

## Usage

    md-cleaner <fichier.md> [options]

Un run = un fichier. La sortie va dans `output/<run>/nettoye.md`.

### Options

| Option | Effet |
| ------ | ----- |
| `--dry-run` | rapport + `suggestion.json`, sans nettoyage |
| `--suggestion F` | applique un `suggestion.json` édité |
| `--pagine` | ajoute `nettoye-pagine.md` + `cartographie.json` |
| `--seuil N` | seuil de fréquence en % de pages (défaut 80) |
| `--echantillon D` | calibrage sur un échantillon (5 fichiers max) |
| `--calibrage N` | pages d'auto-calibrage (défaut 5) |
| `--sortie D` | dossier racine des sorties (défaut `./output`) |
| `--nom-titre X` | nomme le run d'après le titre (X caractères) |

### Exemples

    # Nettoyage simple, suggestion par défaut appliquée
    md-cleaner Examples/Exemple_1/2.Input/consolidated.md

    # Validation humaine avant nettoyage
    md-cleaner consolidated.md --dry-run

    # Nettoyage après édition de la suggestion
    md-cleaner consolidated.md --suggestion output/001/suggestion.json

    # Sortie paginée pour un usage RAG
    md-cleaner consolidated.md --pagine

Contrat CLI complet : `specs/001-nettoyage-md-repetitif/contracts/cli.md`.

## Développement

    pytest                              # tests unitaires et intégration
    pre-commit run --all-files         # hooks du dépôt

Conformité à la constitution du projet (v1.4.0) : local-first sans
réseau, aucune dépendance runtime, secrets exclus, sorties uniquement
dans `output/` (supprimables par l'utilisateur).
