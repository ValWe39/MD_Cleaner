# Data Model: nom de sortie dérivé du document source

**Feature**: 006-nom-sortie-source | **Date**: 2026-10-05

Une seule entité est manipulée ; aucun état persistant nouveau (le nom est calculé, puis utilisé comme chemin d'écriture).

## Entité : Nom de sortie dérivé

Chaîne construite à la volée depuis le nom du document d'entrée, utilisée comme nom de fichier du livrable nettoyé (`.md`).

### Attributs

| Attribut | Règle | Source |
| --------- | ----- | ------ |
| `base` | 20 premiers caractères du nom de fichier d'entrée sans extension (points de code Unicode), chaque blanc (espace U+0020, tabulation U+0009) remplacé par exactement un `_` ; tout autre caractère conservé tel quel ; ni compression ni décapage | FR-001, FR-002, FR-003 |
| `suffixe` | `-nettoye`, invariable | FR-001 |
| `extension` | `.md`, ajoutée par l'appelant après résolution de collision | FR-001 |
| `variante de collision` | Entier ≥ 1, ajouté à la fin du nom avant l'extension (`-1`, `-2`, ...) si le nom cible existe déjà à l'emplacement d'écriture ; ordre de traitement | FR-004 |

### Règles de validation

- `base` vide (stem d'entrée réduit à rien après traitement) : interdit structurellement impossible en pratique — l'entrée existe, son stem est non vide ; un stem uniquement composé de blancs devient une base de `_` répétés, valide telle quelle (cas limite de la spec).
- Unicité : le nom résolu est unique à l'emplacement d'écriture — l'outil n'écrase jamais un fichier existant (FR-004).
- Déterminisme : le nom est une fonction pure du stem d'entrée et des fichiers déjà présents à l'emplacement d'écriture ; sans collision, fonction du seul stem (SC-002).

### Relations

- Dérivé de (1→1) : `Document d'entrée` (son stem). Aucune relation avec le titre de niveau 1 du contenu ni avec le nom du dossier de run (`--nom-titre` reste indépendant).
- Écrit dans (1→1) : `Dossier de run` existant (structure inchangée, FR-005).

### Transitions d'état

Aucune : le nom est calculé puis consommé en une écriture ; il n'est pas persisté ailleurs (la cartographie et la suggestion continuent de référencer le nom du document d'entrée, inchangé).
