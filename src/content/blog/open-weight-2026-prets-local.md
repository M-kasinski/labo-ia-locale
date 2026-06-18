---
title: "Open-weight 2026 : les modèles déjà prêts pour le local"
description: "Une sélection prudente des modèles open-weight récents dont les poids, les quants et les runtimes locaux sont déjà utilisables."
pubDate: 2026-05-29
category: "local"
tags: ["ia-locale", "open-weight", "gemma", "qwen", "modeles"]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "Google Gemma 4 — modèle card Hugging Face", url: "https://huggingface.co/google/gemma-4-31B-it" }
  - { label: "Google Gemma 4 — licence officielle", url: "https://ai.google.dev/gemma/docs/gemma_4_license" }
  - { label: "Unsloth Gemma 4 26B-A4B IT GGUF", url: "https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF" }
  - { label: "MLX Community Gemma 4 31B IT 8-bit", url: "https://huggingface.co/mlx-community/gemma-4-31b-it-8bit" }
  - { label: "Cyankiwi Gemma 4 26B-A4B IT AWQ 4-bit", url: "https://huggingface.co/cyankiwi/gemma-4-26B-A4B-it-AWQ-4bit" }
  - { label: "Qwen3.6-27B — modèle card Hugging Face", url: "https://huggingface.co/Qwen/Qwen3.6-27B" }
  - { label: "Qwen3.6-35B-A3B — modèle card Hugging Face", url: "https://huggingface.co/Qwen/Qwen3.6-35B-A3B" }
  - { label: "Unsloth Qwen3.6-27B MTP GGUF", url: "https://huggingface.co/unsloth/Qwen3.6-27B-MTP-GGUF" }
  - { label: "Unsloth Qwen3.6-35B-A3B MTP GGUF", url: "https://huggingface.co/unsloth/Qwen3.6-35B-A3B-MTP-GGUF" }
  - { label: "MLX Community Qwen3.6-35B-A3B 4-bit", url: "https://huggingface.co/mlx-community/Qwen3.6-35B-A3B-4bit" }
  - { label: "Cyankiwi Qwen3.6-27B AWQ INT4", url: "https://huggingface.co/cyankiwi/Qwen3.6-27B-AWQ-INT4" }
  - { label: "Mistral Ministral 3 3B Instruct 2512", url: "https://huggingface.co/mistralai/Ministral-3-3B-Instruct-2512" }
  - { label: "Mistral Ministral 3 8B Instruct 2512 GGUF", url: "https://huggingface.co/mistralai/Ministral-3-8B-Instruct-2512-GGUF" }
  - { label: "Unsloth Ministral 3 14B Instruct 2512 GGUF", url: "https://huggingface.co/unsloth/Ministral-3-14B-Instruct-2512-GGUF" }
---

Le bon critère pour une stack locale en 2026 n’est plus seulement “le modèle est-il bon ?”. C’est plutôt : est-ce que les poids sont ouverts, est-ce que la licence est lisible, est-ce que des quants existent déjà, et est-ce qu’un runtime sait vraiment le lancer sans séance d’archéologie ?

C’est là que le marché a changé. Il y a deux ans, une sortie de modèle signifiait souvent attendre : attendre les conversions GGUF, attendre les recettes MLX, attendre que vLLM, SGLang ou llama.cpp rattrapent l’architecture. Aujourd’hui, pour quelques familles bien choisies, le pipeline “sortie → quants → usage local” se compte plutôt en jours. Pas pour tout le monde, pas toujours proprement, mais assez souvent pour modifier une stack locale.

Cette sélection garde donc uniquement les modèles dont on peut confirmer les quatre cases : nom exact, taille, licence, et disponibilité locale concrète.

## La sélection courte

| modèle | tailles | licence | quants dispo |
|---|---:|---|---|
| Google Gemma 4 | E2B : 2,3B effectifs / 5,1B avec embeddings ; E4B : 4,5B / 8B ; 26B-A4B : 25,2B total / 3,8B actifs ; 31B : 30,7B | Apache 2.0 | GGUF, MLX, AWQ selon variantes |
| Qwen3.6 | 27B ; 35B-A3B : 35B total / 3B actifs | Apache 2.0 | GGUF MTP, MLX, AWQ |
| Ministral 3 | 3B, 8B, 14B | Apache 2.0 | GGUF, plus service vLLM côté cartes officielles |

Ce tableau n’est volontairement pas un palmarès de benchmark. C’est une shortlist d’exploitation locale : moins sexy qu’un graphe de scores, mais beaucoup plus utile quand il faut choisir quoi mettre dans Ollama, llama.cpp, MLX ou un serveur vLLM.

## Gemma 4 : le retour utile de la licence simple

Gemma 4 mérite une place parce que Google a corrigé le point qui freinait souvent les déploiements sérieux : la licence. Les cartes Hugging Face Gemma 4 indiquent `license: apache-2.0` et renvoient vers la licence Gemma 4 officielle. C’est le genre de détail administratif qui change tout quand on sort du test du dimanche soir.

La famille est aussi claire côté tailles. Les petites variantes sont nommées E2B et E4B : Google précise qu’il s’agit de 2,3B et 4,5B paramètres “effectifs”, avec respectivement 5,1B et 8B paramètres en incluant les embeddings. Le modèle 31B est listé à 30,7B paramètres. La variante MoE `gemma-4-26B-A4B` est annoncée à 25,2B paramètres totaux, 3,8B actifs, avec 8 experts actifs sur 128 plus un expert partagé.

Pour une stack locale, le point fort est l’arrivée rapide des formats. On trouve déjà des dépôts GGUF pour `gemma-4-26B-A4B-it` et `gemma-4-31B-it`, des conversions MLX comme `mlx-community/gemma-4-31b-it-8bit`, et des quants AWQ comme `cyankiwi/gemma-4-26B-A4B-it-AWQ-4bit`. En pratique, cela ouvre trois routes : llama.cpp/Ollama/LM Studio via GGUF, Apple Silicon via MLX, GPU NVIDIA via AWQ.

La réserve : Gemma 4 est multimodal dans plusieurs variantes, et tous les runtimes locaux ne couvrent pas forcément les mêmes chemins texte, vision et audio. Pour une stack robuste, il faut donc choisir la variante selon l’usage réel : E4B pour machine modeste, 26B-A4B pour compromis MoE, 31B pour qualité texte plus lourde. Le nom du modèle ne suffit pas ; il faut regarder le format exact du dépôt quantifié.

## Qwen3.6 : le candidat local le plus directement actionnable

Qwen3.6 coche la case “prêt pour le local” encore plus franchement. Les cartes officielles Hugging Face de `Qwen/Qwen3.6-27B` et `Qwen/Qwen3.6-35B-A3B` indiquent Apache 2.0, avec fichiers de licence Apache dans les dépôts. Les tailles sont explicites : 27B pour le dense ; 35B au total et 3B activés pour le MoE `35B-A3B`.

Le détail important est le MTP, pour Multi-Token Prediction. Les cartes Qwen mentionnent que les modèles sont entraînés avec des étapes MTP. Les dépôts Unsloth `Qwen3.6-27B-MTP-GGUF` et `Qwen3.6-35B-A3B-MTP-GGUF` fournissent déjà les GGUF et documentent l’usage avec llama.cpp, dont l’option `--spec-type draft-mtp --spec-draft-n-max 2`. Unsloth annonce un gain d’inférence de l’ordre de 1,5 à 2x ; à prendre comme revendication fournisseur, mais l’existence du chemin runtime est, elle, vérifiable.

C’est surtout le 35B-A3B qui illustre le changement de génération. Sur le papier, 35B peut sembler trop gros pour du local confortable. Mais avec 3B actifs et des quants 4-bit, il devient beaucoup plus intéressant pour une machine personnelle correctement dotée. Les conversions MLX existent déjà, par exemple `mlx-community/Qwen3.6-35B-A3B-4bit`, et les AWQ sont disponibles via des dépôts comme `cyankiwi/Qwen3.6-27B-AWQ-INT4` ou les variantes AWQ du 35B-A3B.

La recommandation est nette : si l’objectif est un assistant local généraliste ou code avec un bon rapport effort/résultat, Qwen3.6 est aujourd’hui le premier dossier à ouvrir. La prudence reste de mise sur MTP : il faut un runtime récent et les bons réglages. Sans cela, on a juste un GGUF de plus, pas l’effet d’accélération promis.

## Ministral 3 : moins bruyant, mais propre pour les stacks contrôlées

Mistral reste pertinent dans cette sélection pour une raison simple : licence Apache 2.0, tailles lisibles, et chemins runtime officiels. Les dépôts `Ministral-3-3B-Instruct-2512`, `Ministral-3-8B-Instruct-2512` et `Ministral-3-14B-Instruct-2512` documentent l’usage vLLM, avec recommandation de version vLLM récente sur les cartes des modèles BF16. Côté local pur, Mistral publie aussi un dépôt GGUF officiel pour `Ministral-3-8B-Instruct-2512-GGUF`, et Unsloth fournit un GGUF pour `Ministral-3-14B-Instruct-2512`.

Ce n’est pas forcément le choix le plus spectaculaire face à Qwen3.6. Mais pour une stack où l’on veut une licence permissive, un modèle instruct stable et des tailles classiques — 3B pour laptop, 8B pour usage courant, 14B pour marge de qualité — Ministral 3 est un bon candidat. Le 8B GGUF officiel est particulièrement rassurant : moins d’intermédiaires, moins de bricolage.

## Ce que l’effet MTP change vraiment

Le MTP ne rend pas magiquement un modèle plus intelligent. Il raccourcit le coût de génération lorsque le runtime sait exploiter plusieurs prédictions de tokens. Pour le local, c’est très concret : moins de latence perçue, meilleur débit, et donc plus de modèles “limite” qui deviennent agréables.

Mais il introduit aussi un nouveau filtre de sélection. Un modèle “MTP” sans quant adapté, sans build llama.cpp compatible, ou sans configuration documentée n’est pas encore prêt. À l’inverse, Qwen3.6 montre ce que devient une sortie moderne : poids officiels Apache, quants GGUF MTP quasi immédiats, conversions MLX et AWQ, et commandes runtime publiées. C’est exactement le pipeline court que l’on veut voir.

## Verdict

Pour une stack locale neuve, je commencerais par Qwen3.6 : `27B` si l’on veut rester dense et prévisible, `35B-A3B` si l’on accepte le MoE et que l’on veut profiter du ratio actifs/qualité. Gemma 4 vient juste derrière, surtout grâce à Apache 2.0 et à la diversité de tailles, avec une attention particulière au 26B-A4B. Ministral 3 complète la sélection pour les déploiements sobres, permissifs et moins expérimentaux.

Le vrai signal de 2026 n’est donc pas seulement l’ouverture des poids. C’est la compression du délai entre annonce et usage réel. Quand un modèle arrive déjà accompagné de GGUF, MLX, AWQ et d’un runtime documenté, il cesse d’être une promesse. Il devient une pièce de stack.
