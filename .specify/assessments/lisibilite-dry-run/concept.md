# Concept: Extraits lisibles et localisables dans la suggestion

- **Slug**: lisibilite-dry-run
- **Created**: 2026-09-29
- **Recommended option**: B — Commande --extrait N + position, rendu
  multi-lignes

## Options

### Option 0 — Ne rien faire

- **Sketch** : suggestion et rapport inchangés ; l'utilisateur continue de juger
  en ouvrant le document source à côté du JSON.
- **Appetite** : small (nul)
- **Trade-offs** : gagne zéro coût ; sacrifie le flux de validation sur les
  documents riches (12 motifs en doublon d'extrait à 3 lignes, mesuré) ;
  référence du coût de l'inaction (problem.md).
- **Rabbit holes** : aucun.

### Option A — Minimal sans commande : constante 5 lignes

- **Sketch** : l'extrait passe de 3 à 5 lignes par défaut, rendu en vrais sauts
  de ligne, avec le champ position ajouté ; aucune option CLI, le nombre de
  lignes est une constante interne.
- **Appetite** : small (une à deux journées, tests compris)
- **Trade-offs** : gagne la quasi-unicité des extraits (24/25 distincts, mesuré)
  au plus petit coût ; sacrifie le réglage demandé par l'utilisateur — la règle
  de gouvernance du jour (une commande demandée est ajoutée) rend cette sobriété
  inutilement frugale ; un extrait exceptionnellement trop court ou trop long
  n'a pas de soupape.
- **Rabbit holes** : la révision du contrat JSON de la feature 001 (« extrait ≤
  3 lignes jointes par " / " ») — inévitable dans toutes les options, à
  documenter proprement en specification.

### Option B — Complet demandé : `--extrait N` + position (recommandée)

- **Sketch** : une nouvelle option `--extrait N` (défaut 5, bornes ~2-25, JSON
  seul) règle le nombre de lignes de l'extrait ; l'extrait est rendu en vrais
  sauts de ligne (`\n`) ; chaque motif reçoit un champ position (page et lignes
  de sa première occurrence) ; le rapport, hors périmètre de jugement, reçoit
  uniquement une normalisation défensive de ses cellules (sauts neutralisés,
  table préservée). Les décisions de cadrage du problem.md sont servies telles
  quelles.
- **Appetite** : small (deux à trois journées, tests compris)
- **Trade-offs** : gagne exactement le flux demandé — juger depuis le JSON seul,
  régler la dose si un document l'exige, localiser chaque motif dans le document
  source via la position ; sacrifie un peu de sobriété (une option de plus —
  assumé par la règle de gouvernance, le tour final de consolidation des
  commandes est prévu) ; la taille du JSON croît avec N (garde quantitatif < 1
  Mo du problem.md).
- **Rabbit holes** : le garde-fou du rapport découvert en façonnage :
  `generer_rapport` insère aujourd'hui l'extrait dans une cellule de tableau
  markdown — des `\n` non neutralisés casseraient la table ; le périmètre «
  rapport inchangé » doit donc inclure une neutralisation minimale (remplacement
  par un séparateur simple), à ne pas confondre avec une refonte de présentation
  (refusée) ; les bornes exactes de N et le nom de l'option ; la structure
  exacte du champ position (objet dédié vs champs à plat).

### Option C — Étendu : B + ancrage sur la première ligne non vide

- **Sketch** : tout B, plus un ancrage de l'extrait sur la première ligne non
  vide du motif (les 2 doublons résiduels partageraient moins de préfixe) et
  éventuellement une position par occurrence.
- **Appetite** : small-medium (une semaine)
- **Trade-offs** : gagne un peu de distinction sur un cas marginal ; sacrifie la
  simplicité pour un problème déjà jugé acceptable (décision de cadrage n°4 :
  les 2 doublons résiduels sont acceptables, la position les distingue de toute
  façon) ; contredit la décision de l'utilisateur.
- **Rabbit holes** : ancrage = redéfinir la sémantique de l'extrait (« premières
  lignes de l'intervalle » vs « premières lignes utiles ») — subtilité de
  contrat qui n'a pas de besoin constaté.

## Recommendation

**Option B**. Elle sert les quatre décisions de cadrage du problem.md sans en
inventer d'autres : commande demandée (règle de gouvernance), rendu multi-lignes
(démonstration faite), position incluse (simple, les emplacements existent en
interne), doublons résiduels acceptés. Elle est le seul périmètre qui couvre le
garde-fou du rapport découvert en façonnage — sans lui, l'option A livrerait une
régression invisible (table du rapport cassée par les `\n`), ce qui écarte aussi
A en l'état. C reste hors besoin constaté : le problème des doublons est tranché
acceptable.

## Out of Scope (for the recommended option)

- Aucune modification de présentation du rapport au-delà de la neutralisation
  défensive des sauts de ligne dans les cellules (la troncature à 120 caractères
  reste, décision de cadrage n°1)
- Pas de refonte de la détection, des seuils, des actions, des ids
- Pas d'ancrage de l'extrait sur la première ligne non vide (C, refusée par la
  décision de cadrage n°4)
- Pas de position par occurrence multiple (première occurrence seulement)
- Non-goals hérités : pas de dépendance, pas de duplicatat du document, le JSON
  reste sous 1 Mo

## Assumptions to Validate

- Le champ position au format « page + lignes de la première occurrence » suffit
  à localiser un motif sans le document ouvert
- La neutralisation des sauts dans le rapport ne nécessite que le remplacement
  `\n` → séparateur simple, sans autre retouche du tableau
- La validation stricte `lire_suggestion` accepte un champ position
  supplémentaire sans changement de version du schéma (champ additionnel non
  validé aujourd'hui, ou validation à ajouter en specification)
- Le défaut 5 et les bornes ~2-25 tiennent sur les documents du corpus (mesure :
  saturation à 5 ; N=25 sur 26 motifs ≈ quelques dizaines de Ko)
- La révision du contrat « extrait » de la feature 001 (formats.md) se fait dans
  la spec de la nouvelle feature sans rupture pour les suggestions existantes
  (champ texte libre)
