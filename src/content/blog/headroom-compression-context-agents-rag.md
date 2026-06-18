---
title: "Headroom : compresser le contexte avant que l’agent local ne s’étouffe"
description: "Headroom propose une couche locale pour compresser sorties d’outils, logs, fichiers et chunks RAG, avec proxy, SDK et serveur MCP. Prometteur, mais à benchmarker chez soi."
pubDate: 2026-06-06
category: "local"
tags: ["agents", "mcp", "rag", "auto-hébergement"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub — chopratejas/headroom"
    url: "https://github.com/chopratejas/headroom"
  - label: "Documentation — Headroom"
    url: "https://chopratejas.github.io/headroom/"
  - label: "GitHub — Headroom benchmarks"
    url: "https://github.com/chopratejas/headroom/blob/main/docs/content/docs/benchmarks.mdx"
---

Les agents locaux ont un problème très simple : ils lisent trop. Trop de logs, trop de JSON, trop de fichiers, trop de chunks RAG, trop de sorties shell verbeuses qui racontent leur vie avec l’élégance d’un conteneur Docker en mode debug. **Headroom** arrive sur ce terrain avec une proposition claire : compresser tout ce que l’agent consomme **avant** que cela n’entre dans le modèle.

Le projet se présente comme une “context compression layer for AI agents”. Le dépôt GitHub annonce une release **v0.23.0 publiée le 4 juin 2026**, une licence **Apache 2.0**, et plusieurs modes d’usage : bibliothèque Python/TypeScript, proxy compatible OpenAI, wrapper pour agents de code, serveur MCP, mémoire inter-agents et compression réversible. Le pitch est ambitieux : **60 à 95 % de tokens en moins** sur les sorties d’outils, logs, fichiers et chunks RAG, avec des réponses conservées. C’est le genre de promesse qu’il faut lire avec intérêt, puis tester sans pitié.

## Le vrai sujet : pas le contexte, le bruit

On parle beaucoup de fenêtres de contexte longues. 128K, 256K, 1M tokens : la course ressemble parfois à un concours de coffre de voiture. Mais dans les workflows agentiques, le problème n’est pas seulement la taille maximale. C’est la quantité de bruit envoyé au modèle.

Un agent qui inspecte un dépôt peut lire un fichier entier pour ne retenir qu’une signature de fonction. Un agent RAG peut récupérer huit passages dont trois contiennent seulement des métadonnées répétitives. Un agent DevOps peut avaler 2 000 lignes de logs pour repérer une seule erreur `FATAL`. Même avec un grand contexte, ce bruit coûte du temps, de l’argent si vous utilisez une API, et de la qualité attentionnelle. En local, il coûte surtout de la latence et de la mémoire. Charmant, comme payer un déménageur pour transporter de l’air.

Headroom s’intercale entre l’application ou l’agent et le fournisseur LLM. Sa documentation liste plusieurs formes d’intégration : proxy transparent, fonction `compress()`, middleware TypeScript, callback LiteLLM, intégrations LangChain/Agno/Strands, wrapper pour Claude Code, Codex, Cursor, Aider, Copilot, et serveur MCP. Pour une stack locale, le point intéressant est le serveur MCP : il expose notamment `headroom_compress`, `headroom_retrieve` et `headroom_stats`, ce qui permet à un agent compatible MCP d’utiliser la compression comme outil.

## Compression réversible : le détail qui évite le massacre

La compression de contexte peut vite devenir dangereuse. Si l’outil supprime une ligne critique, l’agent raisonne sur une version appauvrie du monde. Headroom essaie de limiter ce risque avec une architecture **CCR — Compress, Cache, Retrieve**. D’après le README, les originaux ne sont pas supprimés : ils sont stockés localement, et le modèle peut récupérer le contenu complet à la demande via un outil de retrieval.

C’est une bonne direction. Elle transforme la compression en résumé consultable plutôt qu’en perte irréversible. Dans un workflow RAG, par exemple, l’agent peut recevoir une version condensée de plusieurs chunks puis demander le texte complet d’un passage s’il devient central. Dans un workflow code, il peut voir une forme compressée d’un fichier ou d’un résultat de recherche, puis récupérer l’original avant de modifier quoi que ce soit.

Le dépôt décrit aussi plusieurs composants spécialisés : `ContentRouter` pour détecter le type de contenu, `SmartCrusher` pour JSON et données structurées, `CodeCompressor` basé sur l’AST pour le code, `Kompress-base` pour le texte, et `CacheAligner` pour stabiliser les préfixes afin de mieux profiter des caches KV côté fournisseur. Cette approche par type de contenu est plus crédible qu’un simple résumé LLM générique appliqué partout.

## Où ça s’insère dans une stack locale

Le cas d’usage évident est l’agent de code local. Architecture typique : un modèle via Ollama, llama.cpp, MLX ou vLLM ; un client agentique compatible MCP ; des outils filesystem/Git/shell ; et Headroom devant les sorties volumineuses. L’agent ne reçoit plus chaque sortie brute dans son intégralité. Il reçoit une version compressée, avec possibilité de récupérer l’original.

Deuxième cas : **RAG auto-hébergé**. Beaucoup de pipelines locaux récupèrent trop large, parce qu’il est difficile de savoir à l’avance quel chunk sera utile. Une couche comme Headroom peut compresser les résultats de retrieval avant injection dans le prompt. Cela ne remplace pas un bon reranker, ni une stratégie de chunking correcte, mais cela peut réduire les dégâts quand le retriever ramène de la matière redondante.

Troisième cas : orchestration multi-agents. La documentation Headroom mentionne une mémoire partagée inter-agents avec déduplication et provenance. Dans une équipe d’agents — un qui explore, un qui code, un qui teste — le transfert de contexte devient vite incontrôlable. Une mémoire compressée et récupérable peut aider à éviter que chaque agent renvoie toute l’histoire à chaque étape.

## Les chiffres : utiles, mais auto-déclarés

Headroom revendique des réductions fortes : le README annonce **60–95 % de tokens en moins**, le site parle d’une **réduction moyenne de 87 %**, et la page de benchmarks mentionnée par GitHub évoque une télémétrie de plus de 250 instances proxy, avec compression plus modeste sur les conversations courtes et **40–80 %** sur les sessions lourdes en tool-use. Le dépôt donne aussi des exemples de logs compressés, comme une sortie passant de **10 144 à 1 260 tokens** tout en conservant l’erreur importante.

Ces chiffres viennent du projet lui-même. Ils sont intéressants pour cadrer, mais ils ne suffisent pas à valider un déploiement. Il manque, au moment de cette veille, des benchmarks indépendants solides sur des workloads variés : code réel, RAG multilingue, logs de production, JSON imbriqué, documents juridiques, prompts français, modèles locaux petits et moyens. Il faut donc traiter Headroom comme un outil prometteur, pas comme une loi physique.

Le bon test est simple : prenez vos traces réelles, mesurez tokens, latence, erreurs et taux de récupération d’originaux. Puis comparez avec votre pipeline actuel. Si la compression réduit le contexte mais augmente les erreurs de décision, le gain est cosmétique. Si elle réduit fortement les tokens sans perte observable sur vos tâches, là, on commence à parler sérieusement.

## Les risques à surveiller

Premier risque : la confiance excessive. Une compression peut masquer une nuance, un avertissement ou une ligne d’erreur secondaire. Pour les modifications de code, l’agent doit toujours relire l’original avant d’éditer. Pour les décisions RAG sensibles, il doit citer ou récupérer le passage complet.

Deuxième risque : la surface de sécurité. Headroom fonctionne localement selon sa documentation, ce qui est positif, mais il peut lire sorties d’outils, fichiers, logs et conversations. Dans un environnement professionnel, cela mérite les mêmes réflexes qu’un indexeur de code ou qu’un serveur MCP : audit de configuration, limitation des chemins accessibles, secrets exclus, logs maîtrisés.

Troisième risque : l’ajout d’une couche de complexité. Un proxy de compression peut rendre le debug plus difficile si l’on ne conserve pas les originaux et les statistiques. Le fait que Headroom expose `headroom_stats` est donc important : sans observabilité, une couche magique devient vite une couche suspecte.

## Verdict local

Headroom cible un vrai goulot d’étranglement des agents locaux : pas seulement “avoir assez de contexte”, mais **ne pas gaspiller le contexte disponible**. Son support MCP, son fonctionnement local-first, sa compression réversible et ses intégrations proxy/SDK en font un candidat sérieux pour les stacks auto-hébergées.

Mais l’outil doit être évalué sur données réelles. Les gains auto-déclarés sont plausibles sur logs, JSON et sorties répétitives ; ils seront probablement plus variables sur prose dense ou documents déjà bien chunkés. En clair : Headroom mérite un essai contrôlé, pas une adoption religieuse. Ce qui, dans ce secteur, est déjà une forme de sagesse rare.

## Sources

- GitHub — `chopratejas/headroom` : https://github.com/chopratejas/headroom
- Documentation — Headroom : https://chopratejas.github.io/headroom/
- GitHub — Headroom benchmarks : https://github.com/chopratejas/headroom/blob/main/docs/content/docs/benchmarks.mdx
