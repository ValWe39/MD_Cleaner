# Decision: Nommer la sortie nettoyée d'après le document source

- **Slug**: nom-sortie-nettoye
- **Decided**: 2026-10-05
- **Verdict**: go
- **Artifacts reviewed**: intake.md | research.md absent | problem.md |
  concept.md

## Scorecard

- **Problem validity** (strong) : Friction réelle exprimée par le seul
  utilisateur de l'outil, propriétaire du dépôt ; chaque run produit un
  `nettoye.md` indissociable des autres (vérifié dans `md_cleaner/cli.py`).
- **Evidence strength** (adequate) : Pas de `research.md`, mais preuves directes
  : demande utilisateur verbatim (intake), comportement actuel observé dans le
  code (`cli.py`, `sortie.py`, `normalisation.py:37`), exemple concret
  d'entrée/sortie fourni. Aucune supposition structurante non documentée.
- **Value vs. inaction** (strong) : Le coût de l'inaction croît avec chaque
  document traité (renommage manuel récurrent, risque de confusion) ; le coût de
  la solution est faible (appetite small).
- **Feasibility / appetite** (strong) : Option A crédible et bornée : renommage
  d'un seul artefact, une règle de nommage simple, collision tranchée par
  décision utilisateur (`-1` par ordre de traitement).
- **Strategic fit** (strong) : Cohérent avec l'outil CLI mono-fichier (FR-001)
  et avec le nommage existant (`--nom-titre`, slug du titre) ; pas de
  contradiction avec les non-goals du projet.
- **Risk posture** (adequate) : Risques identifiés au concept : normalisation
  des caractères non espace, troncature à 20 caractères, interplay avec
  `--nom-titre`, mise à jour des tests attendus sur `nettoye.md`. Aucun risque
  bloquant ; tous se tranchent en spécification.

## Verdict & Rationale

**Go.** Le problème est réel et directement attesté, la solution retenue (option
A, confirmée par l'utilisateur) est la plus petite qui le résout, et les risques
restants sont des décisions de spécification et non des incertitudes de
faisabilité. L'absence de `research.md` est compensée par des preuves directes
(code et demande utilisateur) ; pour un changement de nommage d'artefact dans un
outil CLI mono-utilisateur, un stage de recherche supplémentaire n'apporterait
rien.

## If go — Handoff to `/speckit-specify`

- **Problem**: les sorties nettoyées (`nettoye.md`) sont indissociables de leur
  document source par leur nom ; l'utilisateur veut reconnaître la source dans
  le nom du fichier.
- **Chosen approach**: Option A — renommer le fichier nettoyé en
  `<nom-dérivé-de-l'entrée>-nettoye.md` : 20 premiers caractères du nom de
  l'entrée, espaces → `_`, suffixe `-nettoye` ; collision → suffixe numérique
  `-1` par ordre de traitement (décision utilisateur du 2026-10-05).
- **In scope / out of scope**: en périmètre, le nom du fichier nettoyé
  uniquement. Hors périmètre : les autres artefacts (`nettoye-pagine.md`,
  `cartographie.json`, `suggestion.json`, `rapport-dry-run.md`), le nommage des
  dossiers de run (`--nom-titre`, numérotation), le multi-documents, le
  rétro-nommage de `output/` existant.
- **Success metrics**: sur un lot de documents aux noms distincts, chaque sortie
  nettoyée porte un nom unique dérivé de sa source (baseline : toutes
  s'appellent `nettoye.md`).
- **Carried-forward open questions**:
  - « Titre d'input » = stem du fichier (présumé, cf. exemple
    `retry-failed-records.md`) ou premier titre `#` ?
  - Troncature à 20 caractères : brute ou au dernier mot entier ?
  - Caractères non espace (accents, ponctuation, séparateurs) : conservés ou
    normalisés ?
  - Comportement par défaut sans mode de repli — à confirmer en spécification.
  - Mise à jour des tests et de la documentation attendant `nettoye.md` — à
    inclure dans la livraison.
