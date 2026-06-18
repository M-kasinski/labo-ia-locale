---
title: "Rapid-MLX : le serveur local qui pousse MLX vers les agents Apple Silicon"
description: "Rapid-MLX expose une API OpenAI-compatible sur Mac, avec tool calling, cache de prompt et claims de performances ambitieux. Prometteur, mais à benchmarker soi-même."
pubDate: 2026-06-01
category: "local"
tags: ["mlx", "apple-silicon", "agents", "inference", "openai-compatible"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Dépôt GitHub — raullenchai/Rapid-MLX"
    url: "https://github.com/raullenchai/Rapid-MLX"
  - label: "Discussion LlamaIndex — Rapid-MLX provider"
    url: "https://github.com/run-llama/llama_index/discussions/21123"
  - label: "Analyse MLX sur Apple Silicon — yage.ai"
    url: "https://yage.ai/share/mlx-apple-silicon-en-20260331.html"
---

Rapid-MLX est un projet à surveiller si tu utilises un Mac Apple Silicon pour faire tourner des agents locaux. L’idée est simple : prendre **MLX**, le framework d’Apple taillé pour la mémoire unifiée des puces M, et l’emballer dans un serveur d’inférence pratique, compatible avec les API que les outils savent déjà parler.

Le dépôt GitHub le présente comme un moteur local pour Mac, **OpenAI-compatible**, capable de fonctionner avec Cursor, Claude Code, Aider, OpenCode, Continue, LangChain, LlamaIndex, smolagents ou Open WebUI. Dit autrement : au lieu de modifier tout ton stack agentique, tu changes l’URL de base vers `http://localhost:8000/v1` et tu fais croire au client qu’il parle à une API OpenAI. Vieille astuce, toujours efficace.

## Ce que Rapid-MLX essaie de résoudre

Sur Apple Silicon, il existe déjà plusieurs chemins pour l’inférence locale : **llama.cpp/Metal**, **Ollama**, **LM Studio**, **mlx-lm**, et maintenant une galaxie de serveurs plus spécialisés. Le problème n’est plus seulement “peut-on lancer un modèle ?”. Le problème devient : peut-on le servir assez vite, avec du streaming, du tool calling, des sorties structurées, du cache, et une intégration propre dans les agents de code ?

Rapid-MLX vise précisément cette couche. Le dépôt annonce :

- une API **OpenAI-compatible** (`/v1/chat/completions`) ;
- une API **Anthropic-compatible** (`/v1/messages`) ;
- du **tool calling** avec 17 formats de parseurs ;
- une récupération automatique quand des modèles quantifiés cassent la structure des tool calls ;
- la séparation du raisonnement dans `reasoning_content` ;
- un cache de prompt avec trimming du KV cache et snapshots d’état pour certains modèles hybrides ;
- du streaming, du JSON structuré, des logprobs, de la vision/audio/embeddings via extras ;
- des mécanismes expérimentaux comme DFlash, SuffixDecoding et MTP.

C’est beaucoup. La partie intéressante n’est pas la liste façon brochure, c’est le ciblage : Rapid-MLX ne cherche pas seulement à être un “chat local”. Il veut être une brique serveur pour des **agents locaux**.

## Les claims de performance : séduisants, mais à prendre comme point de départ

Le dépôt annonce jusqu’à **4,2× plus rapide qu’Ollama**, **0,08 s de time-to-first-token en cache**, et souvent **2× à 4× plus rapide** qu’Ollama/llama.cpp sur Apple Silicon. La discussion LlamaIndex publiée par l’auteur donne deux chiffres concrets : **Qwen3.5-9B à 79 tok/s contre 33 tok/s avec Ollama**, et **Qwen3.5-4B à 168 tok/s sur un MacBook Air 16 Go**.

Ces résultats sont intéressants, mais ils viennent du projet lui-même ou de messages de présentation. Il faut donc les traiter comme des claims vérifiables, pas comme un benchmark indépendant définitif. Si tu l’installes, lance le script de benchmark fourni (`scripts/benchmark_engines.py`) sur tes propres prompts, avec tes modèles, et compare contre Ollama, llama.cpp brut et mlx-lm. L’écart peut changer selon le modèle, la quantization, la longueur de prompt, la proportion préfill/décode et le nombre de requêtes concurrentes.

L’analyse de yage.ai sur MLX donne un bon cadre : MLX semble particulièrement fort sur la phase de **decode** — la génération token par token — surtout avec des modèles MoE. Mais elle nuance aussi les comparaisons trop simples contre Ollama. Une partie du gain observé face à Ollama peut venir de l’overhead de la couche serveur Ollama, pas seulement d’une supériorité absolue de MLX sur llama.cpp. Selon cette analyse, l’avantage réel de MLX sur llama.cpp brut serait plutôt autour de **1,4× à 1,8×** dans certains cas, et MLX peut être moins favorable en **prefill**, donc sur les prompts courts ou les conversations qui changent beaucoup de contexte.

C’est exactement le genre de nuance qu’il faut garder. Les benchmarks “tok/s” sont utiles ; ils deviennent vite trompeurs quand on mélange cache chaud, prompt court, MoE, quantization et client HTTP.

## Pourquoi les agents locaux changent l’équation

Pour un simple chatbot, quelques tokens/s de plus ou de moins ne changent pas toujours la vie. Pour un agent, si.

Un agent local passe son temps à : lire un état, appeler un outil, résumer le résultat, décider du prochain outil, reformater en JSON, recommencer. Dans ce régime, trois choses comptent énormément :

1. **TTFT faible** : l’agent ne doit pas attendre une éternité entre deux micro-actions.
2. **Tool calling robuste** : une sortie JSON cassée peut tuer tout le workflow.
3. **Cache utile** : les instructions système, définitions d’outils et contexte projet reviennent souvent.

Rapid-MLX attaque ces trois points. Le support de nombreux parseurs de tool calls est particulièrement intéressant, parce que les familles de modèles ne respectent pas toutes les mêmes conventions. Qwen, GLM, GPT-OSS, Kimi et consorts ont chacun leurs bizarreries. Un serveur local qui répare ou normalise ces sorties peut éviter beaucoup de colle côté orchestrateur.

C’est aussi une bonne direction pour les stacks de code local. Cursor, Aider, Claude Code-like, OpenCode ou des agents maison veulent surtout une API compatible, rapide, et suffisamment stricte pour ne pas transformer chaque appel d’outil en séance d’exorcisme JSON.

## Installation et usage : le chemin prévu

Le dépôt propose plusieurs installations : Homebrew, pip, ou script d’installation. Le chemin recommandé est :

```bash
brew install raullenchai/rapid-mlx/rapid-mlx
```

Puis un chat local :

```bash
rapid-mlx chat
```

Ou un serveur OpenAI-compatible :

```bash
rapid-mlx serve qwen3.5-4b
```

L’endpoint attendu est ensuite :

```text
http://localhost:8000/v1
```

Côté client Python, c’est le schéma classique : `OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")`. La discussion LlamaIndex montre la même idée avec `OpenAILike`, ce qui permet d’intégrer Rapid-MLX comme fournisseur local sans écrire un adaptateur spécifique.

Le dépôt indique une plateforme Apple Silicon **M1 à M4**, Python **3.10+**, et une licence **Apache 2.0**. Il liste aussi un écosystème assez vivant : plusieurs centaines de commits, de nombreux tags, et une release visible **v0.6.69** datée du 30 mai 2026 dans l’extraction consultée.

## Limites et points à vérifier

Rapid-MLX est prometteur, mais il faut éviter l’adoption à l’aveugle. Les points à tester :

- **Stabilité serveur** sur sessions longues avec agents ;
- **validité des tool calls** sur tes modèles réellement utilisés ;
- **comparaison froide/chaude** : premier prompt, cache chaud, contexte qui grandit ;
- **prefill** sur gros prompts de code ou RAG ;
- **mémoire** sous pression, surtout sur Mac 16 ou 24 Go ;
- **compatibilité client** avec Cursor, Aider, LlamaIndex ou ton orchestrateur maison.

Il faut aussi surveiller le rythme de changement. Un projet qui bouge vite est utile, mais cela veut dire que les comportements peuvent changer entre deux releases. Pour un usage sérieux, verrouille la version et garde un benchmark de régression minimal.

## Verdict provisoire

Rapid-MLX est intéressant parce qu’il prend MLX au sérieux comme backend d’agents, pas seulement comme jouet de génération locale. L’API compatible OpenAI, le tool calling multi-format, le cache de prompt et l’intégration avec les outils existants répondent à de vrais irritants.

Je ne considérerais pas encore ses chiffres de performance comme une vérité générale. Je les prendrais comme une invitation à tester. Mais si tu as un Mac Apple Silicon et que tes agents locaux passent aujourd’hui par Ollama ou llama.cpp avec une latence frustrante, Rapid-MLX mérite clairement une place dans ton banc d’essai.
