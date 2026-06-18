---
title: "DeepSeek V3.2 et DSA : l'attention sparse enfin supportée dans llama.cpp"
description: "La PR #23346 fusionne le support complet de DeepSeek V3.2 avec DeepSeek Sparse Attention (DSA) et lightning indexer dans llama.cpp. 685B de paramètres MoE, 128K de contexte — et 700 Go de RAM pour le Q8_0."
pubDate: 2026-05-29
category: "local"
tags: [ia-locale, deepseek, moe, attention-sparse, llama-cpp, quantization, nvfp4]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "llama.cpp PR #23346 — DeepSeek V3.2 DSA support", url: "https://github.com/ggml-org/llama.cpp/pull/23346" }
  - { label: "llama.cpp release b9411 (29 mai 2026)", url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9411" }
  - { label: "arXiv 2512.02556 — DeepSeek-V3.2 paper", url: "https://arxiv.org/abs/2512.02556" }
  - { label: "DeepSeek-V3.2 sur Hugging Face", url: "https://huggingface.co/deepseek-ai/DeepSeek-V3.2" }
  - { label: "DeepSeek-V3.2-Exp sur Hugging Face", url: "https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp" }
  - { label: "GGUF DeepSeek-V3.2-light par sszymczyk", url: "https://huggingface.co/sszymczyk/DeepSeek-V3.2-light-GGUF" }
  - { label: "nvidia/DeepSeek-V3.2-NVFP4 sur Hugging Face", url: "https://huggingface.co/nvidia/DeepSeek-V3.2-NVFP4" }
  - { label: "Tour technique DeepSeek V3 → V3.2 (Sebastian Raschka)", url: "https://magazine.sebastianraschka.com/p/technical-deepseek" }
---

Le 29 mai 2026, la PR [#23346](https://github.com/ggml-org/llama.cpp/pull/23346) a été fusionnée dans `llama.cpp` (build **b9411**), apportant le support complet de **DeepSeek V3.2** avec son mécanisme d'attention sparse **DSA** (DeepSeek Sparse Attention) et son **lightning indexer**.

C'est une première : une architecture MoE de 685 milliards de paramètres avec attention fine-grainée est maintenant inférable localement, sans API.

## Qu'est-ce que DeepSeek V3.2 ?

DeepSeek V3.2 est le successeur de V3, avec la même architecture de base — MoE (Mixture-of-Experts), MLA (Multi-Head Latent Attention) — mais enrichi d'un mécanisme clé : **DSA**, une attention sparse qui réduit la complexité computationnelle sans sacrifier la qualité.

### Les chiffres

- **685B paramètres totaux** (architecture MoE)
- **~37B paramètres actifs** par forward pass
- **128K tokens** de contexte
- MLA + DSA combinés (DSA prend le relais au-delà de 2 048 tokens)
- Disponible en trois variantes : V3.2, V3.2-Exp, V3.2-Speciale

### Le lightning indexer

DSA repose sur un **lightning indexer** : un petit réseau qui calcule un score d'importance entre chaque token de requête et les tokens précédents, déterminant lesquels sont sélectionnés pour l'attention. En dessous de 2 048 tokens, DSA se comporte comme une attention MLA dense. Au-delà, il commence à sélectionner finement les tokens pertinents.

Le papier officiel ([arXiv 2512.02556](https://arxiv.org/abs/2512.02556)) décrit DSA comme un mécanisme qui "réduit substantiellement la complexité computationnelle tout en préservant les performances en contexte long".

## Ce qui a changé dans llama.cpp

La PR implémente DSA **sans ajouter de nouvel opérateur GGML** — l'attention sparse est réalisée en masquant les éléments du KQ mask correspondant aux tokens non sélectionnés par le lightning indexer.

### Composants ajoutés

- **`llama_kv_cache_dsa`** : nouvelle classe mémoire qui agrège deux `llama_kv_cache` — un pour les représentations latentes MLA, un pour les clés du lightning indexer
- **`LLM_ARCH_DEEPSEEK32`** : architecture dédiée dans le moteur d'inférence
- **`llama_model_deepseek32`** : implémentation du modèle
- Conversion GGUF pour `DeepseekV32ForCausalLM`
- Support **NVFP4** (NVIDIA FP4) pour les quantisations compatibles Blackwell
- Support **f16** pour `GGML_OP_FILL`

### PPL mesuré (wiki.test.raw, chunk 4K)

| Quantisation | Attention | PPL |
|---|---|---|
| Q8_0 | Dense (sans indexer) | 2.9115 ± 0.0146 |
| Q8_0 | Sparse (avec indexer) | 2.9126 ± 0.01466 |
| NVFP4 | Sparse (avec indexer) | 3.0727 ± 0.01577 |

La différence de perplexité entre dense et sparse est négligeable — le lightning indexer préserve la qualité tout en réduisant le calcul.

## Benchmarks concrets

Des tests ont été réalisés par [@fairydreaming](https://github.com/fairydreaming) sur une **RTX PRO 6000 Blackwell Max-Q** (96 Go VRAM) avec un EPYC 9374F, experts en RAM :

| Configuration | Prompt (512 tok) | Génér (32 tok) |
|---|---|---|
| Q8_0, pas d'offload | 22.17 t/s | 10.91 t/s |
| Q8_0, offload complet | 42.01 t/s | 10.97 t/s |
| NVFP4, pas d'offload | 41.34 t/s | 1.82 t/s |

**Le NVFP4 est excellent sur GPU** (presque aussi rapide que Q8_0 pour le prompt), mais **horrible sur CPU** — 8× plus lent que Q8_0. Le NVFP4 n'est utile que si tous les tenseurs tiennent sur GPU.

## Contrainte mémoire : 400 à 700 Go

C'est le point qui va filtrer : le modèle pèse **678 Go en Q8_0** et **400 Go en Q4_K_M**. L'implémentation générique du lightning indexer utilise de gros buffers de calcul — si tu rencontres des OOM, réduis le contexte et/ou la taille d'ubatch.

En pratique, il te faut un cluster multi-GPU ou une machine avec 512+ Go de RAM pour faire tourner ça confortablement. Ce n'est pas un modèle pour un MacBook Pro.

### GGUFs disponibles pour tester

- [DeepSeek-V3.2-Exp-light-GGUF](https://huggingface.co/sszymczyk/DeepSeek-V3.2-Exp-light-GGUF)
- [DeepSeek-V3.2-light-GGUF](https://huggingface.co/sszymczyk/DeepSeek-V3.2-light-GGUF)
- [DeepSeek-V3.2-Speciale-light-GGUF](https://huggingface.co/sszymczyk/DeepSeek-V3.2-Speciale-light-GGUF)
- [DeepSeek-V3.2-4Layers-GGUF](https://huggingface.co/sszymczyk/DeepSeek-V3.2-4Layers-GGUF) (16 Go, 4 couches — pour tester l'implémentation)
- [nvidia/DeepSeek-V3.2-NVFP4](https://huggingface.co/nvidia/DeepSeek-V3.2-NVFP4) (NVFP4, nécessite Blackwell)

## Comment l'utiliser

Avec le build b9411 ou supérieur :

```bash
# Conversion (nécessite transformers 4.x, pas 5.x)
pip install transformers==4.57.6
python convert_hf_to_gguf.py /path/to/DeepSeek-V3.2/ --outfile deepseek-v3.2-q8_0.gguf --outtype q8_0

# Inférence
./bin/llama-cli -m deepseek-v3.2-q8_0.gguf \
  -c 4096 -ub 512 -ngl 99 -ncmoe 999 -fa 1 \
  -cnv -p "Explique-moi l'attention sparse"
```

Utilise le chat template `models/templates/deepseek-ai-DeepSeek-V3.2.jinja` inclus dans le dépôt.

## Verdict local

Le support DSA dans llama.cpp est une avancée technique réelle — une architecture d'attention fine-grainée implémentée sans nouvel opérateur GGML, avec une perplexité identique à l'attention dense. C'est du beau travail d'ingénierie.

Mais soyons clairs : **685B de paramètres, c'est un modèle de datacenter**. Même en Q4_K_M (400 Go), ça dépasse largement ce qu'un setup grand public peut absorber. Le NVFP4 promet 386 Go, mais uniquement sur Blackwell.

Pour le moment, cette fonctionnalité est surtout intéressante pour :
- Les équipes avec des clusters multi-GPU qui veulent servir DeepSeek V3.2 localement
- Les contributeurs et testeurs qui veulent valider l'implémentation
- L'écosystème — la preuve qu'even les architectures MoE les plus complexes peuvent être portées en local

Le lightning indexer est un mécanisme prometteur pour l'attention longue. Si on le voit sur des modèles plus petits (10-30B), ça changera la donne. Pour l'instant, c'est un cap technique — impressionnant, mais pas encore accessible.
