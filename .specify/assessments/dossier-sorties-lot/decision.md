# Decision: Un dossier de run par invocation, N sorties dedans

- **Slug**: dossier-sorties-lot
- **Decided**: 2026-10-05
- **Verdict**: go
- **Artifacts reviewed**: intake.md | research.md | problem.md | concept.md
- **User validation**: option A confirmée explicitement à l'invocation
  de la décision

## Scorecard

- **Problem validity — strong** : friction explicite et formulée par
  le décideur le jour même de la livraison de la feature 007, défaut
  nommé par écrit avant la livraison par l'assessment multi-documents
  (« le lot n'est pas identifiable dans output/ »), reproduction
  triviale et certaine du comportement gênant (intake addendum,
  research.md).
- **Evidence strength — strong** : tout est mesuré ou cité — lecture
  directe du code post-007 (`creer_dossier_run` par document,
  `md_cleaner/cli.py:213` ; noms fixes des secondaires), mécanismes
  anti-collision vérifiés (`resoudre_chemin_nettoye`), conventions
  externes documentées (tsc `outDir`, Dart Sass many-to-many), coût de
  migration quantifié (~9 assertions, 2 contrats, README). Seule zone
  soft : la demande émane du seul utilisateur — non décisive, il est
  le décideur.
- **Value vs. inaction — strong** : l'inaction conserve un défaut
  nominal, prédit et pré-corrigé (« extension sans regret ») sur la
  capacité livrée ce jour comme valeur d'usage ; le repérage manuel
  des lots est cassé par toute invocation intercalée.
- **Feasibility / appetite — strong** : appetite small, tout est en
  place : déplacement d'une création de dossier dans `main()`,
  préfixage conditionnel des sorties secondaires, stdlib seule ; le
  coût est une migration bornée de tests et de contrats, pas de
  l'invention (concept.md A).
- **Strategic fit — strong** : le changement simplifie le contrat
  (« un run = une invocation »), n'ajoute aucune option, respecte la
  constitution IV ; la forme est alignée sur les standards tsc/Sass
  (un dossier de sortie par invocation, fichiers nommés d'après
  l'entrée).
- **Risk posture — adequate** : risques identifiés et bornés :
  divergence de nommage des secondaires entre mono et lot (assumption
  à valider), arbitrage `--nom-titre` (deux variantes, tranchable en
  clarification), migration de tests/contrats (bornée, précédent 006).
  Aucun risque non mitigué identifié.

## Verdict & Rationale

**Go.** Aucun critère sous adequate, et la particularité de ce cas est
que la correction a été conçue avant le problème vécu : l'assessment
multi-documents avait documenté le défaut du lot invisible et pré-rédigé
la solution (option B d'alors = option A d'aujourd'hui), la qualifiant
d'extension sans regret. L'utilisateur a tranché la forme (sorties à
plat dans un seul `00X`, pas de sous-dossiers), ce qui écarte la
variante structurellement plus élégante pour le nommage mais contraire à
la demande explicite. Le score reflète une décision à faible risque
technique : les mécanismes existent, la rétrocompatibilité
mono-document est structurellement gratuite, et le seul vrai arbitrage
restant (`--nom-titre` en lot, forme du préfixage des secondaires) est
une question de spécification, pas d'opportunité.

## If go — Handoff to `/speckit-specify`

- **Problem** : les sorties d'une invocation multi-documents sont
  éparpillées dans autant de sous-dossiers de `output/` qu'il y a de
  documents — le lot n'est pas identifiable, la numérotation se
  consomme au rythme des documents (problem.md).
- **Chosen approach** : Option A du concept.md — un dossier de run
  par invocation (créé une fois avant la boucle de traitement,
  numérotation séquentielle inchangée à la racine `--sortie`),
  contenant les N sorties `<stem>-nettoye.md` à plat, anti-collision
  existant pour les stems identiques ; sorties secondaires `--pagine`
  préfixées par le stem en lot de plusieurs
  (`<stem>-nettoye-pagine.md`, `<stem>-cartographie.json`) ;
  mono-document strictement inchangé ; pas de résumé, pas de marqueur
  de lot incomplet.
- **In scope** : déplacement de la création du dossier de run dans le
  flux d'invocation, préfixage conditionnel des sorties secondaires,
  migration des ~9 assertions de `tests/integration/test_lot.py`,
  révision des contrats (007 FR-003/FR-011, table des artefacts de
  001) et du README, mise à jour de la suite de tests sans
  relâchement.
- **Out of scope** (concept.md) : résumé de lot, reprise de lot,
  marqueur « lot incomplet », renommage des secondaires du
  mono-document, sous-dossiers par document, nouvelle option CLI,
  contenu des sorties, résolution du lot et sémantique d'échec (007).
- **Success metrics** : (1) 1 invocation de K documents → 1 dossier
  de run contenant K sorties nettoyées ; (2) stems identiques →
  sorties distinctes, jamais d'écrasement ; (3) mono-document
  strictement inchangé (suite existante au vert) ; (4) secondaires
  attribuables par document dans le dossier partagé ; (5) un numéro
  séquentiel consommé par invocation.
- **Carried-forward open questions**:
  - [NEEDS CLARIFICATION: `--nom-titre` en lot de plusieurs —
    neutralisé avec avertissement (variante recommandée du concept,
    par symétrie avec 007), ou nommage d'après le premier document ?]
  - [NEEDS CLARIFICATION: préfixage des secondaires —
    `<stem>-nettoye-pagine.md` / `<stem>-cartographie.json` en lot de
    plusieurs seulement (divergence assumée avec le mono-document), à
    confirmer]
  - [NEEDS CLARIFICATION: lot d'un seul document — confirmation que la
    structure actuelle vaut (le regroupement ne change rien
    d'observable pour lui)]
  - [NEEDS CLARIFICATION: échec partiel — confirmation qu'aucun
    marquage spécifique n'est attendu (sorties réussies conservées,
    code 1, trace stderr)]
  - [NEEDS CLARIFICATION: ordre des sorties dans le dossier partagé —
    ordre de traitement déterministe (007) retenu comme contrat]
