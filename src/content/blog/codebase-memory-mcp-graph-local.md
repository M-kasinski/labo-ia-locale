---
title: "Codebase-Memory MCP : quand l’agent local arrête de grepper à l’aveugle"
description: "Codebase-Memory transforme un dépôt en graphe persistant exposé via MCP, avec une release 0.7.0 qui renforce la résolution sémantique des appels."
pubDate: 2026-06-05
tags: ["mcp", "agents", "code", "auto-hébergement"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub — DeusData/codebase-memory-mcp"
    url: "https://github.com/DeusData/codebase-memory-mcp"
  - label: "GitHub Releases — v0.7.0"
    url: "https://github.com/DeusData/codebase-memory-mcp/releases"
  - label: "arXiv — Codebase-Memory: Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP"
    url: "https://arxiv.org/abs/2603.27277"
---

Les agents de code locaux ont un problème très banal : ils passent trop de temps à chercher. Ils lisent des fichiers entiers, relancent `grep`, ouvrent le mauvais module, oublient ce qu’ils viennent d’inspecter, puis recommencent avec l’aplomb tranquille d’un stagiaire caffeiné. **Codebase-Memory MCP** attaque ce problème par le bas : indexer le dépôt en graphe persistant, puis exposer ce graphe à l’agent via **Model Context Protocol**.

Le projet n’est pas seulement un “semantic search” de plus. Sa promesse est plus structurelle : construire une représentation locale du code — symboles, appels, routes, liens entre services, métadonnées d’architecture — et permettre à l’agent de poser des questions ciblées au lieu de consommer des dizaines de milliers de tokens en exploration fichier par fichier. La dernière release majeure visible, **v0.7.0 publiée le 30 mai 2026**, met justement l’accent sur la résolution sémantique des appels avec une couche “Hybrid LSP” sur plusieurs familles de langages.

## Le principe : un graphe local, pas un SaaS de plus

Le dépôt GitHub décrit Codebase-Memory MCP comme un serveur MCP de “code intelligence” qui indexe les dépôts dans un graphe de connaissance persistant, sauvegardé localement. L’implémentation est principalement en C/C++, distribuée comme binaire statique, avec une licence MIT. Le projet revendique un fonctionnement sans dépendance runtime, sans API key, sans Docker obligatoire, et avec traitement 100 % local : votre code reste sur la machine.

C’est important pour le local-first. Beaucoup d’outils de code intelligence ajoutent une couche LLM, une base vectorielle distante ou un service managé. Ici, l’idée est différente : **l’agent que vous utilisez déjà** — Claude Code, OpenClaw, Hermes, Cursor-like local, peu importe tant qu’il parle MCP — reste le traducteur en langage naturel. Codebase-Memory fournit les outils structurés. Si vous demandez “qu’est-ce qui appelle `ProcessOrder` ?”, l’agent peut appeler un outil de graphe plutôt que lire tout le backend.

Le README revendique **14 outils MCP**, la prise en charge de nombreux agents de code, une UI optionnelle de visualisation 3D, et un support très large de langages. La page extraite indique **159 langages** et **157 grammaires tree-sitter vendues dans le binaire**. À noter : le papier arXiv associé, soumis en mars 2026, parlait encore de 66 langages ; le dépôt semble donc avoir évolué rapidement depuis la publication académique.

## Ce que change la v0.7.0

La release **v0.7.0** est titrée “Hybrid LSP across six languages”. Le changelog résume bien l’enjeu : “the call graph stops being a guess”. Dit autrement, un graphe basé uniquement sur tree-sitter sait reconnaître qu’un appel existe, mais pas toujours à quelle définition réelle il correspond, surtout dans des langages avec imports, méthodes, héritage, types génériques, traits, callbacks ou JSX.

La release ajoute ou améliore des passes sémantiques légères pour plusieurs familles : **Python**, **PHP**, **TypeScript/JavaScript/JSX/TSX**, **C#/.NET**, ainsi que des améliorations pour **C/C++/CUDA** et **Go**. Ces passes suivent les scopes, infèrent certains types, suivent des imports, traitent l’héritage et réécrivent les arêtes `CALLS` vers des cibles plus précises.

Le projet décrit une architecture en trois niveaux :

- **Tier 1** : résolution par fichier pendant l’extraction.
- **Tier 2** : registre cross-file par langage, construit une fois depuis les définitions du projet.
- **Tier 3** : approche metadata-driven pour Go, afin d’éviter de reparcourir inutilement les AST.

C’est le genre de détail qui fait la différence entre un jouet MCP et un outil qu’on peut laisser branché sur un dépôt de production. Un agent qui confond deux méthodes homonymes peut proposer une modification plausible dans le mauvais module. C’est charmant cinq secondes. Après, c’est un incident.

## Les chiffres : prometteurs, mais à lire proprement

Le dépôt avance des chiffres agressifs : indexation d’un dépôt moyen en millisecondes, requêtes structurelles sous la milliseconde, Linux kernel — **28 millions de lignes et 75 000 fichiers** — indexé en environ **3 minutes**. La release v0.7.0 donne aussi des validations concrètes : par exemple **microsoft/TypeScript** à 40 689 fichiers passant d’un cas catastrophique à environ **50 secondes** en mode full, **dotnet/roslyn** à 17 916 fichiers en **46 secondes**, **kubernetes** en Go à **51 secondes**, **WordPress** en PHP à **7 secondes**, et **postgres** en C à **8 secondes**.

Ces chiffres viennent du projet lui-même : utiles pour cadrer, mais à reproduire sur votre machine avant d’en faire un choix d’infrastructure. La bonne nouvelle est que le projet fournit un binaire local ; il est donc relativement simple de tester sur un dépôt réel, avec votre SSD, votre OS et vos conventions de code.

Le papier arXiv fournit un autre angle. Il évalue Codebase-Memory sur **31 dépôts réels** et rapporte **83 % de qualité de réponse**, contre **92 %** pour un agent explorant les fichiers, mais avec **10× moins de tokens** et **2,1× moins d’appels d’outils**. Pour les requêtes naturellement orientées graphe — hub detection, caller ranking — le système égale ou dépasse l’explorateur sur **19 des 31 langages**.

La lecture honnête : Codebase-Memory ne remplace pas toujours l’exploration complète. Il échange parfois un peu de qualité contre beaucoup moins de tokens et d’allers-retours. Pour un agent local, ce compromis peut être excellent, surtout quand le modèle tourne sur une machine limitée et que chaque millier de tokens ralentit l’action.

## Où l’utiliser dans une stack locale

Le cas d’usage évident est l’agent de code branché sur un gros dépôt. Au lieu de lui donner `read_file` et `grep` comme seules armes, on lui ajoute un serveur MCP capable de répondre à des questions structurelles : appels entrants, dépendances, fonctions proches, routes, impact potentiel d’une modification.

Architecture typique :

1. Un runtime local ou hybride pour l’agent : Ollama, llama.cpp, vLLM, MLX, ou un modèle distant si nécessaire.
2. Un client agentique compatible MCP.
3. Codebase-Memory MCP installé dans le dépôt.
4. Un workflow explicite : indexer, demander au graphe, lire seulement les fichiers pertinents, modifier, tester.

Ce dernier point compte. Un graphe n’est pas une vérité absolue. Il faut toujours lire les fichiers avant modification, lancer les tests, et garder un garde-fou humain pour les changements risqués. Le graphe réduit l’errance, il ne rend pas l’agent omniscient. Petite nuance, énorme facture évitée.

## Ce qu’il faut surveiller

Le projet est jeune et avance vite. C’est positif, mais cela implique des angles morts : qualité variable selon les langages, résolution sémantique incomplète sur certains patterns dynamiques, risque de confiance excessive dans le graphe, et surface de sécurité liée au fait que l’outil lit le code et peut modifier des configurations d’agents. Le README conseille d’auditer l’installateur si nécessaire ; c’est un conseil à prendre littéralement, surtout en environnement professionnel.

La release v0.7.0 montre cependant une direction saine : moins de “recherche floue”, plus de structure, plus de local, plus de MCP. Pour les agents locaux, c’est probablement là que le gain réel se trouve. Pas dans un modèle qui “comprend tout” magiquement, mais dans un environnement qui lui évite de chercher comme une lampe torche dans un hangar.

## Sources

- GitHub — `DeusData/codebase-memory-mcp` : https://github.com/DeusData/codebase-memory-mcp
- GitHub Releases — Codebase-Memory MCP v0.7.0 : https://github.com/DeusData/codebase-memory-mcp/releases
- arXiv — “Codebase-Memory: Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP” : https://arxiv.org/abs/2603.27277
