# Contrat : nettoyage des destinations de liens sans chevrons

**Feature**: 009-nettoyage-liens-sans-chevrons | **Date**: 2026-10-27 |
**Source**: [spec.md](./spec.md), [research.md](./research.md) (D1-D7),
révision de la règle du contrat
[005/contracts/nettoyage-liens-absolus.md](../../005-nettoyage-liens-absolus/contracts/nettoyage-liens-absolus.md)

## Règle de transformation (FR-001, FR-002, FR-007)

Appliquée à l'écriture des sorties livrables seules (`nettoye.md`,
`nettoye-pagine.md` — clarification du 2026-10-27), sur chaque ligne
conservée, après la passe chevrons 004/005 inchangée :

```text
cible   : la sous-chaîne (...) qui suit le crochet fermant ] du
          libellé, destination ne commençant pas par <, avec son
          titre éventuel
          ( ](dest) = ] + ( + destination sans espace ni < + ) )
          ( ](dest "titre") = forme précédente + espace + titre )
retrait : la sous-chaîne complète, parenthèses, espace et guillemets
          du titre compris
restes  : le libellé [texte] avec ses crochets, et le reste de la
          ligne, identiques octet par octet
```

Exemples contractuels (tirés du corpus de calibration) :

```text
entrée : [Lire →](/commentaire/Le%20patrimoine%20des%20...)
sortie : [Lire →]

entrée : [*crédit d'impôt*](Les-crédits-dimp...)
sortie : *crédit d'impôt*

entrée : [une note](https://www.imf.org/en/Publications/...)
sortie : une note

entrée : ... en comptabilité nationale[[1]](#_ftn1).
sortie : ... en comptabilité nationale[[1]].

entrée : [Revenir en haut de page](#haut)
sortie : [Revenir en haut de page]

entrée : [Ressources](#)
sortie : [Ressources]
```

## Garde-fous (FR-003, FR-005, FR-006)

| Forme | Traitement |
| ----- | ---------- |
| `![](/images/FIV11a.png)` (image) | inchangée octet par octet |
| `[![FIPECO](/images/logo.jpg)](/)` | devient `[![FIPECO](/images/logo.jpg)]` |
| `](<...>)` (chevrons — 004/005) | inchangé : règle 004/005 seule |
| URL nue hors syntaxe de lien | intacte (aucun crochet fermant) |
| Bloc de code | intact (aucun crochet fermant suivi de `(`) |
| Marqueur `<!-- page: N -->` | intact, généré après la passe |
| Ligne sans lien | inchangée octet par octet |

Résidus tolérés (option A confirmée le 2026-10-27, D7) : crochets
résiduels autour d'une image dans un lien, libellés de navigation seuls,
`[[1]]` de notes de bas de page, libellés vides `[]` — candidats à la
passe détection de motifs, hors périmètre.

## Contrat CLI (inchangé)

- `--conserver-liens` : désactive l'ensemble des passes de destinations
  (chevrons et sans chevrons) ; sorties identiques octet par octet au
  comportement antérieur à la feature (FR-004).
- Aucun nouveau drapeau, aucune nouvelle option ; codes retour et
  messages inchangés ; seuls les fichiers `nettoye.md` et
  `nettoye-pagine.md` sont affectés (FR-001) ; l'extrait lisible du
  dry-run, `suggestion.json`, `rapport-dry-run.md` et
  `cartographie.json` ne sont pas touchés (D5).

## Bornes de la règle (D2, D3)

- Alt d'image contenant un crochet fermant : non couvert par la
  protection ; aucune occurrence dans les corpus connus.
- Titre avec guillemet interne échappé : arrête le match avant la
  parenthèse fermante — destination laissée en place, sans corruption
  (limite héritée de 005) ; 0 occurrence dans le corpus de calibration.
- Idempotence (FR-008) : un second passage ne modifie pas la sortie.
