---
title: "Monter un agent local autonome : architecture et garde-fous"
description: "Un guide concret pour assembler chez soi un agent local capable d'observer, décider, utiliser des outils et rester sous contrôle humain."
pubDate: 2026-05-29
category: "local"
tags: ["ia-locale", "agents", "tool-use", "mcp", "self-hosting"]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "Model Context Protocol — spécification et documentation officielles", url: "https://github.com/modelcontextprotocol/modelcontextprotocol" }
  - { label: "MCP — architecture overview", url: "https://modelcontextprotocol.io/docs/learn/architecture" }
  - { label: "MCP — tools specification", url: "https://modelcontextprotocol.io/specification/2025-11-25/server/tools" }
  - { label: "Ollama — dépôt officiel", url: "https://github.com/ollama/ollama" }
  - { label: "Ollama — API docs", url: "https://github.com/ollama/ollama/blob/main/docs/api.md" }
  - { label: "llama.cpp — dépôt officiel", url: "https://github.com/ggml-org/llama.cpp" }
  - { label: "vLLM — dépôt officiel", url: "https://github.com/vllm-project/vllm" }
  - { label: "LangGraph — dépôt officiel", url: "https://github.com/langchain-ai/langgraph" }
  - { label: "smolagents — dépôt officiel", url: "https://github.com/huggingface/smolagents" }
  - { label: "CrewAI — dépôt officiel", url: "https://github.com/crewAIInc/crewAI" }
  - { label: "OpenHands — dépôt officiel", url: "https://github.com/OpenHands/OpenHands" }
  - { label: "Open Interpreter — dépôt officiel", url: "https://github.com/openinterpreter/open-interpreter" }
  - { label: "Hermes Agent — dépôt officiel Nous Research", url: "https://github.com/NousResearch/hermes-agent" }
---

## Le vrai sujet : une boucle, pas un chatbot

Un agent local autonome n'est pas juste un modèle qui répond dans un terminal. C'est une boucle d'exécution : perception → décision → action → observation. La différence est simple : le chatbot s'arrête après avoir produit du texte ; l'agent transforme ce texte en appels d'outils, lit le résultat, met à jour son état, puis décide s'il continue.

Sur une machine personnelle, cette boucle peut rester modeste : lire un dossier, chercher dans une base de notes, appeler une API locale, modifier un fichier, lancer des tests, résumer le résultat. C'est déjà puissant. C'est aussi déjà dangereux si l'agent a le droit d'écrire partout, d'exécuter n'importe quelle commande shell ou d'envoyer des données vers Internet. L'architecture doit donc être pensée comme un petit système d'exploitation contrôlé, pas comme une démo magique.

## Architecture minimale à la maison

Une pile locale raisonnable tient en cinq briques.

1. Le modèle pilote : Ollama, llama.cpp ou vLLM. Ollama vise le démarrage rapide avec des modèles locaux et expose une API de chat ; sa documentation API prévoit aussi une liste de tools JSON pour les modèles qui les supportent. llama.cpp fournit l'inférence LLM en C/C++ et reste une base très utilisée pour les modèles quantifiés GGUF. vLLM, lui, vise surtout le service d'inférence performant et mémoire-efficace, avec un intérêt particulier si vous avez un GPU costaud ou plusieurs utilisateurs.

2. Le runtime agent : c'est lui qui garde l'état, choisit les outils, relance le modèle après observation, applique les limites. LangGraph se présente comme un framework bas niveau pour agents stateful, avec exécution durable, supervision humaine et mémoire courte/longue durée. smolagents, chez Hugging Face, privilégie des agents qui écrivent leurs actions en code, avec exécution sandboxable via Docker ou d'autres environnements. CrewAI cible l'orchestration multi-agents : des rôles, des tâches, une collaboration entre agents.

3. Les outils : fichiers, terminal, navigateur, base vectorielle, agenda, Git, domotique. Un outil doit être une fonction bornée : entrée typée, sortie lisible, erreurs explicites. Mauvais outil : « shell illimité ». Bon outil : « lancer `pytest` dans ce dépôt », « lire seulement `~/Notes/IA` », « créer une note dans ce répertoire ».

4. La mémoire : au minimum, un historique de tâche et un carnet de faits persistants. La mémoire courte sert au raisonnement en cours ; la mémoire longue garde des préférences, conventions de projet, chemins utiles. À ne pas confondre avec un dépotoir de logs : si tout est mémoire, plus rien n'est signal.

5. L'interface de supervision : terminal, TUI, web UI ou messagerie. L'important n'est pas le style, mais la possibilité de voir ce que l'agent veut faire, refuser une action et reprendre la main.

## Tool-use : le contrat entre le modèle et la machine

Le tool-use est le point où l'IA cesse d'être seulement bavarde. Le modèle ne doit pas « deviner » qu'il a réussi : il appelle un outil, reçoit une observation, puis continue.

Exemple simple :

- perception : « le fichier `app.py` échoue aux tests » ;
- décision : « lire l'erreur, inspecter le code, proposer un patch » ;
- action : appeler `read_file`, puis `run_tests`, puis `patch_file` ;
- observation : sortie réelle de pytest, diff réel, nouvelle exécution des tests.

Cette discipline évite le théâtre de l'agent qui annonce « corrigé » sans avoir rien lancé. Elle impose aussi un design de permissions. Chaque outil devrait déclarer : lecture seule ou écriture ? accès réseau ? chemin autorisé ? coût possible ? besoin de validation humaine ?

Open Interpreter illustre bien le risque et le remède : son README indique que les LLM peuvent exécuter du code localement, mais précise que l'utilisateur doit approuver le code avant exécution. OpenHands, côté développement logiciel, propose un SDK, une CLI et une GUI locale pour agents de code ; ce type d'outil doit être confiné à un dépôt ou à un conteneur, pas lâché sur tout le disque.

## MCP : brancher des outils sans refaire toute la plomberie

Le Model Context Protocol (MCP) sert à standardiser la connexion entre applications IA et sources de contexte/outils. Sa documentation décrit une architecture host → client → server : l'application IA joue le rôle de host, crée un client par serveur MCP, et chaque serveur fournit du contexte ou des capacités.

Concrètement, un serveur MCP peut exposer des tools. La spécification explique que ces tools peuvent être découverts via `tools/list` et invoqués par le modèle ; elle recommande aussi, explicitement, une boucle humaine capable de refuser les invocations. C'est exactement le bon réflexe pour du local : MCP n'est pas une baguette magique de sécurité, mais un format propre pour dire « voici les outils disponibles, voici leur schéma, voici comment les appeler ».

Une architecture domestique typique : votre agent local parle MCP à un serveur filesystem limité à un dossier, à un serveur Git limité à un dépôt, à un serveur notes, puis à un serveur navigateur ou recherche. Le modèle reste interchangeable : Ollama pour commencer, llama.cpp si vous optimisez finement vos quantifications, vLLM si vous servez plusieurs agents ou modèles.

## Orchestration multi-étapes : éviter l'agent en roue libre

L'autonomie utile n'est pas « fais tout jusqu'à nouvel ordre ». C'est une suite de petites étapes vérifiables. LangGraph est intéressant ici parce qu'il formalise des graphes d'état : un nœud planifie, un nœud agit, un nœud vérifie, un nœud demande validation. CrewAI pousse plutôt le modèle « plusieurs agents spécialisés » : chercheur, rédacteur, reviewer, exécuteur. smolagents offre une approche compacte où l'action peut être du code, à condition de sandboxer l'exécution.

La règle pratique : toute étape qui écrit, supprime, dépense ou publie doit passer par une barrière. Pour un agent de veille locale, publier un résumé sur un blog est une barrière. Pour un agent de code, modifier un fichier peut être autorisé dans une branche Git temporaire, mais le commit, le push ou le déploiement doivent rester manuels.

Hermes Agent, de Nous Research, peut être rangé dans cette famille d'agents open-source : son dépôt officiel le présente comme un agent avec boucle d'apprentissage, mémoire de sessions et système de skills, sous licence MIT. C'est un exemple parmi d'autres, pas une obligation d'architecture. Le point important est le même : inspecter les outils, les permissions et la mémoire avant de confier des actions réelles.

## Garde-fous et sécurité : le local ne rend pas invincible

Faire tourner l'agent chez soi protège contre certains risques cloud, mais en crée d'autres. Un agent local voit potentiellement vos fichiers, vos clés SSH, votre navigateur, vos mails, vos tokens. La bonne posture : moindre privilège, journalisation, sandbox, validation humaine.

Checklist minimale :

- lancer l'agent dans un utilisateur système dédié ou un conteneur ;
- monter seulement les dossiers nécessaires ;
- interdire par défaut les commandes shell arbitraires ;
- séparer outils lecture seule et outils écriture ;
- exiger confirmation pour suppression, paiement, envoi réseau, publication, modification Git destructive ;
- journaliser chaque tool call avec entrée, sortie, durée et statut ;
- limiter budget tokens, temps CPU/GPU et nombre d'itérations ;
- prévoir un bouton stop, pas une incantation.

Les coûts aussi méritent un garde-fou. Local ne veut pas dire gratuit : GPU saturé, ventilateurs, électricité, usure SSD, temps humain de debug. Fixez un plafond : nombre maximal d'appels modèle par tâche, timeout par outil, arrêt si deux observations successives montrent la même erreur.

## Une recette réaliste

Pour commencer sans construire une usine : Ollama avec un modèle instruct local, un runtime comme LangGraph ou smolagents, trois outils seulement — lecture de fichiers dans un dossier, recherche locale, lancement de tests — et une validation obligatoire avant écriture. Ajoutez MCP quand vous avez plusieurs outils à brancher proprement. Ajoutez une mémoire longue seulement quand vous savez ce qui vaut la peine d'être retenu.

Le bon agent local n'est pas celui qui a 80 outils. C'est celui qui fait peu d'actions, mais les fait proprement : il observe, agit dans un périmètre, vérifie, et s'arrête avant de transformer votre machine en escape room numérique.
