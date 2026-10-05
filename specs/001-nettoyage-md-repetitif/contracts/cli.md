# Contrat CLI : md-cleaner

**Feature**: 001-nettoyage-md-repetitif | **Date**: 2026-09-29 | **Source**: [spec.md](./spec.md), [research.md](./research.md)

L'outil expose un point d'entrée unique en ligne de commande. Un run = un fichier d'entrée (FR-001). Tout traitement est local et hors-ligne.

## Point d'entrée

```text
md-cleaner <fichier.md> [options]        # console script
python -m md_cleaner <fichier.md> ...    # équivalent
```

## Options

| Option | Argument | Défaut | Exigence | Description |
| ------ | -------- | ------ | -------- | ----------- |
| `--dry-run` | — | désactivé | FR-007 | Mode validation : produit `rapport-dry-run.md` + `suggestion.json` dans le dossier du run, sans écrire de fichier nettoyé |
| `--suggestion` | chemin | auto | FR-008 | Consomme un `suggestion.json` (édité ou non) au lieu de recalculer ; incohérent avec `--dry-run` |
| `--pagine` | — | désactivé | FR-009 | Produit en plus `nettoye-pagine.md` (marqueurs lisibles) et `cartographie.json` |
| `--conserver-liens` | — | nettoyage actif | 004 : FR-002, FR-003 ; 005 : FR-004 | Conserve les destinations de liens inline `](<...>)` (tout schéma, titre éventuel compris) dans `nettoye.md` et `nettoye-pagine.md` ; sans le drapeau, elles sont retirées à l'écriture (features 004 et 005) |
| `--seuil` | entier 2–100 | 80 | FR-002 | Seuil de fréquence (% de pages) au-delà duquel un motif est proposé à la suppression |
| `--echantillon` | dossier | auto-calibrage | FR-012 | Calibrage sur un échantillon fourni (≤ 5 fichiers `.md`, triés par nom) |
| `--calibrage` | entier 2–50 | 5 | FR-013 | Nombre N de premières pages utilisées par l'auto-calibrage |
| `--sortie` | dossier | `./output` | FR-006 | Dossier racine des sorties |
| `--nom-titre` | entier 5–100 | numérotation | FR-006 | Nomme le sous-dossier du run d'après les X premiers caractères du slug du titre |

## Comportements par défaut (suggestion par défaut = saut du dry-run)

- **Sans `--dry-run` ni `--suggestion`** : l'outil détecte, applique la suggestion par défaut (tout motif ≥ seuil → supprimer) et écrit les sorties — c'est le chemin « sauter le dry-run » de FR-008.
- **Avec `--suggestion`** : la détection n'est pas recalculée ; le fichier fourni fait foi (validation stricte : JSON invalide, `version` ≠ 1, `source` ne correspondant pas à l'entrée, id inconnu, `action` invalide → échec rapide).
- **Avec `--dry-run`** : aucune sortie nettoyée ; le rapport liste aussi les motifs détectés **sous le seuil** (décision humaine) et signale les cas limites (FR-016 : document trop court, sortie quasi vide, segmentation heuristique).

## Fichiers produits par mode

| Mode | Fichiers dans `output/<run>/` |
| ---- | ----------------------------- |
| nettoyage simple | `nettoye.md` |
| nettoyage + `--pagine` | `nettoye.md`, `nettoye-pagine.md`, `cartographie.json` |
| `--dry-run` | `rapport-dry-run.md`, `suggestion.json` |

## Messages et rapports

- Langue des messages : français.
- Chaque avertissement (FR-016) est écrit sur stderr et figure dans le rapport : document à page unique, motifs à fréquence partielle, sortie quasi vide, pagination recréée par heuristique.

## Codes retour

| Code | Signification |
| ---- | ------------- |
| 0 | Succès (y compris dry-run avec avertissements) |
| 1 | Entrée invalide : fichier absent, illisible, non-`.md`, dossier de sortie non créable |
| 2 | Artefact fourni invalide : `suggestion.json` invalide ou incohérent, `--echantillon` vide ou > 5 fichiers |
| 3 | Usage invalide : combinaison d'options interdite, argument hors bornes |

## Exemples

```bash
# Nettoyage simple, suggestion par défaut, auto-calibrage, sortie numérotée
md-cleaner Examples/Exemple_1/2.Input/consolidated.md

# Dry-run pour validation humaine
md-cleaner consolidated.md --dry-run

# Nettoyage après édition de la suggestion
md-cleaner consolidated.md --suggestion output/001/suggestion.json

# Sortie paginée pour RAG, seuil plus strict, run nommé d'après le titre
md-cleaner consolidated.md --pagine --seuil 90 --nom-titre 30
```

Les formats des fichiers échangés (`suggestion.json`, `cartographie.json`) sont spécifiés dans [formats.md](./formats.md).
