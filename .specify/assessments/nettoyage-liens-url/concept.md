# Concept: Retirer les destinations de liens absolues des sorties nettoyées

- **Slug**: nettoyage-liens-url
- **Created**: 2026-10-05
- **Recommended option**: Option A — Extension de la passe existante aux
  destinations absolues

## Options

### Option A — Extension de la passe existante aux destinations absolues

- **Sketch**: l'utilisateur ne voit rien changer dans son usage : chaque run
  produit un `nettoye.md` / `nettoye-pagine.md` où, en plus des chemins relatifs
  `](</...>)` déjà retirés, les destinations absolues `](<https://...>)`,
  `](<http://...>)` (et les autres schémas retenus) disparaissent des lignes
  conservées, libellés et texte environnant intacts. Le drapeau de désactivation
  existant couvre l'ensemble. Une URL nue dans un extrait de code ou dans la
  prose n'est pas touchée : seule la syntaxe de destination de lien est visée,
  la garde-fou demandé est donc satisfait par construction pour ces cas.
- **Appetite**: small (une règle supplémentaire au point d'application déjà
  éprouvé par la feature 004, tests sur les trois corpus, documentation)
- **Trade-offs**: gagne : livrable directement exploitable sur Exemple_3
  (métrique 0 résiduel), cohérence avec le précédent 004, effort minime.
  sacrifie : les destinations absolues retirées sont valides et cliquables —
  l'utilisateur qui voudrait les garder doit utiliser le drapeau de
  désactivation global, qui réactive aussi les chemins relatifs (pas de
  granularité par schéma). risque : un lien inline inséré dans une explicitation
  de prose est indistinguable mécaniquement d'un débris de navigation — il
  serait retiré comme les autres (cas limite du garde-fou, non couvert par
  construction).
- **Rabbit holes**: vouloir distinguer « lien de prose légitime » de « débris de
  nav » par analyse de contexte (glissement vers de la détection sémantique) ;
  vouloir un drapeau par schéma ; vouloir traiter le sort des titres
  `(<url> "titre")` avec repositionnement du texte du titre en sortie.

### Option B — Même extension, mais opt-in via un drapeau dédié

- **Sketch**: le comportement par défaut ne change pas ; l'utilisateur qui veut
  nettoyer les destinations absolues ajoute un drapeau à l'invocation. Les
  sorties par défaut restent identiques à aujourd'hui.
- **Appetite**: small (même mécanique que A, plus un drapeau et son contrat CLI)
- **Trade-offs**: gagne : zéro risque pour les usages qui veulent des URLs
  cliquables ; réversible sans drapeau. sacrifie : le problème principal
  (retouche manuelle à chaque run par défaut) n'est pas résolu — la métrique « 0
  résiduel sur Exemple_3 » n'est atteinte que si l'utilisateur pense à passer le
  drapeau ; contredit l'exigence utilisateur formulée au research, qui demande
  le nettoyage comme comportement normal.
- **Rabbit holes**: multiplication des drapeaux (par schéma, par sortie) ;
  interaction avec `--conserver-liens` à définir en trois états.

### Option C — Attaquer la cause racine : la détection de la nav/pied de page

- **Sketch**: au lieu de nettoyer les URLs, faire en sorte que les lignes de nav
  et de pied de page du corpus type Exemple_3 soient captées comme motifs
  récurrents et supprimées entières — le livrable n'a alors plus ni URLs, ni
  libellés de navigation dégradés (`[]Docs & API`, `[Vibe][Studio]`...).
- **Appetite**: medium (investigation du pourquoi de la non-détection au seuil
  de 80 % sur segmentation heuristique 13 pages, ajustement de la détection ou
  du calibrage, risques de régression sur les corpus 1 et 2)
- **Trade-offs**: gagne : traite le vrai dégradé du livrable (les lignes de nav
  entières, pas seulement leurs URLs) ; les URLs absolues de nav disparaissent
  avec elles. sacrifie : effort et incertitude bien supérieurs (la recherche n'a
  pas établi pourquoi la nav n'est pas détectée) ; ne couvre pas une éventuelle
  destination absolue dans une ligne de contenu ; risque de faire régresser la
  détection sur les corpus existants.
- **Rabbit holes**: refonte du seuil/de la segmentation heuristique ; effet de
  bord sur les motifs M01-M04 du dry-run 008 ; remise en cause des features
  002/003 (granularité, distinctivité).

## Recommendation

**Option A.** Elle est la seule à tenir la métrique principale (0 destination
absolue résiduelle sur Exemple_3, baseline 6/299 au run 009) sans toucher à la
détection, dans l'appétit small et en cohérence avec le précédent 004 (une règle
déterministe par passe, au même point d'application). Le garde-fou exigé par
l'utilisateur est tenu par construction pour les cas majoritaires : une URL nue
dans un bloc de code ou en prose n'est pas une syntaxe de destination de lien et
n'est pas touchée (recherche : 0 URL nue dans Exemple_3). Le cas limite — lien
inline dans une prose explicative, indistinguable d'un débris de nav — est un
manque assumé de A, documenté et couvert par le drapeau de désactivation.
L'option C reste le traitement de fond mais engage un chantier distinct
(detection) hors de l'appétit de ce concept ; elle peut être poursuivie comme
assessment séparée sans perdre la valeur de A.

## Out of Scope (for the recommended option)

- Tout changement de la détection de motifs, du seuil, ou de la segmentation
  (cause racine de la survie de la nav — assessment distinct possible).
- Décodage, réparation, réécriture ou reconstruction d'URLs.
- Réécriture des libellés de liens ou reformatage Markdown au-delà des
  destinations.
- Extraits du dry-run, `suggestion.json`, `rapport-dry-run.md`,
  `cartographie.json` (borne héritée de 004).
- Granularité par schéma (un drapeau par famille d'URL) : un seul comportement
  global.
- Distinction « lien de prose légitime » vs « débris de navigation » par analyse
  de contexte.

## Assumptions to Validate

- Toutes les destinations absolues à nettoyer sont sous forme chevron `](<...>)`
  ; aucune forme `](https://...)` sans chevrons n'a été observée dans les trois
  corpus (à confirmer à la spécification).
- ~~Le retrait d'un titre `(<url> "titre")` en même temps que la destination~~
  **Tranché par l'utilisateur (2026-10-05)** : le titre est conservé dans la
  sortie — seule la destination est retirée. **Révisé au specify (2026-10-05)**
  : seuls les libellés survivent ; destination et titre du lien sont retirés
  ensemble.
- ~~Le drapeau de désactivation existant (`--conserver-liens`) couvre aussi les
  destinations absolues, sans nouveau drapeau~~ **Tranché par l'utilisateur
  (2026-10-05)** : oui, intégration dans le même drapeau `--conserver-liens`,
  pas de nouveau drapeau.
- Les 21 destinations `http` non-https d'Exemple_2 sont bien toutes dans des
  motifs supprimés (mesure research : 0 résiduel dans les runs 004/006 — pas de
  comportement observable à attendre sur ce corpus).
- Le corpus Exemple_3 ne contient aucune URL nue dans le corps (mesuré : vrai
  aujourd'hui) — le garde-fou n'est pas sollicité sur les corpus de référence,
  sa validation reposera sur des tests construits, pas sur un corpus réel.
