# Feature Specification: Nettoyage des destinations de liens résiduelles à l'écriture de la sortie

**Feature Branch**: `004-nettoyage-liens-html`

**Created**: 2026-10-02

**Status**: Draft

**Input**: Handoff de l'assessment `nettoyage-liens-html` (decision.md) : la sortie nettoyée conserve des destinations de liens inline de la forme `](</...>)` collées au texte utile (~31 % des lignes du run 004 : 527/1724), dégradant le livrable final et exigeant une retouche manuelle à chaque run. Option retenue : passe de nettoyage à l'écriture de `nettoye.md` et `nettoye-pagine.md`, en aval de la détection ; cible limitée à la forme `](</...>)` ; activée par défaut, désactivable par drapeau CLI.

## Clarifications

### Session 2026-10-02

- Q: Sous quel nom l'utilisateur désactive-t-il le nettoyage des destinations sur la ligne de commande ? → A: `--conserver-liens` (français, verbe d'abord, cohérent avec `--pagine`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Sortie finale sans destinations résiduelles (Priority: P1)

Un utilisateur lance le nettoyage d'un document Markdown multi-pages issu d'une conversion HTML → Markdown (typiquement un listing contenant des liens inline `[libellé](</...>)`). Sans réglage particulier, le `nettoye.md` produit ne contient plus aucune destination `(</...>)` : les lignes conservées gardent leur texte utile lisible, sans débris de conversion collés au libellé. Il n'a plus aucune retouche manuelle à faire pour ce motif.

**Why this priority**: C'est la valeur centrale du handoff : tenir la promesse « sortie directement exploitable ». C'est la métrique mesurée (0 destination résiduelle contre 527/1724 lignes aujourd'hui).

**Independent Test**: Testable en re Jouant le run équivalent au 004 (entrée `Examples/Exemple_2/2.Input/consolidated.md`) et en vérifiant qu'aucune ligne de la sortie ne contient `](</...>)`, alors que les libellés et le reste du texte des lignes concernées sont inchangés.

**Acceptance Scenarios**:

1. **Given** un document contenant des lignes avec `[libellé](</chemin?encodé>)`, **When** l'utilisateur lance le nettoyage (sans option particulière), **Then** le `nettoye.md` ne contient plus la destination et le libellé reste présent.
2. **Given** le document de listing Cour des comptes (Exemple_2), **When** le nettoyage est lancé, **Then** aucune ligne de la sortie ne contient `(</`, et le nombre de lignes et leur ordre sont inchangés par rapport à un run sans la feature.
3. **Given** une ligne contenant plusieurs liens inline, **When** le nettoyage est lancé, **Then** chaque destination est retirée et les libellés des deux liens restent en place.

---

### User Story 2 - Désactivation pour garder des liens cliquables (Priority: P2)

Un utilisateur qui veut des liens cliquables dans le document final (navigation, vérification des sources) lance le nettoyage avec le drapeau `--conserver-liens` : la sortie est identique au comportement d'avant la feature, destinations comprises.

**Why this priority**: Le comportement par défaut change la sortie pour tous les runs ; la réversibilité explicite est la condition d'acceptabilité de ce changement (handoff, goals du problem.md).

**Independent Test**: Testable en lançant le même run avec `--conserver-liens` et en comparant la sortie octet par octet à la sortie produite sans la feature.

**Acceptance Scenarios**:

1. **Given** un document avec liens inline, **When** l'utilisateur lance le nettoyage avec `--conserver-liens`, **Then** le `nettoye.md` contient les destinations intactes, identiques à une sortie produite sans la feature.
2. **Given** `--conserver-liens`, **When** la sortie paginée est aussi demandée, **Then** `nettoye-pagine.md` contient également les destinations intactes et ses marqueurs de page.

---

### User Story 3 - Sortie paginée nettoyée, marqueurs de page préservés (Priority: P3)

Un utilisateur lance le nettoyage avec la sortie paginée : `nettoye-pagine.md` bénéficie du même nettoyage des destinations, mais les marqueurs de page insérés par l'outil restent strictement inchangés — la cartographie JSON reste cohérente avec le document paginé.

**Why this priority**: Étend la valeur de la P1 au second artefact de sortie sans exposer de nouveau réglage ; protège un contrat existant (cohérence marqueurs/cartographie).

**Independent Test**: Testable en lançant un run `--pagine` sur un document avec liens inline et en vérifiant que chaque marqueur de page attendu est présent à l'identique et que les destinations ont disparu du contenu.

**Acceptance Scenarios**:

1. **Given** un run avec sortie paginée sur un document avec liens inline, **When** le nettoyage est appliqué, **Then** chaque marqueur de page est présent, identique octet par octet, et le contenu des pages ne contient plus de destination.
2. **Given** le fichier `cartographie.json` du même run, **When** on le compare à un run sans la feature, **Then** il est identique (le nettoyage ne touche ni la détection, ni la cartographie).

---

### Edge Cases

- Que se passe-t-il quand la destination contient des caractères encodés (`%5B`, `%3A`, `%20`) ou des chevrons dans le chemin ? La destination est retirée telle quelle, sans décodage ; les caractères encodés disparaissent avec elle.
- Comment le système gère-t-il un lien au libellé vide `[](</chemin>)` ? La destination est retirée comme pour tout lien ; les crochets vides restent, conformément à FR-001 (seule la destination est retirée).
- Que se passe-t-il pour un document sans aucun lien inline (corpus sans la forme `](</...>)`) ? La sortie est identique octet par octet à celle produite sans la feature — la passe ne modifie rien.
- Comment le système gère-t-il les marqueurs de page insérés par l'outil (`<!-- page: N -->`) ? Ils ne correspondent pas à la forme visée et restent strictement inchangés, y compris en sortie paginée.
- Comment le système gère-t-il une ligne entièrement constituée d'un lien `[libellé](</chemin>)` seule sur sa ligne ? La ligne reste présente avec son libellé ; aucune ligne n'est supprimée par cette passe (la suppression de lignes relève de la détection existante).
- Que se passe-t-il des destinations absolues `](https://...)` ou `](</...>` mal refermé ? Hors périmètre : elles ne sont ni retirées ni modifiées (borne explicite de l'assessment).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le nettoyage appliqué à l'écriture de `nettoye.md` retire uniquement la destination des liens inline de la forme `](</...>)` (parenthèses et chevrons compris) ; le libellé du lien, y compris ses crochets `[libellé]`, et le reste du texte de la ligne restent inchangés. Exemple : `[Famille, handicap, sport et jeunesse](</publications?f%5B1%5D=thematic%3A17182>) -` devient `[Famille, handicap, sport et jeunesse] -`.
- **FR-002**: La passe s'applique par défaut à chaque run de nettoyage produisant un `nettoye.md`, sans action de l'utilisateur.
- **FR-003**: L'utilisateur doit pouvoir désactiver la passe par le drapeau `--conserver-liens` ; avec ce drapeau, les sorties sont identiques octet par octet à celles produites sans la feature.
- **FR-004**: La passe s'applique aussi à `nettoye-pagine.md` ; les marqueurs de page insérés par l'outil restent strictement inchangés.
- **FR-005**: La passe ne modifie ni la détection des motifs, ni les extraits, ni `suggestion.json`, ni `rapport-dry-run.md`, ni `cartographie.json`, ni les ids de motifs (M01… inchangés à option de détection égale).
- **FR-006**: La passe retire les destinations telles quelles, sans décoder les caractères encodés ni réécrire les chemins.
- **FR-007**: Le comportement reste déterministe : deux runs sur la même entrée avec les mêmes options produisent des sorties identiques octet par octet.

### Key Entities *(include if feature involves data)*

- **Destination de lien résiduelle**: sous-chaîne `(</...>)` terminant un lien inline Markdown, héritée de la conversion HTML → Markdown ; forme visée `](</...>)`, caractère `>` final non imbriqué. Entité purement textuelle, sans donnée persistée.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Sur le run équivalent au 004 (entrée Exemple_2), aucune ligne de `nettoye.md` ne contient une destination `](</...>)` (baseline : 527 lignes sur 1724).
- **SC-002**: Hors destinations retirées, le texte des lignes conservées est inchangé ; le nombre et l'ordre des lignes de la sortie sont identiques à ceux d'un run sans la feature sur la même entrée.
- **SC-003**: Sur un corpus sans liens inline, la sortie est identique octet par octet à celle d'un run sans la feature.
- **SC-004**: Avec `--conserver-liens`, toutes les sorties (`nettoye.md`, `nettoye-pagine.md`) sont identiques octet par octet à celles d'un run sans la feature, et `cartographie.json` reste cohérente avec les marqueurs de `nettoye-pagine.md`.
- **SC-005**: La suite de tests existante passe sans relâchement des seuils, complétée par les tests de la nouvelle passe (données Exemple_1 et Exemple_2).

## Assumptions

- La forme visée est exactement `](</...>)` (destination entre chevrons, refermée par un `>` sans chevron imbriqué) ; les vraies balises HTML et les destinations absolues sont hors périmètre (assessment, research.md).
- Le drapeau `--conserver-liens` est une option booléenne sans argument du même style que `--pagine` (clarification du 2026-10-02) ; les codes retour (0/1/2/3) et le contrat CLI restent inchangés.
- Les marqueurs de page `<!-- page: N -->` ne matchent jamais la forme visée et ne nécessitent aucune exclusion spéciale dans la règle (à confirmer par test).
- Une seule règle textuelle déterministe suffit ; aucune dépendance runtime nouvelle (conformité constitution v1.4.0 : local-first, stdlib, sorties dans `output/`).
- Les contenus attendus des tests existants qui comparent les sorties seront mis à jour dans le cadre de cette feature (migration bornée, assumée par la décision).
- Les destinations étant des URL relatives sans domaine, leur retrait ne perd aucune information exploitable ; la provenance par page reste dans `cartographie.json` (`url_source`).
