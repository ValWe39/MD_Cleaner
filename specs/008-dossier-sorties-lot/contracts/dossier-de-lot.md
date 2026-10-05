# Contrat CLI : dossier de run par invocation

**Feature**: 008-dossier-sorties-lot | **Date**: 2026-10-05 | **Source**: [spec.md](../spec.md), [research.md](../research.md) (D1-D7)

Ce contrat décrit le delta observable apporté aux features 001 et 007 (`specs/001-nettoyage-md-repetitif/contracts/cli.md`, `specs/007-traitement-multi-documents/contracts/multi-entrees.md`, révisés dans la même livraison). Tout ce qui n'est pas mentionné ici est inchangé : résolution du lot, ordre, doublons, options applicables, neutralisation de `--dry-run`/`--suggestion`, échecs (`ERREUR : ...`, poursuite, fail-fast au 3e échec consécutif), codes retour, messages par document.

## Structure de sortie

- **Une invocation = un dossier de run** dans la racine `--sortie`, quel que soit le nombre de documents ; la numérotation séquentielle consomme **un numéro par invocation**.
- Les sorties nettoyées de tous les documents du lot vivent à plat dans ce dossier : `<nom-dérivé>-nettoye.md` chacun (règle 006 inchangée).
- Jamais d'écrasement : les collisions (stems identiques, doublons) sont résolues par le suffixe existant `-1`, `-2`, ... avant l'extension.

## Sorties de `--pagine`

| Contexte | Fichiers par document |
| -------- | --------------------- |
| lot d'un document (et mono-document) | `nettoye-pagine.md`, `cartographie.json` (inchangés) |
| lot de plusieurs documents | `<nom-dérivé>-nettoye-pagine.md`, `<nom-dérivé>-cartographie.json` |

- Le nom dérivé suit la règle 006 (stem tronqué à 20 points de code, espaces remplacées).
- Unicité par le même mécanisme anti-collision (`-1`, `-2`, ... avant l'extension) ; pour deux documents de stems identiques, les artefacts homologues du second portent le même indice que sa sortie nettoyée (ex. `consolidated-nettoye-1.md`, `consolidated-nettoye-pagine-1.md`, `consolidated-cartographie-1.json`).

## `--nom-titre`

- Mono-document : inchangé (dossier nommé d'après le titre du document).
- Lot de plusieurs : **neutralisée avec avertissement** sur stderr (`AVERTISSEMENT : --nom-titre ignorée en lot : applicable à un seul document`) ; le dossier prend la numérotation séquentielle seule. Jamais silencieuse.

## Cas bornés

| Cas | Comportement |
| --- | ------------ |
| lot vide (aucun document retenu) | erreur code 1, **aucun dossier créé** |
| lot avec échecs | sorties des documents réussis conservées dans le dossier unique, aucun marqueur, code 1 |
| lot entièrement en échec | dossier de run vide en place, code 1 |
| lot interrompu par fail-fast | sorties déjà produites conservées, documents suivants non traités |

## Exemples

```text
md-cleaner a.md b.md                 # output/00X : a-nettoye.md, b-nettoye.md
md-cleaner a.md b.md --pagine        # output/00X : + a-nettoye-pagine.md, a-cartographie.json,
                                     #            + b-nettoye-pagine.md, b-cartographie.json
md-cleaner c1.md c2.md               # stems identiques "c" : c-nettoye.md, c-nettoye-1.md
md-cleaner a.md b.md --nom-titre 30  # avertissement, dossier numéroté (pas de slug)
md-cleaner a.md                     # inchangé : output/00X/a-nettoye.md
```

## Rétrocompatibilité

L'invocation mono-document est strictement inchangée : un dossier, mêmes noms d'artefacts, même numérotation, `--nom-titre` fonctionnel (FR-004, SC-003 de la spec 008).
