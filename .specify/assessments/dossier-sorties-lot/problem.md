# Problem Definition: Les sorties d'un lot sont éparpillées dans output/

- **Slug**: dossier-sorties-lot
- **Created**: 2026-10-05
- **Inputs used**: intake.md | research.md

## Problem Statement

Lors d'une invocation multi-documents (`md-cleaner doc1 doc2`), les
sorties des documents du lot sont dispersées dans autant de sous-dossiers
de `output/` qu'il y a de documents (001, 002, ...) : le lot n'est pas
identifiable comme tel, l'utilisateur doit compter les numéros ou
reconstituer la liste depuis la console pour retrouver « les sorties de
son invocation », et la numérotation séquentielle est consommée au
rythme des documents plutôt que des invocations.

## Affected Users & Stakeholders

- **Users** : le propriétaire-utilisateur du dépôt — chaque lot
  multi-documents (livré ce jour même par la feature 007) le conduit
  à reconstituer mentalement l'appartenance des dossiers de run
  (research.md : friction formulée le jour de la livraison, défaut
  prédit par l'assessment multi-documents).
- **Stakeholders** : le mainteneur-décideur (même personne) — arbitre
  le coût de migration (tests, contrats 007 et 001, README) contre le
  gain de lisibilité des sorties.

## Goals

- Retrouver toutes les sorties d'une même invocation dans un seul
  sous-dossier d'`output/`, identifiable sans ambiguïté.
- Une consommation de numéro séquentiel par invocation (le « run »
  correspond à l'invocation, pas au document).
- Aucune perte ni écrasement de sortie documentaire : chaque document
  du lot garde une sortie distincte et attribuable.
- Un comportement du mono-document strictement inchangé (structure,
  noms, numérotation).
- Une convention de sortie alignée sur les standards des outils de
  traitement par lot (un dossier de sortie par invocation, fichiers
  nommés d'après leur entrée).

## Non-Goals

- Changer le contenu des sorties (nettoyage, pagination, cartographie
  restent ce qu'ils sont document par document).
- Ajouter un résumé de lot, une reprise de lot ou toute autre
  extension de l'option B au-delà du regroupement des sorties.
- Réorganiser les invocations mono-document (leur structure est déjà
  la cible).
- Modifier la résolution du lot, l'ordre de traitement, la
  neutralisation des options ou la sémantique d'échec (livrés et
  testés par 007).

## Success Metrics

- Une invocation de K documents produit exactement 1 sous-dossier de
  run contenant K fichiers nettoyés (baseline : 1 lot de 3 documents
  sur les exemples de référence → 3 dossiers aujourd'hui) —
  mesurable.
- Deux documents de stems identiques dans un même lot produisent deux
  sorties distinctes, jamais d'écrasement (baseline : couvert par le
  suffixe anti-collision, à re-vérifier à l'échelle du dossier
  partagé) — mesurable.
- Le mono-document conserve strictement sa structure actuelle : la
  suite de tests existante passe sans relâchement sur ce point —
  mesurable.
- Les sorties secondaires (`--pagine`) de chaque document du lot
  restent attribuables à leur document dans le dossier partagé
  (baseline : impossible aujourd'hui — noms fixes qui s'écraseraient)
  — mesurable.
- La numérotation consomme un numéro par invocation (baseline : un
  par document) — mesurable.

## Cost of Inaction

Chaque lot multi-documents continue de produire N dossiers de run
consécutifs indiscernables de N invocations séparées ; l'utilisateur
reconstitue l'appartenance à la main (comptage des numéros, relecture
console), ce que la moindre invocation intercalée vient casser ; la
numérotation séquentielle se consomme au rythme des documents. Le
problème est borné au confort de sortie (le contenu nettoyé, lui, est
correct), mais il touche chaque lot et la capacité « lot » vient
précisément d'être livrée comme valeur d'usage (research.md : Market &
Context).

## Open Questions

- [NEEDS CLARIFICATION: `--nom-titre` en lot de plusieurs — le
  dossier partagé prend-il le titre du premier document, l'option
  est-elle neutralisée en lot (numérotation seule), ou refusée ?]
- [NEEDS CLARIFICATION: forme du nommage des sorties secondaires dans
  le dossier partagé — préfixage par stem (`<stem>-nettoye-pagine.md`,
  `<stem>-cartographie.json`), aligné sur la règle 006, ou autre
  mécanisme anti-collision ?]
- [NEEDS CLARIFICATION: divergence de nommage assumée entre
  mono-document (`nettoye-pagine.md` court) et lot (préfixé) — ou
  unification des deux formes ?]
- [NEEDS CLARIFICATION: marquage d'un lot incomplet (échec partiel) —
  aucun marquage (trace console + code 1 suffisent) ou fichier
  marqueur dans le dossier ?]
- [NEEDS CLARIFICATION: confirmation que le lot d'un seul document
  garde la structure actuelle inchangée (le regroupement ne
  s'applique qu'aux lots de plusieurs).]
