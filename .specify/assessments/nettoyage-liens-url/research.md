# Idea Research: Étendre le nettoyage aux destinations de liens absolues

- **Slug**: nettoyage-liens-url
- **Created**: 2026-10-05
- **Evidence confidence (overall)**: high

## Users & Demand

- Demande explicite d'un unique utilisateur (propriétaire du projet) : «
  Pourquoi à ton avis j'ai encore des balises https dans mes sorties ? »
  (2026-10-05), suivie de la validation de l'idée d'intake. — [source: session
  de diagnostic 2026-10-05, intake.md] (confidence: medium)
- Comportement observé sur artefact, pas seulement déclaré : 6 lignes avec
  `](<https...>)` sur 299 lignes (~2 %) dans `output/009/nettoye.md` (run du
  2026-10-05 sur la doc Mistral) ; 0 occurrence résiduelle sur les corpus de
  référence Exemple_1/Exemple_2 (`output/005`, `output/006`). — [source: grep
  sur output/005, 006, 007, 009] (confidence: high)
- Le problème n'apparaît que sur un nouveau type de corpus (documentation
  Mistral convertie, un sujet par page) ; les deux corpus d'exemples historiques
  du dépôt n'en produisent aucune. Le 2026-10-05, l'utilisateur a archivé ce
  corpus comme `Examples/Exemple_3/2.Input/retry-failed-records.md` (320 lignes,
  6 lignes avec `](<https...>)`, 38 avec `](</...>)`), en faisant un corpus de
  référence du projet. — [source: grep output/005, 006 ; find/grep
  Examples/Exemple_3 (mise à jour utilisateur 2026-10-05)] (confidence: high)
- Exigences utilisateur explicites du 2026-10-05 (raffinement de l'idée) : (1)
  élargir le retrait aux autres schémas possibles (`http` ? autres ?) ; (2)
  ajouter un garde-fou : une URL explicitement indiquée dans le corps du texte
  (extrait de code, explicitation particulière) doit être conservée dans la
  sortie finale. — [source: message utilisateur 2026-10-05] (confidence: high)

## Prior Art

- Interne — la borne « destinations absolues hors périmètre » de la feature 004
  n'est pas un jugement sur l'utilité des liens absolus : c'est un garde-fou
  anti-glissement de périmètre posé dès l'intake (« glissement de périmètre
  signalé dès l'intake », `concept.md`) et repris tel quel dans les rabbit
  holes, le problem.md et le decision.md (out of scope). Aucun artefact 004 ne
  documente de raison de fond contre le retrait des absolus. — [source:
  `.specify/assessments/nettoyage-liens-html/{intake,concept,problem,decision}.md`]
  (confidence: high)
- Interne — la mécanique d'extension existe déjà :
  `RE_DESTINATION_LIEN = re.compile(r"(?<=\])\(</[^>]*>\)")` dans
  `md_cleaner/nettoyage.py` exige littéralement `</` après la parenthèse ; une
  variante `](<https...>)` est une modification regex mineure au même point
  d'application (écriture de `nettoye.md` / `nettoye-pagine.md`, en aval de la
  détection). — [source: lecture `md_cleaner/nettoyage.py`] (confidence: high)
- Interne — contre-preuve de prévalence : dans Exemple_2 (Cour des comptes),
  l'entrée contient 672 lignes avec `](<http` (dont 651 `](<https`), mais 0
  survit au nettoyage dans les runs 004 (pré-feature) et 006 (post-feature) :
  toutes ces destinations sont dans des motifs supprimés par la détection. —
  [source: grep `Examples/Exemple_2/2.Input/consolidated.md`, `output/004`,
  `output/006`] (confidence: high)
- Externe — le retrait de destinations Markdown en conservant le libellé est un
  problème récurrent et bien balisé : recettes sed/regex publiées
  (unix.stackexchange.com/questions/798025 « How to remove markdown links from
  headers with sed », gist.github.com/mdonkers), bibliothèque regex101 « Remove
  Markdown Links », et outils en ligne type « Strip Markdown » proposant
  l'option « keep link text ». — [source: résultats de recherche web (snippets,
  non fetchés), hosts unix.stackexchange.com/gist.github.com allowlistés,
  thetexttool.com non fetché] (confidence: medium)

## Market & Context

- Alternative actuelle : retouche manuelle des 6 lignes à chaque run sur corpus
  type doc Mistral — coût faible mais répétitif, contredisant le positionnement
  « directement exploitable » du livrable déjà retenu dans l'assessment 004
  (decision.md, criterion Value vs. inaction). — [source: decision.md 004 ;
  output/009] (confidence: medium)
- Autre alternative : agir sur la détection plutôt que sur les liens — le
  rapport dry-run 008 montre qu'aucun motif n'atteint le seuil de 80 % sur ce
  corpus (« Décisions requises : aucun », motifs M01-M04 conservés, fréquences
  0.23-0.46) ; baisser `--seuil` ou améliorer la détection pourrait supprimer la
  nav/pied de page entiers au lieu d'en nettoyer les URLs. — [source:
  `output/008/rapport-dry-run.md`] (confidence: high)

## Data & Constraints

- Formes résiduelles observées dans `output/009/nettoye.md` : exclusivement
  `](<https://...>)` avec chaînes de requête (`utm_source=docs&...`), 6 lignes
  (en-tête « Reach out » / « Try Studio », pied de page « Why Mistral » / «
  Explore » / « Build » / community). Aucune forme `](https://...)` sans
  chevrons observée dans les sorties vérifiées. — [source: lecture
  output/009/nettoye.md] (confidence: high)
- Mesure sur l'entrée Exemple_3 (`retry-failed-records.md`, 320 lignes) : les 6
  occurrences de `http` du document sont toutes des destinations de liens
  `](<https...>)` situées dans la nav (ligne 13) et le pied de page (lignes 295,
  299, 307, 311, 315) ; aucune URL nue dans le corps du texte ou dans un bloc de
  code dans ce corpus — le garde-fou demandé par l'utilisateur n'y serait donc
  pas sollicité, mais reste pertinent pour les corpus futurs. — [source: grep -n
  http Examples/Exemple_3/2.Input/retry-failed-records.md] (confidence: high)
- Formes à couvrir dans le corpus : `](<https...>)` seul schéma observé à ce
  jour dans tous les corpus (`](<http` non-https : 21 lignes dans Exemple_2, 0
  dans Exemple_1 et Exemple_3) ; Exemple_2 contient aussi des destinations
  absolues dans des motifs supprimés. Le retrait cible la syntaxe `](<...>)`,
  donc une URL nue dans un bloc de code (hors syntaxe de lien) ne matche pas et
  serait conservée par construction. — [source: grep Examples/Exemple_1..3]
  (confidence: high)
- Corpus Mistral désormais archivé :
  `Examples/Exemple_3/2.Input/retry-failed-records.md` (320 lignes, 13 pages,
  segmentation heuristique) — le gap de mesure côté entrée est résolu. —
  [source: find Examples/Exemple_3, mise à jour utilisateur 2026-10-05]
  (confidence: high)
- Contrainte d'architecture : toute extension toucherait le même point
  d'application que la feature 004 (`nettoyer_destinations`), avec le même
  drapeau de désactivation `--conserver-liens` (FR-003 004) ou un drapeau
  distinct à arbitrer ; la constitution impose local, déterministe, stdlib — une
  passe regex reste conforme. — [source:
  `specs/004-nettoyage-liens-html/spec.md` FR-003, lecture code] (confidence:
  high)

## Evidence Against the Idea

- Prévalence faible mais désormais institutionnalisée : 6 lignes sur 320 (~2 %)
  dans Exemple_3, 0 ligne résiduelle sur Exemple_1/Exemple_2 ; l'utilisateur a
  néanmoins archivé le corpus Mistral comme exemple de référence du projet et
  demande explicitement l'extension — le signal de demande est passé de «
  observation » à « exigence formulée », ce qui affaiblit cet argument par
  rapport à la version initiale. — [source: grep Examples/Exemple_1..3, message
  utilisateur 2026-10-05] (confidence: high)
- Forme composée à traiter : Exemple_2 contient 21 lignes `](<http...` non-https
  avec titre inclus, ex. `[Haut Conseil des finances publiques
  (HCFP)](<http://www.hcfp.fr/> "Haut Conseil des finances publiques
  \(HCFP\)\(nouvelle fenêtre\)")` — la cible n'est donc pas toujours la seule
  destination `(<url>)`, parfois `(<url> "titre")` ; l'extension devra définir
  ce qu'il advient du titre. — [source: grep
  Examples/Exemple_2/2.Input/consolidated.md] (confidence: high)
- La cause racine est peut-être la détection, pas les liens : la nav et le pied
  de page Mistral survivent parce qu'aucun motif n'atteint le seuil ; nettoyer
  les URLs laisserait des lignes de nav dégradées (« []Docs & API », «
  [Vibe]\[Studio]... ») toujours présentes — le livrable resterait à retoucher.
  — [source: output/008/rapport-dry-run.md, output/009/nettoye.md] (confidence:
  high)
- Perte d'information potentielle : contrairement aux chemins relatifs cassés
  d'Exemple_2, les URLs absolues sont des destinations réelles et cliquables ;
  les retirer par défaut détruit une information que certains usages peuvent
  vouloir conserver (la question est documentée comme borne de l'assessment 004,
  sans réponse de fond). — [ASSUMPTION] (confidence: medium)
- Décision inverse récente : la limite a été posée il y a 3 jours (decision.md
  004, 2026-10-02) avec un verdict fondé sur la mesure du problème relatif ; le
  rouvrir sans nouvelle mesure d'ampleur risque un glissement de périmètre —
  exactement le rabbit hole que 004 voulait éviter. — [source: decision.md 004]
  (confidence: high)

## Gaps & Open Questions

- [NEEDS CLARIFICATION: pourquoi la nav/pied de page du corpus Mistral n'est pas
  détectée comme motif récurrent au seuil de 80 % — si la détection les
  attrapait, la question du nettoyage des URLs absolues deviendrait secondaire
  pour ces lignes]
- [NEEDS CLARIFICATION: liste exacte des schémas à viser (`https` seul, `http`
  inclus, autres schémas — `mailto`, `ftp`, etc.) ; l'utilisateur a tranché le
  principe (« élargir ») pas la liste]
- [NEEDS CLARIFICATION: définition opérationnelle du garde-fou « URL
  explicitement indiquée dans le corps du texte » : s'agit-il (a) des URLs nues
  hors syntaxe de lien — déjà non-matchées par une cible `](<...>)`, (b) des
  lignes dans des blocs de code — hors du flux Markdown, ou (c) des liens inline
  dans une explicitation de prose, qui exigeraient une distinction contexte par
  contexte ? Le cas (c) n'est pas mécanisable par une simple regex sans critère
  discriminant]
- [NEEDS CLARIFICATION: traitement des formes `(<url> "titre")` (destination +
  titre, 21 lignes dans Exemple_2) — retirer destination et titre, ou conserver
  le titre en sortie ?]
- [NEEDS CLARIFICATION: le retrait des absolus doit-il être activé par défaut
  (comme 004) ou opt-in, sachant que les URLs absolues sont des destinations
  valides et cliquables, contrairement aux chemins relatifs cassés visés par
  004]

## Sources

- `output/009/nettoye.md`, `output/008/rapport-dry-run.md`,
  `output/005..007/nettoye.md` (repo, lecture locale)
- `Examples/Exemple_1/2.Input/consolidated.md`,
  `Examples/Exemple_2/2.Input/consolidated.md` (repo, lecture locale)
- `md_cleaner/nettoyage.py` (repo, lecture locale)
- `.specify/assessments/nettoyage-liens-html/{intake,concept,problem,research,decision}.md`
  (repo, lecture locale)
- `specs/004-nettoyage-liens-html/spec.md` (repo, lecture locale)
- <https://unix.stackexchange.com/questions/798025/how-to-remove-markdown-links-from-headers-with-sed>
  (host: unix.stackexchange.com, policy: allowlisted — snippet de résultats de
  recherche, non fetché)
- <https://gist.github.com/mdonkers/e4d76ad619683195f106bc00a5bff1a5> (host:
  gist.github.com, policy: allowlisted — snippet de résultats de recherche, non
  fetché)
- <https://thetexttool.com/tools/strip-markdown> (host: thetexttool.com, policy:
  unrecognized — non fetché, snippet cité depuis résultats de recherche)
- <https://regex101.com/library/REIVvj> (host: regex101.com, policy:
  unrecognized — non fetché, titre cité depuis résultats de recherche)
