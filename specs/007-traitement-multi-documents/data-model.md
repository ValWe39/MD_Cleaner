# Data Model: Traitement multi-documents en une invocation

**Feature**: 007-traitement-multi-documents | **Date**: 2026-10-05 | **Source**: [spec.md](./spec.md), [research.md](./research.md) (D1-D9)

Le modèle n'introduit aucune entité persistante nouvelle : les sorties restent celles d'aujourd'hui, un dossier de run par document. Les entités ci-dessous décrivent la seule couche nouvelle — la résolution de l'invocation en un lot de documents — et vivent le temps d'une invocation.

## Entités

### Entrée positionnelle

- **Représente** : un chemin tel que tapé par l'utilisateur sur la ligne de commande.
- **Champs** : `chemin: Path` (autant d'instances que d'arguments, ordre d'apparition préservé).
- **Validation** : aucune à ce stade ; un chemin invalide transite tel quel jusqu'au traitement (échec documentaire, code 1) — D2.

### Lot (invocation)

- **Représente** : la collection ordonnée de documents à traiter, résultat du développement des entrées positionnelles.
- **Champs** : `documents: list[Path]` (ordonnée, doublons conservés), `avertissements: list[str]` (messages d'entrées ignorées, ex. dossier sans `.md`).
- **Relations** : produit par `resoudre_lot(entrees)` depuis les entrées positionnelles (D2, D3).
- **Validation** : lot vide → erreur d'entrée, code 1, aucun traitement (FR-008).
- **Règles de dérivation** :
  - fichier `.md` existant → retenu tel quel ;
  - dossier existant → ses fichiers `.md` de premier niveau, triés par nom, non récursif ; les autres fichiers ignorés sans message (FR-002) ;
  - dossier sans aucun `.md` → ignoré avec message explicite (FR-008) ;
  - doublons : chaque occurrence est conservée, traitée dans l'ordre (D3).

### Résultat de document

- **Représente** : l'issue du traitement d'un document du lot.
- **Champs** : `succes: bool`, `code: int` (0 pour un document traité, 1 pour une erreur d'entrée), `raison: str | None`.
- **Relations** : un par document du lot ; les sorties produites par un document en succès sont conservées quoi qu'il arrive ensuite (FR-007, FR-010).
- **Validation** : en lot de plusieurs documents, un résultat ne peut être qu'un succès ou une erreur d'entrée — la suggestion est neutralisée (D5, D6) et l'échantillon est validé globalement avant la boucle (D4).

### Compteur d'échecs consécutifs

- **Représente** : l'état de la boucle de lot vis-à-vis du fail-fast.
- **Champs** : `valeur: int` (0 à 2 en exécution ; 3 déclenche l'arrêt immédiat).
- **Transitions d'état** : échec → +1 ; succès → 0 ; atteindre 3 → arrêt du lot, les documents restants ne sont pas traités, le code final reste 1 (D7).
- **Invariants** : le compteur porte sur les documents traités, indépendamment du nombre d'arguments d'origine ; aucune sortie déjà produite n'est annulée.

## Agrégation finale

- Code retour de l'invocation = 0 si et seulement si tous les documents du lot ont un résultat en succès ; 1 sinon (D7).
- Les codes 2 (artefact) et 3 (usage) restent émis par les validations globales existantes, avant la boucle de documents (D4).

## Diagramme de flux (textuel)

```text
arguments (n ≥ 1) --nargs="+"--> entrées positionnelles
entrées --resoudre_lot--> lot { documents, avertissements }
lot vide ?                --> erreur code 1
|lot| > 1 + dry-run/suggestion --> avertissements + neutralisation
echantillon fourni ?      --> validation globale (code 2 si invalide)
boucle sur documents      --> résultats + compteur consécutif
compteur == 3 ?           --> arrêt immédiat
fin de boucle             --> code 0 si tous succès, sinon 1
```
