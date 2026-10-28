# Quickstart: Nettoyage des destinations de liens sans chevrons

**Feature**: 009-nettoyage-liens-sans-chevrons | **Date**: 2026-10-27 |
**Source**: [spec.md](./spec.md),
[contrat](./contracts/nettoyage-liens-sans-chevrons.md)

Guide de validation de bout en bout : prouve sur le corpus de calibration
que la feature tient ses métriques de succès (SC-001 à SC-005) sans
regression sur les corpus historiques.

## Prérequis

- Environnement Python 3.12+ avec le paquet installé (`pip install -e .`)
  depuis la racine du dépôt.
- Corpus de calibration présent localement :
  `Examples/Nettoyage-balises/` (5 fichiers, gitignoré).
- Corpus historiques : `Examples/Exemple_1` à `Exemple_3`.
- Sorties de référence produites avant la feature (pour SC-003) —
  sinon, les générer au commit précédent et les archiver hors du
  dossier de sortie.

## Scénario 1 — Sortie sans destinations sans chevrons (SC-001, SC-002)

```bash
md-cleaner Examples/Nettoyage-balises/fipeco.fr-000033-nettoye.md
```

Attendu :

- une sortie `fipeco.fr-000033-nettoye-nettoye.md` est écrite à côté de
  l'entrée (dérivation du nom par la feature 006) ;
- avertissements attendus sans impact : « aucune frontière de pages
  fiable : document traité comme section unique » et « document trop
  court » — les lignes sont toutes conservées, seule la passe de liens
  s'applique ;
- aucun `](/`, `](#`, `](https://`, `](http://`, `](Les-` ne subsiste
  dans la sortie (baseline : 43 occurrences pour ce fichier) ;
- les libellés sont présents et inchangés : `[Lire →]`,
  `*crédit d'impôt*`, `[Revenir en haut de page]` ;
- les images sont intactes : `![](/images/FIV11a.png)` inchangé,
  logo réduit à `[![FIPECO](/images/logo_legacy.jpg)]`.

Vérification rapide (grep ne doit rien retourner) :

```bash
grep -nE '\]\([^)<]' <sortie> || echo "0 destination sans chevrons"
```

À rejouer sur les 5 fichiers du corpus (199 occurrences au total).

## Scénario 2 — Réversibilité par --conserver-liens (FR-004)

```bash
md-cleaner Examples/Nettoyage-balises/fipeco.fr-000033-nettoye.md \
  --conserver-liens
```

Attendu : la sortie `fipeco.fr-000033-nettoye-nettoye.md` contient les
destinations sans chevrons intactes, identiques octet par octet à la
sortie produite sans la feature (comparaison `diff` avec la sortie
archivée).

## Scénario 3 — Neutralité sur les corpus historiques (SC-003, FR-005)

```bash
md-cleaner Examples/Exemple_3
```

Attendu : sorties identiques octet par octet aux sorties de référence
(0 forme sans chevrons dans les corpus historiques ; comportement
chevron 004/005 inchangé). Idem sur les documents sans liens inline :
sortie inchangée.

## Scénario 4 — Sortie paginée (FR-001)

```bash
md-cleaner Examples/Nettoyage-balises/fipeco.fr-000033-nettoye.md --pagine
```

Attendu : `nettoye-pagine.md` nettoyé des deux formes de destinations ;
chaque marqueur `<!-- page: N -->` présent à l'identique.

## Scénario 5 — Suite de tests (SC-005)

```bash
pytest tests/unit/test_nettoyage_liens.py \
  tests/integration/test_nettoyage_liens.py
```

Attendu : tous les tests au vert, y compris les nouveaux cas (ancres,
relatifs sans slash, destination vide, titres sans chevrons, images
épargnées, logo imbriqué, idempotence, URLs nues intactes,
`--conserver-liens`).

## En cas d'échec

- Une destination sans chevrons subsiste : comparer avec les formes du
  [contrat](./contracts/nettoyage-liens-sans-chevrons.md) — si la
  destination commence par `<`, elle relève de la règle 004/005 ;
  sinon, échec réel (SC-001).
- Une image a perdu sa destination : échec FR-003 — vérifier la
  protection (D2 de [research.md](./research.md)).
- Un diff apparaît sur Exemple_1..3 : échec FR-005 — vérifier que la
  règle chevron est inchangée (D1).
