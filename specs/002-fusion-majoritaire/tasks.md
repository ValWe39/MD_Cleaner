---
description: "Task list for feature implementation"
---

# Tasks: Décidabilité des motifs au dry-run (fusion majoritaire)

**Input**: Design documents from `/specs/002-fusion-majoritaire/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/rapport-dry-run.md, quickstart.md

**Tests**: inclus — la spec rend chaque critère mécaniquement vérifiable (SC-001 à SC-006) et le quickstart exige `pytest` (Scénario 0).

**Organization**: tâches groupées par user story (US1-US3) ; la feature modifie un outil existant, aucun setup de projet n'est requis — la Phase 1 ci-dessous est directement le socle de tests.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: exécutable en parallèle (fichiers différents, pas de dépendance envers une tâche incomplète)
- **[Story]**: user story de rattachement (US1, US2, US3) — uniquement pour les phases de stories
- Chemins exacts dans chaque description

## Path Conventions

Projet existant : paquet `md_cleaner/` et `tests/` à la racine (plan.md de la feature 002, section Source Code).

---

## Phase 1: Foundational (Blocking Prerequisites)

**Purpose**: Tests écrits d'abord (TDD) — ils DOIVENT échouer avant implémentation. La feature modifie un outil existant ; aucun setup de projet.

- [x] T001 [P] [US1] Étendre `tests/unit/test_detection.py` : frontière majoritaire stricte — une candidate chevauchant un bloc sur exactement la moitié de ses pages ne fusionne PAS (deux blocs distincts), sur strictement plus de la moitié elle fusionne (FR-001, clarification du 2026-09-29, D1)
- [x] T002 [P] [US1] Créer `tests/integration/test_decidabilite.py` : sur `Examples/Exemple_2/2.Input/consolidated.md` — zone filtres et métadonnées de publications dans des motifs distincts (SC-001) ; nombre de motifs `supprimer` ≤ 5 (SC-003) ; bascule ciblée (filtres `supprimer`, métadonnées `conserver`) produit un `nettoye.md` sans filtres mais avec les métadonnées (US1, scénario 2)
- [x] T003 [US1] Étendre `tests/integration/test_decidabilite.py` : non-régression `Examples/Exemple_1/2.Input/consolidated.md` — 4 motifs, zones couvertes et actions identiques à la version précédente (SC-002, FR-003) ; déterminisme octet par octet sur double exécution (SC-005)
- [x] T004 [P] [US2] Étendre `tests/unit/test_suggestion.py` : `generer_rapport()` sépare les motifs `supprimer` (tableau « Décisions requises ») de tous les motifs `conserver` (section secondaire, aucune action requise) ; sections vides affichées « aucun » (FR-004, D3, contracts/rapport-dry-run.md)
- [x] T005 [P] [US2] Étendre `tests/integration/test_dry_run.py` : sur Exemple_1, pas de section secondaire superflue (US2, scénario 3) ; sur Exemple_2, le tableau des décisions requises énumère ≤ 5 lignes (SC-003)

**Checkpoint**: tous les nouveaux tests échouent pour la bonne raison (fusion actuelle soude tout ; rapport actuel à une seule table)

---

## Phase 2: User Story 1 - Décider séparément interface et métadonnées (Priority: P1) — MVP

**Goal**: la coupure de fusion majoritaire sépare les zones hétérogènes ; les blocs compacts ne changent pas.

**Independent Test**: `pytest tests/unit/test_detection.py tests/integration/test_decidabilite.py` — frontière stricte vérifiée, Exemple_2 séparé, Exemple_1 inchangé.

### Implementation for User Story 1

- [x] T006 [US1] Modifier le filtre d'admission de fusion dans `md_cleaner/detection.py` (boucle `touches`) : pour chaque bloc existant, compter les pages de la candidate où le chevauchement se produit ; fusionner la candidate avec les blocs où `2 * pages_chevauchantes > len(pages_cles)` (strictement plus de la moitié, comparaison entière — D1, D6) ; à la moitié exacte ou moins, la candidate crée son propre bloc ; multi-blocs admissibles fusionnent tous dans le premier (D2) ; commentaire renvoyant à FR-001 et à la clarification du 2026-09-29 ; ne rien changer d'autre dans `detecter()` (tri, ids, emplacements)
- [x] T007 [US1] Vérifier que les tests T001-T003 passent et que la suite existante reste au vert sans relâchement de seuil (SC-004) : `pytest`

**Checkpoint**: User Story 1 fonctionnelle — la séparation filtres/métadonnées est effective, Exemple_1 inchangé

---

## Phase 3: User Story 2 - Charge de validation maîtrisée (Priority: P2)

**Goal**: le rapport dry-run reste lisible malgré la multiplication des motifs (~25 listés, ≤ 5 décisions réelles).

**Independent Test**: `pytest tests/unit/test_suggestion.py tests/integration/test_dry_run.py` — deux sections, « aucun » quand vide, tableau ≤ 5 lignes sur Exemple_2.

### Implementation for User Story 2

- [x] T008 [US2] Modifier `generer_rapport()` dans `md_cleaner/suggestion.py` : deux sections conformes à `specs/002-fusion-majoritaire/contracts/rapport-dry-run.md` — tableau « Décisions requises » (motifs `action = supprimer` uniquement), section « Motifs conservés par défaut — aucune action requise » (tous les motifs `conserver`, sous le seuil ou non) remplaçant l'actuelle section « sous le seuil » ; « aucun » affiché pour une section vide ; sections « Cas limites » et « Appliquer la suggestion » inchangées (D3) ; `suggestion.json` inchangé (tous les motifs, chacun actionnable)
- [x] T009 [US2] Vérifier que les tests T004-T005 passent et que le rapport d'un document riche reste parcourable en moins de 5 minutes (SC-006, validation manuelle du quickstart Scénario 2)

**Checkpoint**: User Stories 1 et 2 fonctionnelles indépendamment

---

## Phase 4: User Story 3 - Continuité des suggestions entre versions (Priority: P3)

**Goal**: l'utilisateur est informé ; la consommation d'une suggestion obsolète échoue proprement.

**Independent Test**: le test existant `test_appliquer_actions_id_inconnu` (feature 001) reste au vert ; le README mentionne la régénération.

### Implementation for User Story 3

- [x] T010 [US3] Modifier `README.md` : ajouter une note « les ids de motifs ne sont pas stables entre versions de l'outil ; après une mise à jour, régénérez la suggestion par dry-run ; une suggestion d'une version antérieure échoue proprement (id inconnu, code 2) » (FR-007, D4) — aucune modification de code, le comportement d'échec étant déjà couvert par le test existant (FR-008)
- [x] T011 [US3] Exécuter le Scénario 4 du quickstart (`quickstart.md`) avec une suggestion générée avant la feature : échec rapide, code 2, message ids inconnus — consigner le résultat

**Checkpoint**: les trois user stories sont fonctionnelles indépendamment

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: validation transversale des trois stories

- [x] T012 [P] Exécuter la validation complète de `specs/002-fusion-majoritaire/quickstart.md` (Scénarios 0 à 5) et consigner tout écart
- [x] T013 Revue de conformité : `ruff check` et `ruff format` sur les fichiers modifiés (`md_cleaner/detection.py`, `md_cleaner/suggestion.py`, tests, README), puis `pre-commit run --all-files` complet — zéro nouvelle dépendance, zéro option CLI ajoutée (FR-010), déterminisme re-vérifié (SC-005)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (tests d'abord)**: démarrage immédiat — les tests DOIVENT échouer avant la Phase 2
- **Phase 2 (US1)**: dépend de la Phase 1 — cœur de la feature, MVP
- **Phase 3 (US2)**: dépend de la Phase 1 ; indépendante de US1 (le rapport à deux sections fonctionne quelle que soit la règle de fusion) mais la validation complète n'a de sens qu'après US1
- **Phase 4 (US3)**: indépendante (documentation + comportement déjà couvert) — parallélisable dès la Phase 1
- **Phase 5 (Polish)**: dépend de toutes les stories

### User Story Dependencies

- **US1 (P1)**: aucune dépendance inter-stories — la base
- **US2 (P2)**: s'appuie sur les mêmes motifs que US1 mais se teste indépendamment (rapport)
- **US3 (P3)**: aucune dépendance — documentation

### Within Each User Story

- Tests écrits d'abord et ÉCHOUANT avant implémentation
- Un seul fichier de production par story (`detection.py` pour US1, `suggestion.py` pour US2) — pas de conflit

### Parallel Opportunities

- T001/T004 en parallèle (fichiers de test différents) ; T002/T005 en parallèle (test_decidabilite.py / test_dry_run.py)
- US2 (T008) et US1 (T006) en parallèle : fichiers de production différents
- US3 (T010) en parallèle de tout le reste : README uniquement

---

## Parallel Example: User Story 1

```bash
# Lancer les tests de US1 ensemble (échec attendu) :
Task: "Frontière majoritaire stricte dans tests/unit/test_detection.py"          # T001
Task: "Séparation et bascule ciblée dans tests/integration/test_decidabilite.py" # T002

# Puis l'implémentation (séquentielle, un seul fichier) :
Task: "Filtre d'admission majoritaire dans md_cleaner/detection.py"             # T006
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1: tests en échec
2. Phase 2: US1 (fusion majoritaire)
3. **STOP et VALIDER**: `pytest` — la séparation Exemple_2 et la non-régression Exemple_1 sont les critères go/no-go
4. Le MVP résout déjà le blocage d'origine (supprimer l'interface, garder les métadonnées)

### Incremental Delivery

1. Tests en échec → socle
2. US1 → MVP (la décision ciblée devient exprimable)
3. US2 → rapport lisible sur documents riches
4. US3 → continuité documentée
5. Polish → validation complète du quickstart

### Parallel Team Strategy

Avec plusieurs développeurs :

1. Tous sur la Phase 1 ensemble (tests)
2. Développeur A: US1 (`detection.py`) ; Développeur B: US2 (`suggestion.py`) ; Développeur C: US3 (README)
3. Polish ensemble

---

## Notes

- [P] = fichiers différents, pas de dépendances
- La feature 002 ne touche ni `nettoyage.py`, ni `cartographie.py`, ni `cli.py`, ni les formats JSON (D7) — si une tâche y semble nécessaire, c'est une alerte de dérive de périmètre
- Vérifier que les tests échouent avant d'implémenter
- Committer après chaque tâche ou groupe logique (workflow pre-commit du dépôt ; attention au titre anglais de la section « suivi de complexité » du template de plan, qui déclenche un faux positif du hook constitution)
- S'arrêter à tout checkpoint pour valider une story indépendamment
