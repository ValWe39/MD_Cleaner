# Research: nom de sortie dérivé du document source

**Feature**: 006-nom-sortie-source | **Date**: 2026-10-05

## Contexte technique observé

- Point d'écriture : `md_cleaner/cli.py:210` (`ecrire_nettoye(dossier / "nettoye.md", ...)`) et `md_cleaner/cli.py:222` (message `Sortie : ...`).
- Chaque run écrit dans son propre sous-dossier créé par `creer_dossier_run` (`md_cleaner/sortie.py`) : numérotation `001`, `002`, ... ou slug de titre via `--nom-titre` ; collision de dossiers suffixée `-2`, `-3` (commence à 2).
- `normalisation.py:37` fournit `slug_titre(texte, x)` : NFKD, accents retirés, minuscules, tout non-alphanumérique → `-`, tronqué à x. **Non réutilisable** : la spec exige espaces → `_`, accents et casse conservés, autres caractères conservés.
- Impact inventorié (`grep nettoye.md`) : `md_cleaner/cli.py` (2 points), 7 fichiers de tests d'intégration (~20 chemins attendus), `README.md` (2 mentions), `specs/001-nettoyage-md-repetitif/contracts/cli.md` (table des artefacts, lignes 38-39).

## Décisions

### D1 — Nouvelle fonction pure de nommage dans `normalisation.py`

- **Decision**: Ajouter `nom_sortie_nettoye(stem: str) -> str` dans `md_cleaner/normalisation.py` (module déjà dédié aux transformations de chaînes) : retourne les 20 premiers caractères du stem, blancs remplacés par `_`, suivis du suffixe invariable `-nettoye`. L'extension `.md` est ajoutée par l'appelant.
- **Rationale**: Transformation pure, testable unitairement, au côté de `slug_titre` sans la toucher ; `sortie.py` garde la logique d'emplacement (dossiers, collisions), `cli.py` l'assemblage.
- **Alternatives considered**: réutiliser `slug_titre` (rejeté : minuscules, accents retirés, `-` au lieu de `_`) ; loger le nommage dans `sortie.py` (rejeté : mélange transformation pure et emplacement).

### D2 — Périmètre exact des blancs et des autres caractères

- **Decision**: Seuls l'espace (U+0020) et la tabulation (U+0009) sont remplacés, chacun par exactement un `_` (pas de compression des séquences, pas de décapage aux extrémités). Tout autre caractère (accents, tirets, chiffres, ponctuation) est conservé tel quel. Le comptage des 20 caractères se fait en points de code Unicode (`len()`), pas en octets.
- **Rationale**: FR-002 (espaces, tabulations) et FR-003 (troncature brute) ; la source existe déjà sur le système de fichiers, son stem est donc déjà un nom valide — aucun risque de caractère interdit introduit par la transformation, qui n'ajoute que `_` et `-nettoye`.
- **Alternatives considered**: classe de blancs étendue (rejeté : hors FR-002, imprévisible) ; compression des `_` multiples (rejeté : contredit FR-002 « chaque caractère blanc », teste `rapport  annuel.md` différemment).

### D3 — Ordre troncature / remplacement indifférent (à documenter, pas à spécifier)

- **Decision**: Le remplacement étant bijectif caractère à caractère, tronquer à 20 puis remplacer ou remplacer puis tronquer produisent le même résultat ; l'implémentation remplacera d'abord puis tronquera (une seule passe lisible).
- **Rationale**: Élimine un faux point de décision pour l'implémentation et les tests.
- **Alternatives considered**: aucune — équivalence démontrée par la bijection du remplacement.

### D4 — Résolution de collision dans `sortie.py`, suffixe commençant à `-1`

- **Decision**: Ajouter dans `md_cleaner/sortie.py` une résolution du nom de fichier cible : si `<base>-nettoye.md` existe déjà à l'emplacement d'écriture, essayer `<base>-nettoye-1.md`, puis `-2`, `-3`, ... par ordre de traitement. Le suffixe est ajouté à la fin du nom, avant l'extension (FR-004, clarification du 2026-10-05).
- **Rationale**: Le dossier de run étant fraîchement créé, la collision ne survient jamais en pratique aujourd'hui ; la boucle est une garantie (`NE DOIT JAMAIS écraser`) à coût nul. Le départ à `-1` (et non `-2` comme `creer_dossier_run`) suit la décision explicite de l'utilisateur et la spec.
- **Alternatives considered**: s'appuyer sur l'exclusivité du dossier de run sans boucle (rejeté : FR-004 inconditionnel) ; réutiliser la boucle des dossiers (rejeté : départ à -2, position du suffixe différente).

### D5 — Câblage CLI : un seul point de calcul du nom

- **Decision**: Dans `cli.py`, calculer le chemin nettoyé une fois (après création du dossier de run) : `nom = nom_sortie_nettoye(fichier.stem)` puis résolution de collision ; utiliser ce chemin pour `ecrire_nettoye` ET pour le message `Sortie : ...` (FR-006). `nettoye-pagine.md` et les autres artefacts restent inchangés (FR-005).
- **Rationale**: Écriture et affichage ne peuvent pas diverger ; diff minimal (2 lignes modifiées + 1 import).
- **Alternatives considered**: option CLI de repli vers `nettoye.md` (rejeté : spec, décision du decide) ; renommer aussi les autres artefacts (rejeté : hors périmètre, option B du concept).

### D6 — Mise à jour des tests et documents existants dans la même livraison

- **Decision**: Mettre à jour les ~20 chemins attendus dans les 7 fichiers de `tests/integration/` (chaque test connaît le stem de son entrée : le nom attendu devient `<stem>-nettoye.md`, tronqué à 20 si besoin), les 2 mentions du `README.md`, et réviser la table des artefacts de `specs/001-nettoyage-md-repetitif/contracts/cli.md` (précédent : feature 005 révisant le contrat 004). Ajouter les tests unitaires du nommage (`tests/unit/test_normalisation.py`) et de la collision (`sortie.py`), plus les tests d'intégration des User Stories (US1 : nom exact ; US2 : troncature, accents conservés ; US3 : collision -1/-2 sans écrasement).
- **Rationale**: Handoff du decide (« tests et documentation mis à jour dans la même livraison ») ; cohérence avec le précédent de la feature 005.
- **Alternatives considered**: livrer le nommage sans toucher aux tests (rejeté : la suite échouerait immédiatement).

## Inconnues restantes

Aucune : les points ouverts de la spec ont été arbitrés en session de clarification du 2026-10-05 (position du suffixe de collision, troncature brute).
