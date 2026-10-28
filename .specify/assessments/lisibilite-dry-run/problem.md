# Problem Definition: Extraits indiscernables dans la suggestion

- **Slug**: lisibilite-dry-run
- **Created**: 2026-09-29
- **Inputs used**: intake.md + research.md + décision de cadrage de
  l'utilisateur (session du 2026-09-29)

## Problem Statement

Les extraits des motifs dans `suggestion.json` — la surface de jugement où
l'utilisateur décide de conserver ou supprimer chaque bloc — sont limités à 3
lignes, ce qui rend la majorité des motifs indiscernables entre eux (mesure : 14
motifs sur 26 partagent exactement le même extrait) et oblige à ouvrir le
document source en parallèle pour juger, cassant le flux de validation du
dry-run.

## Affected Users & Stakeholders

- **Users** : l'utilisateur de md-cleaner qui valide un dry-run en éditant les
  `action` dans `suggestion.json` — il ne peut pas juger un motif sans localiser
  à la main la zone correspondante dans le document source (source :
  research.md, mesures output/003)
- **Stakeholders** : le propriétaire-mainteneur — a posé la règle de gouvernance
  du jour : une commande qu'il demande est ajoutée sans objection YAGNI, un tour
  final de consolidation des options étant prévu plus tard ; la constitution
  (IV, simplicité) reste la garde globale

## Goals

- Chaque motif d'une suggestion est **distinguable par son extrait seul**, sans
  ouvrir le document source, sur les documents riches
- Le **nombre de lignes de l'extrait est réglable par l'utilisateur** via une
  commande dédiée (règle de gouvernance du 2026-09-29 : les options demandées
  par l'utilisateur sont légitimes par défaut)
- La valeur par défaut correspond à la **dose de saturation mesurée** (5 lignes
  : 24 extraits distincts sur 25 motifs ; 8 lignes n'apportent rien de plus)
- Le comportement reste déterministe ; la suggestion reste le seul artefact
  contractuel modifié

## Non-Goals

- Le **rapport dry-run n'est pas modifié** : décision de cadrage explicite de
  l'utilisateur — il juge dans le JSON, le tableau du rapport conserve sa
  troncature à 120 caractères comme simple aperçu
- Aucun changement de la détection, des actions supprimer/conserver, des seuils
  ou du schéma de la suggestion en dehors de la longueur de l'extrait
- L'extrait ne devient pas un duplicatat du document : borne haute sur le nombre
  de lignes, le document source reste la référence
- Pas de nouvelles dépendances, pas de changement des formats de sortie de
  nettoyage (nettoye, paginé, cartographie)

## Success Metrics

- Sur un dry-run de `Examples/Exemple_2` avec la valeur par défaut : au plus 2
  motifs partagent le même extrait (baseline actuelle : 12 motifs en doublon à 3
  lignes ; cible mesurée à 5 lignes : 2) — critère mécanique
- La commande de réglage produit l'effet attendu : un extrait de N lignes
  demandé donne exactement N lignes (bornes à définir, ordre de grandeur : 1 à
  25) — testable unitairement
- L'utilisateur juge un dry-run complet d'un document riche sans ouvrir le
  document source — validation qualitative (quickstart)
- La taille de `suggestion.json` sur le corpus réel reste sous 1 Mo (mesure
  actuelle de l'entrée : 125 Ko ; impact attendu de l'extrait étendu : quelques
  dizaines de Ko) — garde quantitatif simple
- Le déterminisme est conservé (deux exécutions identiques → JSON identique
  octet par octet)

## Cost of Inaction

Chaque validation de dry-run sur un document riche exige d'ouvrir le document
source et de rechercher les zones à la main pour juger les motifs indiscernables
; sur la classe de documents où la feature 002 produit ~25 motifs, la friction
est systématique et le temps de validation mesuré (SC-004/SC-006 : < 5 min) est
menacé. Le corpus d'usage réel est aujourd'hui petit (3 documents), mais la
friction est déjà documentée sur le premier document riche traité.

## Decisions de cadrage (session du 2026-09-29)

Les quatre questions ouvertes ont été tranchées par l'utilisateur :

1. **Périmètre de la commande** : le réglage du nombre de lignes s'applique au
   **JSON seul** — le rapport dry-run reste hors périmètre (aperçu tronqué à 120
   caractères inchangé).
2. **Rendu de l'extrait** : **vrais sauts de ligne** (`\n` dans le JSON, rendus
   ligne par ligne par tout lecteur) plutôt que la jonction « / » actuelle —
   démonstration faite : les lignes vides deviennent des lignes vides visibles.
3. **Position** : **incluse** dans la suggestion (page et lignes de la première
   occurrence de chaque motif) — les emplacements existent en interne,
   l'exposition est simple ; complément d'identification qui résout aussi en
   partie le cas des doublons résiduels.
4. **Doublons résiduels** : les 2 motifs partageant encore un extrait à 5 lignes
   sont **acceptables** — la position les distingue de toute façon (point 3).
