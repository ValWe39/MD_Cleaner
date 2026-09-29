# Implementation Plan: Nettoyage de fichiers Markdown répétitifs

**Branch**: `007-Specs01` | **Date**: 2026-09-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-nettoyage-md-repetitif/spec.md`

## Summary

Outil CLI qui, à partir d'un fichier `.md` multi-pages (typiquement issu d'une conversion HTML → Markdown), détecte les motifs textuels répétés à travers les pages (navigation, fils d'Ariane, footers, filtres), produit un `.md` nettoyé ne conservant que le contenu de valeur, et en option une sortie paginée (marqueurs lisibles + cartographie JSON bloc → page) en vue d'un futur RAG. Détection déterministe par normalisation de lignes (URL/nombres/dates remplacés par jetons) et analyse de fréquence de blocs récurrents, avec seuil par défaut de 80 % des pages réglable par option. Dry-run produisant un rapport lisible et un fichier `suggestion.json` éditable consommé par le run de nettoyage. Zéro dépendance runtime (stdlib Python), 100 % local.

## Technical Context

**Language/Version**: Python 3.12 (aligné sur le job CI `setup-python 3.12` et les scripts `.github/workflows/scripts/` existants)

**Primary Dependencies**: aucune en runtime (stdlib : `argparse`, `re`, `json`, `pathlib`, `difflib`, `collections`, `unicodedata`) ; en développement uniquement : `pytest` (MIT), `ruff` (MIT, déjà en CI). Alternatives rejetées : `markdown-it-py` (l'entrée est du texte converti non garanti CommonMark ; la détection repose sur la récurrence de lignes/blocs, pas sur un AST), LLM (non déterministe, réseau, contraire au principe II).

**Storage**: fichiers locaux uniquement. Entrée : un `.md`. Sortie : `output/<run>/` (rapports, suggestion, fichiers nettoyés, cartographie). Aucune base de données, aucune persistance cachée (Data Retention : l'utilisateur supprime en effaçant `output/`).

**Testing**: `pytest` — `tests/unit/` (normalisation, segmentation, détection, seuil, ids déterministes) et `tests/integration/` avec les fixtures `Examples/Exemple_1` et `Examples/Exemple_2` (fixtures commitées, exclues des hooks de lint ; cf. branche `007-Specs01`).

**Target Platform**: CLI locale multi-OS (développement Windows, CI Linux) ; entièrement hors-ligne.

**Project Type**: cli

**Performance Goals**: plusieurs centaines de pages (~10 Mo) traitées en moins de 60 s sur machine de bureau standard (SC-003) ; complexité visée O(lignes × taille fenêtre de motif) par passe.

**Constraints**: déterminisme octet par octet à entrées/options identiques (FR-005 : pas d'aléa, pas d'horloge dans les sorties, itérations déterministes) ; zéro appel réseau (principe II) ; mémoire raisonnable (< 1 Go pour 10 Mo d'entrée).

**Scale/Scope**: documents de 1 à ~1 000 pages ; un fichier par exécution (FR-001) ; fichiers d'exemples de 75 Ko à 125 Ko comme référence.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe / exigence | Statut | Justification |
| ------------------- | ------ | ------------- |
| I. Isolation des secrets (NON NÉGOCIABLE) | PASS | L'outil ne manipule aucun secret ; aucun identifiant requis ; pas de config sensible. |
| II. Local-first & confidentialité (NON NÉGOCIABLE) | PASS | Zéro appel réseau ; stdlib uniquement ; tout traitement et stockage local. |
| III. Open-source & sans trackers | PASS | Zéro dépendance runtime ; dev-only MIT (pytest, ruff) déjà autorisés par les amendements. |
| IV. Simplicité (YAGNI) | PASS | Un point d'entrée CLI, 9 modules courts, pas de plugins ni d'abstraction prématurée. |
| Outils souverains | PASS (note) | Stdlib Python et outils déjà en place dans le dépôt ; aucune nouvelle dépendance externe. |
| Config Validation | PASS | Validation du chemin d'entrée et des options au lancement, échec rapide avec message clair (FR-015). |
| Path Isolation | PASS | Chemins passés en arguments ; défauts relatifs (`./output`), jamais de chemin personnel codé en dur. |
| No Cloud / No Trackers / Network Surface | PASS | Aucun trafic sortant, aucune télémétrie. |
| Data Retention | PASS | Résultats uniquement dans `output/` ; aucune copie cachée. |
| Compliance CI (Ruff, markdownlint, pip-audit) | PASS | Code sous `md_cleaner/` et `tests/` linté par Ruff ; création de `requirements.txt` (dév) répare par ailleurs le job `audit` hebdo qui échoue sur son absence. |

**Re-check post-Phase 1** : aucun changement — la conception (détail dans [research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/)) n'introduit aucune dépendance, aucun appel réseau, aucun secret. Aucune violation à justifier.

## Project Structure

### Documentation (this feature)

```text
specs/001-nettoyage-md-repetitif/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
│   ├── cli.md           # Schéma des commandes CLI, options, codes retour
│   └── formats.md       # Formats des fichiers échangés (suggestion.json, cartographie.json)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
md_cleaner/
├── __init__.py
├── __main__.py        # python -m md_cleaner
├── cli.py             # argparse : commandes, options, codes retour
├── segmentation.py    # découpage en pages (séparateurs explicites, repli heuristique)
├── normalisation.py   # normalisation de lignes (URL, nombres, dates → jetons)
├── detection.py       # blocs récurrents, fréquences, seuil 80 %
├── suggestion.py     # suggestion.json : écriture, lecture, validation
├── nettoyage.py       # production de nettoye.md et nettoye-pagine.md
├── cartographie.py    # cartographie.json (bloc → page, URL source)
└── sortie.py          # dossier output/, sous-dossiers numérotés ou dérivés du titre

tests/
├── unit/
└── integration/       # fixtures : Examples/Exemple_1, Examples/Exemple_2

pyproject.toml         # packaging, console script md-cleaner, métadonnées dev
requirements.txt       # dépendances dev (pytest) — consommé par le job audit CI
```

**Structure Decision**: projet unique (pas de `src/` imbriqué, pas de multi-projet — YAGNI). Le paquet `md_cleaner/` vit à la racine derrière un point d'entrée unique ; les modules reflètent les étapes du pipeline (segmenter → normaliser → détecter → suggérer → nettoyer → cartographier) pour rester testables isolément. Les fixtures de tests d'intégration pointent vers `Examples/` via chemins relatifs, déjà commités et exclus du lint.

## Suivi de complexité

> **Fill ONLY if Constitution Check has violations that must be justified**

Aucune violation de la constitution à justifier.
