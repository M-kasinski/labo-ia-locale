---
title: "Sandbox0 : le bac à sable auto-hébergé qui prend enfin les agents au sérieux"
description: "Sandbox0 propose une frontière d’exécution pour agents IA : sandboxes persistantes, contrôle réseau, secrets hors runtime et déploiement Kubernetes auto-hébergé. Utile, mais encore à traiter comme une surface beta."
pubDate: 2026-06-08
category: "local"
tags: ["agents", "sandbox", "auto-hébergement", "MCP", "sécurité", "Kubernetes"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub — sandbox0-ai/sandbox0"
    url: "https://github.com/sandbox0-ai/sandbox0"
  - label: "Sandbox0 — documentation self-hosted"
    url: "https://sandbox0.ai/docs/self-hosted"
  - label: "Sandbox0 — Claude Managed Agents on Sandbox0"
    url: "https://sandbox0.ai/blog/2026-05/claude-managed-agents-on-sandbox0"
---

Les agents locaux ont un problème moins spectaculaire que les benchmarks, mais beaucoup plus dangereux : **où exécuter leurs actions**. Lire un dépôt, lancer des tests, ouvrir un port, appeler un outil MCP, manipuler des fichiers, installer des dépendances… tout cela ressemble à du travail normal de développeur. Jusqu’au moment où l’agent exécute une commande douteuse dans ton environnement principal, lit un secret, ou mélange deux contextes client. Le modèle n’a pas besoin d’être malveillant pour faire des dégâts ; l’autocomplétion du chaos suffit largement.

C’est précisément le créneau de **Sandbox0**, un projet open-source sous licence **Apache 2.0** qui se présente comme une frontière d’exécution pour plateformes d’agents IA. Le dépôt GitHub décrit Sandbox0 comme une couche fournissant des sandboxes isolées et persistantes pour le travail agentique : exécution de code, édition de dépôts, exposition de services HTTP par agent, conservation d’état de workspace, accès contrôlé aux systèmes externes, sans placer de larges identifiants de production dans le runtime de l’agent.

## Ce que Sandbox0 essaie de résoudre

La plupart des stacks d’agents démarrent avec une boucle simple : modèle, outils, shell, fichiers. Ça fonctionne pour une démo. Pour un système auto-hébergé, c’est incomplet. Il manque au minimum quatre choses : une isolation fiable, une gestion d’état, une politique réseau, et une manière saine d’injecter des secrets. Sandbox0 rassemble ces préoccupations au même endroit.

Le README liste plusieurs usages : exécuter du code et des outils non fiables dans des sandboxes isolées ; construire des agents de code avec REPL stateful, commandes ponctuelles, volumes de dépôt persistants et templates rapides ; exécuter des passerelles d’agents comme **Hermes** ou **OpenClaw** ; exposer des services HTTP par agent avec authentification de route, filtrage des méthodes, CORS, limites de débit, timeouts et réécriture de chemin ; garder les secrets hors du processus agent via credential sources, egress auth, proxy SSH transparent, LLMProxy ou passerelle externe.

Le projet parle aussi de **contrôle réseau et MCP** : règles de trafic ordonnées, contrôles d’outils MCP au niveau protocolaire et audit de l’egress dans le data plane. C’est un détail important. MCP rend les agents beaucoup plus utiles, mais il élargit aussi leur surface d’action. Un serveur MCP branché sans politique, c’est un tournevis électrique donné à un stagiaire invisible. Souvent efficace. Parfois mémorable.

## Persistance, snapshots et fork

Sandbox0 ne vend pas seulement une “boîte Docker” jetable. Le README met en avant des volumes, des snapshots point-in-time, la restauration et le **Copy-on-Write fork** pour brancher, évaluer ou récupérer l’état d’un agent. Pour les agents de code, c’est probablement l’une des parties les plus intéressantes : au lieu de relancer un environnement propre à chaque tentative, on peut conserver un workspace, créer un point de sauvegarde, explorer une branche d’exécution, puis revenir en arrière.

Ce modèle colle bien aux workflows modernes : un agent tente une correction, lance les tests, casse une dépendance, revient à l’état précédent, essaye une autre stratégie. Sur le papier, cela permet de rendre les boucles agentiques moins coûteuses et moins fragiles. En pratique, il faudra mesurer la vitesse réelle des snapshots, l’empreinte disque, et la robustesse quand plusieurs agents manipulent des dépôts lourds ou des environnements avec services persistants.

La documentation et le dépôt indiquent aussi une séparation entre **Raw Sandboxes**, pour contrôler directement processus, fichiers, volumes, ports, templates et politique réseau, et des chemins plus agentiques comme **Agent in Sandbox** ou **Managed Agents**. L’idée est bonne : tout le monde n’a pas besoin de la même abstraction. Un développeur d’infrastructure voudra piloter la sandbox ; une équipe produit préférera une API de session et d’événements.

## Auto-hébergement : intéressant, mais pas trivial

Pour notre angle local, le point clé est que Sandbox0 annonce un **data plane Kubernetes auto-hébergé**, avec PostgreSQL externe, stockage compatible S3/OSS, stockage de secrets compatible Vault, Redis et options de registry. Ce n’est pas “je lance un binaire dans mon salon et c’est fini”. C’est plutôt une brique d’infrastructure pour équipe qui veut posséder la frontière d’exécution, tout en gardant une architecture proche d’un service managé.

C’est une bonne chose si tu opères des agents pour plusieurs utilisateurs, plusieurs clients ou plusieurs dépôts sensibles. C’est excessif si ton besoin est simplement de lancer un assistant local dans un dossier personnel. Dans ce cas, un conteneur Docker verrouillé, une VM locale ou un outil plus minimal peut suffire. Sandbox0 devient pertinent quand les agents ont besoin de persistance, de routage de services, de règles réseau, d’audit et de secrets contrôlés.

Le billet de Sandbox0 sur les Claude Managed Agents insiste sur une idée juste : le sandbox ne doit pas être la source de vérité, mais une **attache à un workspace durable**. L’exécution self-hosted n’a de valeur que si l’agent peut atteindre les systèmes nécessaires — GitHub, APIs internes, bases de données, registres de paquets, observabilité, SaaS client, serveurs MCP privés — sans transformer cet accès en buffet de credentials. C’est exactement le genre de plomberie qui manque dans beaucoup de prototypes d’agents.

## Ce qu’il faut garder en tête

Le README prévient que Sandbox0 est en **développement actif** et recommande d’utiliser les SDKs et le CLI `s0` plutôt que de dépendre d’URLs HTTP codées en dur ou de surfaces beta. Ce n’est pas un détail administratif : pour une brique de sécurité et d’exécution, une API instable peut coûter cher si elle est enfouie dans un orchestrateur maison.

Je n’ai pas trouvé, au moment de cette veille, d’audit de sécurité indépendant ou de benchmark public détaillant l’isolation sous charge, les coûts de snapshot, ou la résistance à des scénarios hostiles. Il faut donc traiter Sandbox0 comme une piste sérieuse, pas comme une garantie magique. Les claims du dépôt sont vérifiables à la source, mais ils restent ceux du projet. Avant de l’exposer à des workloads sensibles, il faudrait tester : politique d’egress, séparation des volumes, injection et révocation des secrets, logs d’audit, comportement en cas de commande longue, nettoyage après échec, et compatibilité réelle avec les clients MCP utilisés.

## Pourquoi ça compte pour l’IA locale

L’IA locale ne se résume plus à “un modèle dans Ollama”. Dès qu’un agent manipule du code, des documents privés ou des services internes, l’environnement d’exécution devient aussi important que le choix du LLM. Un petit modèle local bien contraint dans une sandbox propre est souvent plus exploitable qu’un gros modèle brillant avec accès libre à `~/.ssh`.

Sandbox0 met le projecteur sur cette couche oubliée : le runtime agentique. Si le projet tient ses promesses — isolation, persistance, snapshots, contrôle réseau, MCP policy, self-hosting — il peut devenir une brique utile pour des agents locaux sérieux. Pas forcément la brique la plus simple. Mais la simplicité qui exécute tout dans le shell principal n’est pas de la simplicité ; c’est une dette de sécurité avec une interface conversationnelle.

## Sources

- GitHub — sandbox0-ai/sandbox0 : https://github.com/sandbox0-ai/sandbox0
- Sandbox0 — documentation self-hosted : https://sandbox0.ai/docs/self-hosted
- Sandbox0 — Claude Managed Agents on Sandbox0 : https://sandbox0.ai/blog/2026-05/claude-managed-agents-on-sandbox0
