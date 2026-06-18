---
title: "Ollama v0.30 : MLX mûrit, llama.cpp s'intègre, Gemma 4 QAT arrive"
description: "La série v0.30 d'Ollama consolide le moteur MLX sur Apple Silicon et élargit le support matériel via llama.cpp — avec Gemma 4 QAT, Cohere2Moe et des gains de stabilité concrets."
pubDate: 2026-06-18
category: "local"
tags: ["Ollama", "MLX", "llama.cpp", "Apple Silicon", "Gemma", "GGUF"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Ollama GitHub Releases"
    url: "https://github.com/ollama/ollama/releases"
  - label: "Ollama Blog — MLX on Apple Silicon"
    url: "https://ollama.com/blog/mlx"
  - label: "Ollama Blog — v0.30 announcement"
    url: "https://ollama.com/blog"
  - label: "Releasebot — Ollama June 2026"
    url: "https://releasebot.io/updates/ollama"
---

## La nouvelle

En juin 2026, Ollama a enchaîné cinq releases (v0.30.0 à v0.30.10) qui marquent un tournant dans la maturation de son architecture. Le moteur **MLX d'Apple** n'est plus un simple preview — il est désormais stabilisé, avec des couches linéaires et d'embedding renforcées, des snapshots pendant le traitement de prompt et le speculative decoding. En parallèle, **llama.cpp** est intégré comme moteur complémentaire, élargissant le support matériel bien au-delà d'Apple Silicon.

### Ce qui a changé — v0.30.0 à v0.30.10

**v0.30.0 (13 mai)** — Le gros morceau : intégration de llama.cpp comme moteur à côté de MLX. Cela signifie que les modèles GGUF de Hugging Face, y compris les fine-tunes communautaires, sont directement supportés. Support étendu aux GPU NVIDIA avec des gains de performance mesurés.

**v0.30.6 (5 juin)** — Gemma 4 QAT (Quantization-Aware Training) arrive avec 5 tags :
- `gemma4:e2b-it-qat` (~2B)
- `gemma4:e4b-it-qat` (~4B)
- `gemma4:12b-it-qat` (12B)
- `gemma4:26b-a4b-it-qat` (26B MoE)
- `gemma4:31b-it-qat` (31B)

Les couches d'embedding passent au **NVFP4 global scale** pour une quantification plus précise sur Apple Silicon.

**v0.30.8 (12 juin)** — Le caching de prompt est découplé du contexte pour un meilleur recyclage du KV cache. Le runner MLX crée désormais des snapshots pendant le prompt processing et le speculative decoding. Support amélioré des modèles récurrents via les gated-delta kernels.

**v0.30.9 (15 juin)** — Architecture **Cohere2Moe** supportée. Correction du parser LFM2 pour les thinking tokens. Fix critique sur `ollama launch claude` qui tronquait la sortie à un seul token.

**v0.30.10 (17 juin)** — Les familles Command A et North fonctionnent désormais sur Apple Silicon via MLX. llama.cpp mis à jour au build **9672**.

## Analyse technique

### L'architecture hybride MLX + llama.cpp

Le choix d'Ollama est stratégique : MLX reste le moteur par défaut sur Apple Silicon (où il est nettement plus performant grâce aux Neural Accelerateurs du M5 et à l'unified memory), tandis que llama.cpp couvre le reste — NVIDIA CUDA, AMD ROCm, x86, et les cas où MLX ne supporte pas l'architecture du modèle.

Concrètement, cela signifie que **tout modèle GGUF** est désormais utilisable via Ollama, pas seulement ceux de la bibliothèque officielle. Un fine-tune de Qwen 3.6 publié sur Hugging Face ? `ollama pull` direct.

### Gemma 4 QAT — quantification qui se prend au sérieux

Le QAT (Quantization-Aware Training) n'est pas une simple post-quantification. Le modèle est entraîné en simulant les erreurs de quantification, ce qui produit des poids qui résistent mieux à la réduction de précision. En pratique :

- Moins de dégradation sur les tâches de raisonnement
- Meilleur rapport qualité/mémoire que le Q4_K_M classique
- Disponible directement dans Ollama — pas besoin de convertir soi-même

Sur un M2/M3/M4, les variantes e2b et e4b tournent en vitesse interactive sans effort. Le 12B reste fluide sur un M2 Pro 16 Go et devient intéressant sur M4 Max 36 Go+.

### Cohere2Moe — un MoE de plus dans le ring local

Le support de l'architecture Cohere2Moe ouvre la porte aux modèles MoE de Cohere dans Ollama. Les MoE activent seulement une fraction des paramètres par token — souvent 3 à 5 Go effectifs — ce qui les rend particulièrement adaptés au matériel grand public.

## Impact pour l'usage local

**Pour les Mac Apple Silicon :** La stabilisation de MLX avec snapshots et couches renforcées se traduit par moins de crashes en charge prolongée, un speculative decoding plus fiable, et des modèles QAT qui sortent mieux de la quantification. Si tu as un M2 Pro ou supérieur, mets à jour.

**Pour les setups NVIDIA/AMD :** L'intégration de llama.cpp au build 9672 apporte les dernières optimisations du projet — flash attention, meilleure gestion du GPU offload, support des architectures récentes. Le support des GPU Radeon 8060S iGPU est maintenant activé par défaut depuis v0.30.2.

**Pour les workflow agencés :** Le découplage du prompt caching et du contexte (v0.30.8) améliore le recyclage du KV cache — crucial quand tes agents relancent des conversations avec des variations mineures. Moins de rechargements inutiles, plus de vitesse.
