# Data Model : Extraits lisibles et localisables

**Feature**: 003-extrait-lisible | **Date**: 2026-09-29 | **Source**: [spec.md](./spec.md), data-model des features 001/002, [research.md](./research.md) D1-D7

La feature ne crée aucune entité : elle enrichit deux champs d'une entité existante (l'un étendu, l'autre nouveau) et ajoute une option CLI. Les conventions ci-dessous complètent le data-model de la feature 001.

## MotifRepetitif (suggestion.json — enrichi)

| Champ | Avant (features 001/002) | Après (feature 003) |
| ----- | ------------------------ | -------------------- |
| `extrait` | ≤ 3 lignes de l'intervalle le plus long (global), jointes par « ` / ` » | N premières lignes du **premier intervalle de la page de première occurrence** (N = 5 par défaut, option `--extrait` 2-25), rendu en **vrais sauts de ligne** ; si l'intervalle est plus court que N, tout ce qui existe, sans complément |
| `position` | (absent) | Nouveau : `{"page": P, "debut": D, "fin": F}` — première occurrence du motif, `fin` **inclue**, lignes D à F de la page P |
| autres (`id`, `action`, `nb_lignes`, `frequence`, `pages`) | inchangés | inchangés |

**Ancrage commun** : l'extrait et la position désignent le même endroit — la page de première occurrence (la plus ancienne), premier intervalle. Ce que l'utilisateur lit dans l'extrait est exactement là où la position l'envoie (FR-001/FR-002, D1).

**Validation (relecture, D4)** :

- `position` absent → accepté (suggestions d'avant-feature)
- `position` présent → objet avec `page` entier ≥ 1, `debut` entier ≥ 0, `fin` entier > `debut` (inclue) ; toute malformation → `ErreurSuggestion`, code retour 2, message clair
- cohérence non vérifiée avec le document à la relecture (les actions ne dépendent que des ids) — la cohérence est garantie à la génération et testée en intégration (SC-003)

## Option CLI : --extrait N

| Attribut | Valeur |
| -------- | ------ |
| Type | entier, bornes 2 à 25 |
| Défaut | 5 (dose de saturation mesurée, assessment `lisibilite-dry-run`) |
| Portée | génération de `suggestion.json` uniquement |
| Hors dry-run | acceptée, sans effet observable (clarification du 2026-09-29, Option A), documentée dans l'aide |
| Hors bornes | usage invalide, code retour 3 |
| Incidence détection/nettoyage | aucune (FR-009) |

## Rapport dry-run (présentation — garde-fou uniquement)

Le rapport reste structuré comme la feature 002 l'a défini (deux sections, troncature 120 caractères) avec un unique garde-fou : les sauts de ligne des extraits sont neutralisés en « ` / ` » dans les cellules du tableau, pour ne pas casser les rangées markdown (D5).

## BlocContenu, Page, Cartographie, RunSortie (inchangés)

Formats et conventions inchangés ; en particulier `cartographie.json` conserve sa convention `debut`/`fin` (fin inclue) — que la position de la suggestion reprend pour homogénéité des artefacts utilisateur (D3).

## Règles transverses

- **Déterminisme** : l'enrichissement est une fonction pure de (pages, motifs, N) — ordres de traitement fixes, aucune horloge ni aléa ; deux exécutions identiques → suggestion identique octet par octet (SC-005).
- **Garde de taille** : `suggestion.json` < 1 Mo sur le corpus d'exemples pour toute valeur de N dans les bornes (SC-004) — garde de la constitution contre la dérive vers un duplicatat du document ; l'extrait reste un aperçu, la source reste la référence.
- **Invariance** : consommer une suggestion dont les extraits diffèrent (longueur, contenu) produit le même `nettoye.md` (FR-009) — seuls `id` et `action` pilotent le nettoyage, comme depuis la feature 001.
