# Research : Extraits lisibles et localisables dans la suggestion

**Feature**: 003-extrait-lisible | **Date**: 2026-09-29 | **Sources**: [spec.md](./spec.md) (clarifiée), assessment `lisibilite-dry-run` (5 artefacts, mesures), design des features 001/002 (research.md, contracts/), code existant (`md_cleaner/suggestion.py`, `detection.py`).

## D1. Enrichissement post-detection, sans toucher à detection.py

- **Décision** : l'extrait à N lignes et le champ position sont calculés par une fonction d'enrichissement dans `md_cleaner/suggestion.py` — `enrichir_motifs(pages, motifs, n)` — qui reçoit les motifs détectés (portant leurs `emplacements`) et les pages, et remplace le champ `extrait` de chaque motif par les N premières lignes de son premier intervalle sur sa page de première occurrence, en ajoutant le champ `position` (même ancrage). `detection.py` n'est pas modifié : son extrait interne de 3 lignes devient une valeur intermédiaire écrasée par l'enrichissement.
- **Rationale** : la détection est un calcul de motifs (FR-009 : la longueur d'extrait n'a aucune incidence dessus) ; l'extrait et la position sont des métadonnées de présentation de la suggestion — les placer derrière la frontière `suggestion.py` respecte la séparation et garde le périmètre de code minimal. L'ancrage sur la **première occurrence** (page la plus ancienne, premier intervalle) aligne ce que l'utilisateur lit (extrait) et là où la position l'envoie — cohérence voulue par la spec (FR-001/FR-002), au prix d'un écart documenté avec le comportement 001 (extrait pris sur l'intervalle le plus long global, potentiellement d'une autre page).
- **Alternatives** : passer N à `detecter()` (rejeté : pollue la détection avec un souci de présentation) ; garder l'ancrage sur l'intervalle le plus long (rejeté : extrait et position peuvent pointer des pages différentes — incohérent pour juger puis localiser).

## D2. Option CLI `--extrait N`

- **Décision** : option `--extrait N` ajoutée à `construire_analyseur()` dans `md_cleaner/cli.py` via le validateur `_entier_bornes` existant (bornes 2-25, défaut 5) ; l'aide documente que l'option s'applique à la génération de `suggestion.json` uniquement et est sans effet observable hors `--dry-run` (clarification du 2026-09-29, Option A). L'implémentation passe N à `construire_suggestion`/l'enrichissement dans tous les modes (l'effet n'est visible que lorsque la suggestion est écrite, c'est-à-dire en dry-run).
- **Rationale** : bornes fixes = validation au parsing (code 3) sans nouvelle logique ; le comportement sans effet hors dry-run est le moins surprenant pour le flux en deux temps (`--dry-run --extrait 12` puis `--suggestion`).
- **Alternatives** : refuser hors dry-run (rejeté par la clarification) ; écrire une suggestion à chaque nettoyage (rejeté : changement de contrat de sortie de la feature 001).

## D3. Convention des bornes du champ position : `fin` inclue

- **Décision** : `position = {"page": P, "debut": D, "fin": F}` avec `F` **inclue** (l'intervalle couvre les lignes D à F de la page P), cohérente avec la convention de `cartographie.json` (`data-model` de la feature 001 : « debut/fin indices de lignes dans la page d'origine, fin incluse »), l'autre convention interne (emplacements de détection, demi-intervalles ouverts) n'apparaissant dans aucun artefact visible par l'utilisateur.
- **Rationale** : deux conventions coexistent en interne (emplacements de détection : ouverts ; cartographie : fermés) ; les artefacts JSON visibles par l'utilisateur doivent partager une seule — celle déjà publiée par cartographie. La conversion est triviale (F = fin_interne - 1).
- **Alternatives** : demi-intervalle ouvert `[D, F[` (rejeté : divergerait de cartographie.json, le seul précédent utilisateur-visible).

## D4. Validation stricte du champ position à la relecture

- **Décision** : `lire_suggestion` accepte l'absence du champ position (suggestions d'avant-feature) ; si présent, il doit être un objet `{"page": entier ≥ 1, "debut": entier ≥ 0, "fin": entier > debut}` — toute autre forme (texte, bornes violées, clés manquantes) lève `ErreurSuggestion` (code 2, message clair), conformément au style de validation stricte existant.
- **Rationale** : FR-005 ; la validation existante de `lire_suggestion` ignore les champs inconnus — le champ position nouveau est donc toléré par les anciennes suggestions dans le sens inverse aussi (une suggestion 003 relue par... non applicable : un seul lecteur, la version courante). La tolérance d'absence garantit que les suggestions éditées à la main depuis des dry-runs antérieurs restent consommables.
- **Alternatives** : exiger le champ (rejeté : casserait la continuité promise par FR-005) ; validation croisée avec le document (rejeté : la relecture n'a pas accès aux pages, et les actions ne dépendent que des ids).

## D5. Garde-fou du rapport : neutralisation des sauts

- **Décision** : `generer_rapport` remplace les sauts de ligne de l'extrait par le séparateur historique « ` / ` » dans ses cellules de tableau (après échappement des pipes, avant la troncature à 120 caractères) ; la structure en deux sections (feature 002) et la troncature restent inchangées.
- **Rationale** : un `\n` dans une cellule de tableau markdown termine la rangée — le rapport serait cassé ; réutiliser « ` / ` » comme séparateur visuel maintient l'aspect historique de l'aperçu sans inventer de marqueur.
- **Alternatives** : marquage « ⏎ » (rejeté : personnage exotique dans un tableau déjà serré) ; refonte de présentation du rapport (refusée par le cadrage : le rapport est un aperçu, pas la surface de jugement).

## D6. Stratégie de tests

- **Décision** :
  - Unitaires : `enrichir_motifs` — N lignes exactes quand l'intervalle le permet, rendu tel quel sinon (jamais de complément), position = première occurrence avec `fin` inclue ; `lire_suggestion` — position absente acceptée, mal formée rejetée (code 2) ; `generer_rapport` — aucune cellule ne contient de saut de ligne, troncature 120 inchangée.
  - Intégration (nouveau `tests/integration/test_extrait.py`) : sur Exemple_2 — ≤ 2 extraits en doublon à la valeur par défaut (SC-001, baseline 12), `--extrait 12` donne exactement 12 lignes aux motifs à intervalle suffisant (SC-002), chaque `position.debut` de la page `position.page` est couvert par une occurrence réelle du motif (SC-003), taille < 1 Mo pour N aux bornes (SC-004), déterminisme (SC-005) ; CLI — `--extrait 1` et `--extrait 40` → code 3, `--extrait` sans `--dry-run` → code 0 sans effet.
  - Régression : suite existante (features 001/002) au vert sans relâchement (SC-006).
- **Rationale** : chaque SC de la spec a son test mécanique ; les deux seuls nouveaux comportements unitaires sont l'enrichissement et la neutralisation.
- **Alternatives** : snapshot complet de la suggestion d'Exemple_2 (rejeté : fragile au premier changement du corpus).

## D7. Révision du contrat de la feature 001

- **Décision** : à l'implémentation, la clause `motifs[].extrait` de `specs/001-nettoyage-md-repetitif/contracts/formats.md` (« ≤ 3 lignes jointes par " / " ») est révisée pour refléter la nouvelle définition (N lignes, vrais sauts de ligne, ancrage première occurrence) et le champ `position` est ajouté au schéma ; la révision est citée dans le commit d'implémentation (FR-007). Le contrat de la feature 002 (`rapport-dry-run.md`) reste inchangé.
- **Rationale** : les contrats décrivent le comportement courant — une spec de feature révisant un contrat publié doit le faire en même temps que le code, pas par un commit fantôme.
- **Alternatives** : contrat dupliqué dans specs/003 (rejeté : deux sources de vérité divergentes) ; révision différée (rejetée : le code et la doc décriraient des comportements différents).
