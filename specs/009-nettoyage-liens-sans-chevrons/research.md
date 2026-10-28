# Implementation Research: Nettoyage des destinations de liens sans chevrons

**Feature**: 009-nettoyage-liens-sans-chevrons | **Date**: 2026-10-27 |
**Source**: [plan.md](./plan.md), [spec.md](./spec.md), calibrage du corpus
`Examples/Nettoyage-balises/` (assessment `nettoyage-balises`)

## D1 — Ajouter une seconde règle plutôt que réécrire la règle chevron

- **Decision** : conserver la regex 004/005 `](<...>)` strictement intacte
  et ajouter une passe distincte pour les formes sans chevrons, dans la
  même fonction de nettoyage à l'écriture.
- **Rationale** : FR-005 exige un comportement chevron identique octet par
  octet sur 5 314 destinations des corpus historiques ; une regex réécrite
  « unifiée » mettrait ce patrimoine en risque pour un gain de lisibilité
  nul. L'isolation des deux règles rend la non-régression testable par
  diff de sorties.
- **Alternatives considered** : regex unique couvrant chevrons et
  non-chevrons (rejetée : risque de régression sur le comportement
  éprouvé) ; parsing Markdown complet (rejeté : constitution IV YAGNI,
  stdlib uniquement, la forme visée est un débris de conversion, pas du
  Markdown à interpréter).

## D2 — Protéger les images par placeholders éphémères avant la passe

- **Decision** : avant d'appliquer la règle sans chevrons, remplacer
  temporairement chaque construct d'image `![...](...)` par un placeholder
  sentinelle, puis restaurer après la passe.
- **Rationale** : FR-003 exige d'épargner les images intégralement,
  y compris imbriquées dans un lien (logo `[![FIPECO](img)](/)` : seule la
  destination externe `(/)` doit partir). Une exclusion par lookbehind sur
  le crochet fermant est impossible : dans `![](/img)` (alt vide), le
  crochet fermant est précédé du crochet ouvrant, pas du `!` — la
  distinction image/lien ne peut pas se faire sur la sous-chaîne de
  destination seule. La protection traite les deux cas (image simple,
  image dans un lien) avec une seule règle.
- **Alternatives considered** : lookbehind négatif `(?<!!)` (rejeté :
  ne matche que les alt vides commençant par `!`, faux négatif sur
  `![FIPECO](img)`) ; matching du construct complet avec label (rejeté :
  les libellés peuvent contenir des crochets équilibrés — `[[1]]` — et le
  remplacement deviendrait un mini-parseur, hors budget small).
- **Limite documentée** : un alt d'image contenant un crochet fermant
  (`![a]b](img)`) n'est pas couvert par la regex de protection ; la règle
  lien standard s'applique alors à sa destination (comportement documenté
  et testé, T011) ; aucune occurrence dans les corpus connus, cas
  détectable par grep.

## D3 — Règle sans chevrons : sous-chaîne après crochet fermant, excluant les chevrons

- **Decision** : la nouvelle règle cible la sous-chaîne `(...)` suivant
  un crochet fermant, avec : destination sans espaces ni chevrons
  initiaux (exclusion `(?!<)`), titre éventuel emporté (forme
  `](url "titre")`, arbitrage 005 reconduit), destination vide couverte
  (`(#)`).
- **Rationale** : exclure explicitement les destinations commençant par
  `<` réserve les formes chevrons à la règle 004/005 seule (D1) et évite
  tout double traitement, notamment sur les limites documentées 005
  (titre à guillemet échappé) où la règle chevron ne matche pas. Les
  destinations sans chevrons ne contiennent pas d'espaces en Markdown
  (sinon la forme est `<...>`), ce qui borne la destination au premier
  espace ou à la parenthèse fermante. Précision ajoutée en TDD : `()`
  (destination totalement vide) et `]( "titre")` (titre sans
  destination) ne matchent pas — la destination doit contenir au moins
  un caractère autre qu'espace et que parenthèse fermante.
- **Alternatives considered** : autoriser les chevrons dans la nouvelle
  règle (rejeté : double traitement des formes 004/005 et interaction
  avec leurs limites documentées) ; exclure les ancres (rejeté :
  l'option A de 005 et la spec 009 exigent une seule règle sans cas
  particulier).
- **Limite documentée** : un titre contenant un guillemet interne
  échappé (`\"`) arrête le match avant la parenthèse fermante — la
  destination reste en place, sans corruption (limite héritée de 005) ;
  0 occurrence dans le corpus de calibration.
- **Amendement (bug nettoyage-balises2, 2026-10-27)** : la règle
  couvre désormais les titres à guillemets internes échappés — forme
  footnote du corpus Le Grand Continent, où le titre embarque du HTML
  brut (`<a href=\"https://...\">…</a>`) portant la quasi-totalité des
  URLs résiduelles — et les destinations contenant des espaces tant
  qu'aucun titre ne suit (Markdown invalide produit par les
  convertisseurs) ; la limite reste pour la règle chevron 004/005
  (FR-005, arbitrage : chevron inchangé) et pour une destination à
  espaces suivie d'un titre.

## D4 — Ordre d'application : protection, chevrons, sans chevrons, restauration

- **Decision** : ordre fixe dans la passe d'écriture : (1) protection des
  images par placeholders ; (2) passe chevrons 004/005, inchangée ;
  (3) passe sans chevrons (D3) ; (4) restauration des images.
- **Rationale** : la passe chevron s'exécute sur des lignes où les images
  sont déjà masquées, ce qui la neutralise vis-à-vis des destinations
  d'images ; les deux règles ne peuvent pas interagir ; l'idempotence
  est préservée (après un passage, aucune forme cible ne subsiste, la
  restauration est exacte, sentinelles sans `](` ni `](<`). Précision
  ajoutée en implémentation : le masquage précède aussi la passe
  chevrons — une image à destination chevrons serait épargnée
  également (FR-003 prime sur FR-005 pour les images) ; aucune image
  n'existe dans les corpus historiques, la neutralité testée (T013)
  est donc inchangée.
- **Alternatives considered** : passe sans chevrons avant la passe
  chevrons (rejeté : aucun gain, ajoute une interaction possible avec
  les placeholders) ; passes séparées par fichier (rejeté : complexité
  sans bénéfice).

## D5 — Périmètre d'application : sorties livrables seules

- **Decision** : les deux règles ne s'appliquent que dans les writers de
  `nettoye.md` et `nettoye-pagine.md` (invariant 004/005 reconduit,
  clarification du 2026-10-27).
- **Rationale** : l'extrait lisible du dry-run et les artefacts de
  suggestion doivent refléter l'entrée ; le `Bloc` renvoyé par le
  nettoyage n'est pas muté en amont.
- **Alternatives considered** : étendre à l'extrait du dry-run (rejeté :
  hors périmètre confirmé par l'utilisateur, la prévisualisation doit
  rester fidèle à l'entrée).

## D6 — Garde-fous reconduits : URLs nues, marqueurs de page, blocs de code

- **Decision** : reconduire les contrats 005 : la règle ne matche que la
  sous-chaîne suivant un crochet fermant — les URLs nues du corps du
  texte et les contenus de blocs de code sont intacts par construction ;
  les marqueurs `<!-- page: N -->` ne contiennent pas de crochet fermant
  suivi de parenthèse et sont générés après la passe.
- **Rationale** : contrats éprouvés, reconduits par FR-006 et la spec ;
  vérifiés par tests (005) et quickstart.
- **Alternatives considered** : aucune — reconduction.

## D7 — Résidus tolérés documentés (option A confirmée)

- **Decision** : les résidus suivants sont acceptés et documentés dans le
  contrat : logo réduit à `[![FIPECO](img)]` (destination externe
  retirée, image conservée) ; libellés de notes de bas de page `[[1]]`
  (destination `(#_ftn1)` retirée) ; libellés de navigation seuls
  (`[Faire un don]`) ; libellés vides `[]` sur liens textuels.
- **Rationale** : l'option A (assessment `nettoyage-balises`,
  comparaison A/B sur exemples réels) épargne le contenu d'intérêt au
  prix de ces résidus ; leur suppression relève de la détection de
  motifs (features 001/002), périmètre distinct explicitement hors scope.
- **Alternatives considered** : option B (retrait des constructs
  d'images vides et des libellés) — rejetée par l'utilisateur le
  2026-10-27 : perte de figures de contenu contraire à l'exigence de
  conservation.
