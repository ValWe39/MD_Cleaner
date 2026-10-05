# Implementation Plan: Nettoyage des destinations de liens absolues à l'écriture de la sortie

**Branch**: `005-nettoyage-liens-absolus` | **Date**: 2026-10-05 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/005-nettoyage-liens-absolus/spec.md`, issue du handoff de l'assessment `nettoyage-liens-url` (mesures grep sur `output/009/nettoye.md` et `Examples/Exemple_3` incluses), clarifications arbitrées en session du 2026-10-05.

## Summary

Étendre la passe de nettoyage à l'écriture (feature 004) à toute destination de lien inline entre chevrons `](<...>)`, quel que soit son schéma (relatif déjà couvert, `http`, `https`, `mailto`, `tel`, `ftp`…), et retirer le titre avec la destination pour les formes `(<url> "titre")` : seuls les libellés survivent. La règle devient unifiée et plus simple que celle de 004 (suppression de l'exigence `/` en tête de destination) ; aucune modification CLI (le drapeau `--conserver-liens` existant couvre déjà tout) ; aucune modification de la détection, des extraits, de la suggestion ni de la cartographie. Les URLs nues du corps du texte (hors syntaxe de lien) sont conservées par construction — la règle ne matche que la sous-chaîne de destination suivant un crochet fermant.

## Technical Context

**Language/Version**: Python 3.12 (existant — déploiement identique aux features 001-004).

**Primary Dependencies**: aucune en runtime (stdlib) ; dev : pytest, ruff (en place). Surface modifiée : `md_cleaner/nettoyage.py` uniquement (regex de `nettoyer_destinations` + docstring) ; `md_cleaner/cli.py` inchangé (le drapeau `--conserver-liens` existe et se propage déjà) ; révision du contrat de la feature 004 (`specs/004-nettoyage-liens-html/contracts/nettoyage-liens.md`).

**Storage**: inchangé — fichiers locaux dans `output/<run>/`.

**Testing**: `pytest` existant ; extension de `tests/unit/test_nettoyage_liens.py` (schémas http/https/mailto/tel, titre, titre avec guillemets échappés non couverts, libellé vide absolu, URLs nues intactes, plusieurs liens par ligne) et de `tests/integration/test_nettoyage_liens.py` (0 destination sur Exemple_3, neutralité octet par octet sur Exemple_1/Exemple_2, `--conserver-liens`, marqueurs `--pagine`, dry-run non affecté). Nouveau corpus de test : `Examples/Exemple_3/2.Input/retry-failed-records.md`.

**Target Platform**: CLI locale multi-OS, hors-ligne (inchangé).

**Project Type**: cli (modification d'un outil existant).

**Performance Goals**: inchangé ; une substitution regex par ligne conservée — O(lignes), négligeable (320 lignes pour Exemple_3, 9489 pour le corpus le plus riche).

**Constraints**: déterminisme octet par octet (FR-008) ; aucune modification du texte hors destinations et titres (FR-001, FR-002) ; ids de motifs et cartographie inchangés (FR-005) ; marqueurs `<!-- page: N -->` préservés (FR-003) ; URLs nues intactes (FR-007).

**Scale/Scope**: corpus de validation étendu à trois exemples (`Exemple_1`, `Exemple_2`, `Exemple_3`) + documents construits pour les cas non observés (titre, mailto, URLs nues en bloc de code).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe / exigence | Statut | Justification |
| ------------------- | ------ | ------------- |
| I. Isolation des secrets (NON NÉGOCIABLE) | PASS | Aucun secret manipulé ; inchangé. |
| II. Local-first & confidentialité (NON NÉGOCIABLE) | PASS | Aucun appel réseau ; traitement local uniquement. |
| III. Open-source & sans trackers | PASS | Aucune nouvelle dépendance ; stdlib `re` uniquement. |
| IV. Simplicité (YAGNI) | PASS | La règle unifiée `](<...>)` est plus simple que celle de 004 (l'exigence `/` disparaît) ; aucun nouveau drapeau, aucune nouvelle option ; demandé par l'utilisateur (clarification du 2026-10-05, option A). |
| Config Validation | PASS | Aucune option CLI modifiée ; codes retour inchangés. |
| Path Isolation | PASS | Chemins inchangés. |
| No Cloud / No Trackers / Network Surface | PASS | Aucun trafic. |
| Data Retention | PASS | Sorties uniquement dans `output/` (inchangé). |
| Compliance CI (Ruff, markdownlint) | PASS | Code sous `md_cleaner/` et `tests/` linté ; specs sous config MD013 locale. |

**Re-check post-Phase 1** : aucun changement — les décisions D1-D6 de [research.md](./research.md) n'introduisent ni dépendance, ni réseau, ni secret ; la règle est bornée à la sous-chaîne de destination suivant un crochet fermant (D1), le titre est couvert par la même regex (D2), et les garanties (marqueurs, URLs nues, neutralité) sont testées (D5, D6).

## Project Structure

### Documentation (this feature)

```text
specs/005-nettoyage-liens-absolus/
├── plan.md                      # Ce fichier
├── research.md                  # Phase 0 : décisions D1-D6
├── data-model.md                # Phase 1 : entités impactées
├── quickstart.md                # Phase 1 : validation de bout en bout
├── contracts/
│   └── nettoyage-liens-absolus.md  # Phase 1 : révision de la règle du contrat 004
└── tasks.md                     # Phase 2 (/speckit-tasks — pas encore créé)
```

### Source Code (repository root — fichiers modifiés, structure inchangée)

```text
md_cleaner/
└── nettoyage.py     # MODIFIÉ : regex unifiée de nettoyer_destinations
                     #   (toute destination ](<...>), titre optionnel inclus),
                     #   docstring mise à jour ; cli.py inchangé

tests/
├── unit/
│   └── test_nettoyage_liens.py       # ÉTENDU : schémas, titres, garde-fou
└── integration/
    ├── test_nettoyage_liens.py       # ÉTENDU : Exemple_3, neutralité, --conserver-liens
    └── test_nettoyage_simple.py      # VÉRIFIÉ : contenus attendus inchangés
                                       #   (Exemple_1/2 sans destination résiduelle)
```

**Structure Decision**: structure existante conservée ; la modification vit dans `md_cleaner/nettoyage.py` (lieu de la règle 004 et des writers), les tests s'étendent dans les fichiers dédiés à la passe de nettoyage des liens.
