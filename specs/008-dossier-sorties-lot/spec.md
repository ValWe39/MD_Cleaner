# Feature Specification: Un dossier de sorties partagé pour les documents d'un même lot

**Feature Branch**: `008-dossier-sorties-lot`

**Created**: 2026-10-05

**Status**: Draft

**Input**: Handoff de l'assessment `dossier-sorties-lot` (verdict go, option A « dossier de run par invocation, sorties à plat ») — « Est-il possible que les éléments traités en une seule invocation apparaissent dans le même sous-dossier d'output ? » ; addendum : « Je ne veux qu'un seul 00X avec mes deux outputs. »

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Un seul dossier de run par invocation (Priority: P1)

L'utilisateur lance `md-cleaner doc1.md doc2.md`. L'outil crée **un
seul** sous-dossier numéroté dans `output/` (`00X`) et y écrit les
sorties nettoyées des deux documents, côte à côte. La numérotation
séquentielle consomme un numéro pour toute l'invocation ; l'invocation
suivante prendra `00X+1`. Les messages console par document (`Sortie :
...`) restent inchangés.

**Why this priority**: C'est la demande elle-même (addendum de
l'intake) : retrouver les sorties d'une invocation en un seul endroit
identifiable.

**Independent Test**: Invocable avec les 3 exemples de référence du
projet ; vérifiable par l'existence d'un unique dossier de run
contenant 3 sorties nettoyées.

**Acceptance Scenarios**:

1. **Given** un lot de 3 documents, **When** `md-cleaner doc1.md doc2.md doc3.md`, **Then** exactement 1 sous-dossier de run est créé dans `output/`, contenant 3 fichiers `<stem>-nettoye.md` (règle de nommage 006 inchangée par document).
2. **Given** deux documents de stems identiques dans un même lot, **When** invocation, **Then** deux sorties distinctes (`consolidated-nettoye.md` et `consolidated-nettoye-1.md`), jamais d'écrasement (mécanisme existant, à l'échelle du dossier partagé).
3. **Given** une invocation mono-document, **When** `md-cleaner doc.md`, **Then** la structure de sortie est strictement identique à aujourd'hui : un dossier `00X` contenant `doc-nettoye.md`.
4. **Given** deux invocations successives (lot, puis autre invocation), **When** la seconde invocation se termine, **Then** son dossier de run porte le numéro suivant le lot — la numérotation consomme un numéro par invocation.

---

### User Story 2 - Sorties secondaires attribuables par document (Priority: P2)

L'utilisateur lance un lot de plusieurs documents avec `--pagine`.
Chaque document produit ses sorties paginées **préfixées par son nom
dérivé** dans le dossier partagé : `<stem>-nettoye-pagine.md` et
`<stem>-cartographie.json` — chaque artefact reste attribuable à son
document. En lot d'un seul document (comme en mono-document), les
noms courts actuels (`nettoye-pagine.md`, `cartographie.json`)
demeurent la règle.

**Why this priority**: Sans ce mécanisme, les sorties secondaires à
nom fixe s'écraseraient mutuellement dans le dossier partagé — la
valeur de US1 ne tient que si aucune sortie n'est perdue.

**Independent Test**: Invocable avec un lot de 2 documents et
`--pagine` ; vérifiable par l'existence de 2 paires
`<stem>-nettoye-pagine.md` / `<stem>-cartographie.json` distinctes et
lisibles.

**Acceptance Scenarios**:

1. **Given** un lot de 2 documents avec `--pagine`, **When** invocation, **Then** le dossier de run contient 4 sorties secondaires : `<stem1>-nettoye-pagine.md`, `<stem1>-cartographie.json`, `<stem2>-nettoye-pagine.md`, `<stem2>-cartographie.json`.
2. **Given** une invocation mono-document avec `--pagine`, **When** invocation, **Then** les noms restent `nettoye-pagine.md` et `cartographie.json` (inchangés).
3. **Given** deux documents de stems identiques dans un lot avec `--pagine`, **When** invocation, **Then** les sorties secondaires sont désambiguïsées par le même mécanisme anti-collision que les sorties nettoyées, jamais écrasées.

---

### User Story 3 - Comportements bornés du dossier de lot (Priority: P3)

Le dossier de run est créé une fois par invocation, avant la boucle de
traitement. Un lot dont certains documents échouent conserve les
sorties des documents réussis, sans annulation ni marqueur — le code
retour (1) et la trace stderr documentent l'échec (sémantique 007
inchangée). Un lot dont tous les documents échouent laisse le dossier
de run vide en place, comportement déterministe documenté.

**Why this priority**: Ces cas bornent le contrat du dossier partagé
(échec partiel, échec total) pour qu'aucun comportement ne soit
indéfini ; moins critique que US1/US2 car exceptionnels.

**Independent Test**: Invocable avec un lot contenant un document
invalide entre deux valides ; vérifiable par les sorties conservées,
le code retour 1 et l'absence de marqueur.

**Acceptance Scenarios**:

1. **Given** un lot [doc1 valide, doc2 invalide, doc3 valide], **When** invocation, **Then** le dossier de run unique contient les sorties de doc1 et doc3, l'échec de doc2 est signalé sur stderr (`ERREUR : ...`), code retour 1, aucun marqueur de lot incomplet.
2. **Given** un lot dont tous les documents échouent (avant tout arrêt par fail-fast), **When** invocation, **Then** le dossier de run numéroté existe et est vide, code retour 1.
3. **Given** un lot interrompu par le fail-fast (3 échecs consécutifs), **When** invocation, **Then** les sorties des documents déjà traités sont conservées dans le dossier de run unique, les documents suivants ne sont pas traités (sémantique 007 inchangée).

---

### User Story 4 - Nom du dossier de lot avec --nom-titre (Priority: P4)

En lot de plusieurs documents, l'option `--nom-titre` ne peut plus
nommer le dossier d'après « le » titre du document (chaque document a
le sien). Elle est neutralisée avec un avertissement explicite (arbitrage
utilisateur du 2026-10-05, par symétrie avec la neutralisation 007 de
`--dry-run`/`--suggestion`) : le dossier de lot prend la numérotation
séquentielle seule. En mono-document, l'option reste pleinement
fonctionnelle, strictement inchangée.

**Why this priority**: Le seul point du contrat resté ouvert par la
décision ; il doit être défini pour que le contrat du dossier de lot
soit complet, mais n'affecte pas la valeur principale.

**Independent Test**: Invocable avec un lot de 2 documents et
`--nom-titre 30` ; vérifiable par le nom du dossier créé et la
présence (ou l'absence) d'un avertissement.

**Acceptance Scenarios**:

1. **Given** un lot de 2 documents avec `--nom-titre 30`, **When** invocation, **Then** un avertissement explicite est affiché sur stderr (`--nom-titre` ignorée en lot), le dossier de run prend la numérotation séquentielle seule, et le lot est traité normalement.
2. **Given** une invocation mono-document avec `--nom-titre 30`, **When** invocation, **Then** le dossier de run est nommé d'après le titre du document, strictement comme aujourd'hui, sans avertissement.

---

### Edge Cases

- Stems identiques après troncature à 20 caractères (règle 006) : deux documents distincts peuvent produire le même nom dérivé — le suffixe anti-collision existant (`-1`, `-2`) s'applique à toutes les sorties (nettoyées, paginées, cartographies), jamais d'écrasement.
- Dossier source d'un lot contenant un document déjà traité dans la même invocation (doublon) : chaque occurrence produit sa sortie dans le dossier partagé, suffixée par le mécanisme existant (007 inchangé).
- Lot vide (aucun document retenu, ex. dossier sans `.md`) : aucun dossier de run n'est créé (erreur code 1 avant toute création — 007 inchangé).
- `--nom-titre` avec un document sans titre de niveau 1 (`#`) :
  comportement actuel conservé (fallback sur le stem), inchangé.
- Ordre des sorties dans le dossier partagé : ordre de traitement déterministe de 007 (ordre d'apparition, tri par nom dans un dossier) — inchangé et désormais observable au sein d'un même dossier.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Toute invocation d'une ou plusieurs entrées DOIT produire exactement un dossier de run dans le dossier racine `--sortie`, créé une seule fois, quel que soit le nombre de documents du lot ; la numérotation séquentielle DOIT consommer un numéro par invocation (et non par document).
- **FR-002**: Les sorties nettoyées de tous les documents du lot DOIVENT être écrites dans ce dossier unique, chacune nommée selon la règle 006 (`<nom-dérivé>-nettoye.md`) ; les collisions DOIVENT être résolues par le suffixe anti-collision existant, jamais par écrasement.
- **FR-003**: En lot de plusieurs documents, les sorties de `--pagine` DOIVENT être préfixées par le nom dérivé du document (règle 006) : `<nom-dérivé>-nettoye-pagine.md` et `<nom-dérivé>-cartographie.json` ; en lot d'un seul document, les noms courts actuels (`nettoye-pagine.md`, `cartographie.json`) DOIVENT être conservés.
- **FR-004**: L'invocation mono-document DOIT rester strictement identique au comportement actuel : un dossier de run, mêmes noms pour tous les artefacts (y compris courts pour `--pagine`), même numérotation, mêmes messages.
- **FR-005**: En lot de plusieurs documents, `--nom-titre` DOIT être neutralisée avec un avertissement explicite sur stderr (le dossier prend la numérotation séquentielle seule), jamais appliquée partiellement ni ignorée en silence ; en mono-document, l'option DOIT rester pleinement fonctionnelle et inchangée.
- **FR-006**: Un lot avec échecs DOIT conserver dans le dossier de run unique les sorties des documents traités avec succès ; aucun artefact ne DOIT être annulé ; aucun marqueur de lot incomplet ne DOIT être introduit dans ce périmètre.
- **FR-007**: Un lot dont aucun document n'a été traité avec succès DOIT laisser le dossier de run vide en place (créé en tête d'invocation), sans sortie partielle ambiguë — comportement déterministe documenté.
- **FR-008**: Un lot vide (aucun document retenu à la résolution) NE DOIT PAS créer de dossier de run (erreur d'entrée code 1, 007 inchangé).
- **FR-009**: L'ordre de traitement, la résolution du lot, la neutralisation de `--dry-run`/`--suggestion`, la signalisation des échecs (`ERREUR : ...`), le fail-fast au troisième échec consécutif et les codes retour (007) DOIVENT rester inchangés.
- **FR-010**: Les messages console par document (`Sortie : ...`, `Sortie paginée : ...`, `Cartographie : ...`) DOIVENT refléter les chemins réels dans le dossier partagé et rester au format actuel ; aucun résumé de lot n'est produit.

### Key Entities *(include if feature involves data)*

- **Dossier de run** : unique par invocation, créé en tête (numérotation séquentielle à la racine `--sortie`, ou nommage par titre en mono-document) ; contient toutes les sorties du lot. Un lot entièrement en échec le laisse vide ; un lot vide ne le crée pas.
- **Sortie nettoyée** : `<nom-dérivé>-nettoye.md` par document (règle 006, inchangée) ; l'unicité au sein du dossier de lot est garantie par le suffixe anti-collision.
- **Sortie secondaire préfixée** : `<nom-dérivé>-nettoye-pagine.md` et `<nom-dérivé>-cartographie.json` par document en lot de plusieurs ; noms courts en lot d'un. Le préfixe est le nom dérivé du document (même règle de troncature/normalisation que 006).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Une invocation de K documents produit exactement 1 dossier de run contenant K sorties nettoyées (vérifié sur les 3 exemples de référence ; baseline : 3 dossiers aujourd'hui).
- **SC-002**: Deux documents de stems identiques dans un même lot produisent deux sorties nettoyées distinctes et deux paires de sorties secondaires distinctes, sans aucun écrasement.
- **SC-003**: Le mono-document est strictement inchangé : la suite de tests existante passe sans relâchement, y compris les noms d'artefacts et la numérotation.
- **SC-004**: En lot de plusieurs avec `--pagine`, chaque document est attribuable : ses sorties nettoyées, paginée et cartographie partagent son préfixe de nom dérivé (baseline : impossible aujourd'hui — noms fixes).
- **SC-005**: La numérotation séquentielle consomme un numéro par invocation (baseline : un par document).
- **SC-006**: Les contrats révisés (007 multi-entrees FR-003/FR-011, table des artefacts de 001, README) décrivent le dossier partagé, sans divergence documentaire résiduelle.

## Assumptions

- Le préfixe des sorties secondaires en lot est le nom dérivé du
  document (règle 006 : 20 premiers caractères, espaces remplacées,
  troncature), soit exactement le stem du fichier nettoyé du même
  document — une seule règle de nommage à connaître.
- La divergence de nommage assumée entre lot d'un document (noms
  courts) et lot de plusieurs (préfixés) est retenue pour préserver
  la rétrocompatibilité mono-document sans re-toucher aux tests
  existants du mono (decision.md : Out of scope).
- Le dossier de run est créé en tête d'invocation, après la
  résolution du lot et les neutralisations (donc jamais pour un lot
  vide), avant la boucle de traitement.
- Aucun marquage de lot incomplet : l'information vit dans le code
  retour et la trace stderr (decision.md : Out of scope).
- La migration des ~9 assertions de `tests/integration/test_lot.py`,
  la révision des contrats 007/001 et du README se font dans la même
  livraison (précédent 006 : D6 du plan 006).
- L'ordre des sorties dans le dossier partagé est l'ordre de
  traitement déterministe de 007 — aucun tri supplémentaire.
