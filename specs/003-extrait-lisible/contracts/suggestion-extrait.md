# Contrat : suggestion.json (extrait et position) — feature 003

**Feature**: 003-extrait-lisible | **Date**: 2026-09-29 | **Source**: [spec.md](./spec.md), [research.md](./research.md) D1-D4

Ce contrat définit la **révision** apportée au schéma de `suggestion.json` publié par la feature 001 (`specs/001-nettoyage-md-repetitif/contracts/formats.md`, clause `motifs[].extrait` à réviser, et schéma enrichi ci-dessous). Tous les autres champs et règles du contrat d'origine restent applicables.

## Exemple (extrait d'un motif)

```json
{
  "id": "M03",
  "action": "conserver",
  "nb_lignes": 5,
  "frequence": 0.48,
  "pages": [1, 2, 5, 9],
  "extrait": "\nCOUR DES COMPTES \n\n[Famille, handicap, sport et jeunesse](...) -\n",
  "position": {"page": 1, "debut": 92, "fin": 96}
}
```

(Les sauts de ligne de `extrait` sont encodés `\n` dans le fichier ; tout lecteur de JSON les rend ligne par ligne. Dans l'exemple, `fin` est inclue : l'intervalle couvre les lignes 92 à 96 de la page 1.)

## Champ `extrait` (révisé)

| Règle | Valeur |
| ----- | ------ |
| Source | N premières lignes du premier intervalle du motif sur sa page de première occurrence |
| Rendu | vrais sauts de ligne (`\n`), aucune jonction « ` / ` » |
| N | défaut 5 ; option `--extrait N`, entier 2-25 |
| Intervalle plus court que N | l'extrait rend tout ce qui existe, jamais de complément inventé |
| Troncature | aucune dans le JSON (surface de jugement) ; seule la taille totale est gardée (< 1 Mo sur le corpus) |

## Champ `position` (nouveau)

| Règle | Valeur |
| ----- | ------ |
| Structure | objet `{"page": P, "debut": D, "fin": F}` |
| Sémantique | première occurrence du motif : lignes D à F (**fin inclue**) de la page P du document d'origine |
| Garanties | la ligne D de la page P appartient réellement au motif (SC-003) ; même ancrage que l'extrait |
| À la relecture | absence acceptée (suggestions d'avant-feature) ; présence mal formée (types, bornes, clés) → code retour 2, message clair |

## Option `--extrait N` (CLI)

```text
--extrait N    nombre de lignes d'extrait dans suggestion.json
               (entier 2-25, défaut 5) ; effet limité à la génération
               de la suggestion, sans effet observable hors --dry-run
```

- Hors bornes → usage invalide, code retour 3
- Hors `--dry-run` → acceptée, sans effet observable (le nettoyage simple ne génère pas de suggestion)

## Invariance (rappel contractuel)

La longueur et le contenu des extraits n'ont **aucune incidence** sur le nettoyage : seuls `id` et `action` d'un motif pilotent la décision (héritage du contrat de la feature 001, FR-009 de la spec 003). Une suggestion d'extraits courts ou longs produit le même `nettoye.md`.

## Rapport dry-run (non concerné par la révision)

Le rapport reste un aperçu non contractuel : structure en deux sections de la feature 002, troncature à 120 caractères, avec neutralisation des sauts de ligne dans les cellules du tableau (garde-fou de forme, D5).
