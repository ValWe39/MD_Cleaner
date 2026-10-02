# Quickstart: Nettoyage des destinations de liens

**Feature**: 004-nettoyage-liens-html | **Date**: 2026-10-02 | **Sources**: [spec.md](./spec.md), [contracts/nettoyage-liens.md](./contracts/nettoyage-liens.md)

Guide de validation de bout en bout. Prérequis : installation faite (`md-cleaner --help` fonctionne, cf. README), corpus `Examples/` présents.

## Scénario 1 — Sortie sans destinations (US1, SC-001)

```powershell
md-cleaner .\Examples\Exemple_2\2.Input\consolidated.md
```

Attendu : dans le `output/<run>/nettoye.md` produit, aucune ligne ne contient `](</...>)` ; les libellés `[texte]` restent en place avec leurs crochets ; nombre et ordre des lignes inchangés par rapport à un run `--conserver-liens` (cf. scénario 2).

Vérification :

```powershell
Select-String -Path .\output\<run>\nettoye.md -Pattern '\]\(</'       # aucun résultat attendu
Select-String -Path .\output\<run>\nettoye.md -Pattern '\[Famille'    # libellés présents
```

## Scénario 2 — Réversibilité avec `--conserver-liens` (US2, SC-004)

```powershell
md-cleaner .\Examples\Exemple_2\2.Input\consolidated.md --conserver-liens
```

Attendu : le `nettoye.md` contient les destinations intactes ; octet par octet, il est identique à une sortie produite par la version d'avant la feature (les deux runs du scénario 1 et 2 ne diffèrent que par les destinations retirées).

Vérification : comparer les deux runs — les lignes contenant `](</` dans ce run correspondent aux mêmes lignes sans `](</...>` dans le run du scénario 1.

## Scénario 3 — Sortie paginée et marqueurs préservés (US3, SC-002)

```powershell
md-cleaner .\Examples\Exemple_2\2.Input\consolidated.md --pagine
```

Attendu : `nettoye-pagine.md` ne contient plus de destination dans le contenu des pages ; chaque marqueur `<!-- page: N -->` est présent et identique (un par page conservée) ; `cartographie.json` est identique à celui d'un run `--conserver-liens --pagine` sur la même entrée.

Vérification :

```powershell
Select-String -Path .\output\<run>\nettoye-pagine.md -Pattern '<!-- page:'   # tous les marqueurs présents
Select-String -Path .\output\<run>\nettoye-pagine.md -Pattern '\]\(</'     # aucun résultat attendu
```

## Scénario 4 — Neutralité sur corpus sans liens (SC-003)

```powershell
md-cleaner .\Examples\Exemple_1\2.Input\consolidated.md
```

Attendu : seules les lignes porteuses de `](</...>)` diffèrent de la version d'avant la feature (Exemple_1 en contient peu) ; les lignes sans lien sont identiques octet par octet ; aucun changement de détection, des ids de motifs ou de la suggestion (`--dry-run` produit un `suggestion.json` identique avec et sans la feature).

## Scénario 5 — Dry-run non affecté (FR-005)

```powershell
md-cleaner .\Examples\Exemple_2\2.Input\consolidated.md --dry-run
```

Attendu : `rapport-dry-run.md` et `suggestion.json` identiques octet par octet à ceux produits avant la feature — les extraits conservent les liens de thème, condition des décisions supprimer/conserver des features 002/003.

## Suite de tests

```powershell
pytest
```

Attendu : suite au vert sans relâchement des seuils, y compris les tests migrés (`test_nettoyage_simple.py`) et les nouveaux tests de la passe (SC-005).
