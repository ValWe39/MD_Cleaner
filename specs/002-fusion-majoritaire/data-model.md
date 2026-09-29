# Data Model : Décidabilité des motifs (fusion majoritaire)

**Feature**: 002-fusion-majoritaire | **Date**: 2026-09-29 | **Source**: [spec.md](./spec.md), data-model de la feature 001 (`specs/001-nettoyage-md-repetitif/data-model.md`)

La feature ne crée aucune entité nouvelle : elle modifie une règle de construction d'une entité existante et la présentation d'un artefact. Les entités ci-dessous reprennent celles de la feature 001 en indiquant l'impact.

## MotifRepetitif (impacté — règle de fusion)

Champs inchangés : `id` (`M01`+), `action` (`supprimer | conserver`), `lignes_norm`, `extrait`, `frequence` [0, 1], `pages` (triées), `nb_lignes`, `emplacements` (intervalles disjoints par page).

**Changement** : la règle qui regroupe les fenêtres récurrentes en un même motif passe de « chevauchement sur au moins une page » à « chevauchement sur strictement plus de la moitié des pages de la fenêtre candidate » (FR-001, D1 de research.md).

| Règle | Avant (feature 001) | Après (feature 002) |
| ----- | -------------------- | --------------------- |
| Fusion candidate → bloc | chevauchement sur ≥ 1 page | chevauchement sur > 50 % des pages de la candidate (strict ; à la moitié exacte : refus) |
| Candidate sans bloc majoritaire | fusion quand même dans le premier bloc touché | nouveau bloc distinct |

**Identité et unicité** : ids attribués par (position de première occurrence, fréquence décroissante) — inchangé au sein d'une version ; **les ids ne sont pas stables entre versions de l'outil** (documenté, FR-007).

**Validation** : `frequence` arrondie à 2 décimales ; `pages` sans trou ; `emplacements` intervalles disjoints triés — inchangé.

## Suggestion (fichier suggestion.json — inchangé)

Schéma, validation stricte à la lecture, sérialisation déterministe : inchangés. Le fichier continue de contenir **tous** les motifs (supprimer et conserver), chacun actionnable — c'est le support de la décidabilité.

## Rapport dry-run (présentation modifiée — indicatif)

Le rapport passe de deux sections (tableau de tous les motifs + motifs sous le seuil) à :

| Section | Contenu | Action attendue de l'utilisateur |
| ------- | ------- | ------------------------------- |
| Décisions requises | Tableau des motifs `action = supprimer` uniquement | arbitrer chaque ligne |
| Motifs conservés par défaut | Liste des motifs `action = conserver`, sans action requise | aucune (édition possible via suggestion.json) |

Le rapport rappelle la commande d'édition de la suggestion. Structure détaillée dans [contracts/rapport-dry-run.md](./contracts/rapport-dry-run.md).

## BlocContenu, Page, Cartographie, RunSortie (inchangés)

Format des emplacements consommé par le nettoyage, sorties `nettoye.md` / `nettoye-pagine.md` / `cartographie.json`, numérotation des runs : aucun changement — la feature est interne à la construction des motifs et à la présentation du rapport.

## Relations (inchangées)

```text
DocumentSource 1──n Page 1──n BlocContenu
DocumentSource 1──n MotifRepetitif (règle de regroupement modifiée — périmètre de la feature)
Suggestion n──n MotifRepetitif (par id + action, inchangé)
RunSortie 1──1 DocumentSource
Cartographie 1──n BlocContenu
```

## Règles transverses (inchangées, re- vérifiées)

- **Déterminisme** : ids stables au sein d'une version, clés JSON triées, itérations ordonnées — la nouvelle règle est une comparaison entière (`2 * pages_chevauchantes > pages_totales_candidate`), sans flottant ni aléa.
- **Cohérence cartographie / sortie paginée** : non impactée (le nettoyage consomme les emplacements ; leur format ne change pas).
- **Transitions du run** : identiques à la feature 001 ; seul le contenu du rapport dry-run change d'aspect.
