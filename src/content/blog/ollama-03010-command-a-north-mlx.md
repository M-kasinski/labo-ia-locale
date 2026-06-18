---
title: "Ollama 0.30.10 : Command A et North family sur Apple Silicon via MLX"
description: "La dernière version d'Ollama apporte le support des modèles Command A et North family sur puce Apple grâce au moteur MLX, avec une mise à jour majeure de llama.cpp."
pubDate: 2026-06-18
tags: ["ollama", "apple-silicon", "mlx", "command-a", "local-inference"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "Ollama GitHub Releases v0.30.10"
    url: "https://github.com/ollama/ollama/releases/tag/v0.30.10"
  - label: "Releasebot — Ollama June 2026 Updates"
    url: "https://releasebot.io/updates/ollama"
---

## La nouvelle

Ollama **v0.30.10**, publiée le 17 juin 2026, apporte un changement significatif pour les utilisateurs Apple Silicon : les modèles de la famille **Command A** (IBM) et **North** sont désormais supportés via le moteur MLX d'Apple. Le backend llama.cpp a été mis à jour au build **b9672**.

## Analyse technique

### Command A sur MLX
Les modèles Command A d'IBM — conçus pour l'inférence de haute performance avec une architecture optimisée — peuvent maintenant tourner nativement sur les puces M-series (M1 à M4) via le framework MLX. Cela signifie :

- **Décodeur et préfill accélérés par GPU** Metal, pas seulement CPU
- Quantisation native NVFP4 pour réduire l'empreinte mémoire tout en conservant la précision
- Pas de dépendance CUDA — tout passe par les pipelines Apple Silicon

### North family
La famille North (détails techniques encore limités publiquement) est également intégrée. Ollama gère automatiquement le routage vers MLX quand le modèle est compatible, sans configuration manuelle.

### Moteur llama.cpp b9672
En parallèle, le backend llama.cpp a été mis à jour au build 9672, apportant les corrections et optimisations de ces dernières semaines (voir article dédié sur llama.cpp b9704).

## Impact pour l'écosystème local

C'est un signal clair : **Apple Silicon n'est plus une plateforme de compromis**. Avec MLX mature dans Ollama, les modèles qui étaient réservés aux GPU NVIDIA deviennent accessibles sur Mac Studio/MacBook Pro. Pour quiconque travaille avec des assistants locaux ou des agents de code, ça change la donne en termes de portabilité et de coût.

Les performances réelles dépendront bien sûr du modèle exact et de la taille — un M4 Max 128 Go ne vaut pas un H100 pour l'entraînement — mais pour l'inférence locale, le fossé se réduit sérieusement.

## Sources vérifiées

- [Ollama v0.30.10 sur GitHub](https://github.com/ollama/ollama/releases/tag/v0.30.10)
- [Releasebot — Ollama June 2026](https://releasebot.io/updates/ollama)
