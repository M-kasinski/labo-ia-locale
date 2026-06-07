---
title: "mlxcel : un runtime Rust pour servir MLX sans Python sur Apple Silicon"
description: "Lablup publie mlxcel, un moteur d’inférence MLX en Rust avec serveur OpenAI-compatible. Intéressant pour Mac locaux, mais les benchmarks doivent être lus avec méthode."
pubDate: 2026-06-07
tags: ["mlx", "apple-silicon", "rust", "inference", "openai-compatible"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Dépôt GitHub — lablup/mlxcel"
    url: "https://github.com/lablup/mlxcel"
  - label: "Annonce Lablup — mlxcel open-source"
    url: "https://www.backend.ai/blog/2026-05-lablup-opensourced-mlxcel"
  - label: "Benchmark indépendant — Kubesimplify sur M1 Max"
    url: "https://blog.kubesimplify.com/mlxcel-rust-native-inference-engine-tested-on-m1-max"
---

La pile MLX sur Mac continue de se densifier. Après `mlx-lm`, `mlx-vlm`, Rapid-MLX, LM Studio et les intégrations Ollama, **mlxcel** ajoute une variation intéressante : un runtime d’inférence écrit majoritairement en **Rust**, qui appelle les bindings **MLX C++** et expose à la fois une CLI et un serveur HTTP compatible avec une partie de l’API OpenAI.

Le dépôt `lablup/mlxcel` indique une licence **Apache-2.0**, une implémentation Rust très majoritaire, et une release récente `v0.1.4` datée du **5 juin 2026**. Lablup présente le projet comme un moteur d’inférence LLM/VLM optimisé pour **Apple Silicon**, avec support Linux/CUDA en cible secondaire. Dit simplement : ce n’est pas un nouveau format de modèle, mais une nouvelle manière de servir des checkpoints **MLX** sans traîner toute une pile Python dans le chemin critique.

C’est utile, parce que l’IA locale sur Mac a changé de problème. Il y a deux ans, la question était : “est-ce que mon Mac peut lancer un modèle ?”. Aujourd’hui, elle devient : “est-ce que je peux le servir proprement à un agent, avec streaming, batching, cache de préfixe, redémarrage simple et supervision correcte ?”. mlxcel vise exactement cette couche.

## Ce que mlxcel apporte concrètement

Le README du projet décrit deux binaires principaux : `mlxcel`, pour l’usage CLI, et `mlxcel-server`, pour exposer un serveur compatible avec des endpoints de type `/v1/chat/completions`, `/v1/completions` et `/v1/responses`. Le projet annonce aussi le streaming SSE, le continuous batching, le prompt-prefix caching, le speculative decoding, la compression de KV cache et des modes multi-device/distribués pour certaines familles de modèles.

La différence avec `mlx-lm` n’est donc pas seulement “Rust contre Python”, même si c’est le signal le plus visible. Le point intéressant est opérationnel : un seul processus natif pour le chargement, la planification, l’inférence et le service HTTP. Pour un labo local, une app interne ou un agent de code branché sur une API OpenAI-compatible, c’est plus facile à packager qu’un environnement Python qu’il faut garder en état de marche. Le genre de détail ennuyeux qui devient soudain très important à 2 h du matin, quand ton agent refuse de démarrer parce qu’un paquet a décidé de vivre sa vérité.

L’installation documentée passe notamment par Homebrew :

```bash
brew tap lablup/tap
brew install mlxcel
```

Puis on peut lancer un modèle depuis Hugging Face, par exemple avec un nom complet ou un raccourci résolu vers `mlx-community`. Le dépôt documente aussi une commande `inspect` pour estimer le budget mémoire poids + KV cache avant de lancer une génération longue. C’est sain : sur Apple Silicon, la mémoire unifiée est confortable, mais elle n’est pas magique. Un modèle qui “rentre” sans contexte ne rentre pas forcément avec 32K tokens de KV cache.

## Les benchmarks : prometteurs, mais pas à lire comme une vérité générale

Lablup annonce des chiffres ambitieux. Dans son billet de lancement, l’entreprise affirme que mlxcel atteint en moyenne **119 % du débit de décodage de mlx-lm** et dépasse mlx-lm sur **95 % des modèles comparables**. Le même billet détaille des mesures réalisées sur un **MacBook Pro M5 Max** et un **Mac Studio M1 Ultra**, tous deux avec **128 Go** de mémoire unifiée. Sur texte, Lablup rapporte notamment un préfill médian de **2,70×** face à `mlx-lm` sur M5 Max et **1,76×** sur M1 Ultra, avec un décodage proche de la parité. Sur VLM, les résultats sont plus nuancés : certains cas sont au-dessus, d’autres non.

Ces chiffres sont intéressants, mais ils viennent de l’éditeur du runtime. Il faut donc les prendre comme une hypothèse technique solide, pas comme un verdict indépendant. C’est là que l’analyse de Kubesimplify est utile. Sur un **M1 Max 64 Go**, Saiyam Pathak observe une installation propre via Homebrew, une parité de décodage avec `mlx-lm`, et un avantage d’environ **1,3×** face à Ollama sur les modèles testés en GGUF/llama.cpp Metal. Son test sur **Llama 3.2 3B** donne par exemple environ **63,33 tok/s** pour mlxcel contre **48,73 tok/s** pour Ollama. Sur **Qwen 2.5 7B 4-bit**, il mesure **31,33 tok/s** pour mlxcel, **31,80 tok/s** pour `mlx-lm` et **24,23 tok/s** pour Ollama.

La nuance est importante : dans ce test indépendant, mlxcel ne pulvérise pas `mlx-lm` en décodage ; il se place surtout comme un chemin MLX natif plus facile à servir qu’un script Python, et souvent plus rapide qu’un chemin Ollama/llama.cpp Metal sur les cas mesurés. C’est déjà beaucoup, mais ce n’est pas de l’alchimie.

## Pourquoi c’est pertinent pour les agents locaux

Un agent local ne se comporte pas comme un chatbot classique. Il fait beaucoup de petites générations, relit les mêmes instructions système, manipule des schémas d’outils, reformate du JSON, appelle un service, puis recommence. Dans ce régime, trois dimensions comptent particulièrement :

1. **Le time-to-first-token et le préfill**, parce que l’agent réinjecte souvent du contexte.
2. **Le cache de préfixe**, parce que les outils et consignes changent peu d’une étape à l’autre.
3. **La couche serveur**, parce que les clients parlent déjà souvent OpenAI-compatible.

mlxcel coche plusieurs cases : serveur HTTP, streaming, batching continu, prompt-prefix caching et gestion mémoire documentée. Cela ne garantit pas qu’il sera meilleur que LM Studio, Rapid-MLX, Ollama MLX ou `mlx-lm` dans ton cas précis. Mais il devient une option crédible si tu veux un service local supervisable, avec peu de dépendances runtime, sur Mac.

Le support VLM annoncé est aussi à surveiller. Lablup liste plus de 80 architectures et des familles multimodales comme Gemma, LLaVA, Llama, MiniCPM, Molmo, Phi-Vision ou Qwen-VL. Là encore, prudence : “supporté” ne veut pas dire “rapide et stable sur mon prompt de production”. Mais pour les workflows locaux de documents, screenshots et agents d’ordinateur, le fait d’avoir un serveur MLX natif qui ne se limite pas au texte mérite attention.

## Les points faibles à garder en tête

Le projet est encore jeune : la série `v0.1.x` dit assez clairement qu’on n’est pas devant une brique figée. Certaines fonctions avancées — compression de KV cache, speculative decoding, modes distribués — doivent être validées modèle par modèle et charge par charge. Kubesimplify note par exemple que TurboQuant est prometteur, mais pas performant sur son M1 Max dans les tests réalisés. C’est typiquement le genre de fonctionnalité qui peut être excellente sur une génération de puce et décevante sur une autre.

Autre point : mlxcel sert des checkpoints MLX. Si ton écosystème repose sur GGUF, llama.cpp et des quantizations déjà validées, basculer vers MLX impose de changer de catalogue de modèles, de scripts de benchmark et parfois d’hypothèses mémoire. Sur Mac, cela peut valoir le coût. Sur une machine hybride, ou si tu synchronises avec des serveurs Linux, la réponse est moins évidente.

## À retenir

mlxcel n’est pas “le runtime qui remplace tout”. C’est plus intéressant que ça : un **serveur MLX natif en Rust**, Apache-2.0, pensé pour rendre l’inférence Apple Silicon plus déployable et moins dépendante de Python. Les premiers chiffres officiels sont ambitieux ; les mesures indépendantes disponibles sont plus sobres mais positives, surtout face aux chemins Ollama/llama.cpp Metal dans les cas testés.

Si tu fais tourner des agents locaux sur Mac, mlxcel vaut un essai sérieux. Pas avec un benchmark de démo : avec tes modèles, ta longueur de contexte, ton client OpenAI-compatible, ton cache chaud/froid et tes contraintes mémoire. Le Mac aime les nuances ; les tokens/s aussi.

## Sources

- [Dépôt GitHub — lablup/mlxcel](https://github.com/lablup/mlxcel)
- [Annonce Lablup — mlxcel open-source](https://www.backend.ai/blog/2026-05-lablup-opensourced-mlxcel)
- [Benchmark indépendant — Kubesimplify sur M1 Max](https://blog.kubesimplify.com/mlxcel-rust-native-inference-engine-tested-on-m1-max)
