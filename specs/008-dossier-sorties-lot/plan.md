# Implementation Plan: Un dossier de sorties partagé pour les documents d'un même lot

**Branch**: `015-multi-docs` | **Date**: 2026-10-05 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/008-dossier-sorties-lot/spec.md`, issue du handoff de l'assessment `dossier-sorties-lot` (verdict go, option A « dossier de run par invocation, sorties à plat »), arbitrage `--nom-titre` tranché en spécification le 2026-10-05 : neutralisation avec avertissement en lot de plusieurs.

## Summary

Une invocation produit exactement un dossier de run dans `--sortie`, quel que soit le nombre de documents : le dossier est créé une fois en tête d'invocation (après résolution du lot et neutralisations) pour un lot de plusieurs, tandis que le mono-document conserve strictement son chemin actuel (création interne au traitement, `--nom-titre` fonctionnel). Les N sorties nettoyées vivent à plat dans ce dossier (règle 006 inchangée, suffixe anti-collision existant pour les stems identiques). En lot de plusieurs, les sorties de `--pagine` sont préfixées et rendues uniques par document (`<nom-dérivé>-nettoye-pagine.md`, `<nom-dérivé>-cartographie.json`, suffixe anti-collision de même forme que 006) ; en lot d'un document, les noms courts actuels demeurent. `--nom-titre` est neutralisée avec avertissement en lot de plusieurs. Aucun résumé, aucun marqueur de lot incomplet ; sémantique d'échec 007 inchangée. Trois chantiers : déplacement de la création du dossier (câblage `cli.py`), un résolveur de chemin libre généralisant `resoudre_chemin_nettoye` (`sortie.py`), et la migration bornée des tests et contrats (~9 assertions, contrats 007/001, README).

## Technical Context

**Language/Version**: Python 3.12 (existant — déploiement identique aux features 001-007).

**Primary Dependencies**: aucune en runtime (stdlib) ; dev : pytest, ruff (en place). Surface modifiée : `md_cleaner/cli.py` (création du dossier déplacée en tête d'invocation pour le lot de plusieurs, passage du dossier à `_traiter_document`, préfixage conditionnel des sorties paginées, neutralisation de `--nom-titre`), `md_cleaner/sortie.py` (nouveau résolveur de chemin libre, généralisation du suffixe `-1`, `-2`), `tests/integration/test_lot.py` (migration des ~9 assertions de structure + nouveaux tests US1-US4), `tests/unit/test_sortie.py` (tests du résolveur), révision des contrats (`specs/007-.../contracts/multi-entrees.md` FR-003/FR-011, `specs/001-.../contracts/cli.md` table des artefacts) et du README.

**Storage**: inchangé — fichiers locaux dans `output/<run>/`, un dossier de run par invocation.

**Testing**: `pytest` existant. Unitaires : `tests/unit/test_sortie.py` (résolveur libre : nominal, collision `-1`/`-2`, extensions arbitraires). Intégration : migration de `tests/integration/test_lot.py` (structure attendue : 1 dossier pour un lot, préfixage des secondaires, `--nom-titre` neutralisée, lot entièrement en échec → dossier vide, mono-document inchangé) + nouveaux tests US1-US4 ; la suite existante hors lot doit passer sans relâchement (SC-003).

**Target Platform**: CLI locale multi-OS, hors-ligne (inchangé).

**Project Type**: cli (modification d'un outil existant).

**Performance Goals**: inchangé ; aucune boucle nouvelle de complexité supérieure.

**Constraints**: rétrocompatibilité mono-document stricte — structure, noms de tous les artefacts, numérotation (FR-004, SC-003) ; jamais d'écrasement, unicité garantie par le suffixe anti-collision (FR-002, SC-002) ; sémantique 007 inchangée (résolution du lot, neutralisations, échecs, codes retour — FR-009) ; aucune nouvelle option CLI.

**Scale/Scope**: corpus de taille modeste (hérité de 007) ; corpus de validation = les 3 exemples de référence (dont deux `consolidated.md` de stems identiques, cas de collision nominal) et documents construits en test.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe / exigence | Statut | Justification |
| ------------------- | ------ | ------------- |
| I. Isolation des secrets (NON NÉGOCIABLE) | PASS | Aucun secret manipulé ; inchangé. |
| II. Local-first & confidentialité (NON NÉGOCIABLE) | PASS | Aucun appel réseau ; écritures locales uniquement, dans `--sortie` comme aujourd'hui. |
| III. Open-source & sans trackers | PASS | Aucune nouvelle dépendance ; stdlib uniquement. |
| IV. Simplicité (YAGNI) | PASS | Un déplacement de création de dossier, une généralisation du résolveur existant, un préfixage conditionnel ; aucune nouvelle option, aucun résumé, aucun marqueur — le changement simplifie même le contrat (« un run = une invocation »). |
| Config Validation | PASS | Échec rapide conservé ; le dossier n'est créé qu'après résolution du lot (lot vide → code 1, aucun dossier). |
| Path Isolation | PASS | Aucun chemin codé en dur ; racine `--sortie` inchangée. |
| No Cloud / No Trackers / Network Surface | PASS | Aucun trafic. |
| Data Retention | PASS | Sorties uniquement dans `output/` (supprimables) ; aucune copie cachée. |
| Compliance CI (Ruff, markdownlint, secrets) | PASS | Code sous `md_cleaner/` et `tests/` linté ; artefacts de spec sous `specs/` (config en place). |

**Re-check post-Phase 1** : aucun changement — les décisions D1-D7 de [research.md](./research.md) n'introduisent ni dépendance, ni réseau, ni secret ; le contrat observable ([contracts/dossier-de-lot.md](./contracts/dossier-de-lot.md)) révisant 007/001 reste borné à la structure de sortie, aux noms d'artefacts et à la neutralisation de `--nom-titre`.

## Project Structure

### Documentation (this feature)

```text
specs/008-dossier-sorties-lot/
├── plan.md                  # This file (/speckit-plan command output)
├── research.md              # Phase 0 output (décisions D1-D7)
├── data-model.md            # Phase 1 output (entités « Dossier de run d'invocation », « Base de nom dérivée »)
├── quickstart.md            # Phase 1 output (scénarios de validation)
├── contracts/
│   └── dossier-de-lot.md    # Phase 1 output (contrat observable ; révise 007/multi-entrees et 001/cli.md)
└── tasks.md                 # Phase 2 output (/speckit-tasks command - NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
md_cleaner/
├── cli.py                   # modifié : création du dossier en tête d'invocation (lot de plusieurs),
│                            #   dossier passé à _traiter_document, préfixage des secondaires,
│                            #   neutralisation de --nom-titre en lot
└── sortie.py                # modifié : resoudre_chemin_libre (généralisation du suffixe anti-collision)

tests/
├── unit/
│   └── test_sortie.py       # étendu : tests du résolveur libre
└── integration/
    └── test_lot.py          # migré (~9 assertions) + nouveaux tests US1-US4
```

**Structure Decision**: structure single-project existante conservée ; aucun fichier source nouveau — le seul ajout de code est `resoudre_chemin_libre` dans `sortie.py` (généralisation du mécanisme 006 déjà éprouvé), tout le reste est du câblage dans `cli.py` — cohérent avec le principe IV et avec les précédents 006/007 (transformation pure isolée + câblage minimal).
