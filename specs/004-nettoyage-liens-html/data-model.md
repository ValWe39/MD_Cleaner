# Data Model: Nettoyage des destinations de liens à l'écriture

**Feature**: 004-nettoyage-liens-html | **Date**: 2026-10-02 | **Source**: [spec.md](./spec.md), [research.md](./research.md) (D2, D3)

Aucune nouvelle entité persistée : la feature est une transformation textuelle à l'écriture. Elle touche une entité existante et introduit une entité éphémère purement textuelle.

## Entités impactées

### Bloc (existant, `md_cleaner.nettoyage.Bloc`)

| Champ | Impact |
| ----- | ------ |
| `id` | inchangé — généré avant l'écriture |
| `page`, `debut`, `fin` | inchangés — la cartographie les lit tels quels |
| `texte` | **transformé à l'écriture seulement** : chaque ligne voit ses sous-chaînes `](</...>)` retirées (D1) ; hors ces sous-chaînes, les lignes sont identiques octet par octet (FR-001) |

Invariant : la transformation du `texte` n'a lieu que dans les writers de `nettoye.md` et `nettoye-pagine.md` ; le `Bloc` renvoyé par `nettoyer()` n'est pas muté en amont, donc `suggestion.json`, les extraits et `cartographie.json` (qui n'utilisent jamais `texte`) restent identiques (FR-005).

### Destination de lien résiduelle (éphémère, textuelle)

- **Définition** : sous-chaîne `](</...>)` — `](<` + destination sans `>` + `>)` — terminant un lien inline Markdown issu d'une conversion HTML → Markdown (spec, Key Entities).
- **Cycle de vie** : détectée et retirée en une passe à l'écriture ; rien n'est persisté, rien n'est loggé (D6).
- **Règles de validation** (D1) :
  - la destination est délimitée par le premier `>` suivant `](<` (aucun chevron imbriqué) ;
  - les caractères encodés (`%5B`, `%3A`, `%20`) sont retirés tels quels, sans décodage (FR-006) ;
  - les destinations absolues `](https://...)`, les destinations nues `](chemin)` et les vraies balises HTML ne matchent pas — hors périmètre (edge cases de la spec) ;
  - occurrences en nombre quelconque par ligne (scénario 3 de la US1).

## Interface de la transformation

Fonction pure du module `nettoyage.py` (D3) : liste de lignes → liste de lignes, appliquée au texte des blocs par les deux writers, contrôlée par l'option `--conserver-liens` (D4). Propriétés garanties :

1. **Conservation** : nombre et ordre des lignes inchangés (SC-002) ; aucune ligne vide créée ni supprimée.
2. **Idempotence** : réappliquer la passe sur une sortie déjà nettoyée est un no-op (aucune `](</` restante).
3. **Réversibilité** : avec `--conserver-liens`, aucune transformation — sorties identiques octet par octet à celles d'avant la feature (SC-004).
4. **Neutralité** : sur un corpus sans `](</...>)`, la sortie est identique octet par octet à celle d'avant la feature (SC-003).

Les marqueurs de page `<!-- page: N -->` sont générés après la passe, par construction du morceau de `nettoye-pagine.md` (D5) : ils ne figurent jamais en entrée de la transformation.
