# Feature Specification: Nom de sortie dérivé du document source

**Feature Branch**: `006-nom-sortie-source`

**Created**: 2026-10-05

**Status**: Draft

**Input**: Handoff de l'assessment `nom-sortie-nettoye` (decision.md, verdict go, option A) : les sorties nettoyées s'appellent toutes `nettoye.md`, indissociables de leur document source par le nom. Option retenue : renommer le seul fichier nettoyé en `<nom-dérivé-de-l'entrée>-nettoye.md` — 20 premiers caractères du nom d'entrée, espaces remplacées par `_`, suffixe `-nettoye` ; collision → suffixe numérique `-1` par ordre de traitement (décision utilisateur du 2026-10-05). Hors périmètre : les autres artefacts du run, le nommage des dossiers de run, le multi-documents, le rétro-nommage de l'existant.

## Clarifications

### Session 2026-10-05 (arbitrages au stade specify)

- Q: « Titre du document d'input » = nom de fichier ou premier titre de niveau 1 du contenu ? → A: Nom de fichier sans extension (stem), tranché par l'exemple utilisateur : `retry-failed-records.md` → `retry-failed-records-nettoye.md`.
- Q: Troncature à 20 caractères — brute ou au dernier mot entier ? → A: Troncature brute aux 20 premiers caractères : règle la plus simple à prédire pour l'utilisateur et à tester.
- Q: Caractères autres que les espaces (accents, ponctuation, tirets) ? → A: Seuls les blancs (espaces, tabulations) sont remplacés par `_` ; tout autre caractère du nom d'entrée est conservé tel quel dans la limite des 20 caractères.
- Q: Comportement par défaut ou option ? → A: Le nouveau nommage remplace le comportement par défaut ; aucune option de repli vers `nettoye.md` (handoff du decide, confirmé).
- Q: Quand la règle de collision `-1` s'applique-t-elle, sachant que chaque run a son propre sous-dossier ? → A: Scénario rare avec la structure actuelle, mais la règle reste spécifiée comme garantie : si le nom de sortie cible existe déjà à l'emplacement d'écriture, un suffixe numérique est ajouté, jamais d'écrasement silencieux. Premier conflit → `-1`, suivant → `-2`, par ordre de traitement.

### Session 2026-10-05 (clarification)

- Q: En cas de conflit de nom, où le numéro doit-il être inséré exactement ? → A: À la fin du nom de sortie, juste avant l'extension `.md` : `<nom>-nettoye-1.md` ; le suffixe `-nettoye` reste invariable.
- Q: Pour un nom d'entrée plus long que 20 caractères, comment tronquer la base du nom de sortie ? → A: Troncature brute aux 20 premiers caractères, sans respect de frontière de mot (arbitrage du stade specify confirmé).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Sortie reconnaissable par son nom (Priority: P1)

Un utilisateur nettoie `retry-failed-records.md`. Le fichier nettoyé du run ne s'appelle plus `nettoye.md` mais `retry-failed-records-nettoye.md` : copié, déplacé ou partagé hors de son dossier de run, le fichier reste rattaché à sa source sans l'ouvrir ni parcourir l'arborescence. Le nom reste déterministe : l'utilisateur peut le prédire avant même de lancer la commande.

**Why this priority**: C'est la valeur centrale du handoff : établir le lien nom de sortie → document source, la friction actuelle étant de ne plus savoir quel `nettoye.md` correspond à quelle entrée dès que plusieurs documents sont traités.

**Independent Test**: Testable en lançant le nettoyage sur un document nommé `retry-failed-records.md` et en vérifiant que le fichier nettoyé du run s'appelle `retry-failed-records-nettoye.md` (et non `nettoye.md`), contenu inchangé par ailleurs.

**Acceptance Scenarios**:

1. **Given** un document d'entrée `retry-failed-records.md`, **When** l'utilisateur lance le nettoyage, **Then** le fichier nettoyé s'appelle `retry-failed-records-nettoye.md`.
2. **Given** un document d'entrée `rapport annuel.md`, **When** l'utilisateur lance le nettoyage, **Then** le fichier nettoyé s'appelle `rapport_annuel-nettoye.md` (espaces remplacées par `_`).
3. **Given** un document d'entrée quelconque, **When** le nettoyage est terminé, **Then** le message de fin de commande affiche le chemin réel du fichier renommé.

---

### User Story 2 - Noms longs : troncature prévisible (Priority: P2)

Un utilisateur nettoie un document au nom long, par exemple `comptes-rendus-conseil-municipal-session-octobre.md`. Le nom dérivé est tronqué aux 20 premiers caractères : `comptes-rendus-conse`-nettoye.md. La règle est la même pour tous les documents, sans ajustement au mot le plus proche — l'utilisateur sait exactement ce qu'il obtiendra.

**Why this priority**: Sans règle de troncature définie, deux entrées partageant un préfixe produiraient le même nom sans que l'utilisateur sache pourquoi ; la troncature brute bornée à 20 caractères rend le comportement prévisible et testable. Priorité moindre que P1 car le cas courant (noms courts) fonctionne déjà avec la seule story 1.

**Independent Test**: Testable en lançant le nettoyage sur un document dont le nom dépasse 20 caractères et en vérifiant que le nom dérivé compte exactement 20 caractères avant le suffixe `-nettoye.md`.

**Acceptance Scenarios**:

1. **Given** un document d'entrée `comptes-rendus-conseil-municipal-session-octobre.md` (49 caractères), **When** l'utilisateur lance le nettoyage, **Then** le fichier nettoyé s'appelle `comptes-rendus-conse-nettoye.md`.
2. **Given** un document d'entrée `rapport.md` (7 caractères), **When** l'utilisateur lance le nettoyage, **Then** le fichier nettoyé s'appelle `rapport-nettoye.md` — aucune troncature sous 20 caractères.
3. **Given** un document d'entrée `éco développement.md`, **When** l'utilisateur lance le nettoyage, **Then** les accents sont conservés et seul le blanc devient `_` : `éco_développement-nettoye.md`.

---

### User Story 3 - Jamais d'écrasement silencieux (Priority: P3)

Un utilisateur traite successivement deux documents dont les noms produisent le même nom de sortie dérivé (même préfixe de 20 caractères, à destination d'un même emplacement). Le premier fichier s'appelle `<nom>-nettoye.md` ; le second `nettoye` du même nom de base devient `<nom>-nettoye-1.md` plutôt que d'écraser le premier. Le suffixe numérique suit l'ordre de traitement.

**Why this priority**: C'est la garantie de sûreté du nommage (décision utilisateur du 2026-10-05) ; priorité moindre car le scénario est rare avec la structure actuelle des dossiers de run (chaque run a son propre sous-dossier), mais la règle interdit tout écrasement silencieux quelle que soit l'évolution de la destination.

**Independent Test**: Testable en simulant deux écritures vers un même nom cible au même emplacement et en vérifiant que la seconde reçoit le suffixe `-1` et que le premier fichier est intact.

**Acceptance Scenarios**:

1. **Given** un emplacement contenant déjà `<nom>-nettoye.md`, **When** un nouveau nettoyage produit le même nom dérivé, **Then** le nouveau fichier s'appelle `<nom>-nettoye-1.md` et l'existant est inchangé.
2. **Given** un emplacement contenant déjà `<nom>-nettoye.md` et `<nom>-nettoye-1.md`, **When** un troisième nettoyage produit le même nom dérivé, **Then** le nouveau fichier s'appelle `<nom>-nettoye-2.md`.

---

### Edge Cases

- Nom d'entrée d'exactement 20 caractères (ex. `retry-failed-records.md`) : aucune troncature, aucun suffixe superflu — l'exemple nominal de l'utilisateur.
- Plusieurs blancs consécutifs dans le nom d'entrée : chaque blanc est remplacé par un `_` (pas de compression), la règle reste caractère par caractère.
- Blancs en début ou fin de nom d'entrée (ex. un nom commençant par un blanc : `rapport.md`) : remplacés par `_` aux extrémités, comme partout ailleurs ; pas de décapage implicite.
- Nom d'entrée ne contenant aucun caractère alphanumérique après remplacement (ex. un stem fait uniquement de blancs, devenant `___`) : le nom dérivé reste utilisé tel quel (`___-nettoye.md`) — pas de renommage de secours, le fichier reste dans son dossier de run dédié.
- Nom d'entrée vide techniquement impossible (le fichier existe) ; nom composé uniquement du suffixe après troncature : traité comme n'importe quel nom dérivé.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: L'outil DOIT nommer le fichier nettoyé d'un run d'après le nom de son document d'entrée : les 20 premiers caractères du nom de fichier sans extension, suivis du suffixe `-nettoye` et de l'extension `.md`.
- **FR-002**: L'outil DOIT remplacer chaque caractère blanc (espace, tabulation) du nom dérivé par `_` ; tout autre caractère (accents, tirets, chiffres, ponctuation) DOIT être conservé tel quel.
- **FR-003**: Lorsque le nom d'entrée dépasse 20 caractères, l'outil DOIT tronquer le nom dérivé aux 20 premiers caractères, sans ajustement à la frontière de mot ; en deçà, aucun remplissage ni troncature.
- **FR-004**: Si le nom de sortie cible existe déjà à l'emplacement d'écriture, l'outil DOIT ajouter un suffixe numérique à la fin du nom, juste avant l'extension `.md` : `-1` au premier conflit, puis `-2`, `-3`, ... par ordre de traitement (ex. `<nom>-nettoye-1.md`) ; l'outil NE DOIT JAMAIS écraser un fichier existant.
- **FR-005**: Les autres artefacts du run (`nettoye-pagine.md`, `cartographie.json`, `suggestion.json`, `rapport-dry-run.md`) et le nommage des dossiers de run (numérotation séquentielle, `--nom-titre`) DOIVENT rester inchangés.
- **FR-006**: Le message de fin de commande DOIT afficher le chemin réel du fichier nettoyé tel que nommé.

### Key Entities

- **Nom de sortie dérivé** : chaîne construite depuis le nom du document d'entrée — base = 20 premiers caractères du nom sans extension, blancs remplacés par `_` ; suffixe invariable `-nettoye` ; extension `.md` ; variantes de collision numérotées (`-1`, `-2`, ...) ajoutées à la fin du nom, avant l'extension. Attributs : déterministe depuis le nom d'entrée, prévisible par l'utilisateur, unique à l'emplacement d'écriture.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Sur un lot de documents aux noms distincts, chaque sortie nettoyée porte un nom unique dérivé de sa source ; aucune ne s'appelle simplement `nettoye.md` (baseline actuelle : toutes s'appellent `nettoye.md`).
- **SC-002**: Pour un nom d'entrée donné, tout utilisateur peut prédire le nom de sortie sans consulter la documentation : règle unique (20 premiers caractères, blancs → `_`, suffixe `-nettoye`), vérifiable sur 100 % des cas de test.
- **SC-003**: Aucun fichier existant n'est écrasé par un nettoyage : tout conflit de nom se solde par un suffixe numérique, vérifiable sur les scénarios de collision (0 écrasement).

## Assumptions

- « Titre du document d'input » désigne le nom de fichier sans extension de l'entrée (tranché par l'exemple utilisateur, cf. Clarifications).
- La troncature est brute aux 20 premiers caractères, sans respect de frontière de mot (arbitrage de prévisibilité, cf. Clarifications).
- Le nouveau nommage remplace le comportement par défaut ; aucun drapeau de repli vers `nettoye.md` n'est introduit (handoff du decide).
- Le fichier nettoyé reste écrit dans son dossier de run dédié ; seule la structure actuelle des dossiers de sortie est conservée.
- Les tests et la documentation existants qui attendent le chemin `nettoye.md` sont mis à jour dans la même livraison (handoff du decide).
