# Feature Specification: Nettoyage des destinations de liens absolues à l'écriture de la sortie

**Feature Branch**: `005-nettoyage-liens-absolus`

**Created**: 2026-10-05

**Status**: Draft

**Input**: Handoff de l'assessment `nettoyage-liens-url` (decision.md) : les sorties nettoyées conservent des destinations de liens absolues `](<https://...>)` collées au texte utile des lignes qui survivent à la détection (6 lignes sur 299 au run 009 sur Exemple_3), dégradant le livrable et exigeant une retouche manuelle. Option retenue : extension de la passe d'écriture de la feature 004 aux destinations absolues entre chevrons, activée par défaut, désactivable par le même drapeau `--conserver-liens` ; seuls les libellés survivent (destination et titre du lien retirés — arbitrage final au specify, révisant le decide) ; garde-fou : les URLs légitimes du corps du texte (URLs nues, blocs de code) ne sont pas touchées.

## Clarifications

### Session 2026-10-05

- Q: Le titre des formes `(<url> "titre")` est-il retiré avec la destination ? → A: Révisé au stade specify (2026-10-05) : seuls les libellés sont conservés ; la destination **et** le titre du lien sont retirés. Cet arbitrage remplace la décision du stade decide (« conserver le titre »), prise avant l'illustration concrète de la forme sur l'exemple HCFP.
- Q: Le comportement est-il couvert par un nouveau drapeau ? → A: Non, intégration dans le même drapeau `--conserver-liens` (decision du stade decide, confirmée).
- Q: La passe vise-t-elle toute destination entre chevrons `](<...>)` quel que soit son schéma, ou seulement les destinations absolues `http`/`https` ? → A: Toute destination entre chevrons `](<...>)`, sans distinction de schéma (relatifs, http, https, mailto, tel, ftp, etc.) — une seule règle, aucun cas particulier ; les schémas non observés (mailto, tel, ftp) sont couverts par la même règle (option A, arbitrée sur inventaire des cas).
- Q: Les destinations absolues sans chevrons `[Doc](https://exemple.fr)` sont-elles aussi retirées ? → A: Non, hors périmètre (option A) : seules les formes entre chevrons `](<...>)` sont visées ; aucune forme sans chevrons n'est observée dans les corpus, et le besoin reste détectable par un simple grep sur toute nouvelle entrée.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Sortie finale sans destinations absolues résiduelles (Priority: P1)

Un utilisateur lance le nettoyage d'un document Markdown issu d'une conversion HTML → Markdown dont les lignes de navigation et de pied de page survivent à la détection de motifs (typiquement Exemple_3, documentation Mistral). Sans réglage particulier, le `nettoye.md` produit ne contient plus aucune destination de lien `](<...>)`, quel que soit le schéma : les libellés et le reste du texte des lignes conservés restent lisibles, sans URLs et paramètres de suivi collés au texte. Il n'a plus aucune retouche manuelle à faire pour ce motif.

**Why this priority**: C'est la valeur centrale du handoff : tenir la promesse « sortie directement exploitable » sur le corpus Exemple_3, désormais exemple de référence du projet. C'est la métrique mesurée (0 destination absolue résiduelle contre 6/299 lignes au run 009).

**Independent Test**: Testable en rejouant le run équivalent au 009 (entrée `Examples/Exemple_3/2.Input/retry-failed-records.md`) et en vérifiant qu'aucune ligne de la sortie ne contient `](<`, alors que les libellés et le reste du texte des lignes concernées sont inchangés.

**Acceptance Scenarios**:

1. **Given** un document contenant des lignes avec `[libellé](<https://exemple.fr/contact?utm_source=docs>)`, **When** l'utilisateur lance le nettoyage (sans option particulière), **Then** le `nettoye.md` ne contient plus la destination et le libellé reste présent.
2. **Given** le corpus Exemple_3, **When** le nettoyage est lancé, **Then** aucune ligne de la sortie ne contient `](<`, et le nombre de lignes et leur ordre sont inchangés par rapport à un run avec la seule feature 004.
3. **Given** une ligne contenant plusieurs liens absolus (ex. pied de page « Why Mistral » : `[About us](<https://...>)[Our customers](<https://...>)...`), **When** le nettoyage est lancé, **Then** chaque destination est retirée et les libellés de tous les liens restent en place dans l'ordre.

---

### User Story 2 - Garde-fou : les URLs légitimes du corps du texte sont conservées (Priority: P2)

Un utilisateur nettoie un document qui contient des URLs explicitement indiquées dans le corps du texte : une URL nue dans un extrait de code (ex. `https://api.mistral.ai/v1` dans un bloc de code), ou une URL nue dans une phrase explicative. Le nettoyage des destinations absolues ne touche aucune de ces URLs : elles restent présentes, intactes, dans la sortie finale.

**Why this priority**: C'est le garde-fou explicitement exigé par l'utilisateur au stade research (2026-10-05) : le nettoyage vise les débris de conversion collés aux libellés, pas les URLs qui portent du sens dans le contenu. Sans cette garantie, la valeur de la feature se payerait en pertes d'information.

**Independent Test**: Testable en construisant un document contenant un bloc de code avec URL nue et une phrase avec URL nue hors syntaxe de lien, en lançant le nettoyage, et en vérifiant que ces URLs sont retrouvées intactes octet par octet dans la sortie.

**Acceptance Scenarios**:

1. **Given** un document dont un bloc de code contient `client = Mistral(api_key=...)` et une URL `https://api.mistral.ai`, **When** le nettoyage est lancé, **Then** le bloc de code de la sortie est identique octet par octet, URL comprise.
2. **Given** une phrase contenant une URL nue hors syntaxe de lien (ex. « la documentation est sur `https://docs.mistral.ai` »), **When** le nettoyage est lancé, **Then** l'URL nue reste présente et intacte dans la sortie.

---

### User Story 3 - Liens avec titre : seul le libellé survit (Priority: P3)

Un utilisateur nettoie un document contenant des liens absolus de la forme `[libellé](<url> "titre")` — typiquement des liens institutionnels avec attribut title hérité de la conversion (ex. Exemple_2 : `[Haut Conseil des finances publiques (HCFP)](<http://www.hcfp.fr/> "Haut Conseil des finances publiques \(HCFP\)\(nouvelle fenêtre\)")`). Le `nettoye.md` produit ne contient plus ni la destination ni le titre : seul le libellé reste, lisible et sans débris.

**Why this priority**: Arbitrage final de l'utilisateur au stade specify (2026-10-05) : seul le libellé porte la valeur dans le livrable ; destination et titre sont des débris de conversion. Priorité moindre que P1/P2 car aucune ligne des corpus de référence ne conserve ce motif après détection (les 21 occurrences d'Exemple_2 vivent dans des motifs supprimés).

**Independent Test**: Testable en construisant un document avec un lien `[libellé](<http://exemple.fr/> "titre explicatif")` dans une ligne conservée, en lançant le nettoyage, et en vérifiant que la sortie ne contient ni l'URL ni le titre, mais contient le libellé.

**Acceptance Scenarios**:

1. **Given** une ligne conservée contenant `[HCFP](<http://www.hcfp.fr/> "Haut Conseil \(nouvelle fenêtre\)")`, **When** le nettoyage est lancé, **Then** la sortie contient `[HCFP]` et ne contient ni `http://www.hcfp.fr` ni le texte du titre.
2. **Given** un lien relatif avec titre `](</chemin> "titre")` (forme héritée de 004, sans observation dans les corpus), **When** le nettoyage est lancé, **Then** la même règle s'applique : destination et titre retirés, libellé conservé.

---

### User Story 4 - Désactivation unique et non-régression (Priority: P4)

Un utilisateur qui veut des liens cliquables (absolus comme relatifs) lance le nettoyage avec le drapeau `--conserver-liens` : la sortie est identique à celle produite avant la feature, destinations absolues comprises. Sur les corpus Exemple_1 et Exemple_2, où aucune destination absolue ne survit à la détection, les sorties par défaut sont inchangées octet par octet par rapport aux runs avec la seule feature 004.

**Why this priority**: La réversibilité par le drapeau existant (arbitrage decide : même drapeau, pas de nouveau drapeau) et la non-régression sur les corpus de référence conditionnent l'acceptabilité du comportement par défaut ; la valeur est déjà délivrée par P1-P3.

**Independent Test**: Testable en lançant le même run avec `--conserver-liens` (comparaison octet par octet à une sortie pré-feature) et en rejouant les runs Exemple_1/Exemple_2 (comparaison octet par octet aux sorties 004).

**Acceptance Scenarios**:

1. **Given** un document avec liens absolus, **When** l'utilisateur lance le nettoyage avec `--conserver-liens`, **Then** le `nettoye.md` contient les destinations intactes, identiques à une sortie produite sans la feature.
2. **Given** le corpus Exemple_2, **When** le nettoyage est lancé sans option, **Then** la sortie est identique octet par octet à celle du run équivalent 004 (aucune destination absolue n'y survit à la détection).
3. **Given** un run `--pagine` sur un document avec liens absolus, **When** le nettoyage est appliqué, **Then** `nettoye-pagine.md` est nettoyé comme `nettoye.md`, et chaque marqueur de page reste présent à l'identique.

---

### Edge Cases

- Que se passe-t-il quand l'URL contient des caractères encodés ou des paramètres de suivi longs (`?utm_source=docs&utm_medium=header_cta`) ? La destination est retirée telle quelle, sans décodage ni réécriture ; les paramètres disparaissent avec elle.
- Comment le système gère-t-il un lien absolu au libellé vide `[](<https://exemple.fr>)` ? La destination est retirée comme pour tout lien ; les crochets vides restent (cohérence avec FR-001 de la feature 004).
- Comment le système gère-t-il une ligne entièrement constituée d'un lien absolu seul sur sa ligne ? La ligne reste présente avec son libellé seul ; aucune ligne n'est supprimée par cette passe (la suppression relève de la détection existante).
- Que se passe-t-il des formes sans chevrons `](https://exemple.fr)` ? Hors périmètre : aucune observation dans les trois corpus de référence ; la conversion HTML → Markdown produit systématiquement des destinations entre chevrons (hypothèse à confirmer par les tests sur corpus réels).
- Que se passe-t-il des schémas autres que `http`/`https` (`mailto:`, `tel:`, `ftp://`) ? Ils sont retirés comme toute destination entre chevrons (arbitrage clarify 2026-10-05, option A : une seule règle sans distinction de schéma) ; aucun n'est observé dans les corpus, et `--conserver-liens` reste la porte de sortie pour les conserver.
- Comment le système gère-t-il une URL nue dans une ligne conservée qui n'est pas une syntaxe de lien ? Elle n'est pas touchée (garde-fou, US2) — la passe ne vise que la sous-chaîne de destination qui suit un crochet fermant.
- Que se passe-t-il d'un lien absolu inséré dans une prose explicative légitime ? Il est retiré comme tout lien absolu : indistinguable mécaniquement d'un débris de navigation (risque assumé au stade decide) ; l'utilisateur qui veut le garder utilise `--conserver-liens`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le nettoyage appliqué à l'écriture de `nettoye.md` retire la destination de tout lien inline de la forme `](<...>)` (parenthèses et chevrons compris), quel que soit le schéma de la destination — relatif, `http`, `https`, ou tout autre (`mailto:`, `tel:`, `ftp://`…) ; le libellé du lien, y compris ses crochets `[libellé]`, et le reste du texte de la ligne restent inchangés. Exemples : `[Try Studio ](<https://console.mistral.ai?utm_source=docs>)` devient `[Try Studio ]` ; `[Contact](<mailto:contact@exemple.fr>)` devient `[Contact]`. Cette règle unifie et étend la règle `](</...>)` de la feature 004.
- **FR-002**: Pour les liens dotés d'un titre `[libellé](<url> "titre")`, le retrait emporte la destination et le titre (parenthèses, chevrons et guillemets compris) : seul le libellé `[libellé]` reste, conformément au principe « seul le libellé survit ». Exemple : `[Haut Conseil des finances publiques (HCFP)](<http://www.hcfp.fr/> "Haut Conseil ... \(nouvelle fenêtre\)")` devient `[Haut Conseil des finances publiques (HCFP)]`.
- **FR-003**: La passe s'applique par défaut à chaque run de nettoyage, à `nettoye.md` et à `nettoye-pagine.md` ; les marqueurs de page insérés par l'outil restent strictement inchangés.
- **FR-004**: Le drapeau `--conserver-liens` désactive l'ensemble du nettoyage des destinations (relatives et absolues) ; avec ce drapeau, les sorties sont identiques octet par octet à celles produites sans la feature.
- **FR-005**: La passe ne modifie ni la détection des motifs, ni les extraits, ni `suggestion.json`, ni `rapport-dry-run.md`, ni `cartographie.json`, ni les ids de motifs (M01… inchangés à option de détection égale).
- **FR-006**: La passe retire les destinations telles quelles, sans décoder les caractères encodés, sans réécrire ni réparer les URLs.
- **FR-007**: La passe ne touche aucune URL qui n'est pas la destination d'un lien inline : les URLs nues (dans le corps du texte ou dans un bloc de code) sont conservées intactes octet par octet.
- **FR-008**: Le comportement reste déterministe : deux runs sur la même entrée avec les mêmes options produisent des sorties identiques octet par octet.
- **FR-009**: La passe ne supprime aucune ligne (la suppression de lignes relève de la détection existante).

### Key Entities *(include if feature involves data)*

- **Destination de lien résiduelle**: sous-chaîne `(<...>)` terminant un lien inline Markdown, héritée de la conversion HTML → Markdown ; forme visée `](<...>)` sans distinction de schéma (relatif, `http(s)`, `mailto`, `tel`, `ftp`…), caractère `>` final non imbriqué. Entité purement textuelle, sans donnée persistée.
- **Titre de lien**: texte entre guillemets suivant la destination dans la parenthèse d'un lien inline Markdown (`(<url> "titre")`) ; distinct de la destination et du libellé, il est retiré avec la destination lors du nettoyage (arbitrage specify 2026-10-05 : seul le libellé survit).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Sur le run équivalent au 009 (entrée Exemple_3), aucune ligne de `nettoye.md` ne contient une destination de lien `](<` (baseline : 6 lignes sur 299 avec `](<http`).
- **SC-002**: Hors destinations et titres retirés, le texte des lignes conservées est inchangé ; le nombre et l'ordre des lignes de la sortie sont identiques à ceux d'un run avec la seule feature 004 sur la même entrée.
- **SC-003**: Sur Exemple_1 et Exemple_2, les sorties par défaut sont identiques octet par octet à celles des runs équivalents 004 (aucune destination absolue n'y survit à la détection).
- **SC-004**: Avec `--conserver-liens`, toutes les sorties (`nettoye.md`, `nettoye-pagine.md`) sont identiques octet par octet à celles produites sans la feature.
- **SC-005**: Sur un document construit contenant des URLs nues dans un bloc de code et dans le corps du texte, toutes ces URLs sont retrouvées intactes octet par octet dans la sortie.
- **SC-006**: Sur un document construit contenant des liens `(<url> "titre")` dans des lignes conservées, aucune URL ni aucun texte de titre n'apparaît en sortie et chaque libellé est retrouvé intact dans la sortie.
- **SC-007**: La suite de tests existante passe sans relâchement des seuils, complétée par les tests de la nouvelle passe (données Exemple_1, Exemple_2, Exemple_3 et documents construits).

## Assumptions

- Les formes à nettoyer sont exclusivement des destinations entre chevrons `](<...>)`, quel que soit le schéma (clarification 2026-10-05, option A) ; la conversion HTML → Markdown du pipeline de l'utilisateur produit systématiquement des chevrons (aucune forme `](https://...)` sans chevrons observée dans les trois corpus).
- Le drapeau `--conserver-liens` conserve sa signature actuelle (option booléenne sans argument) ; les codes retour (0/1/2/3) et le contrat CLI restent inchangés.
- Une seule règle textuelle déterministe au point d'application existant suffit ; aucune dépendance runtime nouvelle (conformité constitution v1.4.0 : local-first, stdlib, sorties dans `output/`).
- Les marqueurs de page `<!-- page: N -->` et les URLs éventuelles présentes dans les marqueurs ne matchent jamais la forme visée (à confirmer par test).
- Le cas du lien absolu légitime inséré dans une prose explicative (indistinguable d'un débris de navigation) est un manque assumé, couvert par `--conserver-liens` (decision.md) ; aucune analyse de contexte n'est tentée.
- Les contenus attendus des tests existants qui comparent les sorties resteront valides sur Exemple_1/Exemple_2 (aucun comportement observable attendu sur ces corpus) ; Exemple_3 devient corpus de test de la feature.
