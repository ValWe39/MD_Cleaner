# Concept: Étendre la passe de nettoyage aux destinations sans chevrons

- **Slug**: nettoyage-balises
- **Created**: 2026-10-27
- **Recommended option**: Option A — Règle unifiée à l'écriture, images épargnées

## Options

### Option A — Règle unifiée à l'écriture, images épargnées

- **Sketch**: la passe de nettoyage appliquée à l'écriture des sorties
  (features 004/005) s'étend à toute destination de lien sans chevrons,
  quel que soit son schéma (ancres, relatifs, absolus, relatifs sans
  slash), sans cas particulier — l'utilisateur relance le nettoyage et les
  livrables FIPECO ne portent plus que les libellés ; `--conserver-liens`
  conserve l'ancien comportement ; les images `![...]` ne sont pas
  touchées, par prudence vis-à-vis du contenu.
- **Appetite**: small
- **Trade-offs**: gagne — 199 occurrences éliminées sans retouche, un seul
  mécanisme, cohérence avec l'arbitrage 005, aucun nouveau drapeau ;
  sacrifie — la trace des 48 sources absolues par défaut (réversible),
  débris résiduels possibles sur images et libellés vides. Risque principal
  : régression sur les 5 314 formes chevrons si la règle est mal unifiée.
- **Rabbit holes**: vouloir aussi supprimer les blocs de navigation répétés
  (125 occurrences — périmètre détection de motifs) ; vouloir « réparer »
  ou décoder les URL encodées ; couvrir toutes les formes exotiques de
  Markdown (liens de référence, images-liens imbriqués) sans inventaire.

### Option B — Règle unifiée + nettoyage des résidus (images, libellés vides)

- **Sketch**: l'option A, plus le retrait des constructs devenus débris :
  `![](/images/...png)` à alt vide retiré entièrement, logo imbriqué
  réduit, libellés vides `[]` supprimés — le livrable est plus proche du
  « directement exploitable » sans retouche du tout.
- **Appetite**: small-medium
- **Trade-offs**: gagne — sorties plus propres, moins de débris visuels ;
  sacrifie — des figures (contenu) disparaissent, la frontière
  « débris/contenu » devient une décision de l'outil, risque de perte
  d'information contraire à l'exigence utilisateur de conservation.
- **Rabbit holes**: définir ce qu'est un « débris » (alt vide ? image dans
  un lien de nav ?) glisse vers la détection sémantique — hors budget
  small ; chaque règle de résidu ajoute ses propres cas d'erreur.

### Option C — Ne rien construire : recette manuelle documentée

- **Sketch**: le README documente une recette grep/sed pour retirer les
  destinations sans chevrons après un run ; rien ne change dans l'outil.
- **Appetite**: small (quelques heures de documentation)
- **Trade-offs**: gagne — zéro risque de régression ; sacrifie — le coût
  manuel persiste à chaque run (~40 retouches par fichier), contredit la
  métrique « 0 destination résiduelle » du problem.md.
- **Rabbit holes**: aucun, mais l'option C avait déjà été évaluée et
  rejetée en 004 pour exactement cette raison (précédent documenté).

## Recommendation

L'option A. Elle tient la métrique centrale (199 → 0 destination résiduelle
sur le corpus FIPECO) avec le budget le plus petit, hérite du mécanisme et
de la réversibilité déjà éprouvés (004/005), et tranche les questions
ouvertes du côté de la conservation : les images et figures sont épargnées
parce que l'exigence utilisateur explicite (« sans enlever du contenu
d'intérêt ») prime sur le gain cosmétique de l'option B — les débris
résiduels d'images et de navigation relèvent de la passe détection de
motifs, déjà identifiée comme périmètre distinct. L'option B reste
comme variante de suivi si les résidus gênent, arbitrée sur un run réel.

## Out of Scope (for the recommended option)

- Suppression des blocs de navigation et pieds de page répétés (périmètre
  détection de motifs, features 001/002).
- Traitement des images et figures `![...]` : épargnées intégralement,
  débris résiduels tolérés et documentés.
- Décodage ou réparation des URL (caractères encodés).
- Liens cliquables par défaut ; modification des libellés ou du texte.
- URLs nues et blocs de code (contrats 005 reconduits).

## Assumptions to Validate

- La forme des liens du corpus FIPECO est représentative des sorties du
  convertisseur de l'utilisateur (aucune autre forme exotique attendue).
- Une règle unifiée peut couvrir chevrons et non-chevrons sans changer le
  comportement à l'octet sur les 5 314 formes chevrons historiques.
- Les libellés vides résiduels (`[]`) sont absents ou rarissimes après
  épargne des images (3 libellés vides observés sont des alt d'images).
- Aucun lien de référence `[libellé][ref]` n'apparaît dans les corpus
  futurs (aucun observé à ce jour).
