# Contrat : nommage du fichier nettoyé d'après le document source

**Feature**: 006-nom-sortie-source | **Date**: 2026-10-05 | **Révise**: `specs/001-nettoyage-md-repetitif/contracts/cli.md` (table des artefacts)

## Règle de nommage

Le fichier nettoyé d'un run (nettoyage simple, sans `--dry-run`) est nommé :

```text
<base>-nettoye.md
```

où `base` est construite depuis le nom de fichier du document d'entrée **sans extension** :

1. Remplacer chaque blanc (espace, tabulation) par exactement un `_` (ni compression, ni décapage).
2. Tronquer au 20ᵉ caractère (points de code Unicode ; pas d'ajustement à la frontière de mot).
3. Tout autre caractère (accents, tirets, chiffres, ponctuation) est conservé tel quel.

En cas de conflit (nom déjà présent à l'emplacement d'écriture) : suffixe numérique à la fin du nom, avant l'extension — `<base>-nettoye-1.md`, puis `-2`, `-3`, ... par ordre de traitement. Jamais d'écrasement.

## Exemples

| Entrée | Sortie |
| ------ | ------ |
| `retry-failed-records.md` | `retry-failed-records-nettoye.md` |
| `rapport annuel.md` | `rapport_annuel-nettoye.md` |
| `comptes-rendus-conseil-municipal-session-octobre.md` | `comptes-rendus-conse-nettoye.md` |
| `éco développement.md` | `éco_développement-nettoye.md` |
| `retry-failed-records.md` (nom déjà pris) | `retry-failed-records-nettoye-1.md` |

## Interface CLI

Aucun nouveau drapeau, aucune modification des options existantes : le nommage s'applique par défaut. Le message de fin affiche le chemin réel du fichier (`Sortie : ...`).

## Artefacts inchangés (hors périmètre)

`nettoye-pagine.md`, `cartographie.json`, `suggestion.json`, `rapport-dry-run.md`, nommage des dossiers de run (numérotation séquentielle, `--nom-titre`). Le mode `--dry-run` n'écrit pas de fichier nettoyé : inchangé.
