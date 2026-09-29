# Data Model : Nettoyage de fichiers Markdown répétitifs

**Feature**: 001-nettoyage-md-repetitif | **Date**: 2026-09-29 | **Source**: [spec.md](./spec.md), [research.md](./research.md)

Entités dérivées des exigences (FR-001 à FR-016). Aucun stockage persistant : les entités vivent en mémoire pendant le run et se matérialisent en fichiers dans `output/<run>/`.

## DocumentSource

Le fichier `.md` fourni en entrée, un par exécution (FR-001).

| Champ | Type | Règles de validation |
| ----- | ---- | -------------------- |
| chemin | chemin | Existant, lisible, extension `.md` ; sinon échec rapide avec message clair (FR-015) |
| titre | texte | Premier titre niveau 1 du document ; sinon nom du fichier (D8) |
| contenu | texte | Décodage UTF-8 avec BOM toléré ; lignes conservées telles quelles |
| mode_segmentation | `explicite` \| `heuristique` \| `unique` | Déterminé par segmentation (D4) ; `heuristique` signalé dans les sorties |

## Page

Subdivision du document source (FR-011). Les pages sont numérotées à partir de 1 dans l'ordre du document.

| Champ | Type | Règles |
| ----- | ---- | ------ |
| numero | entier ≥ 1 | Séquentiel, sans trou ; déterministe |
| url_source | URL ou absent | Capturée depuis le séparateur explicite `## Page N: URL` si présente |
| lignes | liste | Découpage du contenu de la page en lignes |
| blocs | liste de BlocContenu | Remplis au nettoyage |

## MotifRepetitif

Bloc récurrent détecté (FR-002, FR-003, D3). Généré par la détection ou chargé depuis `suggestion.json`.

| Champ | Type | Règles |
| ----- | ---- | ------ |
| id | `M01`, `M02`, … | Séquentiel, attribué par ordre (première occurrence, fréquence décroissante, hachage) — déterministe (D9) |
| action | `supprimer` \| `conserver` | Défaut : `supprimer` si fréquence ≥ seuil, sinon `conserver` ; modifiable dans `suggestion.json` (FR-008) |
| lignes_norm | liste de textes | Forme normalisée (URL → `<URL>`, nombre → `<N>`, date → `<DATE>`) servant à la correspondance |
| extrait | texte ≤ 3 lignes | Affiché dans le rapport dry-run et la suggestion |
| frequence | décimal [0, 1] | Pages contenant le motif / pages totales (D3) |
| pages | liste d'entiers | Numéros des pages où le motif apparaît |
| nb_lignes | entier ≥ 1 | Longueur du bloc |

## Suggestion (fichier `suggestion.json`)

Artefact éditable produit par le dry-run, consommé par le run de nettoyage (FR-007, FR-008, D5). Schéma détaillé dans [contracts/formats.md](./contracts/formats.md).

| Champ | Type | Règles |
| ----- | ---- | ------ |
| version | entier | `1` ; toute autre valeur → échec de validation |
| source | nom de fichier | Doit correspondre au fichier d'entrée du run qui la consomme |
| seuil | entier [2, 100] | Seuil effectif utilisé pour la détection |
| motifs | liste de MotifRepetitif | Ids uniques ; validation stricte au chargement (id inconnu ou JSON invalide → échec rapide) |

## BlocContenu

Segment de contenu de valeur conservé dans les sorties (FR-004), unité de localisation pour le RAG (FR-009, FR-010).

| Champ | Type | Règles |
| ----- | ---- | ------ |
| id | `P{n}-B{k}` | Page n, bloc k dans l'ordre du document — déterministe (D9) |
| page | entier ≥ 1 | Page d'origine |
| texte | liste de lignes | Contenu non altéré (formulation, ordre, hiérarchie de titres) |
| debut / fin | entiers | Indices de lignes dans la page d'origine |

## RunSortie

Sous-dossier de `output/` regroupant les résultats d'une exécution (FR-006, D8).

| Champ | Type | Règles |
| ----- | ---- | ------ |
| dossier | nom | `NNN` séquentiel (défaut) ou slug des X premiers caractères du titre (`--nom-titre`) ; collision → suffixe `-2`, `-3`… |
| nettoye.md | fichier | Toujours produit en mode nettoyage |
| nettoye-pagine.md | fichier | Si `--pagine` : idem + marqueurs `---` / `<!-- page: N -->` par page (D6) |
| cartographie.json | fichier | Si `--pagine` : cohérence garantie avec `nettoye-pagine.md` (FR-010) |
| rapport-dry-run.md, suggestion.json | fichiers | Si dry-run |
| autres | fichiers | Jamais de copie cachée ailleurs (Data Retention) |

## Cartographie (fichier `cartographie.json`)

Correspondance bloc → page pour le RAG (FR-010, clarification Q3 → A). Schéma détaillé dans [contracts/formats.md](./contracts/formats.md).

| Champ | Type | Règles |
| ----- | ---- | ------ |
| version | entier | `1` |
| source | nom de fichier | Document d'origine |
| mode_pagination | `explicite` \| `heuristique` \| `unique` | `heuristique` signalé : pagination recréée (FR-011) |
| pages | liste | Page, url_source, ids des blocs, marqueur |
| blocs | liste | Id, page, debut/fin — couvre 100 % des blocs de la sortie paginée |

## Relations

```text
DocumentSource 1──n Page 1──n BlocContenu
DocumentSource 1──n MotifRepetitif (détectés sur ses pages)
Suggestion n──n MotifRepetitif (référence par id + lignes_norm)
RunSortie 1──1 DocumentSource (par exécution)
Cartographie 1──n BlocContenu (via ids P{n}-B{k})
```

## Règles transverses

- **Cohérence cartographie / sortie paginée** (FR-010) : tout bloc présent dans `nettoye-pagine.md` figure dans `cartographie.json` et réciproquement ; le nombre de marqueurs `<!-- page: N -->` égale le nombre d'entrées de `pages`.
- **Déterminisme** (FR-005) : à entrées et options identiques, tous les fichiers produits sont identiques octet par octet — ids stables, clés JSON triées, séparateurs de sérialisation fixes.
- **Transitions d'état du run** : `validation entrée` → `segmentation` → `détection` → (`dry-run : arrêt`) → `application de la suggestion` → `sorties` → `fin`. Chaque transition peut échouer rapidement avec un message clair (FR-015) ; aucun état persisté entre exécutions.
