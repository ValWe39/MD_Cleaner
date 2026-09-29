# Research : Nettoyage de fichiers Markdown répétitifs

**Feature**: 001-nettoyage-md-repetitif | **Date**: 2026-09-29 | **Source**: [spec.md](./spec.md), [plan.md](./plan.md)

Chaque décision suit le format : Décision → Rationale → Alternatives considérées.

## D1. Langage et version

- **Décision** : Python 3.12.
- **Rationale** : le dépôt est déjà outillé Python (CI `setup-python 3.12`, Ruff, `pip-audit`, scripts `.github/workflows/scripts/*.py`). Un seul environnement à maintenir.
- **Alternatives** : Rust/Go (compilation, complexité non justifiée pour un outil de traitement texte), Node (markdownlint déjà en CI mais aucun runtime JS dans le projet).

## D2. Dépendances runtime : zéro (stdlib uniquement)

- **Décision** : aucune bibliothèque externe en runtime. Modules utilisés : `argparse`, `re`, `json`, `pathlib`, `difflib`, `collections`, `unicodedata`.
- **Rationale** : déterminisme maximal (pas de versions de dépendances à épingler), surface d'audit minimale (principe III), aucun risque de télémétrie, installation sans réseau possible (principe II). La détection de boilerplate repose sur la récurrence textuelle, pas sur un arbre syntaxique — un parseur CommonMark n'apporte rien : les entrées sont des conversions HTML → Markdown dont la validité syntaxique n'est pas garantie (champs `## Page N: URL`, listes à indentation non standard, etc.).
- **Alternatives** : `markdown-it-py` (MIT) — rejeté : parsing AST inutile et fragile sur des entrées non conformes ; `tree-sitter-markdown` — rejeté : binaire natif, lourd ; LLM — rejeté : non déterministe (FR-005) et réseau (principe II).

## D3. Algorithme de détection des motifs répétitifs

- **Décision** : pipeline en trois passes, entièrement déterministe :
  1. **Normalisation de lignes** : URLs → `<URL>`, nombres entiers/décimaux → `<N>`, dates (formats courants) → `<DATE>`, pliage des espaces multiples. C'est ce qui rend un motif reconnaissable malgré ses parties variables (FR-003 : numéros de leçon, dates, numéros de page).
  2. **Fenêtres glissantes de lignes** : pour chaque longueur de fenêtre w de 1 à W (W = 25 lignes, borne YAGNI), les séquences normalisées de w lignes sont groupées par hachage de leur contenu ; une fenêtre présente sur ≥ seuil des pages est candidate « motif ».
  3. **Fusion et maximisation** : les fenêtres candidates qui se chevauchent sont fusionnées en blocs maximaux (un motif couvrant w=20 absorbe ses sous-fenêtres w<20). Chaque motif reçoit un id déterministe `M01`, `M02`, … trié par (position de première occurrence, fréquence décroissante, hachage).
- **Rationale** : la répartition en blocs récurrents est le comportement observé dans les exemples (nav de 27 lignes identique sur chaque page, footer identique, fil d'Ariane variant par le numéro de leçon). Le seuil par défaut de 80 % des pages correspond à FR-002 ; les motifs sous le seuil sont listés dans le rapport dry-run sans être appliqués (cas limite « fréquence partielle »).
- **Alternatives** : clustering (k-means, embeddings) — non déterministe ou coûteux, overkill ; arbre des suffixes — détection de répétitions maximales élégante mais complexité d'implémentation inutile à l'échelle visée ; diff par paires de pages (O(pages²)) — possible avec `difflib` mais la fusion de n pages de diffs est moins directe que le comptage par fenêtres.

## D4. Segmentation en pages

- **Décision** : priorité aux séparateurs explicites par expression rationnelle `^#{1,6}\s*[Pp]age\s+(\d+)\s*(?::\s*(\S+))?$` (capture le numéro et l'URL source éventuelle). À défaut, repli heuristique déterministe : les « lignes frontière » (fenêtres d'1–3 lignes normalisées récurrentes en début de segment) servent de points de coupe ; la récurrence est mesurée sur tout le document avec le même seuil que la détection. Si aucune frontière fiable n'est trouvée (moins de 2 segments), le document est traité comme une seule section et l'outil le signale explicitement (FR-011 : signaler plutôt que produire une pagination trompeuse).
- **Rationale** : les deux corpus d'exemples utilisent `## Page N: URL` ; le repli heuristique couvre le cas « recréer la pagination » sans sacrifier le déterminisme (règles fixes, aucune approximation statistique).
- **Alternatives** : uniquement les séparateurs explicites (option rejetée en clarification, Q2 → C) ; détection par densité de titres (fragile, non déterministe dans l'ordre de traitement).

## D5. Dry-run et suggestion éditable

- **Décision** : le dry-run produit **deux fichiers** dans le dossier du run : `rapport-dry-run.md` (lisible : chaque motif avec extrait, fréquence, pages concernées, motifs sous le seuil signalés) et `suggestion.json` (éditable : id, extrait, fréquence, champ `action` = `supprimer`/`conserver`). Le run de nettoyage consomme `suggestion.json` via `--suggestion` ; l'utilisateur peut y basculer des motifs de `supprimer` à `conserver` ou inversement (clarification session 2026-09-29, option B). Sans `--suggestion` et sans dry-run : la suggestion par défaut est calculée puis appliquée directement.
- **Rationale** : un rapport lisible pour l'humain et un fichier structuré pour la machine — le JSON est parsable sans ambiguïté et reste vérifiable. La validation du fichier consommé échoue rapidement avec un message clair si un id est inconnu ou si le JSON est invalide (FR-015).
- **Alternatives** : un seul fichier hybride (frontière rapport/machine fragile) ; validation interactive terminal (non scriptable, rejetée en clarification).

## D6. Format de la sortie paginée et de la cartographie

- **Décision** : le `.md` paginé porte des marqueurs lisibles : chaque page d'origine commence par un séparateur `---` suivi d'un commentaire HTML `<!-- page: N -->` (lisible en source, invisible au rendu — n'altère pas la hiérarchie des titres du contenu). La cartographie JSON (clarification Q1 → C puis Q3 → A) vit à côté : chaque entrée associe un id de bloc (`P{n}-B{k}`), sa page d'origine et l'URL source.
- **Rationale** : le fichier paginé reste autonome pour la lecture humaine ; le RAG futur consomme la cartographie structurée ; aucun risque de collision avec les titres du contenu (`##` conservés pour le contenu réel).
- **Alternatives** : conserver les séparateurs d'origine `## Page N: URL` dans le corps (pollue la hiérarchie de titres) ; identifiants de blocs visibles dans le texte (bruit de lecture, rejeté en clarification Q5 → A).

## D7. Calibrage : échantillon fourni ou auto-calibrage

- **Décision** : auto-calibrage par défaut sur les N = 5 premières pages détectées du document (les fenêtres candidates sont comptées sur l'échantillon, puis les fréquences sont confirmées sur le document complet) ; option `--echantillon <dossier>` pour calibrer sur les pages fournies par l'utilisateur (≤ 5 fichiers `.md`, triés par nom).
- **Rationale** : N = 5 aligne le défaut sur l'usage documenté des dossiers `1.Sample/` (5 pages) ; le calibrage sur échantillon réduit le bruit des pages atypiques ; la confirmation sur document complet maintient le seuil global.
- **Alternatives** : calibrage sur 100 % du document (plus lent, inutile — les motifs de boilerplate sont stables dès quelques pages) ; N variable (non justifié).

## D8. Dossier de sortie et nommage des runs

- **Décision** : dossier `./output` par défaut (`--sortie`), sous-dossier de run numéroté séquentiellement (`001`, `002`, … selon les dossiers existants, tri lexicographique, zéro-paddé sur 3 chiffres) ; option `--nom-titre X` pour dériver le nom du slug des X premiers caractères du titre du document (défaut X = 30, slug ASCII). Collision de nom → suffixe `-2`, `-3`, … Le titre du document = premier titre de niveau 1, sinon nom de fichier.
- **Rationale** : numérotation = tri chronologique lisible, jamais de collision ; dérivation du titre = repérage humain (FR-006).
- **Alternatives** : horodatage (viol FR-005 : non déterministe) ; UUID (illisible, non déterministe).

## D9. Déterminisme : garanties concrètes

- **Décision** : ordre de traitement fixe (haut vers bas), ids séquentiels triés, JSON sérialisé avec clés triées et séparateurs fixes, aucune dépendance à l'heure ou à l'entropie, itérations sur structures triées (jamais sur des sets non ordonnés), chemins émis en relatif au dossier de run. Test de non-régression : deux exécutions successives → sorties identiques octet par octet (SC-002).
- **Rationale** : FR-005 ; condition d'acceptation testable mécaniquement.
- **Alternatives** : aucun — exigence de la spec.

## D10. Packaging et tests

- **Décision** : `pyproject.toml` minimal (setuptools), console script `md-cleaner` + `python -m md_cleaner` ; `requirements.txt` listant pytest pour le job CI `pip-audit` (actuellement absent du dépôt, ce qui fait échouer le job `audit` hebdo — sa création répare ce défaut préexistant) ; `pytest` avec tests unitaires par module et tests d'intégration sur `Examples/`.
- **Rationale** : standards de l'écosystème, coût minimal ; le CI existant lint Ruff et audite pip-audit sans modification.
- **Alternatives** : script unique sans packaging (pas d'installation propre ni de tests découvrables) ; hatchling/poetry (plus lourd, aucun bénéfice ici).
