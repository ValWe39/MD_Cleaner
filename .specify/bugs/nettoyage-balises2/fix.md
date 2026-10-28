# Bug Fix: Balises et liens résiduels sur le corpus Le Grand Continent

- **Slug**: nettoyage-balises2
- **Fixed**: 2026-10-27
- **Assessment**: ./assessment.md
- **Status**: applied

## Summary

La règle sans chevrons de la passe d'écriture couvre désormais les
titres à guillemets internes échappés (footnotes du corpus Le Grand
Continent, HTML brut et URLs embarqués emportés avec la destination),
les destinations contenant des espaces sans titre, et les autolinks
`<https://...>` (quick fix arbitré par l'utilisateur le 2026-10-27) ;
la règle chevron 004/005 est strictement inchangée (FR-005).

## Changes

- `md_cleaner/nettoyage.py` — modifié : regex étendue (2 branches),
  docstring mise à jour.
- `tests/unit/test_nettoyage_liens.py` — 5 tests ajoutés (bug).
- `tests/integration/test_nettoyage_liens.py` — détection alignée sur
  la règle étendue, baseline 000035 ajustée à 41, test corpus Le Grand
  Continent.
- `specs/009-nettoyage-liens-sans-chevrons/contracts/…sans-chevrons.md`
  — règle, exemples et bornes D2/D3 révisés.
- `specs/009-nettoyage-liens-sans-chevrons/research.md` — amendement D3.

## Diff Highlights (optional)

```python
RE_DESTINATION_SANS_CHEVRONS = re.compile(
    r'(?<=\])\((?!<)(?=[^)\s])'
    r'(?:[^)\s]*(?: "(?:[^"\\]|\\.)*")?|[^)"]*)\)'
)
```

- Branche 1 : destination sans espace, titre optionnel acceptant les
  guillemets échappés (`[^"\\]|\\.`) — couvre les footnotes
  `[1](#easy-footnote-... "<a href=\"https://...\">…</a> …")`.
- Branche 2 : destination avec espaces sans guillemet — couvre
  `[Histoire en images](https://.../Histoire en images)`.

## Tests Added or Updated

- `tests/unit/...::test_footnote_titre_echappe_emporte` — footnote réel
  du corpus : destination, titre et HTML emportés, libellé `[1]` gardé.
- `tests/unit/...::test_destination_avec_espaces_retiree` — destination
  non encodée avec espaces retirée.
- `tests/unit/...::test_destination_espaces_avec_titre_intacte` — limite
  documentée épinglée (`](a b "t")` inchangé, sans corruption).
- `tests/unit/...::test_footnote_et_image_sur_la_meme_ligne` — image
  épargnée pendant qu'une footnote est emportée (FR-003).
- `tests/unit/...::test_idempotence_formes_bug` — deux passes = une.
- `tests/integration/...::test_corpus_lgc_footnotes_et_espaces_nettoyes`
  — run sur les 2 fichiers `Examples/Nettoyage-balises2/` (skip si
  absent) : 0 `easy-footnote`, nav à espaces nettoyée, images intactes.
- Baseline FIPECO épinglée ajustée : 000035 passe de 40 à 41 — la
  branche espaces attrape une destination relative valide
  `(../pdf/0.77438100 1460639455.pdf)` du corpus FIPECO.

## Local Verification

- Commandes : `python -m pytest tests/ -q` → 201 passés (195 avant + 6) ;
  `ruff check` + `ruff format` → propres.
- Vérification manuelle sur le corpus réel `Examples/Nettoyage-balises2/` :
  `easy-footnote` 16+8 → **0** ligne résiduelle ; URLs https 55 → 18,
  dont 15 destinations d'images épargnées (FR-003), 1 URL nue (garde-fou
  005) et 2 autolinks `<https://...>` (voir Deviations) ; libellés
  `[1]`, `[Histoire en images]` conservés.

## Deviations from Assessment

Aucune sur les formes couvertes par l'assessment (footnotes à titre
échappé, destinations à espaces) : la remediation préférée a été
appliquée telle quelle, règle chevron intacte. La vérification sur
corpus réel avait révélé 2 autolinks CommonMark `<https://...>` hors
périmètre de l'assessment ; l'utilisateur a arbitré leur retrait en
quick fix le 2026-10-27 — implémenté comme une troisième passe
(`RE_AUTO_LIEN`, exclusion `(?<!\()` pour préserver la limite chevron,
après les passes de destinations, images toujours masquées), avec 4
tests unitaires dédiés et l'épingle d'intégration `<https` absent.

## Follow-ups

- Libellés de notes `[N]` résiduels : périmètre détection de motifs
  (hors scope, arbitrage 009 maintenu).
- Étendre la règle chevron aux titres échappés si un corpus futur
  l'exige (arbitrage 2026-10-27 : non, maintenu).
