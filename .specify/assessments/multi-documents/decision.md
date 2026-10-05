# Decision: Invocation multi-entrées — un lot, un traitement par document

- **Slug**: multi-documents
- **Decided**: 2026-10-05
- **Verdict**: go
- **Artifacts reviewed**: intake.md | research.md | problem.md | concept.md
- **User validation**: recommandation (Option A) confirmée explicitement
  lors de la session

## Scorecard

- **Problem validity — adequate** : friction réelle (N invocations
  manuelles, options réécrites à chaque document, risque d'incohérence de
  paramètres au sein d'un corpus) mais non mesurée : un seul porteur,
  corpus actif de 3 documents, contournement fonctionnel existant
  (research.md, problem.md).
- **Evidence strength — adequate** : côté offre, fort et entièrement cité
  — contrats internes lus (FR-001, `--echantillon`, nommage 006), code
  inspecté, conventions externes documentées (prettier, mdformat,
  markdownlint-cli2) ; côté demande, mince — demande déclarée, non
  observée (research.md : signal faible). La combinaison reste au-dessus
  de adequate car les contraintes techniques qui fondent l'arbitrage
  (suggestion liée à `source`, scan de dossier existant) sont mesurées,
  pas supposées.
- **Value vs. inaction — adequate** : le coût de l'inaction est documenté
  et modéré (boucle shell possible, répétition linéaire, risque
  d'incohérence persistant) ; la valeur est un confort de lancement, non
  une capacité nouvelle. Bat l'inaction sans la dominer.
- **Feasibility / appetite — strong** : option A appetite small crédible :
  chaque document emprunte le chemin de code existant (parité octet par
  octet par construction), le scan de dossier a un précédent direct dans
  `charger_echantillon`, la stdlib suffit, la surface de contrat reste
  l'argumentaire positionnel (concept.md).
- **Strategic fit — strong** : point d'entrée CLI unique conservé, local,
  déterministe, stdlib (constitution II, IV) ; première révision du point
  d'entrée FR-001 assumée et bornée ; le refus explicite des options
  inapplicables sert l'exigence de non-silence du problem.md.
- **Risk posture — adequate** : risques identifiés et mitigués au niveau
  concept : lot invisible dans `output/` (assumé, comblable par l'option B
  sans regret), fail-fast laissant un lot partiel (assumption à valider),
  récursivité (open question bornée hors scope par défaut), sémantique
  exacte du refus des options (spécification). Aucun risque non mitigué
  identifié.

## Verdict & Rationale

**Go.** Aucun critère sous adequate, et le seul critère qui aurait pu être
weak — la force de la demande — est neutralisé comme dans les précédents
004/005 : le décideur unique est l'utilisateur porteur, et les contraintes
qui ont façonné la recommandation sont mesurées sur le code, pas supposées.
L'option A est retenue (confirmation utilisateur) précisément parce qu'elle
maximise le rapport objectifs/contrat-touché : les quatre objectifs du
problem.md sont servis, la métrique de parité est garantie par construction,
et les deux rabbit holes structurants du concept (visibilité de lot, échec
partiel) sont explicitement reportés plutôt que grignotés — l'option B reste
une extension sans regret si la friction du lot invisible se matérialise.
Le verdict est go en connaissance du point faible : c'est une décision de
commodité à petit budget, pas une correction de problème mesuré sur
artefacts comme 004/005.

## If go — Handoff to `/speckit-specify`

- **Problem** : nettoyer un corpus de K documents impose K invocations
  manuelles avec les mêmes options réécrites à chaque fois — charge de
  lancement linéaire et risque d'incohérence de paramètres au sein d'un
  corpus, alors que le traitement est identique document par document
  (problem.md).
- **Chosen approach** : Option A du concept.md — lot positionnel minimal :
  la CLI accepte plusieurs entrées (fichiers `.md` et/ou dossiers dont
  seuls les `.md` de premier niveau sont retenus, précédent
  `--echantillon`), chaque document est traité séquentiellement par le
  chemin de code existant avec ses sorties et son dossier de run propres,
  les options de cleaning s'appliquent telles quelles à tous, `--dry-run`
  et `--suggestion` sont refusés explicitement en lot, fail-fast en cas
  d'erreur (sorties des documents déjà traités conservées).
- **In scope** : révision du contrat CLI et de FR-001 (argumentaire
  positionnel multi-entrées, détection fichier/dossier, refus des options
  inapplicables avec message explicite), traitement séquentiel par document
  sans changement du chemin de nettoyage, mise à jour de la suite de tests
  (parité octet par octet lot vs individuel, refus des options, dossier
  sans `.md`), documentation README.
- **Out of scope** (concept.md + problem.md) : scan récursif (non récursif
  par défaut, open question si révision), résumé de lot, dossier de run
  dédié au lot, codes retour d'échec partiel, continue-on-error, dry-run
  et suggestion en lot, globs et fichiers d'ignore, paramètres par
  document, parallélisme, modification des règles de nettoyage, plafond
  du nombre de documents (proposé : aucun par défaut).
- **Success metrics** : (1) K documents en 1 invocation au lieu de K
  (baseline K=3) ; (2) parité octet par octet sur les 3 exemples de
  référence entre lot et invocation individuelle ; (3) aucune différence
  d'effet des options applicables entre lot et individuel ; (4) refus
  explicite (jamais silencieux) des options inapplicables.
- **Carried-forward open questions**:

  - [NEEDS CLARIFICATION: sémantique exacte du refus de
    `--dry-run`/`--suggestion` en lot — erreur d'usage (code 3) vs
    avertissement + neutralisation]
  - [NEEDS CLARIFICATION: mélange fichiers + dossiers dans une même
    invocation — autorisé ou usage invalide]
  - [NEEDS CLARIFICATION: dossier ne contenant aucun `.md` (ou seulement
    des sous-dossiers) — erreur avec code retour 1, ou entrée simplement
    ignorée]
  - [NEEDS CLARIFICATION: doublons dans le lot et ordre de traitement
    (ordre d'apparition vs tri par nom comme `--echantillon`)]
  - [NEEDS CLARIFICATION: message console en lot — une ligne de sortie par
    document au format actuel, sans résumé]
  - [NEEDS CLARIFICATION: validation de l'assumption fail-fast (sorties
    conservées) auprès de l'utilisateur]
  - [NEEDS CLARIFICATION: confirmation que `--pagine`, `--conserver-liens`
    , `--seuil`, `--calibrage`, `--extrait`, `--nom-titre`, `--sortie`,
    `--echantillon` restent applicables document par document sans
    changement d'effet (`--nom-titre` à examiner : un titre par document)]
