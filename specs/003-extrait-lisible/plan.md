# Implementation Plan: Extraits lisibles et localisables dans la suggestion

**Branch**: `003-extrait-lisible` | **Date**: 2026-09-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-extrait-lisible/spec.md`, issue du handoff de l'assessment `lisibilite-dry-run` (mesures de saturation incluses).

## Summary

Rendre chaque motif de `suggestion.json` jugeable depuis le seul JSON : extrait de N lignes (défaut 5, option `--extrait N` 2-25) rendu en vrais sauts de ligne, ancré sur la première occurrence du motif ; nouveau champ position (page + lignes de la même première occurrence) ; garde-fou du rapport (neutralisation des sauts dans les cellules, troncature 120 conservée) ; validation stricte du champ position à la relecture avec tolérance de son absence (suggestions d'avant-feature). Aucune incidence sur la détection ou le nettoyage.

## Technical Context

**Language/Version**: Python 3.12 (existant — déploiement identique aux features 001/002)

**Primary Dependencies**: aucune en runtime (stdlib) ; dev : pytest, ruff (en place). Surface modifiée : `md_cleaner/suggestion.py` (enrichissement des motifs, validation, rapport), `md_cleaner/cli.py` (option `--extrait`), le contrat de la feature 001 (`specs/001-nettoyage-md-repetitif/contracts/formats.md`, révision FR-007).

**Storage**: inchangé — fichiers locaux dans `output/<run>/`.

**Testing**: `pytest` existant ; nouveaux tests unitaires (enrichissement, validation position, neutralisation rapport) et d'intégration (doublons ≤ 2 sur Exemple_2, N exact, position vérifiable, garde < 1 Mo, déterminisme, CLI bornes).

**Target Platform**: CLI locale multi-OS, hors-ligne (inchangé).

**Project Type**: cli (modification d'un outil existant).

**Performance Goals**: inchangé ; l'enrichissement est O(motifs × N) — négligeable.

**Constraints**: déterminisme octet par octet (SC-005) ; `suggestion.json` < 1 Mo sur le corpus pour toute valeur de N dans les bornes (SC-004, garde de la constitution contre la dérive vers un duplicatat du document) ; aucun changement de la détection, des actions ou du nettoyage (FR-008/FR-009).

**Scale/Scope**: corpus de validation inchangé (`Examples/Exemple_1`, `Exemple_2`).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe / exigence | Statut | Justification |
| ------------------- | ------ | ------------- |
| I. Isolation des secrets (NON NÉGOCIABLE) | PASS | Aucun secret manipulé ; inchangé. |
| II. Local-first & confidentialité (NON NÉGOCIABLE) | PASS | Aucun appel réseau ; traitement local uniquement. |
| III. Open-source & sans trackers | PASS | Aucune nouvelle dépendance ; stdlib uniquement. |
| IV. Simplicité (YAGNI) | PASS | L'option `--extrait` est demandée par l'utilisateur (règle de gouvernance du 2026-09-29, tour final de consolidation prévu) ; garde de taille < 1 Mo contre la dérive. |
| Config Validation | PASS | Bornes de l'option vérifiées (code 3) ; validation stricte du champ position (code 2). |
| Path Isolation | PASS | Chemins inchangés. |
| No Cloud / No Trackers / Network Surface | PASS | Aucun trafic. |
| Data Retention | PASS | Sorties uniquement dans `output/` (inchangé). |
| Compliance CI (Ruff, markdownlint) | PASS | Code sous `md_cleaner/` et `tests/` linté ; specs sous config MD013 locale ; titre de section du template renommé dès le plan (piège connu du hook constitution). |

**Re-check post-Phase 1** : aucun changement — la conception (D1-D7 de [research.md](./research.md)) n'introduit ni dépendance, ni réseau, ni secret ; la garde de taille est intégrée au design (D6).

## Project Structure

### Documentation (this feature)

```text
specs/003-extrait-lisible/
├── plan.md                    # Ce fichier
├── research.md                # Phase 0 : décisions D1-D7
├── data-model.md              # Phase 1 : entités impactées
├── quickstart.md              # Phase 1 : validation de bout en bout
├── contracts/
│   └── suggestion-extrait.md   # Phase 1 : schéma extrait + position + option
└── tasks.md                   # Phase 2 (/speckit-tasks — pas encore créé)
```

### Source Code (repository root — fichiers modifiés, structure inchangée)

```text
md_cleaner/
├── suggestion.py   # MODIFIÉ : enrichissement (extrait N lignes + position),
│                   #   validation stricte du champ position,
│                   #   neutralisation des sauts dans le rapport (D1, D4, D5)
└── cli.py          # MODIFIÉ : option --extrait N, borne 2-25, défaut 5,
                    #   aide documentant l'effet limité au dry-run (D2)

tests/
├── unit/
│   ├── test_suggestion.py     # ÉTENDU : enrichissement, validation position
│   └── (rapport : neutralisation)
└── integration/
    └── test_extrait.py        # NOUVEAU : doublons ≤ 2, N exact, position
                               #   vérifiable, < 1 Mo, CLI bornes (D6)

specs/001-nettoyage-md-repetitif/contracts/formats.md
                    # MODIFIÉ à l'implémentation : clause « extrait ≤ 3 lignes
                    #   jointes par " / " » révisée (FR-007, D7)
```

**Structure Decision**: aucun nouveau module — `detection.py` n'est **pas** modifié : l'extrait et la position sont calculés après la détection, depuis les emplacements existants, dans une fonction d'enrichissement de `suggestion.py` (D1). Le périmètre de code reste deux fichiers de production.

## Suivi de complexité

> **Remplir UNIQUEMENT si le Constitution Check a des violations à justifier**

Aucune violation de la constitution à justifier.
