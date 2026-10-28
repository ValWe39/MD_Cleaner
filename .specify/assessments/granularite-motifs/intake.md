# Idea Intake: Plafonner le nombre de motifs détectés par requête (5-10)

- **Slug**: granularite-motifs
- **Created**: 2026-09-29
- **Source**: pasted text (discussion suite à l'analyse de
  `output/010/nettoye.md` sur un document ccomptes de 21 pages, 505 Ko)
- **Type**: improvement

## Idea (as captured)

> « peux-tu evaluer la faisablité de ce point. Pour avoir entre 5 à 10 bloc max
> par requête (plus facile pour éveluation manuelle, suffisament granulaire quand
> même). »

Contexte de la discussion qui précède : sur le document ccomptes, la détection
produit 2 motifs seulement ; le motif M02 agrège par fusion en chaîne 274 lignes
hétérogènes (barre de filtres, pagination, ET métadonnées de publications —
liens de thème et dates). Le toggle supprimer/conserver de la suggestion
s'applique au bloc entier, ce qui empêche de supprimer l'interface tout en
gardant les métadonnées des publications. Les pistes déjà évoquées dans la
conversation : bloquer le pontage par chevauchement minoritaire, distinguer
blocs compacts et éclatés, réduire W_MAX (fenêtres glissantes).

## Restated

Limiter le nombre de blocs (motifs) produits par exécution à une fourchette de 5
à 10 maximum, afin de rendre la validation manuelle du dry-run plus facile, tout
en conservant une granularité suffisante pour que chaque bloc soit homogène et
décidable indépendamment.

## Origin & Context

- **Raised by**: l'utilisateur (propriétaire du projet MD_Cleaner)
- **Trigger**: expérience concrète d'utilisation sur un document réel
  (`Web-Reader/output/output-016/consolidated.md`, listing Cour des comptes 21
  pages) : le dry-run n'a produit que 2 motifs, dont un (M02) chaînait des
  contenus de natures différentes, rendant la décision supprimer/conserver
  impossible à prendre de façon utile

## First-Glance Unknowns

- [NEEDS CLARIFICATION: le plafond 5-10 s'applique-t-il aux motifs supprimables
  seulement, ou à tous les motifs listés dans la suggestion (y compris sous le
  seuil) ?]
- [NEEDS CLARIFICATION: que faire quand un document produit naturellement plus
  de 10 motifs distincts — fusion forcée, troncature par priorité, ou
  avertissement ?]
- [NEEDS CLARIFICATION: l'objectif réel est-il le nombre de blocs, ou
  l'homogénéité de chaque bloc (les 2 motifs actuels sont-ils le problème, ou
  plutôt le fait que M02 mélange interface et métadonnées) ?]
- [NEEDS CLARIFICATION: quelles pages/patterns la validation manuelle doit-elle
  pouvoir distinguer — interface de navigation vs métadonnées récurrentes de
  contenu ?]
- [NEEDS CLARIFICATION: ce plafond doit-il être une constante du comportement
  par défaut, ou une option réglable (comme --seuil) ?]
