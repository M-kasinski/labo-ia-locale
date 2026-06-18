---
title: "gpt-oss-20b d'OpenAI : un modèle de reasoning qui tient dans 16 Go"
description: "OpenAI publie gpt-oss-20b sous licence Apache 2.0 — 21B paramètres, 3,6B actifs en MoE, performance proche d'o3-mini, et GGUF prêt pour le matériel grand public."
pubDate: 2026-06-18
category: "local"
tags: ["OpenAI", "gpt-oss", "MoE", "GGUF", "Unsloth", "quantization"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "OpenAI — Introducing gpt-oss"
    url: "https://openai.com/index/introducing-gpt-oss/"
  - label: "Unsloth — gpt-oss-20b GGUF"
    url: "https://huggingface.co/unsloth/gpt-oss-20b-GGUF"
  - label: "IntuitionLabs — Hardware Requirements"
    url: "https://intuitionlabs.ai/articles/hardware-requirements-gpt-oss-20b"
---

## La nouvelle

OpenAI a publié **gpt-oss**, sa première famille de modèles open-weight, sous licence **Apache 2.0**. Deux tailles : gpt-oss-120b (117B params, 5,1B actifs) pour le datacenter, et **gpt-oss-20b** (21B params, 3,6B actifs) spécifiquement conçu pour le matériel grand public.

Le 20B est celui qui nous intéresse ici : il atteint des performances **proches d'o3-mini** sur les benchmarks de reasoning, et tient dans **16 Go de RAM/VRAM** en quantification 4-bit.

### Architecture MoE — 21B params, 3,6B actifs

gpt-oss-20b est un **Mixture-of-Experts**. Sur les 21 milliards de paramètres, seuls 3,6 milliards sont activés par token. C'est la même stratégie que DeepSeek V3 ou Mixtral, mais poussée plus loin :

- **Attention locale bandée** — alternating dense and locally banded sparse attention patterns
- **Grouped multi-query attention** (group size 8) pour réduire la mémoire KV cache
- **3,6B params actifs** — comparable à un modèle dense de 3-4B en termes de charge d'inférence

En pratique, le modèle se comporte comme un 4B pendant l'inférence, mais avec la capacité de raisonnement d'un modèle beaucoup plus gros.

## Analyse technique

### Quantification GGUF — Unsloth Dynamic 2.0

Unsloth a déjà publié les GGUF sous **Dynamic 2.0**, leur nouvelle génération de quantification dynamique :

- **Meilleure précision** que les Q4_K_M classiques à bit-width équivalente
- **SOTA en quantization performance** — selon les benchmarks d'Unsloth
- Disponible sur Hugging Face, prêt à être chargé dans Ollama, LM Studio ou llama.cpp

La communauté a aussi produit des variantes **derestricted** (uncensored) en Q4_K_M, pour ceux qui veulent un modèle sans garde-fous conversationnels.

### Hardware requirements — ce qui tourne, ce qui ne tourne pas

| Matériel | Faisable ? | Notes |
|---|---|---|
| **RTX 4080 (16 Go)** | ✅ Oui | Q4_K_M, tout sur GPU |
| **RTX 4090 (24 Go)** | ✅ Oui | Q5_K_M ou Q6_K pour plus de qualité |
| **M2/M3 Pro 16 Go** | ✅ Oui | MLX ou llama.cpp Metal |
| **M4 Max 36 Go** | ✅ Excellent | Q6_K+ sans problème |
| **RTX 4060 (8 Go)** | ⚠️ Partiel | GPU offload partiel, reste sur CPU — lent mais faisable |
| **Mac M1 8 Go** | ⚠️ Difficile | Swap intensif, pas recommandé |

### Performance vs o3-mini

Selon OpenAI, gpt-oss-20b "delivers similar results to OpenAI o3-mini on common benchmarks". C'est une affirmation forte — o3-mini est l'un des modèles reasoning les plus efficaces d'OpenAI. En pratique, les tests communautaires confirment un niveau de raisonnement solide, surtout sur les tâches de code et de logique mathématique.

Le modèle supporte aussi l'**adjustable reasoning** : on peut contrôler le niveau d'effort de raisonnement, comme sur les modèles o1/o3 d'OpenAI. Plus d'effort = meilleures réponses sur les problèmes complexes, mais plus lent.

## Impact pour l'usage local

**Pourquoi ça compte :** Un modèle d'OpenAI, open-weight, Apache 2.0, qui tient sur du matériel grand public et qui rivalise avec leur propre API ? C'est un changement de paradigme.

**Pour les développeurs locaux :** gpt-oss-20b offre une alternative crédible aux modèles open-source existants (Qwen 3.6 27B, Llama 4 Scout) avec un profil d'efficacité MoE qui le rend particulièrement adapté aux setups 16-24 Go.

**Le bémol :** 16 Go, c'est le minimum. Sur une RTX 4060 8 Go ou un Mac 16 Go, le modèle fonctionne mais le offload partiel CPU/GPU réduit significativement la vitesse. Pour une expérience fluide, visez 24 Go (RTX 4090) ou un M4 Pro/Max.

**Commande rapide pour tester :**
```bash
ollama pull gpt-oss:20b
```
Ou télécharger le GGUF Unsloth Dynamic 2.0 depuis Hugging Face et le charger dans LM Studio.
