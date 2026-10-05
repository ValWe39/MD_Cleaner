# Data Model: Un dossier de sorties partagé pour les documents d'un même lot

**Feature**: 008-dossier-sorties-lot | **Date**: 2026-10-05 | **Source**: [spec.md](./spec.md), [research.md](./research.md) (D1-D7)

Aucune entité persistante nouvelle : les sorties restent des fichiers locaux dans `output/<run>/`. Les entités ci-dessous décrivent la nouvelle structure d'invocation ; elles vivent le temps d'une invocation.

## Entités

### Dossier de run d'invocation

- **Représente** : l'unique dossier de sortie d'une invocation, quel que soit le nombre de documents.
- **Champs** : `chemin: Path` (sous la racine `--sortie`, numérotation séquentielle, ou slug de titre en mono-document avec `--nom-titre`), `est_partage: bool` (lot de plusieurs).
- **Cycle de vie** : créé en tête d'invocation pour un lot de plusieurs (après résolution du lot, neutralisations et validation de l'échantillon) ; créé pendant le traitement du document pour un lot d'un. Lot vide → jamais créé.
- **États** :
  - lot entièrement en échec → dossier vide en place (FR-007) ;
  - lot incomplet → contient les sorties des documents réussis, sans marqueur (FR-006) ;
  - lot complet → contient toutes les sorties (nettoyées, et paginées/cartographies si `--pagine`).
- **Relations** : contient N sorties nettoyées et, en lot de plusieurs avec `--pagine`, N paires de sorties secondaires préfixées.

### Sortie nettoyée

- **Représente** : le livrable d'un document, inchangé depuis 006.
- **Champs** : nom `<nom-dérivé>-nettoye.md` (règle 006 : stem tronqué à 20 points de code, espaces remplacées, suffixe `-nettoye`).
- **Unicité** : dans le dossier partagé, garantie par le suffixe anti-collision (`-1`, `-2`, ... avant l'extension) — `resoudre_chemin_nettoye` (006, refactoré en appel à `resoudre_chemin_libre`).

### Sortie secondaire préfixée

- **Représente** : les artefacts `--pagine` d'un document, en lot de plusieurs.
- **Champs** : `<nom-dérivé>-nettoye-pagine.md` et `<nom-dérivé>-cartographie.json`, où le nom dérivé suit la règle 006.
- **Unicité** : suffixe anti-collision de même forme, résolu par artefact dans l'ordre de traitement — deux documents de stems identiques voient leurs artefacts homologues porter le même indice (ex. `-1` pour le second document traité).
- **Relation** : attribuable à son document par le préfixe ; l'indice de suffixe aligne les artefacts d'un même document.
- **Exception** : en lot d'un document (comme en mono-document), les noms courts (`nettoye-pagine.md`, `cartographie.json`) demeurent.

### Involution des entités 007 (inchangées, citées pour frontière)

- **Lot, Résultat de document, Compteur d'échecs consécutifs** : identiques à la feature 007 (résolution, échecs, fail-fast, codes retour) — la 008 ne touche que la destination des écritures.

## Diagramme de flux (textuel)

```text
invocation (n entrées) --007--> lot { documents }
lot vide ?                --> erreur code 1, aucun dossier
|lot| > 1 ?               --> neutralisations (dry-run, suggestion, nom-titre)
                            --> création unique du dossier de run (numérotation)
boucle sur documents      --> écritures dans le dossier partagé :
                              <nom-dérivé>-nettoye.md         (résolveur 006)
                              <nom-dérivé>-nettoye-pagine.md   (lot > 1, résolveur libre)
                              <nom-dérivé>-cartographie.json   (lot > 1, résolveur libre)
                              (noms courts si lot d'un document)
échecs                    --> 007 inchangé (ERREUR, poursuite, fail-fast, code 0/1)
```
