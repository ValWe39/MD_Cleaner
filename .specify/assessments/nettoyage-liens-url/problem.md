# Problem Definition: Destinations de liens absolues résiduelles

- **Slug**: nettoyage-liens-url
- **Created**: 2026-10-05
- **Inputs used**: intake.md (addendum 2026-10-05) | research.md (mise à jour
  2026-10-05)

## Problem Statement

Les sorties nettoyées (`nettoye.md`, `nettoye-pagine.md`) conservent des
destinations de liens absolues `](<https://...>)` collées au texte utile des
lignes qui survivent à la détection de motifs, dégradant la lisibilité du
livrable et exigeant une retouche manuelle. Le nettoyage actuel des destinations
ne couvre que les chemins relatifs `](</...>)` : toute destination absolue — en
particulier dans des corpus de documentation convertie où les lignes de
navigation et de pied de page ne sont pas captées comme motifs récurrents —
traverse la passe sans être touchée.

## Affected Users & Stakeholders

- **Users**: l'unique utilisateur du projet (propriétaire) — chaque run sur un
  corpus de documentation convertie (type Exemple_3) produit un livrable avec
  des débris d'URLs absolues à retoucher à la main (6 lignes sur 299 dans le run
  009 ; 6 lignes sur 320 dans l'entrée Exemple_3).
- **Stakeholders**: le propriétaire du projet — décide de l'appétit et du
  périmètre ; il a formulé explicitement l'exigence (élargissement aux schémas +
  conservation des URLs légitimes du corps du texte) et archivé le corpus
  Mistral comme Exemple_3 de référence.
- **Consommateur final des sorties** : le lecteur du `nettoye.md` — reçoit des
  lignes de navigation dégradées
  (`[Reach out](<https://mistral.ai/contact?utm_source=...>)`) où l'information
  utile (le libellé) est noyée dans des paramètres de suivi. — [NEEDS
  CLARIFICATION: existence et attentes de lecteurs autres que l'utilisateur
  unique — aucune donnée]

## Goals

- Le livrable nettoyé ne contient plus de destinations de liens absolues collées
  au texte utile, quel que soit le schéma de l'URL (`https`, `http`, autres à
  déterminer), sur les corpus où ces lignes survivent à la détection.
- Toute URL légitimement présente dans le contenu utile du document — URL nue
  dans un extrait de code, URL explicitement indiquée dans une explicitation du
  corps du texte — reste disponible dans la sortie finale (garde-fou exigé par
  l'utilisateur).
- Le libellé des liens, le texte environnant et l'ordre des lignes restent
  inchangés ; seules les destinations disparaissent.
- Le comportement reste déterministe et local, conforme à la constitution du
  projet.

## Non-Goals

- Modifier la détection de motifs (la question de la non-détection de la nav
  Mistral au seuil de 80 % est un problème distinct, non couvert ici).
- Décoder, réparer, réécrire ou reconstruire des URLs.
- Supprimer ou réécrire les libellés de liens, ou reformater le Markdown au-delà
  des destinations.
- Toucher aux extraits du dry-run, `suggestion.json`, `rapport-dry-run.md`,
  `cartographie.json` (borne héritée de la feature 004).
- Nettoyer les URLs dans les corpus où les lignes porteuses sont déjà supprimées
  par la détection (rien à faire : 0 destination absolue résiduelle dans les
  runs Exemple_1/Exemple_2).

## Success Metrics

- 0 ligne de `nettoye.md` et `nettoye-pagine.md` contenant une destination de
  lien absolue sur le corpus Exemple_3 (baseline : 6 lignes / 299 dans le run
  009).
- Sur Exemple_3, toute occurrence d'URL dans le corps du texte ou dans un bloc
  de code de l'entrée est retrouvée intacte dans la sortie (baseline : 0
  occurrence d'URL nue hors syntaxe de lien dans Exemple_3 — métrique à garde
  vide sur ce corpus, non vide sur un corpus à construire si le garde-fou est
  sollicité).
- Reste du texte inchangé octet par octet hors destinations retirées (baseline :
  comportement 004, vérifié par tests).
- Sorties inchangées octet par octet sur les corpus sans liens absolues dans le
  contenu conservé (Exemple_1, Exemple_2) — métrique qualitative de
  non-régression (baseline : runs 005/006).

## Cost of Inaction

Chaque run sur un corpus de documentation convertie où la détection ne supprime
pas la nav et le pied de page (type Exemple_3) produit un livrable avec ~2 % de
lignes à retoucher manuellement ; la retouche est répétitive, fragile (chaînes
de requête `utm_*` longues), et contredit le positionnement du livrable «
directement exploitable » déjà retenu comme critère lors de l'assessment 004. Le
corpus Exemple_3 étant désormais un exemple de référence du projet, le problème
se reproduira à chaque démonstration du fonctionnement de l'outil sur ce corpus.

## Open Questions

- [NEEDS CLARIFICATION: liste exacte des schémas visés — `https` seul, `http`
  inclus, ou tout schéma ; l'utilisateur a posé le principe de l'élargissement,
  pas la liste]
- [NEEDS CLARIFICATION: définition opérationnelle du garde-fou « URL
  explicitement indiquée dans le corps du texte » — les URLs nues et les blocs
  de code sont hors de la syntaxe de lien ; le cas difficile est le lien inline
  dans une explicitation de prose, non distinguable mécaniquement d'un débris de
  navigation sans critère discriminant]
- [NEEDS CLARIFICATION: traitement des formes `(<url> "titre")` (destination +
  titre, 21 lignes dans Exemple_2) — le titre est-il retiré, conservé, ou
  repositionné ?]
- [NEEDS CLARIFICATION: retrait activé par défaut (comme 004) ou opt-in, sachant
  que les destinations absolues sont valides et cliquables, contrairement aux
  chemins relatifs cassés visés par 004 ; interaction avec le drapeau de
  désactivation existant]
- [NEEDS CLARIFICATION: pourquoi la nav/pied de page du corpus Mistral n'est pas
  détectée comme motif récurrent au seuil de 80 % — si traitée séparément, elle
  rendrait secondaire le nettoyage des URLs absolues pour les lignes de
  navigation]
