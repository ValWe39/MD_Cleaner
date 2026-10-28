# Feature Specification: Nettoyage des destinations de liens sans chevrons

**Feature Branch**: `009-nettoyage-liens-sans-chevrons`

**Created**: 2026-10-27

**Status**: Draft

**Input**: Handoff de l'assessment `nettoyage-balises` (decision.md, verdict
go du 2026-10-27, option A confirmée par l'utilisateur) : les sorties du
corpus FIPECO conservent 199 destinations de liens sans chevrons
(`](/chemin)`, `](#ancre)`, `](https://...)`) collées au texte utile, la
passe établie par les features 004/005 ne visant que les formes entre
chevrons. Option retenue : étendre la passe d'écriture à toute destination
sans chevrons, sans cas particulier, libellés conservés, images épargnées,
réversible par `--conserver-liens`.

## Clarifications

### Session 2026-10-27

- Q: Le nettoyage s'applique-t-il uniquement aux sorties livrables
  (`nettoye.md`, `nettoye-pagine.md`) ou aussi aux artefacts de travail ?
  → A: Uniquement aux sorties livrables (précédent 004 reconduit) ;
  l'extrait lisible du dry-run et les artefacts de suggestion restent
  intacts.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Sortie finale sans destinations sans chevrons (Priority: P1)

Un utilisateur lance le nettoyage d'un document Markdown issu d'une
conversion HTML → Markdown dont les liens utilisent la forme sans chevrons
(typiquement le corpus FIPECO). Sans réglage particulier, le `nettoye.md`
produit ne contient plus aucune destination de lien sans chevrons :
les libellés et le reste du texte des lignes conservées restent lisibles et
inchangés. Il n'a plus de retouche manuelle à faire pour ce motif.

**Why this priority**: C'est la valeur centrale du handoff : tenir la
promesse « sortie directement exploitable » sur le corpus FIPECO. C'est la
métrique mesurée (0 destination résiduelle contre 199 occurrences sur 5
fichiers, 34 à 47 par fichier).

**Independent Test**: Testable en rejouant le nettoyage des 5 fichiers du
corpus de calibration et en vérifiant qu'aucune ligne de la sortie ne
contient de destination `](...)` sans chevrons, alors que les libellés
(ex. « *crédit d'impôt* », « une note ») et l'ordre des lignes sont
inchangés.

**Acceptance Scenarios**:

1. **Given** un document contenant un lien relatif sans slash
   `[*crédit d'impôt*](Les-crédits-dimp...)`, **When** l'utilisateur
   lance le nettoyage sans option, **Then** la sortie contient
   `*crédit d'impôt*` et ne contient plus la destination.
2. **Given** un document contenant un lien d'ancre
   `[Revenir en haut de page](#haut)`, **When** le nettoyage est lancé,
   **Then** la sortie contient `[Revenir en haut de page]` sans
   `(#haut)`.
3. **Given** un document contenant un lien absolu
   `[une note](https://www.imf.org/...)`, **When** le nettoyage est
   lancé, **Then** la sortie contient `une note` sans destination.
4. **Given** les 5 fichiers du corpus de calibration, **When** le
   nettoyage est lancé, **Then** aucune ligne des sorties ne contient de
   destination sans chevrons (baseline : 199 occurrences).

---

### User Story 2 - Réversibilité par --conserver-liens (Priority: P2)

Un utilisateur qui veut des liens cliquables dans le document final lance
le nettoyage avec le drapeau `--conserver-liens` : les sorties sont
identiques octet par octet au comportement antérieur à la feature,
destinations comprises, dans les deux artefacts (`nettoye.md`,
`nettoye-pagine.md`).

**Why this priority**: Le comportement par défaut change la sortie pour
tous les runs ; la réversibilité explicite est la condition
d'acceptabilité du changement (précédents 004/005).

**Independent Test**: Testable en lançant le même run avec
`--conserver-liens` et en comparant les sorties octet par octet à des
sorties produites sans la feature.

**Acceptance Scenarios**:

1. **Given** un document avec liens sans chevrons, **When** le nettoyage
   est lancé avec `--conserver-liens`, **Then** les destinations restent
   intactes dans `nettoye.md`.
2. **Given** le même run avec sortie paginée, **When** `--conserver-liens`
   est actif, **Then** `nettoye-pagine.md` conserve destinations et
   marqueurs de page à l'identique.

---

### User Story 3 - Garde-fous : images, URLs nues, blocs de code (Priority: P3)

Un utilisateur nettoie un document contenant des images
(`![](/images/FIV11a.png)`, logo imbriqué `[![FIPECO](/images/logo.jpg)]
(/)`), des URLs nues dans le corps du texte et des blocs de code. Le
nettoyage n'altère aucune image (destination comprise) ni aucune URL nue
ou bloc de code : ils restent présents, intacts, dans la sortie.

**Why this priority**: L'exigence utilisateur explicite « sans enlever du
contenu d'intérêt » prime sur le gain cosmétique ; les contrats 005 sont
reconduits. Les résidus tolérés (crochets autour d'un logo, libellés de
navigation seuls) sont documentés et relèvent du périmètre détection de
motifs.

**Independent Test**: Testable en construisant un document avec image,
logo imbriqué, URL nue et bloc de code, et en vérifiant que chacun est
retrouvé intact dans la sortie, le logo étant réduit à son image
(destination externe retirée).

**Acceptance Scenarios**:

1. **Given** une ligne `![](/images/FIV11a.png)Sources : ...`, **When** le
   nettoyage est lancé, **Then** la ligne est inchangée octet par octet.
2. **Given** un logo `[![FIPECO](/images/logo.jpg)](/)` en pied de page,
   **When** le nettoyage est lancé, **Then** la sortie contient
   `[![FIPECO](/images/logo.jpg)]` — destination externe retirée, image
   conservée.
3. **Given** une URL nue hors syntaxe de lien ou un bloc de code,
   **When** le nettoyage est lancé, **Then** ils restent intacts
   (contrats 005 reconduits).

---

### User Story 4 - Non-régression sur les formes et corpus existants (Priority: P4)

Un utilisateur rejoue le nettoyage des corpus historiques (Exemple_1 à
Exemple_3) : les sorties sont inchangées octet par octet, et les
destinations entre chevrons continuent d'être retirées exactement comme
avant la feature.

**Why this priority**: La règle étendue touche une passe qui traite déjà
5 314 destinations chevrons sur les corpus historiques ; la garantie de
non-régression est le garde-fou exigé par la décision.

**Independent Test**: Testable en rejouant les runs des corpus
Exemple_1..3 et en comparant les sorties octet par octet aux sorties de
référence produites avec la seule feature 005.

**Acceptance Scenarios**:

1. **Given** un corpus sans forme sans chevrons (Exemple_1..3), **When**
   le nettoyage est lancé, **Then** les sorties sont identiques octet par
   octet aux sorties de référence.
2. **Given** une destination entre chevrons `](<...>)`, **When** le
   nettoyage est lancé, **Then** elle est retirée comme avant la feature
   (libellé conservé, titre emporté).

---

### Edge Cases

- Destination vide : `[Ressources](#)` — la destination `(#)` est
  retirée, le libellé `[Ressources]` reste.
- Plusieurs liens sans chevrons sur une même ligne : chaque destination
  est retirée, chaque libellé reste dans l'ordre.
- Note de bas de page : `[[1]](#_ftn1)` devient `[[1]]` — le libellé
  résiduel est conservé (périmètre détection de motifs pour la suite).
- Forme à titre `](url "titre")` sans chevrons : destination et titre
  emportés ensemble (arbitrage 005 reconduit ; 0 occurrence dans le
  corpus).
- Ligne entièrement constituée d'un lien : conservée avec son libellé
  seul (précédent 004).
- Libellé vide sur un lien textuel : la destination est retirée, le
  libellé vide reste (précédent 004).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Dans les seules sorties livrables (`nettoye.md` et
  `nettoye-pagine.md`), le nettoyage DOIT retirer à l'écriture toute
  destination de lien inline sans chevrons, quel que soit son schéma
  (ancre, chemin relatif avec ou sans slash initial, URL absolue), sans
  cas particulier.
- **FR-002**: Le nettoyage DOIT conserver le libellé et le reste du texte
  de chaque ligne, inchangés hors destinations.
- **FR-003**: Le nettoyage DOIT épargner intégralement les images
  `![...]` : aucune destination d'image n'est retirée ; dans un lien
  contenant une image, seule la destination du lien externe est retirée.
- **FR-004**: Le drapeau `--conserver-liens` DOIT désactiver le retrait
  des destinations sans chevrons et produire des sorties identiques au
  comportement antérieur, octet par octet.
- **FR-005**: Le traitement des destinations entre chevrons (features
  004/005) DOIT rester identique octet par octet.
- **FR-006**: Les URLs nues hors syntaxe de lien et les contenus de blocs
  de code DOIVENT rester intacts (contrat 005 reconduit).
- **FR-007**: Un titre de lien `](url "titre")` sans chevrons DOIT être
  emporté avec la destination (arbitrage 005 reconduit).
- **FR-008**: La passe DOIT être idempotente : un second passage ne
  modifie pas la sortie (précédent 004).

### Key Entities *(include if feature involves data)*

- **Lien inline sans chevrons**: association libellé → destination
  (chemin, ancre ou URL), avec titre éventuel ; seul le libellé survit.
- **Image inline**: construct `![...]` épargné intégralement, y compris
  imbriqué dans un lien.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 0 destination de lien sans chevrons dans les 5 sorties du
  corpus de calibration rejouées (baseline : 199 occurrences, 34 à 47 par
  fichier).
- **SC-002**: Libellés et texte environnant inchangés octet par octet
  hors destinations, sur tout le corpus de calibration.
- **SC-003**: Sorties inchangées octet par octet sur les corpus
  historiques (Exemple_1 à Exemple_3) et sur les documents sans liens.
- **SC-004**: Aucune retouche manuelle de destinations de liens nécessaire
  sur un run du corpus de calibration.
- **SC-005**: Suite de tests au vert sans relâchement, couvrant les
  nouvelles formes et la non-régression chevron.

## Assumptions

- Les formes observées dans le corpus de calibration (ancres, relatifs,
  absolus, relatifs sans slash) sont représentatives des sorties du
  convertisseur de l'utilisateur.
- La règle unifiée peut couvrir chevrons et non-chevrons sans changer le
  comportement acquis sur les 5 314 destinations chevrons des corpus
  historiques.
- Les résidus tolérés (crochets d'un logo réduit, `[[1]]`, libellés de
  navigation seuls) sont acceptés par l'utilisateur (option A confirmée
  le 2026-10-27) et relèvent d'une future passe de détection de motifs.
- Aucun lien de référence `[libellé][ref]` n'est attendu dans les corpus
  (aucun observé à ce jour) ; le besoin reste détectable par un simple
  grep sur toute nouvelle entrée.
