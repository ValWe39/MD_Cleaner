# Research: Nettoyage des destinations de liens absolues à l'écriture

**Feature**: 005-nettoyage-liens-absolus | **Date**: 2026-10-05 | **Source**: [spec.md](./spec.md), clarifications du 2026-10-05 (option A : toute destination entre chevrons ; formes sans chevrons hors périmètre ; seuls les libellés survivent), lecture du code (`md_cleaner/nettoyage.py`, `md_cleaner/cli.py`), mesures de l'assessment (`nettoyage-liens-url/research.md`), mesures complémentaires sur `Examples/Exemple_3`.

## D1 — La règle unifiée : toute destination `](<...>)`, sans distinction de schéma

- **Décision** : remplacer la regex 004 `(?<=\])\(</[^>]*>\)` par `(?<=\])\(<[^>]*>(?: "[^"]*")?\)` : toute sous-chaîne `](<` + destination sans `>` + `>)`, suivie optionnellement d'un espace et d'un titre entre guillemets, est retirée en un nombre quelconque d'occurrences par ligne. L'exigence `/` en tête de destination disparaît — la règle couvre relatifs, `http`, `https`, `mailto`, `tel`, `ftp` et tout schéma futur, conformément à l'arbitrage option A.
- **Rationale** : la forme reste strictement textuelle et close ; le premier `>` referme toujours la destination (aucun chevron imbriqué observé dans les trois corpus, y compris les 21 lignes à titre d'Exemple_2) ; une seule règle, aucun cas particulier par schéma ; les formes sans chevrons `](https://...)`, les destinations nues `](chemin)` et les marqueurs de page ne commencent pas par `](<` et ne matchent pas.
- **Alternatives considérées** : (a) conserver la regex 004 et en ajouter une seconde pour les absolus — rejeté : deux règles pour une même entité, cas limite du chevauchement, contredit l'arbitrage « une seule règle » ; (b) distinguer les schémas (`http|https|mailto|...`) dans la regex — rejeté : enumération à maintenir, aucun bénéfice (clarification 2026-10-05) ; (c) un mini-parseur Markdown — rejeté : la recherche de la feature 001 a écarté tout parseur au profit du déterminisme textuel.

## D2 — Titres : retirés avec la destination, guillemets compris

- **Décision** : la partie `(?: "[^"]*")?` de la regex emporte l'espace et le titre entre guillemets ; `[HCFP](<http://www.hcfp.fr/> "Haut Conseil ... \(nouvelle fenêtre\)")` devient `[HCFP]`. Parenthèses, chevrons et guillemets disparaissent ; seuls le libellé et le reste de la ligne restent.
- **Rationale** : arbitrage final de l'utilisateur au specify (2026-10-05) : seuls les libellés survivent ; l'option `?` garde la règle unique (les liens sans titre passent par la même regex) ; les échappements du titre (`\(nouvelle fenêtre\)`) sont emportés tels quels, sans décodage, cohérent avec FR-006.
- **Alternatives considérées** : (a) conserver le titre (arbitrage initial du decide) — révoqué au specify ; (b) retirer le titre dans une seconde passe — rejeté : deux substitutions pour une même entité parenthésée, risque de désynchronisation.
- **Limite documentée** : un titre contenant un guillemet interne échappé (`\"`) arrêterait `[^"]*` avant la fin du titre ; la parenthèse fermante ne serait alors pas matchée et la destination resterait en place (comportement conservateur, sans corruption). Aucune occurrence dans les corpus ; borne assumée.

## D3 — Point d'application : inchangé — la fonction pure existante

- **Décision** : la modification vit dans `nettoyer_destinations` (`md_cleaner/nettoyage.py`), seule détentrice de la règle ; les writers `ecrire_nettoye` et `ecrire_nettoye_pagine` l'appellent déjà au bon endroit (texte des blocs, en aval de la détection) et ne changent pas.
- **Rationale** : le point d'application a été validé par la feature 004 (D2/D3 de son research) : la cartographie n'utilise jamais `texte`, les extraits sont construits en amont, les décisions des features 002/003 restent valides ; seule la regex change, pas les invariants.
- **Alternatives considérées** : (a) nouvelle fonction `nettoyer_destinations_absolues` — rejeté : duplication de l'appel dans les writers pour un gain nul ; (b) post-processer le fichier écrit — rejeté : double E/O, contredit l'invariant « une seule écriture déterministe ».

## D4 — CLI : aucune modification — `--conserver-liens` couvre déjà tout

- **Décision** : le drapeau `--conserver-liens` existant (004, store_true, propagé aux writers via `conserver_liens`) désactive l'ensemble de la passe, relatives et absolues comprises ; `md_cleaner/cli.py` n'est pas touché ; codes retour et combinaisons d'options inchangés.
- **Rationale** : arbitrage du decide (2026-10-05, confirmé) : même drapeau, pas de granularité par schéma (hors périmètre de la spec) ; l'absence de modification CLI élimine toute régression de contrat.
- **Alternatives considérées** : (a) un second drapeau dédié aux absolus — rejeté par l'utilisateur au decide ; (b) une valeur `--liens=...` — rejetée : hors style CLI existant.

## D5 — Garde-fou : conservation des URLs nues par construction, verrouillée par tests

- **Décision** : la règle ne matche que la sous-chaîne qui suit un crochet fermant `]` (lookbehind `(?<=\])`) ; une URL nue dans le corps du texte ou dans un bloc de code n'a jamais ce préfixe et reste intacte. Tests dédiés : document construit contenant un bloc de code avec URL nue et une phrase avec URL nue (SC-005).
- **Rationale** : le garde-fou exigé au research (2026-10-05) est une propriété structurelle de la regex, pas une liste d'exclusions à maintenir ; le cas limite du lien absolu légitime en prose est retiré comme tout lien (spécifié en edge case, assumé) et couvert par le drapeau.
- **Alternatives considérées** : (a) exclure les blocs de code du nettoyage — rejeté : aucun besoin (les blocs de code ne contiennent pas la forme `](<...>)` de lien inline ; et un `](<...>)` présent dans un bloc de code est visuellement identique mais serait retiré — la spec ne fait pas cette distinction, aucune observation dans les corpus) ; (b) analyse de contexte prose/navigation — rejeté au decide (rabbit hole, hors périmètre).

## D6 — Neutralité : corpus 1/2 inchangés, marqueurs préservés — tests

- **Décision** : la nouvelle regex est un sur-ensemble de celle de 004 sur les seules formes `](<...>)` non couvertes (absolus, titres) ; or Exemple_1 ne contient aucune destination absolue (0) et les 21 destinations absolues d'Exemple_2 vivent dans des motifs supprimés — les sorties par défaut sur ces deux corpus sont identiques octet par octet aux runs 004 (SC-003, test de non-régression). Les marqueurs `<!-- page: N -->` restent générés après la passe et ne matchent pas la forme (pas de préfixe `](`).
- **Rationale** : la superset-ité garantit que les contenus attendus des tests existants (qui ne portent que des relatifs chevrons) restent valides ; les tests d'intégration 004 (identité `--conserver-liens`, marqueurs) restent vrais sans modification.
- **Alternatives considérées** : réécrire les tests de 004 — rejeté : aucun échec attendu, la vérification « suite au vert sans relâchement » suffit.

## Récapitulatif

| Décision | Choix | Référence spec |
| -------- | ----- | -------------- |
| D1 | Regex unifiée `](<...>)` + titre optionnel, sans distinction de schéma | FR-001, FR-006 |
| D2 | Titre retiré avec la destination ; limite guillemet interne documentée | FR-002 |
| D3 | Modification dans `nettoyer_destinations` seule ; writers inchangés | FR-003, FR-005 |
| D4 | CLI inchangée ; `--conserver-liens` couvre relatives + absolues | FR-004 |
| D5 | Garde-fou par construction (lookbehind `]`) + tests dédiés | FR-007 |
| D6 | Neutralité Exemple_1/2 et marqueurs verrouillés par tests | FR-003, FR-009, SC-003 |

Aucune inconnue NON RÉSOLUE : tous les arbitrages ont été levés en clarification (schéma : option A ; sans chevrons : hors périmètre ; titre : seuls les libellés survivent) et les mesures de prévalence sont documentées (6/299 au run 009, 6/320 en entrée Exemple_3, 21/9489 en entrée Exemple_2, 0 en Exemple_1).
