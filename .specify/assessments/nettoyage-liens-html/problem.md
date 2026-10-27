# Problem Definition: Destinations de liens illisibles qui dégradent la sortie

- **Slug**: nettoyage-liens-html
- **Created**: 2026-10-02
- **Inputs used**: intake.md | research.md

## Problem Statement

L'utilisateur de MD_Cleaner lance l'outil pour obtenir un document Markdown
directement lisible et exploitable (lecture, RAG) ; or la sortie conservée
contient encore, collées au texte utile, des destinations de liens résiduelles
de la forme `(</...>)` — ~31 % des lignes de la sortie réelle du run 004 (527
sur 1724). Le nettoyage actuel retire des lignes entières mais ne nettoie jamais
l'intérieur des lignes conservées, si bien que le livrable final reste pollué
par des débris de conversion HTML → Markdown inexploitables (URL relatives,
caractères encodés) que l'utilisateur doit retoucher à la main après chaque run.

## Affected Users & Stakeholders

- **Users**: l'utilisateur unique connu de l'outil (propriétaire du projet) — il
  doit post-traiter manuellement chaque `nettoye.md` pour supprimer ces
  destinations avant de lire ou d'ingérer le document ; le bénéfice promis «
  sortie directement exploitable » n'est pas tenu sur les corpus à liens inline
  (listings, catalogues). [NEEDS CLARIFICATION: existence d'autres utilisateurs
  du dépôt public]
- **Stakeholders**: le propriétaire du projet — décideur unique, juge de la
  conformité à la constitution du projet (local-first, déterminisme, stdlib) ;
  les consommateurs en aval de la sortie (lecteurs humains, pipeline RAG) —
  impactés par la qualité textuelle du livrable sans voix dans la décision.

## Goals

- Une sortie `nettoye.md` où le texte utile des lignes conservées est lisible
  sans débris de conversion collés au libellé (les libellés de liens restent
  lisibles).
- Zéro retouche manuelle post-run nécessaire pour éliminer ces destinations sur
  le corpus Cour des comptes (Exemple_2) et le corpus Exemple_1.
- La perte d'information reste maîtrisée et explicite : rien d'autre que ces
  destinations n'est modifié dans les lignes concernées.
- Comportement réversible/paramétrable par l'utilisateur, pour qui dépend des
  liens cliquables dans certains usages.

## Non-Goals

- Supprimer ou modifier le texte des libellés, dates, marqueurs d'institution ou
  tout autre contenu des lignes concernées.
- Retirer des lignes entières supplémentaires (la détection supprimer/conserver
  des motifs existants n'est pas rejugée).
- Définir, décoder ou restructurer les URL (décodage des `%5B`/`%3A`,
  reconstruction d'URL absolues) — les destinations sont retirées, pas réparées.
- Étendre le nettoyage à de vraies balises HTML, aux sorties
  `cartographie.json`/`suggestion.json`, ou à un reformatage Markdown général du
  document.

## Success Metrics

- Proportion de lignes de la sortie contenant une destination `(</...>)` : 0
  (mesure grep) sur le run équivalent au 004 avec Exemple_2 (baseline : 527/1724
  lignes, ~31 %).
- Le reste du texte des lignes concernées est inchangé octet par octet en dehors
  des destinations retirées (baseline : non mesuré, à encadrer en
  spécification).
- Temps de retouche manuelle post-run de l'utilisateur pour ce motif : nul
  (baseline : retouche manuelle à chaque run — qualitatif).
- Sorties de l'outil inchangées sur les corpus sans liens inline (Exemple_1 hors
  `[CORSEN AI](</fr/>)` — à qualifier en spécification).

## Cost of Inaction

L'utilisateur continue de post-traiter chaque sortie à la main (fragile,
répétitif, contredit le positionnement « une commande, sortie directement
exploitable » du README) ; ~31 % des lignes du livrable 004 restent polluées ;
la valeur de la sortie pour un pipeline RAG en aval reste dégradée sur toute la
classe de documents à liens inline (listings, catalogues). Les corpus sans ce
motif ne sont pas pénalisés et la situation n'évolue pas d'elle-même.

## Open Questions

- [NEEDS CLARIFICATION: forme exacte du résultat sur une ligne : destination
  seule retirée (`[libellé]` conservé tel quel) ou lien entier réduit au libellé
  nu ?]
- [NEEDS CLARIFICATION: périmètre des destinations visées : uniquement la forme
  chevron `(</...>)`, ou aussi les destinations absolues `](http...)` ?]
- [NEEDS CLARIFICATION: appliqué avant ou après la détection des motifs — impact
  sur les ids M01…, les extraits du dry-run et les décisions des features
  002/003 qui s'appuient sur les liens de thème ?]
- [NEEDS CLARIFICATION: quelle(s) sortie(s) sont concernées : `nettoye.md` seul,
  ou aussi `nettoye-pagine.md` (en préservant les marqueurs `<!-- page: N -->`
  produits par l'outil) ?]
- [NEEDS CLARIFICATION: valeur par défaut (activée) et nom du drapeau de
  désactivation — premier paramètre « activé par défaut » de l'outil, pattern UX
  inédit + migration des tests existants ?]
- [NEEDS CLARIFICATION: suppression brute des caractères encodés (`%5B`, `%3A`)
  sans décodage, confirmée par l'utilisateur ?]
- [NEEDS CLARIFICATION: existence d'autres utilisateurs ou usages du dépôt qui
  dépendraient des liens cliquables dans la sortie ?]
