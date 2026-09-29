# Research : Décidabilité des motifs au dry-run (fusion majoritaire)

**Feature**: 002-fusion-majoritaire | **Date**: 2026-09-29 | **Sources**: [spec.md](./spec.md), assessment `granularite-motifs` (intake, research, problem, concept, decision — mesure prototype du 2026-09-29), design feature 001 (research.md D1-D10, contracts/).

## D1. Règle de fusion majoritaire stricte

- **Décision** : dans `detecter()`, le calcul des blocs « touchés » change : pour chaque bloc existant, compter les pages de la fenêtre candidate où le chevauchement se produit ; la fusion n'est admise qu'avec les blocs où ce nombre est **strictement supérieur à la moitié** du nombre de pages de la candidate (`chevauchantes * 2 > len(pages_cles)`). À la moitié exacte ou en dessous : aucune fusion — la candidate crée son propre bloc.
- **Rationale** : formulation arithmétique entière de « strictement plus de la moitié » (clarification du 2026-09-29, Option B) ; sans flottant, donc sans imprécision de comparaison ; le prototype de l'assessment a validé le comportement à 50 % (25 motifs sur Exemple_2, filtres isolés, Exemple_1 inchangé).
- **Alternatives** : règle actuelle « ≥ 1 page » (rejetée : c'est la cause du blocage) ; proportion 80 % (mesurée : 29 motifs, plus de fragmentation sans gain de séparation) ; proportion ≥ 50 % (rejetée par la clarification : à la moitié exacte, pas de fusion).

## D2. Fusion multi-blocs

- **Décision** : si plusieurs blocs satisfont la règle majoritaire pour une même candidate, tous fusionnent dans le premier (ordre de la liste), comme aujourd'hui.
- **Rationale** : comportement inchangé par ailleurs ; seul le filtre d'admission change ; le tri et l'attribution des ids (position de première occurrence, fréquence décroissante) ne sont pas touchés.
- **Alternatives** : fusionner uniquement avec le bloc majoritaire au meilleur score (rejeté : ajoute un arbitrage arbitraire sans besoin constaté).

## D3. Rapport dry-run en deux sections

- **Décision** : le tableau de tête du rapport n'énumère plus que les motifs `action = supprimer` (« Décisions requises ») ; tous les motifs `action = conserver` (sous le seuil ou non) sont listés dans une section secondaire « Motifs conservés par défaut — aucune action requise » (la section « sous le seuil » actuelle est remplacée par cette section générale). `suggestion.json` reste inchangé : il continue de contenir tous les motifs, chacun actionnable — la section secondaire rappelle la commande d'édition.
- **Rationale** : FR-004 ; absorbe la multiplication des motifs sur les documents riches (mesure : ~25 listés, 4-5 décisions réelles) tout en gardant SC-006 (< 5 min de validation) ; le contrat existant déclare le rapport « structure indicative, seul suggestion.json est contractuel » — aucun changement de contrat requis, la nouvelle structure est documentée dans [contracts/rapport-dry-run.md](./contracts/rapport-dry-run.md).
- **Alternatives** : garder un tableau unique trié par action (rejeté : la table à 25 lignes est la douleur visée) ; plafonner la section secondaire à N lignes (rejeté : information cachée, YAGNI).

## D4. Documentation de l'instabilité des ids

- **Décision** : ajout au README d'une note « les ids de motifs ne sont pas stables entre versions de l'outil ; après une mise à jour, régénérez la suggestion par dry-run ; une suggestion d'une version antérieure échoue proprement (id inconnu, code 2) ».
- **Rationale** : FR-007, US3 ; le comportement d'échec est déjà prévu par le contrat de la feature 001 (`appliquer_actions` : id inconnu → erreur bloquante) — aucune modification de code, uniquement documentaire.
- **Alternatives** : note de version dédiée (rejeté : pas de CHANGELOG dans le projet, YAGNI) ; correspondance approximative des ids entre versions (rejetée : non déterministe et trompeuse).

## D5. Stratégie de tests

- **Décision** :
  - Unitaires : frontière majoritaire stricte — candidate chevauchant un bloc sur exactement la moitié de ses pages → pas de fusion ; sur strictement plus de la moitié → fusion ; blocs compacts d'Exemple_1 → 4 motifs identiques à la version précédente (ids, bornes des emplacements, actions).
  - Intégration (nouveau fichier `tests/integration/test_decidabilite.py`) : sur `Examples/Exemple_2` — la zone filtres (grande zone d'interface, emplacements contigus) et les métadonnées appartiennent à des motifs distincts ; nombre de motifs `supprimer` ≤ 5 ; la bascule du motif d'interface en `supprimer` et des motifs de métadonnées en `conserver` produit un `nettoye.md` sans filtres mais avec les métadonnées.
  - Régression : suite existante au vert sans relâchement des seuils (SC-004), déterminisme octet par octet (SC-005), Exemple_1 inchangé (SC-002).
- **Rationale** : chaque SC de la spec a son test mécanique ; la frontière stricte est le seul nouveau comportement unitaire ; le reste est une non-régression.
- **Alternatives** : snapshot complet des motifs d'Exemple_2 (rejeté : fragile au premier changement du corpus, les critères de la spec suffisent).

## D6. Constantes internes

- **Décision** : la frontière majoritaire est codée comme comparaison entière (`2 * chevauchantes > total_pages_candidate`) sans constante flottante nommée, avec un commentaire renvoyant à FR-001 et à la clarification du 2026-09-29.
- **Rationale** : éviter les artefacts de flottants (0.5, 0.51) et toute tentation d'en faire un paramètre ; FR-010 interdit toute option exposée.
- **Alternatives** : constante `PROPORTION_FUSION = 0.5` (rejetée : suggère un réglage là où la spec interdit d'en exposer).

## D7. Périmètre strictement borné

- **Décision** : ne pas toucher à `nettoyage.py`, `cartographie.py`, `segmentation.py`, `sortie.py`, `cli.py`, aux formats JSON ni aux scénarios d'usage ; la seule surface modifiée est `detecter()` (filtre d'admission des fusions), `generer_rapport()` (présentation) et le README (note ids).
- **Rationale** : FR-010 ; minimiser le risque de régression — le nettoyage consomme les emplacements calculés par la détection, inchangés dans leur format.
- **Alternatives** : aucune — borne explicite de la spec.
