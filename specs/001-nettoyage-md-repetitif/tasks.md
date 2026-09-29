---
description: "Task list template for feature implementation"
---

# Tasks: Nettoyage de fichiers Markdown répétitifs

**Input**: Design documents from `/specs/001-nettoyage-md-repetitif/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

**Tests**: inclus — la validation de bout en bout passe par `pytest` (quickstart.md, Scénario 0) et les critères de succès SC-001 à SC-006 sont mécaniquement vérifiables.

**Organization**: tâches groupées par user story (US1–US4) pour permettre l'implémentation et la validation indépendantes de chaque story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: exécutable en parallèle (fichiers différents, pas de dépendance envers une tâche incomplète)
- **[Story]**: user story de rattachement (US1, US2, US3, US4) — uniquement pour les phases de stories
- Chemins exacts dans chaque description

## Path Conventions

Projet unique (plan.md) : paquet `md_cleaner/` et `tests/` à la racine du dépôt. Fixtures d'intégration : `Examples/` via chemins relatifs.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialisation du projet et structure de base

- [x] T001 Créer la structure du projet : `md_cleaner/__init__.py`, `md_cleaner/__main__.py`, `tests/unit/__init__.py`, `tests/integration/__init__.py` (paquets vides, per plan.md)
- [x] T002 Créer `pyproject.toml` (setuptools, `requires-python >= 3.12`, console script `md-cleaner = md_cleaner.cli:main`) et `requirements.txt` listant `pytest` — répare au passage le job CI `audit` qui échoue sur son absence (research.md D10)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Socle indispensable à toutes les user stories

**CRITICAL**: aucune user story ne peut commencer avant la fin de cette phase

- [x] T003 Créer le squelette CLI argparse dans `md_cleaner/cli.py` : options du contrat [contracts/cli.md](../contracts/cli.md) (`--dry-run`, `--suggestion`, `--pagine`, `--seuil`, `--echantillon`, `--calibrage`, `--sortie`, `--nom-titre`), messages en français, codes retour « 3 usage invalide : combinaison d'options interdite, argument hors bornes », `--help` complet
- [x] T004 [P] Implémenter `md_cleaner/normalisation.py` : normalisation de lignes (URL → `<URL>`, nombres → `<N>`, dates → `<DATE>`, pliage des espaces multiples — research.md D3) et `slug_titre(texte, x)` (slug ASCII, research.md D8)
- [x] T005 Implémenter `md_cleaner/segmentation.py` : séparateurs explicites par regex `^#{1,6}\s*[Pp]age\s+(\d+)\s*(?::\s*(\S+))?$` en priorité ; à défaut repli heuristique déterministe (« lignes frontière » récurrentes) ; si moins de 2 segments fiables, document traité comme section unique et signalé — jamais de pagination trompeuse (FR-011, D4) ; renvoie `mode_segmentation` ∈ `explicite | heuristique | unique`
- [x] T006 [P] Implémenter la validation d'entrée dans `md_cleaner/cli.py` : fichier existant, lisible, extension `.md`, sinon échec rapide code « 1 entrée invalide » avec message clair (FR-015) ; chargement UTF-8 (BOM toléré) ; extraction du titre (premier titre niveau 1, sinon nom du fichier — D8)

**Checkpoint**: socle prêt — les user stories peuvent démarrer en parallèle

---

## Phase 3: User Story 1 - Nettoyage simple d'un fichier Markdown (Priority: P1) — MVP

**Goal**: un run sur un `.md` multi-pages produit `output/<run>/nettoye.md` sans le boilerplate répété, contenu de valeur conservé à 100 %, déterministe.

**Independent Test**: `md-cleaner Examples/Exemple_1/2.Input/consolidated.md` → sortie sans nav/footer répétés, toute ligne unique conservée, deux runs identiques octet par octet (quickstart.md Scénarios 1 et 7).

### Tests for User Story 1

> **NOTE**: écrire ces tests d'abord et s'assurer qu'ils ÉCHOUENT avant implémentation

- [x] T007 [P] [US1] Tests unitaires de normalisation dans `tests/unit/test_normalisation.py` : parties variables reconnues (numéro de leçon, date, URL changent d'une page à l'autre → même forme normalisée, FR-003) ; `slug_titre` (accents, collision de longueur)
- [x] T008 [P] [US1] Tests unitaires de segmentation dans `tests/unit/test_segmentation.py` : séparateurs explicites (avec et sans URL), repli heuristique, mode unique signalé, numéros séquentiels sans trou

### Implementation for User Story 1

- [x] T009 [US1] Implémenter la détection dans `md_cleaner/detection.py` : fenêtres glissantes de lignes w = 1 à 25, groupage par hachage des séquences normalisées, fusion des fenêtres candidates chevauchantes en blocs maximaux, fréquence = pages contenant le motif / pages totales, action par défaut `supprimer` si fréquence ≥ seuil sinon `conserver`, ids `M01`, `M02`, … triés par (première occurrence, fréquence décroissante, hachage) — déterministe (FR-002, FR-003, FR-005, D3) ; option `--seuil` : « entier 2–100, défaut 80 » (data-model.md, contracts/cli.md)
- [x] T010 [P] [US1] Implémenter le dossier de sortie dans `md_cleaner/sortie.py` : `./output` par défaut (`--sortie`), sous-dossier de run numéroté `NNN` séquentiel zéro-paddé (défaut) ou slug des X premiers caractères du titre (`--nom-titre`, « entier 5–100, défaut X = 30 »), collision → suffixe `-2`, `-3`, … (FR-006, D8)
- [x] T011 [US1] Implémenter le nettoyage dans `md_cleaner/nettoyage.py` : suppression des lignes appariées aux motifs `action = supprimer` (suggestion par défaut appliquée directement — chemin « sauter le dry-run », FR-008), contenu non altéré (formulation, ordre, hiérarchie de titres, FR-004), écriture de `nettoye.md` ; avertissements stderr FR-016 : document à page unique, sortie quasi vide
- [x] T012 [US1] Câbler le mode nettoyage par défaut dans `md_cleaner/cli.py` : sans `--dry-run` ni `--suggestion`, détection → suggestion par défaut → `nettoye.md` ; exit 0 ; code « 1 » si le fichier d'entrée est invalide
- [x] T013 [P] [US1] Tests unitaires de détection dans `tests/unit/test_detection.py` : fenêtres fusionnées, fréquences exactes, seuil 80 % par défaut et réglable, ids stables entre deux exécutions
- [x] T014 [P] [US1] Tests d'intégration US1 dans `tests/integration/test_nettoyage_simple.py` sur `Examples/Exemple_1/2.Input/consolidated.md` : ≥ 90 % du boilerplate supprimé, 100 % des lignes uniques conservées (diff), deux exécutions → sorties identiques octet par octet (SC-001, SC-002, SC-005)

**Checkpoint**: User Story 1 fonctionnelle et testable indépendamment — MVP atteignable ici

---

## Phase 4: User Story 2 - Dry-run et suggestion éditable (Priority: P2)

**Goal**: validation humaine des motifs avant nettoyage : rapport lisible + `suggestion.json` éditable consommé par le run suivant.

**Independent Test**: `--dry-run` sur un exemple → rapport + suggestion conformes au contrat, aucun `nettoye.md` ; bascule d'un `action` dans le JSON → appliquée au run suivant (quickstart.md Scénario 2).

### Tests for User Story 2

- [x] T015 [P] [US2] Tests unitaires de suggestion dans `tests/unit/test_suggestion.py` : validation stricte au chargement — JSON invalide, `version ≠ 1`, `source` ne correspondant pas, id dupliqué/inconnu, `action` invalide → code « 2 artefact fourni invalide » (contracts/formats.md)

### Implementation for User Story 2

- [x] T016 [US2] Implémenter l'écriture/lecture/validation de `suggestion.json` dans `md_cleaner/suggestion.py` : schéma exact de [contracts/formats.md](../contracts/formats.md) (`version: 1`, `source`, `seuil`, `mode_segmentation`, `nb_pages`, motifs avec `id M\d{2}`, `action ∈ supprimer|conserver`, `frequence` arrondie à 2 décimales, `pages` triées, `extrait` ≤ 3 lignes jointes par ` / `) ; sérialisation déterministe : clés triées, indentation 2, un saut de ligne en fin de fichier (D5, D9)
- [x] T017 [US2] Générer le rapport `rapport-dry-run.md` dans `md_cleaner/suggestion.py` : tableau des motifs (id, extrait, fréquence, pages, action suggérée), section « motifs sous le seuil », section « cas limites » (FR-016), rappel de la commande `--suggestion` (FR-007, SC-004)
- [x] T018 [US2] Câbler `--dry-run` et `--suggestion` dans `md_cleaner/cli.py` : dry-run → rapport + suggestion sans aucun fichier nettoyé ; `--suggestion` → validation puis application sans recalculer la détection ; `--dry-run` + `--suggestion` ensemble → code 3 (contracts/cli.md)
- [x] T019 [P] [US2] Tests d'intégration dry-run dans `tests/integration/test_dry_run.py` : `suggestion.json` conforme au contrat, édition `supprimer` → `conserver` appliquée au run suivant, id inconnu ajouté à la main → code 2 et message clair (SC-004)

**Checkpoint**: User Stories 1 et 2 fonctionnelles indépendamment

---

## Phase 5: User Story 3 - Sortie paginée et cartographie (Priority: P3)

**Goal**: situer chaque contenu nettoyé dans le document source : `.md` paginé lisible + `cartographie.json` cohérente pour le futur RAG.

**Independent Test**: `--pagine` sur un exemple → marqueurs `<!-- page: N -->` = entrées de la cartographie, aucun marqueur dans le `nettoye.md` simple (quickstart.md Scénarios 3 et 4).

### Tests for User Story 3

- [x] T020 [P] [US3] Tests unitaires de cartographie dans `tests/unit/test_cartographie.py` : ids `P\d+-B\d+` uniques et séquentiels, `mode_pagination` ∈ `explicite|heuristique|unique`, cohérence marqueurs/pages/blocs (contrat de cohérence de contracts/formats.md)

### Implementation for User Story 3

- [x] T021 [US3] Implémenter `cartographie.json` dans `md_cleaner/cartographie.py` : `version: 1`, `source`, `mode_pagination`, `pages` (page, `url_source` absente si le séparateur n'en portait pas, `marqueur` = chaîne exacte insérée, `blocs` triés), `blocs` (`id`, `page`, `debut`/`fin` indices de lignes dans la page, `fin` incluse) ; couverture exacte entre ids de blocs et références de pages (FR-010, D6)
- [x] T022 [US3] Implémenter la sortie paginée dans `md_cleaner/nettoyage.py` : `nettoye-pagine.md` avec séparateur `---` + commentaire `<!-- page: N -->` en tête de chaque page d'origine, lignes vides encadrantes ; `nettoye.md` simple sans aucun marqueur ni séparateur de pages (FR-009, FR-010, clarifications Q2→A et Q5→A)
- [x] T023 [US3] Câbler `--pagine` dans `md_cleaner/cli.py` : produit `nettoye.md`, `nettoye-pagine.md` et `cartographie.json` dans le même run ; `mode_pagination: "heuristique"` signalé sur stderr (FR-011)
- [x] T024 [P] [US3] Tests d'intégration pagination dans `tests/integration/test_pagination.py` : chaque marqueur de `nettoye-pagine.md` apparaît une et une seule fois, ensemble des ids de `cartographie.json` = références de `pages[].blocs`, document sans séparateurs → mode `heuristique` signalé ou `unique`, jamais de pagination silencieuse (SC-006)

**Checkpoint**: User Stories 1, 2 et 3 fonctionnelles indépendamment

---

## Phase 6: User Story 4 - Calibrage sur échantillon ou auto-calibrage (Priority: P4)

**Goal**: précision accrue de la détection : calibrage sur les 5 pages fournies par l'utilisateur, ou auto-calibrage sur les N premières pages du document.

**Independent Test**: `--echantillon Examples/Exemple_2/1.Sample` détecte au moins les mêmes motifs que l'auto-calibrage sur `Examples/Exemple_2/2.Input/consolidated.md` (quickstart.md Scénario 5).

### Tests for User Story 4

- [x] T025 [P] [US4] Tests unitaires de calibrage dans `tests/unit/test_calibrage.py` : échantillon ≤ 5 fichiers `.md` triés par nom, N = 5 par défaut (`--calibrage` « entier 2–50 »), dossier vide ou 6 fichiers → code 2

### Implementation for User Story 4

- [x] T026 [US4] Implémenter le calibrage dans `md_cleaner/detection.py` : `--echantillon <dossier>` (≤ 5 `.md` triés par nom, sinon code « 2 artefact fourni invalide ») ; à défaut auto-calibrage sur les N = 5 premières pages détectées (`--calibrage`, « entier 2–50, défaut 5 ») ; fenêtres candidates comptées sur l'échantillon puis fréquences confirmées sur le document complet (FR-012, FR-013, D7)
- [x] T027 [P] [US4] Tests d'intégration calibrage dans `tests/integration/test_calibrage.py` sur `Examples/Exemple_2` : l'échantillon des 5 premières pages détecte au moins les motifs de l'auto-calibrage (comparaison des `suggestion.json`), filtres et pagination d'interface détectés

**Checkpoint**: toutes les user stories fonctionnelles indépendamment

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Améliorations transversales aux stories

- [x] T028 [P] Exécuter la validation complète de [quickstart.md](../quickstart.md) (Scénarios 0 à 8) et consigner tout écart constaté dans ce fichier
- [x] T029 [P] Mettre à jour `README.md` : installation (`pip install -e .`), usage, options du contrat CLI, exemples
- [x] T030 Vérifier la performance SC-003 : document de plusieurs centaines de pages (Exemple_2 concaténé x3, ~375 Ko) traité en moins de 60 s ; profiler si dépassé
- [x] T031 Revue finale de conformité constitution : zéro dépendance runtime ajoutée, zéro appel réseau, échec rapide validé, suppression de `output/` = suppression totale des résultats (Data Retention)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: aucune dépendance — démarrage immédiat
- **Foundational (Phase 2)**: dépend de la Phase 1 — BLOQUE toutes les user stories
- **User Stories (Phases 3–6)**: toutes dépendent de la Phase 2 ; ensuite parallélisables entre elles, ou séquentielles par priorité (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: dépend de l'ensemble des stories visées

### User Story Dependencies

- **User Story 1 (P1)**: démarre après la Phase 2 — aucune dépendance envers les autres stories
- **User Story 2 (P2)**: démarre après la Phase 2 — consomme la détection de US1 mais reste testable indépendamment (le chemin suggestion par défaut de US1 fonctionne sans elle)
- **User Story 3 (P3)**: démarre après la Phase 2 — s'appuie sur les blocs de US1, testable indépendamment
- **User Story 4 (P4)**: démarre après la Phase 2 — enrichit `detection.py` (US1), testable indépendamment

### Within Each User Story

- Tests écrits d'abord et ÉCHOUANT avant implémentation
- Modules purs (détection, normalisation) avant le câblage CLI
- Câblage CLI en dernier (T012, T018, T023)
- Story complète avant de passer à la priorité suivante

### Parallel Opportunities

- Toutes les tâches [P] de la Phase 2 en parallèle
- Une fois la Phase 2 terminée : US1 et US2 et US3 et US4 peuvent démarrer en parallèle (fichiers majoritairement distincts ; coordination sur `md_cleaner/cli.py` et `detection.py` entre US1 et US4)
- T007/T008 puis T013/T014 en parallèle au sein de US1 ; T016 et T020 en parallèle entre stories

---

## Parallel Example: User Story 1

```bash
# Lancer les tests de US1 ensemble :
Task: "Tests unitaires de normalisation dans tests/unit/test_normalisation.py"      # T007
Task: "Tests unitaires de segmentation dans tests/unit/test_segmentation.py"        # T008

# Puis les modules de US1 ensemble (fichiers différents) :
Task: "Dossier de sortie dans md_cleaner/sortie.py"                                # T010
# (T009 detection.py est séquentiel : dépend de T004 normalisation)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Compléter Phase 1: Setup
2. Compléter Phase 2: Foundational (CRITIQUE — bloque tout)
3. Compléter Phase 3: User Story 1
4. **STOP et VALIDER**: `md-cleaner Examples/Exemple_1/2.Input/consolidated.md` + `pytest`
5. Le MVP nettoie déjà un fichier de bout en bout

### Incremental Delivery

1. Setup + Foundational → socle prêt
2. User Story 1 → test indépendant → MVP
3. User Story 2 → validation humaine possible
4. User Story 3 → contenu localisable (RAG-ready)
5. User Story 4 → détection calibrée plus précise

### Parallel Team Strategy

Avec plusieurs développeurs :

1. L'équipe complète Setup + Foundational ensemble
2. Puis : Développeur A → US1, Développeur B → US2, Développeur C → US3, Développeur D → US4
3. Les stories s'intègrent indépendamment (câblage CLI au point de convergence)

---

## Notes

- [P] = fichiers différents, pas de dépendances
- Le label [Story] rattache chaque tâche à sa user story pour la traçabilité
- Chaque story est complétable et testable indépendamment
- Vérifier que les tests échouent avant d'implémenter
- Committer après chaque tâche ou groupe logique (workflow pre-commit du dépôt)
- S'arrêter à tout checkpoint pour valider une story indépendamment
- À éviter : tâches vagues, conflits sur un même fichier, dépendances inter-stories qui cassent l'indépendance
