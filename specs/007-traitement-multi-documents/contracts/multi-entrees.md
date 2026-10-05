# Contrat CLI : invocation multi-entrées

**Feature**: 007-traitement-multi-documents | **Date**: 2026-10-05 | **Source**: [spec.md](../spec.md), [research.md](../research.md) (D1-D9)

Ce contrat décrit le delta observable apporté à la feature 001 (`specs/001-nettoyage-md-repetitif/contracts/cli.md`, révisé dans la même livraison). Tout ce qui n'est pas mentionné ici est inchangé : options, artefacts par document, messages par document, dossiers de run, codes retour 2 et 3.

## Point d'entrée

```text
md-cleaner <entrée> [<entrée> ...] [options]      # une ou plusieurs entrées
md-cleaner doc1.md doc2.md dossierA [options]     # mélange fichiers + dossiers
python -m md_cleaner <entrée> ...                  # équivalent
```

L'invocation sans argument reste un usage invalide (code 3).

## Résolution des entrées

| Entrée | Résolution |
| ------ | ---------- |
| fichier `.md` existant et lisible | retenu tel quel, à sa position |
| dossier existant | ses fichiers `.md` de premier niveau uniquement, triés par nom (non récursif) ; les autres fichiers sont ignorés sans message |
| dossier sans aucun fichier `.md` (y compris ne contenant que des sous-dossiers) | entrée ignorée avec un message explicite ; le reste du lot est traité |
| chemin inexistant, ou fichier non-`.md` listé directement | conservé dans le lot ; il échoue au traitement avec l'erreur d'entrée actuelle |

- **Ordre de traitement** : ordre d'apparition des arguments ; au sein d'un dossier, ordre alphabétique des noms.
- **Doublons** : chaque occurrence est traitée ; les sorties sont désambiguïsées par le suffixe anti-collision existant (`-1`, `-2`, ...), jamais d'écrasement.
- **Lot vide** (aucun document retenu après résolution) : erreur d'entrée, code 1, aucun traitement.

## Options en lot

- Les paramètres de cleaning (`--pagine`, `--conserver-liens`, `--seuil`, `--calibrage`, `--extrait`, `--nom-titre`, `--sortie`, `--echantillon`) s'appliquent à l'identique à chaque document du lot.
- `--nom-titre` : en mono-document, nomme le dossier de run d'après le titre du document ; en lot de plusieurs, elle est neutralisée avec avertissement (008, FR-005 — voir `specs/008-dossier-sorties-lot/contracts/dossier-de-lot.md`).
- `--dry-run` et `--suggestion` ne sont applicables qu'à un lot d'exactement un document :
  - lot de plusieurs documents → chacune produit un avertissement explicite sur stderr (`AVERTISSEMENT : --dry-run ignorée en lot : applicable à un seul document`, et l'équivalent pour `--suggestion`), est neutralisée, et le lot est traité en nettoyage complet — aucun artefact de dry-run, aucune suggestion consommée ;
  - lot d'un seul document (y compris issu d'un dossier) → comportement actuel inchangé.
- L'incompatibilité `--dry-run` + `--suggestion` ensemble reste une erreur d'usage (code 3), avant résolution du lot.

## Échecs et code retour

- Un document en échec est signalé sur stderr (`ERREUR : <chemin> : <raison>`) ; ses sorties éventuelles n'existent pas, les sorties des documents déjà traités sont conservées.
- Le lot poursuit sur le document suivant ; au **troisième échec consécutif**, il s'arrête immédiatement (les documents suivants ne sont pas traités).
- Code retour de l'invocation :

| Code | Condition d'émission en lot |
| ---- | --------------------------- |
| 0 | tous les documents du lot traités avec succès |
| 1 | au moins un document en échec, ou lot vide |
| 2 | artefact fourni invalide (`--echantillon` vide ou > 5 fichiers) — validation globale avant la boucle |
| 3 | usage invalide (combinaison d'options interdite, argument hors bornes, zéro entrée) |

- Aucun résumé de fin de lot n'est produit : chaque document affiche ses lignes habituelles, les échecs sont tracés individuellement.

## Exemples

```text
md-cleaner a.md b.md c.md          # 1 dossier de run partagé (008), mêmes paramètres
md-cleaner dossierA                # tous les .md de premier niveau, triés par nom
md-cleaner a.md dossierA           # a.md puis les .md du dossier
md-cleaner a.md absent.md b.md      # a.md et b.md traités, absent.md signalé, code 1
md-cleaner a.md b.md --dry-run      # avertissement, dry-run neutralisée, 2 sorties nettoyées
```

## Rétrocompatibilité

`md-cleaner <fichier.md> [options]` est strictement inchangé : mêmes artefacts, mêmes messages, mêmes codes retour (FR-005, SC-005 de la spec 007).
