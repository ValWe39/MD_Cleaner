# Idea Intake: Un dossier de sorties partagé pour les documents d'un même lot

- **Slug**: dossier-sorties-lot
- **Created**: 2026-10-05
- **Source**: pasted text (session CLI du 2026-10-05, suite de la
  livraison de la feature 007)
- **Type**: improvement

## Idea (as captured)

> Est-il possible que les éléments traités en une seule invocation
> appraîssent [sic : « apparaîssent » présumé] dans le même sous-dossier
> d'output ?

Addendum (clarification utilisateur, même session) :

> En effet, actuellement, si je commande "md-cleaner doc1 doc2",
> l'outil créer [sic : « crée » présumé] 2 sous dossier 00X et 00X+1
> pour l'output. Je ne veux qu'un seul 00X avec mes deux outputs.

La forme visée est donc précisée : un **dossier de run unique
numéroté** pour toute l'invocation, contenant les N sorties nettoyées
— et non un dossier parent regroupant des sous-dossiers de run.

## Restated

Regrouper dans un même sous-dossier d'`output/` toutes les sorties des
documents traités lors d'une même invocation multi-documents, au lieu
de la structure actuelle où chaque document du lot produit son propre
dossier de run numéroté, indiscernable d'invocations séparées.

## Origin & Context

- **Raised by**: l'utilisateur (mainteneur du projet MD_Cleaner), juste
  après la livraison de l'implémentation 007 (commit `5c906b9`).
- **Trigger**: friction pressentie ou constatée face au lot invisible
  dans `output/` — exactement le défaut assumé de l'option A retenue
  lors de l'assessment `multi-documents` : « le lot n'est pas
  identifiable dans output/ (N dossiers de run consécutifs
  indiscernables de N invocations manuelles) ». L'option B
  (« Lot avec visibilité de lot ») du concept.md de `multi-documents`
  décrivait déjà ce regroupement comme extension sans regret.
- **Codebase concerné (observation à la prise de note)** : depuis 007,
  chaque document du lot appelle `creer_dossier_run` et produit son
  propre sous-dossier séquentiel (`output/001`, `002`, ...) ; les
  fichiers nettoyés y sont nommés d'après leur stem (feature 006) ;
  la numérotation séquentielle est globale à la racine `--sortie`.

## First-Glance Unknowns

- [RÉSOLU en session : la forme visée est un dossier de run unique
  numéroté contenant les N sorties nettoyées (addendum ci-dessus),
  conformément à l'option B de l'assessment multi-documents.]
- [NEEDS CLARIFICATION: interaction avec la numérotation séquentielle
  existante (le lot consomme un seul numéro 00X) et avec `--nom-titre`
  (lequel titre pour un lot de plusieurs documents ?)]
- [NEEDS CLARIFICATION: le mono-document change-t-il de structure de
  sorties (rétrocompatibilité du contrat 006/007) ou la structure
  actuelle vaut-elle déjà pour le cas « lot d'un document » ?]
- [NEEDS CLARIFICATION: sorties secondaires à nom fixe
  (`nettoye-pagine.md`, `cartographie.json`) — un exemplaire par
  document dans le dossier de lot partagé exige un préfixage ou un
  autre mécanisme anti-collision (deux documents produiraient
  autrement le même nom de fichier) ; les artefacts du dry-run ne
  concernent que le lot d'un document (neutralisés sinon) et ne sont
  pas affectés.]
- [NEEDS CLARIFICATION: collisions de noms au sein du dossier de lot —
  deux documents de stems identiques produisent deux
  `<stem>-nettoye.md` (le suffixe anti-collision existant
  `resoudre_chemin_nettoye` couvre déjà ce cas à l'échelle du
  dossier, à confirmer en spécification).]
- [NEEDS CLARIFICATION: comportement en cas d'échec partiel — le
  dossier de lot contient les sorties des seuls documents réussis ;
  faut-il le marquer comme « lot incomplet » ?]
