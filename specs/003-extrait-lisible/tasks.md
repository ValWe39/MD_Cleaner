---
description: "Task list for feature implementation"
---

# Tasks: Extraits lisibles et localisables dans la suggestion

**Input**: Design documents from `/specs/003-extrait-lisible/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/suggestion-extrait.md, quickstart.md

**Tests**: inclus — chaque SC de la spec est mécaniquement vérifiable et le quickstart exige `pytest` (Scénario 0).

**Organization**: tâches groupées par user story (US1-US3) ; la feature enrichit un outil existant, aucun setup de projet n'est requis — la Phase 1 est le socle de tests.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: exécutable en parallèle (fichiers différents, pas de dépendance envers une tâche incomplète)
- **[Story]**: user story de rattachement (US1, US2, US3) — uniquement pour les phases de stories
- Chemins exacts dans chaque description

## Path Conventions

Projet existant : paquet `md_cleaner/` et `tests/` à la racine (plan.md de la feature 003, section Source Code). `detection.py` n'est pas modifié (D1 : enrichissement post-détection dans `suggestion.py`).

---

## Phase 1: Foundational (Blocking Prerequisites)

**Purpose**: Tests écrits d'abord (TDD) — ils DOIVENT échouer avant implémentation.

- [x] T001 [P] [US1] Étendre `tests/unit/test_suggestion.py` : enrichissement des motifs — extrait de N lignes exactes quand l'intervalle le permet (FR-001), intervalle plus court rendu tel quel sans complément (cas limite de la spec), vrais sauts de ligne, position `{"page": entier >= 1, "debut": entier >= 0, "fin": entier > debut, inclue}` ancrée sur la première occurrence (FR-002), extrait et position désignant le même endroit (D1, D3)
- [x] T002 [US1] Étendre `tests/unit/test_suggestion.py` : validation à la relecture — position absente acceptée (suggestion d'avant-feature, FR-005), position mal formée (types, bornes, clés manquantes) → `ErreurSuggestion`, code retour 2, message clair (D4)
- [x] T003 [P] [US2] Créer `tests/integration/test_extrait.py` : CLI — `--extrait 12` puis `--extrait 2` donnent des extraits d'exactement 12 et 2 lignes sur les motifs à intervalle suffisant (SC-002) ; `--extrait 1` et `--extrait 40` → code retour 3 avec message des bornes (FR-003) ; `--extrait 12` sans `--dry-run` → code retour 0, aucune suggestion générée (clarification du 2026-09-29, Option A)

**Checkpoint**: les nouveaux tests échouent pour la bonne raison (extrait actuel : 3 lignes jointes par « ` / ` », pas de champ position, pas d'option)

---

## Phase 2: User Story 1 - Juger un motif depuis le seul suggestion.json (Priority: P1) — MVP

**Goal**: chaque motif porte un extrait multi-lignes distinguable et une position exacte ; le jugement se fait sans ouvrir le document source.

**Independent Test**: `pytest tests/unit/test_suggestion.py` — enrichissement et validation ; puis dry-run sur Exemple_2 : au plus 2 extraits en doublon (SC-001) et positions vérifiables (SC-003).

### Implementation for User Story 1

- [x] T004 [US1] Étendre `construire_suggestion` dans `md_cleaner/suggestion.py` : nouveaux paramètres `pages` et `extrait_n` (défaut 5) — pour chaque motif, recalculer l'extrait depuis les `emplacements` (N premières lignes du premier intervalle de la page de première occurrence, jointes par vrais sauts de ligne, jamais de complément) et ajouter le champ `position` `{"page": P, "debut": D, "fin": F}` avec `F` inclue (conversion depuis l'intervalle interne demi-ouvert : `F = fin_interne - 1`) ; ancrage identique pour l'extrait et la position (D1, D3) ; ne pas modifier `md_cleaner/detection.py`
- [x] T005 [US1] Câbler l'enrichissement dans `md_cleaner/cli.py` : passer `pages` et la valeur d'extrait à `construire_suggestion` dans tous les modes (l'effet n'est visible qu'en dry-run, seul mode écrivant la suggestion) (D2)
- [x] T006 [US1] Vérifier que T001/T002 passent et que la suite complète reste au vert sans relâchement (SC-006) : `pytest`

**Checkpoint**: User Story 1 fonctionnelle — extrait multi-lignes et position dans le JSON

---

## Phase 3: User Story 2 - Régler le nombre de lignes (Priority: P2)

**Goal**: l'option `--extrait N` règle la dose, bornes 2-25, défaut 5, sans effet observable hors dry-run.

**Independent Test**: `pytest tests/integration/test_extrait.py` — N exact, bornes code 3, no-op hors dry-run code 0.

### Implementation for User Story 2

- [x] T007 [US2] Ajouter l'option `--extrait N` à `construire_analyseur()` dans `md_cleaner/cli.py` : validateur `_entier_bornes` existant, bornes 2 à 25, défaut 5 ; l'aide documente que l'effet est limité à la génération de `suggestion.json` et qu'il est sans effet observable hors `--dry-run` (FR-003, clarification du 2026-09-29, D2)
- [x] T008 [US2] Vérifier que T003 passe et que la suite complète reste au vert : `pytest`

**Checkpoint**: User Stories 1 et 2 fonctionnelles indépendamment

---

## Phase 4: User Story 3 - Continuité : rapport intact et suggestions consommables (Priority: P3)

**Goal**: les `\n` des extraits ne cassent pas le rapport ; les suggestions anciennes restent consommables.

**Independent Test**: rapport d'un dry-run sans saut de ligne dans les cellules ; suggestion sans champ position consommée avec code 0.

### Implementation for User Story 3

- [x] T009 [US3] Neutraliser les sauts de ligne dans `generer_rapport()` (`md_cleaner/suggestion.py`) : remplacer `\n` par le séparateur historique « ` / ` » dans les cellules du tableau, après l'échappement des pipes et avant la troncature à 120 caractères ; structure en deux sections (feature 002) et troncature inchangées (FR-004, D5)
- [x] T010 [US3] Étendre `tests/unit/test_suggestion.py` (ou `tests/integration/test_extrait.py`) : le rapport d'un dry-run ne contient aucun saut de ligne dans ses cellules de tableau (SC-006) ; exécuter le Scénario 5 du quickstart — une suggestion sans champ position se consomme avec code 0 (FR-005)

**Checkpoint**: les trois user stories sont fonctionnelles indépendamment

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: contrat, validation complète, conformité

- [x] T011 [P] Réviser `specs/001-nettoyage-md-repetitif/contracts/formats.md` : clause `motifs[].extrait` (« ≤ 3 lignes jointes par " / " ») remplacée par la définition de `specs/003-extrait-lisible/contracts/suggestion-extrait.md`, champ `position` ajouté au schéma (FR-007, D7)
- [x] T012 [P] Exécuter la validation complète de `specs/003-extrait-lisible/quickstart.md` (Scénarios 0 à 7) et consigner tout écart — en particulier le Scénario 6 (déterminisme et garde < 1 Mo à N = 25) et le Scénario 7 (invariance du nettoyage, FR-009)
- [x] T013 Revue de conformité : `ruff check` et `ruff format` sur les fichiers modifiés, `pre-commit run --all-files` complet — zéro modification de `detection.py` (D1), zéro nouvelle dépendance, garde < 1 Mo vérifiée sur le corpus

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (tests d'abord)**: démarrage immédiat — échec attendu avant les phases suivantes
- **Phase 2 (US1)**: dépend de la Phase 1 — cœur de la feature, MVP
- **Phase 3 (US2)**: dépend de T004 (l'option n'a d'effet qu'à travers l'enrichissement) mais ses tests (T003) peuvent s'écrire dès la Phase 1
- **Phase 4 (US3)**: indépendante de US2 ; dépend de T004 (les `\n` n'existent qu'après l'enrichissement)
- **Phase 5 (Polish)**: dépend de toutes les stories ; T011 peut démarrer dès la Phase 1 (contrat indépendant du code)

### User Story Dependencies

- **US1 (P1)**: la base — enrichissement et validation
- **US2 (P2)**: s'appuie sur l'enrichissement (T004) mais se teste indépendamment (bornes CLI)
- **US3 (P3)**: garde-fou du rapport (T009) et continuité (T010) — dépend de l'existence des `\n` (T004)

### Within Each User Story

- Tests écrits d'abord et ÉCHOUANT avant implémentation
- Un seul fichier de production par story (`suggestion.py` pour US1 et US3, `cli.py` pour US2)

### Parallel Opportunities

- T001/T003 en parallèle (fichiers de test différents)
- T009 (US3, `suggestion.py`) et T007 (US2, `cli.py`) en parallèle — fichiers différents
- T011 (contrat, aucune dépendance au code) parallélisable dès la Phase 1

---

## Parallel Example: User Story 1

```bash
# Lancer les tests de US1 et US2 ensemble (échec attendu) :
Task: "Enrichissement et validation dans tests/unit/test_suggestion.py"  # T001, T002
Task: "CLI --extrait dans tests/integration/test_extrait.py"            # T003

# Puis l'implémentation (séquentielle, un seul fichier) :
Task: "construire_suggestion enrichi dans md_cleaner/suggestion.py"     # T004
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1: tests en échec
2. Phase 2: US1 (enrichissement + position)
3. **STOP et VALIDER**: `pytest` + dry-run manuel sur Exemple_2 — SC-001 (≤ 2 doublons) et SC-003 (positions réelles) sont les critères go/no-go
4. Le MVP rend déjà le jugement possible depuis le JSON à la valeur par défaut

### Incremental Delivery

1. Tests en échec → socle
2. US1 → MVP (juger sans la source)
3. US2 → dose réglable
4. US3 → continuité garantie (rapport, suggestions anciennes)
5. Polish → contrat révisé, quickstart complet, conformité

### Parallel Team Strategy

Avec plusieurs développeurs :

1. Tous sur la Phase 1 ensemble (tests)
2. Développeur A: US1 (`suggestion.py`) ; Développeur B: US2 (`cli.py`) ; Développeur C: T011 (contrat)
3. US3 (T009) après T004, en parallèle de US2
4. Polish ensemble

---

## Notes

- [P] = fichiers différents, pas de dépendances
- La feature ne modifie ni `detection.py` (D1 : enrichissement post-détection), ni `nettoyage.py`, ni `cartographie.py` (FR-009 : la longueur d'extrait n'a aucune incidence sur le nettoyage) — si une tâche y semble nécessaire, c'est une alerte de dérive de périmètre
- Vérifier que les tests échouent avant d'implémenter
- Committer après chaque tâche ou groupe logique (workflow pre-commit du dépôt)
- S'arrêter à tout checkpoint pour valider une story indépendamment
