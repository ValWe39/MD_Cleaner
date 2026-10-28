# Bug Assessment: Balises et liens résiduels sur le corpus Le Grand Continent

- **Slug**: nettoyage-balises2
- **Created**: 2026-10-27
- **Source**: pasted text (message utilisateur) + corpus désigné :
  `Examples/Nettoyage-balises2/` (2 fichiers Le Grand Continent)
- **Verdict**: valid
- **Severity**: medium

## Report (verbatim or summarized)

> J'ai encore des balises dans des textes : cf. nouvel exemple ci-après.
> Je veux une démarche similaire à ce que l'on a fait dans cette discussion,
> avec les nouveaux cas d'exemple.
> `Examples/Nettoyage-balises2` (beaucoup de https notamment)

## Symptom

Après un run de la version courante (feature 009 incluse) sur les deux
fichiers du corpus `Examples/Nettoyage-balises2/`, les sorties conservent
33 liens de notes de bas de page avec destination, titre et HTML brut
(emportant la quasi-totalité des 55 URLs https résiduelles), plus un lien
de navigation par fichier dont la destination contient des espaces — le
livrable exige une retouche manuelle pour ce motif.

## Reproduction

1. `md-cleaner Examples/Nettoyage-balises2/legrandcontinent.eu--nettoye.md
   --sortie <dossier-temp>` (idem sur `-1.md`).
2. Constater dans la sortie : 24 (+9) liens
   `[1](#easy-footnote-... "… <a href=\"https://...\">…</a> …")` intacts ;
   `[Histoire en images](https://.../Histoire en images)` intact ; les
   images (15) et liens image-dans-label (13) intacts (conformes FR-003).
3. `grep -c easy-footnote` sur les sorties : 16 et 8 lignes concernées.

Vérifié le 2026-10-27 en rejouant la version courante : aucune de ces
formes n'est retirée.

## Suspected Code Paths

- `md_cleaner/nettoyage.py:RE_DESTINATION_SANS_CHEVRONS` — le motif de
  titre `(?: "[^"]*")?` ne matche pas un titre contenant un guillemet
  interne échappé (`\"`) : le match s'arrête au premier guillemet du
  HTML embarqué, la parenthèse fermante n'est jamais atteinte, la
  destination reste (limite documentée héritée de 005, D2).
- `md_cleaner/nettoyage.py:RE_DESTINATION_SANS_CHEVRONS` — la borne
  `[^)\s]*` exclut les espaces de la destination : le convertisseur
  produit des destinations non encodées avec espaces (Markdown invalide,
  ex. `](https://.../Histoire en images)`), non couvertes (borne D3 de
  009).

## Root Cause Hypothesis

Le convertisseur du corpus Le Grand Continent (WordPress, plugin
easy-footnote) produit deux formes que la règle 009 ne vise pas : des
liens de notes de bas de page dont le titre contient du HTML brut avec
guillemets échappés — forme légale en Markdown (titre à guillemet
échappé) que les arbitrages 004/005/009 avaient volontairement bornée
hors match (limite « guillemet interne échappé », faute d'occurrence
alors) — et des liens de navigation dont la destination contient des
espaces non encodés. La limite documentée devient matérielle à l'échelle
sur ce corpus : 33 occurrences de footnotes portant la quasi-totalité
des 55 https résiduels. Confiance : high (mesures directes sur corpus
et rejeu de la version courante).

## Proposed Remediation

**Preferred**: étendre la règle sans chevrons (009) sur deux points,
sans toucher la règle chevron (FR-005) ni les garde-fous : (1) motif de
titre acceptant les guillemets échappés — `"(?:[^"\\]|\\.)*"` au lieu de
`"[^"]*"` — pour que destination, titre, HTML embarqué et URLs des
footnotes soient emportés ensemble ; (2) branche alternative acceptant
des espaces dans la destination lorsque aucun titre ne suit
(alternative : branche titre d'abord, puis destination sans guillemet
`[^)"]*\)`), pour couvrir `](https://.../Histoire en images)`. Les
images et les URLs nues restent épargnées (contrats 009 inchangés).

**Alternatives**:

- Étendre aussi la règle chevron 004/005 au titre échappé (cohérence
  totale des deux règles) — coût : révision du comportement 004/005
  garanti octet par octet (FR-005) ; à arbitrer séparément, aucune
  occurrence chevron dans les corpus actuels.
- Ne corriger que les footnotes (forme A) et documenter les
  destinations à espaces comme limite — laisse 2 résidus par corpus
  Le Grand Continent.

**Files likely to change**:

- `md_cleaner/nettoyage.py`
- `tests/unit/test_nettoyage_liens.py`
- `tests/integration/test_nettoyage_liens.py`
- `specs/009-nettoyage-liens-sans-chevrons/` (contrat, research :
  bornes D2/D3 révisées)

**Tests to add or update**:

- Unitaires : footnote réel du corpus (titre échappé avec
  `<a href=\"https://...\">`), destination avec espaces, combinaison
  titre échappé + images sur la même ligne, idempotence,
  `--conserver-liens`, URLs nues et blocs de code intacts.
- Intégration : run sur les 2 fichiers de
  `Examples/Nettoyage-balises2/` (skip si absent) — 0 lien footnote
  résiduel, 0 destination à espaces, images intactes ; neutralité
  Exemple_1..3 et corpus FIPECO inchangée.

## Risks & Considerations

- Le motif de titre étendu peut matcher jusqu'au `")` le plus lointain
  sur un titre malformé (guillemets non appariés) — risque de retrait
  plus large que prévu sur entrées pathologiques ; à borner par tests.
- Accepter des espaces en destination rapproche la règle d'un
  mini-parseur Markdown (constitution IV) — borné par l'exclusion
  explicite des guillemets (un titre reste requis pour `"`).
- Les corpus historiques ne contiennent aucune de ces formes :
  non-régression attendue, à verrouiller par les tests de neutralité.

## Open Questions

- [NEEDS CLARIFICATION: Étendre aussi la règle chevron 004/005 au
  titre échappé (cohérence), ou strictement borner au 009 ?]
- [NEEDS CLARIFICATION: Les libellés de notes de bas de page
  résiduels (`[1]`) restent-ils tolérés (périmètre détection de
  motifs), comme arbitré en 009 ?]
