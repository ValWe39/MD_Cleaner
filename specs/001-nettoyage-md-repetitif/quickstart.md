# Quickstart : validation de md-cleaner

**Feature**: 001-nettoyage-md-repetitif | **Date**: 2026-09-29 | **Source**: [spec.md](./spec.md), [contracts/cli.md](./contracts/cli.md), [contracts/formats.md](./contracts/formats.md)

Guide de validation de bout en bout : chaque scénario est exécutable mécaniquement et prouve une exigence. Les détails des formats sont dans [contracts/](./contracts/), le comportement des commandes dans [contracts/cli.md](./contracts/cli.md).

## Prérequis

- Python 3.12 disponible (`python --version`).
- Dépôt cloné ; dépendances de développement installées : `pip install -e . && pip install pytest`.
- Aucun accès réseau requis à aucun moment.

## Scénario 0 — Tests automatisés

```bash
pytest
```

Attendu : tests unitaires (normalisation, segmentation, détection, seuil, ids) et intégration (fixtures `Examples/`) tous au vert. Couvre notamment le déterminisme (SC-002) : deux exécutions successives sur la même entrée produisent des sorties identiques octet par octet.

## Scénario 1 — Nettoyage simple (FR-004, SC-001, SC-005)

```bash
md-cleaner Examples/Exemple_1/2.Input/consolidated.md
```

Attendu :

- Code retour 0 ; sous-dossier numéroté créé dans `output/` (ex. `output/001/`).
- `output/001/nettoye.md` ne contient plus le menu de navigation ni le pied de page CORSEN AI répétés sur les 14 pages.
- Toute ligne unique du document d'entrée figure dans la sortie (diff : contenu conservé à 100 %).

## Scénario 2 — Dry-run et suggestion éditable (FR-007, FR-008, SC-004)

```bash
md-cleaner Examples/Exemple_1/2.Input/consolidated.md --dry-run
```

Attendu :

- Aucun `nettoye.md` écrit.
- `output/00N/rapport-dry-run.md` liste les motifs (extraits, fréquences, pages) et les motifs sous le seuil ; lisible en moins de 5 minutes.
- `output/00N/suggestion.json` conforme au contrat : ids `M01…`, `action` supprimer/conserver, source et seuil cohérents.

Validation de la boucle humaine : basculer un motif `supprimer` → `conserver`, puis :

```bash
md-cleaner Examples/Exemple_1/2.Input/consolidated.md --suggestion output/00N/suggestion.json
```

Attendu : le motif correspondant est conservé dans `nettoye.md`. Inversement, un id inconnu ajouté à la main → code retour 2 et message clair.

## Scénario 3 — Sortie paginée et cartographie (FR-009, FR-010, SC-006)

```bash
md-cleaner Examples/Exemple_1/2.Input/consolidated.md --pagine
```

Attendu :

- `nettoye-pagine.md` contient un marqueur lisible par page d'origine (`---` + `<!-- page: N -->`).
- `cartographie.json` conforme : chaque bloc `P{n}-B{k}` est associé à sa page et à l'URL source ; l'ensemble des ids du JSON couvre exactement les marqueurs du `.md` paginé.
- Le fichier `.md` nettoyé simple (Scénario 1) ne contient aucun marqueur ni séparateur de pages (clarification Q2 → A).

## Scénario 4 — Document sans séparateurs explicites (FR-011)

Construire une entrée sans `## Page N:` (par exemple en retirant les séparateurs d'un exemple), puis :

```bash
md-cleaner entree-sans-pages.md --pagine
```

Attendu : soit une pagination recréée par heuristique, signalée dans `cartographie.json` (`mode_pagination: "heuristique"`) et sur stderr, soit un signalement explicite qu'aucune frontière fiable n'a été trouvée (document traité comme section unique) — jamais une pagination silencieuse et trompeuse.

## Scénario 5 — Calibrage sur échantillon fourni (FR-012, FR-013)

```bash
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --echantillon Examples/Exemple_2/1.Sample
md-cleaner Examples/Exemple_2/2.Input/consolidated.md
```

Attendu : les deux runs détectent les filtres et la pagination d'interface de l'Exemple_2 ; le calibrage sur l'échantillon des 5 premières pages produit au moins les mêmes motifs que l'auto-calibrage (comparaison des `suggestion.json`). Un dossier vide ou 6 fichiers → code retour 2.

## Scénario 6 — Seuil réglable et cas limites (FR-002, FR-016)

```bash
md-cleaner Examples/Exemple_1/2.Input/consolidated.md --seuil 95 --dry-run
md-cleaner Examples/Exemple_1/1.Sample/1.md
```

Attendu : au seuil 95, des motifs présents sur moins de 95 % des pages passent en « motifs sous le seuil » du rapport. Le fichier à page unique produit un avertissement explicite (pas assez de répétition observable) et une sortie inchangée plutôt qu'un nettoyage arbitraire.

## Scénario 7 — Déterminisme (FR-005, SC-002)

```bash
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --pagine
cp -r output/<run> /tmp/run1
md-cleaner Examples/Exemple_2/2.Input/consolidated.md --pagine
diff -r /tmp/run1 output/<run>
```

Attendu : `diff` ne rapporte aucune différence, octet par octet, y compris les noms de sous-dossiers (pas d'horodatage).

## Scénario 8 — Défauts d'entrée (FR-015)

```bash
md-cleaner fichier-inexistant.md          # code 1, message clair
md-cleaner fichier.txt                    # code 1
md-cleaner consolidated.md --seuil 150    # code 3
```

Attendu : échec rapide avec messages en français, aucun fichier écrit dans `output/`.

## Critères de succès couverts

| Scénario | Critère |
| -------- | ------- |
| 0, 7 | SC-002 (déterminisme) |
| 1 | SC-001 (≥ 90 % du boilerplate supprimé, 100 % du contenu conservé), SC-005 |
| 2 | SC-004 (dry-run validé en < 5 min) |
| 3 | SC-006 (localisation sans ambiguïté) |
| 4 | FR-011 (heuristique signalée) |
| 5 | FR-012, FR-013 |
| 6 | FR-002 (seuil), FR-016 |
| 8 | FR-015 |
