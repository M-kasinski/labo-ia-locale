---
title: "iLLaDA : ByteDance et Renmin U. poussent le LLM par diffusion à l’échelle 8B"
description: "Soumis le 24 juin 2026 sur arXiv, iLLaDA entraîne un modèle masqué entièrement bidirectionnel sur 12T tokens et rivalise avec Qwen2.5 7B — une piste hors autoregression pour l’open research."
pubDate: 2026-06-27
tags: ["diffusion", "open-weight", "ByteDance", "Qwen", "LLaDA", "recherche"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "arXiv — Improved Large Language Diffusion Models (2606.25331)"
    url: "https://arxiv.org/abs/2606.25331"
  - label: "Hugging Face Papers — 2606.25331"
    url: "https://huggingface.co/papers/2606.25331"
  - label: "THE DECODER — iLLaDA vs Qwen2.5 (27 juin 2026)"
    url: "https://the-decoder.com/bytedances-illada-is-a-diffusion-language-model-that-keeps-up-with-qwen2-5/"
---

## La nouvelle

**iLLaDA** (*improved LLaDA*) est un **modèle de langage par diffusion masquée** de **8 milliards de paramètres**, entraîné **from scratch** avec une attention **entièrement bidirectionnelle** — l’inverse du dogme autoregressif + attention causale qui domine GPT, Llama et Qwen. Le papier **arXiv:2606.25331** est daté du **24 juin 2026** ; la couverture presse (THE DECODER, etc.) le place en **fin juin** comme signal fort côté **ByteDance Seed** et **Université Renmin de Pékin**.

Les auteurs publient **poids et code** via le dépôt [ML-GSAI/LLaDA](https://github.com/ML-GSAI/LLaDA). Ce n’est pas encore le remplaçant de ton stack Ollama du week-end, mais ça élargit le menu open research au moment où **DiffusionGemma** (Google, début juin) et les modèles **dLLM** entrent dans **vLLM**.

## Analyse technique

### Objectif et pipeline

Contrairement aux hybrides qui convertissent un AR en diffusion après coup, iLLaDA garde l’**objectif de diffusion masquée** sur tout le cycle :

| Phase | Échelle annoncée |
|-------|------------------|
| **Pré-entraînement** | **12 billions de tokens** |
| **SFT instruction** | **25B tokens**, **12 epochs** |

Deux variantes sont décrites :

- **iLLaDA-Base** — fondation ;
- **iLLaDA-Instruct** — alignement instruction.

Ajouts pratiques cités dans le papier :

- **génération à longueur variable** (efficacité à l’inférence) ;
- **confidence-based scoring** pour les QCM (évaluation plus stable sur choix multiples).

### Gains vs LLaDA (prédécesseur diffusion)

Les deltas les plus cités :

| Variante | Benchmark | Gain vs LLaDA |
|----------|-----------|---------------|
| Base | **BBH** | **+21,6 points** |
| Base | **ARC-Challenge** | **+14,9 points** |
| Instruct | **MATH** | **+14,5 points** |
| Instruct | **HumanEval** | **+16,5 points** |

L’argument central : la diffusion bidirectionnelle **scale** maintenant comme une voie crédible vers des modèles forts en **général**, **math** et **code**.

### Face à Qwen2.5 7B (autoregressif)

Sur **plusieurs** benchmarks, iLLaDA reste **compétitif** avec **Qwen2.5 7B** malgré un entraînement non autoregressif. THE DECODER insiste sur une nuance honnête : **après fine-tuning poussé**, l’écart peut se creuser en faveur des pipelines AR matures — les écosystèmes LoRA/GGUF/vLLM sont encore calibrés AR.

ByteDance enchaîne dans la même veine que **Seed 2.1 Pro/Turbo** (API, 24 juin) et la ligne **Seed Diffusion** : diversification des architectures plutôt qu’un seul pari transformer causal.

## Impact pour l’écosystème local

### Pour qui c’est pertinent

- **Chercheurs & fine-tuneurs** : dépôt GitHub + 8B = faisable sur **1–2 GPU** ou station de dev pour reproduire les courbes du papier.
- **Ingénieurs inference** : si tu suis **vLLM** (blog **DiffusionGemma**, 10 juin 2026), iLLaDA est un **deuxième datapoint** que les moteurs doivent gérer des **dLLM** natifs — pas seulement du speculative decoding sur AR.
- **Consommateurs GGUF** : **pas de promesse** dans le papier d’un export GGUF day-one ; llama.cpp supporte progressivement certaines archis diffusion — à vérifier commit par commit avant de promettre du local desktop.

### Ce que ça ne change pas (encore)

- **Ollama `ollama run`** reste dominé AR (Llama 4, Qwen3, Gemma 4).
- **Agents CLI** (Codex, Claude Code, harness locaux) supposent des APIs **token-par-token** ; la diffusion change la latence perçue (itérations de débruitage vs streaming AR).
- **Licence & géopolitique** : poids académiques/industriels chinois — même prudence compliance que pour Qwen/DeepSeek selon ton secteur.

## Limites honnêtes

- **Reproduction indépendante** : chiffres du papier ; la communauté doit confirmer sur harness publics (pas encore de vague de replays type « artificial analysis » fin juin).
- **SFT 12 epochs** : coût et risque d’overfitting instruction non détaillé pour tous les domaines.
- **Inférence** : la diffusion peut être rapide en tokens/s sur certains kernels (cf. lignée Seed Diffusion) mais **moins mature** que AR sur Apple Silicon MLX aujourd’hui.
- **Catégorie veille** : tant que le chemin **GGUF + llama.cpp** n’est pas trivial, on classe ce sujet en **recherche / industrie** plutôt qu’en guide install local.

## Sources

- arXiv 2606.25331 — Improved Large Language Diffusion Models (24 juin 2026) : https://arxiv.org/abs/2606.25331
- Hugging Face Papers — 2606.25331 : https://huggingface.co/papers/2606.25331
- THE DECODER — ByteDance iLLaDA (27 juin 2026) : https://the-decoder.com/bytedances-illada-is-a-diffusion-language-model-that-keeps-up-with-qwen2-5/
- Code & weights — https://github.com/ML-GSAI/LLaDA