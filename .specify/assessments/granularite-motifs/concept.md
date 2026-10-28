# Concept: Rendre chaque motif décidable indépendamment au dry-run

- **Slug**: granularite-motifs
- **Created**: 2026-09-29
- **Recommended option**: A — Coupure de fusion par chevauchement majoritaire

## Options

### Option 0 — Ne rien faire

- **Sketch** : conserver la détection actuelle ; l'utilisateur continue
  d'arbitrer au niveau bloc, tout-ou-rien, sur les documents à métadonnées
  récurrentes.
- **Appetite** : small (nul)
- **Trade-offs** : gagne zéro coût ; sacrifie l'utilisabilité du dry-run sur la
  classe listings (cas output-016), la douleur est documentée mais reste rare (1
  document sur 3 du corpus).
- **Rabbit holes** : aucun ; c'est la référence de coût de l'inaction
  (problem.md).

### Option A — Coupure de fusion par chevauchement majoritaire

- **Sketch** : aujourd'hui, deux fenêtres récurrentes fusionnent dès qu'elles se
  chevauchent sur *au moins une* page. Le concept : une fusion n'est admise que
  si le chevauchement se vérifie sur la *majorité des pages* concernées. Les
  ponts ponctuels (un lien de thème apparaissant une fois dans chaque zone) ne
  collent plus les blocs entre eux : la barre de filtres et les métadonnées de
  publications deviennent naturellement des motifs distincts, togglables
  séparément.
- **Appetite** : small (quelques jours, tests compris)
- **Trade-offs** : gagne la décidabilité visée (critère binaire du problem.md)
  sans nouvelle machinerie — une règle de plus, pas un nouveau signal ; sacrifie
  la stabilité des ids de motifs entre versions de l'outil (les suggestions
  existantes doivent être régénérées) ; risque de *sur-scission* : des blocs
  légitimement chaînés (nav compacte en plusieurs fenêtres contiguës) pourraient
  se séparer si leur chevauchement est minoritaire — à vérifier sur Exemple_1.
- **Rabbit holes** : le seuil exact de « majorité » (50 % ? 80 % des pages ?) et
  la définition du dénominateur (pages de la fenêtre ? pages du bloc ?) — un
  mauvais choix casse soit le regroupement utile, soit la coupure visée ;
  comportement à valider sur les trois documents du corpus avant de figer.

### Option B — Scission a posteriori des blocs éclatés

- **Sketch** : la détection reste inchangée (couverture garantie) ; en sortie,
  un motif dont les intervalles sont dispersés sur les pages (plusieurs zones
  disjointes) est redécoupé en sous-motifs par zone contiguë, chacun recevant
  son propre id et son toggle dans la suggestion.
- **Appetite** : small-medium (une à deux semaines)
- **Trade-offs** : gagne une granularité présentation sans toucher à la
  mécanique de détection — risque de régression minimal sur le nettoyage ;
  sacrifie la simplicité du contrat (sous-ids, hiérarchie motif/sous-motif dans
  suggestion.json), et la règle de groupement par zone reste heuristique ; sur
  output-016, M02 donnerait ~7-10 sous-blocs — dans la fourchette 5-10 de
  l'intake, mais par coïncidence structurelle plutôt que par design.
- **Rabbit holes** : le critère « éclaté » (combien d'intervalles ? quel ratio
  de couverture ?) et la granularité du groupement — facile de finir avec des
  sous-blocs arbitraires que l'humain ne comprend pas mieux que le méga-bloc.

### Option C — Signaux de contenu comme frontières de fusion

- **Sketch** : s'inspirer de l'art antérieur (trafilatura, Boilerpipe) : chaque
  fenêtre récurrente reçoit un profil — densité de liens par ligne, position
  relative dans la page — et deux fenêtres de profils différents ne fusionnent
  jamais, même si elles se chevauchent. Interface (forte densité de liens, zones
  fixes) et métadonnées (profil mixte) se séparent par nature.
- **Appetite** : medium (quelques semaines)
- **Trade-offs** : gagne la classification la plus fidèle à l'état de l'art et
  potentiellement la plus robuste sur de nouveaux types de documents ; sacrifie
  la simplicité (constitution IV) : nouveaux paramètres, nouveaux seuils, et le
  profil « position/densité » sur des lignes markdown (sans DOM) est bruité — le
  coût de maintenance dépasse le besoin constaté (un cas douloureux).
- **Rabbit holes** : calibrage des seuils de densité ; interaction avec --seuil
  ; risque de casser la détection compacte actuelle (Exemple_1) pour un gain
  théorique.

## Recommendation

**Option A**. Elle attaque directement la cause du problème (le chevauchement
minoritaire qui soude des zones hétérogènes), avec le plus petit budget (small),
une seule nouvelle règle déterministe, et satisfait le critère binaire du
problem.md (filtres et métadonnées séparés sur output-016). Elle est réversible
: si la mesure montre une sur-scission, l'option B est le repli naturel
(scission a posteriori) sans avoir à défaire A. L'option C est disproportionnée
pour un corpus de 3 documents ; l'option 0 laisse le dry-run inutile sur la
classe listings. La cible « 5-10 blocs » de l'intake n'est pas retenue comme
plafond dur : A devrait naturellement produire un compte borné (interface, fil
d'Ariane, footer, métadonnées...), à vérifier en specification contre la
métrique « charge de validation < 5 min » (SC-004).

## Out of Scope (for the recommended option)

- Aucun plafond ni plancher numérique de blocs (la cible 5-10 devient une simple
  observation à surveiller, pas une contrainte)
- Pas de nouvelle option CLI ni de nouveau signal (densité, position)
- Pas de changement des formats de sortie ni du contrat suggestion.json (les ids
  changent *entre versions de l'outil*, mais le schéma reste identique)
- Pas de re-traitement des suggestions anciennes (régénération par dry-run,
  comportement documenté)
- Non-goals hérités de problem.md : pas de DOM, pas de sélection ligne à ligne,
  pas de changement de sémantique supprimer/conserver

## Assumptions to Validate

- Le pontage interface ↔ métadonnées sur output-016 passe bien par des
  chevauchements *minoritaires* — si les chevauchements sont majoritaires, la
  coupure A ne sépare rien et il faut passer à B
- La fusion compacte légitime (nav d'Exemple_1, 54 lignes contiguës) repose sur
  des chevauchements majoritaires et survivra à la coupure
- Les comptages de motifs après coupure restent bornés (ordre de grandeur < 15)
  sur le corpus réel
- La suite de tests existante (SC-001, SC-002, SC-005) passe sans modification
  des seuils d'acceptation
- L'instabilité des ids entre versions de l'outil est acceptable pour
  l'utilisateur (les suggestions se régénèrent par dry-run)
