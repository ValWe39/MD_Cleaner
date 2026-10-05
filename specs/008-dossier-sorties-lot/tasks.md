# Tasks: Un dossier de sorties partagé pour les documents d'un même lot

**Input**: Design documents from `/specs/008-dossier-sorties-lot/`

**Prerequisites**: plan.md, spec.md (US1-US4), research.md (D1-D7), data-model.md, contracts/dossier-de-lot.md, quickstart.md

**Tests**: inclus — la spec exige des tests de structure (SC-001, SC-005), d'unicité sans écrasement (SC-002) et de rétrocompatibilité mono-document (SC-003) ; la convention du dépôt livre la suite pytest avec chaque feature.

**Organization**: tâches groupées par user story ; chaque story est livrable et testable indépendamment.

## Format: `[ID] [P?] [Story] Description`

- **[P]** : parallélisable (fichiers différents, pas de dépendance)
- **[Story]** : user story de rattachement (US1-US4)
- Chemins exacts dans chaque description

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: point de départ vérifié avant toute modification

- [x] T001 Exécuter `pytest` à la racine du dépôt et consigner la baseline verte intégrale (165 tests attendus) ; si un test existe déjà en échec, stopper et corriger avant tout changement

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: mécanisme anti-collision généralisé, préalable à US1 et US2

- [x] T002 Implémenter `resoudre_chemin_libre(dossier, base, extension)` dans `md_cleaner/sortie.py` (D4) : premier chemin libre pour `<base><suffixe><extension>` avec suffixe `-1`, `-2`, ... inséré avant l'extension, jamais d'écrasement ; refactorer `resoudre_chemin_nettoye` en appel mince à cette fonction (comportement inchangé, tests 006 à l'appui)
- [x] T003 [P] Écrire les tests unitaires dans `tests/unit/test_sortie.py` (échouant d'abord pour la nouvelle fonction) : nominal libre, collision `-1`/`-2`, extension `.json`, jamais d'écrasement d'un fichier existant, et non-régression de `resoudre_chemin_nettoye`

**Checkpoint**: Foundation ready — les user stories peuvent commencer

---

## Phase 3: User Story 1 - Un seul dossier de run par invocation (Priority: P1) — MVP

**Goal**: `md-cleaner doc1.md doc2.md` produit exactement un dossier `00X` contenant les sorties des deux documents ; numérotation par invocation

**Independent Test**: lot des 3 exemples de référence → 1 dossier avec 3 sorties (dont `consolidated-nettoye.md` et `consolidated-nettoye-1.md`) ; invocation suivante → `002`

### Tests for User Story 1

- [x] T004 [P] [US1] Migrer et étendre les tests d'intégration dans `tests/integration/test_lot.py` (échouant d'abord) : lot de 3 documents → exactement 1 dossier de run contenant `consolidated-nettoye.md`, `consolidated-nettoye-1.md`, `retry-failed-records-nettoye.md` (SC-001, SC-002) ; deux invocations successives → `001` puis `002` (SC-005) ; mono-document strictement inchangé (SC-003) ; remplacer les ~9 assertions existantes qui codent un dossier par document

### Implementation for User Story 1

- [x] T005 [US1] Câbler dans `md_cleaner/cli.py` (D1, D2) : créer le dossier de run **une fois** dans `main()` après résolution du lot, neutralisations et validation de l'échantillon, uniquement si le lot compte plusieurs documents (`creer_dossier_run(args.sortie, "", None)`) ; passer le dossier à `_traiter_document` via un paramètre `dossier: Path | None` (`None` → création interne inchangée pour le lot d'un document)

**Checkpoint**: US1 fonctionnelle et testable seule — MVP livrable

---

## Phase 4: User Story 2 - Sorties secondaires attribuables (Priority: P2)

**Goal**: en lot de plusieurs avec `--pagine`, chaque document produit sa paire préfixée unique ; noms courts inchangés en lot d'un

**Independent Test**: lot de 2 documents avec `--pagine` → 4 artefacts secondaires distincts et attribuables ; mono-document → `nettoye-pagine.md` / `cartographie.json`

### Tests for User Story 2

- [x] T006 [P] [US2] Étendre les tests d'intégration dans `tests/integration/test_lot.py` (échouant d'abord) : lot de 2 avec `--pagine` → `<stem1>-nettoye-pagine.md`, `<stem1>-cartographie.json`, `<stem2>-nettoye-pagine.md`, `<stem2>-cartographie.json` (FR-003, SC-004) ; deux stems identiques → paires suffixées alignées (`consolidated-nettoye-1.md`, `consolidated-nettoye-pagine-1.md`, `consolidated-cartographie-1.json`) ; lot d'un document (fichier ou dossier à 1 `.md`) → noms courts actuels

### Implementation for User Story 2

- [x] T007 [US2] Implémenter le préfixage conditionnel dans `md_cleaner/cli.py` (D3) : en lot de plusieurs, chemins paginés et cartographie résolus via `resoudre_chemin_libre` avec les bases `<nom-dérivé>-nettoye-pagine` (extension `.md`) et `<nom-dérivé>-cartographie` (extension `.json`) ; en lot d'un document, chemins fixes actuels (`nettoye-pagine.md`, `cartographie.json`) inchangés

**Checkpoint**: US1 et US2 fonctionnelles et testables indépendamment

---

## Phase 5: User Story 3 - Comportements bornés du dossier de lot (Priority: P3)

**Goal**: lot incomplet → sorties des documents réussis conservées, sans marqueur ; lot entièrement en échec → dossier vide en place ; lot vide → aucun dossier

**Independent Test**: lot [valide, absent, valide] → 1 dossier avec 2 sorties, code 1 ; lot de 3 absents → dossier vide, code 1

### Tests for User Story 3

- [x] T008 [P] [US3] Étendre les tests d'intégration dans `tests/integration/test_lot.py` (échouant d'abord) : échec isolé → sorties valides dans l'unique dossier, `ERREUR : ...` signalée, code 1, aucun marqueur (FR-006) ; lot entièrement en échec (2 absents) → dossier de run numéroté **vide** en place, code 1 (FR-007) ; lot vide (dossier sans `.md` seul) → aucun dossier créé, code 1 (FR-008) ; lot interrompu par fail-fast → sorties déjà produites conservées dans l'unique dossier
- [x] T009 [US3] Vérifier et ajuster l'ordre de création dans `md_cleaner/cli.py` si besoin (D1) : le dossier est créé après la résolution du lot et les neutralisations (jamais pour un lot vide) et avant la boucle de traitement (présent dès un échec total) — l'essentiel découle de T005, ce borne le contrat

**Checkpoint**: US1, US2 et US3 fonctionnelles indépendamment

---

## Phase 6: User Story 4 - `--nom-titre` en lot (Priority: P4)

**Goal**: `--nom-titre` neutralisée avec avertissement en lot de plusieurs ; pleinement fonctionnelle en mono-document

**Independent Test**: lot de 2 avec `--nom-titre 30` → avertissement + dossier numéroté ; mono → slug du titre

### Tests for User Story 4

- [x] T010 [P] [US4] Étendre les tests d'intégration dans `tests/integration/test_lot.py` (échouant d'abord) : lot de 2 avec `--nom-titre 30` → avertissement `AVERTISSEMENT : --nom-titre ignorée en lot : applicable à un seul document` sur stderr, dossier numéroté, code 0 (FR-005) ; mono-document avec `--nom-titre 30` → dossier nommé d'après le titre, sans avertissement (rétrocompatibilité)
- [x] T011 [US4] Implémenter la neutralisation dans `md_cleaner/cli.py` (D5) : dans le bloc de neutralisation de `main()`, à côté de `--dry-run`/`--suggestion`, avertissement sur stderr puis `args.nom_titre = None` si le lot compte plusieurs documents

**Checkpoint**: les quatre stories sont fonctionnelles — reste la documentation et la validation croisée

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: contrats, documentation et validation transverses

- [x] T012 [P] Réviser `specs/007-traitement-multi-documents/contracts/multi-entrees.md` selon D7 : FR-003 et FR-011 passent de « un dossier de run par document » à « un dossier de run par invocation », avec renvoi vers `specs/008-dossier-sorties-lot/contracts/dossier-de-lot.md` pour la règle complète
- [x] T013 [P] Réviser `specs/001-nettoyage-md-repetitif/contracts/cli.md` (table des fichiers produits par mode, exemples) et la section « Traiter plusieurs documents » du `README.md` (dossier unique, secondaires préfixées, `--nom-titre` neutralisée)
- [x] T014 Exécuter la validation complète : `pytest` (suite entière au vert, sans relâchement), `pre-commit run --all-files`, et les 8 scénarios de `specs/008-dossier-sorties-lot/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: aucune dépendance — commencer immédiatement
- **Foundational (Phase 2)**: dépend de Phase 1 — BLOQUE US1 (tests de structure) et US2 (préfixage)
- **US1 (Phase 3)**: dépend de Phase 2 — le dossier partagé est la base de tout
- **US2 (Phase 4)**: dépend de US1 (le préfixage vit dans le dossier partagé)
- **US3 (Phase 5)**: dépend de US1 (les cas bornés testent le dossier créé en tête d'invocation) ; indépendante de US2
- **US4 (Phase 6)**: dépend de US1 (la neutralisation s'applique au lot de plusieurs) ; indépendante de US2/US3
- **Polish (Phase 7)**: dépend de toutes les stories livrées

### Within Each User Story

- Tests d'abord, en échec avant implémentation
- Résolveur (Phase 2) avant préfixage (US2)
- Câblage `cli.py` après les tests de la story
- Story complète avant la suivante

### Parallel Opportunities

- T002 et T003 (Phase 2) : fichiers différents, parallélisables
- T004, T006, T008, T010 : tous dans `tests/integration/test_lot.py` — séquentiels entre eux, chacun parallélisable avec les tâches d'implémentation de sa story
- T012 et T013 (Polish) : fichiers différents, parallélisables

---

## Parallel Example: User Story 1

```bash
# Écrire les tests de US1 (après la Phase 2) :
Task: "T004 migrer et étendre tests/integration/test_lot.py"

# Puis l'implémentation (même périmètre fonctionnel, séquentiel) :
Task: "T005 câbler la création unique du dossier dans md_cleaner/cli.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1 : baseline pytest verte
2. Phase 2 : `resoudre_chemin_libre` + tests
3. Phase 3 : US1 complète (dossier unique, numérotation par invocation)
4. **STOP and VALIDATE** : lot des 3 exemples → 1 dossier ; mono-document inchangé
5. Déployable en l'état : la demande de l'utilisateur (« un seul 00X avec mes deux outputs ») est satisfaite

### Incremental Delivery

1. Setup + Foundational → fondation prête
2. Ajouter US1 → MVP (dossier partagé)
3. Ajouter US2 → secondaires attribuables
4. Ajouter US3 → cas bornés (échec partiel/total, lot vide)
5. Ajouter US4 → `--nom-titre` bornée
6. Ajouter Polish → contrats 007/001, README, validation complète

---

## Notes

- [P] = fichiers différents, pas de dépendance sur une tâche incomplète
- Les tests d'une story doivent échouer avant l'implémentation de la story
- Le mono-document ne doit jamais régresser : ses tests ne se modifient pas (SC-003)
- Les ~9 assertions existantes de `tests/integration/test_lot.py` sont migrées dans T004, pas supprimées silencieusement
- Committer après chaque tâche ou groupe logique
- Éviter : tâches vagues, conflits sur un même fichier dans une même vague parallèle
