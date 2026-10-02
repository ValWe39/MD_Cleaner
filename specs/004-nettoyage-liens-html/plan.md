# Implementation Plan: Nettoyage des destinations de liens résiduelles à l'écriture de la sortie

**Branch**: `004-nettoyage-liens-html` | **Date**: 2026-10-02 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/004-nettoyage-liens-html/spec.md`, issue du handoff de l'assessment `nettoyage-liens-html` (mesures grep sur `output/004/nettoye.md` incluses).

## Summary

Retirer des sorties finales (`nettoye.md`, `nettoye-pagine.md`) les destinations de liens inline de la forme `](</...>)`, sans toucher au libellé `[texte]` ni au reste de la ligne, ni à la détection, aux extraits, à la suggestion ni à la cartographie. Une seule règle textuelle déterministe appliquée au texte des blocs à l'écriture, activée par défaut ; le drapeau `--conserver-liens` rétablit le comportement antérieur (identité octet par octet). Migration bornée des contenus attendus des tests qui comparent les sorties.

## Technical Context

**Language/Version**: Python 3.12 (existant — déploiement identique aux features 001-003).

**Primary Dependencies**: aucune en runtime (stdlib) ; dev : pytest, ruff (en place). Surface modifiée : `md_cleaner/nettoyage.py` (passe de nettoyage à l'écriture), `md_cleaner/cli.py` (option `--conserver-liens`), le contrat CLI de la feature 001 (`specs/001-nettoyage-md-repetitif/contracts/cli.md`, révision options).

**Storage**: inchangé — fichiers locaux dans `output/<run>/`.

**Testing**: `pytest` existant ; nouveaux tests unitaires (règle sur cas limites : plusieurs liens par ligne, libellé vide, caractères encodés, destination absolue non touchée, marqueurs de page préservés) et d'intégration (0 destination sur Exemple_2, identité octet par octet avec `--conserver-liens`, identité sur corpus sans liens, marqueurs `--pagine` intacts). Migration : `tests/integration/test_nettoyage_simple.py` (contenus attendus contenant des liens) ; tests de détection/normalisation non impactés (fixtures en entrée, la passe vit en aval).

**Target Platform**: CLI locale multi-OS, hors-ligne (inchangé).

**Project Type**: cli (modification d'un outil existant).

**Performance Goals**: inchangé ; une substitution regex par ligne conservée — O(lignes), négligeable (3110 lignes porteuses sur le corpus le plus riche).

**Constraints**: déterminisme octet par octet (FR-007) ; aucune modification du texte hors destinations (FR-001) ; ids de motifs et cartographie inchangés (FR-005) ; marqueurs `<!-- page: N -->` préservés (FR-004).

**Scale/Scope**: corpus de validation inchangé (`Examples/Exemple_1`, `Exemple_2`).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe / exigence | Statut | Justification |
| ------------------- | ------ | ------------- |
| I. Isolation des secrets (NON NÉGOCIABLE) | PASS | Aucun secret manipulé ; inchangé. |
| II. Local-first & confidentialité (NON NÉGOCIABLE) | PASS | Aucun appel réseau ; traitement local uniquement. |
| III. Open-source & sans trackers | PASS | Aucune nouvelle dépendance ; stdlib `re` uniquement. |
| IV. Simplicité (YAGNI) | PASS | Une règle, un drapeau, demandés par l'utilisateur (assessment go du 2026-10-02) ; pas d'extension aux URL absolues ni aux vraies balises HTML (bornes explicites de la spec). |
| Config Validation | PASS | `--conserver-liens` est un booléen sans argument ; aucune validation supplémentaire requise ; codes retour inchangés. |
| Path Isolation | PASS | Chemins inchangés. |
| No Cloud / No Trackers / Network Surface | PASS | Aucun trafic. |
| Data Retention | PASS | Sorties uniquement dans `output/` (inchangé). |
| Compliance CI (Ruff, markdownlint) | PASS | Code sous `md_cleaner/` et `tests/` linté ; specs sous config MD013 locale. |

**Re-check post-Phase 1** : aucun changement — les décisions D1-D6 de [research.md](./research.md) n'introduisent ni dépendance, ni réseau, ni secret ; la règle est bornée à `](</...>)` (D1) et la préservation des marqueurs est testée (D5).

## Project Structure

### Documentation (this feature)

```text
specs/004-nettoyage-liens-html/
├── plan.md                    # Ce fichier
├── research.md                # Phase 0 : décisions D1-D6
├── data-model.md              # Phase 1 : entités impactées
├── quickstart.md              # Phase 1 : validation de bout en bout
├── contracts/
│   └── nettoyage-liens.md     # Phase 1 : règle de nettoyage + option CLI
└── tasks.md                   # Phase 2 (/speckit-tasks — pas encore créé)
```

### Source Code (repository root — fichiers modifiés, structure inchangée)

```text
md_cleaner/
├── nettoyage.py     # MODIFIÉ : fonction pure de retrait des destinations,
│                    #   appliquée au texte des blocs à l'écriture des deux
│                    #   sorties .md (D2, D3)
└── cli.py          # MODIFIÉ : option --conserver-liens (store_true),
                     #   propagée à l'écriture (D4)

tests/
├── unit/
│   └── test_nettoyage_liens.py    # NOUVEAU : règle sur cas limites (D1, D5)
├── integration/
│   └── test_nettoyage_simple.py  # MIGRÉ : contenus attendus sans destinations
└── integration/
    └── test_nettoyage_liens.py    # NOUVEAU : SC-001 à SC-004 (D6)
```

**Structure Decision**: structure existante conservée ; la passe vit dans `md_cleaner/nettoyage.py` (déjà responsable de l'écriture des sorties), l'option dans `md_cleaner/cli.py` (seul point d'entrée des paramètres).
