# Problem Definition: Blocs de motifs indivisibles au dry-run

- **Slug**: granularite-motifs
- **Created**: 2026-09-29
- **Inputs used**: intake.md + research.md

## Problem Statement

Sur certains documents (listings, catalogues à métadonnées
récurrentes), la détection chaîne des zones de natures différentes —
interface de navigation et métadonnées de contenu — dans un **seul
motif indivisible** ; l'utilisateur qui valide le dry-run ne peut donc
prendre qu'une décision tout-ou-rien sur un bloc hétérogène, ce qui
rend le nettoyage impossible à piloter utilement sur cette classe de
documents.

## Affected Users & Stakeholders

- **Users** : l'utilisateur de md-cleaner qui valide un dry-run — il
  doit pouvoir dire « supprime l'interface, garde les métadonnées des
  publications », ce que le bloc M02 actuel (279 lignes, 7 intervalles
  disjoints, interface + métadonnées) ne permet pas (source :
  research.md, mesures output-016)
- **Stakeholders** : le propriétaire-mainteneur du projet — arbitre la
  complexité algorithmique contre la simplicité (constitution IV) ;
  le futur consommateur RAG — bénéficie indirectement de sorties
  correctement nettoyées

## Goals

- Chaque motif proposé au dry-run est **décidable indépendamment** :
  il regroupe des lignes d'une même nature structurelle, sans mélanger
  interface et métadonnées de contenu
- La charge de validation humaine reste **bornée et prévisible** pour
  un document (l'ordre de grandeur visé par l'utilisateur : une
  dizaine de décisions tout au plus — à distinguer d'un plafond dur)
- Le comportement reste **déterministe** (FR-005) et les critères de
  succès existants (SC-001, SC-002, SC-004, SC-005) ne régressent pas

## Non-Goals

- Pas d'introduction de dépendances (pas de parseur DOM, pas de
  modèle statistique ou neuronal) — l'entrée reste des lignes
  markdown traitées en stdlib (constitution II, III, IV)
- Pas de sélection manuelle ligne à ligne dans le dry-run (hors
  périmètre : le grain de décision reste le bloc)
- Pas de changement de la sémantique de nettoyage (supprimer /
  conserver) ni du format des sorties (nettoye.md, paginé, carto)
- Pas de recherche de précision parfaite : l'objectif est la
  décidabilité, pas l'exactitude automatique totale

## Success Metrics

- Sur output-016 (document déclencheur), la zone filtres/pagination et
  la zone métadonnées de publications appartiennent à des motifs
  distincts après un dry-run (baseline : un seul motif M02 aujourd'hui)
  — critère binaire, mesurable mécaniquement
- Le nombre de motifs par document du corpus réel (Exemple_1,
  Exemple_2, output-016) reste dans un intervalle borné dont les
  bornes restent à définir (baseline : 4 / 2 / 2 motifs ; cible
  indicative : pas plus d'une quinzaine, ordre de grandeur validable
  en < 5 min conformément à SC-004)
- Aucune régression sur Exemple_1 et Exemple_2 : contenu unique
  conservé à 100 % (SC-005), déterminisme octet par octet (SC-002)
  — vérifié par la suite de tests existante
- [NEEDS CLARIFICATION: métrique mesurable d'« homogénéité » d'un
  motif à définir en specification (dispersion des intervalles ?
  profil de densité de liens ? autre proxy ?)]

## Cost of Inaction

Sur la classe de documents à métadonnées récurrentes, l'utilisateur
doit choisir entre deux mauvaises options : conserver le bloc entier
(l'interface pollue la sortie — cas constaté au run 010) ou le
supprimer (les métadonnées des publications disparaissent). Le dry-run
perd sa valeur sur ces documents, la confiance dans la boucle de
validation humaine s'érode, et la qualité des corpus pour le RAG aval
en pâtit. Le corpus actuel est petit (3 documents, 1 cas douloureux),
donc la douleur est réelle mais encore peu fréquente.

## Open Questions

- [NEEDS CLARIFICATION: quelle définition mesurable de l'« homogénéité
  » d'un bloc — et le nombre de blocs en est-il un proxy acceptable
  ou un leurre (cf. research.md : comptages actuels 2-4, déjà sous
  la cible 5-10) ?]
- [NEEDS CLARIFICATION: la cible « 5 à 10 blocs » de l'intake
  survit-elle comme contrainte de charge de validation, ou est-elle
  abandonnée au profit du seul critère d'homogénéité ?]
- [NEEDS CLARIFICATION: que faire d'un document produisant
  naturellement plus de zones récurrentes distinctes que la borne
  visée — regroupement, troncature, avertissement ?]
- [NEEDS CLARIFICATION: réglage par défaut ou option CLI, et
  interaction avec --seuil et la stabilité des ids de motifs entre
  exécutions (contrat suggestion.json) ?]
