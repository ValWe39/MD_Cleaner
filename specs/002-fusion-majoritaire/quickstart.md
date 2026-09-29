# Quickstart : validation de la fusion majoritaire

**Feature**: 002-fusion-majoritaire | **Date**: 2026-09-29 | **Source**: [spec.md](./spec.md), [contracts/rapport-dry-run.md](./contracts/rapport-dry-run.md)

Guide de validation de bout en bout : chaque scénario est exécutable mécaniquement et prouve un critère de la spec. Prérequis : environnement de la feature 001 installé (`pip install -e .`, `pytest`), aucun réseau requis.

## Scénario 0 — Tests automatisés

```bash
pytest
```

Attendu : suite complète au vert, y compris les nouveaux tests de la feature (frontière majoritaire, séparation, non-régression). Couvre SC-004 (aucune régression), SC-005 (déterminisme) et la frontière stricte (FR-001).

## Scénario 1 — Non-régression sur un document compact (SC-002)

```bash
md-cleaner Examples/Exemple_1/2.Input/consolidated.md --dry-run
```

Attendu : le rapport comporte 4 motifs `supprimer`, aucun motif conserver supplémentaire par rapport à la version précédente ; les zones couvertes et les actions sont identiques à la version précédente (aucune section secondaire superflue — US2, scénario 3).

## Scénario 2 — Séparation interface / métadonnées (SC-001, US1)

```bash
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --dry-run
```

Attendu :

- la zone de filtres/pagination et les métadonnées de publications appartiennent à des **motifs distincts** ;
- le tableau « Décisions requises » énumère **au plus 5** motifs `supprimer` (SC-003) ;
- les motifs conservés par défaut sont regroupés dans la section secondaire « aucune action requise » (FR-004) ;
- la lecture du rapport identifie les décisions requises en moins de 5 minutes (SC-006).

## Scénario 3 — La décision ciblée devient exprimable (US1, scénario 2)

```bash
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --dry-run
# éditer suggestion.json : motif des filtres = "supprimer",
# motifs des métadonnées (institution, dates, thèmes) = "conserver"
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --suggestion output/<run>/suggestion.json
```

Attendu : le `nettoye.md` résultat **ne contient plus** les filtres/pagination **mais conserve** les métadonnées des publications (marqueur d'institution, dates, liens de thème) — la décision impossible avant la feature est obtenue en n'éditionnant que les actions.

## Scénario 4 — Suggestion d'une version antérieure (US3, FR-008)

```bash
# si disponible : une suggestion.json générée avant la mise à jour
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --suggestion <ancienne_suggestion.json>
```

Attendu : échec rapide, code retour 2, message sur les ids inconnus — aucune correspondance approximative tentée. Le README mentionne la régénération par dry-run (FR-007).

## Scénario 5 — Déterminisme (SC-005)

```bash
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --dry-run --sortie /tmp/run1
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --dry-run --sortie /tmp/run2
diff -r /tmp/run1 /tmp/run2
```

Attendu : aucune différence, octet par octet, y compris les ids de motifs.

## Critères couverts

| Scénario | Critère |
| -------- | ------- |
| 0 | SC-004, SC-005, FR-001 (frontière stricte) |
| 1 | SC-002, US2 scénario 3 |
| 2 | SC-001, SC-003, SC-006, FR-004 |
| 3 | US1 scénario 2 (la décision ciblée) |
| 4 | US3, FR-007, FR-008 |
| 5 | SC-005 |
