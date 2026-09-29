# Quickstart : validation des extraits lisibles et localisables

**Feature**: 003-extrait-lisible | **Date**: 2026-09-29 | **Source**: [spec.md](./spec.md), [contracts/suggestion-extrait.md](./contracts/suggestion-extrait.md)

Guide de validation de bout en bout : chaque scénario est exécutable mécaniquement et prouve un critère de la spec. Prérequis : environnement des features 001/002 installé (`pip install -e .`, `pytest`), aucun réseau requis.

## Scénario 0 — Tests automatisés

```bash
pytest
```

Attendu : suite complète au vert, y compris les nouveaux tests de la feature (enrichissement, validation position, neutralisation rapport, intégration Exemple_2). Couvre SC-001 à SC-006.

## Scénario 1 — Juger depuis le JSON seul (US1, SC-001, SC-003)

```bash
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --dry-run
```

Attendu :

- dans `output/<run>/suggestion.json`, chaque extrait s'affiche ligne par ligne dans un lecteur de JSON, avec les éléments distinctifs visibles (liens de thème, dates) — au plus 2 motifs partagent le même extrait ;
- chaque motif porte un `position` dont la ligne `debut` de la page `page` correspond à une occurrence réelle dans le document ;
- l'expérience de jugement se fait sans ouvrir le document source (validation qualitative : à vérifier de votre main).

## Scénario 2 — Régler la dose (US2, SC-002)

```bash
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --dry-run --extrait 12
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --dry-run --extrait 2
```

Attendu : les extraits comptent exactement 12 (ou 2) lignes pour les motifs dont l'intervalle le permet ; les motifs plus courts rendent tout ce qui existe, sans complément.

## Scénario 3 — Bornes de l'option (US2, scénario 2)

```bash
md-cleaner Examples/Exemple_1/2.Input/consolidated.md --dry-run --extrait 1
md-cleaner Examples/Exemple_1/2.Input/consolidated.md --dry-run --extrait 40
md-cleaner Examples/Exemple_1/2.Input/consolidated.md --extrait 12
```

Attendu : code retour 3 avec message des bornes pour 1 et 40 ; code retour 0 pour la dernière commande, sans effet observable (pas de suggestion générée hors dry-run) — comportement documenté dans `--help`.

## Scénario 4 — Le rapport reste intact (US3, SC-006)

```bash
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --dry-run
```

Attendu : le rapport conserve ses deux sections et sa troncature à 120 caractères ; aucune cellule de tableau ne contient de saut de ligne (tableau bien formé) — l'aperçu est intact malgré les `\n` dans le JSON.

## Scénario 5 — Suggestions anciennes et champ position (US3, FR-005)

```bash
# une suggestion générée avant la feature (sans champ position) reste consommable :
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --suggestion <ancienne_suggestion.json>
# un champ position mal formé (ex. "page": "un") est refusé :
# code retour 2, message clair
```

Attendu : code 0 pour la suggestion ancienne (absence de position tolérée) ; code 2 pour une position mal formée.

## Scénario 6 — Déterminisme et garde de taille (SC-004, SC-005)

```bash
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --dry-run --extrait 25 --sortie /tmp/run1
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --dry-run --extrait 25 --sortie /tmp/run2
diff /tmp/run1/<run>/suggestion.json /tmp/run2/<run>/suggestion.json
du -h /tmp/run1/<run>/suggestion.json
```

Attendu : aucune différence octet par octet ; taille < 1 Mo même à N = 25 sur le document riche.

## Scénario 7 — Invariance du nettoyage (FR-009)

```bash
md-cleaner Examples/Exemple_1/2.Input/consolidated.md
md-cleaner Examples/Exemple_1/2.Input/consolidated.md --extrait 2
```

Attendu : les deux `nettoye.md` sont identiques octet par octet — la longueur d'extrait n'a aucune incidence sur le nettoyage.

## Critères couverts

| Scénario | Critère |
| -------- | ------- |
| 0 | SC-001 à SC-006 |
| 1 | US1, SC-001, SC-003 |
| 2 | US2, SC-002 |
| 3 | US2 scénario 2, FR-003 |
| 4 | US3 scénario 1, SC-006 |
| 5 | US3 scénario 2, FR-005 |
| 6 | SC-004, SC-005 |
| 7 | FR-009 |
