# Data Model: Nettoyage des destinations de liens absolues à l'écriture

**Feature**: 005-nettoyage-liens-absolus | **Date**: 2026-10-05 | **Source**: [spec.md](./spec.md), [research.md](./research.md) (D1, D2, D3)

Aucune nouvelle entité persistée : la feature étend la transformation textuelle à l'écriture introduite par la feature 004. Elle touche la même entité existante et élargit l'entité éphémère textuelle.

## Entités impactées

### Bloc (existant, `md_cleaner.nettoyage.Bloc`)

| Champ | Impact |
| ----- | ------ |
| `id` | inchangé — généré avant l'écriture |
| `page`, `debut`, `fin` | inchangés — la cartographie les lit tels quels |
| `texte` | **transformé à l'écriture seulement** : chaque ligne voit ses sous-chaînes `](<...>)` (destination, et titre le cas échéant) retirées (D1, D2) ; hors ces sous-chaînes, les lignes sont identiques octet par octet (FR-001, FR-002) |

Invariant (hérité de 004, non modifié) : la transformation du `texte` n'a lieu que dans les writers de `nettoye.md` et `nettoye-pagine.md` ; le `Bloc` renvoyé par `nettoyer()` n'est pas muté en amont, donc `suggestion.json`, les extraits et `cartographie.json` (qui n'utilisent jamais `texte`) restent identiques (FR-005).

### Destination de lien résiduelle (éphémère, textuelle — élargie)

- **Définition** : sous-chaîne `](<...>)` — `](<` + destination sans `>` + `>)`, optionnellement suivie d'un espace et d'un titre entre guillemets — terminant un lien inline Markdown issu d'une conversion HTML → Markdown (spec, Key Entities). La définition 004 (destination relative `](</...>)`) devient le cas particulier relatif de cette définition générale.
- **Cycle de vie** : détectée et retirée en une passe à l'écriture ; rien n'est persisté, rien n'est loggé (D6 de 004, inchangé).
- **Règles de validation** (D1, D2) :
  - tout schéma de destination est couvert : relatif, `http`, `https`, `mailto`, `tel`, `ftp`, tout autre (clarification 2026-10-05, option A) — aucun décodage, aucune réécriture (FR-006) ;
  - la destination est délimitée par le premier `>` suivant `](<` (aucun chevron imbriqué) ;
  - le titre éventuel — forme `](<...> "titre")` — est retiré avec la destination, guillemets compris ; seuls les libellés survivent (arbitrage specify 2026-10-05) ;
  - occurrences en nombre quelconque par ligne (scénario 3 de la US1) ;
  - **limite documentée** : un titre contenant un guillemet interne échappé (`\"`) arrête le match avant la parenthèse fermante — la destination reste en place, sans corruption (D2).

### Titre de lien (éphémère, textuelle — retirée)

- **Définition** : texte entre guillemets suivant la destination dans la parenthèse d'un lien inline (`(<url> "titre")`).
- **Cycle de vie** : détecté et retiré avec sa destination en une passe à l'écriture ; rien n'est persisté.
- **Règles** : jamais dissocié de sa destination (une seule entité de match, D2) ; les échappements (`\(`, `\)`) sont emportés tels quels.

## Interface de la transformation

Fonction pure existante `nettoyer_destinations` du module `nettoyage.py` (D3) : liste de lignes → liste de lignes, appliquée au texte des blocs par les deux writers, contrôlée par l'option `--conserver-liens` (D4 — inchangée). Propriétés garanties :

1. **Conservation** : nombre et ordre des lignes inchangés (SC-002) ; aucune ligne vide créée ni supprimée ; aucune ligne supprimée par la passe (FR-009).
2. **Idempotence** : réappliquer la passe sur une sortie déjà nettoyée est un no-op (aucune `](<` restante).
3. **Réversibilité** : avec `--conserver-liens`, aucune transformation — sorties identiques octet par octet à celles d'avant la feature (SC-004).
4. **Neutralité** : sur un corpus sans `](<...>)` dans les lignes conservées, la sortie est identique octet par octet à celle d'un run 004 (SC-003) ; les URLs nues du corps du texte et des blocs de code ne passent jamais par la règle (FR-007, D5).
5. **Garde de schéma** : les formes sans chevrons `](https://...)` et les destinations nues `](chemin)` ne matchent pas — hors périmètre (clarification 2026-10-05).

Les marqueurs de page `<!-- page: N -->` sont générés après la passe, par construction du morceau de `nettoye-pagine.md` (D5 de 004, inchangé) : ils ne figurent jamais en entrée de la transformation.
