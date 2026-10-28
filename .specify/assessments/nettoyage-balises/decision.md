# Decision: Étendre le nettoyage aux destinations sans chevrons

- **Slug**: nettoyage-balises
- **Decided**: 2026-10-27
- **Verdict**: go
- **Artifacts reviewed**: intake.md | research.md | problem.md | concept.md

## Scorecard

| Critère | Note | Justification |
| ----------- | -------- | --------------- |
| Validité du problème | strong | Mesuré : 199 occurrences, retouche manuelle |
| Force des preuves | strong | Calibrage exhaustif du corpus, mesures directes |
| Valeur vs inaction | strong | ~40 retouches par fichier, promesse rompue |
| Faisabilité / appétit | strong | Option A small, socle 004/005 éprouvé |
| Alignement stratégique | strong | Règle unique, déterministe, stdlib |
| Posture de risque | adequate | Régression chevrons testable, résidus assumés |

## Verdict & Rationale

Go. Le problème est réel, mesuré et récurrent (troisième forme de débris de
liens en un mois) ; les preuves sont directes et exhaustives (calibrage
regex du corpus désigné, inventaire des formes, zéro URL nue et zéro bloc
de code menaçant les garde-fous) ; l'option A tient la métrique centrale
(199 → 0 destination résiduelle) dans un budget small en héritant du
mécanisme déjà éprouvé par les features 004/005. La posture de risque reste
adequate plutôt que strong : la réécriture de la règle touche une regex qui
traite 5 314 destinations chevrons sur les corpus historiques (garantie
octet par octet exigée dans les métriques), et l'épargne des images laisse
des résidus de syntaxe assumés (`[![FIPECO](img)]`, `[[1]]`), explicitement
reportés au périmètre détection de motifs. L'utilisateur a confirmé l'option
A le 2026-10-27 après comparaison A/B sur exemples réels du corpus.

## If go — Handoff to `/speckit-specify`

- **Problem**: les livrables FIPECO conservent 199 destinations de liens
  sans chevrons collées au texte utile, exigeant une retouche manuelle.
- **Chosen approach**: Option A — étendre la passe d'écriture 004/005 à
  toute destination sans chevrons, sans cas particulier (ancres,
  relatifs-racine, relatifs sans slash, absolus), libellés conservés,
  images `![...]` épargnées intégralement, réversibilité par
  `--conserver-liens` inchangée.
- **In scope**: la règle étendue et son application aux sorties
  `nettoye.md` et `nettoye-pagine.md` ; la mise à jour des tests (nouvelles
  formes + non-régression chevron octet par octet) ; la documentation
  (README, contrats CLI).
- **Out of scope**: blocs de navigation répétés (détection de motifs) ;
  images et figures (épargnées, débris tolérés et documentés) ; décodage
  d'URL ; URLs nues et blocs de code (contrats 005 reconduits) ;
  modification des libellés.
- **Success metrics**: 0 destination sans chevrons sur les 5 fichiers
  FIPECO rejoués (baseline 199) ; libellés et texte inchangés octet par
  octet hors destinations ; sorties des corpus historiques inchangées ;
  tests au vert sans relâchement.
- **Carried-forward open questions**:
  - Formes à titre `](url "titre")` : 0 occurrence dans le corpus —
    reconduire l'arbitrage 005 (titre emporté avec la destination) par
    précaution.
  - Résidus acceptés à documenter dans la spec : logo imbriqué réduit à
    `[![FIPECO](img)]`, notes de bas de page `[[1]]`, libellés de nav
    seuls — candidats à une future passe détection de motifs.
  - Hypothèse à valider par tests : comportement chevron identique octet
    par octet sur Exemple_1..3.
