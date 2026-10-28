# Idea Research: Plafonner le nombre de motifs détectés par requête (5-10)

- **Slug**: granularite-motifs
- **Created**: 2026-09-29
- **Evidence confidence (overall)**: medium (données internes : high ; art
  antérieur externe : medium ; signal utilisateur : low, n=1)

## Users & Demand

- Un seul utilisateur identifié : le propriétaire du projet, après un blocage
  concret sur `output/016` (impossible de supprimer la barre de filtres tout en
  gardant les métadonnées des publications, M02 étant un bloc indivisible de 274
  lignes) — [source: session de travail 2026-09-29, runs output/009-010]
  (confidence: high)
- Signal d'usage : ~10 runs dans `output/` sur la journée de mise en service ;
  une seule plainte de granularité, sur 1 document sur 3 testés — [source:
  dossier output/ local] (confidence: medium)
- Le besoin exprimé (« 5 à 10 blocs max ») est un souhait **dérivé** du besoin
  observé (des blocs décidables indépendamment) ; aucun utilisateur n'a demandé
  un chiffre précis — ASSUMPTION (confidence: medium)

## Prior Art

- **Site Style Tree (SST, Yi/Liu/Li 2003)** : les blocs de bruit d'un site
  partagent contenus et styles de présentation entre pages, tandis que les blocs
  de contenu principal diffèrent ; un arbre construit par échantillonnage de
  pages du même site détermine bruit vs contenu. Pertinent : c'est la famille
  d'approche de MD_Cleaner (comparaison multi-pages). La granularité y est le
  **bloc DOM**, pas une fusion transitive d'éléments — [source: recherche
  ResearchGate, « Boilerplate Detection Using Shallow Text Features » / SST]
  (confidence: medium)
- **Trafilatura** (référence open-source du domaine) : scoring par noeud sur
  longueur de texte, densité de liens et position ; modes `favor_precision` /
  `favor_recall`. Aucun contrôle « nombre de blocs » exposé à l'utilisateur — le
  curseur est la précision/rappel, pas un comptage — [source:
  trafilatura.readthedocs.io, « How extraction works » et « Evaluation »]
  (confidence: high)
- **Boilerpipe / shallow text features (Kohlschütter et al.)** : densité de
  liens et densité de texte comme signaux de bruit au niveau du bloc — [source:
  doc trafilatura citant boilerpy3 et la comparaison Bevendorff et al. 2023]
  (confidence: medium)
- Interne : décision D3 de `research.md` (feature 001) — la fusion des fenêtres
  chevauchantes en blocs maximaux est un choix de conception délibéré, corrigé
  une fois (intervalles disjoints au lieu d'union min-max) pour ne pas avaler
  les lignes intermédiaires — [source:
  specs/001-nettoyage-md-repetitif/research.md D3 + commit 010] (confidence:
  high)

## Market & Context

- Alternative actuelle de l'utilisateur : éditer la suggestion au niveau bloc
  (tout ou rien sur M02) — inadaptée au cas constaté ; pas d'alternative hors
  outil — [source: session 2026-09-29] (confidence: high)
- Coût de ne rien faire : la décision dry-run reste possible mais grossière ;
  sur des documents à métadonnées récurrentes (listings, catalogues), l'outil
  perd en utilité perçue — ASSUMPTION (confidence: medium)

## Data & Constraints

- **Comptages mesurés** (détection actuelle, seuil 80) : Exemple_1 = 4 motifs
  (tous compacts, 1 intervalle/page) ; Exemple_2 = 2 motifs ; output-016 = 2
  motifs dont M02 = 279 lignes max, 7 intervalles disjoints sur la page 1, 312
  lignes couvertes — [source: mesures locales du 2026-09-29] (confidence: high)
- Les trois documents réels produisent donc **déjà moins de 5 motifs** : un
  plafond à 10 ne changerait rien ; la borne basse (5) exigerait au contraire de
  **scinder** — [source: mêmes mesures] (confidence: high)
- Contraintes de la constitution : zéro dépendance runtime (pas de parseur DOM
  possible — l'entrée est du markdown en lignes), simplicité YAGNI, déterminisme
  FR-005 (tout plafond/split doit être une règle déterministe, pas un paramètre
  magique) — [source: .specify/memory/constitution.md, specs/001 spec.md]
  (confidence: high)
- Contrat existant : la suggestion et son édition portent sur des ids de motifs
  (M01+) ; toute re-granularisation change la sémantique des ids entre documents
  (déjà identifiée comme limite du contrôle `source` par nom) — [source:
  contracts/formats.md] (confidence: high)
- Les signaux de l'art antérieur (densité de liens, densité de texte, position)
  sont calculables sur des lignes markdown sans DOM — ASSUMPTION (confidence:
  medium)

## Evidence Against the Idea

- Le « max 10 » est un no-op sur les trois documents réels mesurés (2 à 4 motifs
  actuellement) — le problème constaté n'est pas un dépassement de nombre —
  [source: mesures locales] (confidence: high)
- Le « min 5 » forcerait une scission artificielle : Exemple_1 et ses 4 blocs
  compacts et homogènes n'ont aucun besoin d'être scindés — un plancher uniforme
  contredit YAGNI — [source: mesures locales] (confidence: high)
- Fusionner pour respecter un plafond réintroduirait exactement le défaut
  constaté (blocs hétérogènes non décidables) — ASSUMPTION (confidence: high)
- Aucun outil de l'art antérieur n'expose de comptage de blocs ; le réglage se
  fait sur des signaux (densité, précision/rappel) — un plafond numérique est un
  proxy fragile de l'objectif réel (homogénéité/décidabilité de chaque bloc) —
  [source: trafilatura docs] (confidence: medium)
- Un document riche peut légitimement contenir plus de 10 zones récurrentes
  distinctes (nav, fil d'Ariane, pub, filtres, footer, pagination,
  métadonnées...) : un plafond dur perdrait des distinctions utiles — ASSUMPTION
  (confidence: medium)

## Gaps & Open Questions

- [NEEDS CLARIFICATION: définir « homogène » de façon mesurable (contiguïté des
  intervalles, profil de densité de liens, position relative) — le nombre de
  blocs en est-il même un bon proxy ?]
- [NEEDS CLARIFICATION: la cible 5-10 vise-t-elle les motifs supprimables, tous
  les motifs, ou les « zones récurrentes » avant fusion ?]
- [NEEDS CLARIFICATION: quel comportement quand un document produit
  naturellement plus de blocs que la cible — fusion par proximité, troncature
  par priorité, avertissement ?]
- [NEEDS CLARIFICATION: les signaux de l'art antérieur (densité de liens par
  ligne, position) sont-ils compatibles avec l'entrée « lignes markdown » et la
  contrainte zéro dépendance ?]
- [NEEDS CLARIFICATION: ce réglage serait-il par défaut ou option CLI, et quelle
  interaction avec --seuil et le contrat des ids ?]

## Sources

- <https://trafilatura.readthedocs.io/en/latest/extraction-overview.html> (host:
  trafilatura.readthedocs.io, policy: résultats du connecteur web_search
  uniquement — aucune page fetchée)
- <https://trafilatura.readthedocs.io/en/latest/evaluation.html> (host:
  trafilatura.readthedocs.io, policy: idem)
- <https://www.researchgate.net/publication/221519989_Boilerplate_Detection_Using_Shallow_Text_Features>
  (host: researchgate.com, policy: idem — snippets seulement)
- Mesures locales : Examples/Exemple_1, Examples/Exemple_2,
  Web-Reader/output/output-016 (confidence: high)
- Documents internes : specs/001-nettoyage-md-repetitif/research.md (D3),
  contracts/formats.md, .specify/memory/constitution.md
