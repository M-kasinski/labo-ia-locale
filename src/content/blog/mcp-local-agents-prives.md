---
title: "MCP en local : des agents privés et un tool-use maîtrisé"
description: "Comment combiner MCP, modèles locaux et serveurs auto-hébergés pour garder la main sur les outils, les données et l’audit."
pubDate: 2026-05-29
tags: ["ia-locale", "mcp", "agents", "tool-use", "self-hosting"]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "MCP Overview", url: "https://modelcontextprotocol.io/specification/2025-06-18/basic" }
  - { label: "MCP Transports", url: "https://modelcontextprotocol.io/specification/2025-06-18/basic/transports" }
  - { label: "MCP reference servers", url: "https://raw.githubusercontent.com/modelcontextprotocol/servers/main/README.md" }
  - { label: "MCP Python SDK", url: "https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md" }
  - { label: "Ollama tool calling", url: "https://docs.ollama.com/capabilities/tool-calling" }
  - { label: "vLLM tool calling", url: "https://docs.vllm.ai/en/latest/features/tool_calling/" }
  - { label: "llama.cpp README", url: "https://raw.githubusercontent.com/ggml-org/llama.cpp/master/README.md" }
---

Quand on parle d’“agents privés”, le vrai sujet n’est pas de faire parler un modèle dans le vide. Le sujet, c’est de savoir précisément quels outils il voit, où s’exécutent ces outils, quelles données ils touchent, et comment on peut relire l’historique après coup. MCP devient intéressant exactement là : il découple le raisonnement, l’accès aux outils et l’exécution. Le modèle n’ouvre pas magiquement tes fichiers, ta base ou ton dépôt Git ; il produit une intention. Le client MCP, lui, tranche, route, exécute, journalise.

## MCP, en pratique : un contrat, pas une religion

La spec MCP décrit un protocole JSON-RPC avec une séparation nette des rôles. Les serveurs exposent des outils, des ressources et des prompts. Les clients apportent aussi des capacités comme les racines de fichiers et le sampling. Cette modularité évite de mélanger le moteur de raisonnement, l’I/O et les intégrations.

Deux transports standards sont définis : `stdio` et `Streamable HTTP`. En `stdio`, le client lance le serveur MCP comme sous-processus ; les messages passent sur stdin/stdout, avec stderr réservé au log. En `Streamable HTTP`, le serveur parle via POST et GET, peut utiliser SSE pour streamer, et doit respecter des garde-fous de sécurité comme la validation de l’Origin, le binding sur localhost en local et une vraie authentification.

Autrement dit : MCP n’est pas “le protocole des agents”. C’est la couche de contrôle qui rend le tool-use explicite, auditable et remplaçable.

Schéma minimal d’une pile locale :

```text
Utilisateur
   ↓
Agent local / orchestrateur
   ↓
LLM local (Ollama, vLLM, llama.cpp)
   ↓  sort un tool-call structuré
Client MCP
   ├─→ serveur Filesystem (stdio)
   ├─→ serveur Git (stdio)
   ├─→ serveur SQLite / PostgreSQL (HTTP localhost ou stdio)
   └─→ autres serveurs auto-hébergés
   ↓
résultat renvoyé au modèle, puis réponse finale
```

Le point clé : le modèle ne parle pas “à MCP” directement. Il parle à un runtime ou à un client agent qui sait lire sa sortie, détecter un appel d’outil, puis invoquer le serveur MCP adéquat.

## Pourquoi le local change vraiment la donne

Avec un modèle cloud, tu déportes à la fois le raisonnement et une partie des traces d’exécution. Avec un modèle local, tu gardes le calcul chez toi ; avec MCP local, tu gardes aussi la couche outil sous ton toit.

C’est là que la combinaison devient intéressante :
- les prompts, les résultats d’outils et les logs restent sur la machine ou le réseau interne ;
- tu peux limiter chaque serveur à un périmètre précis ;
- tu peux lire le code des serveurs MCP, les wrapper, les containeriser, les couper du réseau ;
- tu peux reproduire un incident, car l’audit n’est plus noyé dans une plateforme distante.

Le gain n’est pas théorique. Il est opérationnel : moins d’incertitude sur la donnée qui sort, moins de dépendance à une plateforme, plus de contrôle sur les permissions.

## Trois briques locales qui marchent bien ensemble

### 1) Ollama : simple pour démarrer

La doc officielle d’Ollama dit clairement que le runtime prend en charge le tool calling, aussi appelé function calling. Le modèle peut invoquer des outils, puis intégrer leur résultat dans la réponse. La doc montre aussi le pattern à une boucle : le modèle propose un tool call, l’application exécute la fonction, réinjecte le résultat, puis redemande une réponse finale.

Pour un stack local, c’est pratique parce que l’orchestration reste dans ton code. Tu peux connecter ce code à un ou plusieurs serveurs MCP, sans jamais sortir du réseau local.

### 2) vLLM : plus d’options côté serving

La doc vLLM consacre une page entière au tool calling. Elle documente le named function calling, l’usage de `tool_choice="auto"`, les backends de structured outputs, et même des appels parallèles pour certains modèles et parseurs. En clair : vLLM ne fait pas juste du “texte qui ressemble à un appel d’outil”. Il sait structurer la sortie pour que le client puisse l’interpréter de façon fiable.

C’est utile si tu veux servir plusieurs modèles, garder une API compatible OpenAI, et brancher derrière une couche MCP bien contrôlée.

### 3) llama.cpp : l’option la plus sobre

Le dépôt officiel présente `llama-server` comme un serveur d’API OpenAI-compatible. Pour une architecture MCP, l’intérêt est simple : tu peux garder un backend local très minimaliste, puis faire porter l’orchestration des outils au client agent. Ce n’est pas la pile la plus “magique”, mais c’est souvent la plus lisible. Et, en local, la lisibilité est une forme de sécurité.

## Des serveurs MCP utiles en local

Le dépôt officiel des serveurs MCP liste plusieurs implémentations de référence. Pour un usage local, les plus utiles sont souvent les plus sobres :

- Filesystem : opérations de fichiers avec contrôles d’accès configurables.
- Git : lecture, recherche et manipulation de dépôts locaux.
- Memory : mémoire persistante en graphe de connaissances.
- Fetch : récupération et conversion de contenu web.
- SQLite : interaction avec une base locale.
- PostgreSQL : accès base en lecture seule avec inspection de schéma.

Pour un poste de travail ou un labo, ça couvre déjà beaucoup : explorer un dossier projet, fouiller un repo, interroger une base locale, résumer un contenu, conserver un état de travail sans passer par un SaaS.

En pratique, la pile peut être très simple : un serveur Filesystem pour le répertoire projet, un serveur Git pour le dépôt, un serveur SQLite pour les données, et c’est déjà un agent qui travaille comme un vrai collègue — mais sous laisse courte.

## Les pièges, parce qu’il y en a toujours

Le principal risque n’est pas MCP. C’est l’élargissement incontrôlé des permissions.

1. Un serveur Filesystem trop large peut transformer un agent en aspirateur à secrets.
2. Un serveur HTTP local mal protégé peut être exposé via DNS rebinding si tu négliges l’Origin, le binding local et l’auth.
3. Un serveur de shell, même “local”, peut exfiltrer des données s’il a accès au réseau.
4. Les logs sont souvent plus sensibles que les résultats : ils contiennent les prompts, les chemins, parfois les erreurs avec du contexte utile.
5. Le mélange des rôles — modèle, client, serveur, exécution — finit vite en casserole d’architecture.

Le remède est connu : least privilege, sandbox, réseau fermé par défaut, logs conscients, et séparation stricte entre le runtime du modèle et les outils à risque.

## Le bon modèle mental

Le vrai bénéfice de MCP en local n’est pas “on a un standard cool”. C’est :
- un protocole pour déclarer les capacités des outils ;
- un transport clair pour les exécuter ;
- un client qui garde la main sur les permissions ;
- un modèle local qui ne fait que proposer des actions, pas les auto-autoriser.

C’est beaucoup moins sexy qu’un agent magique. Et c’est précisément pour ça que ça marche.
