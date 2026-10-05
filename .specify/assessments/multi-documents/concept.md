# Concept: Invocation multi-entrées — un lot, un traitement par document

- **Slug**: multi-documents
- **Created**: 2026-10-05
- **Recommended option**: A — Lot positionnel minimal (un run par document)

## Options

### Option A — Lot positionnel minimal (un run par document)

- **Sketch** : la ligne de commande accepte plusieurs entrées à la suite
  (`md-cleaner doc1.md doc2.md dossierA`), chaque entrée étant un fichier
  `.md` ou un dossier (dans ce cas, seuls les `.md` du premier niveau sont
  retenus, comme le fait déjà `--echantillon`). L'outil traite les
  documents un par un, exactement comme aujourd'hui : chaque document
  obtient son propre dossier de run (numérotation séquentielle existante)
  et ses sorties habituelles. Les options de cleaning s'appliquent telles
  quelles à chacun. Les capacités non applicables à un lot (dry-run,
  suggestion — liées par construction à un document unique) sont refusées
  explicitement, jamais ignorées en silence. En cas d'erreur sur un
  document, le lot s'arrête net (fail-fast) ; les documents déjà traités
  conservent leurs sorties.
- **Appetite**: small
- **Trade-offs** : gagne — une seule invocation pour tout le corpus,
  parité octet par octet garantie par construction (chaque document suit le
  chemin de code existant), réutilisation intégrale du nommage et des
  dossiers de run, révision du contrat limitée à l'argumentaire positionnel
  et au refus des options inapplicables. Sacrifie — le lot n'est pas
  identifiable dans `output/` (N dossiers de run consécutifs
  indiscernables de N invocations manuelles), pas de résumé de fin de lot,
  fail-fast laisse un lot à moitié traité en cas d'erreur en milieu de
  liste. Risque : ambiguïté pour l'utilisateur qui cherche « les sorties de
  mon lot d'hier ».
- **Rabbit holes** : vouloir « quand même » un résumé console par document
  (glissement vers B) ; vouloir rattraper les erreurs (continue-on-error,
  codes retour composites — glissement vers B) ; récursivité du dossier
  (pandore ouverte par la structure d'`Examples/`, déjà identifiée en open
  question).

### Option B — Lot avec visibilité de lot

- **Sketch** : même surface d'entrée que A (fichiers et dossiers, `.md`
  seuls, non récursif), mais le lot devient une entité visible : un dossier
  de run unique pour tout le lot contenant les N sorties nettoyées (le
  nommage dérivé par document, déjà en place depuis 006, désambiguïse sans
  écrasement), une ligne de sortie console par document puis un résumé (N
  traités, K en erreur), et une sémantique d'échec partiel : on continue
  après un document en erreur et le code retour distingue succès total /
  succès partiel / échec. Les options inapplicables sont signalées
  explicitement (forme exacte — erreur ou avertissement — à trancher en
  spécification).
- **Appetite**: small à medium (la frontière se joue sur la sémantique
  d'échec partiel)
- **Trade-offs** : gagne — le lot est identifiable et auditable dans
  `output/`, l'utilisateur sait immédiatement quoi relancer, cohérent avec
  la convention des linters (résultats par fichier + résumé, cf.
  markdownlint-cli2). Sacrifie — révision plus large du contrat CLI :
  structure des dossiers de run en lot, codes retour étendus (le contrat
  actuel ne connaît que tout-ou-rien), migration de la suite de tests,
  interaction avec `--nom-titre` (lequel titre pour un lot ?). Risque : la
  structure « un run = un document » est un invariant des six features
  livrées ; la casser déplace beaucoup de tests.
- **Rabbit holes** : codes retour composites (bitmask, récapitulatif
  JSON...) ; reprise de lot (« reprendre où ça a échoué ») ; résumés
  riches ; structure de sous-dossiers par document dans le run de lot.

### Option C — Faire confiance au shell (recette documentée, pas de code)

- **Sketch** : aucun changement d'outil ; le README documente une recette
  PowerShell de boucle sur les fichiers d'un dossier
  (`Get-ChildItem *.md | ForEach-Object { md-cleaner $_.FullName }`), avec
  l'avertissement d'utiliser les mêmes options d'une itération à l'autre.
- **Appetite**: small (une demi-journée de doc)
- **Trade-offs** : gagne — zéro risque de contrat, zéro code, conforme au
  principe IV en apparence. Sacrifie — l'objectif « une seule expression
  des paramètres » n'est pas garanti (la boucle réécrit les options à
  chaque itération, la cohérence repose sur la discipline de
  l'utilisateur), l'invocation multiple reste la réalité, la découverte
  est faible (une recette enterrée dans le README). C'est le statu quo
  embellie, pas une réponse au problème.
- **Rabbit holes** : aucun technique ; le rabbit hole est l'acceptation
  durable d'un problème documenté mais non résolu.

## Recommendation

**Option A.** Elle est la seule qui serve les quatre objectifs du
problem.md (une invocation, N sorties, une seule expression des
paramètres, dossier accepté en entrée) en touchant le moins de contrat :
chaque document conserve le chemin de code et la parité octet par octet est
garantie par construction — la métrique de parité devient quasi
tautologique, ce qui est exactement ce qu'on veut d'un appetite small sur
une demande de commodité portée par un seul utilisateur (research.md :
Evidence Against). Les options inapplicables sont refusées explicitement
(métrique qualitative du problem.md), conformément à l'arbitrage de
l'intake. Le défaut d'A — le lot invisible dans `output/` — est réel mais
proportionné : il peut être comblé plus tard par B si la friction se
matérialise, sans regret d'architecture (B enchâsse A). C'est aussi
l'option la plus fidèle au principe IV de la constitution : la plus petite
extension du point d'entrée qui résolve le problème. C est rejetée parce
qu'elle ne garantit pas la cohérence des paramètres, qui est le cœur du
problème, pas la commodité brute. B est légitime mais prématurée : sa
valeur (auditabilité du lot) n'est étayée par aucune friction observée, et
elle paie en invariant cassé (« un run = un document »).

## Out of Scope (pour l'option recommandée)

- Scan récursif des dossiers (le dossier cible ses `.md` de premier
  niveau ; la récursivité reste une open question de spécification,
  motivée par la structure d'`Examples/`).
- Résumé de lot, dossier de run dédié au lot, codes retour d'échec
  partiel (territoire de B, reporté).
- Continue-on-error : fail-fast assumé.
- Dry-run et suggestion en lot (refusés, conformément à l'arbitrage de
  l'intake ; la boucle de jugement reste mono-document).
- Motifs glob (`*.md`) et fichiers d'ignore (`.mdcleanerignore`) : le
  shell et le dossier suffisent à l'appetite small.
- Paramètres de cleaning différents par document, parallélisme,
  modification des règles de nettoyage (non-goals du problem.md).
- Plafond explicite du nombre de documents du lot (à trancher en
  spécification ; aucun plafond proposé par défaut).

## Assumptions to Validate

- Le scan non récursif de premier niveau suffit aux usages réels
  (assumption fondée sur le précédent `--echantillon` et la structure
  d'`Examples/` ; à valider avec l'utilisateur en spécification).
- Le refus explicite de `--dry-run`/`--suggestion` en lot est bien
  l'arbitrage voulu (l'intake dit « ignorées » ; le problem.md exige «
  non silencieux » ; la forme exacte — erreur d'usage vs avertissement —
  reste à trancher).
- Mélanger fichiers et dossiers dans une même invocation est acceptable
  (sinon : usage invalide, code 3).
- Le fail-fast avec sorties conservées des documents déjà traités est un
  comportement acceptable pour l'utilisateur.
- Les corpus réels restent de taille modeste (quelques documents) : pas de
  plafond, pas de préoccupation de performance.
- La parité octet par octet est vérifiable automatiquement sur les 3
  exemples de référence (métrique du problem.md).
