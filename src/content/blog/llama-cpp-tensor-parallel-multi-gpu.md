---
title: "llama.cpp muscle le multi-GPU : le mode tensor devient le vrai sujet local"
description: "Le support expérimental du tensor parallelism dans llama.cpp change la donne pour les homelabs multi-GPU, mais il reste à manier avec précaution."
pubDate: 2026-06-05
tags: ["llama.cpp", "multi-GPU", "inference", "CUDA", "homelab"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "PR officielle llama.cpp #19378 — backend-agnostic tensor parallelism"
    url: "https://github.com/ggml-org/llama.cpp/pull/19378"
  - label: "Documentation officielle llama.cpp — Using Multiple GPUs"
    url: "https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md"
  - label: "Analyse indépendante — llama.cpp performance breakthrough for multi-GPU setups"
    url: "https://medium.com/@jagusztinl/llama-cpp-performance-breakthrough-for-multi-gpu-setups-04c83a66feb2"
---

Le multi-GPU dans **llama.cpp** a longtemps été un compromis assez simple : tu pouvais répartir un modèle sur plusieurs cartes pour gagner de la VRAM, mais pas forcément pour gagner beaucoup en génération token par token. La nouveauté qui mérite attention, c’est l’arrivée du **tensor parallelism expérimental** via `--split-mode tensor`, introduit dans la PR officielle `ggml-org/llama.cpp#19378` et désormais documenté dans le guide multi-GPU du projet.

Le signal a refait surface ces derniers jours dans l’écosystème local, notamment autour des gains récents obtenus avec NVIDIA et ggml. Mais les sources vraiment exploitables ne sont pas les posts sociaux : ce sont la PR upstream, la documentation officielle, et les analyses techniques qui expliquent la différence entre les modes de split. Et cette différence compte, parce qu’elle touche directement les machines que beaucoup construisent pour l’IA locale : deux RTX d’occasion, un serveur homelab, parfois un Frankenstein PCIe qui ronronne sous le bureau avec la grâce d’un grille-pain anxieux.

## Avant : surtout répartir la mémoire

La documentation officielle de llama.cpp distingue plusieurs modes multi-GPU via `--split-mode` ou `-sm`. Le mode par défaut est **`layer`**. Il fait de la pipeline parallelization : chaque GPU possède une tranche contiguë de couches, et le KV cache d’une couche vit sur le GPU qui possède cette couche. C’est le mode le plus compatible, utile quand le modèle ne rentre pas dans la VRAM d’une seule carte ou quand on veut un prefill rapide sans dépendre d’un interconnect très rapide.

Ce mode a un avantage évident : il est robuste. Il tolère mieux les configurations imparfaites, les GPU hétérogènes, et les interconnexions PCIe modestes. Mais il a aussi une limite : pendant la génération séquentielle, toutes les cartes ne travaillent pas toujours comme on l’espérerait. On gagne de la capacité mémoire, parfois du débit en batch/prefill, mais pas forcément une latence token par token spectaculaire.

Le mode **`row`**, lui, est désormais indiqué comme **déprécié** dans la documentation officielle. Il s’agissait d’un ancien chemin tensor-parallel qui divisait seulement certains poids denses. La doc conseille clairement de l’éviter pour les nouveaux déploiements, puisqu’il est remplacé par `tensor`.

## Maintenant : `--split-mode tensor`

La PR `#19378` ajoute un support initial de **tensor parallelism backend-agnostic** dans ggml/llama.cpp. L’activation se fait avec :

```bash
llama-cli -m model.gguf -sm tensor
```

ou, dans la forme longue :

```bash
llama-cli -m model.gguf --split-mode tensor
```

L’idée n’est pas seulement de placer des couches différentes sur des GPU différents. Le nouveau chemin crée un backend “meta” qui enveloppe plusieurs backends ggml classiques et permet de traiter plusieurs GPU comme un ensemble coordonné. La PR explique que ce meta backend infère l’état de split des tenseurs à partir du graphe de calcul ggml, puis synchronise seulement aux endroits nécessaires au lieu de synchroniser après chaque opération.

C’est ce point qui rend l’approche intéressante : elle vise à paralléliser le calcul lui-même, pas seulement à distribuer le modèle. La documentation officielle résume bien le compromis : le mode `layer` maximise plutôt le throughput en pipeline, tandis que le mode `tensor` cherche plutôt à minimiser la latence en divisant chaque couche entre plusieurs GPU. En échange, `tensor` dépend beaucoup plus de la vitesse d’interconnexion entre cartes, parce qu’il implique plusieurs réductions inter-GPU par couche.

## Ce que ça change pour un homelab local

Pour une machine locale avec plusieurs GPU NVIDIA, `--split-mode tensor` peut devenir le mode à tester quand la priorité est la génération rapide, pas seulement le fait de charger un modèle trop gros. La documentation officielle le décrit comme expérimental, utile quand on veut plus de VRAM et une génération token par token plus rapide, surtout avec de grands modèles denses et un interconnect rapide.

Concrètement, cela peut intéresser trois profils :

1. **Les homelabs multi-RTX** qui veulent exploiter deux ou trois cartes au lieu d’en laisser une attendre.
2. **Les serveurs locaux d’agents** où la latence de génération compte plus que le débit batch massif.
3. **Les gros modèles GGUF** qui rentrent tout juste sur plusieurs GPU et dont le mode `layer` ne tire pas assez parti du compute disponible.

Mais il ne faut pas vendre ça comme une baguette magique. La PR officielle dit explicitement que le support est **expérimental** et “not yet production ready”. La documentation officielle garde le même ton : `tensor` est un mode à tester, pas le nouveau défaut universel.

## Les contraintes techniques à ne pas ignorer

La documentation officielle liste plusieurs prérequis importants pour `--split-mode tensor`. D’abord, **FlashAttention doit être activé**. Si `--flash-attn off` est utilisé, ou si `auto` résout vers `off`, c’est une erreur. Ensuite, le KV cache doit rester dans un type non quantifié : `f32`, `f16` ou `bf16`. Les caches quantifiés ne sont pas supportés dans ce mode au moment documenté.

La PR mentionne aussi que `-fit`, l’auto-ajustement de certains paramètres à la mémoire disponible, n’est pas implémenté pour ce chemin. En clair : il peut falloir définir manuellement `--ctx-size`, surveiller la VRAM, et accepter de tâtonner. Pour une machine locale, c’est acceptable en labo ; pour un service de production auto-hébergé, c’est un risque opérationnel.

Autre point : la PR indique que CUDA est le terrain le plus crédible pour de bonnes performances, avec **NCCL recommandé**. ROCm/HIP fonctionne en théorie via la traduction du code CUDA, mais l’auteur de la PR signale des performances pauvres dans ses tests. Vulkan est mentionné comme problématique ou instable selon les cas. Donc, si ton setup est AMD ou Vulkan-first, `tensor` est à considérer comme expérimental au carré. Oui, c’est une unité scientifique : l’expérimental au carré, c’est quand le README te tutoie avant de planter.

## Et les performances ? Prudence sur les chiffres

L’analyse de László Jagusztin sur Medium, publiée en janvier 2026 autour d’un fork performant (`ik_llama.cpp`) et d’un “Split Mode Graph”, rapporte des gains de **3x à 4x** sur des setups multi-GPU CUDA, avec une meilleure utilisation simultanée des cartes. L’article explique que l’approche consiste à distribuer le graphe de calcul au niveau ggml plutôt qu’à seulement répartir des couches ou des lignes.

Ces chiffres sont utiles comme contexte, mais il faut les lire avec prudence. D’abord, ils viennent d’un fork et d’un contexte de test spécifique. Ensuite, l’article mentionne notamment une configuration avec **4 Tesla T4** sur serveur AMD EPYC, ce qui ne reflète pas forcément une machine grand public avec deux RTX sur PCIe. Enfin, la PR upstream llama.cpp ne promet pas un gain universel ; elle insiste au contraire sur le caractère expérimental, les limites backend et la nécessité de NCCL pour de bonnes performances CUDA.

Le bon réflexe, pour un utilisateur local, n’est donc pas “activer `-sm tensor` partout”. C’est plutôt : benchmarker `layer` contre `tensor` sur son propre modèle, son propre contexte, son propre batch, et son propre interconnect.

## Commandes de départ raisonnables

La documentation officielle donne une recette minimale pour tensor parallelism :

```bash
llama-cli -m model.gguf -sm tensor -ctk f16 -ctv f16
```

Dans la pratique, il faudra souvent ajouter ou vérifier :

```bash
llama-cli \
  -m model.gguf \
  -sm tensor \
  -fa on \
  -ctk f16 \
  -ctv f16 \
  --ctx-size 8192
```

Pour comparer, il faut garder une baseline en mode par défaut :

```bash
llama-cli -m model.gguf
```

ou explicitement :

```bash
llama-cli -m model.gguf -sm layer
```

Le paramètre `--tensor-split` reste utile pour distribuer la charge selon les cartes. Par exemple, `-ts 3,1` donne 75 % à la première carte et 25 % à la seconde. En mode `tensor`, si rien n’est précisé, la documentation indique que les segments sont divisés équitablement.

## Pourquoi c’est important pour l’IA locale

L’IA locale progresse souvent par les modèles, mais elle devient vraiment utilisable grâce aux runtimes. Un modèle open-weight de 30B, 70B ou MoE récent n’a pas beaucoup d’intérêt si le runtime local ne sait pas exploiter efficacement le matériel disponible. Le travail dans ggml/llama.cpp est donc stratégique : il transforme un tas de cartes modestes en plateforme d’inférence plus crédible.

Ce n’est pas seulement une affaire de performance brute. Pour les agents locaux, la latence token par token change l’expérience. Un agent qui réfléchit, appelle un outil, lit un résultat, puis reprend la génération doit rester réactif. Si plusieurs GPU peuvent réduire cette latence sans passer par vLLM ou une stack serveur plus lourde, llama.cpp garde son rôle central : petit binaire, gros impact.

## Verdict provisoire

Le mode `--split-mode tensor` de llama.cpp est une avancée réelle, mais pas encore un réglage par défaut à cocher les yeux fermés. Il est surtout pertinent pour les setups multi-GPU CUDA, avec FlashAttention, KV cache non quantifié, et idéalement NCCL. Pour les machines hétérogènes, AMD/Vulkan, ou les déploiements qui exigent de la stabilité absolue, le mode `layer` reste probablement le choix le plus raisonnable.

La bonne nouvelle, c’est que llama.cpp ne se contente plus de “faire rentrer” les modèles localement. Le projet travaille maintenant à mieux exploiter les machines locales complexes. Et ça, pour les homelabs IA, c’est une évolution plus importante qu’un énième graphique de leaderboard.

## Sources

- [PR officielle llama.cpp #19378 — backend-agnostic tensor parallelism](https://github.com/ggml-org/llama.cpp/pull/19378)
- [Documentation officielle llama.cpp — Using Multiple GPUs](https://github.com/ggml-org/llama.cpp/blob/master/docs/multi-gpu.md)
- [Analyse indépendante — llama.cpp performance breakthrough for multi-GPU setups](https://medium.com/@jagusztinl/llama-cpp-performance-breakthrough-for-multi-gpu-setups-04c83a66feb2)
