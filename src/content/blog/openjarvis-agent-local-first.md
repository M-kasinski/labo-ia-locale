---
title: "OpenJarvis : Stanford veut standardiser l’agent IA local-first"
description: "OpenJarvis 1.0 arrive avec Ollama, une architecture hardware-aware et des métriques d'efficacité. Une piste sérieuse pour sortir les agents personnels du tout-cloud."
pubDate: 2026-05-30
category: "local"
tags: ["OpenJarvis", "agents locaux", "Ollama", "auto-hébergement", "Stanford", "RAG"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Stanford Scaling Intelligence — OpenJarvis: Personal AI, On Personal Devices"
    url: "https://scalingintelligence.stanford.edu/blogs/openjarvis/"
  - label: "Ollama — OpenJarvis: a local-first personal AI is now available to run with Ollama"
    url: "https://ollama.com/blog/openjarvis"
  - label: "GitHub — open-jarvis/OpenJarvis"
    url: "https://github.com/open-jarvis/OpenJarvis"
---

OpenJarvis vient d'arriver en version 1.0 avec une intégration Ollama mise en avant publiquement. Le projet est porté par Stanford Hazy Research et Scaling Intelligence, dans le cadre de leurs travaux **Intelligence Per Watt**. Son objectif : fournir une pile open-source pour construire des agents personnels qui tournent d'abord sur ta machine, avec le cloud comme option, pas comme réflexe.

Ce positionnement mérite qu'on s'y arrête. Depuis deux ans, beaucoup d'« agents personnels » sont locaux uniquement en façade : interface desktop, stockage partiel sur la machine, parfois quelques connecteurs, mais le raisonnement principal part vers une API distante. OpenJarvis attaque précisément cette contradiction. Le modèle, les outils, la mémoire et l'orchestration doivent pouvoir tourner localement, tout en mesurant la latence, l'énergie, le coût et la qualité.

## Le problème : les agents sont fragmentés

Le blog de Stanford décrit une situation que tous ceux qui bricolent des agents locaux connaissent : l'écosystème fonctionne, mais il est éclaté. Il faut choisir un runtime, un modèle, un orchestrateur, une mémoire vectorielle, des connecteurs, un système d'évaluation, puis prier pour que tout reste compatible après trois mises à jour.

OpenJarvis propose une couche commune autour de cinq primitives :

1. **Intelligence** : les modèles de langage locaux ;
2. **Engine** : le runtime d'inférence ;
3. **Agents** : les comportements et workflows ;
4. **Tools & Memory** : outils, connecteurs, mémoire locale, RAG ;
5. **Learning** : optimisation à partir de traces locales.

Ce n'est pas révolutionnaire conceptuellement. C'est même plutôt raisonnable. Mais dans l'IA locale, « raisonnable et intégré » est déjà un petit miracle administratif.

## Une interface hardware-aware au-dessus des runtimes

Le point le plus intéressant est probablement la couche **Engine**. Stanford liste explicitement plusieurs backends : **Ollama**, **vLLM**, **SGLang**, **llama.cpp**, Apple Foundation Models, Exo, Nexa, Mirai Uzu et d'autres selon la documentation. Le but n'est pas de remplacer ces runtimes, mais de fournir une interface qui sait tenir compte du matériel : GPU disponible, mémoire, plateforme, contraintes de latence.

L'idée est simple : un utilisateur ne devrait pas avoir à comprendre à la main tous les compromis entre un Qwen quantifié via Ollama, un modèle servi par vLLM, un runtime MLX sur Mac, ou un fallback cloud. OpenJarvis veut recommander et configurer l'option réaliste selon la machine.

Ollama publie de son côté un billet très concret : installation d'Ollama, installation d'OpenJarvis, puis commandes `jarvis`. Exemple :

```bash
curl -fsSL https://open-jarvis.github.io/OpenJarvis/install.sh | bash
jarvis
```

Pour choisir un modèle via Ollama :

```bash
jarvis model pull qwen3.5:35b
jarvis ask -m qwen3.5:35b "Votre prompt"
```

Et pour fixer un modèle par défaut :

```toml
[intelligence]
default_model = "qwen3.5:35b"
preferred_engine = "ollama"
```

Les noms exacts des modèles disponibles dépendront évidemment du catalogue Ollama installé et des capacités de la machine. Sur un laptop 16 Go, un 35B n'est pas le premier choix raisonnable. La gravité existe encore, même dans les démos.

## Les presets : productivité locale plutôt que benchmark abstrait

Ollama mentionne plusieurs presets prêts à l'emploi :

- **morning briefing** : résumé quotidien à partir du calendrier, des emails et de l'actualité ;
- **deep research** : recherche web et documents locaux avec citations ;
- **code assistant** : agent de code capable d'écrire et d'exécuter du Python localement.

Ces exemples sont bien choisis, parce qu'ils correspondent aux usages où le local-first a du sens. Un briefing personnel peut toucher des emails, un calendrier, des documents internes. Un agent de recherche peut indexer des fichiers privés. Un assistant de code peut lire un dépôt complet. Ce sont exactement les cas où envoyer tout le contexte à une API distante devient vite inconfortable, juridiquement ou simplement humainement.

Côté architecture, OpenJarvis pousse aussi l'idée d'une mémoire locale et d'un apprentissage en boucle fermée. Les traces d'usage peuvent servir à améliorer les prompts, la logique agentique, le choix du runtime ou même les poids, selon les capacités disponibles. C'est ambitieux. C'est aussi le genre de fonctionnalité qui devra être auditable : une pile locale qui apprend sans transparence peut devenir aussi pénible qu'un service cloud opaque, juste plus proche du ventilateur.

## Intelligence Per Watt : le bon angle d'évaluation

Le billet de Stanford cite une conclusion forte de leurs travaux Intelligence Per Watt : les modèles locaux et accélérateurs locaux pourraient traiter **88,7 % des requêtes single-turn de chat et raisonnement** à latence interactive, avec une efficacité d'intelligence améliorée de **5,3× entre 2023 et 2025**. C'est un claim important, mais il faut le lire correctement.

Cela ne veut pas dire qu'un petit modèle local remplace toujours les meilleurs modèles cloud. Cela veut dire que pour une grande part des requêtes courantes, le coût de sortir du device n'est plus automatiquement justifié. La question devient donc : quand faut-il rester local, quand faut-il escalader vers plus gros, et comment mesurer ce compromis ?

OpenJarvis rend ces dimensions explicites : qualité, latence, énergie, mémoire, FLOPs, coût. C'est sain. Les benchmarks d'agents oublient trop souvent que l'utilisateur attend devant l'écran, sur une machine qui chauffe, avec une batterie et parfois une connexion médiocre.

## Ce que ça change pour l'auto-hébergement

Pour l'auto-hébergement, OpenJarvis peut devenir une couche d'orchestration intéressante au-dessus d'un stack existant. Si tu as déjà Ollama pour les modèles quotidiens, llama.cpp pour les tests GGUF, vLLM pour servir plus sérieusement sur GPU, et une brique RAG locale, OpenJarvis pourrait servir de point d'entrée commun.

Le projet ne supprime pas les questions difficiles : sécurité des outils, permissions système, isolation de l'exécution de code, gestion des secrets, qualité du retrieval, observabilité. Au contraire, il les rend plus visibles. C'est plutôt bon signe. Un agent local qui peut lire tes fichiers et lancer du code doit être traité comme un vrai logiciel sensible, pas comme un chatbot avec des stickers.

La licence annoncée côté Stanford est **Apache 2.0**, ce qui facilite l'expérimentation et l'intégration dans des projets internes. Il faudra vérifier la maturité réelle du dépôt, la stabilité des APIs et la qualité des connecteurs. Une version 1.0 n'est pas une garantie de tranquillité ; c'est parfois seulement une manière polie de dire « ça compile chez nous ».

## Verdict provisoire

OpenJarvis est l'un des signaux les plus intéressants du moment pour les agents locaux, non pas parce qu'il invente une brique magique, mais parce qu'il assemble les bonnes contraintes : local-first, hardware-aware, compatible avec les runtimes existants, mesuré en efficacité, et pensé pour des workflows personnels.

La prudence reste nécessaire. Les promesses d'agents autonomes sont un cimetière de démos brillantes et de tâches réelles ratées. Mais ici, l'angle est solide : rendre l'agent local composable, mesurable et moins dépendant d'une API distante. Pour le Labo IA Locale, c'est exactement le bon terrain de jeu.
