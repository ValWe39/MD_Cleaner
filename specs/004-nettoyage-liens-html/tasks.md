---
description: "Task list for feature implementation"
---

# Tasks: Nettoyage des destinations de liens résiduelles à l'écriture de la sortie

**Input**: Design documents from `/specs/004-nettoyage-liens-html/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/nettoyage-liens.md, quickstart.md

**Tests**: inclus — SC-005 exige la suite au vert sans relâchement et le quickstart exige `pytest` (Scénario 5).

**Organization**: tâches groupées par user story (US1-US3) ; la feature modifie un outil existant, aucun setup de projet n'est requis — la Phase 1 est le socle de tests écrits d'abord (TDD).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: exécutable en parallèle (fichiers différents, pas de dépendance envers une tâche incomplète)
- **[Story]**: user story de rattachement (US1, US2, US3) — uniquement pour les phases de stories
- Chemins exacts dans chaque description

## Path Conventions

Projet existant : paquet `md_cleaner/` et `tests/` à la racine (plan.md de la feature 004, section Source Code). `detection.py`, `suggestion.py` et `cartographie.py` ne sont pas modifiés (D2 : la passe vit dans `nettoyage.py`, en aval de la détection).

---

## Phase 1: Foundational (Blocking Prerequisites)

**Purpose**: Tests écrits d'abord (TDD) — ils DOIVENT échouer avant implémentation.

- [x] T001 [P] [US1] Créer `tests/unit/test_nettoyage_liens.py` : tests de la fonction pure — un lien `[libellé](</chemin>)` devient `[libellé]` (FR-001) ; plusieurs liens sur une même ligne tous retirés (US1, scénario 3) ; libellé vide `[](</chemin>)` → destination retirée, crochets vides conservés ; caractères encodés `%5B`/`%3A` retirés tels quels sans décodage (FR-006) ; `](https://...)` et `](chemin)` inchangés (hors périmètre) ; `<!-- page: 3 -->` inchangé (D5) ; ligne sans `](</...>)` inchangée octet par octet ; idempotence (2e passe = no-op)
- [x] T002 [US1] Créer `tests/integration/test_nettoyage_liens.py` : run CLI sur `Examples/Exemple_2/2.Input/consolidated.md` → aucune ligne de `nettoye.md` ne contient `](</` (SC-001), libellés `[texte]` présents, nombre et ordre des lignes inchangés par rapport à un run `--conserver-liens` (SC-002)
- [x] T003 [P] [US2] Étendre `tests/integration/test_nettoyage_liens.py` : run avec `--conserver-liens` → destinations intactes ; diff des deux runs limité aux seules sous-chaînes `](</...>)` retirées, reste identique octet par octet (SC-004) ; sur un corpus sans liens, sorties des deux modes identiques octet par octet (SC-003)
- [x] T004 [P] [US3] Étendre `tests/integration/test_nettoyage_liens.py` : run `--pagine` → contenu des pages de `nettoye-pagine.md` sans destination, chaque marqueur `<!-- page: N -->` présent et identique, `cartographie.json` identique entre les deux modes (FR-004, FR-005, SC-004)

**Checkpoint**: les nouveaux tests échouent pour la bonne raison (aucune fonction de retrait n'existe, pas d'option `--conserver-liens`).

---

## Phase 2: User Story 1 - Sortie finale sans destinations résiduelles (Priority: P1) — MVP

**Goal**: le `nettoye.md` produit par un run standard ne contient plus aucune destination `](</...>)`, libellés et reste du texte inchangés.

**Independent Test**: `pytest tests/unit/test_nettoyage_liens.py` puis run sur Exemple_2 : 0 destination dans `nettoye.md` (SC-001), libellés en place.

### Implementation for User Story 1

- [x] T005 [US1] Implémenter la fonction pure dans `md_cleaner/nettoyage.py` : `nettoyer_destinations(lignes)` retire les sous-chaînes `](</...>)` — `](<` + destination sans `>` (le premier `>` referme, aucun chevron imbriqué) + `>)` — sans décoder les caractères encodés, occurrences multiples par ligne, liste de lignes → liste de lignes (D1, D3, FR-001, FR-006)
- [x] T006 [US1] Appliquer la passe dans `ecrire_nettoye` de `md_cleaner/nettoyage.py` : sur le texte des blocs avant écriture de `nettoye.md`, active par défaut à chaque run de nettoyage, sans muter les `Bloc` renvoyés par `nettoyer()` ni toucher `cartographie.json` (D2, FR-002, FR-005)
- [x] T007 [US1] Migrer `tests/integration/test_nettoyage_simple.py` : mettre à jour les contenus attendus — destinations retirées, libellés conservés (SC-005, migration bornée du plan)
- [x] T008 [US1] Vérifier que T001/T002 passent et que la suite complète reste au vert sans relâchement des seuils : `pytest` (SC-005)

**Checkpoint**: un run standard produit un `nettoye.md` sans destination ; la suite est au vert.

---

## Phase 3: User Story 2 - Désactivation par `--conserver-liens` (Priority: P2)

**Goal**: l'utilisateur retrouve des liens cliquables via un drapeau unique ; sans lui, nettoyage actif.

**Independent Test**: run avec `--conserver-liens` → destinations intactes ; diff des deux runs = uniquement les destinations retirées (SC-004).

### Implementation for User Story 2

- [x] T009 [US2] Ajouter l'option dans `construire_analyseur` de `md_cleaner/cli.py` : `--conserver-liens`, booléenne sans argument (`store_true`), défaut absent = nettoyage actif, aide en français, codes retour 0-3 inchangés, compatible avec toutes les options existantes (D4, FR-002, FR-003)
- [x] T010 [US2] Propager le paramètre dans `md_cleaner/cli.py` et `md_cleaner/nettoyage.py` : argument explicite jusqu'aux writers (pas d'état global) ; avec le drapeau, aucune transformation — sorties identiques octet par octet à avant la feature (D3, D4, FR-003)
- [x] T011 [US2] Vérifier que T003 passe et que la suite complète reste au vert : `pytest`

**Checkpoint**: `--conserver-liens` rétablit le comportement antérieur ; US1 reste fonctionnel sans le drapeau.

---

## Phase 4: User Story 3 - Sortie paginée nettoyée, marqueurs préservés (Priority: P3)

**Goal**: `nettoye-pagine.md` bénéficie du même nettoyage ; les marqueurs de page restent intacts ; la cartographie reste cohérente.

**Independent Test**: run `--pagine` → contenu des pages sans destination, chaque marqueur `<!-- page: N -->` présent à l'identique, `cartographie.json` identique aux deux modes (SC-004).

### Implementation for User Story 3

- [x] T012 [US3] Appliquer la passe dans `ecrire_nettoye_pagine` de `md_cleaner/nettoyage.py` : sur le contenu des pages, les marqueurs `---\n\n<!-- page: N -->\n\n` étant générés après la passe par construction (D5, FR-004)
- [x] T013 [US3] Vérifier que T004 passe et que la suite complète reste au vert : `pytest`

**Checkpoint**: les trois stories sont indépendamment fonctionnelles ; la sortie paginée est cohérente avec sa cartographie.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: documentation, contrat et validation de bout en bout.

- [x] T014 [P] Mettre à jour la table des options dans `specs/001-nettoyage-md-repetitif/contracts/cli.md` : ajouter `--conserver-liens` (révision du contrat par `specs/004-nettoyage-liens-html/contracts/nettoyage-liens.md`)
- [x] T015 [P] Documenter l'option dans `README.md` : liste des paramètres et bloc d'exemples (`md-cleaner $fichier --conserver-liens`)
- [x] T016 Exécuter les scénarios 1 à 5 de `specs/004-nettoyage-liens-html/quickstart.md` sur `Examples/Exemple_1` et `Examples/Exemple_2` et constater les attendus
- [x] T017 Vérification finale : `pytest` au vert et `pre-commit run --all-files` sans échec (SC-005)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 1)**: à faire d'abord — les tests DOIVENT échouer avant implémentation (TDD)
- **US1 (Phase 2)**: dépend de la Phase 1 — MVP
- **US2 (Phase 3)**: dépend de T005-T006 (la règle existe) ; le drapeau ne fait rien sans elle
- **US3 (Phase 4)**: dépend de T005-T006 ; indépendante de US2
- **Polish (Phase 5)**: dépend de toutes les stories retenues

### User Story Dependencies

- **US1 (P1)**: aucune dépendance vers une autre story — MVP autonome
- **US2 (P2)**: réutilise la règle de US1, n'ajoute que l'option et la propagation
- **US3 (P3)**: réutilise la règle de US1, n'ajoute que l'application au writer paginé

### Parallel Opportunities

- T001, T003, T004 sont indépendantes (mêmes fichiers de test créés/étendus séparément ou mêmes fichiers mais tâches séquentielles acceptables) — T002 dépend du contenu de T001/T003/T004 dans le même fichier : écrire les tests dans l'ordre T001 → T002 → T003 → T004 ou en parallèle puis consolidation
- T009 et T012 touchent des fichiers différents (`cli.py` vs `nettoyage.py`) mais dépendent tous deux de la Phase 2

---

## Parallel Example: User Story 1

```bash
# Écriture des tests en parallèle (Phase 1) :
Task: "T001 Créer tests/unit/test_nettoyage_liens.py (cas unitaires de la règle)"
Task: "T004 Étendre tests/integration/test_nettoyage_liens.py (run --pagine)"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1 : tests écrits, échec constaté pour la bonne raison
2. Phase 2 : règle + application à `nettoye.md` + migration des contenus attendus
3. **STOP et VALIDER** : run sur Exemple_2 → 0 destination, suite au vert

### Incremental Delivery

1. US1 → sortie standard nettoyée (MVP)
2. US2 → réversibilité par `--conserver-liens`
3. US3 → sortie paginée couverte
4. Polish → contrat CLI, README, quickstart, vérification finale

---

## Notes

- [P] = fichiers différents, pas de dépendance envers une tâche incomplète
- Le [Story] rattache chaque tâche à sa story pour la traçabilité
- Les contraintes de la spec sont citées verbatim dans les descriptions (FR-001 à FR-007, SC-001 à SC-005, D1-D6)
- Committer après chaque tâche ou groupe logique
- Ne jamais relâcher un seuil de test existant (SC-005)
