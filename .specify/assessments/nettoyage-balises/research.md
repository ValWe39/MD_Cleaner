# Idea Research: Nettoyage par défaut des liens sans chevrons

- **Slug**: nettoyage-balises
- **Created**: 2026-10-27
- **Evidence confidence (overall)**: high

## Users & Demand

- Demande explicite et formulée de l'unique utilisateur (propriétaire) le
  2026-10-27 : « Je veux que tous les (...) et autres balises et liens soient
  nettoyés », avec exigence de conservation du texte — le signal passe
  d'observation (investigation lecture seule) à exigence formulée.
  — [source: intake.md, citation d'origine] (confidence: high)
- Comportement observé : les sorties du corpus FIPECO exigent une retouche
  manuelle — 199 destinations sans chevrons subsistent sur 5 fichiers
  (961 lignes), la ligne 6 de `fipeco.fr-000033-nettoye.md` ayant été
  signalée. — [source: investigation 2026-10-27 + calibrage corpus]
  (confidence: high)
- Troisième demande de nettoyage de liens en un mois (004 chevrons, 005
  absolus, maintenant sans chevrons) : motif persistant — chaque nouveau
  corpus de conversion révèle une nouvelle forme résiduelle.
  — [source: specs/004, specs/005, intake.md] (confidence: high)

## Prior Art

- Features 004/005 (implémentées, fusionnées) : mécanisme établi identique —
  passe regex à l'écriture (`nettoyer_destinations`,
  `md_cleaner/nettoyage.py:12`), activée par défaut, réversible par
  `--conserver-liens` (`md_cleaner/cli.py:90`). L'extension hériterait de ce
  socle sans nouveau drapeau. — [source: md_cleaner/nettoyage.py, cli.py]
  (confidence: high)
- La spec 005 avait délibérément exclu les formes sans chevrons (option A,
  2026-10-05) sur l'hypothèse qu'« aucune forme sans chevrons n'est observée
  dans les corpus » et que « la conversion HTML → Markdown produit
  systématiquement des destinations entre chevrons ». Le corpus FIPECO
  réfute cette hypothèse : la borne était propre au convertisseur d'alors,
  pas universelle. — [source: specs/005-nettoyage-liens-absolus/spec.md
  (clarifications, recherche)] (confidence: high)
- Filet de tests existant : plus de 20 tests unitaires et d'intégration sur
  la passe actuelle (`tests/unit/test_nettoyage_liens.py`,
  `tests/integration/test_nettoyage_liens.py`) — couverture de
  non-régression à étendre. — [source: tests/] (confidence: high)
- Externe : le retrait de destinations Markdown en conservant le libellé est
  un problème classique (sed, pandoc, bibliothèques regex) — aucune
  recherche web menée ici, non nécessaire à l'arbitrage interne.
  — ASSUMPTION (confidence: medium)

## Market & Context

- Alternative actuelle : retouche manuelle (grep/sed) sur chaque sortie —
  coût répétitif à chaque run FIPECO, risque d'oubli et d'incohérence entre
  fichiers. — [source: constat utilisateur, investigation] (confidence:
  high)
- Coût de l'inaction : chaque fichier FIPECO porte ~40 liens sans chevrons
  (34 à 47 mesurés), dont un pied de page et une navigation identiques sur
  les 5 fichiers. — [source: calibrage corpus] (confidence: high)

## Data & Constraints

- Calibrage exhaustif du corpus désigné `Examples/Nettoyage-balises/`
  (5 fichiers, 199 liens sans chevrons) :
  - ancres `(#main-content)`, `(#haut)`, `(#)` : 15 occurrences ;
  - relatifs-racine `(/...)` : 132 occurrences (nav, menus, footer) ;
  - absolus `https://...` : 48 occurrences (partage + références du corps) ;
  - relatifs sans slash `(Les-crédits-dimp%C3%B4t)` : 4 occurrences ;
  - formes à titre `](url "titre")` : 0 occurrence — mais la règle peut
    reconduire l'arbitrage 005 sans coût.
  — [source: calibrage regex sur corpus, script de comptage] (confidence:
  high)
- Concentration : environ 64 % des occurrences (125/199) vivent dans des
  blocs de navigation/pied de page répétés à l'identique sur les 5 fichiers
  (libellés « Accueil », « Encyclopédie », « Faire un don »...) ; environ 35
  % (70/199) sont des liens de référence dans le corps du texte, dont le
  libellé porte le contenu d'intérêt (« rapport sur le budget »,
  « *crédit d'impôt* », « tome II des voies et moyens »).
  — [source: inventaire des libellés, calibrage] (confidence: high)
- Garde-fous du corpus : 0 URL nue hors syntaxe de lien, 0 bloc de code —
  les contrats 005 sur ces cas ne seraient pas sollicités sur ce corpus mais
  restent à préserver. — [source: calibrage] (confidence: high)
- Images présentes : 9 occurrences — 5 logos imbriqués dans un lien
  (`[![FIPECO](/images/logo_legacy.jpg)](/)`) et 4 figures à alt vide
  (`![](/images/FIV11a.png)`). — [source: calibrage] (confidence: high)
- Corpus historiques non concernés par la nouvelle forme : Exemple_1 (532
  destinations chevrons), Exemple_2 (4314), Exemple_3 (68) — 0 forme sans
  chevrons. La régression potentielle porte sur la préservation exacte du
  comportement chevron. — [source: grep Examples/Exemple_1..3]
  (confidence: high)
- Constitution du projet : une seule règle déterministe, stdlib, local —
  une extension regex unifiée y conforme. — [source: constitution]
  (confidence: high)

## Evidence Against the Idea

- Perte d'information par défaut : les destinations absolues des liens de
  référence du corps du texte (48 occurrences) sont des sources
  vérifiables ; les retirer par défaut rend les références non traçables
  (réversibilité uniquement via `--conserver-liens`).
  — [source: calibrage] (confidence: high)
- Les images échappent à la règle « libellé conservé » : retirer la
  destination de `![](/images/FIV11a.png)` (alt vide) laisserait un débris
  `![]`, et le logo imbriqué `[![FIPECO](img)](/)` risque une corruption
  par une regex naïve (2 niveaux imbriqués, 9 occurrences au total).
  — [source: calibrage] (confidence: high)
- Le correctif ne résout pas le bruit de navigation : après retrait des
  destinations, les libellés de nav (« Faire un don », « QCM »...) restent
  (125 occurrences) — le livrable exigera toujours une passe détection de
  motifs pour être « directement exploitable ».
  — [source: calibrage] (confidence: high)
- Risque de régression : la règle étendue touche une regex qui traite
  aujourd'hui 5 000+ destinations chevrons sur les corpus historiques ;
  toute réécriture doit préserver le comportement à l'octet.
  — [source: grep Examples/] (confidence: medium)

## Gaps & Open Questions

- [NEEDS CLARIFICATION: Figures à alt vide `![](/images/...png)` — épargner
  intégralement les images, ou retirer le construct entier (laissant le
  texte « Sources : ... » collé) ?]
- [NEEDS CLARIFICATION: Logo imbriqué `[![FIPECO](img)](/)` — ordre de
  traitement externe/interne, 5 occurrences identiques en pied de page ?]
- [NEEDS CLARIFICATION: Libellés devenus vides après retrait (`[]` ou
  libellés d'un caractère) — nettoyage résiduel ?]
- [NEEDS CLARIFICATION: Faut-il traiter dans le même mouvement les blocs de
  navigation répétés (125 occurrences, périmètre détection de motifs), ou
  strictement borner à la passe liens ?]
- [NEEDS CLARIFICATION: La règle unifiée inclut-elle les relatifs sans
  slash et les ancres sans cas particulier, conformément à l'option A de
  la spec 005 ?]

## Sources

- Corpus de calibrage : `Examples/Nettoyage-balises/fipeco.fr-00003{3..7}`
  -nettoye.md (host: n/a, fichiers locaux — aucune page fetchée, policy:
  lecture seule du dépôt)
- `md_cleaner/nettoyage.py:12` et `md_cleaner/cli.py:90` (host: n/a,
  lecture du dépôt)
- `specs/005-nettoyage-liens-absolus/spec.md` (host: n/a, lecture du dépôt)
- `tests/unit/test_nettoyage_liens.py` (host: n/a, lecture du dépôt)
- `.specify/assessments/nettoyage-balises/intake.md` (host: n/a)
