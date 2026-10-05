---
description: "Task list for feature implementation"
---

# Tasks: nom de sortie dérivé du document source

**Input**: Design documents from `/specs/006-nom-sortie-source/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/nommage-sortie.md, quickstart.md

**Tests**: inclus — la spec exige des critères vérifiables (SC-001 à SC-003), la mise à jour des tests existants fait partie du périmètre (D6, handoff du decide), et le quickstart exige `pytest` (Scénario 5).

**Organization**: tâches groupées par user story (US1-US3) ; la feature modifie un outil existant, aucun setup de projet n'est requis — la Phase 1 est le socle de tests écrits d'abord (TDD), par référence au cycle validé en 004 et 005.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: exécutable en parallèle (fichiers différents, pas de dépendance envers une tâche incomplète)
- **[Story]**: user story de rattachement (US1, US2, US3) — uniquement pour les phases de stories
- Chemins exacts dans chaque description

## Path Conventions

Projet existant : paquet `md_cleaner/` et `tests/` à la racine (plan.md, section Source Code). `nettoyage.py`, `detection.py`, `segmentation.py`, `suggestion.py`, `cartographie.py` ne sont pas modifiés (seul le nom du fichier écrit change, pas son contenu ni la détection) ; `normalisation.py` reçoit la transformation pure (D1), `sortie.py` la résolution de collision (D4), `cli.py` le câblage (D5).

---

## Phase 1: Foundational (Blocking Prerequisites)

**Purpose**: Tests écrits d'abord (TDD) — ils DOIVENT échouer avant implémentation ; tests existants mis au nouveau comportement attendu.

- [ ] T001 [P] [US1] Étendre `tests/unit/test_normalisation.py` (nommage) : `nom_sortie_nettoye("retry-failed-records")` → `retry-failed-records-nettoye` (20 caractères exactement, aucun retrait, FR-001) ; `rapport` → `rapport-nettoye` ; `rapport annuel` → `rapport_annuel-nettoye` et un stem contenant une tabulation → chaque tabulation remplacée par un `_` (espace U+0020 et tabulation U+0009, chacun un `_`, FR-002) ; `rapport  annuel` (double espace) → `rapport__annuel-nettoye` (pas de compression, FR-002) ; un blanc en tête de stem → `_rapport-nettoye` et un blanc en fin de stem → `rapport_-nettoye` (pas de décapage, cas limite spec) ; `éco développement` → `éco_développement-nettoye` (accents et casse conservés, FR-002) ; `comptes-rendus-conseil-municipal-session-octobre` → `comptes-rendus-conse-nettoye` (troncature brute à 20 points de code, FR-003, clarification 2026-10-05) ; un stem uniquement composé de trois blancs → `___-nettoye` (cas limite spec)
- [ ] T002 [P] [US3] Créer `tests/unit/test_sortie.py` (résolution de collision, D4) : dossier vide → nom retourné tel quel `<base>-nettoye.md` ; `<base>-nettoye.md` existant → `<base>-nettoye-1.md` (suffixe à la fin, avant l'extension, clarification 2026-10-05, FR-004) ; `<base>-nettoye.md` et `<base>-nettoye-1.md` existants → `<base>-nettoye-2.md` ; les fichiers existants ne sont ni modifiés ni supprimés (SC-003)
- [ ] T003 [P] [US1] Étendre `tests/integration/test_nettoyage_simple.py` : run CLI sur une entrée nommée `retry-failed-records.md` (dossier temporaire) → le fichier nettoyé du run s'appelle `retry-failed-records-nettoye.md`, aucun `nettoye.md` dans l'arborescence de sortie (FR-001, SC-001) ; le message de fin affiche le chemin réel du fichier renommé (FR-006)
- [ ] T004 [P] [US2] Étendre `tests/integration/test_nettoyage_simple.py` : entrée `comptes-rendus-conseil-municipal-session-octobre.md` (49 caractères) → sortie `comptes-rendus-conse-nettoye.md` (base de 20 caractères exactement, FR-003) ; entrée `rapport annuel.md` → sortie `rapport_annuel-nettoye.md` ; entrée `éco développement.md` → sortie `éco_développement-nettoye.md` (US2, scénario 3)
- [ ] T005 [P] [US3] Étendre `tests/integration/test_nettoyage_simple.py` : deux runs successifs sur la même entrée `retry-failed-records.md` vers le même `--sortie` → dossiers `001` et `002`, chacun contenant `retry-failed-records-nettoye.md`, le fichier du premier run intact (jamais d'écrasement, FR-004, SC-003)
- [ ] T006 Mettre à jour les ~20 chemins attendus des tests d'intégration existants au nouveau nommage (D6) : `tests/integration/test_nettoyage_simple.py`, `tests/integration/test_nettoyage_liens.py`, `tests/integration/test_dry_run.py`, `tests/integration/test_extrait.py`, `tests/integration/test_calibrage.py`, `tests/integration/test_decidabilite.py`, `tests/integration/test_pagination.py` — chaque occurrence de `"nettoye.md"` devient le nom dérivé du stem de l'entrée du test (tronqué à 20 caractères, blancs → `_`) ; `nettoye-pagine.md`, `cartographie.json`, `suggestion.json`, `rapport-dry-run.md` inchangés (FR-005) ; `tests/integration/test_dry_run.py:18` (aucun `nettoye.md` en dry-run) devient : aucun fichier `*-nettoye.md` (rglob `*-nettoye.md`)

**Checkpoint**: les nouveaux tests T001-T005 échouent pour la bonne raison (aucune fonction de nommage, sortie encore fixe `nettoye.md`) ; les tests existants de T006 échouent également ; les garde-fous (artefacts secondaires inchangés) doivent déjà passer.

---

## Phase 2: User Story 1 - Sortie reconnaissable par son nom (Priority: P1) — MVP

**Goal**: le fichier nettoyé d'un run porte un nom dérivé du document d'entrée, prévisible et affiché par la commande.

**Independent Test**: `pytest tests/unit/test_normalisation.py` puis run sur une entrée `retry-failed-records.md` : sortie `retry-failed-records-nettoye.md`, message de fin exact (FR-001, FR-006, SC-001).

### Implementation for User Story 1

- [ ] T007 [US1] Implémenter `nom_sortie_nettoye(stem: str) -> str` dans `md_cleaner/normalisation.py` (D1, D2, D3) : remplacer chaque espace U+0020 et tabulation U+0009 par exactement un `_` (ni compression ni décapage), tronquer aux 20 premiers caractères (points de code Unicode, `len()`), tout autre caractère conservé tel quel, retourner `<base>-nettoye` — l'extension `.md` est ajoutée par l'appelant ; docstring référençant le contrat `specs/006-nom-sortie-source/contracts/nommage-sortie.md` ; ne pas toucher `slug_titre`
- [ ] T008 [US1] Câbler dans `md_cleaner/cli.py` (D5) : après `creer_dossier_run`, calculer `chemin_nettoye = dossier / (nom_sortie_nettoye(fichier.stem) + ".md")` ; remplacer `ecrire_nettoye(dossier / "nettoye.md", ...)` (ligne ~210) et le message `Sortie : ...` (ligne ~222) par ce chemin (FR-001, FR-006) ; import depuis `md_cleaner.normalisation` ; `nettoye-pagine.md` et les autres artefacts inchangés (FR-005)
- [ ] T009 [US1] Vérifier que T001, T003 et T006 passent et que la suite complète reste au vert : `pytest` (SC-001) — corriger l'implémentation, jamais les tests, en cas d'écart

**Checkpoint**: un run standard produit `<stem>-nettoye.md` et l'affiche ; la suite est au vert.

---

## Phase 3: User Story 2 - Noms longs : troncature prévisible (Priority: P2)

**Goal**: toute entrée, longue ou courte, accentuée ou avec blancs, produit le nom attendu par la règle unique.

**Independent Test**: `pytest tests/integration/test_nettoyage_simple.py` — troncature à 20, espaces, accents (US2, SC-002).

### Implementation for User Story 2

- [ ] T010 [US2] Vérifier que T004 passe avec l'implémentation de T007 (garde-fou par construction : la règle de troncature et de remplacement est déjà couverte par la fonction, D3) — aucune modification de code attendue ; si le test échoue, corriger `nom_sortie_nettoye` (T007), jamais le test

**Checkpoint**: US2 verrouillé par test ; US1 reste fonctionnel.

---

## Phase 4: User Story 3 - Jamais d'écrasement silencieux (Priority: P3)

**Goal**: tout conflit de nom à l'emplacement d'écriture se solde par un suffixe numérique ; aucun fichier existant n'est écrasé.

**Independent Test**: `pytest tests/unit/test_sortie.py` (suffixes `-1`, `-2`, fichiers intacts) et `pytest tests/integration/test_nettoyage_simple.py` (deux runs, premier intact) (FR-004, SC-003).

### Implementation for User Story 3

- [ ] T011 [US3] Implémenter la résolution de collision dans `md_cleaner/sortie.py` (D4) : fonction retournant le premier chemin libre parmi `<dossier>/<base>-nettoye.md`, `<base>-nettoye-1.md`, `<base>-nettoye-2.md`, ... (suffixe à la fin, avant l'extension ; départ à `-1`, décision utilisateur 2026-10-05) ; jamais d'écriture si le nom existe ; indépendante de la boucle de `creer_dossier_run` (qui démarre à `-2` et nomme des dossiers)
- [ ] T012 [US3] Câbler la résolution dans `md_cleaner/cli.py` : `chemin_nettoye` (T008) passe par la résolution de collision avant `ecrire_nettoye` (FR-004) ; le message `Sortie :` affiche le chemin résolu
- [ ] T013 [US3] Vérifier que T002 et T005 passent et que la suite complète reste au vert : `pytest` (SC-003)

**Checkpoint**: la garantie de non-écrasement est verrouillée par tests ; US1/US2 inchangés.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Documentation et validation transversales (D6).

- [ ] T014 [P] Mettre à jour `README.md` : ligne 51 (`notepad .\output\001\nettoye.md` → exemple avec nom dérivé, ex. `notepad .\output\001\retry-failed-records-nettoye.md`) et ligne 90 (aide `--pagine`, mention du nommage si pertinente) ; référencer la règle de nommage (20 premiers caractères, blancs → `_`, suffixe `-nettoye`, collision `-1`)
- [ ] T015 [P] Réviser `specs/001-nettoyage-md-repetitif/contracts/cli.md` : table des artefacts (lignes 38-39) — `nettoyage simple` produit `<nom-dérivé>-nettoye.md` avec référence au contrat `specs/006-nom-sortie-source/contracts/nommage-sortie.md` ; vérifier que `specs/004-nettoyage-liens-html/contracts/nettoyage-liens.md` et `specs/005-nettoyage-liens-absolus/contracts/nettoyage-liens-absolus.md` ne référencent pas le nom de fichier (contenu uniquement, attendu sans changement)
- [ ] T016 Exécuter les scénarios 1 à 4 de `specs/006-nom-sortie-source/quickstart.md` en local et consigner les résultats (le scénario 5 est couvert par la suite `pytest` des phases précédentes)
- [ ] T017 Suite complète au vert et lint conforme : `pytest` puis `ruff check md_cleaner tests` et `pre-commit run --all-files` — aucun relâchement

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 1)**: aucune dépendance — à faire d'abord ; BLOQUE toutes les stories
- **US1 (Phase 2)**: dépend de Phase 1 (T001, T003, T006) — MVP
- **US2 (Phase 3)**: dépend de T007 (US1) — vérification seule, aucune implémentation attendue
- **US3 (Phase 4)**: dépend de T008 (câblage US1 à étendre avec la résolution)
- **Polish (Phase 5)**: dépend de toutes les stories

### Parallel Opportunities

- T001 à T005 : cinq fichiers de tests différents ou sections disjointes — parallélisables
- T014 et T015 : fichiers différents — parallélisables
- T007 (`normalisation.py`) et T011 (`sortie.py`) : fichiers différents, mais T012 dépend des deux — exécuter T007 avant T011/T012 si séquentiel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1 complète (tests d'abord, checkpoint d'échec pour la bonne raison)
2. Phase 2 (US1) → valider : run nominal produit et affiche `<stem>-nettoye.md`
3. **STOP et VALIDER** : la suite `pytest` est au vert

### Incremental Delivery

1. US1 → MVP (le besoin central : reconnaître la source)
2. US2 → troncature et caractères vérifiés (rien à implémenter, la règle est unique)
3. US3 → garantie de non-écrasement
4. Polish → README, contrat 001, quickstart, suite et lint au vert

---

## Notes

- [P] = fichiers différents, pas de dépendance envers une tâche incomplète
- Corriger l'implémentation, jamais les tests, en cas d'écart (T009, T010)
- Le contenu du fichier nettoyé, la détection, la suggestion et la cartographie ne sont pas touchés par cette feature — toute régression de contenu est un signal d'implémentation erronée
- Committer après chaque tâche ou groupe logique ; la spec clarifiée, le plan et le présent fichier sont à committer ensemble (branche `014-outputfix`)
