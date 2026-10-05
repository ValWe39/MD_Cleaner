# Quickstart: valider le dossier de sorties partagé

**Feature**: 008-dossier-sorties-lot | **Date**: 2026-10-05

Guide de validation exécutable de bout en bout. Contrat complet :
[contracts/dossier-de-lot.md](./contracts/dossier-de-lot.md) ; entités :
[data-model.md](./data-model.md). La suite automatisée de référence reste
`pytest` (voir plan).

## Prérequis

```powershell
cd MD_Cleaner
.venv\Scripts\Activate.ps1
pip install -e .
md-cleaner --help
```

Les scénarios utilisent `--sortie` vers un dossier de validation jetable
(remplacez `$env:TEMP\md-qs-008`) ; notez les numéros de run créés.

## Scénario 1 — Lot de plusieurs : un seul dossier (SC-001)

```powershell
md-cleaner .\Examples\Exemple_1\2.Input\consolidated.md .\Examples\Exemple_2\2.Input\consolidated.md .\Examples\Exemple_3\2.Input\retry-failed-records.md --sortie $env:TEMP\md-qs-008.sc1
echo $LASTEXITCODE
```

**Attendu** : exactement **un** dossier (ex. `001`) contenant
`consolidated-nettoye.md`, `consolidated-nettoye-1.md` et
`retry-failed-records-nettoye.md` — jamais 3 dossiers.

## Scénario 2 — Sorties secondaires attribuables (SC-004)

```powershell
md-cleaner .\Examples\Exemple_1\2.Input\consolidated.md .\Examples\Exemple_3\2.Input\retry-failed-records.md --pagine --sortie $env:TEMP\md-qs-008.sc2
```

**Attendu** : un dossier contenant, par document, la paire préfixée
`consolidated-nettoye-pagine.md` + `consolidated-cartographie.json` et
`retry-failed-records-nettoye-pagine.md` +
`retry-failed-records-cartographie.json`, en plus des deux sorties
nettoyées.

## Scénario 3 — Mono-document inchangé (SC-003)

```powershell
md-cleaner .\Examples\Exemple_3\2.Input\retry-failed-records.md --pagine --sortie $env:TEMP\md-qs-008.sc3
```

**Attendu** : `001/retry-failed-records-nettoye.md`,
`001/nettoye-pagine.md`, `001/cartographie.json` — noms courts,
structure et numérotation d'aujourd'hui. La suite pytest existante
(non migrée sur les cas mono) fait foi au passage.

## Scénario 4 — `--nom-titre` neutralisée en lot (FR-005)

```powershell
md-cleaner .\Examples\Exemple_1\2.Input\consolidated.md .\Examples\Exemple_3\2.Input\retry-failed-records.md --nom-titre 30 --sortie $env:TEMP\md-qs-008.sc4
echo $LASTEXITCODE
```

**Attendu** : avertissement `AVERTISSEMENT : --nom-titre ignorée en lot :
applicable à un seul document` sur stderr ; dossier numéroté (`001`) ;
code 0. En mono-document, `--nom-titre 30` nomme toujours le dossier
d'après le titre (à vérifier avec la même invocation à un seul document).

## Scénario 5 — Numérotation par invocation (SC-005)

```powershell
md-cleaner .\Examples\Exemple_1\2.Input\consolidated.md .\Examples\Exemple_2\2.Input\consolidated.md --sortie $env:TEMP\md-qs-008.sc5
md-cleaner .\Examples\Exemple_3\2.Input\retry-failed-records.md --sortie $env:TEMP\md-qs-008.sc5
```

**Attendu** : le lot occupe `001` (une seule consommation), l'invocation
suivante prend `002` — plus jamais un dossier par document.

## Scénario 6 — Échec partiel puis échec total (FR-006, FR-007)

```powershell
md-cleaner .\Examples\Exemple_1\2.Input\consolidated.md inexistant.md .\Examples\Exemple_3\2.Input\retry-failed-records.md --sortie $env:TEMP\md-qs-008.sc6
echo $LASTEXITCODE
md-cleaner absent-a.md absent-b.md absent-c.md --sortie $env:TEMP\md-qs-008.sc6b
echo $LASTEXITCODE
```

**Attendu** : premier cas — un dossier contenant les deux sorties valides
(l'échec est signalé, code 1, aucun marqueur) ; second cas — un dossier
numéroté **vide** en place, code 1.

## Scénario 7 — Collision de stems, aucun écrasement (SC-002)

Couvert nominalement par le scénario 1 (les deux `consolidated.md`
produisent `consolidated-nettoye.md` et `consolidated-nettoye-1.md`) ;
avec `--pagine` sur les mêmes deux documents, vérifier la paire
`consolidated-nettoye-pagine.md` / `consolidated-nettoye-pagine-1.md`
et `consolidated-cartographie.json` / `consolidated-cartographie-1.json`.

## Scénario 8 — Suite automatisée

```powershell
pytest
pre-commit run --all-files
```

**Attendu** : suite au vert intégrale, sans relâchement (tests migrés de
`tests/integration/test_lot.py` inclus).
