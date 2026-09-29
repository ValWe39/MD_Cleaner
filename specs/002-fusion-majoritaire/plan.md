# Implementation Plan: Décidabilité des motifs au dry-run (fusion majoritaire)

**Branch**: `002-fusion-majoritaire` | **Date**: 2026-09-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-fusion-majoritaire/spec.md`, issue du handoff de l'assessment `granularite-motifs` (mesures du prototype incluses).

## Summary

Modifier la règle de fusion de la détection : deux blocs récurrents ne fusionnent que si leur chevauchement se vérifie sur **strictement plus de la moitié** des pages concernées par la fenêtre candidate (au lieu d'« au moins une page » aujourd'hui). Les zones d'interface (filtres, pagination) et les métadonnées récurrentes de contenu deviennent des motifs distincts, individuellement actionnables dans la suggestion. Le rapport dry-run est restructuré en deux sections (décisions requises / motifs conservés par défaut) pour absorber la multiplication des motifs (~25 sur un document riche, dont 4-5 exigent une décision). Documentation de l'instabilité des ids entre versions. Zéro nouvelle dépendance, zéro nouvelle option CLI, aucune régression de la feature 001.

## Technical Context

**Language/Version**: Python 3.12 (existant — déploiement identique à la feature 001)

**Primary Dependencies**: aucune en runtime (stdlib) ; dev : pytest, ruff (déjà en place). La feature est une modification interne de `md_cleaner/detection.py` et de la génération du rapport dans `md_cleaner/suggestion.py`.

**Storage**: inchangé — fichiers locaux dans `output/<run>/`.

**Testing**: `pytest` existant ; nouveaux tests unitaires sur la frontière majoritaire stricte et tests d'intégration sur le corpus (Exemple_1 : identité avec la version précédente ; Exemple_2 : séparation filtres/métadonnées).

**Target Platform**: CLI locale multi-OS, hors-ligne (inchangé).

**Project Type**: cli (modification d'un outil existant).

**Performance Goals**: inchangé — la règle majoritaire n'ajoute qu'un comptage par bloc touché ; mesure de l'assessment : pas d'écart perceptible.

**Constraints**: déterminisme octet par octet (SC-005 de la spec 002) ; ids stables au sein d'une version ; aucune régression des SC de la feature 001 ; pas de constante exposée en CLI.

**Scale/Scope**: le corpus de validation reste `Examples/Exemple_1` et `Examples/Exemple_2` (mêmes structures que les documents réels de l'utilisateur).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe / exigence | Statut | Justification |
| ------------------- | ------ | ------------- |
| I. Isolation des secrets (NON NÉGOCIABLE) | PASS | Aucun secret manipulé ; inchangé. |
| II. Local-first & confidentialité (NON NÉGOCIABLE) | PASS | Aucun appel réseau ; traitement local uniquement. |
| III. Open-source & sans trackers | PASS | Aucune nouvelle dépendance ; stdlib uniquement. |
| IV. Simplicité (YAGNI) | PASS | Une règle de fusion modifiée + une re-présentation du rapport ; ni option, ni paramètre, ni plafond. |
| Config Validation | PASS | Comportement inchangé (codes retour 1/2/3). |
| Path Isolation | PASS | Chemins inchangés. |
| No Cloud / No Trackers / Network Surface | PASS | Aucun trafic. |
| Data Retention | PASS | Sorties uniquement dans `output/` (inchangé). |
| Compliance CI (Ruff, markdownlint) | PASS | Code sous `md_cleaner/` et `tests/` linté ; specs sous config MD013 locale. |

**Re-check post-Phase 1** : aucun changement — la conception (D1-D7 de [research.md](./research.md)) n'introduit ni dépendance, ni réseau, ni secret, ni option supplémentaire.

## Project Structure

### Documentation (this feature)

```text
specs/002-fusion-majoritaire/
├── plan.md                       # Ce fichier
├── research.md                   # Phase 0 : décisions D1-D7
├── data-model.md                 # Phase 1 : entités impactées
├── quickstart.md                 # Phase 1 : validation de bout en bout
├── contracts/
│   └── rapport-dry-run.md        # Phase 1 : structure indicative du rapport
└── tasks.md                      # Phase 2 (/speckit-tasks — pas encore créé)
```

### Source Code (repository root — fichiers modifiés, structure inchangée)

```text
md_cleaner/
├── detection.py      # MODIFIÉ : règle de fusion majoritaire stricte (D1, D2)
├── suggestion.py     # MODIFIÉ : rapport dry-run en deux sections (D3)
└── (autres modules inchangés)

tests/
├── unit/
│   └── test_detection.py   # ÉTENDU : frontière majoritaire stricte (D5)
└── integration/
    ├── test_nettoyage_simple.py  # ÉTENDU : non-régression Exemple_1 (SC-002)
    └── test_decidabilite.py      # NOUVEAU : séparation Exemple_2 (SC-001),
                                  #   comptage supprimer ≤ 5 (SC-003)

README.md             # MODIFIÉ : note d'instabilité des ids entre versions (D4)
```

**Structure Decision**: aucune nouvelle structure — la feature modifie deux modules existants et la documentation ; les tests s'étendent dans les fichiers existants plus un nouveau fichier d'intégration dédié aux critères propres à la feature (SC-001, SC-003).

## Suivi de complexité

> **Fill ONLY if Constitution Check has violations that must be justified**

Aucune violation de la constitution à justifier.
