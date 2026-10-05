# Implementation Plan: nom de sortie dérivé du document source

**Branch**: `014-outputfix` | **Date**: 2026-10-05 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/006-nom-sortie-source/spec.md`, issue du handoff de l'assessment `nom-sortie-nettoye` (verdict go, option A), clarifications arbitrées en session du 2026-10-05 (position du suffixe de collision, troncature brute).

## Summary

Nommer le fichier nettoyé d'un run d'après son document d'entrée : `<20 premiers caractères du nom d'entrée, blancs remplacés par _>-nettoye.md` au lieu du nom fixe `nettoye.md`, avec suffixe numérique `-1`, `-2`, ... à la fin du nom en cas de conflit, jamais d'écrasement. Deux fonctions nouvelles : une transformation pure dans `normalisation.py` (D1, D2) et une résolution de collision dans `sortie.py` (D4) ; câblage en deux points de `cli.py` (D5) ; mise à jour des ~20 chemins attendus des tests d'intégration, du README et du contrat CLI de la feature 001 dans la même livraison (D6). Aucune nouvelle option CLI, aucun autre artefact touché.

## Technical Context

**Language/Version**: Python 3.12 (existant — déploiement identique aux features 001-005).

**Primary Dependencies**: aucune en runtime (stdlib) ; dev : pytest, ruff (en place). Surface modifiée : `md_cleaner/normalisation.py` (nouvelle fonction pure), `md_cleaner/sortie.py` (résolution de collision), `md_cleaner/cli.py` (câblage, 2 points) ; révision du contrat de la feature 001 (`specs/001-nettoyage-md-repetitif/contracts/cli.md`, table des artefacts).

**Storage**: inchangé — fichiers locaux dans `output/<run>/`.

**Testing**: `pytest` existant ; unitaires : `tests/unit/test_normalisation.py` (nommage : nominal, espaces/tabulations, troncature à 20 points de code, accents conservés, blancs en extrémités, stem uniquement de blancs) et nouveaux tests de collision de sortie ; intégration : mise à jour des ~20 chemins attendus dans `tests/integration/` (`test_nettoyage_simple`, `test_nettoyage_liens`, `test_dry_run`, `test_extrait`, `test_calibrage`, `test_decidabilite`, `test_pagination`) + nouveaux tests US1-US3 (nom exact, troncature, collision `-1`/`-2` sans écrasement).

**Target Platform**: CLI locale multi-OS, hors-ligne (inchangé).

**Project Type**: cli (modification d'un outil existant).

**Performance Goals**: inchangé ; le nommage est O(longueur du stem), la boucle de collision est sans itération en pratique (dossier de run fraîchement créé) — négligeable.

**Constraints**: déterminisme du nom depuis le seul stem d'entrée (SC-002) ; jamais d'écrasement (FR-004, SC-003) ; artefacts secondaires et dossiers de run inchangés (FR-005) ; message de fin affichant le chemin réel (FR-006).

**Scale/Scope**: une règle de nommage bornée à un artefact ; corpus de validation = noms construits (nominal, > 20 caractères, espaces, accents) sur les documents d'exemple existants.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe / exigence | Statut | Justification |
| ------------------- | ------ | ------------- |
| I. Isolation des secrets (NON NÉGOCIABLE) | PASS | Aucun secret manipulé ; inchangé. |
| II. Local-first & confidentialité (NON NÉGOCIABLE) | PASS | Aucun appel réseau ; traitement local uniquement. |
| III. Open-source & sans trackers | PASS | Aucune nouvelle dépendance ; stdlib uniquement. |
| IV. Simplicité (YAGNI) | PASS | Deux petites fonctions, aucun nouveau drapeau, aucune option ; réutilisation de `slug_titre` rejetée car incompatible avec la règle de la spec (D1) ; la boucle de collision est une garantie bornée, pas une généralisation. |
| Config Validation | PASS | Aucune option CLI modifiée ; codes retour inchangés. |
| Path Isolation | PASS | Chemins inchangés (`--sortie`, dossiers de run) ; seul le nom de fichier change. |
| No Cloud / No Trackers / Network Surface | PASS | Aucun trafic. |
| Data Retention | PASS | Sorties uniquement dans `output/` (inchangé) ; aucune copie cachée. |
| Compliance CI (Ruff, markdownlint, secrets) | PASS | Code sous `md_cleaner/` et `tests/` linté ; artefacts de spec rédigés conformément à la config markdownlint en place (MD038 traité au commit de la spec). |

**Re-check post-Phase 1** : aucun changement — les décisions D1-D6 de [research.md](./research.md) n'introduisent ni dépendance, ni réseau, ni secret ; le contrat observable ([contracts/nommage-sortie.md](./contracts/nommage-sortie.md)) est borné à un seul artefact, et la garantie de non-écrasement (D4) renforce la sûreté sans complexifier l'interface.

## Project Structure

### Documentation (this feature)

```text
specs/006-nom-sortie-source/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (décisions D1-D6)
├── data-model.md        # Phase 1 output (entité « Nom de sortie dérivé »)
├── quickstart.md        # Phase 1 output (scénarios de validation)
├── contracts/
│   └── nommage-sortie.md  # Phase 1 output (contrat CLI observable ; révise 001/contracts/cli.md)
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
md_cleaner/
├── normalisation.py    # + nom_sortie_nettoye(stem) : transformation pure (D1, D2, D3)
├── sortie.py            # + résolution de collision du nom de fichier (D4)
└── cli.py               # câblage : calcul du nom, écriture, message (D5)

tests/
├── unit/
│   ├── test_normalisation.py   # tests du nommage
│   └── test_sortie.py          # tests de collision (nouveau)
└── integration/                 # ~20 chemins attendus mis à jour + tests US1-US3

README.md                          # 2 mentions mises à jour
specs/001-nettoyage-md-repetitif/contracts/cli.md  # table des artefacts révisée (D6)
```

**Structure Decision**: structure existante du dépôt conservée (aucun nouveau répertoire hors `contracts/` de la feature) ; deux fonctions placées dans les modules qui portent déjà leurs responsabilités (`normalisation.py` pour la transformation de chaînes, `sortie.py` pour l'emplacement et les collisions), conformément au précédent des features 001-005.

## Suivi de complexité

> **Fill ONLY if Constitution Check has violations that must be justified**

Aucune violation : tableau vide — le check constitutionnel passe sans exception.
