# Quickstart: valider le nommage de sortie dérivé de la source

**Feature**: 006-nom-sortie-source | **Date**: 2026-10-05 | **Contrat**: [contracts/nommage-sortie.md](./contracts/nommage-sortie.md)

## Prérequis

- Environnement Python du projet (dépendances installées) ; `pytest` disponible.
- Un document Markdown de travail, par exemple `Examples/Exemple_1/2.Input/*.md` (tout fichier .md court convient).

## Scénario 1 — Nom dérivé de l'entrée (US1)

```bash
cp Examples/Exemple_1/2.Input/*.md /tmp/retry-failed-records.md   # adapter au nom réel
python -m md_cleaner /tmp/retry-failed-records.md --sortie /tmp/qs-006
```

**Attendu** : message `Sortie : /tmp/qs-006/001/retry-failed-records-nettoye.md` ; le fichier porte ce nom exact, aucun `nettoye.md` n'est présent.

## Scénario 2 — Espaces remplacées (US1)

```bash
cp /tmp/retry-failed-records.md "/tmp/rapport annuel.md"
python -m md_cleaner "/tmp/rapport annuel.md" --sortie /tmp/qs-006
```

**Attendu** : sortie `rapport_annuel-nettoye.md`.

## Scénario 3 — Troncature à 20 caractères (US2)

```bash
cp /tmp/retry-failed-records.md /tmp/comptes-rendus-conseil-municipal-session-octobre.md
python -m md_cleaner /tmp/comptes-rendus-conseil-municipal-session-octobre.md --sortie /tmp/qs-006
```

**Attendu** : sortie `comptes-rendus-conse-nettoye.md` (base de 20 caractères exactement).

## Scénario 4 — Artefacts secondaires et dry-run inchangés (FR-005)

```bash
python -m md_cleaner /tmp/retry-failed-records.md --sortie /tmp/qs-006 --pagine
python -m md_cleaner /tmp/retry-failed-records.md --sortie /tmp/qs-006 --dry-run
```

**Attendu** : `nettoye-pagine.md`, `cartographie.json` (noms inchangés) aux côtés de `retry-failed-records-nettoye.md` ; le dry-run produit uniquement `suggestion.json` et `rapport-dry-run.md`, aucun fichier nettoyé.

## Scénario 5 — Collision sans écrasement (US3, FR-004)

Scénario rare avec les dossiers de run séparés — validé par la suite automatisée :

```bash
pytest tests/unit/test_normalisation.py tests/unit/test_sortie.py -k "nom or collision" -q
pytest tests/integration -q
```

**Attendu** : tous les tests passent, dont les cas `<base>-nettoye-1.md`, `-2` sans écrasement.

## Remise à zéro

Supprimer `/tmp/qs-006` et les copies temporaires (l'outil ne conserve aucune copie cachée).
