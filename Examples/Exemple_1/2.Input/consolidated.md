## Page 1: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/1/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 1

# Qu'est-ce que le Model Context Protocol ?

Mis à jour le 29 juillet 2026 

## Un standard ouvert pour connecter l’IA au monde

Imaginez que vous demandiez à votre assistant de consulter vos tickets GitHub, de mettre à jour votre documentation Notion, puis de vérifier un paiement Stripe, sans jamais quitter la fenêtre de conversation. C’est précisément ce que rend possible le **Model Context Protocol** (MCP), un standard ouvert qui change la manière dont les modèles d’intelligence artificielle dialoguent avec les outils et services externes.

Avant le MCP, chaque plateforme d’IA implémentait ses propres méthodes pour brancher des outils. Une intégration écrite pour un framework devait être entièrement recodée pour un autre. L’écosystème était fragmenté et personne ne disposait d’un guide clair pour créer un outil, puis le partager d’un environnement à l’autre.

## Le problème que MCP résout

Le function calling traditionnel — la capacité d’un modèle à appeler des fonctions que vous lui décrivez — se heurte à quatre limites. La première est la fragmentation : un outil écrit pour un SDK n’est pas réutilisable ailleurs sans réécriture complète. La deuxième touche à la sécurité, puisque la gestion des clés d’API et des jetons d’authentification est laissée à chaque développeur, sans standard commun. Viennent ensuite la duplication et le manque d’interopérabilité : chaque équipe recode de zéro les mêmes intégrations, y compris pour des services aussi répandus que GitHub ou Slack, et rien ne permet de transmettre simplement un outil à un collègue ou de le déplacer vers un autre projet.

Le MCP répond à ces quatre points en définissant un protocole de communication standard entre un **client** , c’est-à-dire l’application d’IA, et un **serveur** , qui fournit les outils.

## Architecture client-serveur

Le client est l’application qui consomme les outils : dans cette formation, il s’agit du Chat de Mistral AI, mais ce peut être un SDK comme le Mistral Agent SDK, un IDE comme VS Code ou Cursor, ou tout autre logiciel compatible. Le serveur, lui, héberge les outils et les expose via le protocole ; il peut en proposer un seul ou une dizaine, chacun accompagné de sa description textuelle, de ses paramètres typés et de ses valeurs de retour.

Les deux échangent en JSON. Le client commence par interroger le serveur pour découvrir ce qu’il sait faire, puis appelle les outils voulus par des requêtes structurées. Voici le déroulé complet d’un appel, tel que vous le vivez côté utilisateur.

1

#### Requête utilisateur

Vous posez une question ou demandez une action dans Le Chat, par exemple : "Quels sont mes tickets ouverts sur GitHub ?"

2

#### Décision du modèle

Le modèle Mistral analyse votre requête et décide s'il doit appeler un ou plusieurs serveurs MCP pour y répondre.

3

#### Appel au serveur MCP

Le client (Le Chat) envoie une requête JSON au serveur MCP concerné, avec les paramètres identifiés par le modèle.

4

#### Exécution de l'outil

Le serveur exécute la fonction demandée (requête API GitHub, lecture de base de données, etc.) et retourne le résultat.

5

#### Réponse synthétisée

Le Chat reçoit les données du serveur et les intègre dans une réponse naturelle et contextualisée pour vous.

Ce cycle se répète autant de fois que nécessaire dans une même conversation. Le modèle peut enchaîner des appels vers plusieurs serveurs MCP pour mener une tâche composée : scanner Reddit pour repérer un problème signalé par des utilisateurs, vérifier ensuite sur Linear si un ticket existe déjà, puis ouvrir une pull request sur GitHub.

## MCP et function calling : complémentaires, pas concurrents

Une confusion revient souvent : le MCP ne remplace pas le function calling, il le prolonge. Avec le function calling, vous définissez les fonctions du côté client et le modèle détermine les paramètres à passer ; c’est direct et parfaitement adapté à un cas isolé, par exemple une fonction de calcul propre à votre application. Avec le MCP, les outils vivent sur un serveur distant et sont décrits de façon standardisée, ce qui devient déterminant dès que vous voulez partager, réutiliser ou combiner plusieurs outils.

L’avantage décisif tient en un mot : la portabilité. Un serveur MCP écrit pour Le Chat fonctionnera tel quel avec le Mistral Agent SDK, avec VS Code ou avec tout autre client compatible. Vous l’écrivez une fois, vous l’utilisez partout. Avant de poursuivre, identifiez les deux ou trois services que vous consultez le plus souvent dans votre travail : ce sont eux qui donneront le plus de valeur à vos premiers connecteurs.

## Points clés à retenir

  * MCP est un **standard ouvert** qui unifie la connexion entre les applications IA et les outils externes
  * Il repose sur une **architecture client-serveur** avec communication en JSON
  * Le protocole résout les problèmes de **fragmentation** , de **sécurité** et de **duplication** du function calling traditionnel
  * Un même serveur MCP peut être utilisé par **plusieurs clients** différents (Le Chat, SDK, IDE)
  * MCP et function calling sont **complémentaires** : MCP ajoute portabilité et standardisation



[Lecon suivante →MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

## Page 2: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/2/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 2

# MCP dans Le Chat de Mistral AI

Mis à jour le 29 juillet 2026 

## Le Chat : votre assistant IA augmenté par MCP

Le Chat, l’assistant conversationnel de Mistral AI, prend en charge nativement le protocole MCP : vous branchez vos outils et services professionnels directement dans l’interface de conversation, sans développement spécifique. Le Chat cesse alors d’être un simple agent conversationnel pour devenir une plateforme d’automatisation qui touche à l’ensemble de votre environnement de travail.

En avril 2026, il proposait déjà un répertoire fourni de connecteurs pré-intégrés, complété par la possibilité d’ajouter vos propres serveurs MCP. Cette double offre — le catalogue officiel d’un côté, l’ouverture totale de l’autre — en fait l’un des clients MCP les plus complets du marché.

## Le répertoire de connecteurs

L’onglet **Connectors** rassemble deux familles d’intégrations. La première regroupe les connecteurs en vedette, développés ou validés par l’équipe Mistral AI, ce qui garantit un niveau de fiabilité et de sécurité élevé. On y trouve GitHub pour les repositories, issues et pull requests, Notion pour la recherche et la création de pages, PayPal pour la consultation des transactions, Hugging Face pour les modèles, Spaces et datasets de la communauté IA, Linear pour la gestion de projet, Gmail pour la lecture et la gestion des emails via OAuth, Atlassian pour Jira et Confluence, et Box pour les fichiers stockés dans le cloud.

La seconde famille est celle des connecteurs personnalisés. Le Chat accepte n’importe quel serveur MCP distant : vous fournissez son URL, et il devient utilisable comme les autres. C’est la porte d’entrée vers vos API internes, vers des services de niche que personne n’a encore intégrés, ou vers des outils publiés par la communauté.

## Activer et gérer les connecteurs

Pour activer un connecteur du répertoire, la procédure tient en quatre étapes :

  1. Ouvrez l’onglet **Connectors** dans Le Chat
  2. Parcourez les connecteurs en vedette ou recherchez celui qui vous intéresse
  3. Cliquez sur **Connect** pour lancer le processus de connexion
  4. Selon le type d’authentification, fournissez un token, autorisez l’accès OAuth ou connectez-vous simplement



Le connecteur apparaît ensuite avec une icône activée dans votre barre d’outils. Vous pouvez le désactiver temporairement sans le supprimer, ce qui évite de tout reconfigurer à chaque changement de sujet.

Cette désactivation est loin d’être un détail cosmétique, car les connecteurs se gèrent **par conversation**. Travaillez-vous sur un projet GitHub ? Activez GitHub seul pour cette session. Passez-vous ensuite au tri de vos emails ? Coupez GitHub et activez Gmail. La raison est la même que pour tout système d’agents : le modèle choisit d’autant mieux l’outil pertinent qu’il en a moins sous les yeux. Une dizaine de connecteurs actifs simultanément brouille la sélection et produit des appels approximatifs.

En organisation, l’administrateur dispose de leviers supplémentaires. Il peut activer ou bloquer certains connecteurs pour l’ensemble de l’entreprise, et il garde une visibilité d’audit sur ce qui est actif dans les équipes. En revanche, l’authentification reste individuelle : le token GitHub de chaque membre est personnel et n’ouvre l’accès qu’à ses propres repositories, ce qui évite qu’une connexion partagée ne devienne une faille de gouvernance.

## L’interface en action

Quand un connecteur est actif, une petite icône d’outil s’affiche dans la zone de saisie. Un survol suffit pour voir la liste des outils disponibles dans la conversation en cours — réflexe utile avant de formuler une demande complexe.

Dès que le modèle décide d’utiliser un outil, l’interface vous montre le nom de l’outil appelé, les arguments envoyés au serveur en JSON, et deux boutons : **Allow** pour autoriser l’exécution, **Decline** pour la refuser. Cette validation humaine, le fameux « human in the loop », constitue la couche de sécurité principale : rien ne part vers vos systèmes sans que vous l’ayez vu passer. Une option **Always Allow** existe pour un outil auquel vous faites entièrement confiance, mais réservez-la à des actions de lecture ; l’activer sur un outil qui écrit dans un repository partagé revient à retirer le seul garde-fou dont vous disposiez.

## Fonctionnalités complémentaires et mobilité

Le MCP ne travaille pas seul dans Le Chat. Le mode **Canvas** prévisualise du code HTML, CSS ou Markdown et affiche un résultat visuel, par exemple une iframe Google Maps ou une page web générée à la volée. Les **Memories** , lancées en même temps que le support MCP, permettent au Chat de retenir des informations vous concernant pour personnaliser ses réponses, y compris en important vos préférences depuis d’autres assistants. L’**OCR** et le **speech-to-text** sont intégrés nativement : inutile de brancher un serveur MCP pour lire du texte dans une image ou transcrire un message vocal.

Enfin, tous les connecteurs disponibles sur le web fonctionnent aussi dans l’application mobile. Vérifier un ticket Jira dans les transports, consulter une page Notion avant une réunion ou déclencher un workflow depuis votre téléphone relève exactement du même usage que sur ordinateur.

## Points clés à retenir

  * Le Chat intègre nativement le protocole MCP avec un **répertoire de connecteurs** pré-intégrés
  * Vous pouvez ajouter des **connecteurs personnalisés** avec une simple URL
  * Les connecteurs se gèrent **par conversation** pour optimiser les performances du modèle
  * La **validation humaine** à chaque appel d’outil garantit la sécurité
  * Les administrateurs d’organisation contrôlent les connecteurs disponibles pour leur équipe
  * MCP fonctionne aussi sur l’**application mobile** de Le Chat



[← Lecon precedenteQu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)[Lecon suivante →Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

## Page 3: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/3/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 3

# Architecture Technique du MCP

Mis à jour le 29 juillet 2026 

## Comprendre les rouages du protocole

Utiliser un connecteur ne demande aucune connaissance technique. Le diagnostiquer quand il se comporte mal, choisir le bon mode d’authentification ou décider d’où héberger votre propre serveur suppose en revanche de savoir ce qui se passe sous le capot.

## Les modes de transport

Le protocole définit deux grandes familles de transport. La première, **STDIO** (Standard Input/Output), est destinée aux serveurs qui tournent sur la même machine que le client : la communication emprunte les flux d’entrée et de sortie standard du système d’exploitation. On la retrouve dans les outils en ligne de commande, l’accès au système de fichiers local et l’intégration d’applications de bureau. L’avantage est évident — aucun réseau, exécution immédiate — mais la limite l’est tout autant : STDIO ne fonctionne qu’en local et reste inutilisable avec Le Chat, qui est un service cloud. C’est le mode privilégié des IDE comme VS Code ou Cursor, où le serveur s’exécute directement sur le poste du développeur.

La seconde famille, **Streamable HTTP** , est le standard actuel pour les serveurs distants. Elle a succédé au protocole SSE (Server-Sent Events), dont l’inconvénient majeur était d’exiger une connexion permanente entre le client et le serveur. Streamable HTTP s’en affranchit, ce qui le rend plus robuste et plus facile à mettre à l’échelle ; il convient aux services cloud, aux API tierces et aux outils partagés entre équipes, et expose son point d’accès à l’URL `/mcp`. Le SSE reste accepté par la plupart des clients, mais il est considéré comme déprécié et devrait disparaître dans les prochains mois : n’écrivez plus de nouveau serveur sur cette base.

Pour Le Chat, la conséquence est directe : application cloud, il ne dialogue qu’avec des serveurs **distants** , et un serveur sur votre `localhost` n’a aucune signification pour lui. Si vous développez un serveur MCP et souhaitez le tester, deux voies s’offrent à vous — le déployer sur un service cloud, ou l’exposer temporairement avec une URL publique via un outil comme **ngrok**.

## Les mécanismes d’authentification

Trois niveaux de sécurité coexistent. Le plus simple est l’absence d’authentification : le serveur est accessible à quiconque connaît son URL, ce qui convient à des outils publics manipulant des données non sensibles, par exemple un serveur qui récupère des informations publiques sur Reddit ou qui renvoie la météo.

Le deuxième niveau repose sur un **token d’accès** que vous générez depuis le service concerné, avec un périmètre de droits précis — lecture seule, écriture, accès à certains repositories. Le connecteur GitHub en est l’illustration typique : vous créez un Personal Access Token en cochant exactement ce que Le Chat pourra faire, lire vos repos, créer des issues, ouvrir des pull requests. Ce token est stocké de manière sécurisée et rattaché à votre compte utilisateur, jamais à l’organisation.

Le troisième niveau, **OAuth 2.0** , offre l’intégration la plus aboutie. Plutôt que de manipuler un token à la main, vous autorisez Le Chat à accéder à votre compte via un flux standardisé. Sur le connecteur Linear, un clic sur « Connect » ouvre une fenêtre d’autorisation ; une fois confirmée, Le Chat obtient des droits complets sur votre compte et vous pouvez les révoquer à tout instant. Le bénéfice est double : aucune manipulation manuelle de secret, et une révocation immédiate en cas de doute.

## Architecture multi-serveurs

Dans la pratique, Le Chat ne parle jamais à un seul serveur mais à plusieurs simultanément, chacun apportant ses propres outils, prompts et ressources. Lorsqu’un serveur est activé, Le Chat lui envoie d’abord une requête de découverte, à laquelle le serveur répond en décrivant textuellement chaque outil disponible :
    
    
    {
      "name": "get_weather",
      "description": "Retourne la météo pour une position donnée",
      "parameters": {
        "latitude": { "type": "float", "description": "Latitude" },
        "longitude": { "type": "float", "description": "Longitude" }
      },
      "returns": "string"
    }

Cette description est le seul élément dont le modèle dispose pour décider quand et comment employer l’outil. Un `description` vague comme « fait des choses avec les données » condamne l’outil à ne jamais être appelé au bon moment. Les créateurs de serveurs MCP doivent donc soigner autant la formulation que le typage et les exemples.

À chaque message, le modèle déroule ensuite une boucle décisionnelle : il analyse la requête, détermine si un ou plusieurs outils sont nécessaires, sélectionne le plus pertinent et prépare ses arguments, envoie la requête au serveur et attend le résultat, puis décide s’il faut appeler autre chose ou s’il peut formuler sa réponse, avant de synthétiser le tout en langage naturel. Cette boucle peut tourner plusieurs fois et solliciter des serveurs différents au sein d’une même conversation.

## Considérations de performance

Deux facteurs conditionnent la qualité de l’expérience. Le premier est le nombre d’outils : comme tout système d’agents, le modèle perd en précision quand la liste s’allonge. N’activez que les connecteurs utiles à la tâche du moment, coupez ceux dont vous n’avez plus besoin, et préférez des outils spécifiques et bien décrits à des outils génériques. Le second est la latence : chaque appel MCP est une requête réseau, dont le coût dépend de la localisation et des performances du serveur. Sur un workflow critique, choisissez des serveurs optimisés et géographiquement proches.

## Points clés à retenir

  * Le Chat utilise le mode **Streamable HTTP** pour communiquer avec les serveurs MCP distants
  * Trois niveaux d’authentification sont supportés : **aucune** , **token** et **OAuth 2.0**
  * Le Chat peut se connecter à **plusieurs serveurs MCP** simultanément
  * Le modèle utilise les **descriptions textuelles** des outils pour décider quand les utiliser
  * Limitez le nombre de connecteurs actifs pour optimiser la **précision** du modèle



[← Lecon precedenteMCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)[Lecon suivante →Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

## Page 4: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/4/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 4

# Connecteur GitHub

Mis à jour le 29 juillet 2026 

## GitHub directement depuis Le Chat

GitHub est l’une des intégrations MCP les plus puissantes du répertoire du Chat. Elle donne accès à vos repositories, issues, pull requests et branches sans quitter la conversation. Pour une équipe de développement, l’économie n’est pas anecdotique : les tâches courantes — trier des issues, ouvrir une PR, vérifier un fichier sur une branche — cessent d’imposer un aller-retour vers l’interface web ou un rappel de la bonne commande Git.

## Connexion et authentification

Le connecteur s’authentifie par **Personal Access Token** (PAT). La configuration se déroule en quatre temps :

  1. Rendez-vous sur GitHub dans **Settings > Developer settings > Personal access tokens**
  2. Créez un nouveau token en sélectionnant les scopes nécessaires (repositories, issues, pull requests, etc.)
  3. Dans Le Chat, ouvrez l’onglet **Connectors** et sélectionnez GitHub
  4. Collez votre token et validez



Le token est stocké de manière sécurisée et rattaché à votre seul compte utilisateur. Si vous appartenez à une organisation sur Le Chat, vos collègues ne le voient pas et ne peuvent pas s’en servir : chacun se connecte avec ses propres identifiants, et le périmètre visible par Le Chat est exactement celui de la personne connectée.

Le choix des scopes mérite quelques secondes de réflexion. Voici les principaux :

  * **repo** : accès complet aux repositories (lecture, écriture, création de branches et PRs)
  * **read:org** : lecture des informations d’organisation
  * **write:discussion** : participation aux discussions
  * **admin:repo_hook** : gestion des webhooks (rarement nécessaire)



Appliquez le principe de moindre privilège : commencez avec des droits limités, quitte à régénérer un token plus large le jour où un usage précis le justifie. Un PAT `repo` complet donné pour simplement consulter des issues est un risque gratuit.

## Ce que le connecteur sait faire

Une fois branché, Le Chat couvre quatre domaines. Sur la consultation d’abord, il liste vos repositories et leurs branches, affiche le contenu d’un fichier donné, parcourt l’historique des commits et vérifie le statut des checks CI/CD. Sur les issues, il liste celles qui sont ouvertes, en crée avec titre, description et labels, commente les existantes et modifie leur statut.

Le travail sur les pull requests suit la même logique : lister les PR ouvertes, en créer une depuis une branche, consulter les diffs et les commentaires de review, puis fusionner. Enfin, sur le code lui-même, Le Chat crée une branche à partir d’une autre, crée ou modifie un fichier sur une branche précise et y pousse les changements. C’est cette dernière catégorie qui demande le plus de vigilance, puisqu’elle écrit dans le repository.

## Trois situations concrètes

Prenons une matinée ordinaire. Vous voulez faire le point sur les tâches en attente :

> “Montre-moi les issues ouvertes sur le repo company/backend qui ont le label ‘bug’ et sont assignées à personne.”

Le Chat appelle le connecteur, applique les filtres et vous présente une liste synthétisée. Vous enchaînez dans la même conversation pour assigner, labelliser ou commenter, sans jamais ouvrir GitHub.

Deuxième situation, vous venez d’identifier un manque dans la documentation et vous dictez le travail :

> “Crée un fichier docs/guide-migration.md sur la branche docs/migration du repo company/documentation avec un guide expliquant comment migrer de la v2 à la v3.”

Le fichier est créé sur la branche indiquée, et vous demandez dans la foulée l’ouverture de la pull request associée. Troisième situation, vous préparez une revue de code et souhaitez une vue d’ensemble avant d’entrer dans le détail :

> “Quelles sont les pull requests ouvertes sur company/frontend ? Donne-moi un résumé des changements pour chacune.”

Le Chat liste les PR, lit les diffs et produit un résumé structuré qui vous indique où concentrer votre attention.

## Deux réflexes à installer

Le premier concerne l’activation. Le connecteur GitHub expose beaucoup d’outils ; dans une conversation qui ne parle pas de code, désactivez-le. Vous constaterez que le modèle sélectionne plus sûrement l’outil pertinent lorsque sa liste est courte — c’est le même principe que pour n’importe quel système d’agents.

Le second concerne les écritures. À chaque fois que Le Chat propose de créer un fichier, une branche ou une pull request, l’interface affiche les arguments JSON avant exécution. Lisez-les. Vérifiez en particulier le nom de la branche cible, car une confusion entre `main` et une branche de travail se paie cher ; contrôlez ensuite le contenu du fichier créé ou modifié, puis le titre et la description de la PR.

## Le connecteur au sein d’un workflow

GitHub prend toute sa dimension combiné à d’autres connecteurs MCP. Un enchaînement type consiste à scanner un outil de support pour repérer un bug remonté par un utilisateur, vérifier sur GitHub si un ticket existe déjà, créer l’issue si ce n’est pas le cas, puis créer une branche, pousser un correctif et ouvrir la pull request. L’ensemble se pilote depuis Le Chat, chaque écriture restant soumise à votre validation.

## Points clés à retenir

  * Le connecteur GitHub utilise un **Personal Access Token** avec des scopes configurables
  * Vous pouvez **consulter, créer et modifier** des repositories, issues et pull requests
  * Chaque action d’écriture nécessite votre **approbation explicite** dans l’interface
  * **Désactivez le connecteur** quand vous ne l’utilisez pas pour améliorer la précision du modèle
  * La combinaison avec d’autres connecteurs MCP crée des **workflows automatisés** puissants



[← Lecon precedenteArchitecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)[Lecon suivante →Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

## Page 5: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/5/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 5

# Connecteur Notion

Mis à jour le 29 juillet 2026 

## Notion comme extension de votre assistant

Notion s’est imposé comme un point de centralisation pour la gestion des connaissances, la documentation d’équipe et l’organisation des projets. Le connecteur MCP correspondant permet d’interroger, de créer et d’organiser ce contenu depuis Le Chat. Le bénéfice est net pour les équipes dont la documentation vit entièrement dans Notion : au lieu de chercher une page, de l’ouvrir, de la lire puis de revenir à votre travail, vous posez la question et obtenez la réponse dans le fil de la conversation.

## Mise en place de la connexion

Le connecteur s’appuie sur un token d’intégration Notion. La configuration se déroule ainsi :

  1. Dans Notion, rendez-vous dans **Settings & Members > Connections** (ou créez une intégration via la page des développeurs Notion)
  2. Créez une nouvelle intégration interne et copiez le token généré
  3. Dans Notion, partagez les pages ou bases de données auxquelles vous souhaitez donner accès à l’intégration
  4. Dans Le Chat, ouvrez l’onglet **Connectors** , sélectionnez Notion et collez votre token



La troisième étape est celle qu’on oublie le plus souvent, et c’est la plus importante. Une intégration Notion ne voit que les pages et bases de données **explicitement partagées** avec elle : si votre première recherche ne renvoie rien alors que la page existe, le partage est presque toujours en cause. Ce mécanisme n’est pas une contrainte mais une garantie, puisqu’il vous laisse définir au cas par cas le périmètre que Le Chat pourra consulter.

## Ce que vous pouvez faire

La recherche est l’usage le plus fréquent. Une demande du type « Cherche dans Notion toutes les pages qui parlent de la migration vers la version 3 » déclenche une interrogation de l’API Notion, et Le Chat vous restitue les pages pertinentes accompagnées d’un résumé et des liens pour y accéder.

La création vient ensuite. Vous dictez du contenu structuré et le connecteur le matérialise au bon endroit, en respectant la structure de votre base de données :

> “Crée une nouvelle page dans la base de données ‘Documentation Technique’ avec le titre ‘Guide d’installation v3’ et ajoute une section sur les prérequis système.”

Restent les opérations d’organisation et de mise à jour, qui couvrent la modification des propriétés d’une page — statut, tags, assignation —, l’ajout de contenu à une page existante, le déplacement de pages entre sections et la mise à jour des champs d’une base de données. Ce sont elles qui permettent à Notion de rester à jour sans effort de saisie manuelle.

## Trois usages qui font gagner du temps

Le premier est le compte rendu de réunion. Vos notes brutes deviennent une page structurée en une seule instruction : « Crée une page de compte-rendu dans la section ‘Meetings’ de Notion avec la date d’aujourd’hui. Ajoute les décisions suivantes : migration prévue pour le 15 mai, responsable technique : Marie, budget approuvé. » Le deuxième est la documentation technique écrite au fil de l’eau, pendant que le contexte est encore frais :

> “Dans la page ‘Architecture API’ de Notion, ajoute une section décrivant le nouveau endpoint /api/v3/users avec les paramètres attendus et les codes de retour.”

Le troisième relève de l’entretien de la base de connaissances, et il illustre bien la capacité du modèle à conditionner son action : « Cherche dans Notion s’il existe déjà une page sur le processus d’onboarding. Si oui, montre-moi son contenu. Si non, crée-en une avec un template de checklist d’onboarding. » Le Chat commence par chercher, puis choisit entre lire et créer selon ce qu’il trouve.

## Combiner Notion avec d’autres connecteurs

C’est en croisant les sources que Notion révèle son intérêt. Associé à GitHub, il sert à documenter les décisions techniques prises dans les pull requests. Associé à Linear ou à Jira, il maintient la cohérence entre la roadmap de l’outil de gestion de projet et la documentation. Utilisé seul, il transforme des notes brutes en documentation présentable grâce à la capacité de rédaction du modèle Mistral.

Un exemple de workflow croisé donne la mesure de ce que cela permet :

> “Regarde les issues fermées cette semaine sur GitHub pour le repo company/api. Crée une page de synthèse dans Notion avec un résumé de chaque correction apportée.”

Le Chat interroge d’abord GitHub, agrège les issues fermées, puis rédige et publie la page Notion correspondante. Ce qui prenait une demi-heure de copier-coller devient une phrase et une validation.

## Bonnes pratiques

La qualité des résultats dépend directement de la structure de votre espace. Privilégiez les **bases de données** aux pages libres pour tout contenu structuré, et nommez explicitement vos pages et sections : le modèle s’appuie sur ces intitulés pour retrouver l’information, et une page baptisée « Notes diverses 3 » restera invisible dans les faits.

Limitez ensuite le périmètre partagé. Donner accès à l’intégralité de votre espace Notion dégrade la sécurité, mais aussi la pertinence des recherches, qui remontent alors des pages obsolètes ou hors sujet. Sélectionnez les bases et pages réellement utiles. Enfin, comme pour tout connecteur, Le Chat affiche les arguments de chaque appel avant exécution : relisez ce qui va être créé ou modifié, en particulier lorsque la page est visible par toute l’équipe.

## Points clés à retenir

  * Notion se connecte via un **token d’intégration** avec un périmètre d’accès que vous contrôlez
  * Vous pouvez **rechercher** , **créer** et **modifier** des pages et bases de données depuis Le Chat
  * L’intégration ne voit que les pages **explicitement partagées** avec elle
  * Notion se combine puissamment avec **GitHub** , **Jira** et d’autres connecteurs pour des workflows croisés
  * Structurez votre espace Notion avec des **noms clairs** et des **bases de données** pour optimiser l’intégration



[← Lecon precedenteConnecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)[Lecon suivante →Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

## Page 6: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/6/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 6

# Connecteur Atlassian : Jira et Confluence

Mis à jour le 29 juillet 2026 

## La suite Atlassian dans Le Chat

Atlassian équipe des millions d’équipes avec deux produits complémentaires : **Jira** pour la gestion de projet et le suivi de tickets, **Confluence** pour la documentation collaborative. Le connecteur MCP Atlassian réunit les deux derrière une seule interface conversationnelle. Pour qui passe ses journées à suivre un sprint dans Jira tout en maintenant la documentation dans Confluence, l’intérêt est immédiat : les allers-retours permanents entre les deux applications disparaissent.

## Connexion à Atlassian

Ce connecteur utilise **OAuth 2.0** , ce qui rend la mise en route particulièrement directe :

  1. Dans Le Chat, ouvrez l’onglet **Connectors** et sélectionnez Atlassian
  2. Cliquez sur **Connect** — une fenêtre d’autorisation Atlassian s’ouvre
  3. Connectez-vous à votre compte Atlassian et autorisez l’accès
  4. Le Chat reçoit automatiquement les droits nécessaires pour interagir avec vos projets Jira et espaces Confluence



Aucun token à générer, aucun secret à copier-coller, et des droits qui correspondent exactement à ceux de votre compte Atlassian. C’est également le point fort de cette approche du point de vue de la gouvernance : si un projet Jira vous est fermé, il l’est aussi pour Le Chat, sans configuration supplémentaire ni risque d’élargissement involontaire du périmètre.

## Travailler avec Jira

La consultation est l’usage d’entrée. Vous interrogez l’état de vos projets en langage naturel — « Quels sont les tickets en cours dans le sprint actuel du projet BACKEND ? » ou « Montre-moi tous les bugs critiques non assignés dans le projet MOBILE. » — et Le Chat interroge l’API Jira, filtre puis synthétise le résultat au lieu de vous renvoyer une liste brute.

La création suit la même logique conversationnelle. Plutôt que d’ouvrir un formulaire et de remplir sept champs, vous décrivez le ticket voulu :

> “Crée un ticket Jira dans le projet BACKEND avec le titre ‘Optimiser les requêtes SQL du dashboard’, priorité medium, et ajoute une description détaillant le problème de performance observé.”

La modification fonctionne de la même manière, et c’est souvent là que le gain de temps est le plus sensible, parce qu’il s’agit de micro-actions répétées vingt fois par semaine : « Passe le ticket BACKEND-142 en statut ‘In Review’ et ajoute un commentaire indiquant que les tests unitaires sont passés. » Enfin, sur le pilotage de sprint, une question comme « Quels tickets du sprint 23 ne sont pas encore terminés ? Donne-moi un résumé de l’avancement. » remplace la fabrication manuelle d’un point d’étape.

## Travailler avec Confluence

Un espace Confluence accumule fréquemment plusieurs années de documentation, dont une partie que plus personne ne sait retrouver. La recherche assistée répond à ce problème : « Cherche dans Confluence la documentation sur l’architecture de notre API de paiement. » La création de pages, elle, sert surtout à capitaliser juste après l’événement, quand les informations sont encore fraîches :

> “Crée une page Confluence dans l’espace ‘Engineering’ avec un compte-rendu de la rétrospective du sprint 23. Inclus les points positifs, les axes d’amélioration et les actions décidées.”

La mise à jour complète le tableau. Confluence étant collaboratif, une documentation qui vieillit devient rapidement dangereuse, car les équipes continuent de s’y fier. Une instruction du type « Mets à jour la page ‘Processus de déploiement’ dans Confluence pour ajouter l’étape de vérification des migrations de base de données avant le déploiement en production. » abaisse suffisamment le coût de la mise à jour pour qu’elle soit effectivement faite.

## Trois scénarios complets

En fin de sprint, la revue devient une question unique : « Fais un résumé de tous les tickets terminés dans le sprint 23 du projet BACKEND. Pour chaque ticket, indique le titre, l’assignee et le type (feature, bug, chore). » Le Chat interroge Jira et vous restitue un tableau synthétique exploitable tel quel en réunion.

En situation d’incident, la vitesse prime et le connecteur permet d’ouvrir le ticket sans quitter le canal de coordination : « Crée un ticket Jira de type ‘Incident’ avec priorité critique dans le projet OPS. Titre : ‘Indisponibilité du service de paiement’. Assigne-le à l’équipe On-Call. »

Le troisième scénario croise les deux produits pour assurer la traçabilité, un travail rarement fait parce qu’il est fastidieux : « Prends les 5 derniers tickets résolus dans le projet API et crée une page Confluence récapitulative dans l’espace ‘Changelog’ avec un résumé de chaque correction. » Jira fournit la matière, Confluence reçoit la synthèse.

## Bonnes pratiques

Soyez précis dans vos demandes, car une instance Jira contient facilement plusieurs milliers de tickets. Trois éléments cadrent efficacement une requête :

  * Le **projet** concerné (clé du projet Jira)
  * Le **type de ticket** (bug, story, task, epic)
  * Les **filtres** souhaités (statut, priorité, assignee, sprint)



Gardez également en tête que vos droits dans Le Chat sont exactement vos droits Atlassian, ce qui simplifie beaucoup les discussions de sécurité avec votre équipe. Enfin, désactivez le connecteur dans les conversations qui ne concernent ni Jira ni Confluence : il expose de nombreux outils, et le modèle gagne en efficacité sur un périmètre réduit.

## Points clés à retenir

  * Le connecteur Atlassian utilise **OAuth 2.0** pour une connexion fluide à Jira et Confluence
  * Vous pouvez **consulter** , **créer** et **modifier** des tickets Jira depuis Le Chat
  * La **recherche** et la **création de pages** Confluence sont également supportées
  * Vos **droits d’accès** Atlassian s’appliquent identiquement dans Le Chat
  * Combinez Jira et Confluence pour des workflows de **documentation automatique**



[← Lecon precedenteConnecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)[Lecon suivante →Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

## Page 7: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/7/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 7

# Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks

Mis à jour le 29 juillet 2026 

## Un écosystème de connecteurs en expansion

GitHub, Notion et Atlassian couvrent l’essentiel des besoins d’une équipe technique, mais le répertoire du Chat va bien au-delà. Il s’étend à la gestion de fichiers, aux paiements, à l’écosystème de l’intelligence artificielle, à la gestion de projet et à l’analyse de données. Cette leçon fait le tour des connecteurs complémentaires et de ce que chacun apporte réellement au quotidien.

Connecteur| Fonction principale| Cas d’usage| Authentification  
---|---|---|---  
Box| Gestion de fichiers cloud| Recherche, lecture et organisation de documents d’entreprise| OAuth 2.0  
PayPal| Consultation de paiements| Vérifier des transactions, suivre des paiements reçus| OAuth 2.0  
Hugging Face| Accès à l’écosystème IA| Explorer des modèles, lancer des Spaces, utiliser des datasets| Token  
Asana| Gestion de projet| Suivre des tâches, créer des projets, assigner du travail| OAuth 2.0  
Databricks| Analyse de données et ML| Exécuter des requêtes SQL, consulter des pipelines de données| Token  
Gmail| Messagerie électronique| Lire, rechercher et gérer des emails| OAuth 2.0  
Stripe| Paiements et facturation| Consulter les paiements, gérer les abonnements, analyser les revenus| Token  
  
## Box : la gestion documentaire

Box est une plateforme de stockage de fichiers en cloud très répandue dans les grandes entreprises. Le connecteur MCP permet d’y rechercher des fichiers et dossiers par nom ou par contenu, de lire les documents stockés et de les organiser, c’est-à-dire de les déplacer, les renommer ou les classer. L’authentification passe par OAuth 2.0, et une fois connecté, Le Chat accède aux fichiers strictement selon vos permissions Box.

L’usage qui revient le plus souvent est la recherche dans une arborescence devenue trop profonde pour être parcourue à la main. Le second, plus intéressant encore, consiste à faire extraire par Le Chat les informations utiles d’un rapport PDF stocké dans Box, sans avoir à le télécharger ni à le lire en entier.

## PayPal et Stripe : le suivi financier

Ces deux connecteurs donnent une vue sur votre activité financière depuis la conversation. PayPal sert principalement à vérifier le statut d’un paiement et à consulter l’historique des transactions récentes. Stripe va un peu plus loin, avec le suivi des paiements, la gestion des abonnements et l’analyse des métriques de revenus.

Ils s’utilisent essentiellement en lecture, ce qui limite mécaniquement les risques : vous consultez, vous ne déclenchez pas de mouvement d’argent. Une question typique tient en une ligne :

> “Quels sont les paiements reçus via Stripe cette semaine pour un montant supérieur à 100 euros ?”

## Hugging Face : l’IA à portée de main

Pour les praticiens du machine learning, ce connecteur ouvre l’accès à l’écosystème le plus riche de la communauté IA. Vous y explorez les modèles en filtrant par tâche — classification, génération de texte —, vous interagissez avec les applications hébergées sur les Spaces, dont certaines sont elles-mêmes des serveurs MCP, et vous parcourez les datasets disponibles pour l’entraînement.

Retenez ce dernier point, car il resservira : Hugging Face Spaces est l’une des options recommandées pour héberger vos propres serveurs MCP, les Spaces sans GPU étant gratuits.

## Asana et Databricks

Asana est très implanté dans les équipes marketing, produit et opérationnelles, souvent là où Jira ne l’est pas. Le connecteur y liste les tâches d’un projet ou d’un workspace, crée de nouvelles tâches avec description, assignation et date d’échéance, met à jour le statut des tâches existantes et consulte les projets ainsi que leurs sections.

Databricks s’adresse aux équipes data. Il exécute des requêtes SQL sur vos tables, consulte les résultats de pipelines et vérifie le statut des jobs en cours — de quoi obtenir un chiffre en cours de discussion sans changer d’outil. Sa véritable puissance apparaît lorsqu’on l’associe à Asana, combinaison que nous détaillerons dans les leçons consacrées aux workflows automatisés.

## Choisir le bon connecteur

Le bon assemblage dépend de votre métier bien plus que du catalogue disponible. Une équipe de développement s’appuiera sur GitHub, Jira ou Linear, et Notion ou Confluence. Une équipe produit combinera Asana ou Jira avec Notion et Stripe ou PayPal. Une équipe data associera Databricks à GitHub et Notion. Côté marketing, Asana, Notion et Box couvrent l’essentiel, tandis qu’un freelance trouvera généralement son compte avec GitHub, Notion et Stripe.

Dans tous les cas, la règle vue précédemment reste valable : mieux vaut activer **2 ou 3 connecteurs pertinents** par conversation que d’ouvrir tout le catalogue. Prenez un instant pour établir votre propre triplet — c’est lui que vous garderez actif par défaut, et vous n’ajouterez les autres qu’à la demande.

## Le répertoire en constante évolution

Le catalogue de connecteurs MCP du Chat s’étoffe régulièrement, de nouveaux partenaires et de nouvelles intégrations arrivant au fil des mois. L’onglet **Connectors** reste la source à jour : consultez-le de temps en temps pour repérer les dernières additions, plutôt que de vous fier à une liste figée.

Et si l’outil dont vous avez besoin n’y figure pas encore, rien n’est bloqué : vous pouvez créer un **connecteur personnalisé** , sujet auquel la section suivante de cette formation est entièrement consacrée.

## Points clés à retenir

  * Le Chat propose des connecteurs pour la **gestion de fichiers** (Box), les **paiements** (PayPal, Stripe), l’**IA** (Hugging Face), la **gestion de projet** (Asana) et l’**analyse de données** (Databricks)
  * Chaque connecteur utilise son propre mode d’authentification (**OAuth 2.0** ou **token**)
  * Activez uniquement **2-3 connecteurs pertinents** par conversation pour optimiser les performances
  * Le répertoire s’enrichit régulièrement avec de **nouveaux partenaires**
  * Vous pouvez toujours créer un **connecteur personnalisé** si votre outil n’est pas encore supporté



[← Lecon precedenteConnecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)[Lecon suivante →Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

## Page 8: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/8/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 8

# Workflow Stripe + Linear : Automatiser le Support

Mis à jour le 29 juillet 2026 

## Connecter paiements et gestion de projet

Le MCP prend toute sa valeur lorsqu’une tâche traverse plusieurs outils. Nous prenons ici un scénario réel : lier **Stripe** , la plateforme de paiement, et **Linear** , l’outil de gestion de projet, pour automatiser le suivi des problèmes liés aux paiements. Au lieu de copier-coller des informations d’une application à l’autre, vous demandez à Le Chat d’orchestrer l’ensemble du processus dans une seule conversation : une intention exprimée une fois, exécutée sur deux services distincts.

## Le scénario

Imaginons que vous gériez un produit SaaS avec des paiements récurrents via Stripe, et qu’un client signale un problème de facturation. Le travail se décompose en quatre temps : vérifier le statut du paiement du client dans Stripe, identifier la nature du problème (échec de paiement, double facturation, remboursement en attente), créer un ticket dans Linear contenant toutes les informations pertinentes, puis l’assigner à l’équipe compétente avec la bonne priorité.

Sans MCP, ce processus impose d’ouvrir Stripe, de chercher le client, de copier les détails, d’ouvrir Linear, de créer le ticket manuellement et d’y recoller les informations — chaque transfert manuel étant une occasion de se tromper de montant ou de date. Avec MCP, une seule conversation suffit.

## Mise en place des connecteurs

Côté Stripe, ouvrez l’onglet **Connectors** dans Le Chat, sélectionnez Stripe et fournissez votre clé API — le mode restreint est recommandé, avec un accès en lecture sur les paiements et les clients — puis validez la connexion. Côté Linear, sélectionnez le connecteur dans le répertoire : Linear passe par OAuth 2.0, vous cliquez sur **Connect** et autorisez l’accès depuis votre compte Linear. Une fois la connexion établie, Le Chat a accès à vos équipes, à vos projets et à vos tickets.

## Le workflow en action

Tout commence par le diagnostic. Vous interrogez Stripe sur la situation du client :

> “Vérifie dans Stripe les derniers paiements du client avec l’email [[email protected]](</cdn-cgi/l/email-protection#99faf5f0fcf7edd9fce1f8f4e9f5fcb7faf6f4>). Y a-t-il des paiements échoués ou des remboursements en attente ?”

Le Chat consulte le connecteur Stripe, récupère l’historique des transactions et vous présente un résumé clair : montants, dates et statuts (réussi, échoué, remboursé). Vient ensuite l’analyse, qui reste une conversation ordinaire — vous exposez ce que vous voyez et vous demandez un avis :

> “Le dernier paiement de 49,99 euros a échoué le 28 mars. La carte du client a expiré. Que recommandes-tu comme action ?”

Le modèle synthétise les données et propose des actions : contacter le client pour qu’il mette à jour sa carte, créer un ticket pour le suivi interne, éventuellement accorder une prolongation d’accès. La troisième étape bascule dans l’écriture, et c’est là que la formulation devient déterminante :

> “Crée un ticket dans Linear dans le projet ‘Support Client’. Titre : ‘Échec de paiement - [[email protected]](</cdn-cgi/l/email-protection#51323d38343f25113429303c213d347f323e3c>) \- carte expirée’. Priorité : medium. Ajoute dans la description les détails du paiement échoué avec le montant et la date.”

Le Chat prépare les arguments JSON, vous les montre pour validation, puis crée le ticket dans Linear avec toutes les informations structurées. Le suivi se poursuit dans la même conversation, sans reformuler le contexte : « Assigne ce ticket à l’équipe Billing et ajoute le label ‘payment-failure’ » suffit pour que le ticket soit mis à jour directement dans Linear.

## Variantes du workflow

Ce scénario de base se décline facilement. En surveillance proactive, demandez la liste de tous les paiements Stripe échoués de la semaine et un ticket Linear par échec dans le projet Support, avec les détails du client et du paiement ; le modèle boucle et sollicite votre validation à chaque création. En réconciliation financière, vous croisez les sources : comparer les paiements Stripe de mars avec les tickets Linear marqués « resolved » dans le projet Billing révèle les échecs restés sans ticket de suivi — c’est précisément ce que deux connecteurs actifs dans une même conversation rendent possible. Pour un rapport d’équipe enfin, demandez un résumé hebdomadaire croisant Stripe et Linear : tickets créés, tickets résolus, montant total impacté.

## Les limites à connaître

Chaque appel à un connecteur MCP prend quelques secondes, si bien qu’un workflow de cinq ou six appels sera plus lent qu’une action manuelle unique. Chaque action d’écriture demande par ailleurs votre approbation : c’est une sécurité, mais elle rend impossible une automatisation entièrement silencieuse. Enfin, pour des opérations massives — créer cinquante tickets d’un coup —, le processus devient long, et un script dédié au traitement en lot reste préférable.

## Points clés à retenir

  * Le workflow Stripe + Linear automatise le **diagnostic de paiement** et la **création de tickets** en une seule conversation
  * Chaque étape est **validée par l’utilisateur** avant exécution
  * Ce pattern se généralise à toute combinaison de connecteurs : diagnostic dans un outil, action dans un autre
  * Les workflows MCP sont idéaux pour les **tâches ponctuelles et semi-automatisées** , pas pour le traitement massif en lot
  * La clé du succès est d’être **précis dans vos requêtes** pour guider le modèle efficacement



[← Lecon precedenteAutres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)[Lecon suivante →Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

## Page 9: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/9/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 9

# Workflows Multi-Outils

Mis à jour le 29 juillet 2026 

## Chaîner les connecteurs pour des automatisations puissantes

La véritable force du MCP se révèle lorsque vous combinez plusieurs connecteurs au sein d’une même conversation. Plutôt que d’utiliser chaque outil isolément, vous créez des chaînes d’actions où la sortie de l’un alimente l’entrée du suivant. Un connecteur seul remplace un onglet ; trois connecteurs chaînés remplacent une procédure.

## GitHub + Notion : du code à la documentation

L’association la plus naturelle relie GitHub, où se trouve le code, et Notion, où se trouve la documentation. Le cas le plus rentable est le changelog automatique : vous demandez à Le Chat de regarder les pull requests fusionnées cette semaine sur `company/backend` et de créer, pour chacune, une entrée dans la page « Changelog Mars 2026 » de Notion avec le titre de la PR, l’auteur et un résumé des changements. Le Chat liste d’abord les PR fusionnées, puis rédige le contenu structuré dans Notion — le changelog est à jour sans qu’aucune ligne n’ait été recopiée.

Le même principe sert à documenter les décisions techniques. En demandant de lire le fichier `décisions/ADR-042.md` du repo `company/architecture` et d’en tirer une page Notion dans l’espace « Architecture » résumant la décision avec ses avantages et inconvénients, vous transformez un document réservé aux développeurs en une page lisible par toute l’équipe. Troisième variante, le suivi de dette technique : listez les issues GitHub du repo `company/api` portant le label `tech-debt` et ouvertes depuis plus de trente jours, et faites-en un tableau récapitulatif dans la page « Dette Technique Q1 ».

## Asana + Databricks : de la donnée à l’action

Cette combinaison intéresse les équipes data et produit, qui doivent traduire des analyses en actions concrètes. Prenons une alerte sur les métriques :

> “Exécute une requête SQL sur Databricks pour vérifier le taux de conversion de la dernière semaine. Si le taux est inférieur à 2%, crée une tâche Asana dans le projet ‘Growth’ avec le titre ‘Investiguer la baisse du taux de conversion’ et les chiffres dans la description.”

Le Chat sert ici de pont entre vos données et votre gestion de projet : il détecte l’anomalie dans Databricks et ouvre la tâche de suivi dans Asana. Le même pont vaut pour les rapports de sprint data — récupérer les résultats du pipeline de recommandation (précision, recall, latence p99) et créer une tâche « ML Ops » avec un résumé de performance et une recommandation sur la mise en production — ou pour les audits de qualité : vérifier la table `users` (doublons, champs vides, dates incohérentes) puis créer une tâche Asana par problème détecté, avec les détails et la sévérité.

## Jira + GitHub : le cycle de développement complet

Pour les équipes qui pilotent avec Jira et développent sur GitHub, le MCP fluidifie les deux extrémités du cycle. À l’ouverture, vous partez du ticket : consulter BACKEND-245 dans Jira, créer une branche `feature/BACKEND-245` sur `company/backend` à partir de `main`, puis commenter le ticket pour signaler que la branche existe. À la fermeture, vous partez du code : une fois la pull request #142 fusionnée, faites passer BACKEND-245 au statut « Done » et ajoutez-y un commentaire contenant le lien vers la PR. Les allers-retours entre les deux interfaces disparaissent.

## Patterns de workflows efficaces

Derrière ces exemples, trois structures reviennent. La plus courante est **« Diagnostic → Action → Documentation »** : interroger un outil pour comprendre la situation (Stripe, Databricks, GitHub), créer ou modifier un élément dans un outil de gestion (Linear, Jira, Asana), puis consigner le résultat dans un outil de knowledge management (Notion, Confluence). Presque tous les workflows métier se ramènent à cet enchaînement.

Le pattern **« Agrégation → Synthèse »** collecte des informations depuis plusieurs sources pour produire un résumé unifié, typiquement un point de situation demandant en une phrase les PR ouvertes sur GitHub, les tickets bloquants dans Jira et les derniers commentaires de la page « Sprint Planning » dans Notion. Le pattern **« Surveillance → Alerte »** vérifie un état et déclenche une action conditionnelle : vérifier les paiements échoués dans Stripe, et s’il y en a de nouveaux depuis hier, créer un ticket dans Linear et mettre à jour la page « Incidents Paiement » dans Notion.

## Conseils pour orchestrer des workflows complexes

Le modèle réussit nettement mieux quand vous décomposez explicitement les étapes plutôt que de tout demander en une phrase vague : « D’abord, consulte les issues GitHub du repo X. Ensuite, pour chaque issue critique, crée un ticket Jira. Enfin, fais un résumé dans Notion. » L’ordre est ainsi imposé, pas deviné. Pensez aussi à limiter les connecteurs actifs : pour un workflow à trois étapes impliquant trois outils, n’activez que ces trois connecteurs et désactivez le reste. Enfin, servez-vous de la validation humaine pour contrôler les données intermédiaires — si le diagnostic initial est faux, mieux vaut le corriger avant que le modèle ne crée une série de tickets erronés qu’il faudra ensuite supprimer un par un.

## Points clés à retenir

  * Les workflows multi-outils combinent **diagnostic** , **action** et **documentation** en une seule conversation
  * GitHub + Notion est idéal pour la **documentation automatique** du code
  * Asana + Databricks relie les **analyses de données** aux **actions de gestion de projet**
  * Décomposez vos workflows en **étapes séquentielles** pour guider le modèle efficacement
  * Activez uniquement les connecteurs **nécessaires** à votre workflow



[← Lecon precedenteWorkflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)[Lecon suivante →Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

## Page 10: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/10/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 10

# Bonnes Pratiques pour les Workflows MCP

Mis à jour le 29 juillet 2026 

## Structurer ses workflows pour la fiabilité

Vous maîtrisez désormais les connecteurs individuels et les workflows multi-outils. Reste ce qui sépare un workflow fragile d’un workflow fiable : la manière dont vous formulez vos instructions, ce que vous faites quand un appel échoue, la façon dont vous limitez les droits accordés et les réflexes qui réduisent la latence.

## Structurer ses prompts de workflow

Un workflow complexe doit être décomposé en instructions claires et séquentielles. Le modèle n’est pas un moteur d’automatisation classique : il interprète vos instructions en langage naturel, et l’imprécision se paie en résultats aléatoires. La différence saute aux yeux sur un même besoin. À éviter :

> “Gère tous les paiements échoués et crée les tickets nécessaires.”

À privilégier :

> “Étape 1 : Liste les paiements Stripe échoués depuis le 1er avril 2026. Étape 2 : Pour chaque paiement échoué, donne-moi le nom du client, le montant et la raison de l’échec. Étape 3 : Pour chaque cas, crée un ticket Linear dans le projet ‘Billing’ avec ces informations.”

La seconde formulation ne laisse rien à interpréter : la période est bornée, les champs sont nommés, le projet cible est explicite. Quand vous attendez un résultat structuré, exigez-le de la même façon — « Présente les résultats sous forme de tableau avec les colonnes : Client, Montant, Date, Raison de l’échec. » Le modèle gère aussi bien les instructions conditionnelles, ce qui vous évite de trier ensuite à la main : « Si le paiement échoué est supérieur à 500 euros, donne la priorité ‘urgent’ au ticket. Sinon, donne la priorité ‘medium’. »

## Gérer les erreurs

Un appel à un serveur MCP peut échouer pour des raisons étrangères à votre prompt : timeout réseau, token expiré, service temporairement indisponible. Quand un token a expiré, reconnectez-vous au connecteur depuis l’onglet Connectors ; les tokens OAuth se renouvellent généralement seuls, mais les tokens manuels comme un PAT GitHub doivent être régénérés. Un timeout signale le plus souvent une requête trop large — demander « tous les tickets Jira » dépasse les limites de l’API — et se corrige en reformulant plus précisément. Un service indisponible relève du tiers, pas de Le Chat : attendez quelques minutes et réessayez.

Les erreurs de logique sont plus insidieuses. Le modèle peut appeler le mauvais outil, par exemple Linear au lieu de Jira, envoyer des arguments incorrects — mauvais nom de projet, mauvaise branche — ou sauter une étape du workflow. Votre protection est la validation humaine : avant chaque action d’écriture, Le Chat vous montre les arguments, et il faut prendre le temps de les lire réellement. Si quelque chose ne correspond pas, cliquez sur **Decline** et reformulez.

Quand un workflow s’interrompt en cours de route, identifiez l’étape qui a échoué, corrigez la cause (token, formulation, paramètres) et reprenez à partir de cette étape, jamais du début — sans quoi vous recréerez des éléments déjà créés :

> “L’étape précédente a échoué parce que le projet Linear s’appelle ‘Customer-Support’ et non ‘Support Client’. Recommence la création du ticket avec le bon nom de projet.”

## Sécurité des données

Le principe du moindre privilège s’applique connecteur par connecteur. Un token GitHub ne doit ouvrir l’accès qu’aux repositories concernés, jamais à l’ensemble de votre compte. Sur Stripe, une clé en mode restreint limitée à la lecture suffit dès lors que vous n’avez pas besoin de modifier des paiements. Sur Notion, ne partagez avec l’intégration que les pages et bases de données pertinentes. Ces réglages prennent deux minutes et bornent définitivement l’étendue d’une erreur.

L’option « Always Allow » est tentante pour accélérer les workflows, mais elle supprime votre dernier rempart. Gardez-la désactivée pour toutes les actions d’écriture (création, modification, suppression), pour les connecteurs qui manipulent des données sensibles comme les paiements ou les emails, et pour les connecteurs personnalisés dont vous ne contrôlez pas le code source.

Un risque propre aux systèmes MCP mérite une vigilance particulière : l’injection de prompts via le contenu des outils. Un événement de calendrier peut contenir des instructions malveillantes cachées dans sa description ; si un connecteur MCP lit ce contenu, le modèle risque de les interpréter comme des consignes. La parade reste la même — vérifier les arguments avant de valider — et le signal d’alarme est une action inattendue de type envoi d’email ou extraction de données : refusez et investiguez. Ne faites pas non plus transiter dans vos prompts des mots de passe, des clés API, des données personnelles de clients (sauf via des connecteurs sécurisés et autorisés) ou des informations financières détaillées : ils pourraient être transmis à des serveurs MCP tiers.

## Optimiser ses workflows

Chaque appel MCP ajoute de la latence, et le cumul se ressent vite. Demandez plusieurs informations en un seul appel quand l’API le permet, évitez les boucles inutiles — n’interrogez pas les détails de chaque ticket un par un si vous pouvez les obtenir en lot — et posez des filtres précis pour limiter le volume des résultats. Structurez ensuite votre espace de travail en conversations dédiées, une par type de workflow, sans mélanger suivi financier et revue de code : vous n’activez que les connecteurs pertinents et vous gardez un contexte propre pour le modèle. Pour les routines répétées, conservez un template de prompt prêt à coller — « Routine quotidienne : 1) Vérifie les paiements Stripe échoués depuis hier. 2) Pour chaque échec, crée un ticket Linear dans ‘Billing-Ops’ avec priorité medium. 3) Résume le tout dans la page Notion ‘Journal Billing’. » Le gain n’est pas seulement du temps de frappe : un prompt éprouvé donne des résultats reproductibles.

## Points clés à retenir

  * **Décomposez** vos workflows en étapes claires et séquentielles pour guider le modèle
  * **Vérifiez** chaque action d’écriture via la validation humaine avant exécution
  * Appliquez le **principe du moindre privilège** sur les droits de chaque connecteur
  * **Limitez le nombre d’appels** MCP pour réduire la latence
  * Créez des **templates de prompts** réutilisables pour vos workflows récurrents
  * Restez vigilant face aux **injections de prompts** dans le contenu des outils



[← Lecon precedenteWorkflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)[Lecon suivante →Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

## Page 11: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/11/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 11

# Ajouter un Connecteur MCP Personnalisé

Mis à jour le 29 juillet 2026 

## Au-delà du répertoire officiel

Les connecteurs pré-intégrés couvrent de nombreux cas d’usage, mais votre entreprise utilise probablement des outils internes, des APIs propriétaires ou des services de niche qui ne figurent pas dans le répertoire de Le Chat. C’est là que les **connecteurs personnalisés** entrent en jeu : vous pouvez ajouter n’importe quel serveur MCP distant à Le Chat en fournissant simplement son URL. Le CRM maison développé il y a six ans devient alors utilisable dans une conversation, au même titre que GitHub ou Notion.

## Le processus d’ajout

L’ajout se fait en quelques clics depuis l’interface. Ouvrez l’onglet **Connectors** , cliquez sur **Add a custom connector** en bas de la liste, puis renseignez les informations demandées :

  * **Nom** : un nom descriptif pour identifier le connecteur (par exemple, « CRM Interne » ou « API Météo »)
  * **URL du serveur** : l’adresse publique de votre serveur MCP, avec le point d’accès `/mcp` (par exemple, `https://mon-serveur.example.com/mcp`)
  * **Description** : une description de ce que fait le connecteur (optionnel mais recommandé)
  * **Méthode d’authentification** : aucune, token ou OAuth 2.0



Cliquez enfin sur **Create** pour enregistrer le connecteur. Le Chat interroge alors automatiquement le serveur pour découvrir les outils disponibles : la liste des fonctions exposées s’affiche, et vous pouvez commencer à les utiliser dans vos conversations.

Cette requête de découverte retourne, pour chaque outil, son **nom** , sa **description** textuelle, les **paramètres** attendus avec leur nom, leur type et leur description, ainsi que le **type de retour**. Ce sont ces seules informations qui permettent au modèle Mistral de savoir quand et comment utiliser chaque outil — d’où l’attention que nous porterons, dans la leçon suivante, à la qualité de ces descriptions. Un outil bien écrit mais mal décrit reste invisible pour le modèle.

## Méthodes d’authentification

Le cas le plus simple est l’absence d’authentification : votre serveur MCP est accessible à quiconque connaît son URL. Cela convient aux outils publics qui ne manipulent pas de données sensibles, aux prototypes et démonstrations, et aux serveurs MCP qui encapsulent des APIs publiques. L’authentification par token consiste à fournir une clé qui sera envoyée avec chaque requête au serveur ; le token est stocké de manière sécurisée côté Le Chat. C’est le choix adapté aux APIs internes protégées par une clé API, aux serveurs qui doivent identifier l’appelant, et plus largement à tous les cas où vous souhaitez limiter l’accès. Vient enfin OAuth 2.0, le flux complet avec redirection vers la page d’autorisation du service : c’est le mécanisme le plus sécurisé, mais aussi le plus complexe à mettre en place côté serveur, et il fera l’objet d’un approfondissement dans de futurs guides de Mistral AI.

## Pré-requis pour votre serveur MCP

**Ce que Le Chat exige d'un serveur MCP**

  * Être accessible via une **URL publique** (pas de localhost)
  * Exposer un point d'accès au format **Streamable HTTP** (endpoint `/mcp`)
  * Répondre aux requêtes de **découverte d'outils** au format JSON standard MCP
  * Gérer correctement les **appels d'outils** et retourner les résultats au format attendu



La contrainte d’URL publique bloque en apparence le développement local, mais elle se contourne pendant la phase de mise au point. Si vous développez sur votre machine et souhaitez tester avec Le Chat avant de déployer, ouvrez un tunnel vers votre serveur local avec **ngrok** :
    
    
    ngrok http 8000

ngrok vous fournit une URL publique temporaire que vous pouvez utiliser comme URL de connecteur dans Le Chat. Cette approche est idéale pour le développement et les tests : vous modifiez votre code, vous relancez, et Le Chat voit immédiatement la nouvelle version sans aucun déploiement.

## Test avec le MCP Inspector

Avant même d’ajouter votre serveur à Le Chat, testez-le avec le **MCP Inspector** , un outil open source qui vérifie que votre serveur répond correctement aux requêtes de découverte, liste les outils disponibles avec leurs descriptions et paramètres, exécute des appels d’outils manuellement pour en contrôler les résultats, et vous aide à déboguer les problèmes de format ou de typage. Il se lance avec une simple commande npx :
    
    
    npx @modelcontextprotocol/inspector

L’Inspector ouvre une interface web locale où vous connectez votre serveur MCP et testez chaque outil individuellement. L’étape n’est pas une formalité : elle vous évite de consommer des messages de conversation pour du debugging, et elle isole clairement les erreurs de votre serveur des erreurs d’interprétation du modèle.

## Gestion organisationnelle

Si vous faites partie d’une organisation sur Le Chat, sachez que les connecteurs personnalisés que vous ajoutez sont visibles par les autres membres. L’administrateur peut désactiver l’un d’eux pour l’ensemble de l’organisation s’il le juge inapproprié ou non sécurisé. Chaque utilisateur doit en revanche fournir ses propres credentials — token ou OAuth — pour les connecteurs qui requièrent une authentification : partager le connecteur ne revient jamais à partager les accès.

## Sécurité des connecteurs personnalisés

Contrairement aux connecteurs officiels validés par Mistral AI, un connecteur personnalisé peut exécuter n’importe quel code côté serveur, et la description textuelle que vous voyez ne garantit en rien ce que le serveur fait réellement. Limitez-vous donc aux serveurs que vous avez développés vous-même, à ceux de collègues ou de partenaires de confiance, et aux serveurs open source dont vous avez vérifié le code. Même avec vos propres connecteurs, gardez la validation humaine activée pendant toute la phase de mise au point ; une fois que vous êtes certain que tout fonctionne, vous pourrez envisager d’« Always Allow » certains outils en lecture seule.

## Points clés à retenir

  * Vous pouvez ajouter n’importe quel serveur MCP distant comme **connecteur personnalisé** dans Le Chat
  * Le serveur doit être accessible via une **URL publique** avec un endpoint `/mcp`
  * Trois méthodes d’authentification sont supportées : **aucune** , **token** et **OAuth 2.0**
  * Utilisez **ngrok** pour tester votre serveur local avec Le Chat avant de le déployer
  * Le **MCP Inspector** est indispensable pour déboguer votre serveur avant intégration
  * N’ajoutez que des connecteurs de **sources fiables** et gardez la validation humaine activée



[← Lecon precedenteBonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)[Lecon suivante →Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

## Page 12: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/12/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 12

# Démo : Connecter Pokémon Showdown en MCP

Mis à jour le 29 juillet 2026 

## Apprendre par le jeu

Pour illustrer concrètement la création et l’utilisation d’un connecteur MCP personnalisé, nous prenons un cas ludique mais instructif : connecter **Pokémon Showdown** , le célèbre simulateur de combats Pokémon en ligne, à Le Chat via MCP. Ce cas d’étude, présenté par l’équipe Mistral AI lors de ses sessions live, met en œuvre des principes directement transposables à n’importe quelle intégration professionnelle. Le sujet est léger, les leçons techniques ne le sont pas.

## Le concept

Pokémon Showdown est une plateforme web où des joueurs s’affrontent dans des combats stratégiques au tour par tour. L’objectif du serveur MCP est de permettre à Le Chat de se connecter à la plateforme en tant que joueur, de lancer un défi contre un adversaire, d’analyser l’état du combat — Pokémon en jeu, PV, attaques disponibles — et de choisir la meilleure action à chaque tour. L’exercice est intéressant parce qu’il concentre quatre difficultés rarement réunies : communication en temps réel, gestion d’état, prise de décision séquentielle et guidage du modèle par les retours d’outils.

## Architecture du serveur MCP

Le serveur expose d’abord un outil `battle_player`, qui initie un combat. Il prend en paramètre un nom d’utilisateur et retourne un **identifiant de combat** unique, l’**état initial** du combat (Pokémon de chaque équipe, PV, etc.) et des **instructions** destinées au modèle sur les outils à appeler ensuite. Ce troisième élément n’a rien d’anecdotique : inclure des instructions de workflow dans les valeurs de retour d’un outil est un pattern avancé de conception MCP, et nous y revenons plus bas.

Vient ensuite l’outil d’action de combat. À chaque tour, Le Chat doit choisir entre attaquer, changer de Pokémon ou utiliser un objet. L’outil reçoit l’identifiant du combat, le type d’action et l’identifiant de l’attaque ou du Pokémon à envoyer, puis retourne le nouvel état du combat après l’action. Le cycle se répète jusqu’à la fin de la partie, chaque retour servant de point de départ à la décision suivante.

## Le pattern de guidage par retour

La leçon la plus importante de cette démo est le **guidage du modèle par les valeurs de retour**. Plutôt que de compter sur le seul prompt utilisateur pour diriger le workflow, le serveur MCP glisse les consignes dans ses réponses :
    
    
    Résultat : le combat a commencé. Votre Pokémon actif est Pikachu (PV : 100 %).
    L'adversaire a envoyé Dracaufeu.
    
    → Utilisez l'outil 'choose_move' pour sélectionner une attaque,
      ou 'switch_pokemon' pour changer de Pokémon.
      Attaques disponibles : Tonnerre, Surf, Vive-Attaque, Protection.

Le modèle n’a plus à deviner l’étape suivante : elle lui est indiquée, avec les options valides du moment. Le comportement final naît alors d’une **symbiose** entre le **prompt utilisateur** , qui porte l’intention générale (« joue un combat Pokémon »), les **descriptions d’outils** , qui disent quand et comment utiliser chaque outil, et les **retours d’outils** , qui précisent quel outil appeler ensuite et avec quels arguments.

Avant de connecter ce serveur à Le Chat, l’équipe Mistral le passe au MCP Inspector : vérifier que `battle_player` répond correctement avec l’état initial du combat, tester les actions de combat une à une, s’assurer que les instructions de guidage sont bien présentes dans les retours, et valider le format JSON des paramètres et des réponses. Dans un jeu au tour par tour, la moindre erreur de format interrompt la partie ; l’Inspector permet de déboguer sans consommer de messages de conversation.

## Principes applicables à vos projets

Le premier principe transposable est la **gestion d’état dans les retours**. Tout système qui évolue au fil des interactions — un processus de commande, un pipeline CI/CD, un workflow de validation — gagne à ce que le serveur retourne l’état actuel et les actions possibles à chaque étape. Un serveur MCP gérant des commandes retournerait ainsi l’état de la commande et les suites disponibles : valider le paiement, confirmer l’expédition, annuler.

Le deuxième est l’intégration des **instructions de workflow dans les retours** plutôt que dans le prompt utilisateur, où la logique serait longue à écrire et fragile à maintenir. Un serveur MCP de déploiement peut par exemple répondre, après une étape réussie : « Les tests sont passés. Utilisez l’outil ‘deploy_staging’ pour déployer en pré-production. »

Le troisième tient aux **descriptions claires et typées**. Chaque outil du serveur Pokémon possède une description précise, des paramètres typés et des valeurs de retour documentées, si bien que le modèle sait exactement ce que fait l’outil et quels arguments fournir. Appliqué au métier, cela signifie nommer explicitement (`create_invoice` plutôt que `process`), typer utilement (`user_email: string` plutôt que `user: string`) et décrire les retours attendus.

Le quatrième est la **décomposition en outils spécialisés**. Le serveur ne propose pas un unique outil « jouer_pokemon » qui gérerait tout : chaque action a son outil et sa responsabilité propre. De la même façon, préférez `start_order`, `add_item`, `confirm_payment` et `track_shipment` à un fourre-tout `manage_order`, plus difficile à décrire et donc plus souvent mal employé.

## Les limites du temps réel

La démo met aussi en évidence une limite actuelle : les serveurs MCP dans Le Chat ne supportent pas encore nativement les tâches longues ni le streaming en temps réel, chaque appel d’outil attendant une réponse synchrone. Pour les systèmes nécessitant des mises à jour continues, le contournement recommandé consiste à exposer un outil `start_task` qui lance l’opération et un outil `get_status` que l’utilisateur appelle pour vérifier l’avancement.

## Points clés à retenir

  * Le cas Pokémon Showdown illustre des **patterns MCP avancés** applicables à tout projet
  * Le **guidage par retour** d’outil est un pattern puissant pour orchestrer des workflows multi-étapes
  * Les **descriptions d’outils** , les **retours structurés** et la **décomposition en outils spécialisés** sont les clés d’un bon serveur MCP
  * Testez toujours avec le **MCP Inspector** avant d’intégrer à Le Chat
  * Les principes sont identiques pour un jeu ou pour un **processus métier** complexe



[← Lecon precedenteAjouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)[Lecon suivante →Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

## Page 13: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/13/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 13

# Créer et Déployer son Propre Serveur MCP

Mis à jour le 29 juillet 2026 

## De l’idée au serveur en production

Vous savez utiliser les connecteurs existants et ajouter un connecteur personnalisé. Il reste à franchir la dernière marche : écrire votre propre serveur MCP et le déployer pour l’exploiter dans Le Chat. Nous suivons ici le chemin complet, du premier fichier Python sur votre machine jusqu’à l’hébergement en production, en passant par les choix de conception qui feront la différence entre un serveur utilisable et un serveur que le modèle n’appellera jamais correctement.

## Créer un serveur MCP en local

La bibliothèque **FastMCP** est l’option la plus populaire en Python, parce qu’elle réduit le serveur à quelques décorateurs :
    
    
    from fastmcp import FastMCP
    
    mcp = FastMCP("Mon Serveur")
    
    @mcp.tool()
    def greet(name: str) -> str:
        """Salue une personne par son nom.
    
        Args:
            name: Le prénom de la personne à saluer.
    
        Returns:
            Un message de salutation personnalisé.
        """
        return f"Bonjour {name} ! Bienvenue sur notre plateforme."

Tout se joue dans ces quelques lignes. Le décorateur `@mcp.tool()` enregistre la fonction comme outil MCP. La docstring devient la description que le modèle voit pour décider s’il doit appeler l’outil — elle n’est donc pas un commentaire à destination de vos collègues, mais un élément fonctionnel. Le typage des paramètres (`name: str`) et du retour (`-> str`) informe le modèle sur les types attendus, et le nom de la fonction doit être clair et descriptif. L’alternative officielle est le SDK MCP d’Anthropic, disponible en Python et en TypeScript : il offre plus de contrôle au prix d’une configuration un peu plus lourde.

Puisque le modèle ne voit que la description textuelle de votre outil, écrivez-la comme une notice d’emploi complète :
    
    
    @mcp.tool()
    def search_products(
        query: str,
        category: str = "all",
        max_results: int = 10
    ) -> str:
        """Recherche des produits dans le catalogue.
    
        Utilisez cet outil quand l'utilisateur cherche un produit
        par nom, référence ou catégorie.
    
        Args:
            query: Termes de recherche (nom du produit, référence, mots-clés).
            category: Catégorie de filtre. Valeurs possibles : 'all',
                      'electronics', 'clothing', 'food'. Défaut : 'all'.
            max_results: Nombre maximum de résultats à retourner (1-50).
    
        Returns:
            Liste de produits avec nom, prix, disponibilité et référence.
        """

Remarquez ce que cette docstring apporte et que la précédente n’avait pas : la condition d’usage, les valeurs possibles de `category` et les bornes de `max_results`. Deux autres règles complètent l’exercice. Les noms doivent être explicites — préférez `search_products` à `search`, `create_invoice` à `create`, `get_user_orders` à `get_data`. Et les retours doivent être lisibles : renvoyez des textes compréhensibles plutôt que des identifiants bruts, faute de quoi le modèle ne pourra pas s’en servir pour formuler une réponse naturelle.

## Tester en local

Lancez d’abord le serveur, qui démarre sur un port local, par défaut `localhost:8000` :
    
    
    python server.py

Exposez-le ensuite pour que Le Chat puisse l’atteindre :
    
    
    ngrok http 8000

ngrok fournit une URL publique, par exemple `https://abc123.ngrok.io`, que vous utiliserez comme URL de connecteur dans Le Chat — en pensant à ajouter `/mcp` à la fin pour obtenir l’endpoint complet. Avant d’aller dans Le Chat, validez le serveur avec le MCP Inspector :
    
    
    npx @modelcontextprotocol/inspector

Connectez-vous à votre serveur local, listez les outils, testez-les individuellement et vérifiez les retours. Vous saurez ainsi si un éventuel problème vient de votre code ou de la façon dont le modèle interprète vos descriptions.

## Options de déploiement

Une fois le serveur au point, l’hébergement dépend surtout de vos contraintes. **Hugging Face Spaces** est l’option gratuite recommandée par l’équipe Mistral AI : ce sont des machines virtuelles qui hébergent des applications web, entièrement gratuites tant que vous n’avez pas besoin de GPU. Vous pouvez y monter votre serveur MCP avec FastAPI et déployer plusieurs serveurs sur le même Space, chacun avec son propre endpoint — `/api1/mcp`, `/api2/mcp` — que Le Chat ajoutera comme connecteurs distincts. Avantage supplémentaire, rien ne vous empêche d’ajouter au Space un frontend pour visualiser l’activité de vos serveurs.

**FastMCP Cloud** propose d’importer directement un repository GitHub contenant un serveur MCP : si le code est au bon format, le déploiement est quasi instantané. Pour les serveurs légers, sans dépendances lourdes, **Cloudflare Workers** offre un déploiement edge rapide et peu coûteux. Enfin, les fournisseurs classiques restent parfaitement viables pour les équipes déjà outillées : AWS (Lambda, ECS), Google Cloud (Cloud Run, Cloud Functions) ou Azure (Functions, Container Apps).

## Serveurs multi-outils ou mono-outil

Un réflexe fréquent consiste à découper très finement les outils. L’expérience va plutôt dans l’autre sens : un hackathon MCP organisé par Mistral a montré que les équipes les plus performantes concevaient des outils de haut niveau, correspondant à des workflows complets. Elles exposaient `book_restaurant` au lieu de `list_restaurants` \+ `check_availability` \+ `make_reservation`, ou `deploy_application` au lieu de `build` \+ `test` \+ `push` \+ `deploy`. Le modèle a moins d’occasions de se tromper d’enchaînement, et la latence cumulée diminue d’autant.

La granularité garde toutefois son intérêt dans trois situations : lorsque vous créez un serveur MCP générique utilisé par différentes équipes, lorsque les étapes du workflow peuvent servir indépendamment les unes des autres, et lorsque vous avez besoin de flexibilité dans l’ordre des opérations.

## Gestion des variables d’environnement

Vos serveurs auront souvent besoin de clés API, de credentials de base de données ou d’autres secrets. Stockez-les systématiquement dans des variables d’environnement, jamais dans le code. Gardez surtout à l’esprit qu’un serveur MCP public, sans authentification, fait consommer vos clés API par toute personne qui l’utilise : protégez-le avec un token ou OAuth dès qu’il appelle un service facturé. Sur Hugging Face Spaces, les **Secrets** du Space sont prévus exactement pour cela.

## Points clés à retenir

  * **FastMCP** est le moyen le plus simple de créer un serveur MCP en Python
  * Soignez les **descriptions** , les **noms** et le **typage** de vos outils
  * Testez d’abord en local avec **ngrok** et le **MCP Inspector** avant de déployer
  * **Hugging Face Spaces** offre un hébergement gratuit idéal pour les serveurs MCP
  * Préférez les outils de type **workflow** aux outils trop granulaires
  * Protégez vos **secrets** et envisagez une authentification pour vos serveurs



[← Lecon precedenteDémo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)[Lecon suivante →L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

## Page 14: https://corsen.ai/fr/formations/mistral-ai/le-chat-mcp/14/

Aller au contenu principal 

[CORSEN AI](</fr/>)

[Insights](</fr/insights/>)[Academy](</fr/formations/>)

[ EN](</> "English")

Nous Contacter

[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)

### Introduction au MCP

  * [1Qu'est-ce que le Model Context Protocol ?](</fr/formations/mistral-ai/le-chat-mcp/1/>)
  * [2MCP dans Le Chat de Mistral AI](</fr/formations/mistral-ai/le-chat-mcp/2/>)
  * [3Architecture Technique du MCP](</fr/formations/mistral-ai/le-chat-mcp/3/>)



### Connecteurs Pré-intégrés

  * [4Connecteur GitHub](</fr/formations/mistral-ai/le-chat-mcp/4/>)
  * [5Connecteur Notion](</fr/formations/mistral-ai/le-chat-mcp/5/>)
  * [6Connecteur Atlassian : Jira et Confluence](</fr/formations/mistral-ai/le-chat-mcp/6/>)
  * [7Autres Connecteurs : Box, PayPal, Hugging Face, Asana et Databricks](</fr/formations/mistral-ai/le-chat-mcp/7/>)



### Workflows Automatisés

  * [8Workflow Stripe + Linear : Automatiser le Support](</fr/formations/mistral-ai/le-chat-mcp/8/>)
  * [9Workflows Multi-Outils](</fr/formations/mistral-ai/le-chat-mcp/9/>)
  * [10Bonnes Pratiques pour les Workflows MCP](</fr/formations/mistral-ai/le-chat-mcp/10/>)



### Connecteurs Personnalisés

  * [11Ajouter un Connecteur MCP Personnalisé](</fr/formations/mistral-ai/le-chat-mcp/11/>)
  * [12Démo : Connecter Pokémon Showdown en MCP](</fr/formations/mistral-ai/le-chat-mcp/12/>)
  * [13Créer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)



### Conclusion

  * [14L'Avenir de l'Écosystème MCP](</fr/formations/mistral-ai/le-chat-mcp/14/>)



[Formations](</fr/formations/>)/[Mistral AI](</fr/formations/mistral-ai/>)/[Le Chat et MCP — Automatisez vos Workflows](</fr/formations/mistral-ai/le-chat-mcp/>)/Leçon 14

# L'Avenir de l'Écosystème MCP

Mis à jour le 29 juillet 2026 

## Un écosystème en pleine expansion

Le Model Context Protocol est encore jeune, mais son adoption s’accélère à un rythme remarquable. En quelques mois, MCP est passé d’un concept expérimental à un standard supporté par les principaux acteurs de l’IA : Mistral AI avec Le Chat, Anthropic avec Claude, OpenAI avec ChatGPT, ainsi que des IDE comme VS Code, Cursor et Windsurf. Quand des concurrents directs choisissent le même protocole d’intégration, c’est le signe d’un véritable standard industriel en train de s’imposer — et la garantie, pour vous, qu’un serveur écrit aujourd’hui restera utilisable demain.

## Ce que vous avez appris

Cette formation vous a d’abord donné les fondamentaux : le protocole MCP et son architecture client-serveur, les modes de transport avec STDIO pour le local et Streamable HTTP pour le distant, et les mécanismes d’authentification — aucune, token, OAuth 2.0. Sur cette base, vous savez activer et configurer les connecteurs pré-intégrés de Le Chat (GitHub, Notion, Atlassian, Box, Stripe, etc.), gérer les connecteurs par conversation comme au niveau de l’organisation, et vous appuyer sur la validation humaine pour garantir la sécurité.

Vous avez ensuite abordé les workflows avancés : combiner plusieurs connecteurs pour créer des automatisations multi-outils, appliquer le pattern « Diagnostic → Action → Documentation » et structurer des prompts assez précis pour que les résultats soient reproductibles. La dernière partie vous a fait passer du côté du développement, avec la création d’un serveur MCP sous FastMCP, les tests via le MCP Inspector et ngrok, le déploiement sur Hugging Face Spaces ou d’autres plateformes cloud, et les patterns avancés de guidage par retour d’outil.

## Les évolutions attendues du protocole

Aujourd’hui, les serveurs MCP échangent principalement du texte. Le support natif des **images** et de l’**audio** est en cours : des contournements existent déjà, comme les iframes via Canvas ou les liens vers des fichiers hébergés, mais la prise en charge directe simplifiera considérablement les cas d’usage multimédia.

Un projet prometteur, **MCP UI** , vise à permettre aux serveurs de fournir des interfaces utilisateur interactives directement dans le client. Au lieu de simples échanges texte-in/texte-out, un serveur pourrait afficher un formulaire, un tableau de bord ou une visualisation — de quoi rendre certains workflows nettement plus lisibles qu’une réponse en paragraphes.

Le support des tâches longues est l’évolution la plus attendue. Chaque appel d’outil attend aujourd’hui une réponse synchrone, ce qui interdit de fait la génération d’un rapport volumineux, une analyse de données ou un déploiement. Le support natif des tâches asynchrones permettra de lancer le traitement et de recevoir une notification à la fin. En parallèle, le protocole évolue vers **OAuth 2.1** pour les serveurs distants, avec des améliorations de sécurité significatives ; des guides détaillés sont prévus par les équipes Mistral AI pour accompagner cette transition. Enfin, l’introduction des **serveurs stateless** via Streamable HTTP simplifie le développement : chaque requête devient indépendante, ce qui supprime la gestion de sessions complexes et facilite le déploiement comme la montée en charge.

## Où trouver des serveurs MCP

La communauté grandit vite, et plusieurs répertoires recensent déjà les serveurs disponibles :

  * Le **répertoire de connecteurs de Le Chat** : les intégrations officielles validées par Mistral AI
  * Le **MCP Hub** : un répertoire communautaire de serveurs MCP open source
  * **Hugging Face Spaces** : filtrez par « MCP » pour découvrir des serveurs hébergés gratuitement
  * **GitHub** : de nombreux serveurs MCP y sont publiés en open source



Le mouvement fonctionne dans les deux sens. Si vous créez un serveur pour un service populaire, envisagez de le partager : la force du MCP repose sur la taille de son écosystème, et chaque serveur publié rend le protocole plus utile pour tous.

## Cas d’usage émergents

Les hackathons MCP organisés par Mistral AI ont révélé des usages inattendus. En éducation, des plateformes comme EduAdapt connectent Google Classroom via MCP pour permettre aux enseignants de générer du matériel pédagogique personnalisé et aux étudiants de poser des questions sur leurs cours. Côté gaming, des jeux comme Minecraft ou Clash Royale ont été intégrés pour créer des adversaires IA ou des assistants de jeu. Dans le domaine du fitness, la connexion à Strava permet de générer des itinéraires de course avec Google Maps et des plans d’entraînement personnalisés. Et en développement, des serveurs MCP chaînés orchestrent le cycle de vie logiciel complet, du code aux tests, du déploiement au monitoring.

## Recommandations finales

Si vous utilisez Le Chat au quotidien, explorez régulièrement le répertoire de connecteurs pour repérer les nouvelles intégrations, commencez par les connecteurs pré-intégrés avant d’en créer, gardez toujours la validation humaine activée pour les actions d’écriture et constituez-vous des templates de prompts pour vos workflows récurrents.

Si vous développez, partez d’un serveur simple d’un ou deux outils et itérez plutôt que de viser l’exhaustivité d’emblée. Investissez du temps dans les descriptions et la documentation de vos outils, car c’est là que se joue la qualité des appels. Testez systématiquement avec le MCP Inspector avant d’intégrer à Le Chat, puis partagez vos serveurs avec la communauté.

Si vous encadrez une équipe, définissez une politique de connecteurs MCP autorisés au sein de l’organisation et formez les membres à la validation humaine comme aux risques d’injection de prompts. Créez ensuite des serveurs MCP internes pour vos processus métier récurrents et documentez vos workflows, faute de quoi ils resteront la propriété de la seule personne qui les a écrits.

## Ressources pour aller plus loin

  * **Documentation Mistral AI** : guides officiels sur l’intégration MCP avec Le Chat et le SDK Agent
  * **Spécification MCP** : le protocole complet sur le site officiel MCP
  * **FastMCP** : documentation et exemples pour créer des serveurs MCP en Python
  * **Blog Mistral AI** : articles et annonces sur les nouvelles fonctionnalités MCP
  * **Chaîne YouTube Mistral AI** : enregistrements des sessions live sur MCP



## Points clés à retenir

  * L’écosystème MCP est en **croissance rapide** avec le support des principaux acteurs de l’IA
  * Des évolutions majeures arrivent : **multimodalité** , **interfaces UI** , **tâches asynchrones**
  * La communauté est active : explorez les **répertoires** et **partagez** vos créations
  * MCP transforme Le Chat en une **plateforme d’automatisation** capable de s’intégrer à l’ensemble de votre écosystème professionnel
  * Le meilleur moment pour commencer est **maintenant** : les outils sont matures, la documentation est disponible et la communauté est accueillante



## Testez vos connaissances

Connecteurs, workflows, serveurs maison : le tour MCP est complet.

1\. Que change MCP pour Le Chat ?

**Réponse :** Le Chat se connecte à vos outils (GitHub, Notion, Jira…) par un protocole standard : il lit et agit sur vos systèmes réels au lieu de raisonner en vase clos.

2\. Que permet un connecteur comme GitHub ou Atlassian ?

**Réponse :** Interroger et manipuler le service en langage naturel — issues, pages, tickets — avec les droits du compte connecté : l’outil devient une extension de la conversation.

3\. Qu'est-ce qu'un workflow multi-outils ?

**Réponse :** Un enchaînement où Le Chat combine plusieurs connecteurs — l’exemple Stripe + Linear du cours : détecter un problème de paiement et créer le ticket — l’orchestration en une conversation.

4\. Quelles bonnes pratiques pour des workflows MCP fiables ?

**Réponse :** Des demandes précises, des connecteurs limités au nécessaire, une validation humaine sur les actions qui engagent, et des tests sur les cas limites avant l’usage récurrent.

5\. Comment ajouter une capacité qui n'existe pas en connecteur ?

**Réponse :** En créant son propre serveur MCP (la démo Pokémon Showdown le prouve) puis en le branchant comme connecteur personnalisé — le protocole est ouvert, l’écosystème s’étend par vous.

Le protocole est jeune et l’écosystème grandit vite — mais la grille du cours (connecter, orchestrer, sécuriser, étendre) restera la bonne.

[← Lecon precedenteCréer et Déployer son Propre Serveur MCP](</fr/formations/mistral-ai/le-chat-mcp/13/>)

[← Dashboard](</fr/app/dashboard/>)Passer la certification officielle →

CORSEN AI

SASU · Paris, France · © 2026 CORSEN AI. Tous droits réservés.

[Insights](</fr/insights/>)[Mentions légales](</fr/legal/>)[Politique de confidentialité](</fr/privacy/>)[Cookies](</fr/cookies/>)[Accessibilité](</fr/accessibility/>)

[ EN](</> "English")

---

