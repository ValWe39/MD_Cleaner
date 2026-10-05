# Quickstart: valider le traitement multi-documents

**Feature**: 007-traitement-multi-documents | **Date**: 2026-10-05

Guide de validation exécutable de bout en bout. Le contrat complet est dans [contracts/multi-entrees.md](./contracts/multi-entrees.md) ; les entités dans [data-model.md](./data-model.md). La suite automatisée de référence reste `pytest` (voir plan).

## Prérequis

```powershell
cd MD_Cleaner
.venv\Scripts\Activate.ps1
pip install -e .
md-cleaner --help
```

Les scénarios créent des dossiers de run dans `output\` (numérotation séquentielle) ; notez le numéro de départ (`001`, `002`, ...) pour repérer les sorties produites.

## Scénario 1 — Lot de fichiers listés

```powershell
md-cleaner .\Examples\Exemple_1\2.Input\consolidated.md .\Examples\Exemple_2\2.Input\consolidated.md .\Examples\Exemple_3\2.Input\retry-failed-records.md
echo $LASTEXITCODE
```

**Attendu** : 3 dossiers de run consécutifs, chacun avec son `<stem>-nettoye.md` ; code retour 0 ; une ligne `Sortie : ...` par document.

## Scénario 2 — Parité lot / individuel (SC-002)

Traitez chaque document seul (invocations séparées), puis en lot (scénario 1), et comparez les contenus :

```powershell
md-cleaner .\Examples\Exemple_1\2.Input\consolidated.md
# ... idem pour les deux autres, puis :
fc /b <sortie-individuelle-consolidated>.md <sortie-lot-consolidated>.md
```

**Attendu** : `fc` ne rapporte aucune différence octet par octet pour chaque paire (options identiques des deux côtés).

## Scénario 3 — Dossier en entrée

```powershell
md-cleaner .\Examples\Exemple_1\1.Sample
echo $LASTEXITCODE
```

**Attendu** : les 5 fichiers `.md` de premier niveau sont traités, dans l'ordre alphabétique (`1.md` ... `5.md`) ; code 0.

## Scénario 4 — Dossier sans `.md` (ignoré avec message, puis lot vide)

```powershell
md-cleaner .\Examples\Exemple_1
echo $LASTEXITCODE
```

**Attendu** : `Examples\Exemple_1` ne contient que des sous-dossiers → entrée ignorée avec un message explicite, lot vide, code 1, aucun traitement. En invocation mixte (`md-cleaner un-doc.md .\Examples\Exemple_1`), le message apparaît et le document valide est traité (code 0).

## Scénario 5 — Options neutralisées en lot (SC-004)

```powershell
md-cleaner .\Examples\Exemple_1\2.Input\consolidated.md .\Examples\Exemple_2\2.Input\consolidated.md --dry-run
echo $LASTEXITCODE
```

**Attendu** : avertissement `AVERTISSEMENT : --dry-run ignorée en lot : applicable à un seul document` sur stderr ; aucune sortie de dry-run ; 2 sorties nettoyées ; code 0. Même forme pour `--suggestion`.

## Scénario 6 — Échec isolé puis code 1 (FR-007)

```powershell
md-cleaner .\Examples\Exemple_1\2.Input\consolidated.md absent.md .\Examples\Exemple_3\2.Input\retry-failed-records.md
echo $LASTEXITCODE
```

**Attendu** : `absent.md` signalé (`ERREUR : ...`) ; les deux documents valides traités avec leurs sorties conservées ; code 1.

## Scénario 7 — Fail-fast au 3e échec consécutif (FR-007)

```powershell
md-cleaner absent1.md absent2.md absent3.md .\Examples\Exemple_1\2.Input\consolidated.md
echo $LASTEXITCODE
```

**Attendu** : trois messages d'erreur consécutifs puis arrêt — `consolidated.md` n'est pas traité, aucune sortie pour lui ; code 1.

## Scénario 8 — Rétrocompatibilité mono-document (SC-005)

```powershell
md-cleaner .\Examples\Exemple_3\2.Input\retry-failed-records.md
md-cleaner .\Examples\Exemple_1\2.Input\consolidated.md --dry-run
```

**Attendu** : comportements strictement identiques à aujourd'hui (nettoyage simple ; rapport + suggestion sans sortie nettoyée). La suite pytest existante, non modifiée sur ces cas, fait foi.
