# Tasks: Traitement multi-documents en une invocation

**Input**: Design documents from `/specs/007-traitement-multi-documents/`

**Prerequisites**: plan.md, spec.md (US1-US4), research.md (D1-D9), data-model.md, contracts/multi-entrees.md, quickstart.md

**Tests**: inclus — la spec exige des tests de parité (SC-002), de non-silence (SC-004) et de rétrocompatibilité (SC-005) ; la convention du dépôt livre la suite pytest avec chaque feature.

**Organization**: tâches groupées par user story ; chaque story est livrable et testable indépendamment.

## Format: `[ID] [P?] [Story] Description`

- **[P]** : parallélisable (fichiers différents, pas de dépendance)
- **[Story]** : user story de rattachement (US1-US4)
- Chemins exacts dans chaque description

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: point de départ vérifié avant toute modification

- [ ] T001 Exécuter `pytest` à la racine du dépôt et consigner la baseline verte intégrale (fond de régression pour SC-002/SC-005) ; si un test existe déjà en échec, stopper et corriger avant tout changement

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: refactor préservant le comportement, préalable à toutes les stories

- [ ] T002 Refactorer `md_cleaner/cli.py` : extraire le traitement mono-document de `main()` en `_traiter_document(args, fichier) -> int` (D4 de research.md), sans aucun changement de comportement observable — validations globales (`--extrait`, incompatibilité `--dry-run`+`--suggestion`), lecture, segmentation, détection, suggestion par défaut, dossier de run, écritures et messages restent dans la fonction ; `main()` garde l'aiguillage ; suite pytest existante au vert intégral après le refactor

**Checkpoint**: Foundation ready — les user stories peuvent commencer

---

## Phase 3: User Story 1 - Lot de fichiers listés (Priority: P1) — MVP

**Goal**: `md-cleaner doc1.md doc2.md doc3.md` traite chaque document par le chemin existant, un run par document, code 0 ssi tout a réussi

**Independent Test**: lot des 3 exemples de référence → 3 dossiers de run ; parité octet par octet avec les invocations individuelles ; `md-cleaner doc.md` strictement inchangé

### Tests for User Story 1

- [ ] T003 [P] [US1] Écrire les tests d'intégration dans `tests/integration/test_lot.py` (échouant d'abord) : lot des 3 entrées `Examples/*/2.Input/*.md` → 3 dossiers de run consécutifs avec `<stem>-nettoye.md`, code 0 ; parité octet par octet lot vs invocations individuelles aux options par défaut (SC-002) ; ordre de traitement = ordre d'apparition ; doublon (même fichier deux fois) → 2 runs, sortie suffixée `-1`, jamais d'écrasement (FR-010) ; invocation mono-document existante inchangée (SC-005)

### Implementation for User Story 1

- [ ] T004 [US1] Créer `md_cleaner/lot.py` : fonction pure `resoudre_lot(entrees: list[Path]) -> tuple[list[Path], list[str]]` — version fichiers uniquement : chaque entrée fichier est retenue telle quelle à sa position, doublons conservés, chemin inexistant ou non-`.md` listé directement conservé tel quel dans le lot (il échouera au traitement, D2/D3 de research.md)
- [ ] T005 [P] [US1] Écrire les tests unitaires dans `tests/unit/test_lot.py` : fichiers seuls retenus dans l'ordre ; doublons conservés ; chemin inexistant conservé ; liste des avertissements vide dans ce périmètre
- [ ] T006 [US1] Câbler dans `md_cleaner/cli.py` : argument positionnel `nargs="+"` avec `type=Path` (zéro argument reste un usage invalide code 3, D1) ; résolution du lot via `resoudre_lot` ; boucle séquentielle appelant `_traiter_document` pour chaque document ; agrégation du code retour : 0 si et seulement si tous les documents ont réussi, 1 sinon (D7)

**Checkpoint**: US1 fonctionnelle et testable seule — MVP livrable

---

## Phase 4: User Story 2 - Dossier en entrée (Priority: P2)

**Goal**: `md-cleaner dossierA` traite les `.md` de premier niveau triés par nom ; dossier sans `.md` ignoré avec message ; lot vide → erreur 1

**Independent Test**: dossier mixte (`.md` + `.txt`) → seuls les `.md` traités ; `Examples\Exemple_1` (sous-dossiers uniquement) → message + code 1 sans traitement

### Tests for User Story 2

- [ ] T007 [P] [US2] Étendre les tests d'intégration dans `tests/integration/test_lot.py` (échouant d'abord) : dossier contenant `.md` et non-`.md` → seuls les `.md` traités, dans l'ordre alphabétique, non-`.md` ignorés sans message (FR-002) ; mélange fichier + dossier → union dans l'ordre d'apparition ; dossier sans `.md` seul → message explicite + code 1 + aucun traitement (FR-008) ; dossier sans `.md` en lot mixte → message + document valide traité + code 0

### Implementation for User Story 2

- [ ] T008 [P] [US2] Étendre les tests unitaires dans `tests/unit/test_lot.py` : expansion d'un dossier en ses `.md` de premier niveau (`suffix.lower() == ".md"`, `iterdir()` non récursif, tri par `name`, précédent `charger_echantillon` de `md_cleaner/detection.py`) ; filtrage silencieux des non-`.md` ; dossier sans `.md` → message d'entrée ignorée dans la liste des avertissements ; mélange fichier + dossier dans l'ordre d'apparition
- [ ] T009 [US2] Étendre `resoudre_lot` dans `md_cleaner/lot.py` avec le développement des dossiers (règles FR-002/FR-008 ci-dessus) et câbler dans `md_cleaner/cli.py` : lot vide après résolution → message + erreur d'entrée code 1 avant toute boucle de traitement

**Checkpoint**: US1 et US2 fonctionnelles et testables indépendamment

---

## Phase 5: User Story 3 - Options non applicables en lot (Priority: P3)

**Goal**: `--dry-run`/`--suggestion` neutralisées avec avertissement explicite dès que le lot compte plus d'un document ; lot d'un document → comportement inchangé

**Independent Test**: `md-cleaner a.md b.md --dry-run` → avertissement + 2 sorties nettoyées ; `md-cleaner dossierA --dry-run` avec un seul `.md` → dry-run fonctionnel

### Tests for User Story 3

- [ ] T010 [P] [US3] Étendre les tests d'intégration dans `tests/integration/test_lot.py` (échouant d'abord) : `--dry-run` en lot de 2 → avertissement `AVERTISSEMENT : --dry-run ignorée en lot : applicable à un seul document` sur stderr, aucune sortie de dry-run, 2 sorties nettoyées, code 0 (FR-006, SC-004) ; `--suggestion` en lot → avertissement équivalent, suggestion neutralisée ; lot d'exactement un document (fichier listé, ou dossier contenant un seul `.md`) avec `--dry-run` → rapport + suggestion produits, comportement actuel inchangé (FR-005)

### Implementation for User Story 3

- [ ] T011 [US3] Implémenter dans `md_cleaner/cli.py` : neutralisation conditionnelle de `--dry-run` et `--suggestion` quand le lot résolu contient plus d'un document (D5), avertissements sur stderr au format des avertissements existants, un par option, avant la boucle de traitement (D6) ; l'incompatibilité `--dry-run` + `--suggestion` reste une erreur d'usage code 3 avant résolution du lot

**Checkpoint**: les trois stories sont indépendamment fonctionnelles

---

## Phase 6: User Story 4 - Échecs en lot (Priority: P4)

**Goal**: échec documentaire signalé, lot poursuivi, arrêt net au 3e échec consécutif, code 0 ssi tout a réussi

**Independent Test**: `md-cleaner valide.md absent.md valide2.md` → 2 sorties conservées + ERREUR + code 1 ; 3 échecs consécutifs → arrêt avant le document suivant

### Tests for User Story 4

- [ ] T012 [P] [US4] Étendre les tests d'intégration dans `tests/integration/test_lot.py` (échouant d'abord) : échec isolé (chemin inexistant entre deux documents valides) → 2 sorties conservées, message `ERREUR : <chemin> : <raison>` sur stderr, code 1 (FR-007) ; trois échecs consécutifs suivis d'un document valide → arrêt net au troisième, document valide non traité, sorties déjà produites conservées, code 1 ; deux échecs non consécutifs encadrant un succès → lot complet traité, compteur remis à zéro par le succès, code 1

### Implementation for User Story 4

- [ ] T013 [US4] Implémenter dans `md_cleaner/cli.py` : signalisation de chaque échec sur stderr au format `ERREUR : <chemin> : <raison>`, compteur d'échecs consécutifs incrémenté à chaque échec et remis à zéro à chaque succès, arrêt immédiat au troisième consécutif sans traiter les documents suivants (D7), conservation intégrale des sorties déjà produites

**Checkpoint**: les quatre stories sont fonctionnelles — reste la documentation et la validation croisée

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: contrat, documentation et validation transverses

- [ ] T014 [P] Réviser `specs/001-nettoyage-md-repetitif/contracts/cli.md` selon D9 : point d'entrée multi-entrées (révision de « Un run = un fichier d'entrée »), note d'applicabilité de `--dry-run`/`--suggestion` (lot d'un seul document), condition d'émission des codes retour en lot — le détail autoritaire reste dans `specs/007-traitement-multi-documents/contracts/multi-entrees.md`
- [ ] T015 [P] Mettre à jour `README.md` : section « Traiter plusieurs documents » (fichiers listés, dossier, mélange ; avertissement sur les options neutralisées en lot ; ordre et doublons)
- [ ] T016 Exécuter la validation complète : `pytest` (suite entière au vert, sans relâchement), `pre-commit run --all-files`, et les 8 scénarios de `specs/007-traitement-multi-documents/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: aucune dépendance — commencer immédiatement
- **Foundational (Phase 2)**: dépend de Phase 1 — BLOQUE toutes les stories
- **US1 (Phase 3)**: dépend de Phase 2 (le refactor `_traiter_document` et la boucle s'y câblent)
- **US2 (Phase 4)**: dépend de US1 (`resoudre_lot` et la boucle existent)
- **US3 (Phase 5)**: dépend de US1 (la cardinalité du lot est connue après résolution) ; indépendante de US2
- **US4 (Phase 6)**: dépend de US1 (boucle et agrégation des codes) ; indépendante de US2/US3
- **Polish (Phase 7)**: dépend de toutes les stories livrées

### Within Each User Story

- Tests d'abord, en échec avant implémentation
- Module de résolution (`lot.py`) avant câblage (`cli.py`)
- Unitaires avant intégration
- Story complète avant la suivante

### Parallel Opportunities

- T003, T005 (US1) : fichiers de tests différents, parallélisables
- T007, T008 (US2) : fichiers différents, parallélisables
- T010 (US3) et T012 (US4) : même fichier `tests/integration/test_lot.py` ajouté à des phases différentes — séquentiel entre elles, parallélisables avec les tâches d'implémentation de leur propre story seulement après l'écriture des tests
- T014, T015 (Polish) : fichiers différents, parallélisables

---

## Parallel Example: User Story 1

```bash
# Écrire les tests de US1 ensemble (fichiers différents) :
Task: "T003 tests d'intégration tests/integration/test_lot.py"
Task: "T005 tests unitaires tests/unit/test_lot.py"

# Puis l'implémentation (même périmètre fonctionnel, séquentiel) :
Task: "T004 créer md_cleaner/lot.py"
Task: "T006 câbler nargs='+' et la boucle dans md_cleaner/cli.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1 : baseline pytest verte
2. Phase 2 : refactor `_traiter_document` sans changement de comportement
3. Phase 3 : US1 complète (nargs, `resoudre_lot` fichiers, boucle, agrégation des codes)
4. **STOP and VALIDATE** : parité octet par octet + rétrocompat mono-document
5. Déployable en l'état pour un lot de fichiers listés

### Incremental Delivery

1. Setup, puis Foundational → fondation prête
2. Ajouter US1 → MVP (lot de fichiers)
3. Ajouter US2 → dossier accepté en entrée
4. Ajouter US3 → non-silence sur les options neutralisées
5. Ajouter US4 → sémantique d'échec complète
6. Ajouter Polish → contrat 001 révisé, README, validation complète

---

## Notes

- [P] = fichiers différents, pas de dépendance sur une tâche incomplète
- Les tests d'une story doivent échouer avant l'implémentation de la story
- Le mono-document ne doit jamais régresser : la suite existante ne se modifie pas sur les cas mono-document (SC-005)
- Committer après chaque tâche ou groupe logique
- Éviter : tâches vagues, conflits sur un même fichier dans une même vague parallèle
