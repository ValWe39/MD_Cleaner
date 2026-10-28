# Problem Definition: Sorties avec destinations de liens sans chevrons

- **Slug**: nettoyage-balises
- **Created**: 2026-10-27
- **Inputs used**: intake.md | research.md

## Problem Statement

Les livrables nettoyés du nouveau corpus FIPECO conservent des destinations
de liens dites « sans chevrons » (`](/chemin)`, `](#ancre)`,
`](https://...)`) collées au texte utile — 199 occurrences sur 5 fichiers —
car la passe de nettoyage établie par les features 004/005 ne cible que les
formes entre chevrons. Chaque run produit donc un livrable qui exige une
retouche manuelle, contredisant la promesse « sortie directement
exploitable » du projet.

## Affected Users & Stakeholders

- **Users**: l'utilisateur unique (propriétaire) de `md-cleaner`, qui
  nettoie les sorties de conversion HTML → Markdown du corpus FIPECO — il
  retouche à la main chaque livrable (signalement : ligne 6 de
  `fipeco.fr-000033-nettoye.md`). — [source: intake.md, investigation]
- **Stakeholders**: le mainteneur du projet (même personne) — arbitre le
  périmètre entre passe liens et détection de motifs ; la constitution du
  projet impose une règle déterministe, locale, stdlib. — [source:
  constitution]

## Goals

- Les sorties nettoyées du corpus FIPECO ne portent plus aucune destination
  de lien sans chevrons, sans intervention manuelle.
- Le contenu d'intérêt survit intact : les libellés et le texte environnant
  (ex. « *tome II des voies et moyens* ») restent lisibles et inchangés.
- Le comportement reste réversible par l'utilisateur (conservation des
  liens cliquables à la demande).
- Le comportement acquis sur les formes entre chevrons (corpus historiques,
  5 314 destinations) n'est pas régressé.

## Non-Goals

- Supprimer les blocs de navigation et pieds de page répétés (125
  occurrences) : relève de la détection de motifs (features 001/002),
  périmètre distinct.
- Décoder ou réparer les URL (caractères encodés `%20`, `%C3%A9`...).
- Conserver par défaut des liens cliquables (la trace des 48 sources
  absolues du corps du texte n'est pas une exigence par défaut).
- Modifier les libellés ou le reste du texte des lignes conservées.
- Traiter les URLs nues ou les blocs de code, déjà hors périmètre par les
  contrats 005.

## Success Metrics

- 0 destination de lien sans chevrons dans les 5 sorties FIPECO rejouées
  (baseline : 199 occurrences, 34 à 47 par fichier). (mesurable)
- Libellés et texte environnant inchangés octet par octet hors destinations
  (baseline : libellés présents, ex. « *crédit d'impôt* », « une note »).
  (mesurable)
- Sorties inchangées sur les corpus historiques sans la nouvelle forme
  (baseline : 0 forme sans chevrons dans Exemple_1..3). (mesurable)
- Tests au vert sans relâchement, comportement chevron à l'octet identique
  (baseline : suite existante, plus de 20 tests). (mesurable)

## Cost of Inaction

Chaque run sur le corpus FIPECO (et tout futur corpus issu d'un convertisseur
produisant des formes sans chevrons) laisse ~40 destinations par fichier à
retoucher à la main, avec risque d'oubli et d'incohérence entre fichiers du
même lot ; c'est la troisième forme de débris de liens découverte en un mois
(004, 005, sans chevrons), et la retouche manuelle n'empêche pas la
prochaine de réapparaître.

## Open Questions

- [NEEDS CLARIFICATION: Sort des figures à alt vide `![](/images/...png)`
  (4 occurrences) — le retrait de leur destination laisserait un débris
  `![]` ; les épargner ou les traiter ?]
- [NEEDS CLARIFICATION: Logo imbriqué `[![FIPECO](img)](/)` (5 occurrences
  en pied de page) — attente de traitement, sans corruption ?]
- [NEEDS CLARIFICATION: Libellés devenus vides après retrait de la
  destination — retrait résiduel ou tolérés ?]
- [NEEDS CLARIFICATION: La borne « toutes destinations sans chevrons,
  ancres et relatifs sans slash compris » suit-elle l'option A de la spec
  005 (une seule règle, aucun cas particulier) ?]
- [NEEDS CLARIFICATION: Les formes à titre `](url "titre")`, absentes du
  corpus (0 occurrence), suivent-elles l'arbitrage 005 par précaution ?]
