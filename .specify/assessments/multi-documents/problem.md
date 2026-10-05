# Problem Definition: Nettoyer plusieurs documents impose N invocations manuelles

- **Slug**: multi-documents
- **Created**: 2026-10-05
- **Inputs used**: intake.md | research.md

## Problem Statement

Le propriétaire du projet, travaillant sur des corpus de plusieurs documents
Markdown (aujourd'hui 3 exemples de référence, potentiellement plus), doit
lancer `md-cleaner` une fois par document en ré-écrivant les mêmes options de
cleaning à chaque invocation : la charge de lancement croît linéairement avec
la taille du corpus, et chaque relance manuelle est une occasion
d'incohérence (option oubliée, seuil différent d'un document à l'autre)
alors que le traitement lui-même est identique document par document.

## Affected Users & Stakeholders

- **Users** : le propriétaire-utilisateur du dépôt (seul utilisateur
  identifié) — nettoie ses corpus en série, document par document, en
  répétant la même commande (research.md : signal de demande faible, un
  seul porteur).
- **Stakeholders** : le mainteneur-décideur (même personne) — arbitre le
  coût de révision du contrat CLI fondateur « un run = un fichier
  d'entrée » (FR-001) contre le gain de commodité.

## Goals

- Traiter un corpus de K documents en une seule opération de lancement,
  sans dépendre du nombre de documents.
- Un résultat par document : N documents en entrée → N sorties nettoyées,
  une par document, sans qu'un document soit perdu ou fusionné.
- Une seule expression des paramètres de cleaning pour tout le corpus —
  les mêmes règles s'appliquent à chacun des documents.
- Capacité à viser un corpus par dossier (le lot de documents est déjà
  regroupé sur le disque) sans énumérer les fichiers un à un.
- Comportement prévisible et non silencieux lorsque certaines capacités de
  l'outil ne s'appliquent pas à un lot.

## Non-Goals

- Des paramètres de cleaning différents par document au sein d'un même lot
  (hors périmètre : le lot est homogène par définition).
- Accélérer le traitement lui-même (parallélisme, performance) — le sujet
  est le nombre d'invocations, pas la vitesse par document.
- Modifier les règles de nettoyage, de détection, de segmentation ou les
  sorties d'un document individuel — le résultat par document doit rester
  celui d'aujourd'hui.
- Automatiser la boucle de jugement dry-run → suggestion → relance pour un
  lot (chaque document garde son arbitrage individuel, réalisé
  séquentiellement).
- Tout ce qui sort du CLI (GUI, serveur, watch de dossier).

## Success Metrics

- Nettoyer un corpus de K documents nécessite 1 invocation au lieu de K
  (baseline : K=3 documents d'entrée dans `Examples/` → 3 invocations
  aujourd'hui) — mesurable.
- Parité document par document : la sortie nettoyée de chaque document d'un
  lot est identique octet par octet à celle obtenue en l'invocationnant
  seul avec les mêmes options (baseline : inconnu, à établir sur les 3
  exemples de référence lors de la spécification) — mesurable.
- Aucun paramètre de cleaning applicable (seuil, conservation des liens,
  pagination, etc.) ne change d'effet entre un traitement en lot et un
  traitement individuel (baseline : à définir par les tests de parité) —
  mesurable.
- Toute capacité non applicable en lot fait l'objet d'un signalement
  explicite à l'utilisateur, jamais d'un silence (baseline : inexistante,
  notion nouvelle) — qualitatif.

## Cost of Inaction

Si rien n'est construit : chaque corpus multi-documents continue d'exiger
une invocation manuelle par document avec les mêmes options réécrites (ou
un script de boucle non documenté, écrit et maintenu par l'utilisateur). Le
coût reste modéré au volume actuel (3 documents) mais croît linéairement
avec le corpus ; le risque d'incohérence de paramètres entre documents d'un
même corpus persiste ; la capacité multi-fichiers, standard de fait chez
les formatters/linters Markdown (prettier, mdformat, markdownlint-cli2),
continue de manquer. Aucune perte fonctionnelle en revanche : le
contournement (boucle shell) couvre déjà le besoin, sans limitation autre
que la répétition (research.md : Market & Context).

## Open Questions

- [NEEDS CLARIFICATION: récursivité du scan d'un dossier — non récursif
  comme `--echantillon` ou récursif comme prettier ? Cas d'un dossier ne
  contenant que des sous-dossiers (ex. `Examples/Exemple_1/` avec
  `1.Sample/` + `2.Input/`).]
- [NEEDS CLARIFICATION: une même invocation peut-elle mélanger fichiers
  individuels et dossiers ?]
- [NEEDS CLARIFICATION: sémantique de « ignorées » pour les options non
  applicables en lot (dry-run, suggestion) — erreur bloquante,
  avertissement, silence ; le dry-run est-il réellement inapplicable par
  lot ou seulement hors périmètre choisi ?]
- [NEEDS CLARIFICATION: échec partiel — un document en erreur arrête-il
  le lot ? Quel code retour pour un succès partiel ? Sorties des documents
  réussis conservées ou annulées ?]
- [NEEDS CLARIFICATION: organisation des sorties d'un lot (dossier de run
  unique vs sous-dossiers par document) et interaction avec la numérotation
  séquentielle et le nommage par titre.]
- [NEEDS CLARIFICATION: doublons dans le lot (même fichier deux fois,
  fichier listé et contenu dans le dossier) et ordre de traitement (ordre
  d'apparition vs tri par nom).]
- [NEEDS CLARIFICATION: plafond éventuel du nombre de documents d'un lot
  (précédent : `--echantillon` plafonne à 5).]
- [NEEDS CLARIFICATION: confirmation que `--pagine`, `--conserver-liens`,
  `--seuil`, `--calibrage`, `--extrait` restent applicables document par
  document en lot.]
