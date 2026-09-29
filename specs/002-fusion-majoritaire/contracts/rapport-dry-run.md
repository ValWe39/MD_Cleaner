# Contrat : rapport dry-run (structure indicative)

**Feature**: 002-fusion-majoritaire | **Date**: 2026-09-29 | **Source**: [spec.md](./spec.md) FR-004, [contracts/formats.md de la feature 001](../../001-nettoyage-md-repetitif/contracts/formats.md)

Rappel de statut hérité : seul `suggestion.json` est contractuel ; le rapport `rapport-dry-run.md` a une structure **indicative**, mais la présente feature en fixe l'organisation cible pour rendre la validation humaine praticable sur les documents riches.

## Structure cible

```markdown
# Rapport dry-run

Source : <fichier>
Seuil : <N> % des <P> pages
Mode de segmentation : <mode>

## Décisions requises

| Id | Action suggérée | Fréquence | Pages | Extrait |
| -- | --------------- | --------- | ----- | ------- |
| M01 | supprimer | 1.0 | 21 pages | ... |

## Motifs conservés par défaut — aucune action requise

- M03 (0.48) : <extrait>
- M07 (0.62) : <extrait>
...

## Cas limites

- <avertissements, ou « aucun »>

## Appliquer la suggestion (éditable puis relancer)

<commande md-cleaner ... --suggestion ...>
```

## Règles de structure

- La section « Décisions requises » n'énumère **que** les motifs dont l'action suggérée est `supprimer` ; c'est la seule section exigeant une action de l'utilisateur (FR-004).
- La section « Motifs conservés par défaut » énumère **tous** les motifs `conserver` (sous le seuil ou non), chacun avec son id, sa fréquence et son extrait ; aucune action n'y est requise.
- Si l'une des deux sections est vide, elle affiche « aucun » plutôt que de disparaître (le lecteur sait alors qu'il n'a rien à arbitrer / rien d'autre détecté).
- Les sections « Cas limites » et « Appliquer la suggestion » sont inchangées par rapport à la feature 001.
- `suggestion.json` contient toujours tous les motifs des deux sections — le rapport n'est qu'une vue ; l'édition fine (bascule d'un motif conserver vers supprimer) passe toujours par la suggestion, rappelée en fin de rapport.

## Critère de lisibilité (SC-006 de la spec)

Un utilisateur parcourt le rapport d'un document riche (~25 motifs dont ≤ 5 à décider) et identifie les décisions requises en moins de 5 minutes — vérifié au quickstart.
