# Implementation Plan: Traitement multi-documents en une invocation

**Branch**: `015-multi-docs` | **Date**: 2026-10-05 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/007-traitement-multi-documents/spec.md`, issue du handoff de l'assessment `multi-documents` (verdict go, option A « lot positionnel minimal »), arbitrages tranchés en session du 2026-10-05 : avertissement + neutralisation des options non applicables en lot, poursuite avec fail-fast au troisième échec consécutif, dossier sans `.md` ignoré avec message.

## Summary

Étendre le point d'entrée CLI à plusieurs entrées positionnelles — fichiers `.md` et/ou dossiers dont seuls les `.md` de premier niveau sont retenus (triés par nom) — avec un traitement séquentiel par document strictement identique à l'actuel : chaque document emprunte le chemin de code existant et produit son propre dossier de run et ses sorties habituelles (FR-003, SC-002 par construction). Les options de cleaning s'appliquent à l'identique à tous (FR-004) ; `--dry-run` et `--suggestion` sont neutralisées avec avertissement explicite dès que le lot contient plus d'un document (FR-006) ; un échec de document est signalé, le lot poursuit, et s'arrête net au troisième échec consécutif (FR-007) ; code retour 0 si et seulement si tout le lot a réussi. Trois chantiers : résolution du lot (fonction pure nouvelle), refactor de `cli.py` en « résoudre le lot puis traiter chaque document » sans toucher aux modules de nettoyage, et révision du contrat CLI de la feature 001 (FR-001 devient multi-entrées, cas mono-document strictement inchangé).

## Technical Context

**Language/Version**: Python 3.12 (existant — déploiement identique aux features 001-006).

**Primary Dependencies**: aucune en runtime (stdlib : `argparse`, `pathlib`) ; dev : pytest, ruff (en place). Surface modifiée : `md_cleaner/cli.py` (argument positionnel `nargs="+"`, extraction du traitement mono-document en fonction, boucle de lot, avertissements, compteur d'échecs consécutifs), nouveau module `md_cleaner/lot.py` (résolution du lot, fonction pure), révision du contrat CLI de la feature 001 (`specs/001-nettoyage-md-repetitif/contracts/cli.md`) et du README. Aucun module de nettoyage (`nettoyage`, `detection`, `segmentation`, `normalisation`, `sortie`, `suggestion`, `cartographie`) n'est modifié.

**Storage**: inchangé — fichiers locaux dans `output/<run>/`, un dossier de run par document.

**Testing**: `pytest` existant. Unitaires : `tests/unit/test_lot.py` (résolution : fichiers seuls, dossier avec `.md` seuls retenus, mélange fichier+dossier, dossier sans `.md` ignoré avec message, tri alphabétique du dossier, doublons conservés). Intégration : `tests/integration/test_lot.py` (parité octet par octet lot vs individuel sur les 3 exemples de référence, avertissement + neutralisation de `--dry-run`/`--suggestion` en lot, échec isolé → reste du lot traité + code 1, trois échecs consécutifs → arrêt net, dossier sans `.md` ignoré, mono-document strictement inchangé). La suite existante doit passer sans relâchement (SC-005).

**Target Platform**: CLI locale multi-OS, hors-ligne (inchangé).

**Project Type**: cli (modification d'un outil existant).

**Performance Goals**: inchangé ; traitement séquentiel volontaire, la parallélisation est un non-goal du problem.md.

**Constraints**: parité octet par octet entre lot et invocation individuelle (SC-002) ; rétrocompatibilité stricte du mono-document (FR-005, SC-005) ; jamais d'écrasement (FR-010, mécanisme de suffixe existant) ; déterminisme de l'ordre (ordre d'apparition, tri par nom dans un dossier) ; non-silence sur toute option neutralisée ou entrée ignorée (SC-004).

**Scale/Scope**: corpus de taille modeste (quelques documents), aucun plafond introduit (assumption de la spec) ; corpus de validation = les 3 exemples de référence (`Examples/*/2.Input/`) et dossiers construits en test.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe / exigence | Statut | Justification |
| ------------------- | ------ | ------------- |
| I. Isolation des secrets (NON NÉGOCIABLE) | PASS | Aucun secret manipulé ; aucune donnée nouvelle en entrée. |
| II. Local-first & confidentialité (NON NÉGOCIABLE) | PASS | Aucun appel réseau ; lecture de fichiers locaux supplémentaires uniquement (dossiers passés en argument par l'utilisateur). |
| III. Open-source & sans trackers | PASS | Aucune nouvelle dépendance ; stdlib uniquement. |
| IV. Simplicité (YAGNI) | PASS | Une fonction pure nouvelle + un refactor d'aiguillage dans `cli.py` ; aucune nouvelle option CLI ; aucun module de nettoyage touché ; le fail-fast au 3e échec consécutif est borné par la spec, pas généralisé ; le lot reste une simple itération, pas une infrastructure de lot. |
| Config Validation | PASS | Échec rapide conservé : arguments invalides (code 3) avant tout traitement, entrée non résolue signalée, lot vide → erreur (code 1). |
| Path Isolation | PASS | Aucun chemin codé en dur ; l'utilisateur passe les dossiers ; sorties dans `output/` via `--sortie` (inchangé). |
| No Cloud / No Trackers / Network Surface | PASS | Aucun trafic. |
| Data Retention | PASS | Sorties uniquement dans `output/` ; aucune copie cachée ; l'utilisateur garde le contrôle par suppression. |
| Compliance CI (Ruff, markdownlint, secrets) | PASS | Code sous `md_cleaner/` et `tests/` linté (ruff) ; artefacts de spec sous `specs/` (MD013 désactivée par la config en place, autres règles respectées). |

**Re-check post-Phase 1** : aucun changement — les décisions D1-D9 de [research.md](./research.md) n'introduisent ni dépendance, ni réseau, ni secret ; le contrat observable ([contracts/multi-entrees.md](./contracts/multi-entrees.md)) révisant le point d'entrée de 001 reste borné à l'argumentaire positionnel, aux avertissements et aux codes retour déjà définis.

## Project Structure

### Documentation (this feature)

```text
specs/007-traitement-multi-documents/
├── plan.md                  # This file (/speckit-plan command output)
├── research.md              # Phase 0 output (décisions D1-D9)
├── data-model.md            # Phase 1 output (entités « Lot » et « Résolution d'entrée »)
├── quickstart.md            # Phase 1 output (scénarios de validation)
├── contracts/
│   └── multi-entrees.md     # Phase 1 output (contrat CLI observable ; révise 001/contracts/cli.md)
└── tasks.md                 # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
md_cleaner/
├── cli.py                   # modifié : nargs="+", boucle de lot, refactor en _traiter_document
└── lot.py                   # nouveau : résolution du lot (fonction pure)

tests/
├── unit/
│   └── test_lot.py          # nouveau : résolution du lot
└── integration/
    └── test_lot.py          # nouveau : parité, neutralisation, échecs, codes retour
```

**Structure Decision**: structure single-project existante conservée ; le seul fichier source nouveau est `md_cleaner/lot.py` (fonction pure de résolution, testable isolément), tout le reste est du câblage dans `cli.py` — cohérent avec le principe IV et avec le précédent 006 (transformation pure isolée + câblage minimal).
