# Formats des fichiers : suggestion.json et cartographie.json

**Feature**: 001-nettoyage-md-repetitif | **Date**: 2026-09-29 | **Source**: [data-model.md](../data-model.md), [research.md](../research.md)

Deux formats JSON échangés avec l'utilisateur ou avec le futur RAG. Sérialisation déterministe : clés triées, indentation de 2 espaces, séparateurs fixes (guillemets sur les clés, `": "` / `","`), fin de fichier par un saut de ligne unique.

## suggestion.json

Produit par `--dry-run`, éditable par l'humain, consommé par `--suggestion` (FR-007, FR-008).

```json
{
  "version": 1,
  "source": "consolidated.md",
  "seuil": 80,
  "mode_segmentation": "explicite",
  "nb_pages": 14,
  "motifs": [
    {
      "id": "M01",
      "action": "supprimer",
      "nb_lignes": 27,
      "frequence": 1.0,
      "pages": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
      "extrait": "Aller au contenu principal
[CORSEN AI](</fr/>)
..." ,
      "position": {"page": 1, "debut": 1, "fin": 27}
    },
    {
      "id": "M04",
      "action": "conserver",
      "nb_lignes": 1,
      "frequence": 0.57,
      "pages": [1, 2, 3, 4, 5, 6, 7, 8],
      "extrait": "Lecon suivante ...",
      "position": {"page": 1, "debut": 40, "fin": 40}
    }
  ]
}
```

| Champ | Type | Contraintes |
| ----- | ---- | ----------- |
| `version` | entier | Doit valoir `1` |
| `source` | texte | Nom de base du fichier d'entrée ; vérifié au chargement |
| `seuil` | entier 2–100 | Seuil utilisé pour la détection |
| `mode_segmentation` | `explicite` \| `heuristique` \| `unique` | Information du rapport |
| `nb_pages` | entier ≥ 1 | Pages détectées dans le document |
| `motifs[].id` | `M\d{2}` | Unique, stable entre dry-run et run |
| `motifs[].action` | `supprimer` \| `conserver` | Seul champ destiné à l'édition humaine |
| `motifs[].frequence` | décimal [0, 1] | Arrondi à 2 décimales |
| `motifs[].pages` | liste d'entiers | Triée croissante |
| `motifs[].extrait` | texte | Révisé par la feature 003 : N premières lignes du premier intervalle de la page de première occurrence (N défaut 5, option `--extrait` 2–25), rendues en vrais sauts de ligne ; intervalle plus court → tout ce qui existe |
| `motifs[].position` | objet `{page, debut, fin}` | Feature 003 : première occurrence, `fin` inclue ; absent des suggestions d'avant-feature (accepté à la relecture), mal formé → code 2 |

Révision de contrat (feature 003, FR-007) : la clause « extrait ≤ 3 lignes jointes par ` / ` » de la feature 001 est remplacée par la définition ci-dessus ; détail complet dans `specs/003-extrait-lisible/contracts/suggestion-extrait.md`.

Validation au chargement (`--suggestion`) : échec rapide (code 2) si JSON invalide, `version` incorrecte, `source` ne correspondant pas à l'entrée, id dupliqué ou `action` invalide. Le run de nettoyage apparie chaque motif au document par `id` + lignes normalisées recalculées ; un id sans correspondance est une erreur bloquante, signalée avec son libellé.

## cartographie.json

Produit avec `--pagine` (FR-009, FR-010), consommé par le futur RAG.

```json
{
  "version": 1,
  "source": "consolidated.md",
  "mode_pagination": "explicite",
  "pages": [
    {
      "page": 1,
      "url_source": "https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/1/",
      "marqueur": "<!-- page: 1 -->",
      "blocs": ["P1-B1", "P1-B2"]
    }
  ],
  "blocs": [
    {
      "id": "P1-B1",
      "page": 1,
      "debut": 41,
      "fin": 97
    }
  ]
}
```

| Champ | Type | Contraintes |
| ----- | ---- | ----------- |
| `version` | entier | `1` |
| `source` | texte | Nom de base du document d'origine |
| `mode_pagination` | `explicite` \| `heuristique` \| `unique` | `heuristique` signale une pagination recréée (FR-011) |
| `pages[].page` | entier ≥ 1 | Séquentiel, sans trou |
| `pages[].url_source` | URL ou absent | Absent si le séparateur d'origine n'en portait pas |
| `pages[].marqueur` | texte | Chaîne exacte insérée dans `nettoye-pagine.md` |
| `pages[].blocs` | liste d'ids | Ids des blocs de la page, triés |
| `blocs[].id` | `P\d+-B\d+` | Unique |
| `blocs[].debut` / `fin` | entiers ≥ 0 | Indices de lignes dans la page d'origine, `fin` incluse |

**Contrat de cohérence** (FR-010) : l'ensemble des `blocs[].id` de `cartographie.json` est exactement l'ensemble référencé par `pages[].blocs`, et chaque marqueur `marqueur` apparaît une fois et une seule dans `nettoye-pagine.md` à la position de sa page. Les blocs sont séparés du contenu supprimé : aucune entrée ne référence un motif de `suggestion.json`.

## Rapport dry-run (rapport-dry-run.md)

Markdown lisible : tableau des motifs (id, extrait, fréquence, pages, action suggérée), section « motifs sous le seuil », section « cas limites » (document à page unique, sortie quasi vide, segmentation heuristique), et rappel de la commande pour consommer la suggestion éditée. Structure indicative — seul `suggestion.json` est contractuel.
