# Problem Definition: Sorties nettoyées indissociables de leur document source

- **Slug**: nom-sortie-nettoye
- **Created**: 2026-10-05
- **Inputs used**: intake.md | research.md absent | user input (note sur les
  collisions)

## Problem Statement

L'utilisateur de md-cleaner ne peut pas identifier, par le nom de son fichier,
de quel document source provient une sortie nettoyée : tous les runs produisent
un fichier au nom identique (`nettoye.md`), seule l'arborescence ou l'ouverture
du fichier permettant de faire le lien avec l'entrée. Cela coûte du temps et
provoque des confusions dès qu'il traite plusieurs documents ou réutilise les
sorties hors de leur dossier de run.

## Affected Users & Stakeholders

- **Users**: l'utilisateur du dépôt (propriétaire, seul utilisateur actuel) —
  doit deviner ou ouvrir chaque `nettoye.md` pour savoir quelle source il
  manipule, et risque des erreurs de manipulation (mauvais fichier copié,
  écrasé, envoyé).
- **Stakeholders**: le propriétaire du projet — décide du périmètre exact du
  changement (fichier seul, dossier de run, toutes les sorties).

## Goals

- Toute sortie nettoyée est reconnaissable comme appartenant à un document
  source précis, sans ouvrir le fichier ni parcourir l'arborescence.
- Le lien nom de sortie → document d'entrée est lisible et prévisible pour
  l'utilisateur (il peut anticiper le nom produit).
- Les espaces et collisions de noms ne produisent ni nom fragile ni écrasement
  silencieux.

## Non-Goals

- Renommer ou réorganiser les dossiers de run existants (numérotation
  séquentielle, `--nom-titre`) — hors périmètre sauf clarification contraire.
- Traiter plusieurs documents en une invocation (exclué par FR-001, feature
  001).
- Contenu des sorties, format des rapports ou JSON — inchangés.

## Success Metrics

- Sur un lot de documents aux noms distincts, chaque sortie nettoyée porte un
  nom unique et dérivé de sa source (baseline : toutes s'appellent
  `nettoye.md`). (qualitative : lisibilité du lien nom/source pour
  l'utilisateur)

## Cost of Inaction

Chaque nouveau document traité ajoute un `nettoye.md` de plus, indissociable des
autres par son nom ; le risque de confusion et de manipulation erronée croît
linéairement avec l'usage, et l'utilisateur continue de renommer les sorties à
la main.

## Open Questions

- [NEEDS CLARIFICATION: « titre du document d'input » = nom de fichier (stem,
  comme l'exemple) ou premier titre `#` du contenu ?]
- [NEEDS CLARIFICATION: périmètre des sorties concernées — `nettoye.md` seul, ou
  aussi `nettoye-pagine.md`, `cartographie.json`, `suggestion.json`,
  `rapport-dry-run.md` ?]
- [NEEDS CLARIFICATION: troncature à 20 caractères — brute, ou au dernier mot
  entier ? caractères non espace (accents, ponctuation, séparateurs) conservés
  ou normalisés ?]
- [RÉSOLU (décision utilisateur, session du 2026-10-05): collision de noms →
  suffixe numérique `-1` par ordre de traitement, appliqué au nom de la sortie.]
- [NEEDS CLARIFICATION: comportement par défaut ou option — le nommage actuel
  `nettoye.md` doit-il rester accessible ?]
