# Decision: Extraits lisibles et localisables dans la suggestion

- **Slug**: lisibilite-dry-run
- **Decided**: 2026-09-29
- **Verdict**: go
- **Artifacts reviewed**: intake.md | research.md | problem.md | concept.md

## Scorecard

- **Problem validity** (strong) : Friction réelle mesurée sur le corpus : 14
  motifs sur 26 partagent exactement le même extrait dans la surface de jugement
  (suggestion.json) ; l'utilisateur a documenté son contournement (ouvrir le
  document source en parallèle) (problem.md, research.md)
- **Evidence strength** (strong) : Tout est mesuré et reproductible localement :
  doublons à 3 lignes (12), saturation à 5 lignes (24/25 distincts, 8 lignes
  sans gain), taille de fichier négligeable ; les quatre questions ouvertes ont
  été tranchées par l'utilisateur avec démonstration à l'appui pour le rendu
  `\n`
- **Value vs. inaction** (strong) : Le jugement depuis le JSON seul est le flux
  de travail réel de l'utilisateur (c'est le fichier qu'il édite) ; l'inaction
  maintient une friction systématique sur chaque document riche
- **Feasibility / appetite** (strong) : Small (2-3 jours) ; toutes les
  mécaniques existent en interne (emplacements pour la position, construction
  d'extrait déjà en place) ; le seul risque technique découvert (cellule de
  tableau cassée par `\n`) est couvert dans le périmètre recommandé par une
  neutralisation défensive
- **Strategic fit** (strong) : La règle de gouvernance du jour (une commande
  demandée est légitime, consolidation des options prévue plus tard) lève la
  tension FR-010 ; la constitution reste servie par les bornes de l'option, la
  garde de taille (< 1 Mo) et le refus de duplicater le document
- **Risk posture** (adequate) : Risques identifiés et couverts : casse du
  tableau du rapport (garde-fou inclus), révision du contrat `extrait` de la
  feature 001 (champ texte libre, pas de rupture de validation), validation du
  nouveau champ position à préciser en specification, bornes exactes de l'option
  à fixer — aucun risque non mitigué identifié

## Verdict & Rationale

**Go.** Les six critères sont à strong ou adequate, avec la particularité de ce
cas : le problème est entièrement mesuré (aucune supposition), l'utilisateur a
lui-même tranché les quatre questions de cadrage en cours d'assessment, et le
concept recommandé couvre le seul risque technique découvert (garde-fou du
rapport). La règle de gouvernance sur les commandes demandées écarte la seule
objection de simplicité qui aurait pu s'appliquer. L'option B du concept sert
les quatre décisions de cadrage sans en inventer de nouvelles.

## If go — Handoff to `/speckit-specify`

- **Problem** : les extraits de motifs dans `suggestion.json` (la surface de
  jugement) sont limités à 3 lignes et rendus en jonction « / », rendant 14
  motifs sur 26 indiscernables et obligeant à juger avec le document source
  ouvert en parallèle (problem.md).
- **Chosen approach** : Option B du concept.md — nouvelle option `--extrait N`
  (défaut 5, bornes indicatives 2-25, s'applique au JSON seul), extraits rendus
  en vrais sauts de ligne (`\n`), champ position par motif (page et lignes de la
  première occurrence), neutralisation défensive des sauts dans les cellules du
  rapport (troncature à 120 caractères conservée).
- **In scope** : construction de l'extrait (N lignes, `\n`), champ position dans
  suggestion.json, option CLI `--extrait`, garde-fou du rapport, révision du
  contrat « extrait » de la feature 001 (formats.md), validation stricte du
  champ position à la relecture, tests (effet exact N, doublons ≤ 2 sur
  Exemple_2, déterminisme, garde de taille).
- **Out of scope** (concept.md) : présentation du rapport au-delà du garde-fou,
  refonte de la détection/seuils/actions/ids, ancrage sur première ligne non
  vide (refusé), position par occurrence multiple, dépendances, duplicatat du
  document (JSON < 1 Mo).
- **Success metrics** (problem.md) : ≤ 2 extraits en doublon à la valeur par
  défaut sur Exemple_2 (baseline mesurée : 12) ; N demandé → exactement N lignes
  ; suggestion.json < 1 Mo sur le corpus ; déterminisme octet par octet ;
  validation d'un dry-run riche sans ouvrir le document source (qualitative,
  quickstart).
- **Carried-forward open questions** (choix de specification, pas de blocage) :
  - Bornes exactes et nom définitif de l'option (`--extrait`, indicatif 2-25)
  - Structure du champ position (objet `{"page": N, "debut": X, "fin": Y}` vs
    champs à plat) et sa validation stricte dans `lire_suggestion`
  - Sémantique exacte de l'extrait quand l'intervalle du motif est plus court
    que N (rendre ce qui existe vs compléter depuis l'intervalle suivant)
  - Emplacement de la révision du contrat : spec de la nouvelle feature citant
    la clause de la feature 001 à remplacer
