# Implementation Plan: Nettoyage des destinations de liens sans chevrons

**Branch**: `009-nettoyage-liens-sans-chevrons` | **Date**: 2026-10-27 |
**Spec**: [spec.md](./spec.md)

**Input**: Feature specification from
`/specs/009-nettoyage-liens-sans-chevrons/spec.md`, issue du handoff de
l'assessment `nettoyage-balises` (decision.md, verdict go, option A
confirmée par l'utilisateur le 2026-10-27 ; calibrage exhaustif du corpus
`Examples/Nettoyage-balises/` : 199 occurrences sans chevrons, 9 images,
0 URL nue, 0 bloc de code), clarification du périmètre en session
2026-10-27 (sorties livrables seules).

## Summary

Étendre la passe de nettoyage à l'écriture (features 004/005) aux
destinations de liens inline **sans chevrons** — `](/chemin)`, `](#ancre)`,
`](https://...)`, relatifs sans slash — quel que soit le schéma, sans cas
particulier : seuls les libellés survivent, le titre éventuel est emporté
avec la destination (arbitrage 005 reconduit). Les images `![...]` sont
épargnées intégralement (destination comprise) via une protection
éphémère ; dans un lien contenant une image, seule la destination externe
est retirée (résidu de crochets documenté, option A). Aucune modification
CLI : le drapeau `--conserver-liens` existant désactive l'ensemble
(comportement antérieur octet par octet). La règle chevron 004/005 reste
strictement inchangée. Aucune modification de la détection, des extraits,
de la suggestion ni de la cartographie.

## Technical Context

**Language/Version**: Python 3.12 (existant — déploiement identique aux
features 001-008).

**Primary Dependencies**: aucune en runtime (stdlib `re`) ; dev : pytest,
ruff (en place). Surface modifiée : `md_cleaner/nettoyage.py` (passe
d'écriture : protection images + nouvelle règle sans chevrons) ;
`md_cleaner/cli.py` (aide du drapeau `--conserver-liens` à mettre à jour,
contrat inchangé). Révision du contrat de la feature 005
(`specs/005-nettoyage-liens-absolus/contracts/nettoyage-liens-absolus.md`).

**Storage**: inchangé — fichiers locaux dans le dossier de sortie du run.

**Testing**: `pytest` existant ; extension de
`tests/unit/test_nettoyage_liens.py` (formes sans chevrons : ancres,
relatifs, absolus, sans slash, destination vide, titres, multi-liens,
images épargnées, logo imbriqué, idempotence, URLs nues intactes) et de
`tests/integration/test_nettoyage_liens.py` (0 destination sur le corpus
de calibration, neutralité octet par octet sur Exemple_1..3,
`--conserver-liens`, marqueurs `--pagine`). Corpus de test :
`Examples/Nettoyage-balises/` (local, gitignoré — présent sur la machine
de l'utilisateur) + documents construits pour les cas non observés
(titres sans chevrons, images dans le corps).

**Target Platform**: CLI locale multi-OS, hors-ligne (inchangé).

**Project Type**: cli (modification d'un outil existant).

**Performance Goals**: inchangé ; passes regex linéaires par ligne
conservée — O(lignes), négligeable (961 lignes pour le corpus de
calibration, 9 489 pour le corpus le plus riche).

**Constraints**: déterminisme octet par octet ; aucune modification du
texte hors destinations et titres (FR-002) ; comportement chevron
identique octet par octet (FR-005) ; images épargnées (FR-003) ; borné aux
sorties livrables (clarification 2026-10-27).

**Scale/Scope**: corpus de validation : les 5 fichiers du corpus de
calibration + les trois corpus historiques (neutralité) + documents
construits pour les cas non observés.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe / exigence | Statut | Justification |
| ------------------- | ------ | ------------- |
| I. Isolation des secrets | PASS | Aucun secret manipulé. |
| II. Local-first | PASS | Aucun appel réseau ; traitement local. |
| III. Open-source, sans trackers | PASS | Aucune dépendance ; stdlib `re`. |
| IV. Simplicité (YAGNI) | PASS | Une règle de plus, aucun drapeau. |
| Config Validation | PASS | Aucune option CLI ajoutée. |
| Path Isolation | PASS | Chemins inchangés. |
| No Cloud / No Trackers | PASS | Aucun trafic. |
| Data Retention | PASS | Sorties du run uniquement. |

**Re-check post-Phase 1** : aucun changement — les décisions D1-D7 de
[research.md](./research.md) n'introduisent ni dépendance, ni réseau, ni
secret ; la protection d'images est une transformation textuelle
éphémère en mémoire (D2), la règle sans chevrons est bornée à la
sous-chaîne suivant un crochet fermant et exclut les formes chevrons
(D3), et les garanties (marqueurs, URLs nues, neutralité chevron) sont
testées au quickstart (D5, D6).

## Project Structure

### Documentation (this feature)

```text
specs/009-nettoyage-liens-sans-chevrons/
├── plan.md              # Ce fichier
├── research.md          # Phase 0 : décisions D1-D7
├── data-model.md        # Phase 1 : entités impactées
├── quickstart.md        # Phase 1 : validation de bout en bout
├── contracts/
│   └── nettoyage-liens-sans-chevrons.md  # Phase 1 : règle étendue
└── tasks.md             # Phase 2 (/speckit-tasks — non créé ici)
```

### Source Code (repository root)

```text
md_cleaner/
├── nettoyage.py         # Passe d'écriture : protection images + règle
└── cli.py               # Aide du drapeau --conserver-liens uniquement

tests/
├── unit/
│   └── test_nettoyage_liens.py       # Formes sans chevrons, images
└── integration/
    └── test_nettoyage_liens.py       # Corpus de calibration, neutralité
```

**Structure Decision**: structure unique existante (paquet `md_cleaner`
et `tests/{unit,integration}`), inchangée — la feature étend un module
existant sans créer de nouveau fichier source.
