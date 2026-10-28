# Data Model: Nettoyage des destinations de liens sans chevrons

**Feature**: 009-nettoyage-liens-sans-chevrons | **Date**: 2026-10-27 |
**Source**: [spec.md](./spec.md), [research.md](./research.md) (D1-D5)

Aucune nouvelle entité persistée : la feature étend la transformation
textuelle à l'écriture introduite par la feature 004 et étendue par la
005. Elle touche la même entité existante, élargit l'entité éphémère
textuelle et introduit une entité éphémère de protection.

## Entités impactées

### Bloc (existant, `md_cleaner.nettoyage.Bloc`)

| Champ | Impact |
| ----- | ------ |
| `id` | inchangé — généré avant l'écriture |
| `page`, `debut`, `fin` | inchangés — lus tels quels par la cartographie |
| `texte` | transformé à l'écriture seulement : les destinations sans chevrons sont retirées en plus des chevrons ; hors ces sous-chaînes, identique octet par octet (D5) |

Invariant (hérité de 004/005, non modifié) : la transformation du
`texte` n'a lieu que dans les writers de `nettoye.md` et
`nettoye-pagine.md` ; le `Bloc` renvoyé par `nettoyer()` n'est pas muté
en amont, donc `suggestion.json`, les extraits et `cartographie.json`
restent identiques.

### Destination de lien sans chevrons (éphémère, textuelle — nouvelle)

- **Définition** : sous-chaîne `(...)` qui suit le crochet fermant `]`
  du libellé — parenthèses comprises, destination sans espaces et ne
  commençant pas par `<` (D3), titre éventuel de la forme
  `](url "titre")` emporté avec la destination, guillemets compris
  (arbitrage 005 reconduit, FR-007), destination vide `(#)` couverte.
- **Cycle de vie** : détectée et retirée en une passe à l'écriture, après
  la passe chevrons (D4) ; rien n'est persisté, rien n'est loggé.
- **Règles de validation** :
  - tout schéma couvert : ancre, chemin relatif avec ou sans slash
    initial, URL absolue — aucun décodage, aucune réécriture (FR-001) ;
  - exclusion explicite des destinations commençant par `<` : les formes
    chevrons restent la propriété de la règle 004/005 (D1, D3) ;
  - occurrences en nombre quelconque par ligne ;
  - limite héritée de 005 : un titre à guillemet interne échappé arrête
    le match avant la parenthèse fermante — la destination reste en
    place, sans corruption.

### Image inline (éphémère, protégée — nouvelle)

- **Définition** : construct `![alt](destination)` rencontré sur une
  ligne conservée, alt sans crochet fermant (limite D2).
- **Cycle de vie** : masquée par placeholder sentinelle avant les passes
  de destinations, restaurée à l'identique après (D2, D4) ; aucune
  destination d'image n'est retirée (FR-003).
- **Règles de validation** :
  - image simple (`![](/images/FIV11a.png)`) : ligne inchangée octet par
    octet ;
  - image imbriquée dans un lien (`[![FIPECO](/images/logo.jpg)](/)`) :
    seule la destination externe du lien est retirée ; l'image et son
    alt sont restaurés intacts (résidu `[![FIPECO](img)]` documenté,
    D7) ;
  - sentinelles sans crochet fermant suivi de parenthèse : les deux
    passes de destinations sont aveugles aux placeholders.

### Titre de lien sans chevrons (éphémère, textuelle — retirée)

- **Définition** : titre de la forme `](url "titre")` suivant une
  destination sans chevrons.
- **Cycle de vie** : emporté avec la destination, espace et guillemets
  compris (FR-007) ; 0 occurrence dans le corpus de calibration, règle
  défensive reconduite de 005.
