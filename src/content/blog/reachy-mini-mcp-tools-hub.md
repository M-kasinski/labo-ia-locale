---
title: "Reachy Mini branche MCP au Hub : des outils distants sans greffer du code au robot"
description: "Hugging Face ajoute des outils MCP hébergés dans Spaces à l’app conversationnelle de Reachy Mini. Un petit changement qui clarifie beaucoup l’architecture des agents locaux."
pubDate: 2026-06-07
category: "local"
tags: ["mcp", "agents", "auto-hebergement", "robotique"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Hugging Face — Adding MCP Tools to Reachy Mini"
    url: "https://huggingface.co/blog/adding-mcp-tools-to-reachy-mini"
  - label: "GitHub — pollen-robotics/reachy_mini_conversation_app"
    url: "https://github.com/pollen-robotics/reachy_mini_conversation_app"
  - label: "GitHub — pollen-robotics/reachy_mini SDK"
    url: "https://github.com/pollen-robotics/reachy_mini"
---

Hugging Face a publié le 3 juin 2026 un billet discret mais intéressant : l’application conversationnelle de **Reachy Mini** peut désormais utiliser des **outils MCP distants hébergés dans des Hugging Face Spaces**. Dit comme ça, cela ressemble à une note de release pour robot mignon. En réalité, c’est un bon cas d’école pour l’architecture des agents locaux : comment donner des capacités nouvelles à un assistant sans lui faire télécharger du code arbitraire, sans modifier l’application principale, et sans mélanger les outils matériels avec les services web.

Reachy Mini, côté Pollen Robotics, est présenté comme un robot open-source expressif pour hackers et builders IA. Son SDK et son application conversationnelle sont publics sur GitHub. L’app conversationnelle permet déjà de parler au robot, de lancer des mouvements, d’utiliser une caméra, de jouer des émotions ou des danses. Le changement annoncé par Hugging Face ajoute une troisième catégorie d’outils : après les outils intégrés au robot et les outils Python locaux personnalisés, des outils **MCP** peuvent être appelés à distance depuis le Hub.

## Ce qui change concrètement

Avant cette mise à jour, les outils de Reachy Mini étaient principalement locaux. Ils étaient faits pour le corps du robot : bouger la tête, déclencher une danse, jouer une émotion, activer le suivi de tête, capturer une image avec la caméra, ou rester explicitement inactif. Ces capacités ont du sens en local : elles touchent au matériel, aux capteurs, à l’état physique du robot. Les exécuter ailleurs serait absurde, un peu comme piloter un tournevis via satellite. Possible, mais révélateur d’une architecture qui a perdu le nord.

Le problème apparaît avec les capacités non corporelles : météo, recherche web, horaires, informations courantes, appels API, petits lookups stateless. Pour ces tâches, embarquer un fichier Python dans chaque installation est pénible. Il faut distribuer le code, le mettre à jour, l’activer dans l’application, vérifier qu’il ne casse rien, et répéter l’opération à chaque nouvelle capacité.

La nouvelle approche consiste à installer une référence vers un Space compatible MCP, par exemple :

```bash
reachy-mini-conversation-app tool-spaces add pollen-robotics/reachy-mini-weather-tool
```

Puis l’application peut découvrir les outils exposés par ce Space, les activer dans le profil courant, et les appeler via le backend conversationnel comme s’il s’agissait d’outils disponibles pour le modèle. Hugging Face donne deux canaris : `pollen-robotics/reachy-mini-weather-tool` pour la météo et `pollen-robotics/reachy-mini-search-tool` pour la recherche.

## MCP comme frontière entre local et distant

Le point important n’est pas que Reachy Mini sache demander la météo. Le point important est la frontière d’exécution. Le billet Hugging Face précise que l’outil distant **reste dans son Space** : aucun code arbitraire n’est téléchargé dans l’app locale. L’application découvre l’outil via l’endpoint MCP du Space, puis l’appelle. Cela rend le modèle de distribution beaucoup plus propre.

Pour l’IA locale, cette frontière est essentielle. Tous les outils ne méritent pas le même niveau de confiance. Un outil qui contrôle une caméra, un moteur, un fichier local ou une base privée doit rester local, auditable et verrouillé. Un outil qui interroge une API météo publique peut vivre dans un environnement distant, mis à jour indépendamment. MCP sert ici de contrat : description de l’outil, appel, réponse. Ce n’est pas une baguette magique de sécurité, mais c’est mieux que le bricolage où l’agent importe du Python trouvé au hasard.

Le système de profils renforce cette séparation. Dans l’app Reachy Mini, un outil n’est pas disponible simplement parce qu’il existe. Il doit être listé dans le profil, avec des fichiers comme `instructions.txt` et `tools.txt`. Le modèle ne peut appeler que les outils activés. C’est basique, mais c’est exactement le genre de basique qui manque souvent dans les démos d’agents : un périmètre explicite.

## Ce que dit le dépôt GitHub

Le dépôt `pollen-robotics/reachy_mini_conversation_app` décrit une app conversationnelle avec dispatch asynchrone d’outils, interface Gradio optionnelle, intégration du robot matériel ou de la simulation, et prise en charge de capacités comme mouvement, caméra et head tracking. Le dépôt mentionne aussi l’usage possible d’un modèle vision local **SmolVLM2** pour les requêtes liées à la caméra, à condition d’installer l’extra correspondant.

Le SDK `pollen-robotics/reachy_mini` présente Reachy Mini comme un kit robotique open-source, avec installation via SDK et contrôle par quelques lignes de Python. Il mentionne également une logique d’app store alimentée par Hugging Face Spaces. La nouveauté MCP s’inscrit donc dans une tendance plus large : utiliser le Hub non seulement comme dépôt de modèles, mais comme canal de distribution d’apps, d’outils et de capacités agentiques.

C’est intéressant, mais il faut garder le bon niveau d’enthousiasme. Ce n’est pas une preuve que MCP résout la robotique. C’est une intégration pragmatique qui rend certains outils plus faciles à partager et à mettre à jour.

## Les limites à ne pas ignorer

Hugging Face signale deux limites importantes. Premièrement, le Space doit réellement se comporter comme un serveur MCP : si la découverte d’outils échoue, l’installation échoue. Deuxièmement, les instructions de prompt peuvent encourager des appels parallèles, mais ne peuvent pas les garantir. Autrement dit, l’orchestration reste dépendante du modèle, du backend et du runtime.

Il y a aussi une limite de confiance. Un outil distant peut changer. Il peut tomber. Il peut être lent. Il peut journaliser des entrées. Pour un agent local sérieux, chaque outil distant doit être considéré comme une dépendance externe, pas comme une extension de confiance. La bonne pratique consiste à réserver ce mode aux capacités stateless et non sensibles : météo, recherche publique, lookup générique, documentation, etc. Pour les données privées, les fichiers locaux, les secrets ou les actions irréversibles, on reste local et on audite.

Enfin, cette architecture introduit une dépendance réseau. Un robot ou assistant local qui perd ses outils dès qu’Internet tombe n’est pas vraiment autonome. La bonne approche est donc hybride : noyau local robuste, outils distants optionnels.

## Pourquoi c’est pertinent pour les agents auto-hébergés

Reachy Mini donne une forme physique à un problème que les agents logiciels ont déjà : comment organiser les outils. Sur un poste de travail auto-hébergé, on retrouve la même séparation : certains outils doivent rester locaux — shell, fichiers, calendrier privé, base de connaissances, RAG — tandis que d’autres peuvent être distants — recherche web, API publiques, services de conversion.

L’intégration de Hugging Face montre un schéma propre : le Hub distribue ou référence des outils ; MCP fournit l’interface ; les profils contrôlent l’exposition ; l’app locale garde la main sur ce qui est activé. Ce modèle pourrait très bien s’appliquer à un agent de bureau local, à un assistant familial auto-hébergé, ou à un petit serveur d’équipe.

Le détail qui me plaît ici : l’équipe ne prétend pas que tout doit devenir distant. Les outils corporels restent locaux. Les outils web deviennent des Spaces MCP. La séparation est simple, lisible, et suffisamment réaliste pour survivre au-delà d’une vidéo de démo.

## À surveiller

La suite dépendra de trois choses. D’abord, la qualité des permissions : qui peut activer quoi, avec quels garde-fous, et comment l’utilisateur comprend ce que l’agent peut appeler. Ensuite, la traçabilité : logs d’appels, arguments envoyés, résultats reçus, erreurs. Enfin, la portabilité : un outil MCP publié pour Reachy Mini devrait idéalement rester utilisable par d’autres clients MCP sans adaptation excessive.

Pour le Labo IA Locale, cette annonce est moins une news robotique qu’un signal d’architecture. MCP devient un plan de câblage pour agents. Le Hub devient un registre d’outils. Et le local garde son rôle : contrôler les permissions, protéger les données, exécuter ce qui doit rester proche de la machine. Ce n’est pas spectaculaire. C’est mieux : c’est exploitable.

## Sources

- Hugging Face — [Adding MCP Tools to Reachy Mini](https://huggingface.co/blog/adding-mcp-tools-to-reachy-mini)
- GitHub — [pollen-robotics/reachy_mini_conversation_app](https://github.com/pollen-robotics/reachy_mini_conversation_app)
- GitHub — [pollen-robotics/reachy_mini](https://github.com/pollen-robotics/reachy_mini)
