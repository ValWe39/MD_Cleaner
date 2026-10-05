# Idea Research: Un dossier de sorties partagé pour les documents d'un même lot

- **Slug**: dossier-sorties-lot
- **Created**: 2026-10-05
- **Evidence confidence (overall)**: high

## Users & Demand

- Le porteur de la demande est l'utilisateur-décideur, auteur de
  l'addendum : « Je ne veux qu'un seul 00X avec mes deux outputs » —
  friction formulée le jour même de la livraison de la feature 007
  (commit `5c906b9`), sur son propre flux d'usage — [source:
  intake.md] (confidence: high).
- La friction était documentée avant même la livraison :
  l'assessment `multi-documents` avait nommé ce défaut (« le lot n'est
  pas identifiable dans `output/` : N dossiers de run consécutifs
  indiscernables de N invocations manuelles ») et qualifié la
  correction d'« extension sans regret » (option B du concept.md,
  reportée par la décision du 2026-10-05) — [source:
  `.specify/assessments/multi-documents/concept.md` (option B),
  decision.md] (confidence: high, cité).
- La demande est déclarée, pas encore mesurée sur artefacts (aucun run
  de lot réel posant problème n'est cité) ; mais le mécanisme
  reproductible est trivial : `md-cleaner doc1.md doc2.md` →
  `output/001` + `output/002` au lieu d'un dossier unique —
  [ASSUMPTION : reproduction directe du code ci-dessous] (confidence:
  high).

## Prior Art

### Interne

- **Mécanisme actuel** : `_traiter_document` appelle
  `creer_dossier_run(args.sortie, titre, args.nom_titre)` pour chaque
  document (`md_cleaner/cli.py:213`), et `creer_dossier_run`
  (`md_cleaner/sortie.py`) crée un sous-dossier séquentiel (001, 002,
  ...) ou nommé d'après le titre — d'où N dossiers pour un lot de N.
  Le câblage pour un dossier partagé est local : créer le dossier de
  run une fois dans `main()` avant la boucle et le passer à chaque
  document — [source: md_cleaner/cli.py, md_cleaner/sortie.py]
  (confidence: high, cité).
- **Nommage anti-collision déjà en place** : depuis 006, la sortie est
  `<stem>-nettoye.md` avec suffixe `-1`, `-2` en cas de collision via
  `resoudre_chemin_nettoye` (`md_cleaner/sortie.py`), garanti sans
  écrasement. Dans un dossier partagé, deux stems identiques (ex. les
  `consolidated.md` d'Exemple_1 et Exemple_2) donneraient
  `consolidated-nettoye.md` + `consolidated-nettoye-1.md` — le
  mécanisme couvre déjà ce cas à l'échelle du dossier, sans nouveau
  code — [source: md_cleaner/sortie.py, specs/006-nom-sortie-source]
  (confidence: high, cité).
- **Point dur identifié : sorties secondaires à nom fixe** — avec
  `--pagine`, chaque document produit `nettoye-pagine.md` et
  `cartographie.json` à noms constants (`md_cleaner/cli.py:232-239`) ;
  dans un dossier partagé, N documents s'écraseraient mutuellement ces
  fichiers. Un mécanisme de nommage dérivé du document (ex.
  `<stem>-nettoye-pagine.md`, `<stem>-cartographie.json`) est
  nécessaire — cohérent avec la philosophie de 006 (noms dérivés de
  l'entrée) ; les artefacts du dry-run (`rapport-dry-run.md`,
  `suggestion.json`) ne sont produits qu'en lot d'un document
  (neutralisés en lot de plusieurs par 007) et ne sont pas affectés —
  [source: md_cleaner/cli.py, contracts 007/multi-entrees.md]
  (confidence: high, cité).
- **Contrats et tests touchés** : la spec 007 pose « un dossier de run
  par document » (FR-003) et « un run par document » (FR-011 du
  contrat multi-entrees) — cette idée révisera ces deux clauses pour
  le lot de plusieurs ; ~9 assertions de tests d'intégration
  `test_lot.py` codent en dur les dossiers 001/002 par document et
  devront être migrées ; le README (section « Traiter plusieurs
  documents ») et le contrat 001 (table des fichiers produits)
  devront suivre — [source: specs/007-traitement-multi-documents,
  tests/integration/test_lot.py, README.md] (confidence: high, cité).
- **Rétrocompatibilité mono-document gratuite** : la structure visée
  (un dossier de run contenant `<stem>-nettoye.md`) est déjà
  exactement celle du mono-document aujourd'hui — le cas « lot d'un
  document » ne change pas de forme, seul le lot de plusieurs se
  regroupe — [source: observation du comportement actuel] (confidence:
  high, cité).

### Externe (conventions de sortie par lot)

- **TypeScript (`tsc --outDir`)** : une invocation écrit tous les
  fichiers compilés dans un seul répertoire de sortie, en préservant
  la structure et les noms dérivés des entrées (« TypeScript will
  never write an output file to a directory outside of outDir, and
  will never skip emitting a file ») — [source:
  <https://www.typescriptlang.org/tsconfig/#outDir> (host:
  typescriptlang.org, via résultats web_search)] (confidence: high,
  cité). Précédent du « un dossier de sortie par invocation, fichiers
  nommés d'après l'entrée ».
- **Dart Sass (mode many-to-many)** : la compilation d'un dossier
  entier produit un arbre de sortie unique où chaque fichier de
  sortie porte le nom de son fichier d'entrée (un `output.css` par
  `input.scss`, la collision étant impossible par construction) —
  [source: <https://sass-lang.com/documentation/cli/dart-sass/>
  (host: sass-lang.com, via résultats web_search)] (confidence:
  medium, cité). Renforce la convention : noms dérivés de l'entrée
  dans un dossier partagé, plutôt que noms fixes.
- **Aucun des précédents externes examinés ne produit un sous-dossier
  par fichier d'entrée dans une même invocation** ; les sous-dossiers
  reflètent au besoin la hiérarchie des entrées, jamais l'itération —
  [source: synthèse tsc/sass + assessment multi-documents (prettier,
  mdformat)] (confidence: medium, ASSUMPTION d'exhaustivité : deux
  outils examinés pour ce point précis).

## Market & Context

- Alternative actuelle : repérer « à la main » les N dossiers
  consécutifs créés par un lot (en comptant les numéros), ou
  re-lister les `Sortie : ...` affichés en console — fragile et
  cassé dès qu'une autre invocation s'intercale — [source:
  observation du comportement] (confidence: high).
- Coût de l'inaction : la confusion entre « les sorties de mon lot »
  et « N invocations séparées » persiste sur chaque lot, tandis que
  la numérotation séquentielle consomme N numéros par lot — [source:
  observation] (confidence: medium).

## Data & Constraints

- Mécanismes disponibles sans nouvelle dépendance :
  `creer_dossier_run` (numérotation/slug), `resoudre_chemin_nettoye`
  (anti-collision), `nom_sortie_nettoye` (nommage 006),
  `slug_titre` (normalisation) — tout est stdlib et en place —
  [source: md_cleaner/sortie.py, normalisation.py] (confidence: high).
- Constitution IV (simplicité) : le changement est un déplacement de
  la création du dossier de run (une ligne dans `main()`), un
  préfixage des sorties secondaires paginées, et la migration des
  tests/contrats — aucune nouvelle option CLI n'est requise ; le
  principe « un run = une invocation » simplifie même le contrat
  (réciproque du « un run par document » de 007) — [source:
  constitution.md] (confidence: high).
- `--nom-titre` en lot de plusieurs : aujourd'hui appliqué par
  document (chaque document nomme son run d'après son propre titre) ;
  avec un dossier partagé, un seul nom est possible — conflit ouvert
  (premier document ? neutralisation en lot ? numérotation seule ?) —
  [source: md_cleaner/cli.py, contrat 007] (confidence: high, cité,
  à trancher en spécification).
- Échec partiel : le dossier de lot contiendrait les sorties des
  seuls documents réussis ; le code retour (1) et les messages
  stderr tracent déjà l'échec ; un marquage « lot incomplet » serait
  une nouveauté de contrat à arbitrer (par défaut : aucun marquage,
  l'information existe dans la trace console) — [ASSUMPTION]
  (confidence: medium).

## Evidence Against the Idea

- **Coût de migration observable** : ~9 assertions de test codent la
  structure actuelle, deux contrats (007 multi-entrees FR-003/FR-011,
  001 table des artefacts) et le README décrivent « un dossier par
  document » — le changement n'est pas gratuit côté documentation et
  tests — [source: tests, contracts] (confidence: high).
- **Complexification des sorties secondaires** : le préfixage
  `<stem>-nettoye-pagine.md` / `<stem>-cartographie.json` rompt la
  symétrie avec le mono-document (où les noms restent courts) ou
  impose une règle à deux formes — divergence de contrat à assumer —
  [source: md_cleaner/cli.py] (confidence: medium).
- **Perte d'information du run par document** : aujourd'hui, le
  dossier de run isole aussi les avertissements et artefacts d'un
  document ; dans un dossier partagé, un œil humain ne peut plus
  associer un artefact secondaire à son document que par son préfixe
  — coût cognitif faible mais réel — [ASSUMPTION] (confidence:
  low).
- Contre-argument dominant : la demande vient du décideur unique, le
  mécanisme existe, la rétrocompatibilité mono-document est
  structurellement gratuite, et la correction avait été prédite
  comme « extension sans regret » avant la livraison — [source:
  intake, decision.md multi-documents] (confidence: high).

## Gaps & Open Questions

- [NEEDS CLARIFICATION: `--nom-titre` en lot de plusieurs — nom du
  dossier partagé : titre du premier document, neutralisation en lot
  (numérotation seule), ou refus ?]
- [NEEDS CLARIFICATION: forme exacte du nommage des sorties
  secondaires partagées — `<stem>-nettoye-pagine.md` et
  `<stem>-cartographie.json` (aligné sur 006), ou autre ?]
- [NEEDS CLARIFICATION: marquage d'un lot incomplet (échec partiel) —
  aucun par défaut (trace console + code 1), ou fichier marqueur ?]
- [NEEDS CLARIFICATION: le lot d'un seul document garde-t-il
  strictement la structure actuelle (cas déjà conforme), le
  changement ne s'appliquant qu'aux lots de plusieurs ?]
- [NEEDS CLARIFICATION: ordre des sorties dans le dossier partagé —
  ordre de traitement (déjà déterministe par 007), à confirmer comme
  contrat.]

## Sources

- <https://www.typescriptlang.org/tsconfig/> (host:
  typescriptlang.org, policy: hors liste de confiance pour fetch —
  consulté via résultats du connecteur web_search, extraits cités
  sans fetch direct)
- <https://sass-lang.com/documentation/cli/dart-sass/> (host:
  sass-lang.com, policy: idem)
- Sources internes (lecture directe du dépôt, 2026-10-05, état post-007
  commit `5c906b9`) : `md_cleaner/cli.py`, `md_cleaner/sortie.py`,
  `md_cleaner/normalisation.py`,
  `tests/integration/test_lot.py`, `README.md`,
  `specs/007-traitement-multi-documents/` (spec, contracts,
  tasks), `specs/001-nettoyage-md-repetitif/contracts/cli.md`,
  `specs/006-nom-sortie-source/`,
  `.specify/assessments/multi-documents/` (intake, research, problem,
  concept, decision), `.specify/assessments/dossier-sorties-lot/intake.md`
