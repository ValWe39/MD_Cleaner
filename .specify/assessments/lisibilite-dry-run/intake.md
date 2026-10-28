# Idea Intake: Élargir l'extrait des motifs dans la suggestion

- **Slug**: lisibilite-dry-run
- **Created**: 2026-09-29
- **Source**: pasted text (retour d'utilisation après le dry-run de la feature
  002 sur Exemple_2)
- **Type**: improvement

## Idea (as captured)

> « Est-il envisageable d'indiquer au mois les 5 premières lignes de chaque bloc
> dans la rubrique "extrait" dans le json de suggestion ? Ou d'avoir une commande
> pour paramétrer le nombre de lignes à faire apparaître dans cet extrait ? Ce
> sera plus facile pour juger... »

Contexte d'utilisation : l'extrait actuel de chaque motif dans `suggestion.json`
et le rapport dry-run montre 3 lignes au plus, jointes par « / », avec les
lignes vides réduites à des séparateurs vides (ex. « / COUR DES COMPTES / ») —
insuffisant pour juger de la nature d'un motif, notamment les blocs éclatés de
la feature 002 (~25 motifs, dont les extraits se ressemblent). Deux variantes
sont proposées : relever le minimum à 5 lignes, ou exposer un paramètre de
nombre de lignes.

## Restated

Donner à l'utilisateur plus de contenu par motif dans l'extrait de la suggestion
(au moins 5 lignes) — soit par défaut, soit via un réglage du nombre de lignes
affichées — afin de faciliter le jugement supprimer/conserver au dry-run.

## Origin & Context

- **Raised by**: l'utilisateur (propriétaire du projet), retour d'usage concret
  sur les 25 motifs du dry-run de la feature 002 (Exemple_2 / listing ccomptes)
- **Trigger**: expérience de validation réelle : juger de la nature d'un motif
  sur 3 lignes (dont des vides) demande d'ouvrir le document source en
  parallèle, ce qui casse le flux de validation

## First-Glance Unknowns

- [NEEDS CLARIFICATION: la demande vise-t-elle le JSON de suggestion, le rapport
  dry-run, ou les deux — et le rapport en deux sections de la feature 002
  doit-il absorber la même amélioration ?]
- [NEEDS CLARIFICATION: la variante « commande pour paramétrer » entre en
  tension avec FR-010 de la feature 002 (aucune nouvelle option CLI) — faut-il
  lever cette contrainte ou préférer une simple constante par défaut relevée à 5
  ?]
- [NEEDS CLARIFICATION: l'extrait doit-il rester des lignes brutes jointes, ou
  un rendu plus lisible (numérotation, lignes vides représentées explicitement,
  troncature par longueur de ligne) ?]
- [NEEDS CLARIFICATION: quelle limite haute pour un extrait paramétré — le JSON
  de suggestion ne doit pas devenir un conteneur de contenu (le document source
  reste la référence) ?]
- [NEEDS CLARIFICATION: impact sur la taille des fichiers de sortie et sur le
  temps de validation < 5 min (SC-004/SC-006) sur les documents riches ?]
