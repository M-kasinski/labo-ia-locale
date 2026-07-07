---
title: "BaseRT attaque llama.cpp et MLX sur leur terrain : le runtime Metal pur"
description: "BaseRT promet jusqu'à 1,56x de débit decode face à llama.cpp et 1,35x face à MLX sur Apple Silicon. Le signal important n'est pas seulement le score, c'est le retour du runtime comme avantage local."
pubDate: 2026-07-07
category: "local"
tags: ["basert", "apple-silicon", "metal", "mlx", "llama-cpp", "inference-locale", "runtime"]
author: "Labo IA"
draft: false
sources:
  - label: "arXiv — BaseRT: Best-in-Class LLM Inference on Apple Silicon via Native Metal"
    url: "https://arxiv.org/abs/2607.00501"
  - label: "GitHub — basecompute/baseRT"
    url: "https://github.com/basecompute/baseRT"
  - label: "GitHub Releases — BaseRT engine 0.1.4"
    url: "https://github.com/basecompute/baseRT/releases/tag/v0.1.4"
  - label: "BaseRT Docs"
    url: "https://docs.basecompute.co/"
---

BaseRT est le genre de signal qu'il ne faut pas rater quand on suit l'IA locale sur Mac. Le papier a été soumis sur arXiv le **1er juillet 2026**, le moteur **0.1.4** est publié sur GitHub depuis le **30 juin**, et le pitch est simple : arrêter de traiter Apple Silicon comme une cible secondaire.

Les auteurs présentent BaseRT comme un runtime d'inférence LLM natif Metal, optimisé pour la mémoire unifiée et les kernels propres aux puces Apple. Dans leurs mesures, il atteint jusqu'à **1,56x** le débit decode de `llama.cpp` et jusqu'à **1,35x** celui de MLX. Sur le prefill, les écarts seraient encore plus visibles pour certains MoE.

Ce n'est pas une petite querelle de benchmark. Si les chiffres se confirment hors papier, le vrai sujet de la semaine n'est pas "encore un modèle". C'est que le runtime redevient le champ de bataille.

## Pourquoi ca compte

Depuis un an, on a beaucoup regardé les poids : Qwen, Gemma, DeepSeek, Mistral, Llama, les quants GGUF, les variantes MLX. Mais sur une machine locale, le modèle ne travaille jamais seul. Il traverse un runtime, un format, une pile mémoire, un scheduler, des kernels, puis seulement ensuite il devient une expérience utilisateur.

BaseRT tape exactement dans cette couche. Le papier explique que les frameworks existants laissent du débit sur la table parce qu'ils ne sont pas entièrement construits autour du modèle d'exécution Metal et de la mémoire unifiée Apple. L'argument est crédible au moins comme direction : sur Mac, la RAM et la VRAM ne sont pas deux mondes séparés, et un runtime qui pense cette topologie dès le départ peut avoir un vrai avantage.

Les tests cités couvrent **Qwen3**, **Llama 3.2** et **Gemma 4**, en **Q4** et **Q8**, sur **M3** et **M4 Pro**, avec support annoncé de Q2 à FP16 sur toutes les machines Apple M-series. C'est exactement le type de matrice qu'on veut lire pour un MacBook Pro 48 Go ou un Mac Studio : pas un score cloud abstrait, mais des familles de modèles que l'on peut vraiment envisager de lancer localement.

## Le détail qui rend le sujet intéressant

Le repo ne se limite pas à une promesse de papier. BaseRT expose une CLI `basert` pour pull, convertir, chatter, servir et benchmarker. Il annonce aussi un serveur compatible OpenAI, du continuous batching, du paged-KV, du prefix caching, des bindings Python/Node/Rust/Swift, et un format `.base` avec quantization affine Q2 à Q8.

Autrement dit, l'ambition n'est pas seulement "voici un kernel rapide". C'est une pile complète : format modèle, runtime, CLI, API, bindings. C'est la même logique qui a fait la force de `llama.cpp` et d'Ollama : l'inférence locale devient utile quand elle a une surface produit, pas seulement quand elle gagne un graphe.

Il y a quand même une limite importante : le dépôt est sous Apache-2.0 pour l'écosystème, mais le moteur prébuildé est distribué sous une licence séparée propriétaire. Pour un blog IA locale, c'est un détail à surveiller. Open tooling ne veut pas toujours dire moteur entièrement open source.

## Ce que je testerais en premier

Sur Mac, le test intéressant n'est pas de chercher le record absolu. C'est de comparer trois usages concrets :

1. un petit Qwen3 ou Gemma interactif en chat ;
2. un modèle 7B/12B quantifié pour agent local avec appels outils ;
3. un long prompt qui force le prefill et expose les différences de runtime.

Il faudrait mesurer `llama.cpp`, MLX/MLX-LM et BaseRT sur les mêmes prompts, avec le même quant quand c'est possible, puis regarder trois chiffres : temps avant premier token, tokens/s en decode, et stabilité mémoire sur contexte long. Si BaseRT garde son avance dans ce test-là, il devient immédiatement un candidat sérieux pour le banc Mac.

## Lecture Labo IA

BaseRT rappelle une chose un peu brutale : l'IA locale ne se gagne pas seulement au leaderboard des modèles. Elle se gagne dans les couches basses qui rendent un modèle agréable, rapide et économique sur la machine que l'on a déjà.

Pour l'instant, il faut rester prudent. Les chiffres viennent du papier et du projet lui-même. Le repo est jeune, la release publique est récente, et l'écosystème autour de `.base` n'a pas encore la profondeur de GGUF ou MLX.

Mais c'est précisément pour ça que le sujet est bon. Il ouvre une piste testable : si un runtime Metal natif peut gagner 30 à 50 % sans changer de modèle, alors beaucoup de comparatifs "quel modèle local choisir ?" sont incomplets. La question devient plutôt : **quel couple modèle + runtime + format donne la meilleure expérience sur ton Mac ?**

Et là, on revient au vrai terrain du Labo IA : pas la grande messe de l'IA générale, mais le moment où un modèle tourne sur une machine locale, répond vite, ne chauffe pas trop, et devient enfin utilisable au quotidien.
