# Research: Un dossier de sorties partagé pour les documents d'un même lot

- **Feature**: 008-dossier-sorties-lot
- **Date**: 2026-10-05
- **Sources**: `md_cleaner/cli.py` et `md_cleaner/sortie.py` (état post-007,
  commit `5c906b9`, lus et modifiés ce jour), spec 008 et assessment
  `dossier-sorties-lot`, plan de la feature 006 (précédent de structure),
  `specs/007-traitement-multi-documents/contracts/multi-entrees.md`.

## Décisions

### D1 — Création du dossier de run : en tête d'invocation pour le lot de plusieurs, interne au traitement pour le mono-document

- **Decision** : dans `main()`, après la résolution du lot, les
  neutralisations et la validation de l'échantillon, le dossier de run
  est créé **une fois** si le lot compte plusieurs documents, puis
  passé à chaque itération de `_traiter_document`. Pour un lot d'un
  document, la création reste interne à `_traiter_document`, comme
  aujourd'hui (elle dépend du titre du document pour `--nom-titre`,
  lu pendant le traitement).
- **Rationale** : la rétrocompatibilité mono-document est garantie par
  construction — le chemin de code du mono ne bouge pas (SC-003),
  `--nom-titre` reste pleinement fonctionnel en mono sans lecture
  anticipée du document ; côté lot, un dossier créé avant la boucle
  donne le comportement déterministe exigé par la spec (lot entièrement
  en échec → dossier vide en place, FR-007 ; lot vide → aucun dossier,
  FR-008, la création étant postérieure à la résolution).
- **Alternatives considered** : créer le dossier dans `main()` pour
  tous les lots, mono compris (rejeté : oblige à lire le titre du
  document avant son traitement pour `--nom-titre`, déplacement de
  logique sans bénéfice observable) ; créer paresseusement au premier
  document réussi (rejeté : un lot entièrement en échec ne laisserait
  aucune trace de son numéro — moins déterministe, contredit FR-007).

### D2 — Signature de `_traiter_document` : dossier fourni ou créé

- **Decision** : `_traiter_document` reçoit un paramètre
  `dossier: Path | None` : `None` → création interne par
  `creer_dossier_run` (mono-document, comportement actuel) ; fourni →
  utilisation tel quel, sans création (lot de plusieurs).
- **Rationale** : un seul point de branchement, la différence
  mono/lot est explicite dans la signature ; les écritures
  (nettoyée, paginée, cartographie) restent inchangées dans la
  fonction.
- **Alternatives considered** : deux fonctions distinctes
  mono/lot (rejeté : duplication du chemin de nettoyage, risque de
  divergence) ; retour du dossier par `_traiter_document` et création
  au premier appel (rejeté : état mutable partagé entre itérations,
  moins lisible qu'un dossier passé en paramètre).

### D3 — Sorties secondaires en lot : gabarits de la spec + suffixe anti-collision par artefact

- **Decision** : en lot de plusieurs, les sorties de `--pagine` suivent
  les gabarits de la spec —
  `<nom-dérivé>-nettoye-pagine.md` et
  `<nom-dérivé>-cartographie.json` (nom dérivé = règle 006 : stem
  tronqué/normalisé, ex. `consolidated`) ; l'unicité est garantie par
  un suffixe `-1`, `-2`, ... inséré avant l'extension, de même forme
  que le mécanisme 006, résolu **par artefact** dans l'ordre de
  traitement : deux documents de stems identiques produisent, pour le
  second, `consolidated-nettoye-1.md` (résolveur existant),
  `consolidated-nettoye-pagine-1.md` et
  `consolidated-cartographie-1.json` — l'indice de suffixe est
  cohérent entre artefacts d'un même document puisque chaque
  résolveur parcourt les documents dans le même ordre. En lot d'un
  document, les noms courts actuels (`nettoye-pagine.md`,
  `cartographie.json`) demeurent.
- **Rationale** : conforme aux gabarits littéraux de FR-003 et à
  l'exigence d'attribution (US2) ; le suffixe final est la forme
  éprouvée de 006, applicable à toute extension ; une seule règle de
  lecture des noms (préfixe = document, suffixe = ordre de collision).
- **Alternatives considered** : dériver toutes les secondaires du stem
  **résolu** du fichier nettoyé (ex.
  `consolidated-nettoye-cartographie.json` — rejeté : s'écarte du
  gabarit `<nom-dérivé>-cartographie.json` de la spec et double le
  suffixe dans le nom) ; sous-dossier par document (rejeté : forme
  écartée par l'utilisateur, cf. intake addendum et décision).

### D4 — `resoudre_chemin_libre` : généralisation du résolveur de collision dans `sortie.py`

- **Decision** : nouvelle fonction pure dans `md_cleaner/sortie.py`,
  jumelle de `resoudre_chemin_nettoye` :
  `resoudre_chemin_libre(dossier, base_sans_extension, extension)`
  retourne le premier chemin libre pour
  `<base><suffixe><extension>` (`-1`, `-2`, ... insérés avant
  l'extension), jamais d'écrasement ; `resoudre_chemin_nettoye`
  devient un appel mince à cette généralisation (comportement
  octet pour octet identique, suite de tests 006 à l'appui).
- **Rationale** : une seule implémentation du mécanisme anti-collision
  pour deux usages (sorties nettoyées 006, secondaires préfixées 008) ;
  testable isolément ; aucune dépendance.
- **Alternatives considered** : copier-coller la boucle de suffixe
  dans `cli.py` (rejeté : duplication d'un garde-fou critique) ;
  renvoyer les chemins depuis `resoudre_lot` (rejeté : mélange
  résolution d'entrées et plan de sortie, responsabilités croisées).

### D5 — Neutralisation de `--nom-titre` en lot de plusieurs

- **Decision** : dans le bloc de neutralisation de `main()`, à côté de
  `--dry-run`/`--suggestion` : si le lot compte plusieurs documents et
  `args.nom_titre is not None`, avertissement sur stderr au format
  existant (`AVERTISSEMENT : --nom-titre ignorée en lot : applicable à
  un seul document`) puis `args.nom_titre = None` ; le dossier de lot
  est créé avec la numérotation séquentielle seule
  (`creer_dossier_run(args.sortie, "", None)` — le titre est ignoré
  quand `nom_titre` est `None`, vérifié dans `sortie.py`).
- **Rationale** : arbitrage utilisateur du 2026-10-05 (Q1 de la
  spécification, réponse A) ; symétrie parfaite avec la neutralisation
  007, jamais de silence (SC-004 de l'esprit 007).
- **Alternatives considered** : nommage d'après le titre du premier
  document (rejeté en clarification : arbitraire pour un lot
  hétérogène) ; refus bloquant code 3 (rejeté : la spec exige
  l'avertissement + neutralisation, pas le refus).

### D6 — Messages console : inchangés, chemins reflétant le dossier partagé

- **Decision** : aucune modification des messages : `Sortie : ...`,
  `Sortie paginée : ...`, `Cartographie : ...` affichent les chemins
  réels dans le dossier partagé (l'alignement est automatique puisque
  les chemins viennent du dossier passé à `_traiter_document`).
- **Rationale** : FR-010 ; aucun résumé de lot (Out of scope).
- **Alternatives considered** : ligne de résumé de lot (rejeté :
  Out of scope de la décision).

### D7 — Migration des tests, contrats et documentation dans la même livraison

- **Decision** : (1) migration des ~9 assertions de structure de
  `tests/integration/test_lot.py` (lot → 1 dossier) et ajout des
  tests US1-US4 (dossier unique, secondaires préfixées et uniques,
  `--nom-titre` neutralisée, lot entièrement en échec → dossier vide,
  mono-document inchangé) ; (2) révision de
  `specs/007-.../contracts/multi-entrees.md` (FR-003 « un dossier de
  run par document » → « un dossier de run par invocation » ; FR-011
  idem) et de `specs/001-.../contracts/cli.md` (table des fichiers
  produits par mode) ; (3) section README mise à jour ; (4) le détail
  autoritaire est consigné dans
  `specs/008-.../contracts/dossier-de-lot.md`. La suite existante hors
  lot doit passer sans relâchement.
- **Rationale** : précédent 006 (D6 du plan 006 : contrat 001 et
  README révisés dans la même livraison) ; SC-006 exige l'absence de
  divergence documentaire résiduelle.
- **Alternatives considered** : livrer le code et différer la doc
  (rejeté : les contrats 007/001 décriraient un comportement faux).

## NEEDS CLARIFICATION résolus

Aucun marqueur restant : l'unique arbitrage (`--nom-titre` en lot :
neutralisation avec avertissement) a été tranché en clarification de la
spécification le 2026-10-05 (réponse A) et est intégré à la spec (FR-005,
US4) et à la décision D5 ci-dessus.
