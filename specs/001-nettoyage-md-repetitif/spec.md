# Feature Specification: Nettoyage de fichiers Markdown répétitifs

**Feature Branch**: `001-nettoyage-md-repetitif`

**Created**: 2026-09-29

**Status**: Draft

**Input**: User description: "Outil de nettoyage textuel de fichiers markdown multi-pages : repérer les éléments répétitifs (headers, footers, pagination, filtres, menus déroulants), ne garder que le contenu textuel de valeur, isoler ou recréer la pagination (commande optionnelle, en vue d'un futur RAG), déterministe, adapté à chaque fichier via calibrage (échantillon fourni ou auto-calibrage), dry-run avec suggestion par défaut, sortie dans un dossier output dédié."

## Clarifications

### Session 2026-09-29

- Q: Après un dry-run, comment l'utilisateur peut-il ajuster les motifs répétitifs détectés avant le nettoyage définitif ? → A: Option B — la suggestion par défaut est écrite dans un fichier éditable (liste des motifs avec extraits et fréquences) ; l'utilisateur peut y retirer ou ajouter des motifs, puis relancer le nettoyage qui consomme ce fichier.
- Q: Que devient le séparateur de pages explicite dans le fichier `.md` nettoyé simple, quand il est présent dans le document source ? → A: Option A — les séparateurs sont supprimés de la sortie simple ; la provenance (numéro de page, URL source) est conservée uniquement dans la cartographie annexe du run paginé.
- Q: Sous quel format la cartographie annexe contenu → page doit-elle être produite, sachant qu'elle sera consommée par un futur RAG ? → A: Option A — fichier structuré JSON : chaque entrée associe un identifiant de bloc de contenu, sa page d'origine et l'URL source.
- Q: À partir de quel seuil de fréquence d'apparition un motif est-il considéré comme répétitif par défaut ? → A: 80 % par défaut (majorité stricte haute), réglable par l'utilisateur via une commande optionnelle.
- Q: Qu'est-ce qui distingue concrètement le fichier `.md` nettoyé et paginé du fichier `.md` nettoyé simple, sachant que la cartographie machine vit déjà dans l'annexe JSON ? → A: Option A — le paginé inclut des marqueurs de pages lisibles (ex. un titre ou séparateur par page d'origine) en plus de l'annexe JSON ; le simple n'en contient pas.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Nettoyer un fichier Markdown multi-pages (Priority: P1)

Un utilisateur fournit un fichier `.md` consolidé de plusieurs pages (typiquement issu d'une conversion HTML → Markdown de pages web) contenant des éléments répétitifs sur chaque page : en-têtes de site, menus de navigation, filtres, fil d'Ariane, pieds de page. Il lance l'outil en ligne de commande sur ce seul fichier. L'outil analyse le document, détecte les motifs répétitifs, et produit un fichier `.md` nettoyé ne contenant que le contenu textuel de valeur, dans un dossier de sortie dédié.

**Why this priority**: C'est la fonctionnalité coeur de l'outil ; sans elle, rien d'autre n'a de valeur. Un run = un fichier (outil généraliste).

**Independent Test**: Peut être testé seul avec les fichiers des dossiers `Examples/Exemple_*/2.Input/consolidated.md` : le fichier nettoyé obtenu ne contient plus les blocs de navigation/footer répétés et conserve l'intégralité du contenu rédactionnel.

**Acceptance Scenarios**:

1. **Given** un fichier `.md` de 14 pages contenant un menu de navigation répété sur chaque page, **When** l'utilisateur lance l'outil sur ce fichier, **Then** un fichier `.md` nettoyé est produit dans un sous-dossier dédié du dossier de sortie, sans le menu de navigation, et avec tout le contenu rédactionnel conservé.
2. **Given** un fichier `.md` où un même pied de page apparaît sur au moins 80 % des pages, **When** l'outil s'exécute, **Then** ce pied de page est retiré de toutes les pages où il apparaît.
3. **Given** deux exécutions de l'outil sur le même fichier avec les mêmes options, **Then** les sorties sont identiques octet par octet (déterminisme).

---

### User Story 2 - Valider les éléments répétitifs détectés via dry-run (Priority: P2)

Avant de nettoyer pour de bon, l'utilisateur veut pouvoir vérifier ce que l'outil considère comme répétitif. L'outil produit en mode dry-run un rapport lisible par un humain listant les motifs répétitifs détectés (avec des extraits et leur fréquence d'apparition), accompagné d'une suggestion par défaut. L'utilisateur valide, ajuste ou accepte la suggestion, puis relance le nettoyage — ou saute directement le dry-run en acceptant la suggestion par défaut.

**Why this priority**: La confiance dans le nettoyage dépend de la transparence sur ce qui sera supprimé. Le dry-run est le mécanisme de validation humaine requis par la description, mais le nettoyage de base reste utilisable sans lui.

**Independent Test**: Peut être testé en lançant l'outil avec l'option dry-run sur un fichier d'exemple et en vérifiant que le rapport liste les motifs répétitifs connus (nav, footer, fil d'Ariane) sans modifier ni produire de fichier nettoyé.

**Acceptance Scenarios**:

1. **Given** un fichier `.md` multi-pages, **When** l'utilisateur lance l'outil avec l'option dry-run, **Then** un rapport des motifs répétitifs détectés est produit, avec extraits, fréquences et suggestion par défaut, et aucun fichier nettoyé n'est écrit.
2. **Given** le rapport de dry-run, **When** l'utilisateur relance l'outil sans dry-run (ou avec l'option de saut), **Then** le nettoyage applique la suggestion par défaut validée.

---

### User Story 3 - Obtenir une sortie paginée pour situer le contenu (Priority: P3)

En vue d'un développement ultérieur de RAG, l'utilisateur veut, via une commande optionnelle, que l'outil isole la pagination existante du document ou la recrée, afin que chaque bloc de contenu nettoyé reste localisable dans le document source (page d'origine). L'outil produit alors un second fichier `.md` nettoyé et paginé en plus du fichier nettoyé simple.

**Why this priority**: Utile pour le cas d'usage aval (RAG) mais non indispensable au nettoyage de base ; la valeur du contenu est déjà préservée par la Story 1.

**Independent Test**: Peut être testé sur un fichier d'exemple contenant des séparateurs de pages explicites : la sortie paginée associe chaque section nettoyée à un identifiant de page vérifiable.

**Acceptance Scenarios**:

1. **Given** un fichier `.md` contenant des séparateurs de pages explicites (ex. `## Page N: URL`), **When** l'utilisateur lance l'outil avec l'option de pagination, **Then** un fichier `.md` nettoyé et paginé est produit où chaque contenu est associé à sa page d'origine.
2. **Given** un fichier `.md` sans séparateurs explicites mais dont la structure révèle des frontières de pages, **When** l'option de pagination est active, **Then** l'outil recrée une pagination à partir des indices structurels, ou signale clairement qu'aucune pagination fiable n'a pu être établie.

---

### User Story 4 - Calibrer la détection sur un échantillon ou en auto-calibrage (Priority: P4)

Pour être plus précis, l'utilisateur peut fournir un échantillon des 5 premières pages (fichiers séparés) sur lesquels l'outil calibre sa détection de motifs répétitifs. À défaut, l'outil s'auto-calibre par défaut sur un extrait des N premières pages qu'il repère lui-même dans le document complet.

**Why this priority**: Améliore la précision mais l'outil doit fonctionner sans échantillon grâce à l'auto-calibrage ; c'est une optimisation de qualité de détection.

**Independent Test**: Peut être testé avec les dossiers `Examples/Exemple_*/1.Sample/` : le calibrage sur l'échantillon détecte au moins les mêmes motifs que l'auto-calibrage, idéalement davantage.

**Acceptance Scenarios**:

1. **Given** un document complet et un échantillon de 5 pages fournies par l'utilisateur, **When** l'utilisateur lance l'outil avec l'option d'échantillon, **Then** la détection est calibrée sur cet échantillon et appliquée au document complet.
2. **Given** un document complet sans échantillon fourni, **When** l'utilisateur lance l'outil sans option d'échantillon, **Then** l'outil s'auto-calibre sur un extrait des N premières pages du document et applique cette calibration à tout le document.

### Edge Cases

- Que se passe-t-il quand le fichier fourni ne contient qu'une seule page ou est très court (pas de répétition observable) ? L'outil doit le signaler et produire une sortie inchangée plutôt qu'un nettoyage arbitraire.
- Comment l'outil gère-t-il un motif répétitif contenant des parties variables (ex. un fil d'Ariane dont le numéro de leçon change à chaque page) ? Le motif doit être reconnu malgré ses parties variables.
- Comment l'outil gère-t-il un motif présent sur une partie seulement des pages (ex. un bandeau publicitaire sur 60 % des pages) ? Le seuil de fréquence par défaut (80 % des pages), réglable par commande optionnelle, détermine si le motif est supprimé ; les motifs sous le seuil restent visibles dans le dry-run pour décision humaine.
- Comment l'outil gère-t-il un document où presque tout est répétitif (résultat quasi vide) ? Le dry-run/rapport doit alerter l'utilisateur avant nettoyage définitif.
- Comment l'outil gère-t-il un fichier `.md` malformé ou vide ? Échec rapide avec un message clair, conformément à la validation de configuration de la constitution.
- Que se passe-t-il quand deux runs sur des fichiers différents produiraient des noms de sous-dossiers identiques (collision) ? Un suffixe distinct doit garantir l'unicité.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: L'outil DOIT accepter en entrée, via un point d'entrée en ligne de commande, un seul fichier `.md` par exécution.
- **FR-002**: L'outil DOIT détecter les motifs textuels répétés à travers les pages/sections du document : en-têtes de site, menus de navigation, filtres, menus déroulants, fils d'Ariane, pieds de page, éléments de pagination d'interface, et plus généralement tout bloc sans apport par rapport au contenu. Par défaut, un motif est considéré comme répétitif s'il apparaît sur au moins 80 % des pages ; l'utilisateur DOIT pouvoir régler ce seuil via une commande optionnelle.
- **FR-003**: L'outil DOIT reconnaître un motif répétitif même lorsque certaines de ses parties varient d'une page à l'autre (numéros de page, dates, numéros de leçon).
- **FR-004**: L'outil DOIT produire un fichier `.md` nettoyé ne conservant que les éléments textuels de valeur, sans altérer leur formulation, leur ordre ni leur hiérarchie de titres. Les séparateurs de pages explicites sont supprimés de la sortie simple ; la provenance (numéro de page, URL source) est conservée uniquement dans la cartographie annexe du run paginé.
- **FR-005**: L'outil DOIT être déterministe : des entrées et options identiques produisent une sortie identique, sans dépendance à l'heure, à des identifiants aléatoires ou à l'ordre de traitements non spécifiés.
- **FR-006**: L'outil DOIT créer par défaut un dossier de sortie et y insérer ses résultats dans un sous-dossier dédié, numéroté séquentiellement par défaut, ou nommé à partir des X premiers caractères du titre du document (option).
- **FR-007**: L'outil DOIT proposer un mode dry-run (commande optionnelle) produisant un rapport lisible listant les motifs répétitifs détectés (extraits, fréquence d'apparition, localisation) sans écrire de fichier nettoyé.
- **FR-008**: Le dry-run DOIT écrire la suggestion par défaut des motifs à supprimer dans un fichier éditable listant chaque motif avec son extrait et sa fréquence ; l'utilisateur peut y retirer ou ajouter des motifs, puis relancer le nettoyage, qui consomme ce fichier comme référence des motifs à supprimer. Ce mécanisme couvre aussi le cas où l'utilisateur saute le dry-run : la suggestion par défaut est alors appliquée directement.
- **FR-009**: L'outil DOIT proposer une commande optionnelle d'isolement ou de recréation de la pagination, produisant un fichier `.md` nettoyé et paginé en plus du fichier nettoyé simple. Le fichier paginé inclut des marqueurs de pages lisibles (ex. un titre ou séparateur par page d'origine), absents du fichier simple, et s'accompagne de l'annexe JSON de correspondance (FR-010), permettant de situer chaque contenu dans le document source.
- **FR-010**: La sortie paginée DOIT s'accompagner d'un fichier annexe de correspondance entre chaque bloc de contenu nettoyé et sa page d'origine (cartographie contenu → page), au format JSON structuré : chaque entrée associe un identifiant de bloc de contenu, sa page d'origine et l'URL source. Le `.md` paginé reste lisible et la donnée structurée de localisation vit à côté. L'outil DOIT garantir la cohérence entre les deux fichiers produits.
- **FR-011**: Lorsque le document comporte des séparateurs de pages explicites, l'outil DOIT s'appuyer sur eux en priorité. En leur absence, l'outil DOIT tenter une détection heuristique des frontières de pages (motifs récurrents de début/fin de page) et signaler explicitement que la pagination a été recréée par heuristique ; si aucune segmentation fiable ne peut être établie, l'outil DOIT le signaler clairement plutôt que de produire une pagination trompeuse.
- **FR-012**: L'outil DOIT proposer (commande optionnelle) un calibrage sur un échantillon des 5 premières pages fournies par l'utilisateur.
- **FR-013**: En l'absence d'échantillon fourni, l'outil DOIT s'auto-calibrer par défaut sur un extrait des N premières pages qu'il repère dans le document complet fourni.
- **FR-014**: L'outil DOIT fonctionner entièrement en local, sans accès réseau ni transmission de données, conformément aux principes de la constitution du projet (local-first, pas de cloud, pas de trackers, dépendances open-source).
- **FR-015**: L'outil DOIT valider au lancement la présence du fichier d'entrée et des chemins requis, et échouer rapidement avec un message clair en cas d'absence ou de fichier illisible.
- **FR-016**: L'outil DOIT signaler dans son rapport les cas limites : document trop court pour détecter des répétitions, motifs à fréquence partielle, sortie quasi vide.

### Key Entities *(include if feature involves data)*

- **DocumentSource**: fichier `.md` multi-pages fourni en entrée ; attributs : chemin, titre, taille, présence ou absence de séparateurs de pages explicites.
- **Page/Section**: subdivision du document source, explicite (séparateur `## Page N`) ou détectée ; porte le contenu à nettoyer.
- **MotifRépétitif**: bloc ou ligne récurrent à travers les pages, avec parties fixes et parties variables ; attributs : extrait représentatif, fréquence d'apparition, localisation, suggestion (supprimer/conserver).
- **ÉchantillonDeCalibrage**: ensemble optionnel de 5 pages fournies par l'utilisateur servant de référence de détection.
- **DocumentNettoyé**: fichier `.md` de sortie ne contenant que le contenu de valeur ; existe en variante simple et en variante paginée.
- **PaginationCarte**: correspondance entre les blocs de contenu nettoyés et leur page d'origine ; support de la sortie paginée et du futur RAG.
- **RunDeSortie**: sous-dossier du dossier output, numéroté ou dérivé du titre, regroupant les résultats d'une exécution.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Sur chacun des fichiers des dossiers `Examples/Exemple_*/2.Input/`, l'outil supprime au moins 90 % des lignes ou blocs répétitifs de boilerplate (navigation, footer, filtres) tout en conservant 100 % des lignes de contenu unique.
- **SC-002**: Deux exécutions successives avec les mêmes entrées et options produisent des sorties identiques octet par octet, vérifiable par comparaison de fichiers.
- **SC-003**: Un document de plusieurs centaines de pages (plusieurs Mo) est traité en moins d'une minute sur une machine de bureau standard.
- **SC-004**: Un utilisateur humain peut valider le rapport de dry-run d'un document d'exemple en moins de 5 minutes.
- **SC-005**: Aucune ligne de contenu rédactionnel unique n'est perdue lors du nettoyage (vérifiable par diff : toute ligne unique de l'entrée figure dans la sortie).
- **SC-006**: La sortie paginée permet de localiser sans ambiguïté chaque bloc de contenu nettoyé dans le document source (chaque contenu est associé à un identifiant de page).

## Assumptions

- Les fichiers d'entrée sont du texte Markdown, typiquement issus de conversions de pages web (HTML → Markdown), avec des motifs de boilerplate similaires à ceux des dossiers `Examples/`.
- Les fichiers consolidés peuvent comporter des séparateurs de pages explicites de la forme `## Page N: URL` ; leur présence n'est pas garantie pour tous les fichiers.
- L'outil est un outil en ligne de commande à un fichier par exécution ; les interfaces graphiques et le traitement par lots de plusieurs fichiers en une commande sont hors périmètre de cette version.
- Le dossier de sortie par défaut est un dossier `output` local au répertoire d'exécution ; l'utilisateur peut le configurer.
- Les documents fournis sont en français ou en anglais ; la langue du contenu n'influence pas la détection de motifs (approche structurelle, pas linguistique).
- Le futur RAG est un consommateur aval de la sortie paginée ; aucune fonctionnalité RAG n'est incluse dans ce périmètre.
- La conformité à la constitution du projet (secrets, local-first, open-source sans trackers, simplicité) est un prérequis non négociable appliqué à cette fonctionnalité.
- Les motifs répétitifs à fréquence partielle (présents sur une fraction des pages seulement) sont traités à partir d'un seuil de fréquence par défaut de 80 % des pages, réglable via une commande optionnelle, et signalés dans le dry-run.
