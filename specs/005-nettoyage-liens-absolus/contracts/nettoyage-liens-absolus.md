# Contrat : nettoyage des destinations de liens absolues à l'écriture

**Feature**: 005-nettoyage-liens-absolus | **Date**: 2026-10-05 | **Source**: [spec.md](./spec.md), [research.md](./research.md) (D1, D2, D4), révision de la règle du contrat [004/contracts/nettoyage-liens.md](../../004-nettoyage-liens-html/contracts/nettoyage-liens.md)

## Règle de transformation (FR-001, FR-002, FR-006)

Appliquée à l'écriture de `nettoye.md` et `nettoye-pagine.md`, sur chaque ligne conservée :

```text
cible   : la sous-chaîne (<...>) qui suit le crochet fermant ] du libellé,
          avec son titre éventuel
          ( ](<...>) = ] + ( + < + destination sans > + > + ) )
          ( ](<...> "titre") = forme précédente + espace + titre entre guillemets )
retrait : la sous-chaîne complète, parenthèses, chevrons, espace et
          guillemets du titre compris
restes  : le libellé [texte] avec ses crochets, et le reste de la ligne,
          identiques octet par octet
```

Exemples contractuels :

```text
entrée : [Try Studio ](<https://console.mistral.ai?utm_source=docs&utm_medium=header_cta>)
sortie : [Try Studio ]

entrée : [Haut Conseil des finances publiques (HCFP)](<http://www.hcfp.fr/> "Haut Conseil des finances publiques \(HCFP\)\(nouvelle fenêtre\)")
sortie : [Haut Conseil des finances publiques (HCFP)]

entrée : [Contact](<mailto:contact@exemple.fr>)
sortie : [Contact]
```

Bornes de la règle :

| Forme | Traitement |
| ----- | ---------- |
| `](</...>)` (relatif — forme 004) | retirée : cas particulier de la règle générale, comportement 004 inchangé |
| `](<https://...>)`, `](<http://...>)` (absolus chevrons) | retirée, telle quelle, sans décodage ni réécriture |
| `](<mailto:...>)`, `](<tel:...>)`, `](<ftp://...>)` (autres schémas) | retirée : même règle, aucun cas particulier (clarification 2026-10-05, option A) |
| `](<url> "titre")` (avec titre) | destination **et** titre retirés ; seuls les libellés survivent |
| `[](</...>)` (libellé vide) | destination retirée, crochets vides conservés |
| plusieurs occurrences sur une même ligne | toutes retirées |
| `](https://...)` sans chevrons, `](chemin)` nu | hors périmètre : inchangées (clarification 2026-10-05) |
| URL nue dans le corps du texte ou dans un bloc de code | hors périmètre : intacte octet par octet (garde-fou, FR-007) |
| vraies balises HTML (`<div>`, `<!-- page: N -->`) | hors périmètre : inchangées |
| titre contenant un guillemet interne échappé (`\"`) | non matché : destination laissée en place, sans corruption (limite documentée, D2) |

## Option CLI (inchangée — héritée de la feature 004)

| Option | Argument | Défaut | Exigence | Description |
| ------ | -------- | ------ | -------- | ----------- |
| `--conserver-liens` | — | nettoyage actif | FR-004 | Désactive le retrait de **toutes** les destinations (relatives et absolues, titres compris) : `nettoye.md` et `nettoye-pagine.md` conservent les liens inline tels quels, identiques octet par octet à une sortie produite sans la feature |

- Aucune option ajoutée ni modifiée ; la sémantique du drapeau existant s'étend de fait aux destinations absolues (arbitrage decide 2026-10-05).
- `--dry-run` : aucun effet observable (aucune sortie nettoyée n'est écrite ; la suggestion et le rapport restent identiques, FR-005).

## Sorties concernées et non concernées (FR-003, FR-005)

| Artefact | Nettoyé ? |
| -------- | --------- |
| `nettoye.md` | oui |
| `nettoye-pagine.md` | oui (contenu des pages ; marqueurs `<!-- page: N -->` générés intacts) |
| `suggestion.json` (extraits) | non |
| `rapport-dry-run.md` (extraits) | non |
| `cartographie.json` | non (n'utilise jamais le texte des blocs) |

## Codes retour et messages

Inchangés (contrat CLI de la feature 001) : 0/1/2/3 ; aucun message, avertissement ni compteur émis par la passe.

## Garanties vérifiables

- Sur un run Exemple_3 : aucune ligne de `nettoye.md` ne contient `](<` (SC-001, baseline 6/299 au run 009).
- Sur Exemple_1 et Exemple_2 : sorties par défaut identiques octet par octet aux runs équivalents 004 (SC-003).
- Sur un document construit avec URLs nues (bloc de code, corps du texte) : URLs intactes octet par octet (SC-005).
- Avec `--conserver-liens` : toutes les sorties identiques octet par octet à avant la feature (SC-004).
- Deux runs identiques (mêmes entrée et options) : sorties identiques octet par octet (FR-008).
