# Feature Specification: Décidabilité des motifs au dry-run (fusion majoritaire)

**Feature Branch**: `002-fusion-majoritaire`

**Created**: 2026-09-29

**Status**: Draft

**Input**: Handoff de la décision d'assessment `granularite-motifs` (.specify/assessments/granularite-motifs/decision.md) : rendre chaque motif décidé au dry-run indépendamment, via la coupure de fusion par chevauchement majoritaire ; sans plafond numérique de blocs ; sans nouvelle option CLI.

## Clarifications

### Session 2026-09-29

- Q: Quand une fenêtre candidate chevauche un bloc sur exactement la moitié des pages concernées, doit-elle fusionner avec ce bloc ? → A: Option B — non : la règle majoritaire s'entend au sens strict, la fusion exige un chevauchement sur strictement plus de la moitié des pages concernées ; à la moitié exacte, la fusion est refusée.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Décider séparément interface et métadonnées (Priority: P1)

Un utilisateur lance un dry-run sur un document à métadonnées récurrentes (listing, catalogue — les publications y portent des thèmes, des dates et des marqueurs d'institution qui se répètent). Aujourd'hui, la détection soude la barre de filtres et les métadonnées des publications dans un seul motif indivisible ; l'utilisateur ne peut que tout supprimer ou tout garder. Après la feature, ces zones appartiennent à des motifs distincts : il peut décider « supprimer les filtres, conserver les métadonnées » en basculant uniquement le bon motif.

**Why this priority**: c'est le blocage constaté qui a déclenché l'assessment (document déclencheur : listing ccomptes de 21 pages — même structure que `Examples/Exemple_2`) ; sans cette séparation, le dry-run reste inexploitable sur cette classe de documents.

**Independent Test**: dry-run sur `Examples/Exemple_2/2.Input/consolidated.md` — la zone filtres/pagination et les métadonnées de publications appartiennent à des motifs distincts, et basculer l'un sans l'autre produit l'effet attendu dans `nettoye.md`.

**Acceptance Scenarios**:

1. **Given** un document où la zone de filtres et les métadonnées de publications sont aujourd'hui fusionnées en un seul motif, **When** l'utilisateur lance un dry-run, **Then** ces zones appartiennent à des motifs distincts, chacun avec son id et sa fréquence.
2. **Given** le dry-run d'un tel document, **When** l'utilisateur bascule le motif des filtres en `supprimer` et les motifs des métadonnées en `conserver`, **Then** le nettoyage retire la zone filtres et conserve les métadonnées des publications.
3. **Given** un document à blocs compacts et homogènes (`Examples/Exemple_1`), **When** la détection s'exécute, **Then** les motifs produits restent identiques à ceux d'aujourd'hui (4 motifs, mêmes zones, mêmes actions).

---

### User Story 2 - Charge de validation maîtrisée malgré plus de motifs (Priority: P2)

La coupure de fusion produit davantage de motifs sur les documents riches (mesure : ~25 motifs listés sur un listing, contre 2 aujourd'hui). L'utilisateur ne doit pas être noyé : les motifs exigeant réellement une décision (proposés à `supprimer`) restent en petit nombre (mesure : 4 à 5), et les motifs conservés par défaut sont présentés dans une section secondaire du rapport, sans action requise.

**Why this priority**: la séparation de la Story 1 n'a de valeur que si la validation reste rapide ; mais un rapport illisible ne détruit pas la fonctionnalité de base — c'est une exigence de lisibilité, prioritaire mais secondaire.

**Independent Test**: dry-run sur `Examples/Exemple_2` — compter les motifs proposés à `supprimer` (≤ 5), vérifier que les motifs conservés par défaut sont regroupés dans une section distincte du rapport.

**Acceptance Scenarios**:

1. **Given** le dry-run d'un document riche en zones récurrentes, **When** l'utilisateur ouvre le rapport, **Then** les motifs proposés à `supprimer` sont listés en tête et les motifs conservés par défaut dans une section secondaire clairement séparée.
2. **Given** ce rapport, **When** l'utilisateur le parcourt, **Then** le temps de validation reste dans l'objectif existant (moins de 5 minutes, SC-004 de la feature 001).
3. **Given** un document à blocs compacts (`Examples/Exemple_1`), **When** la détection s'exécute, **Then** le rapport ne comporte pas de section secondaire superflue (comportement inchangé).

---

### User Story 3 - Continuité des suggestions entre versions (Priority: P3)

La coupure de fusion change les ids de motifs entre versions de l'outil : une `suggestion.json` générée avant la feature ne correspond plus aux motifs détectés après. L'utilisateur est informé de manière claire : la documentation indique que les suggestions se régénèrent par dry-run, et le comportement en cas de consommation d'une suggestion obsolète reste l'échec rapide existant (id inconnu).

**Why this priority**: pure exigence de continuité documentaire ; aucune valeur fonctionnelle nouvelle, mais nécessaire pour que la transition ne surprenne pas l'utilisateur.

**Independent Test**: consommer une suggestion d'avant-feature sur un document après-feature → échec rapide avec message clair (comportement déjà prévu par le contrat de la feature 001) ; vérifier que la documentation mentionne la régénération.

**Acceptance Scenarios**:

1. **Given** une `suggestion.json` générée avant la feature, **When** l'utilisateur la consomme après la mise à jour, **Then** l'outil échoue rapidement avec le message existant sur les ids inconnus.
2. **Given** la documentation du projet (README), **When** l'utilisateur la lit, **Then** elle mentionne que les ids de motifs ne sont pas stables entre versions et que les suggestions se régénèrent par dry-run.

---

### Edge Cases

- Que se passe-t-il quand un bloc compact légitime (navigation contiguë de plusieurs dizaines de lignes) repose sur des chevauchements justement majoritaires ? Il fusionne normalement — comportement inchangé (validé par la mesure sur `Examples/Exemple_1`).
- Que se passe-t-il quand une fenêtre candidate chevauche un bloc sur exactement la moitié des pages concernées ? La fusion est refusée (règle majoritaire au sens strict, clarification du 2026-09-29) ; cette frontière est testée unitairement.
- Que se passe-t-il si le nombre de motifs explose sur un document très hétérogène ? Le rapport doit rester lisible (section secondaire), et aucun plafond numérique n'est introduit — l'explosion est observée et signalée si elle survient, pas arbitrairement plafonnée.
- Que se passe-t-il pour les documents à page unique ou très courts ? Comportement inchangé (aucun motif, sortie identique).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La fusion de deux blocs récurrents ne DOIT être admise que si le chevauchement se vérifie sur **strictement plus de la moitié** des pages concernées par la fenêtre candidate ; un chevauchement présent sur la moitié exacte ou moins ne soude pas deux zones distinctes.
- **FR-002**: Sur les documents à métadonnées récurrentes, la zone d'interface (navigation, filtres, pagination) et les métadonnées de contenu DOIVENT appartenir à des motifs distincts, chacun individuellement actionnable dans la suggestion.
- **FR-003**: La détection ne DOIT PAS modifier les motifs des documents à blocs compacts et homogènes : les zones, ids et actions produits restent identiques à ceux de la version précédente sur le corpus d'exemples.
- **FR-004**: Le rapport de dry-run DOIT distinguer les motifs exigeant une décision (proposés à `supprimer`) des motifs conservés par défaut, ces derniers étant regroupés dans une section secondaire sans action requise.
- **FR-005**: Le nombre de motifs proposés à `supprimer` sur le corpus d'exemples DOIT rester inférieur ou égal à 5.
- **FR-006**: Le comportement DOIT rester déterministe (à entrées et options identiques, sorties identiques octet par octet) et les ids de motifs DOIVENT rester stables au sein d'une même version de l'outil.
- **FR-007**: La documentation du projet DOIT mentionner l'instabilité des ids de motifs entre versions et la régénération des suggestions par dry-run.
- **FR-008**: La consommation d'une suggestion issue d'une version antérieure DOIT continuer d'échouer rapidement avec le message existant sur les ids inconnus (aucune tentative de correspondance approximative).
- **FR-009**: Les critères de succès existants de la feature 001 ne DOIVENT pas régresser : contenu unique conservé à 100 % (SC-001, SC-005), déterminisme (SC-002), validation du rapport en moins de 5 minutes (SC-004), cohérence cartographie/sortie paginée (SC-006).
- **FR-010**: La feature ne DOIT introduire ni nouvelle option en ligne de commande, ni plafond ou plancher numérique de motifs, ni nouvelle dépendance.

### Key Entities

Les entités de la feature 001 (`specs/001-nettoyage-md-repetitif/data-model.md`) restent applicables ; la présente feature fait évoluer une règle de construction de l'une d'elles :

- **MotifRépétitif** : la règle de fusion change (chevauchement majoritaire requis) ; les champs (id, action, fréquence, pages, emplacements) sont inchangés.
- **Rapport dry-run** : nouvelle présentation en deux sections (décisions requises / motifs conservés par défaut), sans changement du format contractuel de `suggestion.json`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Sur `Examples/Exemple_2/2.Input/consolidated.md`, la zone filtres/pagination et les métadonnées de publications appartiennent à des motifs distincts après un dry-run (critère binaire, vérifiable mécaniquement ; baseline : un seul motif fusionné aujourd'hui).
- **SC-002**: Sur `Examples/Exemple_1/2.Input/consolidated.md`, les motifs produits (nombre, zones couvertes, actions) sont identiques à ceux de la version précédente.
- **SC-003**: Sur le corpus d'exemples, le nombre de motifs proposés à `supprimer` est inférieur ou égal à 5 par document.
- **SC-004**: La suite de tests de la feature 001 passe sans relâchement des seuils d'acceptation.
- **SC-005**: Deux exécutions successives avec les mêmes entrées et options produisent des sorties identiques octet par octet.
- **SC-006**: Un utilisateur parcourt le rapport dry-run d'un document riche et identifie les décisions requises en moins de 5 minutes.

## Assumptions

- La règle de fusion exige un chevauchement sur strictement plus de la moitié des pages concernées (clarification du 2026-09-29) ; la valeur de la frontière s'appuie sur la mesure de l'assessment (50 % produit la meilleure séparation des deux valeurs essayées, 25 motifs contre 29 à 80 %), l'écart avec le prototype (qui admettait le chevauchement à la moitié exacte) ne jouant que sur ce cas limite, non observé dans le corpus ; il s'agit d'une constante interne, pas d'une option exposée.
- Le document déclencheur (listing ccomptes de 21 pages issu du projet Web-Reader) et `Examples/Exemple_2` partagent la même structure ; les critères mesurables s'appuient sur le corpus versionné.
- La présentation en deux sections du rapport suffit à absorber l'augmentation du nombre de motifs listés (~25 sur un document riche) sans dépasser l'objectif de temps de validation.
- L'instabilité des ids entre versions est acceptable : les suggestions se régénèrent par dry-run (position actée dans la décision d'assessment).
- La présente feature modifie la détection de la feature 001 sans changer les formats de sortie ni la sémantique supprimer/conserver.
- Conformité à la constitution du projet (v1.4.0) inchangée : zéro dépendance, zéro réseau, simplicité, déterminisme.
