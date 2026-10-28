# Decision: Nettoyer les destinations de liens résiduelles à l'écriture

- **Slug**: nettoyage-liens-html
- **Decided**: 2026-10-02
- **Verdict**: go
- **Artifacts reviewed**: intake.md | research.md | problem.md | concept.md

## Scorecard

- **Problem validity** (strong) : Problème réel et mesuré sur un livrable
  concret : 527/1724 lignes (~31 %) de `output/004/nettoye.md` portent une
  destination `(</...>)` ; le livrable « directement exploitable » exigé une
  retouche manuelle à chaque run (problem.md, research.md)
- **Evidence strength** (strong) : Faits décisifs mesurés, pas supposés :
  dénombrement grep sur sortie et entrée réelles, lecture du code
  (`normalisation.py` ne tokenize pas ces destinations), précédents 002/003
  documentés, collision `<!-- page: N -->` identifiée. Seule zone soft : demande
  d'un unique utilisateur (research.md, confidence low) — non décisive ici car
  le problème est observé sur les artefacts, pas seulement déclaré
- **Value vs. inaction** (strong) : L'inaction maintient une retouche manuelle
  répétitive et fragile contredisant le positionnement du README ; l'option C
  (recette documentée) a été évaluée et rejetée précisément pour cela
  (concept.md)
- **Feasibility / appetite** (strong) : Option A crédible en appetite small :
  une passe regex stdlib à l'écriture, un drapeau, tests, doc — cohérente avec
  les précédents features 001-003 (une règle déterministe par passe)
- **Strategic fit** (strong) : Conforme à la constitution (local, déterministe,
  stdlib, sorties dans `output/`) ; le placement en aval de la détection
  neutralise la tension avec les décisions des features 002/003 qui s'appuient
  sur les liens de thème au dry-run
- **Risk posture** (adequate) : Risques majeurs identifiés et mitigés par design
  (passe post-détection ; marqueurs `<!-- page: N -->` non matchés par
  `](</...>)`, à confirmer par tests) ; risques résiduels assumés : premier
  paramètre « activé par défaut » (pattern UX inédit, migration des tests
  existants), forme finale `[libellé]` vs `libellé` non tranchée, validation sur
  un seul corpus réel

## Verdict & Rationale

**Go.** Aucun critère sous adequate ; les deux critères make-or-break sont tenus
par de la mesure, pas de l'enthousiasme : le problème est quantifié sur la
sortie réelle du run 004, et la collision avec les décisions antérieures (liens
de thème conservés pour le dry-run, marqueurs de pagination produits par
l'outil) a été découverte et neutralisée au stade recherche/concept par le choix
du point d'application (à l'écriture, en aval de la détection). Le point faible
— un seul utilisateur porteur de la demande — n'affaiblit pas le problème,
observé sur les artefacts. Les risques résiduels (pattern « activé par défaut »,
forme exacte de la ligne de sortie) sont bornés et relèvent de la spécification,
pas de l'opportunité : le concept les a explicitement listés comme hypothèses à
valider plutôt que comme inconnues bloquantes.

## If go — Handoff to `/speckit-specify`

- **Problem**: la sortie nettoyée conserve des destinations de liens inline
  `(</...>)` collées au texte utile (~31 % des lignes du run 004), dégradant le
  livrable final et exigeant une retouche manuelle à chaque run.
- **Chosen approach**: Option A du concept.md — passe de nettoyage à l'écriture
  de `nettoye.md` et `nettoye-pagine.md`, en aval de la détection ; cible
  limitée à la forme `](</...>)` ; activée par défaut, désactivable par drapeau
  CLI.
- **In scope**: la passe de nettoyage et sa règle ; le drapeau de désactivation
  et son contrat CLI ; la mise à jour des tests (contenus attendus, marqueurs
  `<!-- page: N -->` préservés) ; la documentation.
- **Out of scope**: décodage/réparation d'URL ; destinations absolues
  `](http...)` et vraies balises HTML ; modification des libellés ou du reste du
  texte ; extraits du dry-run, `suggestion.json`, `rapport-dry-run.md`,
  `cartographie.json` ; reformatage Markdown général.
- **Success metrics**: (1) 0 ligne de la sortie avec destination `(</...>)` sur
  le run équivalent au 004 (baseline 527/1724) ; (2) reste du texte inchangé
  octet par octet hors destinations ; (3) sorties inchangées sur corpus sans
  liens inline ; (4) tests au vert sans relâchement ; (5) déterminisme conservé.
- **Carried-forward open questions**:
  - [NEEDS CLARIFICATION: forme de la ligne de sortie : `[libellé]` conservé tel
    quel, ou lien réduit au libellé nu ?]
  - [NEEDS CLARIFICATION: nom du drapeau de désactivation et intégration au
    contrat CLI (codes retour inchangés)]
  - [NEEDS CLARIFICATION: suppression brute des caractères encodés (`%5B`,
    `%3A`) — confirmation utilisateur]
  - [NEEDS CLARIFICATION: validation de la forme `](</...>)` sur d'autres corpus
    que Exemple_2 (Exemple_1 contient `[CORSEN AI](</fr/>)`)]
  - [NEEDS CLARIFICATION: existence d'autres usages du dépôt dépendant des liens
    cliquables en sortie]
