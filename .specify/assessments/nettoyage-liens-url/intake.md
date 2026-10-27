# Idea Intake: Étendre le nettoyage aux destinations de liens absolues

- **Slug**: nettoyage-liens-url
- **Created**: 2026-10-05
- **Source**: repo path: `output/009/nettoye.md` (diagnostic en lecture seule du
  2026-10-05)
- **Type**: improvement

## Idea (as captured)

Question initiale de l'utilisateur :

> « Pourquoi à ton avis j'ai encore des balises https dans mes sorties ? »

Intention extraite en fin de diagnostic :

> « Étendre le retrait aux destinations absolues `](<https://...>)` → lancer
> l'assessment d'une nouvelle feature, car la borne "absolus hors périmètre" est
> un arbitrage de l'assessment 004 qu'il ne convient pas de contourner par un
> simple patch. »

Faits constatés lors du diagnostic :

- La feature 004-nettoyage-liens-html retire uniquement les destinations
  relatives de la forme `](</...>)` (`md_cleaner/nettoyage.py`,
  `RE_DESTINATION_LIEN = re.compile(r"(?<=\])\(</[^>]*>\)")`).
- Les destinations absolues `](<https://...>)` sont explicitement hors périmètre
  de la feature 004 (`specs/004-nettoyage-liens-html/spec.md`, questions
  ouvertes : « Que se passe-t-il des destinations absolues `](https://...)` ?
  Hors périmètre : elles ne sont ni retirées ni modifiées (borne explicite de
  l'assessment) »).
- Le run 009 (2026-10-05) ne contient plus aucune occurrence de `](</` mais
  conserve 6 occurrences de `](<https` (en-tête de navigation et pied de page
  Mistral).

## Restated

Étendre la passe de nettoyage des destinations de liens inline, aujourd'hui
limitée aux chemins relatifs `](</...>)`, pour retirer aussi les destinations
absolues de la forme `](<https://...>)` dans `nettoye.md` et
`nettoye-pagine.md`. Cette extension relèverait la borne posée volontairement
par l'assessment 004 et nécessite donc un assessment dédié avant toute
implémentation.

## Origin & Context

- **Raised by**: [NEEDS CLARIFICATION: utilisateur unique du projet, lors d'une
  session de test post-implémentation de la feature 004]
- **Trigger**: constat de destinations `](<https://...>)` résiduelles dans
  `output/009/nettoye.md` (run de test de la feature 004 sur un document de la
  documentation Mistral), alors que la feature venait d'être implémentée ; le
  diagnostic a établi que la présence de ces liens est conforme au périmètre
  borné de la feature 004, d'où la demande d'un assessment dédié.

## First-Glance Unknowns

- [NEEDS CLARIFICATION: faut-il retirer toutes les formes de destinations
  absolues (`https`, `http`, autres schémas) ou seulement `https` ?]
- [NEEDS CLARIFICATION: la désactivation via `--conserver-liens` doit-elle
  couvrir aussi cette extension, ou un drapeau distinct est-il nécessaire ?]
- [NEEDS CLARIFICATION: faut-il viser toutes les formes `](<...>)`
  indépendamment du schéma (y compris relatives), c'est-à-dire élargir la cible
  à « toute destination entre chevrons » ?]
- [NEEDS CLARIFICATION: pourquoi la borne « absolus hors périmètre » avait-elle
  été posée dans l'assessment 004 — coût, risque de perte d'information utile,
  ou simple découpage d'appétit ?]
- [NEEDS CLARIFICATION: la prévalence de ces liens absolus dans les corpus
  cibles (Exemple_1, Exemple_2, Exemple_3) justifie-t-elle une feature dédiée ?]

## Addendum (2026-10-05, post-research)

L'utilisateur a raffiné l'idée et apporté une nouvelle donnée après le premier
passage de recherche :

1. Le corpus Mistral est désormais archivé dans le dépôt :
   `Examples/Exemple_3/2.Input/retry-failed-records.md` (320 lignes, 6
   destinations `](<https...>)`, 38 `](</...>)`), en faisant le troisième corpus
   de référence du projet.
2. Exigence de périmètre : élargir le retrait aux autres schémas possibles
   au-delà de `https` (`http` ? autres ?) — réponse partielle au premier unknown
   ci-dessus (le principe est posé, la liste exacte ne l'est pas).
3. Exigence de garde-fou : une URL explicitement indiquée dans le corps du texte
   (extrait de code, explicitation particulière) doit être conservée dans la
   sortie finale.

Détail et mesure : voir `research.md` (mise à jour du 2026-10-05).
