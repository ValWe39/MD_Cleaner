# Idea Research: Traitement de plusieurs documents en une seule invocation

- **Slug**: multi-documents
- **Created**: 2026-10-05
- **Evidence confidence (overall)**: medium

## Users & Demand

- Un seul utilisateur porte la demande : le propriétaire du dépôt, auteur de
  l'idée — [source: intake.md, session du 2026-10-05 | ASSUMPTION sur
  l'absence d'autres utilisateurs : le projet n'a pas d'issue tracker actif
  ni de canaux de retour identifiés] (confidence: medium). Précédent
  interne : les assessments 004/005 ont déjà retenu qu'un unique porteur
  n'est pas décisif quand le problème est observé sur les artefacts
  (decision.md de nettoyage-liens-html, nettoyage-liens-url).
- Signal de besoin observable : le corpus d'exemples compte 3 documents
  d'entrée consolidés (`Examples/Exemple_1/2.Input/consolidated.md`,
  `Examples/Exemple_2/2.Input/consolidated.md`,
  `Examples/Exemple_3/2.Input/retry-failed-records.md`) et le workflow
  documenté du README traite un fichier par invocation — traiter plusieurs
  corpus impose aujourd'hui N invocations manuelles — [source: README.md,
  Examples/] (confidence: high, cité).
- Comportement observé vs déclaré : la demande est déclarée (« j'envisage
  »), sans friction mesurée (pas de script de boucle existant, pas
  d'historique d'exécutions multiples documentées) — [source: lecture du
  dépôt, aucune trace de contournement existant] (confidence: medium).

## Prior Art

### Interne

- **Contrat CLI actuel : « Un run = un fichier d'entrée » (FR-001)** —
  l'idée modifie directement ce contrat fondateur ;
  `specs/001-nettoyage-md-repetitif/contracts/cli.md` et `md_cleaner/cli.py`
  (argument positionnel unique `fichier`, refus explicite de tout ce qui
  n'est pas un fichier `.md` existant, code retour 1 sinon) — [source:
  specs/001-nettoyage-md-repetitif/contracts/cli.md, md_cleaner/cli.py]
  (confidence: high, cité). Toute implémentation devra réviser ce contrat
  et sa suite de tests.
- **Précédent de scan de dossier : `--echantillon` (FR-012)** — l'outil
  scanne déjà un dossier : `charger_echantillon`
  (`md_cleaner/detection.py:34`) filtre les `.md` par `iterdir()` (non
  récursif), trie par nom, plafonne à 5 fichiers, échoue si vide. C'est un
  précédent direct pour la règle « dossier → seuls les .md, ignorés sinon
  » et suggère une lecture non récursive — [source:
  md_cleaner/detection.py] (confidence: high, cité).
- **Suggestion liée au document source** — `suggestion.json` porte un
  champ `source` validé strictement contre le nom du fichier d'entrée
  (`lire_suggestion(args.suggestion, fichier.name)` dans
  `md_cleaner/cli.py`) : une suggestion n'est par construction valide que
  pour un seul document. Cela fonde l'arbitrage de l'intake (« suggestion
  ignorée en multi-docs ») comme contrainte technique, pas seulement
  préférence — [source: md_cleaner/cli.py, suggestion.py] (confidence:
  high, cité).
- **Nommage des runs et des sorties conçu pour un document** —
  `creer_dossier_run` (`md_cleaner/sortie.py`) crée un sous-dossier
  séquentiel (001, 002...) ou nommé d'après le titre (`--nom-titre`) par
  run ; depuis la feature 006, le fichier nettoyé est nommé d'après le stem
  de l'entrée avec résolution de collision `-1`, `-2`. Un lot de N
  documents devra arbitrer : un dossier de run pour tout le lot, ou un
  sous-dossier par document ; les collisions de noms (deux stems tronqués
  identiques à 20 caractères) sont déjà couvertes par le mécanisme de
  suffixe — [source: md_cleaner/sortie.py,
  specs/006-nom-sortie-source] (confidence: high, cité).
- **Dry-run existant par document** — `--dry-run` produit
  `rapport-dry-run.md` + `suggestion.json` dans le dossier du run, sans
  sortie nettoyée ; rien dans le code ne le rend structurellement
  mono-document, mais son rôle est de nourrir la boucle
  éditer-suggestion-relancer qui est, elle, par nature mono-document —
  [source: contracts/cli.md, md_cleaner/cli.py] (confidence: high, cité).

### Externe (conventions des CLI Markdown batch)

- **prettier** — résolution native multi-chemins : un chemin fichier
  existant est traité tel quel ; un chemin dossier existant déclenche une
  recherche **récursive** des fichiers supportés ; les arguments
  acceptent aussi des globs, et le mode `--check`/`--list-different`
  fonctionne uniformément sur le lot — [source:
  <https://prettier.io/docs/cli> (host: prettier.io, via résultats
  web_search)] (confidence: high, cité). Contraste direct avec le
  précédent interne non récursif (`--echantillon`) : les deux conventions
  existent, le choix devra être tranché.
- **mdformat** — argument positionnel variadique `paths ...` (« files to
  format », « glob pattern (multiple allowed) »), options de formatage
  identiques pour tous les fichiers du lot, mode `--check` sans écriture —
  [source:
  <https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html>
  (host: mdformat.readthedocs.io, via résultats web_search)] (confidence:
  high, cité). Modèle conforme à la règle « mêmes paramètres de cleaning
  pour tous ».
- **markdownlint-cli2** — tous les motifs d'entrée passés sur la ligne de
  commande (globs inclus), résultats par fichier puis résumé global ; la
  configuration (options) est homogène pour l'ensemble du lot — [source:
  <https://github.com/DavidAnson/markdownlint-cli2> (host: github.com,
  allowlisted)] (confidence: medium, cité). Précédent pour la structure de
  sortie console « par document + résumé ».
- **Aucun outil examiné ne « désactive silencieusement » des options en
  batch** : chez prettier, mdformat et markdownlint, les modes sans
  écriture (`--check`) restent applicables à chaque fichier d'un lot.
  L'arbitrage « options ignorées en multi-docs » est donc propre à
  MD_Cleaner, motivé par la liaison suggestion↔document, mais sans
  précédent externe direct — [source: synthèse des trois précédents
  ci-dessus] (confidence: medium, ASSUMPTION d'exhaustivité : trois outils
  examinés, pas un survey complet).

## Market & Context

- Contournement actuel : boucle shell (PowerShell) de N invocations
  `md-cleaner` — possible aujourd'hui, documentée nulle part, et ne
  souffrant d'aucune limitation fonctionnelle si ce n'est la répétition
  manuelle — [source: README.md (absence de doc batch) | ASSUMPTION :
  aucun autre contournement identifié] (confidence: medium).
- Coût de l'inaction : faible à modéré — N invocations manuelles par
  corpus multi-documents ; le corpus actif du projet est de 3 documents
  d'entrée, l'inconvenance est réelle mais non mesurée — [source:
  Examples/, ASSUMPTION sur la taille des usages réels hors dépôt]
  (confidence: medium).
- La capacité multi-fichiers est un standard de fait des
  formatters/linters Markdown et de code (prettier, mdformat,
  markdownlint-cli2, black) : un utilisateur familier de cet écosystème
  l'attend naturellement — [source: prettier.io,
  mdformat.readthedocs.io, github.com/markdownlint-cli2 via web_search]
  (confidence: medium).

## Data & Constraints

- Corpus du dépôt : 13 fichiers `.md` sous `Examples/`, dont 3 documents
  d'entrée consolidés ; structure des exemples : `Exemple_N/1.Sample/`
  (5 pages) et `Exemple_N/2.Input/` (document consolidé) — [source:
  `find Examples -name "*.md"` exécuté le 2026-10-05] (confidence: high,
  cité).
- Point de données structurel : `Examples/Exemple_1/` contient à la fois
  `1.Sample/` (5 pages brutes) et `2.Input/` (le consolidé à nettoyer). Un
  scan **récursif** d'un tel dossier mélangerait pages d'échantillon et
  documents consolidés — natures différentes pour l'outil (`1.Sample` est
  du calibrage, `2.Input` du nettoyage) ; un scan **non récursif** (comme
  `--echantillon`) évite ce piège mais ne trouve rien dans un dossier qui
  ne contient que des sous-dossiers — [source: Examples/,
  md_cleaner/detection.py] (confidence: high, cité). À trancher en
  spécification.
- Contrainte de constitution : principe IV (simplicité/YAGNI, point
  d'entrée CLI unique, pas d'abstraction prématurée) — un lot
  multi-documents reste dans le périmètre CLI mais accroît la surface de
  l'argumentaire positionnel ; principe « local, déterministe, stdlib »
  non impacté (`pathlib` suffit, comme le prouve `charger_echantillon`) —
  [source: .specify/memory/constitution.md] (confidence: high, cité).
- Contrainte technique existante favorable : `resoudre_chemin_nettoye`
  garantit déjà l'absence d'écrasement par suffixe `-1`, `-2` — utilisable
  tel quel pour désambiguïser deux sorties de lot aux noms dérivés
  identiques — [source: md_cleaner/sortie.py] (confidence: high, cité).
- Codes retour à arbitrer : le contrat actuel distingue entrée invalide
  (1) et artefact invalide (2) ; un lot de N entrées dont K échouent
  introduit le cas mixte (succès partiel) inconnu du contrat actuel —
  [source: contracts/cli.md] (confidence: high, cité).

## Evidence Against the Idea

- **Tension avec la boucle de jugement, cœur de l'outil** : le workflow
  documenté (README étape 3) est inspecter (`--dry-run`), arbitrer
  (`suggestion.json` édité), relancer (`--suggestion`). Ce workflow est
  intrinsèquement interactif et mono-document ; le lot ne sert que le
  chemin « sauter le dry-run », une fraction des capacités — [source:
  README.md, contracts/cli.md] (confidence: medium).
- **Signal de demande faible** : un seul porteur, aucune friction mesurée,
  corpus de 3 documents — le gain de commodité est modeste au regard de
  la révision du contrat FR-001, de la suite de tests et de la doc —
  [source: intake.md | ASSUMPTION sur l'absence d'autres usages]
  (confidence: medium).
- **Complexité de contrat** : détection fichier/dossier, récursivité,
  mélange fichiers+dossiers, échecs partiels, codes retour, structure des
  dossiers de run en lot, options réinterprétées (`--nom-titre` devient
  ambiguë avec plusieurs titres) — l'ensemble élargit significativement la
  surface du contrat CLI pour un bénéfice de confort — [source: synthesis
  de contracts/cli.md et md_cleaner/cli.py] (confidence: medium).
- **Simplicité constitutionnelle (IV)** : le projet a jusqu'ici ajouté des
  règles déterministes une à une sans toucher au squelette d'invocation ;
  ce serait la première révision du point d'entrée lui-même — [source:
  .specify/memory/constitution.md, historique specs/001-006] (confidence:
  medium).
- Contre-argument à nuancer : ces coûts sont des coûts de *conception du
  contrat*, pas de technologie — le scan de dossier existe déjà
  (`--echantillon`), la stdlib suffit, et la convention multi-chemins est
  éprouvée industriellement (prettier, mdformat) — [source:
  md_cleaner/detection.py, sources externes ci-dessus] (confidence:
  medium).

## Gaps & Open Questions

- [NEEDS CLARIFICATION: récursivité du scan dossier — non récursif comme
  `--echantillon` (plutôt cohérent avec la structure d'`Examples/`) ou
  récursif comme prettier ? Le cas « dossier ne contenant que des
  sous-dossiers » (ex. `Examples/Exemple_1/`) doit être tranché : erreur,
  0 document traité, ou descente ?]
- [NEEDS CLARIFICATION: mélange d'arguments fichier + dossier dans une
  même invocation (`md-cleaner doc1.md dossierA`) — autorisé ou usage
  invalide (code 3) ?]
- [NEEDS CLARIFICATION: sémantique exacte de « ignorées » pour
  dry-run/suggestion en multi-docs : erreur bloquante, avertissement +
  option neutralisée, ou silence ? Le dry-run est-il réellement non
  applicable par lot (il pourrait produire N rapports), ou est-ce un choix
  de périmètre ?]
- [NEEDS CLARIFICATION: structure des sorties d'un lot — un dossier de run
  unique contenant N sorties, ou N sous-dossiers ? Interaction avec la
  numérotation séquentielle et `--nom-titre` (lequel titre ?)]
- [NEEDS CLARIFICATION: échec partiel — un document du lot en erreur 1 ou
  2 arrête-il le lot, ou traite-t-on les autres ? Quel code retour pour un
  succès partiel ? Sorties des documents réussis conservées ou annulées ?]
- [NEEDS CLARIFICATION: dédoublonnage — que faire de doublons dans le lot
  (même fichier donné deux fois, fichier listé et aussi contenu dans le
  dossier) ? Ordre de traitement (ordre CLI, tri par nom comme
  `--echantillon`) ?]
- [NEEDS CLARIFICATION: volumétrie cible — `--echantillon` plafonne à 5 ;
  le lot a-t-il un plafond analogue (garde-fou de constitution déjà
  employé ailleurs : taille < 1 Mo) ?]
- [NEEDS CLARIFICATION: statut de `--pagine`, `--conserver-liens`,
  `--seuil`, `--calibrage`, `--extrait` en lot — tous applicables document
  par document sans conflit ; confirmer qu'ils ne relèvent pas de «
  l'ignoré » de l'intake]

## Sources

- <https://prettier.io/docs/cli> (host: prettier.io, policy: hors liste de
  confiance pour fetch — consulté via résultats du connecteur web_search,
  extraits cités sans fetch direct)
- <https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html>
  (host: mdformat.readthedocs.io, policy: idem)
- <https://mdformat.readthedocs.io/en/stable/users/configuration_file.html>
  (host: mdformat.readthedocs.io, policy: idem)
- <https://github.com/DavidAnson/markdownlint-cli2> (host: github.com,
  policy: allowlisted, consulté via résultats web_search)
- Sources internes (lecture directe du dépôt, 2026-10-05) :
  `md_cleaner/cli.py`, `md_cleaner/sortie.py`, `md_cleaner/detection.py`,
  `README.md`, `specs/001-nettoyage-md-repetitif/contracts/cli.md`,
  `specs/006-nom-sortie-source/`, `.specify/memory/constitution.md`,
  `.specify/assessments/*/decision.md`, `Examples/`
