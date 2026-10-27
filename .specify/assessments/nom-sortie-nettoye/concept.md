# Concept: Nommer les sorties d'après le document source

- **Slug**: nom-sortie-nettoye
- **Created**: 2026-10-05
- **Recommended option**: A — Renommage du fichier nettoyé dérivé de la source

## Options

### Option A — Renommage du fichier nettoyé dérivé de la source

- **Sketch**: Le fichier nettoyé d'un run s'appelle
  `<nom-dérivé-de-l'entrée>-nettoye.md` au lieu de `nettoye.md` : nom dérivé du
  document d'entrée (20 premiers caractères), espaces remplacées par `_`,
  suffixe `-1` ajouté en cas de collision, par ordre de traitement. Le reste de
  l'expérience (dossier de run, autres artefacts) est inchangé.
- **Appetite**: small (quelques jours)
- **Trade-offs**: répond directement au besoin exprimé (identifier la source par
  le nom du fichier) à coût minimal ; mais les autres sorties
  (`nettoye-pagine.md`, `cartographie.json`, `suggestion.json`,
  `rapport-dry-run.md`) restent génériques, et c'est un changement de
  comportement par défaut (chemins `nettoye.md` attendus par les usages
  existants à mettre à jour : tests, habitudes).
- **Rabbit holes**: normalisation des caractères (accents, ponctuation) — la
  fonction `slug_titre` existante remplace tout par `-`, elle ne satisfait pas
  la règle « espaces → `_` » ; troncature à 20 caractères sur des noms
  multi-octets ; interplay avec `--nom-titre` (le dossier de run et le fichier
  risquent de porter des noms dérivés différemment).

### Option B — Nommatage systématique de tous les artefacts du run

- **Sketch**: Tous les artefacts d'un run sont préfixés par le nom dérivé de
  l'entrée : `<nom>-nettoye.md`, `<nom>-nettoye-pagine.md`,
  `<nom>-cartographie.json`, `<nom>-suggestion.json`,
  `<nom>-rapport-dry-run.md`. Cohérence totale : chaque fichier du dossier de
  run traîne sa source.
- **Appetite**: small → medium (dizaines de jours-homme)
- **Trade-offs**: cohérence complète et une seule règle à documenter ; mais
  surface de changement plus large (CLI, tests d'intégration, contrat
  `contracts/cli.md`, documentation), gain marginal pour les artefacts
  secondaires que personne ne confond, et risque d'incohérence si `--nom-titre`
  nomme déjà le dossier différemment.
- **Rabbit holes**: chaque artefact renommé élargit les tests et la doc à
  toucher ; les chemins attendus dans `lire_suggestion` et le flux dry-run →
  suggestion doivent rester alignés.

### Option C — Ne rien construire : s'appuyer sur `--nom-titre` existant

- **Sketch**: Aucun changement. L'utilisateur utilise déjà `--nom-titre X` pour
  que le dossier de run porte le slug du titre ; le lien source ↔ sortie se fait
  par le nom du dossier, et l'utilisateur renomme `nettoye.md` à la main si
  besoin.
- **Appetite**: aucun
- **Trade-offs**: zéro coût ; mais le fichier lui-même reste générique (le nom
  le plus visible, celui qu'on copie ou partage hors du dossier), et le
  renommage manuel reste la source de friction que l'utilisateur demande
  précisément d'éliminer. De plus `slug_titre` remplace les espaces par `-`, pas
  `_`, et tronque au slug complet et non aux 20 premiers caractères du titre
  d'entrée.
- **Rabbit holes**: aucun, mais le problème tel que défini n'est pas résolu.

## Recommendation

Option A. Elle est la plus petite chose qui répond au problème énoncé (le
fichier nettoyé doit être reconnaissable sans ouvrir le dossier ni le fichier),
elle colle à l'exemple fourni par l'utilisateur, et son coût est faible.
L'option B n'apporte de la valeur que pour des artefacts rarement confondus ;
l'option C ne résout pas le problème.

## Out of Scope (for the recommended option)

- Renommage des autres artefacts du run (`nettoye-pagine.md`,
  `cartographie.json`, `suggestion.json`, `rapport-dry-run.md`) — inchangés.
- Logique de nommage des dossiers de run (numérotation séquentielle,
  `--nom-titre`) — inchangée.
- Traitement multi-documents en une invocation (FR-001, hors périmètre projet).
- Rétro-nommage des sorties déjà produites dans `output/`.

## Assumptions to Validate

- « Titre du document d'input » = nom de fichier (stem) de l'entrée, comme le
  suggère l'exemple (`retry-failed-records.md`), et non le premier titre `#` du
  contenu.
- Le nouveau nommage remplace le comportement par défaut (`nettoye.md`
  disparaît) ; aucun mode de repli exigé.
- La collision de noms ne peut survenir que dans un même dossier de destination
  (scénario rare avec les dossiers de run séparés) ; la règle `-1` par ordre de
  traitement s'applique alors au nom du fichier.
- Les caractères non espace (accents, ponctuation) restent tels quels ou
  subissent une normalisation à définir en spécification ; l'exemple ne tranche
  pas.
- Les tests et la documentation existants qui attendent le chemin `nettoye.md`
  sont mis à jour dans la même livraison.
