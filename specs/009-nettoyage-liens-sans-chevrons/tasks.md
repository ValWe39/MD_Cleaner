---
description: "Task list template for feature implementation"
---

# Tasks: 009-nettoyage-liens-sans-chevrons

**Input**: Design documents from `/specs/009-nettoyage-liens-sans-chevrons/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md,
contracts/nettoyage-liens-sans-chevrons.md, quickstart.md

**Tests**: inclus — la spec exige une suite au vert sans relâchement
(SC-005) et des tests couvrant chaque forme (FR-001 à FR-008).

**Organization**: tâches groupées par user story (US1 à US4, spec.md),
chaque story étant implémentable et testable indépendamment.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: exécutable en parallèle (fichiers différents, pas de dépendance)
- **[Story]**: user story de rattachement (US1-US4, spec.md)
- Chemins exacts dans chaque description

## Path Conventions

Projet unique : paquet `md_cleaner/` et `tests/{unit,integration}` à la
racine du dépôt (structure existante, inchangée — plan.md).

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: vérifier l'environnement de départ avant toute modification.

- [x] T001 Vérifier la présence locale du corpus de calibration
  `Examples/Nettoyage-balises/` (5 fichiers
  `fipeco.fr-00003{3..7}-nettoye.md`, gitignoré) et la baseline :
  `pytest tests/unit/test_nettoyage_liens.py
  tests/integration/test_nettoyage_liens.py` au vert sur le HEAD courant

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: briques textuelles partagées par toutes les stories ;
aucun comportement changé à ce stade (`nettoyer_destinations` intacte).

- [x] T002 [P] Ajouter dans `md_cleaner/nettoyage.py` la constante
  `RE_IMAGE_INLINE` (construct `![alt](destination)`, alt sans crochet
  fermant — limite D2 de research.md) et les fonctions de
  protection/restauration par sentinelles éphémères sans `](` ni `](<`
  (D2, D4) ; les sentinelles sont invisibles pour les deux passes
- [x] T003 [P] Ajouter dans `md_cleaner/nettoyage.py` la constante
  `RE_DESTINATION_SANS_CHEVRONS` : sous-chaîne `(...)` suivant un
  crochet fermant, destination sans espaces ne commençant pas par `<`
  (exclusion `(?!<)`, D3), destination vide `(#)` couverte, titre
  éventuel `](url "titre")` emporté (FR-007) ; la règle chevron
  `RE_DESTINATION_LIEN` reste strictement inchangée (D1)

**Checkpoint**: briques en place, aucun comportement modifié — les
stories peuvent démarrer.

---

## Phase 3: User Story 1 - Sortie sans destinations sans chevrons (P1) - MVP

**Goal**: sans réglage, les sorties livrables ne contiennent plus aucune
destination de lien sans chevrons ; libellés et texte inchangés.

**Independent Test**: rejouer le nettoyage des 5 fichiers de
`Examples/Nettoyage-balises/` et vérifier 0 destination résiduelle
(baseline 199) avec libellés présents (SC-001, SC-002).

### Tests for User Story 1

> **NOTE**: écrire ces tests AVANT l'implémentation, les faire ÉCHOUER
> d'abord.

- [x] T004 [P] [US1] Étendre `tests/unit/test_nettoyage_liens.py` :
  ancre `(#main-content)` et `(#)`, relatif-racine `(/fiches)`, relatif
  sans slash `(Les-crédits-dimp...)`, absolu `(https://...)`, titre
  `](url "titre")` sans chevrons, plusieurs liens par ligne, note de
  bas de page `[[1]](#_ftn1)`, ligne entièrement-lien conservée
  (FR-001, FR-002, FR-007)
- [x] T005 [P] [US1] Étendre `tests/integration/test_nettoyage_liens.py` :
  run sur les 5 fichiers de `Examples/Nettoyage-balises/` (skip si le
  dossier est absent — corpus gitignoré), 0 destination sans chevrons
  dans les sorties, libellés et ordre des lignes inchangés (SC-001)

### Implementation for User Story 1

- [x] T006 [US1] Intégrer dans `md_cleaner/nettoyage.py`
  `nettoyer_destinations` l'ordre D4 : protection images → passe
  chevrons inchangée → passe sans chevrons → restauration ; mettre à
  jour la docstring (règles D1, D3, D4) ; dépend de T002, T003
- [x] T007 [US1] Faire passer T004 et T005 au vert ; vérifier
  l'idempotence de la passe sur un document à double passage (FR-008)

**Checkpoint**: US1 fonctionnelle et testable indépendamment — MVP
livrable (quickstart.md scénario 1).

---

## Phase 4: User Story 2 - Réversibilité --conserver-liens (P2)

**Goal**: `--conserver-liens` produit des sorties identiques au
comportement antérieur, octet par octet, toutes formes comprises.

**Independent Test**: comparer la sortie d'un run `--conserver-liens`
sur le corpus de calibration à la sortie produite sans la feature
(FR-004, quickstart.md scénario 2).

### Tests for User Story 2

- [x] T008 [P] [US2] Étendre `tests/unit/test_nettoyage_liens.py` :
  `conserver_liens=True` laisse intactes les formes sans chevrons
  (ancres, relatifs, absolus) — les deux règles sont désactivées
  ensemble (FR-004)
- [x] T009 [P] [US2] Étendre `tests/integration/test_nettoyage_liens.py` :
  run `--conserver-liens` sur un fichier du corpus
  `Examples/Nettoyage-balises/`, sortie octet par octet identique à la
  sortie produite sans la feature (FR-004)

### Implementation for User Story 2

- [x] T010 [US2] Vérifier la propagation du drapeau existant dans
  `md_cleaner/cli.py` → `ecrire_nettoye`/`ecrire_nettoye_pagine` : aucun
  changement de code attendu (contrat D5), sinon corriger ; faire
  passer T008 et T009 au vert

**Checkpoint**: US1 et US2 indépendamment fonctionnelles.

---

## Phase 5: User Story 3 - Garde-fous images, URLs nues, code (P3)

**Goal**: aucune image altérée ; URLs nues et blocs de code intacts ;
résidus documentés (logo réduit, `[[1]]`) tolérés.

**Independent Test**: document construit avec image, logo imbriqué, URL
nue et bloc de code — chacun retrouvé intact dans la sortie (FR-003,
FR-006, quickstart.md scénarios 1 et 4).

### Tests for User Story 3

- [x] T011 [P] [US3] Étendre `tests/unit/test_nettoyage_liens.py` :
  image simple `![](/images/FIV11a.png)` inchangée octet par octet ;
  logo imbriqué `[![FIPECO](/images/logo.jpg)](/)` devient
  `[![FIPECO](/images/logo.jpg)]` (FR-003, D7) ; alt contenant un
  crochet fermant → ligne inchangée (limite D2) ; URL nue hors lien et
  contenu de bloc de code intacts (FR-006, D6)

### Implementation for User Story 3

- [x] T012 [US3] Faire passer T011 au vert en s'appuyant sur la
  protection T002 (aucune règle supplémentaire attendue — si un cas
  échoue, corriger la protection ou documenter l'écart dans
  `specs/009-nettoyage-liens-sans-chevrons/research.md`

**Checkpoint**: toutes les stories 1-3 indépendamment fonctionnelles.

---

## Phase 6: User Story 4 - Non-régression formes et corpus (P4)

**Goal**: sorties des corpus historiques inchangées octet par octet ;
comportement chevron 004/005 identique ; documents sans liens inchangés.

**Independent Test**: `diff` des sorties d'Exemple_1 à Exemple_3 contre
les sorties de référence produites avant la feature (SC-003, FR-005,
quickstart.md scénario 3).

### Tests for User Story 4

- [x] T013 [P] [US4] Étendre `tests/integration/test_nettoyage_liens.py` :
  neutralité octet par octet sur `Examples/Exemple_1/2.Input/consolidated.md`,
  `Examples/Exemple_2/2.Input/consolidated.md` et
  `Examples/Exemple_3/2.Input/retry-failed-records.md` (0 forme sans
  chevrons dans ces corpus — SC-003), et corpus sans aucune forme de
  destination inchangé
- [x] T014 [P] [US4] Étendre `tests/unit/test_nettoyage_liens.py` :
  formes chevrons `](<...>)` et `](<...> "titre")` traitées à
  l'identique de 004/005 (mêmes sorties que les tests existants,
  FR-005) ; marqueurs `<!-- page: N -->` et pagination intacts

### Implementation for User Story 4

- [x] T015 [US4] Faire passer T013 et T014 au vert ; tout écart
  indique une atteinte à D1 — corriger la passe sans chevrons sans
  toucher la règle chevron

**Checkpoint**: les 4 stories sont fonctionnelles ; la suite complète
est au vert.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: documentation, contrats et validation de bout en bout.

- [x] T016 [P] Mettre à jour l'aide du drapeau `--conserver-liens` dans
  `md_cleaner/cli.py` : couvre désormais les destinations avec et sans
  chevrons
- [x] T017 [P] Mettre à jour `README.md` : section
  `--conserver-liens` étendue aux formes sans chevrons
- [x] T018 [P] Réviser
  `specs/005-nettoyage-liens-absolus/contracts/nettoyage-liens-absolus.md` :
  la borne « formes sans chevrons hors périmètre » devient un renvoi au
  contrat 009
- [x] T019 Exécuter la validation de bout en bout
  `specs/009-nettoyage-liens-sans-chevrons/quickstart.md` (scénarios 1
  à 5) sur le corpus réel `Examples/Nettoyage-balises/`
- [x] T020 Revue finale : `ruff` et `markdownlint` au vert, suite
  complète `pytest` au vert, aucun diff inattendu dans le dépôt

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: aucune dépendance — démarrage immédiat
- **Foundational (Phase 2)**: dépend du Setup — BLOQUE toutes les
  stories (T002, T003 sont des briques communes)
- **User Stories (Phases 3-6)**: dépendent de la Phase 2 ; US1 à US4
  peuvent ensuite avancer en parallèle ou séquentiellement (P1 → P4)
- **Polish (Phase 7)**: dépend des stories retenues ; T019 exige US1-US4
  complètes

### User Story Dependencies

- **US1 (P1)**: après Phase 2 — dépend de T002, T003 (intégration D4)
- **US2 (P2)**: après Phase 2 — indépendante ; le drapeau existant
  couvre la nouvelle passe (contrat CLI inchangé)
- **US3 (P3)**: après Phase 2 — indépendante ; s'appuie sur T002
- **US4 (P4)**: après Phase 2 — indépendante ; neutre par construction
  (D1), les tests verrouillent la non-régression

### Within Each User Story

- Tests d'abord (échec attendu avant implémentation)
- Briques (Phase 2) avant intégration
- Implémentation avant vérification finale de la story

### Parallel Opportunities

- T002 et T003 en parallèle (Phase 2)
- T004 et T005 en parallèle (US1) ; T008 et T009 (US2) ; T013 et T014
  (US4) — fichiers ou périmètres distincts
- T016, T017, T018 en parallèle (Phase 7, fichiers distincts)
- Les stories US1-US4 peuvent être menées en parallèle par des
  intervenants différents une fois la Phase 2 terminée

---

## Parallel Example: User Story 1

```text
# Lancer ensemble les tests de la story (échec attendu) :
Tâche: "Étendre tests/unit/test_nettoyage_liens.py (formes sans chevrons)"
Tâche: "Étendre tests/integration/test_nettoyage_liens.py (corpus)"

# Puis l'implémentation (dépend de T002, T003) :
Tâche: "Intégrer l'ordre D4 dans nettoyer_destinations (nettoyage.py)"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1 : baseline verte, corpus présent
2. Phase 2 : T002 + T003 (briques)
3. Phase 3 : US1 complète (T004-T007)
4. **STOP et VALIDER** : quickstart.md scénario 1 sur le corpus réel

### Incremental Delivery

1. Setup puis Foundational → fondation prête
2. Ajout US1 → test indépendant → MVP (SC-001 tenu sur le corpus réel)
3. Ajout US2 → réversibilité verrouillée
4. Ajout US3 → garde-fous verrouillés
5. Ajout US4 → non-régression verrouillée
6. Phase 7 → documentation à jour, quickstart complet

---

## Notes

- [P] = fichiers différents, pas de dépendance entre tâches en cours
- Les tests sur `Examples/Nettoyage-balises/` skippent si le dossier
  est absent (corpus gitignoré, présent localement)
- Committer après chaque tâche ou groupe logique
- S'arrêter à chaque checkpoint pour valider la story indépendamment
