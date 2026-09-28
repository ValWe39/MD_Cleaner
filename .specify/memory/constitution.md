<!--
Sync Impact Report - Constitution v1.0.0
=========================================
Version change: [empty template] -> 1.0.0 (MAJOR: initial adoption)
Added sections: Core Principles, Security & Privacy Requirements, Development Workflow, Additional Requirements, Governance
Modified principles: N/A (initial creation)
Removed sections: N/A
Follow-up TODOs: None
-->

# MD Cleaner Constitution

## Core Principles

### I. Isolation des secrets (NON NÉGOCIABLE)
Aucune clé API, token ou identifiant ne doit figurer dans le code source, la configuration, les tests ou tout fichier commité. Les identifiants sont chargés à l'exécution depuis des variables d'environnement ou un fichier de config local exclu par .gitignore. Seuls des placeholders (YOUR_API_KEY, DATA_DIR) sont autorisés dans les exemples.

Rationale: Prévenir les fuites de données sensibles via le contrôle de version et assurer la sécurité par défaut.

### II. Local-first & confidentialité (NON NÉGOCIABLE)
Toutes les données, résultats et logs restent sur la machine locale : pas de cloud, pas de base distante, pas de sync tiers. Le fonctionnement hors-ligne doit être possible pour les parties locales (parsing, stockage).

Rationale: Garantir la souveraineté des données et le respect de la vie privée des utilisateurs.

### III. Open-source & sans trackers
Toutes les dépendances d'exécution doivent être open-source et sans trackers/télémétrie. Licences permissives privilégiées (MIT, Apache-2.0, BSD) pour rester compatibles avec la licence MIT du projet.

Rationale: Assurer la transparence, l'auditabilité et la compatibilité avec la philosophie open-source du projet.

### IV. Simplicité (YAGNI)
Toute fonctionnalité au coeur de l'outil doit être justifiée. Pas d'abstraction prématurée, pas de plugins, pas de multi-tenant. Un point d'entrée CLI est préféré à un serveur web ou GUI.

Rationale: Maintenir un codebase minimal, maintenable et axé sur le besoin réel.

## Security & Privacy Requirements

### Secrets Management
Clés et tokens fournis uniquement via variables d'environnement ou config git-ignorée. Un template config.example.* avec placeholders peut être commité, jamais la config réelle.

### Path Isolation
Les répertoires de données et de résultats sont résolus depuis la config locale, jamais codés en dur. Les valeurs par défaut éventuelles doivent être des chemins relatifs ou des placeholders clairement marqués.

### No Cloud
Aucun upload, sync ou backup vers un service cloud n'est autorisé.

### No Trackers
Aucun SDK d'analytics, télémétrie ou crash-reporting n'est autorisé. Les dépendances sont auditées avant adoption.

### Network Surface
Les appels sortants sont limités à l'URL demandée par l'utilisateur. Aucun autre trafic sortant n'est autorisé.

### Data Retention
L'utilisateur contrôle la rétention en supprimant les fichiers du répertoire de sortie. Le tool ne doit conserver aucune copie cachée.

## Development Workflow

### Config Validation
Le tool doit valider au lancement que la configuration et les chemins requis sont présents et échouer rapidement avec un message clair. Interdiction de recourir à des défauts codés en dur pour les secrets ou chemins personnels.

### Commit Hygiene
Avant tout commit, vérification qu'aucune clé réelle ni chemin personnel n'est dans le diff. Le .gitignore doit couvrir les configs locales et répertoires de sortie.

## Additional Requirements

### Sovereign Tools Preference
Les outils et packages utilisés doivent, dans la mesure du possible, être souverains : création et hébergement en Europe ou en France.

## Governance

La Constitution prime sur toutes les autres pratiques et documents du projet. Tout amendement doit être documenté, approuvé et accompagné d'un plan de migration si nécessaire. La compliance avec cette Constitution doit être vérifiée pour chaque PR et review. Les principes marqués NON NÉGOCIABLE ne peuvent être modifiés qu'avec l'accord unanime de tous les mainteneurs.

**Version**: 1.0.0 | **Ratified**: 2026-09-28 | **Last Amended**: 2026-09-28
