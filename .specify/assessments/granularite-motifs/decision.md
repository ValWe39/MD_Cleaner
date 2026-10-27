# Decision: Rendre chaque motif décidable indépendamment au dry-run

- **Slug**: granularite-motifs
- **Decided**: 2026-09-29
- **Verdict**: go
- **Artifacts reviewed**: intake.md | research.md | problem.md | concept.md

## Scorecard

- **Problem validity** (strong) : Cas réel et reproductible : M02 indivisible
  (interface + métadonnées, 279 lignes, 7 intervalles disjoints) sur output-016,
  décision tout-ou-rien documentée au run 010 (problem.md, research.md)
- **Evidence strength** (strong) : L'hypothèse critique de l'option A a été
  **mesurée** lors de la décision : prototype temporaire de la règle majoritaire
  sur les 3 documents réels — le pontage passe bien par des chevauchements
  minoritaires, la séparation filtres/métadonnées s'obtient, et les blocs
  compacts d'Exemple_1 survivent à l'identique (4 motifs inchangés)
- **Value vs. inaction** (strong) : La décision « supprimer l'interface, garder
  les métadonnées » devient exprimable — exactement le blocage constaté ; le
  coût de l'inaction est une boucle dry-run inutile sur la classe listings
- **Feasibility / appetite** (strong) : Prototype fonctionnel en quelques heures
  (variante temporaire de `detecter`, source non modifiée) ; budget small
  confirmé ; performance inchangée
- **Strategic fit** (strong) : Une seule règle déterministe de plus, stdlib
  uniquement, pas de nouveau paramètre exposé — conforme aux principes III et IV
  de la constitution
- **Risk posture** (adequate) : Risque principal mesuré : la coupure produit
  **25-29 motifs** sur les documents ccomptes (contre 2 aujourd'hui), au-dessus
  de la cible 5-10 de l'intake — mais seulement **4 à 5 sont action=supprimer**
  (nav, marqueur institution, dates, filtres), les ~21-25 autres sont des motifs
  sous le seuil proposés « conserver » par défaut, sans action requise. Risques
  secondaires : instabilité des ids entre versions (suggestions à régénérer),
  lisibilité du rapport. Non encore tranchés, à porter en specification

## Verdict & Rationale

**Go.** Les six critères sont à adequate ou mieux, et l'hypothèse faiseuse ou
briseuse d'Option A n'est plus une supposition : la mesure la confirme
(chevauchements minoritaires = ponts ; blocs compacts = chevauchements
majoritaires). Le critère binaire du problem.md — filtres et métadonnées dans
des motifs distincts sur output-016 — est satisfait par le prototype, sans
régression visible sur Exemple_1. La cible « 5-10 blocs » de l'intake n'est pas
tenue au sens strict (25-29 motifs listés), mais la charge de décision *réelle*
(motifs supprimables à arbitrer) retombe dans la cible (4-5) ; la tension
comptage/présentation est explicitement portée en question ouverte pour la
specification plutôt qu'en critère bloquant.

## If go — Handoff to `/speckit-specify`

- **Problem** : les motifs chaînés par fusion regroupent des natures différentes
  (interface + métadonnées) dans un bloc indivisible, rendant la décision du
  dry-run tout-ou-rien sur les documents à métadonnées récurrentes (problem.md).
- **Chosen approach** : Option A du concept.md — coupure de fusion par
  chevauchement majoritaire (une fusion n'est admise que si le chevauchement se
  vérifie sur une proportion des pages du candidat ; prototype validé, cf.
  mesure du 2026-09-29).
- **In scope** : la nouvelle règle de fusion dans la détection ; la
  re-présentation du rapport dry-run si nécessaire ; la mise à jour de la suite
  de tests (SC-001/002/005 inchangés, nouveaux tests sur la coupure) ;
  documentation de l'instabilité des ids entre versions.
- **Out of scope** (concept.md + problem.md) : plafond/plancher numérique de
  blocs ; nouvelle option CLI ; signaux de densité/position (option C) ;
  scission a posteriori (option B) sauf si la spec échoue ; DOM/dépendances ;
  sélection ligne à ligne ; changement des formats de sortie.
- **Success metrics** : (1) sur output-016, filtres et métadonnées dans des
  motifs distincts — **déjà démontré par le prototype** ; (2) Exemple_1 : 4
  motifs compacts inchangés — démontré ; (3) charge de validation : les motifs
  action=supprimer restent ≤ ~5 sur le corpus réel — démontré (4) ; (4) tests
  existants au vert sans relâchement des seuils ; (5) déterminisme octet par
  octet conservé.
- **Carried-forward open questions** :
  - Valeur de la proportion majoritaire (0.5 mesuré : 25 motifs ; 0.8 mesuré :
    29 motifs — 0.5 est le meilleur des deux essayés ; le nombre exact reste un
    choix de specification)
  - Présentation du rapport dry-run face à 20+ motifs « conserver » :
    regroupement en section secondaire déjà existante (« sous le seuil »), tri,
    ou pliage ? (SC-004 : validation < 5 min à re-vérifier)
  - Instabilité des ids entre versions de l'outil : note de version / README, et
    rappel dans le rapport dry-run
  - Faut-il une entrée CHANGELOG ou une note de migration pour les suggestions
    existantes (régénération par dry-run) ?

## Mesure de validation (annexe, 2026-09-29)

Prototype en fichier temporaire (source du dépôt non modifiée), règle « fusion
si chevauchement sur ≥ proportion des pages du candidat » :

- Exemple_1 : 4 motifs à 0.5 **et** 0.8 — identiques à la détection actuelle
  (les chaînes compactes légitimes survivent)
- Exemple_2 / output-016 à 0.5 : 25 motifs ; filtres isolés en un motif
  supprimer (bornes 180-450 de la page 1) distinct des métadonnées de
  publications ; 4 motifs supprimer au total
- output-016 à 0.8 : 29 motifs — proportion plus stricte = plus de
  fragmentation, sans gain de séparation

Le fichier du prototype a été supprimé après la mesure ; aucune modification du
code source n'a été effectuée lors de l'évaluation.
