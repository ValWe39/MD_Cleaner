# Research: Nettoyage des destinations de liens à l'écriture

**Feature**: 004-nettoyage-liens-html | **Date**: 2026-10-02 | **Source**: [spec.md](./spec.md), mesures de l'assessment (`nettoyage-liens-html/research.md`), lecture du code (`md_cleaner/nettoyage.py`, `md_cleaner/cli.py`, `md_cleaner/cartographie.py`).

## D1 — La règle de retrait : une regex bornée à `](</...>)`

- **Décision** : retirer les correspondances exactes de `](<` suivi d'une destination sans `>` (jusqu'au premier `>`, exclusif) suivi de `>)` — c'est-à-dire la sous-chaîne `](</...>)` complète, parenthèses et chevrons compris, en un nombre quelconque d'occurrences par ligne.
- **Rationale** : la forme est strictement textuelle et close ; le premier `>` referme la destination (aucun chevron imbriqué observé dans les corpus) ; les destinations absolues `](https://...)` et les liens à destination nue `](chemin)` ne commencent pas par `](</` et ne matchent pas ; les marqueurs de page `<!-- page: N -->` n'ont pas de préfixe `](<` et ne matchent pas (D5).
- **Alternatives considérées** : (a) décoder les % avant matching — rejeté : FR-006 impose le retrait sans décodage ; (b) un mini-parseur Markdown — rejeté : la recherche de la feature 001 a écarté tout parseur CommonMark au profit du déterminisme textuel ; (c) retirer aussi les crochets du libellé — rejeté : clarification du 2026-10-02 (FR-001), seule la destination est retirée.

## D2 — Point d'application : le texte des blocs, à l'écriture

- **Décision** : appliquer la règle dans `md_cleaner/nettoyage.py`, sur les lignes de chaque `Bloc` conservé, au moment d'écrire `nettoye.md` et `nettoye-pagine.md` — en aval de `nettoyer()`, qui ne change pas.
- **Rationale** : `ecrire_nettoye` et `ecrire_nettoye_pagine` sont les deux seuls endroits où le texte conservé devient livrable ; `cartographie.json` n'utilise que `id`/`page`/`debut`/`fin` (jamais `texte`), donc la cartographie reste identique (FR-005) ; les extraits de la suggestion sont construits en amont sur les lignes d'origine (feature 003), donc le dry-run garde les liens de thème — les décisions des features 002/003 restent valides.
- **Alternatives considérées** : (a) nettoyer avant segmentation/détection — rejeté par l'assessment (option B du concept : rend les motifs indiscernables et change les ids M01…) ; (b) nettoyer dans `_compacter` — rejeté : mélange de responsabilités (plies de lignes vides vs retrait de destinations).

## D3 — Fonction pure, testable isolément

- **Décision** : une fonction pure du module `nettoyage.py` (entrée : liste de lignes ; sortie : liste de lignes transformées), sans état ni effet de bord ; les deux writers l'appliquent au texte des blocs.
- **Rationale** : testable en unitaire sans fichier ni CLI ; déterminisme trivial ; cohérente avec le style des fonctions existantes du module (`nettoyer`, `_compacter`).
- **Alternatives considérées** : post-processer le fichier écrit (relecture + réécriture) — rejeté : double E/O pour aucun gain, et casse l'invariant « une seule écriture déterministe ».

## D4 — Option CLI : `--conserver-liens` (store_true, nettoyage actif par défaut)

- **Décision** : option booléenne sans argument de `construire_analyseur` ; absente par défaut → nettoyage actif (FR-002) ; présente → passe désactivée, sorties identiques à avant la feature (FR-003, SC-004). Le paramètre est propagé jusqu'aux writers via un argument explicite — pas d'état global.
- **Rationale** : même pattern que `--pagine` ; la sémantique « je conserve les liens » décrit le résultat obtenu (clarification du 2026-10-02) ; codes retour 0-3 et combinaisons d'options inchangés.
- **Alternatives considérées** : (a) `--nettoyer-liens/--no-nettoyer-liens` (paire symétrique) — rejetée : verbeuse, aucun usage du drapeau d'activation explicite ; (b) une valeur `--liens=conserver|nettoyer` — rejetée : hors style CLI existant (booléens et valeurs bornées seulement).

## D5 — Préservation des marqueurs de page : garantie structurelle + test

- **Décision** : les marqueurs `<!-- page: N -->` insérés par `ecrire_nettoye_pagine` ne passent pas par la règle : ils sont générés après la passe, par construction du morceau `---\n\n<!-- page: N -->\n\n`, et la regex ne matche de toute façon pas cette forme (pas de `](<`). Un test dédié verrouille les deux niveaux.
- **Rationale** : l'hypothèse de la spec (« ne matchent jamais la forme visée ») devient un invariant testé ; la cohérence marqueurs/cartographie (contrat feature 001) reste assurée par construction.
- **Alternatives considérées** : liste d'exclusions de marqueurs dans la règle — rejetée : complexité injustifiée, l'ordre d'application suffit.

## D6 — Observabilité : silence (pas de compte affiché)

- **Décision** : la passe n'émet ni message, ni avertissement, ni compteur ; les impressions du run (`Sortie : ...`) restent inchangées.
- **Rationale** : la sortie attendue est le texte nettoyé lui-même ; un compteur ajouterait du bruit sans décision associable (rien à arbitrer) ; YAGNI (principe IV). Le compte de destinations retirées reste vérifiable par diff entre runs avec et sans `--conserver-liens`.
- **Alternatives considérées** : avertissement stderr « N destinations retirées » — rejetée : les avertissements existants (FR-016 de la feature 001) signalent des situations exigeant une décision ; ce n'est pas le cas ici.

## Récapitulatif

| Décision | Choix | Référence spec |
| -------- | ----- | -------------- |
| D1 | Regex bornée `](</...>)`, premier `>` referme | FR-001, FR-006 |
| D2 | Passe sur le texte des blocs à l'écriture | FR-002, FR-004, FR-005 |
| D3 | Fonction pure dans `nettoyage.py` | FR-007 |
| D4 | `--conserver-liens` store_true, défaut = nettoyage actif | FR-002, FR-003 |
| D5 | Marqueurs générés après la passe + test dédié | FR-004 |
| D6 | Aucun message ni compteur | — |

Aucune inconnue NON RÉSOLUE : tous les NEEDS CLARIFICATION de la spec ont été levés (FR-001 : clarification du 2026-10-02 ; drapeau : clarification du 2026-10-02).
