# Idea Research: Élargir l'extrait des motifs dans la suggestion

- **Slug**: lisibilite-dry-run
- **Created**: 2026-09-29
- **Evidence confidence (overall)**: high (mesures internes reproductibles sur
  le corpus réel ; le sujet est local, aucun art antérieur externe pertinent à
  fetcher)

## Users & Demand

- Un utilisateur : le propriétaire, en validation réelle du dry-run de la
  feature 002 sur Exemple_2 — juger 25-26 motifs dont les extraits se
  ressemblent oblige à ouvrir le document source en parallèle — [source: session
  du 2026-09-29] (confidence: high)
- Mesure du problème : sur les 26 motifs du dernier dry-run, seulement **13
  extraits distincts** ; **14 motifs partagent exactement le même extrait** « /
  COUR DES COMPTES / » et 25 extraits sur 26 ne contiennent qu'une seule ligne
  non vide (les fenêtres de 3 lignes commencent et finissent par des lignes
  vides) — [source: mesure locale output/003/suggestion.json] (confidence: high)
- Mesure de la dose utile : en simulant l'extrait depuis les emplacements réels,
  **3 lignes → 14 extraits distincts / 12 motifs en doublon ; 5 lignes → 24
  distincts / 2 en doublon ; 8 lignes → 24 distincts / 2 en doublon** — la
  valeur 5 demandée par l'utilisateur est le point de saturation, 8 n'apporte
  rien de plus — [source: simulation locale du 2026-09-29, Exemple_2]
  (confidence: high)

## Prior Art

- Interne : le contrat de la feature 001 (`contracts/formats.md`) fixe « extrait
  ≤ 3 lignes jointes par ` / ` » et le rapport tronque l'extrait à 120
  caractères — la limite à 3 lignes vient de la feature 001, où les motifs
  étaient peu nombreux et compacts ; elle n'a pas été re-questionnée par la
  feature 002, qui a multiplié les motifs — [source: specs/001
  contracts/formats.md, ligne 50] (confidence: high)
- Interne : la feature 002 a déjà traité la lisibilité du côté du rapport (deux
  sections, FR-004) mais pas du côté du contenu de l'extrait — même racine
  (multiplication des motifs), remediation partielle — [source: specs/002
  spec.md, decision.md assessment granularite-motifs] (confidence: high)
- Externe : aucune recherche menée — question d'UX purement locale à l'outil ;
  les pratiques de prévisualisation d'artefacts de review (contexte suffisant
  pour décider sans ouvrir la source) sont du sens commun — ASSUMPTION
  (confidence: medium)

## Market & Context

- Alternative actuelle : ouvrir le document source et chercher les zones à la
  main pour juger un motif — coûteux, casse le flux, contredit l'objectif de
  validation < 5 min (SC-004/SC-006) — ASSUMPTION (confidence: medium)
- Autre alternative non demandée : renseigner la **position** (page, lignes) de
  chaque motif dans la suggestion — les emplacements existent déjà en interne
  mais ne figurent pas dans suggestion.json ; une référence « page N, lignes X-Y
  » permettrait de localiser sans allonger l'extrait — [source: data-model
  001/002, emplacements internes] (confidence: high)

## Data & Constraints

- Taille de fichier : l'extrait le plus long actuel fait 224 caractères ; passer
  à 5 lignes multiplierait la taille du JSON de quelques Ko au plus sur un
  document riche — négligeable — [source: mesure locale] (confidence: high)
- Contrainte directe : **FR-010 de la feature 002 interdit toute nouvelle option
  CLI** — la variante « commande pour paramétrer » demande soit de lever cette
  contrainte (changement de spec), soit d'être écartée au profit d'une constante
  par défaut relevée — [source: specs/002 spec.md FR-010] (confidence: high)
- Contrainte de présentation : le tableau du rapport tronque l'extrait à 120
  caractères — des extraits à 5 lignes (jusqu'à ~500 caractères) exigent une
  adaptation du rapport (troncature relâchée, rendage multi-lignes, ou extrait
  plein uniquement dans le JSON) — [source: md_cleaner/suggestion.py,
  generer_rapport] (confidence: high)
- Déterminisme : un extrait plus long ou paramétré reste déterministe
  (construction fixe depuis les emplacements) — aucune incidence sur SC-005 —
  ASSUMPTION (confidence: high)
- Les lignes vides restent la principale source de confusion dans le rendu joint
  par « / » (l'extrait à 5 lignes de M03 vaut « / COUR DES COMPTES / / [Famille,
  handicap...] - / ») : un rendage plus explicite (sauts affichés « ⏎ », vides
  ignorées) est une variante possible — [source: simulation locale] (confidence:
  high)

## Evidence Against the Idea

- La variante « paramètre CLI » contredit une contrainte de spec fraîchement
  actée (FR-010, feature 002) — lever une interdiction posée deux heures plus
  tôt demande une justification solide, et le besoin constaté (distinguer les
  motifs) est déjà servi par la simple mesure « 5 lignes par défaut » — [source:
  specs/002] (confidence: high)
- « Au moins 5 lignes » ne fait pas disparaître tous les doublons (2 motifs
  restent indiscernables par l'extrait seul à 5 comme à 8 lignes) et n'identifie
  pas la position du motif — l'extrait étendu atténue le problème sans garantir
  le jugement sans le document source — [source: simulation locale] (confidence:
  high)
- Un extrait long rend le rapport plus lourd à lire (tableau à 120 caractères
  aujourd'hui) : la lisibilité gagnée côté JSON peut se perdre côté rapport si
  la présentation n'est pas repensée en même temps — ASSUMPTION (confidence:
  medium)

## Gaps & Open Questions

- [NEEDS CLARIFICATION: la cible est-elle le JSON seul, le rapport seul, ou les
  deux — et avec quel rendu des lignes vides ?]
- [NEEDS CLARIFICATION: la variante « option CLI » doit-elle être présentée en
  spec comme levée de FR-010, ou écartée au profit d'une constante 5 par défaut
  ?]
- [NEEDS CLARIFICATION: faut-il en profiter pour ajouter la position (page,
  lignes) de chaque motif à la suggestion — signal complémentaire mesuré comme
  faisable ?]
- [NEEDS CLARIFICATION: quelle borne haute si un paramètre est retenu (l'extrait
  ne doit pas dupliquer le contenu du document) ?]

## Sources

- Mesures locales du 2026-09-29 : output/003/suggestion.json (26 motifs, 13
  extraits distincts, 14 doublons), simulation 3/5/8 lignes sur
  Examples/Exemple_2 via detecter() (confidence: high)
- Documents internes : specs/001 contracts/formats.md (extrait ≤ 3 lignes,
  troncature 120 caractères du rapport), specs/002 spec.md (FR-010), data-model
  des features 001/002 (emplacements internes)
- Aucune source externe fetchée : question locale, données internes suffisantes
  (policy: pas de fetch nécessaire)
