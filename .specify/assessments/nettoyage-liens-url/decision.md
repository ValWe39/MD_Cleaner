# Decision: Retirer les destinations de liens absolues des sorties nettoyées

- **Slug**: nettoyage-liens-url
- **Decided**: 2026-10-05
- **Verdict**: go
- **Artifacts reviewed**: intake.md (addendum) | research.md (mise à jour) |
  problem.md | concept.md

## Scorecard

- **Problem validity** (strong) : Problème réel et mesuré sur artefacts : 6
  lignes / 299 du run 009 portent une destination absolue ; le corpus concerné
  est désormais un exemple de référence du projet (Exemple_3, 6/320 en entrée)
  et l'exigence est formulée explicitement par l'utilisateur (problem.md,
  research.md)
- **Evidence strength** (strong) : Mesure sur les trois corpus (grep entrées et
  sorties), lecture du code (regex 004 exigeant `</`), lecture des artefacts 004
  (borne = garde-fou anti-glissement, pas un jugement de fond), contre-preuve
  Exemple_2 (0 résiduel car liens dans motifs supprimés). Seule zone soft : un
  seul utilisateur porteur — non décisive, le problème est observé sur les
  artefacts et l'utilisateur est le décideur
- **Value vs. inaction** (strong) : L'inaction maintient une retouche manuelle
  répétitive sur chaque run type Exemple_3 (~2 % des lignes, chaînes `utm_*`
  longues et fragiles), contredisant le positionnement « directement exploitable
  » du livrable déjà retenu comme critère en 004
- **Feasibility / appetite** (strong) : Option A crédible en appetite small :
  même point d'application que la passe 004 déjà éprouvée, une règle
  supplémentaire, tests sur les trois corpus ; les deux hypothèses ouvertes du
  concept viennent d'être tranchées par l'utilisateur (titre conservé, même
  drapeau `--conserver-liens`)
- **Strategic fit** (strong) : Conforme à la constitution (local, déterministe,
  stdlib, sorties dans `output/`) ; cohérente avec les précédents 001-004 : une
  règle déterministe par passe ; ne touche ni la détection, ni les artefacts du
  dry-run
- **Risk posture** (adequate) : Risques identifiés : (1) retrait par défaut
  d'URLs valides et cliquables — mitigé par le drapeau `--conserver-liens`
  couvrant tout ; (2) lien inline dans une prose explicative indistinguable d'un
  débris de nav — manque assumé de l'option A, couvert par le drapeau, gardé
  hors périmètre ; (3) garde-fou URLs légitimes — tenu par construction pour les
  URLs nues et blocs de code (la cible est la syntaxe de destination de lien
  uniquement) ; validation à construire par tests, aucun corpus réel ne l'exerce
  aujourd'hui

## Verdict & Rationale

**Go.** Aucun critère sous adequate ; les critères make-or-break sont tenus par
de la mesure, pas de l'enthousiasme : le problème est quantifié sur le run 009
et sur l'entrée Exemple_3 (6 lignes dans chaque cas), le corpus est
institutionnalisé comme exemple de référence, et l'exigence est explicitement
formulée par l'utilisateur — le signal de demande est passé d'observation à
exigence. L'option A recommandée tient la métrique principale (0 résiduel sur
Exemple_3) dans un appétit small au point d'application déjà éprouvé par 004,
sans toucher à la détection. Les deux hypothèses qui demandaient validation
viennent d'être tranchées par l'utilisateur : le titre `(<url> "titre")` est
conservé en sortie, et le comportement est intégré au drapeau
`--conserver-liens` existant. Le risque résiduel principal — un lien absolu
légitime inséré dans une prose explicative est retiré comme tout autre — est
assumé et réversible par drapeau ; le traitement de fond (non-détection de la
nav Mistral) est explicitement hors périmètre et peut faire l'objet d'un
assessment distinct sans perdre la valeur de cette feature.

## If go — Handoff to `/speckit-specify`

- **Problem**: les sorties nettoyées conservent des destinations de liens
  absolues `](<https://...>)` collées au texte utile des lignes qui survivent à
  la détection, dégradant le livrable et exigeant une retouche manuelle (6/299
  lignes au run 009 sur Exemple_3).
- **Chosen approach**: Option A du concept.md — extension de la passe d'écriture
  existante (feature 004) aux destinations absolues entre chevrons, activée par
  défaut, désactivable par le même drapeau `--conserver-liens` ; s'applique à
  `nettoye.md` et `nettoye-pagine.md`, en aval de la détection, sans toucher aux
  artefacts du dry-run.
- **In scope**: la règle de retrait des destinations absolues (schémas à lister
  en spécification, minimum `https` et `http`) ; le sort des titres des formes
  `(<url> "titre")` (révisé au specify le 2026-10-05 : seuls les libellés
  survivent, titre retiré avec la destination) ; le maintien du garde-fou par
  construction pour les URLs nues et blocs de code ; les tests sur les trois
  corpus (Exemple_3 : 6 lignes à nettoyer ; Exemple_1/2 : non-régression octet
  par octet) ; la documentation.
- **Out of scope**: tout changement de la détection/segmentation/seuil ;
  décodage ou réparation d'URLs ; réécriture des libellés ; extraits du dry-run,
  `suggestion.json`, `rapport-dry-run.md`, `cartographie.json` ; granularité par
  schéma ; distinction prose/nav par analyse de contexte.
- **Success metrics**: (1) 0 ligne de sortie avec destination absolue sur
  Exemple_3 (baseline 6/299) ; (2) reste du texte inchangé octet par octet hors
  destinations, titres conservés ; (3) sorties inchangées sur
  Exemple_1/Exemple_2 ; (4) URLs nues et blocs de code intacts (tests
  construits) ; (5) tests au vert sans relâchement ; (6) déterminisme conservé.
- **Carried-forward open questions**:
  - [NEEDS CLARIFICATION: liste exacte des schémas visés — `https` et `http` au
    minimum observés ; inclure ou non les autres schémas (mailto, ftp, relatifs
    avec schéma, etc.)]
  - ~~forme exacte de la conservation du titre~~ **Résolu au specify
    (2026-10-05)** : seuls les libellés survivent ; destination et titre
    retirés.
  - [NEEDS CLARIFICATION: sémantique du retrait pour une destination absolue
    dans une ligne entièrement constituée du lien (libellé seul en sortie),
    cohérence avec le précédent FR-001 de 004]
  - [NEEDS CLARIFICATION: validation de la non-régression sur Exemple_2 où 21
    destinations `http` non-https vivent dans des motifs supprimés (aucun effet
    observable attendu — à confirmer par test)]
