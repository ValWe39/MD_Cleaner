# Feature Specification: Extraits lisibles et localisables dans la suggestion

**Feature Branch**: `003-extrait-lisible`

**Created**: 2026-09-29

**Status**: Draft

**Input**: Handoff de la décision d'assessment `lisibilite-dry-run` (.specify/assessments/lisibilite-dry-run/decision.md) : extraits de motifs étendus (N lignes réglables, défaut 5, rendus en vrais sauts de ligne), champ position par motif (page + lignes de première occurrence), garde-fou du rapport ; suggestion.json est la surface de jugement, le rapport reste un aperçu tronqué.

## Clarifications

### Session 2026-09-29

- Q: Que doit faire `--extrait N` quand la commande est lancée sans `--dry-run` (le nettoyage simple n'écrit pas de suggestion.json) ? → A: Option A — l'option est acceptée sans effet observable hors dry-run, le comportement étant documenté dans l'aide de la commande.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Juger un motif depuis le seul suggestion.json (Priority: P1)

Un utilisateur valide un dry-run sur un document riche (la feature 002 y produit ~25 motifs). Aujourd'hui, l'extrait de 3 lignes jointes par « / » rend 14 motifs sur 26 indiscernables, et juger exige d'ouvrir le document source en parallèle. Après la feature, chaque motif porte un extrait de 5 lignes en vrais sauts de ligne — les lignes vides deviennent des lignes vides visibles, le contexte distinctif (liens de thème, dates) apparaît — ainsi qu'une position (page et lignes de sa première occurrence) : l'utilisateur juge et décide sans quitter le JSON.

**Why this priority**: c'est le cœur de la demande — la surface de jugement est suggestion.json (le fichier que l'utilisateur édite pour basculer les actions) ; tout le reste sert ce flux.

**Independent Test**: dry-run sur `Examples/Exemple_2` — les extraits des motifs métadonnées sont distincts (liens de thème visibles), chaque motif porte une position, et au plus 2 motifs partagent le même extrait.

**Acceptance Scenarios**:

1. **Given** un dry-run sur un document riche, **When** l'utilisateur ouvre `suggestion.json` dans un lecteur de JSON, **Then** chaque extrait s'affiche ligne par ligne et suffit à distinguer le motif de ses voisins, sans ouvrir le document source.
2. **Given** un motif du JSON, **When** l'utilisateur consulte sa position, **Then** elle désigne la page et les lignes de la première occurrence réelle du motif dans le document d'origine.
3. **Given** un motif dont l'intervalle est plus court que le nombre de lignes demandé, **When** l'extrait est construit, **Then** il contient ce qui existe, sans complément inventé depuis d'autres zones.

---

### User Story 2 - Régler le nombre de lignes de l'extrait (Priority: P2)

Un document atypique peut exiger plus (ou moins) de contexte par motif. L'utilisateur ajuste la dose via une nouvelle option : `--extrait N` (défaut 5, bornes 2 à 25), qui s'applique à la génération de `suggestion.json` uniquement — le rapport reste un aperçu tronqué, conformément au cadrage.

**Why this priority**: le réglage est demandé par l'utilisateur (règle de gouvernance du 2026-09-29 : une commande demandée est ajoutée, un tour final de consolidation des options est prévu) ; la valeur par défaut mesurée (5) sert déjà l'usage courant, l'option sert les cas atypiques.

**Independent Test**: deux dry-runs avec `--extrait 2` et `--extrait 12` sur le même document donnent des extraits d'exactement 2 et 12 lignes (quand l'intervalle le permet) ; `--extrait 1` et `--extrait 40` sont refusés (code retour 3).

**Acceptance Scenarios**:

1. **Given** un document et `--extrait 12`, **When** la suggestion est générée, **Then** chaque extrait comporte exactement 12 lignes si l'intervalle du motif le permet, sinon tout ce qui existe.
2. **Given** une valeur hors bornes (`--extrait 1` ou `--extrait 40`), **When** la commande est lancée, **Then** l'outil échoue en usage invalide (code retour 3) avec un message clair des bornes acceptées.
3. **Given** un nettoyage avec `--suggestion` (sans nouveau dry-run), **When** la suggestion consommée contient des extraits d'une autre longueur, **Then** elle s'applique telle quelle — la longueur d'extrait n'a aucune incidence sur le nettoyage.

---

### User Story 3 - Continuité : rapport intact et suggestions consommables (Priority: P3)

L'arrivée de sauts de ligne dans les extraits ne doit rien casser : le rapport dry-run neutralise les sauts dans ses cellules de tableau (sa présentation en deux sections et sa troncature à 120 caractés restent inchangées), et les suggestions générées avant la feature — dépourvues du champ position — restent consommables sans erreur.

**Why this priority**: garde de continuité pure ; aucune valeur fonctionnelle nouvelle, mais sans elle les deux régressions invisibles identifiées en façonnage (table du rapport cassée, suggestions anciennes rejetées) annuleraient la feature sur le terrain.

**Independent Test**: le rapport d'un dry-run sur Exemple_2 contient un tableau bien formé (aucun saut de ligne dans les cellules) ; une suggestion ancienne sans champ position se consomme avec le code retour 0.

**Acceptance Scenarios**:

1. **Given** un dry-run après la feature, **When** le rapport est généré, **Then** aucune cellule de son tableau ne contient de saut de ligne et le tableau reste bien formé.
2. **Given** une suggestion générée avant la feature (sans champ position), **When** elle est consommée avec `--suggestion`, **Then** le nettoyage s'applique normalement (code retour 0).

---

### Edge Cases

- Que se passe-t-il quand un motif n'a qu'une ou deux lignes ? L'extrait rend ce qui existe — jamais de complément inventé ; la position reste exacte.
- Que se passe-t-il quand la valeur de `--extrait` dépasse la longueur de tout intervalle du document ? Tous les extraits rendent l'intégralité de leur intervalle ; aucun remplissage.
- Que se passe-t-il pour un extrait contenant des lignes très longues (liens de 200+ caractères) ? Aucune troncature dans le JSON (surface de jugement) ; seule la taille totale est gardée (< 1 Mo sur le corpus réel).
- Que se passe-t-il si une suggestion éditée à la main contient un champ position mal formé (texte au lieu d'entiers) ? Échec rapide à la relecture (code retour 2, message clair), conformément à la validation stricte existante.
- Que se passe-t-il des extraits avec des caractères de retour chariot hérités de fins de ligne Windows ? Les fins de ligne sont normalisées à la lecture du document (déjà le cas), l'extrait ne contient que des sauts de ligne simples.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: L'extrait de chaque motif dans `suggestion.json` DOIT comporter les N premières lignes de l'intervalle le plus long de sa première occurrence, N valant 5 par défaut ; l'extrait est rendu en vrais sauts de ligne ; si l'intervalle est plus court que N, l'extrait contient tout ce qui existe, sans complément.
- **FR-002**: Chaque motif de `suggestion.json` DOIT porter un champ position désignant sa première occurrence sous la forme `{"page": <entier ≥ 1>, "debut": <entier ≥ 0>, "fin": <entier > debut>}`, la ligne `debut` de la page `page` du document d'origine appartenant réellement au motif.
- **FR-003**: L'outil DOIT proposer l'option `--extrait N` (entier de 2 à 25, défaut 5) réglant N pour la génération de `suggestion.json` uniquement ; toute valeur hors bornes DOIT être refusée en usage invalide (code retour 3) ; lancée sans `--dry-run`, l'option DOIT être acceptée sans effet observable (le nettoyage simple ne génère pas de suggestion), ce comportement étant documenté dans l'aide de la commande (clarification du 2026-09-29).
- **FR-004**: Le rapport dry-run DOIT neutraliser les sauts de ligne des extraits dans ses cellules de tableau (remplacement par un séparateur simple) ; sa structure en deux sections (feature 002) et sa troncature à 120 caractères restent inchangées.
- **FR-005**: La relecture d'une suggestion (`--suggestion`) DOIT accepter l'absence du champ position (suggestions d'avant-feature) et DOIT rejeter un champ position mal formé par un échec rapide (code retour 2, message clair).
- **FR-006**: Le comportement DOIT rester déterministe et `suggestion.json` DOIT rester sous 1 Mo sur le corpus d'exemples (Exemple_1, Exemple_2) pour toute valeur de N dans les bornes.
- **FR-007**: La présente spec révisant le contrat « extrait » de la feature 001 (`specs/001-nettoyage-md-repetitif/contracts/formats.md` : « extrait ≤ 3 lignes jointes par " / " »), la révision DOIT être documentée dans le contrat mis à jour lors de l'implémentation.
- **FR-008**: Aucune régression des critères de succès des features 001 et 002 : nettoyage, déterminisme, pagination/cartographie, séparation des motifs (SC-001 à SC-006 de 002), rapport en deux sections.
- **FR-009**: La longueur d'extrait n'a AUCUNE incidence sur la détection, les actions ou le nettoyage : consommer une suggestion d'extraits courts ou longs produit le même `nettoye.md`.

### Key Entities *(include if feature involves data)*

Les entités des features 001/002 restent applicables ; la présente feature fait évoluer deux champs de l'une d'elles et ajoute une option :

- **MotifRepetitif** (suggestion.json) : champ `extrait` étendu (N lignes, vrais sauts de ligne) et nouveau champ `position` (`{"page", "debut", "fin"}` de la première occurrence) ; tous les autres champs inchangés (id, action, nb_lignes, frequence, pages).
- **Option CLI** : `--extrait N` (2-25, défaut 5), sans effet sur la détection ni le nettoyage, effet limité à la génération de la suggestion.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Sur un dry-run de `Examples/Exemple_2` à la valeur par défaut, au plus 2 motifs partagent le même extrait (baseline mesurée avant la feature : 12 motifs en doublon).
- **SC-002**: Pour toute valeur de N dans les bornes, chaque extrait comporte exactement N lignes quand l'intervalle du motif le permet (vérification mécanique sur les motifs à intervalle suffisant).
- **SC-003**: Pour chaque motif, la ligne à l'indice `position.debut` de la page `position.page` du document d'origine est couverte par une occurrence réelle du motif (vérification mécanique).
- **SC-004**: `suggestion.json` reste sous 1 Mo sur le corpus d'exemples pour toute valeur de N dans les bornes.
- **SC-005**: Deux exécutions identiques produisent des `suggestion.json` identiques octet par octet.
- **SC-006**: Le rapport dry-run d'un document riche contient des tableaux bien formés (aucun saut de ligne dans les cellules) et la suite de tests des features 001/002 reste au vert sans relâchement des seuils.

## Assumptions

- Bornes et nom de l'option : `--extrait`, 2 à 25, défaut 5 — la mesure a établi la saturation à 5 ; 25 couvre les cas atypiques sans risquer la garde de taille ; le tour final de consolidation des commandes (règle de gouvernance) pourra réviser le nom.
- Structure du champ position : objet `{"page", "debut", "fin"}` (plutôt que champs à plat `position_page`, `position_debut`) pour l'extensibilité et la lisibilité du JSON.
- La position désigne la première occurrence du motif (page la plus ancienne, premier intervalle) — cohérent avec l'ordre d'attribution des ids ; une position par occurrence multiple est hors périmètre.
- Les suggestions d'avant-feature restent consommables (champ position absent toléré) — la validation n'exige jamais un champ que la version génératrice ne produisait pas.
- Le rapport reste un aperçu non contractuel : sa neutralisation des sauts est un garde-fou de forme, pas une refonte de présentation.
- Conformité à la constitution (v1.4.0) inchangée : zéro dépendance, zéro réseau, la garde < 1 Mo protège de la dérive vers un duplicatat du document.
