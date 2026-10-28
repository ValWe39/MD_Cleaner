# Concept: Nettoyer les destinations de liens résiduelles à l'écriture

- **Slug**: nettoyage-liens-html
- **Created**: 2026-10-02
- **Recommended option**: Option A — Passe de nettoyage à l'écriture, activée
  par défaut

## Options

### Option A — Nettoyage à l'écriture (smallest thing that could work)

- **Sketch**: Lors de la production de `nettoye.md` (et de `nettoye-pagine.md`),
  une passe retire les destinations de liens de la forme `](</...>)` ; le
  libellé et tout le reste de la ligne restent inchangés. Activée par défaut,
  désactivable par un drapeau CLI, pour qui veut des liens cliquables. La
  détection, le dry-run et les extraits ne changent pas : les liens de thème
  restent visibles pour juger les motifs (features 002/003 intactes) ; seule la
  sortie finale est nettoyée.
- **Appetite**: small (quelques jours : une règle, un drapeau, tests, doc)
- **Trade-offs**: Tient la promesse « sortie directement exploitable » sans
  toucher au moteur ; coût : premier paramètre « activé par défaut » de l'outil
  (pattern UX inédit, migration des tests existants qui comparent le contenu des
  sorties), et la sortie finale n'a plus de liens cliquables sauf désactivation
  explicite. Risque faible sur les marqueurs `<!-- page: N -->` produits par
  l'outil : ils ne matchent pas la forme `](</...>)`, à confirmer par tests.
- **Rabbit holes**: Étendre la règle aux destinations absolues `](http...)` ou
  aux vraies balises HTML (glissement de périmètre signalé dès l'intake) ;
  vouloir décoder/réparer les URL ; vouloir aussi nettoyer les extraits du
  dry-run (casserait la distinctivité des motifs, feature 003).

### Option B — Nettoyage en amont, avant la détection

- **Sketch**: Les destinations sont retirées des lignes dès le chargement, avant
  segmentation/détection : tout le pipeline (motifs, extraits, dry-run, sorties)
  travaille sur du texte déjà épuré.
- **Appetite**: small–medium (la règle est simple mais les conséquences se
  propagent : recalibrage, extraits, tests)
- **Trade-offs**: Sortie cohérente d'un bout à l'autre ; mais les extraits du
  dry-run perdent les liens de thème qui rendent aujourd'hui les motifs
  métadonnées indiscernables distinctifs (feature 003), la sémantique
  supprimer/conserver de la feature 002 s'appuie sur des éléments qui
  disparaissent, et les ids de motifs M01… changent pour tous les documents
  (suggestions à régénérer). Sacrifie des décisions produites pour un gain de
  lisibilité final qui n'en a pas besoin.
- **Rabbit holes**: Régression des features 002/003 ; revalidation complète de
  la suite de tests d'acceptation ; renégociation des seuils de détection.

### Option C — Ne rien construire : recette manuelle documentée

- **Sketch**: Le README documente une commande de post-traitement
  (sed/PowerShell) que l'utilisateur lance après chaque run.
- **Appetite**: small (une heure de doc)
- **Trade-offs**: Zéro risque sur le moteur ; mais la retouche reste répétitive,
  fragile (regex à recopier, Windows/Unix), et contredit le positionnement « une
  commande, sortie directement exploitable ». Ne tient aucune des success
  metrics automatisables.
- **Rabbit holes**: Maintenance de recettes par OS ; divergence entre recette
  documentée et usages réels.

## Recommendation

**Option A.** Elle est la seule à tenir les goals sans toucher au moteur :
destinations absentes de la sortie finale (métrique grep = 0), reste du texte
inchangé (la passe ne cible que `](</...>)`), réversibilité par drapeau pour les
usages cliquables. Les features 002/003 — dont les décisions reposent sur les
liens de thème visibles au dry-run — restent intactes parce que le nettoyage vit
en aval de la détection, ce que la recherche identifiait comme le principal
risque (Option B). L'appetite small est cohérent avec un projet à une seule
règle déterministe par passe (précédents features 001–003). Le coût assumé est
le pattern inédit « activé par défaut » : c'est précisément la demande explicite
de l'utilisateur, et la migration des tests est bornée.

## Out of Scope (for the recommended option)

- Décoder ou réparer les URL (`%5B`, `%3A` laissés tels quels puis supprimés
  avec la destination) ; reconstruire des URL absolues.
- Destinations absolues `](http...)` et vraies balises HTML — périmètre limité à
  la forme chevron `](</...>)`.
- Modifier les libellés, le reste du texte des lignes, ou retirer des lignes
  entières (la détection supprimer/conserver n'est pas rejugée).
- Nettoyer les extraits du dry-run, `suggestion.json`, `rapport-dry-run.md` ou
  `cartographie.json`.
- Un reformatage Markdown général (listes, titres, espaces).

## Assumptions to Validate

- La forme visée est exactement `](</...>)` (destination entre chevrons, pas de
  vraies balises HTML dans les corpus réels) — confirmé sur Exemple_2, à valider
  sur d'autres corpus.
- Les libellés `[texte]` restent tels quels, crochets compris (l'utilisateur a
  demandé de ne pas toucher le reste du texte ; la forme finale `[libellé]` vs
  `libellé` reste à trancher en spécification).
- Le drapeau de désactivation suit le pattern argparse standard et le contrat
  CLI (codes retour inchangés).
- Les marqueurs `<!-- page: N -->` de `nettoye-pagine.md` ne sont pas matchés
  par la règle.
- Une seule regex stdlib suffit (aucune dépendance runtime, conformité
  constitution).
- Le comportement par défaut activé est acceptable pour les tests existants
  après mise à jour (contenus attendus régénérés).
