# Quickstart: Nettoyage des destinations de liens absolues

**Feature**: 005-nettoyage-liens-absolus | **Date**: 2026-10-05 | **Sources**: [spec.md](./spec.md), [contracts/nettoyage-liens-absolus.md](./contracts/nettoyage-liens-absolus.md)

Guide de validation de bout en bout. Prérequis : installation faite (`md-cleaner --help` fonctionne, cf. README), corpus `Examples/` présents (dont `Exemple_3/2.Input/retry-failed-records.md`).

## Scénario 1 — Sortie sans destinations sur le corpus Mistral (US1, SC-001)

```powershell
md-cleaner .\Examples\Exemple_3\2.Input\retry-failed-records.md
```

Attendu : dans le `output/<run>/nettoye.md` produit, aucune ligne ne contient `](<` ; les libellés (`[Reach out]`, `[Try Studio ]`, `[Discord↗]`…) restent en place avec leurs crochets ; nombre et ordre des lignes inchangés par rapport à un run `--conserver-liens` (cf. scénario 3).

Vérification :

```powershell
Select-String -Path .\output\<run>\nettoye.md -Pattern '\]\(<'      # aucun résultat attendu
Select-String -Path .\output\<run>\nettoye.md -Pattern '\[Reach out\]'  # libellé présent
```

## Scénario 2 — Garde-fou : URLs légitimes conservées (US2, SC-005)

Construire un petit document de test (multi-pages avec séparateur `---`) contenant un bloc de code avec une URL nue (`client = Mistral(...)` et `https://api.mistral.ai`) et une phrase avec une URL nue hors syntaxe de lien, puis :

```powershell
md-cleaner .\chemin\document-garde-fou.md
```

Attendu : le bloc de code et la phrase sont identiques octet par octet à l'entrée, URLs nues comprises ; aucune URL du corps du texte n'a disparu.

Vérification :

```powershell
Select-String -Path .\output\<run>\nettoye.md -Pattern 'api\.mistral\.ai'  # URL nue intacte
```

## Scénario 3 — Réversibilité avec `--conserver-liens` (US4, SC-004)

```powershell
md-cleaner .\Examples\Exemple_3\2.Input\retry-failed-records.md --conserver-liens
```

Attendu : le `nettoye.md` contient les destinations absolues intactes (`](<https://mistral.ai/about>`, etc.) ; octet par octet, il est identique à une sortie produite par la version d'avant la feature (les runs des scénarios 1 et 3 ne diffèrent que par les destinations retirées).

Vérification :

```powershell
Select-String -Path .\output\<run>\nettoye.md -Pattern '\]\(<https'  # 6 lignes attendues
```

## Scénario 4 — Sortie paginée et marqueurs préservés (US4, FR-003)

```powershell
md-cleaner .\Examples\Exemple_3\2.Input\retry-failed-records.md --pagine
```

Attendu : `nettoye-pagine.md` ne contient plus de destination dans le contenu des pages ; chaque marqueur `<!-- page: N -->` est présent et identique ; `cartographie.json` est identique à celui d'un run `--conserver-liens --pagine` sur la même entrée.

Vérification :

```powershell
Select-String -Path .\output\<run>\nettoye-pagine.md -Pattern '<!-- page:'   # tous les marqueurs présents
Select-String -Path .\output\<run>\nettoye-pagine.md -Pattern '\]\(<'         # aucun résultat attendu
```

## Scénario 5 — Neutralité sur les corpus 1 et 2 (US4, SC-003)

```powershell
md-cleaner .\Examples\Exemple_1\2.Input\consolidated.md
md-cleaner .\Examples\Exemple_2\2.Input\consolidated.md
```

Attendu : sorties identiques octet par octet aux runs équivalents de la version 004 (Exemple_1 : aucune destination absolue ; Exemple_2 : toutes dans des motifs supprimés) ; les libellés de liens relatifs restent sans destination, comme en 004.

## Scénario 6 — Dry-run non affecté (FR-005)

```powershell
md-cleaner .\Examples\Exemple_3\2.Input\retry-failed-records.md --dry-run
```

Attendu : `rapport-dry-run.md` et `suggestion.json` identiques octet par octet à ceux produits par la version 004 sur la même entrée — les extraits conservent les liens absolus intacts, condition des décisions supprimer/conserver des features 002/003.

## Suite de tests

```powershell
pytest
```

Attendu : suite au vert sans relâchement des seuils, y compris les tests 004 inchangés (règle en sur-ensemble) et les nouveaux tests (schémas absolus, titres, garde-fou URLs nues, neutralité Exemple_1/2, Exemple_3 → 0 destination) — SC-007.
