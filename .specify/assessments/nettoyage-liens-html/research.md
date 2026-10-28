# Idea Research: Nettoyage optionnel des destinations de liens résiduelles

- **Slug**: nettoyage-liens-html
- **Created**: 2026-10-02
- **Evidence confidence (overall)**: medium (interne, mesurée : high ; demande
  externe : single-user, non vérifiée)

## Users & Demand

- Signal mesuré fort : dans `output/004/nettoye.md` (sortie réelle, source Cour
  des comptes), 527 lignes sur 1724 (~31 %) contiennent une destination de lien
  inline de la forme `[texte](</...>)` ; l'entrée
  `Examples/Exemple_2/2.Input/consolidated.md` en compte 3110 lignes. — [source:
  mesure grep sur `output/004/nettoye.md` et
  `Examples/Exemple_2/2.Input/consolidated.md`, 2026-10-02] (confidence: high)
- Les 527 occurrences de la sortie sont toutes des liens Markdown complets
  `[texte](</...>)` ; aucune destination "nue" `(</...>)` sans libellé n'existe
  dans ce fichier. — [source: mesure grep `output/004/nettoye.md` :
  `\[[^]]*\](</[^>]*>)` = 527 = total `(</`] (confidence: high)
- Deux familles de destinations : (a) filtres thématiques
  `/publications?f%5B1%5D=thematic%3A<id>` (~15 variantes, la plus fréquente à
  49 occurrences), (b) pages de publication `/fr/publications/<slug>`.
  Caractères encodés (`%5B`, `%3A`) présents. — [source: dénombrement uniq sur
  `output/004/nettoye.md`] (confidence: high)
- Demande émise par l'unique utilisateur connu de l'outil (propriétaire du
  projet), sur la base d'un run réel. Aucun autre utilisateur ou signal de
  demande externe. — [source: intake.md ; ASSUMPTION : pas d'autres utilisateurs
  connus] (confidence: low)

## Prior Art

- Interne — aucune règle existante ne touche aux destinations de liens.
  `md_cleaner/normalisation.py` ne tokenize que `https?://` et `www.` : les
  destinations relatives `(</...>)` ne sont pas normalisées avant la détection
  de motifs. Un nettoyage par regex serait cohérent avec l'approche déterministe
  textuelle déjà retenue (rejet explicite d'un parseur CommonMark dans
  `specs/001-nettoyage-md-repetitif/research.md`). — [source: lecture
  `md_cleaner/normalisation.py`, `specs/001-nettoyage-md-repetitif/research.md`]
  (confidence: high)
- Interne — tension avec deux décisions antérieures : la feature 002
  (`specs/002-fusion-majoritaire`) vise explicitement à « conserver les
  métadonnées des publications (marqueur d'institution, dates, liens de thème)
  », et la feature 003 s'appuie sur les « liens de thème » comme éléments
  distinctifs des extraits du dry-run. Ces décisions portent sur la détection et
  le dry-run, pas sur l'écriture finale, mais un nettoyage appliqué en amont de
  la détection casserait ces deux features. — [source:
  `specs/002-fusion-majoritaire/quickstart.md` l.45,
  `specs/003-extrait-lisible/spec.md` l.21-25] (confidence: high)
- Interne — collision potentielle : l'outil produit lui-même des balises HTML
  dans `nettoye-pagine.md` (commentaires `<!-- page: N -->`, décision D6 de la
  feature 001, contrat de cohérence dans
  `md_cleaner/cartographie.py::marqueur_page`). Un nettoyage "des balises HTML"
  du document de sortie doit explicitement les préserver. — [source:
  `specs/001-nettoyage-md-repetitif/research.md` l.42,
  `md_cleaner/cartographie.py`,
  `md_cleaner/nettoyage.py::ecrire_nettoye_pagine`] (confidence: high)
- Terminologie : les éléments visés ne sont pas des balises HTML — ce sont des
  destinations de liens Markdown inline entre chevrons (forme
  `](<destination>)`). Une vraie balise HTML (ex. `<div>`) n'a pas été observée
  dans les sorties examinées. — [source: lecture `output/004/nettoye.md` ;
  ASSUMPTION pour l'absence d'autres formes dans d'autres corpus] (confidence:
  medium)

## Market & Context

- Alternative actuelle : post-traitement manuel (sed/PowerShell) par
  l'utilisateur après chaque run — coûteux et fragile, contredit le
  positionnement « une commande, sortie directement exploitable (RAG) » du
  README. — [source: `README.md` ; ASSUMPTION sur le coût perçu] (confidence:
  medium)
- Perte d'information faible : les destinations visées sont des URL relatives
  (sans domaine, ex. `</publications?f%5B1%5D=...>`), inexploitables en l'état ;
  la provenance par page reste disponible dans `cartographie.json`
  (`url_source`) et le libellé du lien serait conservé. — [source:
  `output/004/nettoye.md`,
  `md_cleaner/cartographie.py::construire_cartographie`] (confidence: high)
- Coût de l'inaction : ~31 % des lignes de la sortie 004 gardent un suffixe de
  destination illisible dans un document destiné à la lecture/RAG ; les chunkers
  et lecteurs rendent par ailleurs le lien cliquable, ce qui peut être
  souhaitable dans certains cas d'usage. — [source: mesure output/004 ;
  ASSUMPTION sur l'usage RAG] (confidence: medium)

## Data & Constraints

- Constitution du projet (v1.4.0, citée dans le README) : local-first sans
  réseau, zéro dépendance runtime (stdlib `re` suffit), déterminisme, sorties
  uniquement dans `output/`. Une option CLI est compatible. — [source:
  `README.md` section Développement] (confidence: high)
- Contrat CLI (`specs/001-nettoyage-md-repetitif/contracts/cli.md`,
  implémentation `md_cleaner/cli.py`) : toutes les options booléennes actuelles
  (`--dry-run`, `--pagine`) sont opt-in ; aucune option "activée par défaut"
  n'existe encore. Une option par défaut activée + drapeau de désactivation
  serait un nouveau pattern UX pour l'outil. — [source: `md_cleaner/cli.py`]
  (confidence: high)
- Étape d'application : `md_cleaner/nettoyage.py::nettoyer` conserve les lignes
  telles quelles ; le nettoyage des destinations serait une nouvelle passe
  (avant/pendant/après `nettoyer`), à définir. Si appliquée avant la détection,
  elle changerait les motifs détectés et les ids M01… (déjà documentés comme
  instables entre versions, README « Notes de version »). — [source:
  `md_cleaner/nettoyage.py`, `README.md`] (confidence: high)
- Volumes concernés : documents de plusieurs centaines de Ko, 21 pages, 3110
  lignes porteuses dans l'entrée Exemple_2 ; impact performance attendu
  négligeable (une regex par ligne). — [source: mesure grep ; ASSUMPTION sur
  l'impact perf] (confidence: medium)

## Evidence Against the Idea

- Décisions antérieures opposées : les liens de thème ont été traités comme
  métadonnées de valeur à conserver (features 002 et 003). Supprimer les
  destinations du document final est défendable (les libellés restent), mais
  l'historique montre que ces éléments ont été jugés utiles — le revoir doit
  être explicite. — [source: `specs/002-fusion-majoritaire/quickstart.md`,
  `specs/003-extrait-lisible/spec.md`] (confidence: high)
- Défaut activé = changement de comportement pour tous les runs : les sorties
  actuelles et les tests d'acceptation existants (SC-*, `tests/`) comparent des
  contenus ; activer par défaut modifie `nettoye.md` attendu et impose une
  migration de tests. — [source: `tests/`, `specs/*/tasks.md` ; ASSUMPTION sur
  des tests comparant le contenu exact] (confidence: medium)
- Périmètre flou : « balises html » est un abus de langage (destinations
  Markdown, pas de balises) ; un périmètre mal borné risque de supprimer des
  liens légitimes du contenu rédactionnel ou les marqueurs `<!-- page: N -->`
  produits par l'outil. — [source: terminologie intake vs mesure ;
  `md_cleaner/cartographie.py`] (confidence: high)
- Demande d'un seul utilisateur, sans donnée d'usage au-delà du run 004 ; le
  bénéfice pour d'autres corpus (Exemple_1) n'est pas mesuré — Exemple_1
  contient aussi le motif (`[CORSEN AI](</fr/>)` dans le contrat formats). —
  [source: `specs/001-nettoyage-md-repetitif/contracts/formats.md` l.26 ;
  ASSUMPTION sur l'ampleur dans Exemple_1] (confidence: medium)

## Gaps & Open Questions

- [NEEDS CLARIFICATION: supprime-t-on uniquement la destination `(</...>)` en
  conservant `[libellé]` tel quel (crochets compris), ou transforme-t-on
  `[libellé](</...>)` en `libellé` nu ?]
- [NEEDS CLARIFICATION: le nettoyage s'applique-t-il aussi à `nettoye-pagine.md`
  (en préservant les marqueurs `<!-- page: N -->` produits par l'outil) et aux
  extraits du dry-run ?]
- [NEEDS CLARIFICATION: appliqué avant ou après la détection des motifs (impact
  ids M01…, feature 003) ?]
- [NEEDS CLARIFICATION: nom du drapeau de désactivation (`--no-...` vs valeur
  booléenne), premier paramètre « activé par défaut » de l'outil]
- [NEEDS CLARIFICATION: caractères encodés (`%5B`, `%3A`) : suppression brute
  sans décodage, ou décodage préalable ?]
- [NEEDS CLARIFICATION: le périmètre couvre-t-il aussi les destinations absolues
  `](http...)` ou uniquement la forme chevron `(</...>)` ?]

## Sources

- `output/004/nettoye.md` (mesures grep, host: n/a — fichier local du dépôt,
  policy: interne, aucune URL externe consultée)
- `Examples/Exemple_2/2.Input/consolidated.md` (mesure grep, interne)
- `md_cleaner/normalisation.py`, `md_cleaner/cli.py`, `md_cleaner/nettoyage.py`,
  `md_cleaner/cartographie.py` (lecture de code, interne)
- `specs/001-nettoyage-md-repetitif/` (research.md, contracts/cli.md,
  contracts/formats.md), `specs/002-fusion-majoritaire/` (spec.md,
  quickstart.md), `specs/003-extrait-lisible/spec.md` (précédents de décision,
  interne)
- `.specify/assessments/granularite-motifs/` (intake.md, decision.md — précédent
  feature 002, interne)
- `README.md` (constitution, options CLI, notes de version, sources des
  exemples, interne)
- Aucune URL externe fetchée : aucune URL fournie, et le sujet est couvert par
  les artefacts internes du dépôt.
