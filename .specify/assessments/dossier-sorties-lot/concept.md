# Concept: Un dossier de run par invocation, N sorties dedans

- **Slug**: dossier-sorties-lot
- **Created**: 2026-10-05
- **Recommended option**: A — Dossier de run par invocation (sorties à
  plat)

## Options

### Option A — Dossier de run par invocation (sorties à plat)

- **Sketch** : une invocation = un dossier de run numéroté (`00X`),
  quel que soit le nombre de documents ; les N sorties nettoyées
  (`<stem>-nettoye.md`) y vivent côte à côte, l'anti-collision
  existant (`-1`, `-2`) couvrant les stems identiques. Le dossier est
  créé une fois avant la boucle de traitement et passé à chaque
  document. En lot de plusieurs, les sorties secondaires de
  `--pagine` sont préfixées par le stem (`<stem>-nettoye-pagine.md`,
  `<stem>-cartographie.json`) pour rester attribuables ; le
  mono-document garde ses noms courts actuels. `--nom-titre` est
  neutralisé en lot de plusieurs (avertissement, numérotation seule) —
  ou, variante à trancher, nomme le dossier d'après le premier
  document. Un lot incomplet (échec partiel) contient simplement les
  sorties des documents réussis, sans marqueur.
- **Appetite**: small
- **Trade-offs** : gagne — exactement la forme demandée (addendum de
  l'intake : « un seul 00X avec mes deux outputs »), alignée sur les
  conventions tsc/Sass (un dossier de sortie par invocation, fichiers
  nommés d'après l'entrée) ; rétrocompatibilité mono-document
  structurellement gratuite ; mécanismes tous en place (aucune
  nouvelle dépendance, stdlib). Sacrifie — une divergence de nommage
  des sorties secondaires entre mono (noms courts) et lot (préfixés) ;
  migration bornée mais réelle (~9 assertions de test, contrats 007
  et 001, README). Risque : la divergence de nommage surprend en
  lisant le contrat.
- **Rabbit holes** : unifier les noms secondaires partout (re-touche
  au mono-document et à ses tests — glissement) ; marquage « lot
  incomplet » (fichier marqueur, récapitulatif — glissement vers le
  résumé de B) ; arbitrage `--nom-titre` (titre du premier document,
  puis du deuxième si échec ?).

### Option B — Dossier de lot contenant un sous-dossier par document

- **Sketch** : une invocation crée un dossier de lot `00X` contenant
  un sous-dossier par document, chacun avec ses sorties au format
  actuel (noms courts, artefacts confondus). L'attribution des
  sorties secondaires est parfaite sans aucun renommage, et la
  structure mono/multi devient uniforme.
- **Appetite**: small à medium
- **Trade-offs** : gagne — zéro problème de nommage (chaque document
  garde son espace), structure mono/multi identique, migration de
  tests plus légère. Sacrifie — la forme explicitement rejetée par
  l'utilisateur dans l'addendum de l'intake (« Je ne veux qu'un seul
  00X avec mes deux outputs » : les fichiers nettoyés ne sont pas
  directement visibles dans `00X`) ; une arborescence plus profonde ;
  la numérotation des sous-dossiers par document restaure une
  micro-version du problème initial (compter pour s'y retrouver).
- **Rabbit holes** : numérotation ou nommage des sous-dossiers par
  document (slug du titre ? ordre ?) ; interface avec `--nom-titre`
  à deux niveaux (nom du lot ET du sous-dossier).

### Option C — Statu quo documenté (rien ne change)

- **Sketch** : aucun changement d'outil ; le README documente que les
  sorties d'un lot occupent les numéros consécutifs suivants et
  comment les repérer (l'ordre d'apparition des `Sortie : ...` en
  console).
- **Appetite**: small (quelques lignes de doc)
- **Trade-offs** : gagne — zéro code, zéro migration. Sacrifie — la
  demande explicite du décideur reste insatisfaite ; le repérage à la
  main reste cassé par toute invocation intercalée ; la prédiction de
  l'assessment multi-documents (« extension sans regret ») reste en
  attente. C'est la conservation d'un défaut connu et nommé.
- **Rabbit holes** : aucun technique.

## Recommendation

**Option A.** C'est la seule qui réponde à la forme précisée par
l'utilisateur (« un seul 00X avec mes deux outputs ») tout en
respectant les objectifs du problem.md : un dossier par invocation,
sorties attribuables, mono-document inchangé, numérotation par
invocation. Tous les mécanismes existent (research.md : Prior Art
interne) — le coût réel est la migration bornée des tests et contrats,
pas de l'invention. B résout le nommage des secondaires plus
élégamment mais impose la forme que l'utilisateur vient d'écarter, et
réintroduit une navigation par sous-dossiers. C est rejetée : le
problème est nominal, prédit, et sa correction prédéfinie. L'appetite
est small : un déplacement de création de dossier, un préfixage
conditionnel, des tests et contrats à mettre à jour.

## Out of Scope (pour l'option recommandée)

- Résumé de fin de lot, reprise de lot, codes retour d'échec partiel
  nouveaux, fichier marqueur « lot incomplet » (le reste de l'option
  B de l'assessment multi-documents).
- Renommage des sorties secondaires du mono-document (les noms courts
  `nettoye-pagine.md` / `cartographie.json` restent la règle en lot
  d'un document).
- Contenu des sorties, règles de nettoyage, résolution du lot,
  neutralisation des options, sémantique d'échec (007 livré et testé).
- Sous-dossiers par document dans le dossier de lot (forme B).
- Nouvelle option CLI (le regroupement est le comportement par défaut,
  sans drapeau).

## Assumptions to Validate

- Les sorties secondaires d'un lot de plusieurs sont préfixées par le
  stem (`<stem>-nettoye-pagine.md`, `<stem>-cartographie.json`),
  règle appliquée au seul lot de plusieurs ; le mono-document garde
  les noms courts actuels (divergence assumée).
- `--nom-titre` en lot de plusieurs est neutralisé avec avertissement
  (numérotation seule), par symétrie avec la neutralisation 007 de
  `--dry-run`/`--suggestion` — variante « titre du premier document »
  à écarter ou retenir en clarification.
- Le lot d'un seul document garde la structure actuelle (le
  regroupement ne s'applique qu'aux lots de plusieurs — ou,
  équivalent observable, il s'applique à tous les lots puisque la
  structure mono est déjà la cible).
- Aucun marquage de lot incomplet : les sorties réussies sont
  conservées, le code retour 1 et la trace stderr documentent l'échec.
- Les ~9 assertions de tests de `test_lot.py` et les contrats (007
  FR-003/FR-011, table 001, README) sont migrés dans la même
  livraison, comme l'a fait 006 pour ses changements de contrat.
