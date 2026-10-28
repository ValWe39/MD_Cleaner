# Bug Verification: Balises résiduelles corpus Le Grand Continent

- **Slug**: nettoyage-balises2
- **Tested**: 2026-10-27
- **Assessment**: ./assessment.md
- **Fix**: ./fix.md
- **Result**: verified

## Summary

Le symptôme d'origine ne se reproduit plus : rejeu de la version corrigée
sur les deux fichiers du corpus — 0 lien footnote résiduel (16+8 lignes
avant), 0 destination à espaces, 0 autolink (quick fix arbitré le
2026-10-27) ; les seules URLs restantes sont des destinations d'images
épargnées (15) et 1 URL nue (garde-fou 005). Aucune régression : la
neutralité des corpus historiques et les baselines épinglées FIPECO
tiennent.

## Checks Performed

- **Reproduction (post-fix)** — `md-cleaner` sur les 2 fichiers du
  corpus, sorties temporaires → **pass** : 0 `easy-footnote`, 0
  `<https`, https 55 → 16 (uniquement images épargnées + 1 URL nue).
- **Tests du fix** — `pytest` sur les fichiers de tests liens →
  **pass** : 10 nouveaux tests (5 bug, 4 autolink, 1 corpus).
- **Suite de régression** — `python -m pytest tests/ -q` → **pass** :
  205 passés (baseline 195), neutralité Exemple_1..3 et baselines
  FIPECO épinglées tenues.
- **Lint** — `ruff check` et `ruff format --check` → **pass**.
- **Markdown** — `markdownlint-cli2` sur les fichiers modifiés →
  **pass**.

## Output Excerpts

```text
python -m pytest tests/ -q → 205 passed in 17.54s

Reproduction post-fix (corpus réel, sorties temporaires) :
  legrandcontinent.eu--nettoye.md   easy-footnote=0 autolinks=0 https=9 images=8
  legrandcontinent.eu--nettoye-1.md easy-footnote=0 autolinks=0 https=7 images=7
  (les https restants = destinations d'images épargnées FR-003 + 1 URL nue)
```

## Residual Risks

- Les 2 autolinks retirés deviennent des références vides (`13.`) —
  débris assumés cohérents avec l'option A (libellés résiduels), à traiter
  par la détection de motifs si besoin.
- La branche destination-à-espaces peut théoriquement matcher un texte
  ordinaire `](...)` malformé adjacent à un crochet fermant ; forme non
  observée dans les corpus connus, limite épinglée par tests.
- La limite chevron 004/005 (titre à guillemets échappés) est
  volontairement préservée — l'exclusion `(?<!\(` de la passe autolink
  est testée contre la corruption.

## Recommendation

Clôturer le bug — vérifié de bout en bout : reproduction exercée sur le
corpus réel désigné par l'utilisateur, symptôme disparu, suite complète
au vert sans régression, quick fix autolink inclus et épinglé par tests.
Prochaine étape : versionner le correctif (`/commit-push-ameliore` sur
016-balises-liens).
