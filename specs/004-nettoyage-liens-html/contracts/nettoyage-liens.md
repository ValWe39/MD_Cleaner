# Contrat : nettoyage des destinations de liens à l'écriture

**Feature**: 004-nettoyage-liens-html | **Date**: 2026-10-02 | **Source**: [spec.md](./spec.md), [research.md](./research.md) (D1, D4, D5), révision du contrat CLI [001/contracts/cli.md](../../001-nettoyage-md-repetitif/contracts/cli.md)

## Règle de transformation (FR-001, FR-006)

Appliquée à l'écriture de `nettoye.md` et `nettoye-pagine.md`, sur chaque ligne conservée :

```text
cible   : la sous-chaîne ](</...>)  — ](< + destination sans > + >)
retrait : la sous-chaîne complète, parenthèses et chevrons compris
restes  : tout le reste de la ligne, identique octet par octet
```

Exemple contractuel :

```text
entrée : [Famille, handicap, sport et jeunesse](</publications?f%5B1%5D=thematic%3A17182>) -
sortie : [Famille, handicap, sport et jeunesse] -
```

Bornes de la règle :

| Forme | Traitement |
| ----- | ---------- |
| `](</...>)` (chevrons, premier `>` referme) | retirée, telle quelle, sans décodage |
| plusieurs occurrences sur une même ligne | toutes retirées |
| `[](</...>)` (libellé vide) | destination retirée, crochets vides conservés |
| `](https://...)`, `](chemin)` | hors périmètre : inchangées |
| vraies balises HTML (`<div>`, `<!-- page: N -->`) | hors périmètre : inchangées |

## Option CLI (révision du contrat de la feature 001)

| Option | Argument | Défaut | Exigence | Description |
| ------ | -------- | ------ | -------- | ----------- |
| `--conserver-liens` | — | nettoyage actif | FR-002, FR-003 | Désactive le retrait des destinations : `nettoye.md` et `nettoye-pagine.md` conservent les liens inline tels quels, identiques octet par octet à une sortie produite sans la feature |

- Booléenne sans argument, même pattern que `--pagine` ; compatible avec toutes les autres options (`--pagine`, `--suggestion`, `--seuil`, …).
- Sans le drapeau : la passe est active à chaque run de nettoyage (y compris avec `--suggestion`).
- `--dry-run` : aucun effet observable (aucune sortie nettoyée n'est écrite ; la suggestion et le rapport restent identiques, FR-005).

## Sorties concernées et non concernées (FR-004, FR-005)

| Artefact | Nettoyé ? |
| -------- | --------- |
| `nettoye.md` | oui |
| `nettoye-pagine.md` | oui (contenu des pages ; marqueurs `<!-- page: N -->` générés intacts) |
| `suggestion.json` (extraits) | non |
| `rapport-dry-run.md` (extraits) | non |
| `cartographie.json` | non (n'utilise jamais le texte des blocs) |

## Codes retour et messages

Inchangés (contrat CLI de la feature 001) : 0/1/2/3 ; aucun message, avertissement ni compteur émis par la passe (D6).

## Garanties vérifiables

- Sur un run sans `](</...>)` dans les lignes conservées : sorties identiques octet par octet à avant la feature (SC-003).
- Avec `--conserver-liens` : toutes les sorties identiques octet par octet à avant la feature (SC-004).
- Deux runs identiques (mêmes entrée et options) : sorties identiques octet par octet (FR-007, SC-002).
