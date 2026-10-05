---
description: "Task list for feature implementation"
---

# Tasks: Nettoyage des destinations de liens absolues à l'écriture de la sortie

**Input**: Design documents from `/specs/005-nettoyage-liens-absolus/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/nettoyage-liens-absolus.md, quickstart.md

**Tests**: inclus — SC-007 exige la suite au vert sans relâchement et le quickstart exige `pytest` (Scénario 7).

**Organization**: tâches groupées par user story (US1-US4) ; la feature modifie un outil existant, aucun setup de projet n'est requis — la Phase 1 est le socle de tests écrits d'abord (TDD), par référence au cycle validé en 004.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: exécutable en parallèle (fichiers différents, pas de dépendance envers une tâche incomplète)
- **[Story]**: user story de rattachement (US1, US2, US3, US4) — uniquement pour les phases de stories
- Chemins exacts dans chaque description

## Path Conventions

Projet existant : paquet `md_cleaner/` et `tests/` à la racine (plan.md, section Source Code). `detection.py`, `suggestion.py`, `cartographie.py` et `cli.py` ne sont pas modifiés pour la règle (D3 : la passe vit dans `nettoyage.py`, en aval de la détection ; D4 : le drapeau `--conserver-liens` existant couvre déjà tout) — seule l'aide CLI de `--conserver-liens` est mise à jour en Polish pour rester exacte.

---

## Phase 1: Foundational (Blocking Prerequisites)

**Purpose**: Tests écrits d'abord (TDD) — ils DOIVENT échouer avant implémentation.

- [x] T001 [P] [US1] Étendre `tests/unit/test_nettoyage_liens.py` : `[Try Studio ](<https://console.mistral.ai?utm_source=docs&utm_medium=header_cta>)` devient `[Try Studio ]` (FR-001) ; `](<http://...>)` idem ; `[Contact](<mailto:contact@exemple.fr>)` et `](<tel:+33123456789>)` retirés — même règle, aucun cas particulier (clarification 2026-10-05, option A) ; plusieurs liens absolus sur une même ligne tous retirés (US1, scénario 3) ; `[](<https://exemple.fr>)` → destination retirée, crochets vides conservés ; `](https://exemple.fr)` sans chevrons et `](chemin)` nu inchangés (hors périmètre) ; URL nue dans le texte et `<!-- page: 3 -->` inchangés ; idempotence (2e passe = no-op)
- [x] T002 [P] [US3] Étendre `tests/unit/test_nettoyage_liens.py` (formes à titre) : `[HCFP](<http://www.hcfp.fr/> "Haut Conseil des finances publiques \(HCFP\)\(nouvelle fenêtre\)")` devient `[HCFP]` (FR-002) ; titre court et titre avec échappements emportés tels quels ; lien relatif à titre `](</chemin> "titre")` → libellé seul (US3, scénario 2) ; cas limite D2 : titre contenant un guillemet interne échappé (`\"`) → ligne inchangée (non matché, sans corruption)
- [x] T003 [P] [US2] Étendre `tests/integration/test_nettoyage_liens.py` : document construit multi-pages contenant un bloc de code avec URL nue (`client = Mistral(api_key=...)`, `https://api.mistral.ai`) et une phrase avec URL nue hors syntaxe de lien → toutes les URLs nues intactes octet par octet dans `nettoye.md` (FR-007, SC-005)
- [x] T004 [US1] Étendre `tests/integration/test_nettoyage_liens.py` : run CLI sur `Examples/Exemple_3/2.Input/retry-failed-records.md` → aucune ligne de `nettoye.md` ne contient `](<` (SC-001, baseline 6/299), libellés `[Reach out]`, `[Try Studio ]`, `[Discord↗]` présents, nombre et ordre des lignes inchangés par rapport à un run `--conserver-liens` (SC-002)
- [x] T005 [P] [US4] Étendre `tests/integration/test_nettoyage_liens.py` : neutralité — sorties par défaut sur `Examples/Exemple_1/2.Input/consolidated.md` et `Examples/Exemple_2/2.Input/consolidated.md` identiques octet par octet aux sorties de la version 004 (SC-003) ; `--conserver-liens` conserve destinations absolues et titres, sorties identiques octet par octet à avant la feature (SC-004) ; `--pagine` → marqueurs `<!-- page: N -->` présents à l'identique et `cartographie.json` identique entre les deux modes (FR-003) ; `--dry-run` → `suggestion.json` et `rapport-dry-run.md` inchangés (FR-005)

**Checkpoint**: les nouveaux tests échouent pour la bonne raison (la règle en place ne couvre toujours que `](</...>)` : les formes absolues sans `/` et les titres ne sont pas retirés ; les garde-fous, eux, doivent déjà passer).

---

## Phase 2: User Story 1 - Sortie finale sans destinations résiduelles (Priority: P1) — MVP

**Goal**: le `nettoye.md` produit par un run standard ne contient plus aucune destination `](<...>)` quel que soit le schéma, libellés et reste du texte inchangés.

**Independent Test**: `pytest tests/unit/test_nettoyage_liens.py` puis run sur Exemple_3 : 0 destination dans `nettoye.md` (SC-001), libellés en place.

### Implementation for User Story 1

- [x] T006 [US1] Remplacer la regex de `nettoyer_destinations` dans `md_cleaner/nettoyage.py` : `(?<=\])\(</[^>]*>\)` → `(?<=\])\(<[^>]*>\)` — toute destination entre chevrons sans distinction de schéma, le premier `>` refermant toujours, sans décodage des caractères encodés, occurrences multiples par ligne (D1, FR-001, FR-006) ; mettre à jour la docstring de la fonction (formes couvertes, référence à la règle unifiée)
- [x] T007 [US1] Vérifier que T001 et T004 passent et que la suite complète reste au vert sans relâchement des seuils : `pytest` (SC-007) — les tests 004 doivent rester verts sans modification (règle en sur-ensemble, D6)

**Checkpoint**: un run standard sur Exemple_3 produit un `nettoye.md` sans destination ; la suite est au vert.

---

## Phase 3: User Story 2 - Garde-fou : les URLs légitimes du corps du texte sont conservées (Priority: P2)

**Goal**: les URLs nues (bloc de code, corps du texte) survivent au nettoyage ; la garantie est structurelle (lookbehind `]`).

**Independent Test**: document construit du T003 → URLs nues intactes octet par octet (SC-005).

### Implementation for User Story 2

- [x] T008 [US2] Vérifier que T003 passe avec la règle unifiée de T006 (garde-fou par construction, D5, FR-007) — aucune modification de code attendue ; si le test échoue, corriger la règle (T006), jamais le test

**Checkpoint**: le garde-fou est verrouillé par test ; US1 reste fonctionnel.

---

## Phase 4: User Story 3 - Liens avec titre : seul le libellé survit (Priority: P3)

**Goal**: les formes `(<url> "titre")` perdent destination et titre ; seuls les libellés restent.

**Independent Test**: `pytest tests/unit/test_nettoyage_liens.py` — les formes à titre (y compris HCFP d'Exemple_2) deviennent `[libellé]` (SC-006).

### Implementation for User Story 3

- [x] T009 [US3] Étendre la regex de `nettoyer_destinations` dans `md_cleaner/nettoyage.py` : `(?<=\])\(<[^>]*>\)` → `(?<=\])\(<[^>]*>(?: "[^"]*")?\)` — le titre éventuel (espace + guillemets compris) est emporté avec la destination, échappements tels quels (D2, FR-002, FR-006) ; docstring mise à jour
- [x] T010 [US3] Vérifier que T002 passe et que la suite complète reste au vert : `pytest` (SC-006, SC-007)

**Checkpoint**: seuls les libellés survivent sur toutes les formes chevrons, avec ou sans titre.

---

## Phase 5: User Story 4 - Désactivation unique et non-régression (Priority: P4)

**Goal**: `--conserver-liens` (existant) couvre l'ensemble ; les corpus 1/2 restent inchangés ; marqueurs et dry-run intacts.

**Independent Test**: T005 au vert — aucune modification de code attendue (D4).

### Implementation for User Story 4

- [x] T011 [US4] Vérifier que T005 passe (SC-003, SC-004, FR-003, FR-005) — aucune modification CLI attendue : `--conserver-liens` se propage déjà aux deux writers ; si un test échoue, investiguer la propagation dans `md_cleaner/nettoyage.py` sans toucher au contrat CLI (codes retour inchangés)

**Checkpoint**: les quatre stories sont indépendamment fonctionnelles ; la sortie paginée reste cohérente avec sa cartographie.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: documentation exacte, contrats et validation de bout en bout.

- [x] T012 [P] Mettre à jour l'aide de `--conserver-liens` dans `construire_analyseur` de `md_cleaner/cli.py` : « conserve les destinations de liens inline `](<...>)` » (au lieu de `](</...>)`) — exactitude de l'aide, aucun changement de comportement ni de contrat (D4)
- [x] T013 [P] Mettre à jour `README.md` : description de l'option `--conserver-liens` (destinations entre chevrons, tout schéma) et exemple sur Exemple_3
- [x] T014 [P] Mettre à jour la table des options dans `specs/001-nettoyage-md-repetitif/contracts/cli.md` : description de `--conserver-liens` révisée par `specs/005-nettoyage-liens-absolus/contracts/nettoyage-liens-absolus.md`
- [x] T015 Exécuter les scénarios 1 à 7 de `specs/005-nettoyage-liens-absolus/quickstart.md` sur `Examples/Exemple_1`, `Exemple_2`, `Exemple_3` et le document garde-fou construit, et constater les attendus
- [x] T016 Vérification finale : `pytest` au vert et `pre-commit run --all-files` sans échec (SC-007)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundational (Phase 1)**: à faire d'abord — les tests DOIVENT échouer avant implémentation (TDD)
- **US1 (Phase 2)**: dépend de la Phase 1 — MVP
- **US2 (Phase 3)**: dépend de T006 (la règle unifiée existe) ; vérification pure
- **US3 (Phase 4)**: dépend de T006 (la base de la regex existe) ; indépendante de US2
- **US4 (Phase 5)**: dépend de T006 (et T009 pour les titres conservés par `--conserver-liens`) ; vérification pure
- **Polish (Phase 6)**: dépend de toutes les stories retenues

### User Story Dependencies

- **US1 (P1)**: aucune dépendance vers une autre story — MVP autonome
- **US2 (P2)**: propriété structurelle de la règle de US1, verrouillée par test
- **US3 (P3)**: extension de la regex de US1 (partie optionnelle titre)
- **US4 (P4)**: réutilise la règle complète ; aucune modification CLI (drapeau existant)

### Within Each User Story

- Tests d'abord (Phase 1), échec constaté pour la bonne raison
- Règle de base (T006) avant extension titre (T009)
- Vérifications (T008, T011) après implémentation
- Suite au vert à chaque checkpoint

### Parallel Opportunities

- T001, T002, T003 sont parallélisables (cas unitaires US1 / cas unitaires US3 / test d'intégration US2 — extensions du même fichier `tests/unit/test_nettoyage_liens.py` pour T001-T002 : écrire dans l'ordre T001 → T002 ou consolider après écriture parallèle)
- T003 et T005 touchent le même fichier d'intégration : ordre T003 → T004 → T005 recommandé, ou écriture parallèle puis consolidation
- T012, T013, T014 sont parallélisables en Polish (fichiers différents)

---

## Parallel Example: User Story 1

```bash
# Écriture des tests en parallèle (Phase 1) :
Task: "T001 Étendre tests/unit/test_nettoyage_liens.py (schémas absolus, garde-fou unitaire)"
Task: "T003 Étendre tests/integration/test_nettoyage_liens.py (document garde-fou)"

# Puis implémentation unique (Phase 2) :
Task: "T006 Remplacer la regex dans md_cleaner/nettoyage.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1 : tests écrits, échec constaté pour la bonne raison
2. Phase 2 : règle unifiée sans distinction de schéma (T006)
3. **STOP et VALIDER** : run sur Exemple_3 → 0 destination `](<` (SC-001), suite au vert

### Incremental Delivery

1. US1 → sortie standard nettoyée de toutes destinations chevrons (MVP)
2. US2 → garde-fou URLs légitimes verrouillé par test
3. US3 → titres couverts, seuls les libellés survivent
4. US4 → réversibilité et non-régression vérifiées
5. Polish → aide CLI, README, contrat 001, quickstart, vérification finale

---

## Notes

- [P] = fichiers différents, pas de dépendance envers une tâche incomplète
- Le [Story] rattache chaque tâche à sa story pour la traçabilité
- Les contraintes de la spec sont citées verbatim dans les descriptions (FR-001 à FR-009, SC-001 à SC-007, D1-D6, clarifications 2026-10-05)
- US2 et US4 sont des vérifications par construction : aucun code ne doit être écrit en dehors de T006 et T009 ; un test qui échoue signale un défaut de la règle, pas du test
- Committer après chaque tâche ou groupe logique
- Ne jamais relâcher un seuil de test existant (SC-007)
