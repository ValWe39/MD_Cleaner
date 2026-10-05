# Feature Specification: Traitement multi-documents en une invocation

**Feature Branch**: `007-traitement-multi-documents`

**Created**: 2026-10-05

**Status**: Draft

**Input**: User description: « Permettre à l'outil de traiter plusieurs documents en une seule invocation. Règles : un traitement par document (N documents input => N sorties), les paramètres de cleaning sont les mêmes pour tous les documents, l'outil repère seul s'il y a plusieurs docs ou un seul. Documents ajoutés dans le chemin à la suite ("md-cleaner doc1 doc2 doc3") ou à partir d'un dossier ("md-cleaner dossierA", seuls les .md traités). Options non applicables à plusieurs docs : ignorées en lot (dry-run, suggestion, etc.). » — assessment `multi-documents` (intake → research → problem → concept → decision : go, option A).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Nettoyer plusieurs fichiers listés en une invocation (Priority: P1)

L'utilisateur a plusieurs documents Markdown à nettoyer avec les mêmes paramètres. Il les liste à la suite sur la ligne de commande : `md-cleaner doc1.md doc2.md doc3.md`. L'outil traite chaque document exactement comme s'il avait été invoqué seul avec ces mêmes paramètres : chaque document produit sa sortie nettoyée dans son propre dossier de run. La sortie console affiche pour chaque document les mêmes lignes qu'aujourd'hui (chemins des sorties, avertissements).

**Why this priority**: C'est le cœur de la valeur : une seule invocation au lieu de N, avec une seule expression des paramètres pour tout le corpus.

**Independent Test**: Invocable avec les 3 exemples de référence du projet (`Examples/*/2.Input/*.md`) ; vérifiable par l'existence de 3 sorties et la parité octet par octet avec les invocations individuelles.

**Acceptance Scenarios**:

1. **Given** 3 documents `.md` valides, **When** `md-cleaner doc1.md doc2.md doc3.md`, **Then** 3 dossiers de run sont créés (un par document) contenant chacun la sortie nettoyée du document correspondant, nommée selon la règle en vigueur (feature 006).
2. **Given** les mêmes documents et options, **When** on compare chaque sortie du lot à la sortie obtenue en invoquant le document seul avec les mêmes options, **Then** les contenus sont identiques octet par octet.
3. **Given** une invocation mono-document, **When** `md-cleaner doc1.md`, **Then** le comportement est identique à aujourd'hui (aucune régression du contrat existant).

---

### User Story 2 - Nettoyer un corpus entier via un dossier (Priority: P2)

L'utilisateur a regroupé ses documents dans un dossier. Il invoque `md-cleaner dossierA`. L'outil retient uniquement les fichiers `.md` de premier niveau du dossier (les autres fichiers sont ignorés) et les traite tous, dans l'ordre de leur nom.

**Why this priority**: Le corpus est déjà regroupé sur le disque ; énumérer les fichiers un à un serait réintroduire la friction que la feature supprime.

**Independent Test**: Invocable sur un dossier de test contenant un mélange de `.md` et de fichiers non-`.md` ; vérifiable par le traitement exclusif des `.md` dans l'ordre des noms.

**Acceptance Scenarios**:

1. **Given** un dossier contenant 2 fichiers `.md` et 1 fichier `.txt`, **When** `md-cleaner dossierA`, **Then** seuls les 2 `.md` sont traités, dans l'ordre alphabétique de leur nom.
2. **Given** un dossier ne contenant aucun fichier `.md` (ou seulement des sous-dossiers), **When** `md-cleaner dossierA` (seul ou au sein d'un lot mixte), **Then** l'entrée est ignorée avec un message explicite et le reste du lot est traité ; si aucun document n'est retenu au final, l'invocation échoue en erreur d'entrée (code 1).
3. **Given** une invocation mélangeant fichiers et dossiers, **When** `md-cleaner doc1.md dossierA`, **Then** le lot est l'union des fichiers listés et des `.md` du dossier, dans l'ordre d'apparition.

---

### User Story 3 - Signalement explicite des options non applicables en lot (Priority: P3)

L'utilisateur tente un traitement en lot avec une option qui ne s'applique qu'à un document unique (`--dry-run`, `--suggestion`). L'outil émet un avertissement explicite en console, neutralise l'option, et traite le lot en nettoyage complet : jamais d'application partielle, jamais de silence.

**Why this priority**: Le problem.md exige un comportement non silencieux ; c'est la garantie de confiance la plus importante de la feature (aucun paramètre perdu sans trace).

**Independent Test**: Invocable avec `md-cleaner doc1.md doc2.md --dry-run` ; vérifiable par le message observé et le comportement associé (arrêt ou traitement).

**Acceptance Scenarios**:

1. **Given** un lot de 2 documents et l'option `--dry-run`, **When** invocation, **Then** un avertissement explicite est affiché, l'option est neutralisée et le lot est traité en nettoyage complet (aucune sortie de dry-run produite).
2. **Given** un lot de 2 documents et l'option `--suggestion` avec un fichier de suggestion, **When** invocation, **Then** même avertissement et même neutralisation : une suggestion est par construction liée à un seul document (champ source validé strictement), la suggestion par défaut est recalculée pour chaque document.

---

### User Story 4 - Comportement déterminé en cas d'échec d'un document du lot (Priority: P4)

Un document du lot est invalide (absent, illisible, non-`.md`) ou provoque une erreur en cours de traitement. L'outil poursuit le traitement des documents suivants, en signalant chaque échec individuellement en console ; au troisième échec consécutif, le lot s'arrête net (fail-fast). Les sorties des documents traités avec succès sont conservées, et le code retour est 0 si et seulement si tous les documents du lot ont été traités.

**Why this priority**: Moins critique que les trois précédentes (le cas est l'exception, pas le flux nominal), mais nécessaire pour que le comportement du lot soit complet et testable.

**Independent Test**: Invocable avec un lot contenant un document invalide entre deux valides ; vérifiable par l'état des sorties, les messages d'échec et le code retour.

**Acceptance Scenarios**:

1. **Given** un lot [doc1 valide, doc2 invalide, doc3 valide], **When** invocation, **Then** doc1 et doc3 sont traités avec leurs sorties, l'échec de doc2 est signalé explicitement, et le code retour est 1 (au moins un document non traité).
2. **Given** un lot contenant trois documents en échec consécutifs suivis d'un document valide, **When** invocation, **Then** le lot s'arrête au troisième échec consécutif : le document suivant n'est pas traité, les échecs sont signalés, les sorties déjà produites sont conservées, code retour 1.
3. **Given** un lot dont aucun document n'est traitable, **When** invocation, **Then** aucune sortie n'est produite, chaque échec est signalé, et le code retour est 1.

---

### Edge Cases

- Le même fichier apparaît deux fois dans le lot (listé deux fois, ou listé et aussi contenu dans le dossier) : chaque occurrence est traitée dans l'ordre, les sorties étant désambiguïsées par le mécanisme anti-collision existant (suffixes `-1`, `-2`).
- Deux documents différents dont les noms produisent le même préfixe de sortie (troncature à 20 caractères) : désambiguïsation par le suffixe anti-collision existant, jamais d'écrasement.
- Un lot d'un seul document issu d'un dossier (`dossierA` contenant exactement un `.md`) : traité comme un lot — comportement identique au mono-document.
- Dossier passé en argument n'existe pas ou n'est pas un dossier : entrée invalide (code 1), comme un fichier absent.
- Fichier non-`.md` listé directement en argument : entrée invalide (code 1), comme aujourd'hui.
- Ordre de traitement : ordre d'apparition des arguments sur la ligne de commande ; au sein d'un dossier, ordre alphabétique des noms de fichiers.
- Trois échecs consécutifs interrompent le lot ; deux échecs suivis d'un succès remettent le compteur d'échecs consécutifs à zéro (le compteur porte sur les documents, pas sur l'invocation).
- Échecs isolés (non consécutifs) : le lot se poursuit jusqu'au bout, chaque échec est signalé, le code retour reste 1 dès qu'au moins un document a échoué.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La ligne de commande DOIT accepter une ou plusieurs entrées positionnelles ; chaque entrée DOIT être un fichier `.md` existant et lisible, ou un dossier existant.
- **FR-002**: Lorsqu'une entrée est un dossier, le lot DOIT retenir uniquement les fichiers `.md` de premier niveau, triés par nom ; les fichiers non-`.md` du dossier DOIVENT être ignorés sans erreur.
- **FR-003**: Chaque document du lot DOIT être traité par le chemin de traitement existant, produisant exactement les sorties qu'il produirait invoqué seul : un dossier de run par document et une sortie nettoyée par document (N entrées → N sorties).
- **FR-004**: Les paramètres de cleaning (seuil, conservation des liens, pagination, calibrage, extraction, échantillon) DOIVENT s'appliquer à l'identique à chaque document du lot.
- **FR-005**: Le système DOIT déterminer seul le nombre de documents du lot, y compris lorsqu'il est d'un seul, et le traitement mono-document DOIT rester strictement identique au comportement actuel (rétrocompatibilité du contrat de la feature 001).
- **FR-006**: Les options non applicables à un lot (`--dry-run`, `--suggestion`) DOIVENT déclencher un avertissement explicite en console, être neutralisées (le lot est traité en nettoyage complet), et ne DOIVENT jamais être appliquées partiellement ni ignorées en silence.
- **FR-007**: En cas d'échec d'un document, le système DOIT poursuivre le traitement des documents suivants en signalant chaque échec individuellement ; au troisième échec consécutif, il DOIT s'arrêter immédiatement, en conservant les sorties déjà produites. Le code retour DOIT être 0 si et seulement si tous les documents du lot ont été traités avec succès, et 1 sinon.
- **FR-008**: Un dossier ne contenant aucun fichier `.md` applicable DOIT être ignoré avec un message explicite, sans interrompre le reste du lot ; une invocation dont aucun document n'est retenu DOIT échouer en erreur d'entrée (code 1).
- **FR-009**: Les options applicables document par document (`--pagine`, `--conserver-liens`, `--seuil`, `--calibrage`, `--extrait`, `--nom-titre`, `--sortie`, `--echantillon`) DOIVENT conserver leur effet et leur contrat actuels, appliqués à chaque document du lot.
- **FR-010**: Aucune sortie existante ne DOIT jamais être écrasée ; les collisions de noms (doublons du lot, préfixes identiques) DOIVENT être résolues par le mécanisme de suffixe existant.
- **FR-011**: La sortie console DOIT présenter, pour chaque document traité, les lignes d'information actuelles (chemins des sorties, avertissements sur stderr) ; aucun résumé de lot n'est produit dans ce périmètre.

### Key Entities *(include if feature involves data)*

- **Lot (invocation)** : collection ordonnée de documents à traiter, reconstituée depuis les arguments positionnels (fichiers listés dans l'ordre d'apparition, fichiers `.md` des dossiers triés par nom). Homogène : un seul jeu de paramètres de cleaning pour tout le lot.
- **Document d'entrée** : fichier `.md` existant et lisible, unité de traitement inchangée.
- **Dossier de run** : inchangé (un par document, numérotation séquentielle ou nommage par titre) ; le lot n'introduit aucune entité de sortie nouvelle.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un corpus de K documents est traité en une seule invocation au lieu de K (vérifié sur les 3 exemples de référence du projet, baseline : 3 invocations aujourd'hui).
- **SC-002**: Pour chaque document d'un lot, la sortie nettoyée est identique octet par octet à celle obtenue en invoquant le document seul avec les mêmes options (parité sur les 3 exemples de référence, options applicables).
- **SC-003**: Aucune option applicable ne change d'effet entre le traitement en lot et le traitement individuel (vérifié par les tests de parité).
- **SC-004**: Toute option non applicable en lot fait l'objet d'un signalement explicite observable par l'utilisateur (message en console), jamais d'un silence (vérifié par test sur `--dry-run` et `--suggestion`).
- **SC-005**: Le comportement mono-document est strictement inchangé : toutes les tests existants de la suite passent sans relâchement (rétrocompatibilité du contrat 001 pour le cas individuel).

## Assumptions

- Les trois arbitrages structurants ont été tranchés par l'utilisateur le 2026-10-05 : (1) options non applicables en lot → avertissement + neutralisation, lot traité ; (2) échec d'un document → poursuite avec signalement de chaque échec, fail-fast au troisième échec consécutif ; (3) dossier sans `.md` → entrée ignorée avec message, lot poursuivi.
- Le mélange de fichiers et de dossiers dans une même invocation est autorisé (l'ordre d'apparition fait foi) ; le concept A l'inclut dans son sketch.
- Le scan de dossier est non récursif (premier niveau uniquement), par cohérence avec le précédent interne `--echantillon` et la structure d'`Examples/`.
- Un doublon (fichier listé deux fois, ou listé et contenu dans le dossier) est traité à chaque occurrence ; le déterminisme est assuré par l'ordre et le suffixe anti-collision.
- Les corpus réels restent de taille modeste : aucun plafond de nombre de documents n'est introduit (à réviser si un usage volumineux apparaît).
- La sortie console reste document par document, sans résumé de fin de lot (périmètre de l'option A ; un résumé relèverait de l'extension B).
- `--nom-titre` s'applique par document : chaque document du lot nomme son propre dossier de run d'après son propre titre.
- La boucle de jugement (dry-run → suggestion → relance) reste hors lot, conformément à l'arbitrage de l'intake et de la décision.
