---
title: "vLLM 0.24.0 : MiniMax-M3, DeepSeek-V4 et la fin de CUDA_VISIBLE_DEVICES par défaut"
description: "La version 0.24.0 de vLLM élargit nettement le support des modèles et change la façon de sélectionner les GPU. Une release d’infrastructure avec un vrai poids pour les serveurs locaux musclés."
pubDate: 2026-06-30
tags: ["vllm", "minimax-m3", "deepseek-v4", "gpu", "inference locale"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "GitHub Releases — vLLM v0.24.0"
    url: "https://github.com/vllm-project/vllm/releases/tag/v0.24.0"
---

## La nouvelle

**vLLM 0.24.0** est sorti le **29 juin 2026 à 19:41 UTC**. La release est volumineuse : **571 commits**, **256 contributeurs** dont **77 nouveaux**. On n’est plus dans le patch cosmétique ; on est dans la release qui fait bouger le socle.

Le message clé est simple : vLLM renforce son support des modèles récents, améliore plusieurs chemins d’exécution et change une hypothèse historique sur la sélection des GPU.

## Analyse technique

### MiniMax-M3 entre dans la danse

Le point le plus visible est le support de **MiniMax-M3**. Ce n’est pas juste “un modèle de plus” : la release associe ce support à plusieurs optimisations matérielles et quantifiées :

- **BF16/FP8 indexer via MSA**
- **MXFP4 support**
- **FP8 sparse GQA**
- tuning AMD/ROCm poussé
- correction d’une régression de performance sur **MiniMax-M2**

Pour les équipes qui servent du code, des agents ou du raisonnement, MiniMax-M3 devient un candidat sérieux dans la pile vLLM. Le message implicite est clair : le projet traite ce modèle comme une cible de premier plan, pas comme une curiosité de laboratoire.

### DeepSeek-V4 gagne en maturité

L’autre gros bloc concerne **DeepSeek-V4**. Les optimisations décrites ne sont pas décoratives :

- **FlashInfer sparse index cache** : **2–4 %** de gain sur le **TTFT**
- **prefill chunk-planning** : environ **4 %** de gain de throughput end-to-end
- **cluster-cooperative topK kernel** : meilleure latence
- **allocations KV contiguës** par bloc
- **TEP=16** pour l’expert partagé block-FP8
- décodage DSA natif pour `next_n > 2` sur **SM100**

Autrement dit, vLLM ne se contente plus de “supporter” DeepSeek-V4. Il l’optimise vraiment pour les configurations de prod sérieuses.

### Model Runner V2 continue de grignoter le centre du moteur

La release fait aussi monter **Model Runner V2** d’un cran :

- les **modèles quantifiés** sont supportés par défaut,
- **GraniteMoE** devient le chemin par défaut,
- les modèles **Qwen** et **DeepSeek-V2 MoE** migrent,
- **DFlash speculative decoding** arrive,
- et l’échantillonnage **FP32 Gumbel** est corrigé.

Ça a une conséquence pratique : vLLM se rapproche de plus en plus d’un runtime qui absorbe les familles de modèles sans exiger un bricolage par modèle. C’est exactement ce qu’on attend d’un serveur d’inférence quand les labs changent de format tous les quinze jours.

### Le changement qui casse les habitudes : `device_ids`

Le point à surveiller, c’est la gestion des GPU.

vLLM **ne définit plus `CUDA_VISIBLE_DEVICES` en interne**. À la place, la release introduit un argument **`device_ids`**.

Pourquoi c’est important ? Parce que beaucoup de scripts et de déploiements présumaient que vLLM allait gérer cette couche à leur place. Ce n’est plus le cas.

Impact concret :

- plus de contrôle explicite côté orchestration,
- moins d’effets de bord invisibles,
- mais aussi une migration à faire dans les scripts qui reposaient sur l’ancien comportement.

Sur **ROCm**, la release ouvre aussi une fenêtre de dépréciation pour `CUDA_VISIBLE_DEVICES`. C’est le genre de détail qui n’a l’air de rien, puis qui te casse un cluster au mauvais moment. Le classique du lundi matin.

## Ce que ça change pour l’écosystème local

### Pour les stations GPU locales

Si tu fais tourner vLLM sur :

- une machine RTX 4090 / 5090,
- un nœud ROCm,
- ou une station multi-GPU pour du serving d’équipe,

0.24.0 vaut surtout pour deux choses :

1. la meilleure prise en charge des modèles récents,
2. la clarification de la sélection de device.

La release ne cherche pas à simplifier la vie de l’utilisateur débutant. Elle cherche à rendre la couche serveur plus robuste quand le hardware, les modèles et les kernels se multiplient.

### Pour les équipes qui servent des agents

Les gains TTFT et throughput sur DeepSeek-V4 ne sont pas anecdotiques pour des workloads agentiques :

- moins de temps avant la première réponse,
- moins de latence perçue,
- plus de débit sur des séquences longues,
- et des comportements plus stables sous charge.

Dans un système d’agents, les quelques pourcents gagnés sur le moteur se ressentent vite dans le produit final.

## Limites honnêtes

Cette release n’est pas une révolution frontale.

Elle n’ajoute pas un nouveau paradigme d’usage.

Elle ne transforme pas vLLM en runtime desktop “plug and play”.

Elle fait quelque chose de plus utile à long terme : elle **durcit** la pile. Et pour un serveur d’inférence, c’est souvent ça la vraie nouvelle.

## En bref

- **Version :** vLLM 0.24.0
- **Date de release :** 29 juin 2026
- **Scale :** 571 commits, 256 contributeurs
- **Faits marquants :** MiniMax-M3, DeepSeek-V4, MRv2, `device_ids`
- **Lecture produit :** une release de maturité, pas un simple patch

## Sources vérifiées

- [GitHub Releases — vLLM v0.24.0](https://github.com/vllm-project/vllm/releases/tag/v0.24.0)
