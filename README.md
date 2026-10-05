# MD_Cleaner

Outil de nettoyage de fichiers Markdown multi-pages : il détecte les
éléments répétitifs (menus de navigation, fils d'Ariane, pieds de page,
filtres, pagination d'interface) et ne conserve que le contenu textuel
de valeur. 100 % local, déterministe, zéro dépendance runtime.

## Démarrage rapide (PowerShell)

Ouvrez PowerShell dans le dossier du projet, puis copiez-collez les
blocs ci-dessous dans l'ordre. Chaque bloc s'exécute d'une traite.

### Étape 1 — Installer l'outil (une seule fois)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
pip install -r requirements.txt
md-cleaner --help
```

Si PowerShell affiche « l'exécution de scripts est désactivée »,
copiez-collez la ligne ci-dessous puis relancez l'activation :

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

Quand `md-cleaner --help` affiche la liste des options, l'outil est prêt.
Dans les sessions suivantes, seule l'activation est à refaire :

```powershell
.venv\Scripts\Activate.ps1
```

### Étape 2 — Effectuer une requête (nettoyer un fichier)

Mettez le chemin du fichier dans une variable, puis lancez l'outil :

```powershell
$fichier = ".\Examples\Exemple_1\2.Input\consolidated.md"
md-cleaner $fichier
```

Le résultat est créé dans un sous-dossier numéroté de `output`
(001, puis 002 au run suivant, etc.). Le fichier nettoyé est nommé
d'après le document d'entrée : les 20 premiers caractères de son nom,
espaces remplacées par `_`, suivis du suffixe `-nettoye`
(`consolidated.md` → `consolidated-nettoye.md`). En cas de conflit
de nom, un numéro est ajouté à la fin (`-nettoye-1.md`, jamais
d'écrasement). Ouvrez-le :

```powershell
notepad .\output\001\consolidated-nettoye.md
```

### Étape 3 — Jouer sur les paramètres

Chaque run crée le numéro suivant (002, 003, ...) : le dry-run ci-dessous
crée donc `.\output\002`, puisque l'étape 2 a déjà utilisé le 001.

```powershell
md-cleaner $fichier --dry-run
notepad .\output\002\rapport-dry-run.md
notepad .\output\002\suggestion.json
```

Chaque motif y présente un extrait multi-lignes (5 lignes par défaut)
et sa position (`page`, `debut`, `fin`) dans le document d'origine —
de quoi juger sans ouvrir le document source.

Dans `suggestion.json`, remplacez une action `"supprimer"` par
`"conserver"` (ou l'inverse) pour garder ou retirer un motif, sauvegardez,
puis relancez le nettoyage avec votre version :

```powershell
md-cleaner $fichier --suggestion .\output\002\suggestion.json
```

Les autres paramètres, combinables librement :

```powershell
md-cleaner $fichier --pagine
md-cleaner $fichier --seuil 95
md-cleaner $fichier --conserver-liens
md-cleaner $fichier --dry-run --extrait 12
md-cleaner $fichier --nom-titre 30
md-cleaner $fichier --sortie .\mes-sorties
md-cleaner $fichier --echantillon .\Examples\Exemple_2\1.Sample
```

```text
--pagine        : ajoute nettoye-pagine.md + cartographie.json (RAG)
--conserver-liens : garde les destinations de liens inline ](<...>), tout
                   schéma confondu, dans les sorties .md (retirées par défaut)
--seuil N       : seuil de fréquence en % de pages (défaut 80)
--nom-titre X   : nomme le run d'après les X premiers caractères du titre
--sortie D      : dossier racine des sorties (défaut .\output)
--echantillon D : calibrage sur un échantillon (5 fichiers .md max)
--extrait N    : lignes d'extrait dans suggestion.json (2-25, défaut 5)
--calibrage N   : pages d'auto-calibrage (défaut 5)
```

Contrat CLI complet : `specs/001-nettoyage-md-repetitif/contracts/cli.md`.
Règle de nommage du fichier nettoyé :
`specs/006-nom-sortie-source/contracts/nommage-sortie.md`.

## Traiter plusieurs documents (feature 007)

Une invocation accepte plusieurs documents à la suite — des fichiers
`.md`, des dossiers, ou un mélange :

```powershell
md-cleaner doc1.md doc2.md doc3.md
md-cleaner dossierA          # seuls les .md du premier niveau, triés par nom
md-cleaner doc1.md dossierA   # doc1, puis les .md du dossier
```

Chaque document est traité avec les mêmes paramètres de cleaning, dans
l'ordre des arguments, et **toutes les sorties de l'invocation vont dans
un seul et même dossier de run numéroté** (`output\00X`). Les doublons
sont traités à chaque occurrence (sorties suffixées `-1`, `-2`, jamais
d'écrasement).

Points d'attention :

- En lot de plusieurs avec `--pagine`, les sorties secondaires sont
  préfixées par le nom du document : `doc-nettoye-pagine.md`,
  `doc-cartographie.json` (noms courts inchangés pour un seul document).
- `--dry-run`, `--suggestion` et `--nom-titre` ne s'appliquent qu'à un
  lot d'un seul document ; en lot de plusieurs, elles sont neutralisées
  avec un avertissement explicite et le lot est nettoyé (dossier
  numéroté pour `--nom-titre`).
- Un document en échec est signalé (`ERREUR : ...` sur stderr) et le
  lot poursuit ; au troisième échec consécutif, le lot s'arrête net.
- Code retour : 0 si tous les documents ont réussi, 1 sinon.
- Un dossier sans fichier `.md` est ignoré avec un message ; si aucun
  document n'est retenu, l'invocation échoue (code 1).

Règles complètes :
`specs/007-traitement-multi-documents/contracts/multi-entrees.md` et
`specs/008-dossier-sorties-lot/contracts/dossier-de-lot.md`.

## Notes de version

Les ids de motifs (M01, M02, ...) ne sont pas stables entre versions de
l'outil : après une mise à jour, régénérez la suggestion par un
`--dry-run`. Une suggestion issue d'une version antérieure échoue
proprement (id inconnu, code retour 2) ou, si les ids coïncident,
s'applique à des motifs différents — dans tous les cas, régénérez.

## Sources des fichiers d'exemple

Les fichiers du dossier `Examples/` sont des extraits bruts de pages
publiques, utilisés uniquement comme données de test d'une fonction
de nettoyage de Markdown sans lien avec les sites d'origine ni leurs
contenus. Aucune exploitation commerciale n'en est faite.

- `Examples/Exemple_1/` : pages de Corsen Academy — Mistral AI
  (<https://corsen.ai/fr/formations/mistral-ai>), consultées en
  septembre 2026. © CORSEN AI — tous droits réservés.
- `Examples/Exemple_2/` : pages « Publications » de la Cour des
  comptes (<https://www.ccomptes.fr/fr>), consultées en septembre 2026.
  Source citée conformément aux mentions légales du site ; le propos
  des textes n'est pas altéré, seuls les éléments d'interface ont
  été retirés.

Ces contenus restent la propriété de leurs ayants droit respectifs
et ne sont pas couverts par la licence du présent outil. Toute
réutilisation des exemples reste soumise aux conditions définies
par les sites d'origine ; toute demande de retrait sera honorée.

## Développement

```powershell
pytest
pre-commit run --all-files
```

Conformité à la constitution du projet (v1.4.0) : local-first sans
réseau, aucune dépendance runtime, secrets exclus, sorties uniquement
dans `output/` (supprimables par l'utilisateur).
