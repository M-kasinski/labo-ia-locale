---
title: "llama.cpp b9840 : DeepSeek V4 entre enfin dans le moteur GGUF"
description: "Release du 29 juin 2026 : support inference et conversion deepseek4, flash attention, graph reuse et templates Jinja — le plus gros MoE open-weight devient jouable en local sur llama-server."
pubDate: 2026-06-29
tags: ["llama-cpp", "DeepSeek V4", "GGUF", "MoE", "inférence locale", "flash attention"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "llama.cpp GitHub Releases — b9840"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9840"
  - label: "PR #24162 — model : add DeepSeek V4"
    url: "https://github.com/ggml-org/llama.cpp/pull/24162"
  - label: "vLLM Blog — DeepSeek V4 in vLLM"
    url: "https://vllm.ai/blog/2026-04-24-deepseek-v4"
---

## La nouvelle

**llama.cpp b9840**, publié ce **29 juin 2026** sur GitHub, n’est pas une release cosmétique : le changelog tient sur un gros morceau — **ajout complet de DeepSeek V4** (`deepseek4`) pour l’inférence et la conversion GGUF ([PR #24162](https://github.com/ggml-org/llama.cpp/pull/24162)). Après des semaines où vLLM et les APIs hébergées absorbaient l’architecture, le runtime le plus répandu pour **GGUF sur CPU/GPU grand public** rattrape enfin le modèle open-weight le plus surveillé du printemps 2026.

Pour les équipes qui self-hostent sans cluster NVIDIA dédié, c’est le signal que **DeepSeek V4-Flash** (et les variantes Pro une fois quantifiées) ne sont plus réservés à un seul stack serveur.

## Analyse technique

### Ce que la PR apporte concrètement

Le merge documenté dans **b9840** couvre toute la chaîne, pas seulement un stub d’architecture :

| Zone | Changement |
|------|------------|
| **Conversion** | Chemin GGUF dédié DSV4, compatibilité avec les GGUF **antirez/ds4**, support du **modèle Pro** |
| **Graphe** | `llm_graph_input_dsv4`, save/load state, **graph reuse** activé |
| **Performance** | **Flash Attention** activée ; padding `n_kv` à **256** pour FA ; checkpointing partiel ; réservation **worst-case KV-cache** |
| **Cache** | Suppression du **V cache** redondant ; `llama_model_n_swa` fixé à **0** pour dsv4 |
| **Chat** | Templates Jinja **inlinés par architecture** ; retrait des templates C++ embarqués obsolètes |
| **Séquences** | Passage de **n_seq=1** à **multi-seq** au fil des commits de la PR |

Les co-auteurs listés (Georgi Gerganov, Piotr Wilkin, fairydreaming, etc.) indiquent un travail de fond comparable à d’autres intégrations MoE récentes (GLM, Qwen3) — avec les subtilités propres à DeepSeek : **Sinkhorn** sur le routing experts, corrections RoPE, et renommage unifié `deepseek-v4-flash` → **`deepseek4`** dans le code.

### Où ça se situe par rapport à vLLM

**vLLM 0.22+** reste la référence pour **débit multi-utilisateurs** sur **8× B200** avec NVFP4, MTP speculative decoding et sparse MLA — le blog vLLM cite encore **DeepSeek-V4-Pro** sur du matériel datacenter et **V4-Flash** sur **4× B200** minimum pour un serving « confortable ».

**llama.cpp** vise un autre compromis :

- **Un binaire** (ou une release précompilée macOS arm64 / CUDA 12–13 / ROCm 7.2 / Vulkan) ;
- **Quantisation GGUF** (Q4_K_M, IQ quants, etc.) pour réduire la VRAM ;
- **llama-server** + flag **`--agent`** (depuis b9726) pour des agents locaux sans cloud.

b9840 ne rend pas **1,6T paramètres** « laptop-friendly ». En revanche, il **ferme l’écart de compatibilité** : tu peux enfin tester les GGUF communautaires (y compris ceux alignés sur les formats **ds4**) dans le même outil que Qwen3 ou GLM-5.2 quantifiés.

### Binaries du jour

La release **b9840** publie la matrice habituelle : **macOS arm64/x64**, **Ubuntu** CPU/Vulkan/ROCm/OpenVINO/SYCL, **Windows** CUDA 12.4 et **13.3**, **Android arm64**, bundle **UI**. Note maintenance : builds **KleidiAI** macOS et toute la ligne **openEuler** restent **DISABLED** (issues #23780 / #23705) — à vérifier si tu comptais sur ces cibles.

Les releases **b9838** et **b9839** du même 29 juin (nettoyage regex UI Tailwind) sont des micro-patches ; **b9840** est celle à installer pour DeepSeek V4.

## Impact pour l’écosystème local

### Pourquoi ça compte maintenant

1. **Parité runtime** — Les benchmarks « open-weight » de juin (GLM-5.2, Kimi K2.7 Code, Nemotron 3 Ultra) tournent déjà sur plusieurs backends ; sans **deepseek4** dans llama.cpp, une partie du marché GGUF restait en **second ordre** (conversion manuelle, forks privés).

2. **Ollama / LM Studio** — Les distributions grand public **embarquent llama.cpp** en submodule ; l’intégration upstream accélère en général leur support modèle sous **quelques jours à quelques semaines** (comme pour Qwen3.5 ou les fixes MoE+MTP en **b9789**).

3. **Agents locaux** — DeepSeek V4 est positionné **coding + long contexte** (jusqu’à **1M tokens** annoncés côté famille V4). Coupler **b9840** avec **`--reasoning-preserve`** (**b9837**, même journée) et un modèle reasoning-compatible en GGUF devient un scénario testable sur **Mac Studio / RTX 4090** avec quants agressifs — pas sur la config Pro full precision.

4. **Économie self-host** — Quand les APIs frontier passent par des **preview gouvernementales** (GPT-5.6 Sol, Mythos 5), disposer d’un **MoE MIT** jouable en local redevient un **plan B opérationnel**, pas un hobby.

### Limites honnêtes

- **VRAM / RAM** : même quantifié, V4-Flash reste un **gros MoE** ; prévois **plusieurs dizaines de Go** selon le quant et le parallélisme GPU (`-ngl`).
- **MTP** : la correction quant MoE+MTP (**b9789**) est prérequis pour des GGUF sains ; l’inférence MTP spéculative n’est pas automatiquement au niveau vLLM.
- **Benchmarks** : les chiffres **LiveCodeBench / SWE** publiés par DeepSeek ou des hébergeurs sont **auto-reportés** — à re-valider sur **ton** harness.
- **Compliance** : poids chinois open-weight — même prudence export / secteur régulé que pour Qwen ou GLM selon ton contexte.

## Pistes pratiques

```bash
# Exemple typique après téléchargement d'un GGUF deepseek4 compatible
llama-server -m /chemin/deepseek4-*.gguf -ngl 99 --flash-attn -c 131072
# Agent local (expérimental) :
llama-server -m ... --agent --reasoning-preserve
```

Commence par un **petit contexte** et un **quant Q4** pour valider le chargement avant de viser le million de tokens annoncé par la famille V4.

## Sources

- [Release b9840 — ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp/releases/tag/b9840)
- [PR #24162 — DeepSeek V4](https://github.com/ggml-org/llama.cpp/pull/24162)
- [DeepSeek V4 in vLLM (contexte architecture)](https://vllm.ai/blog/2026-04-24-deepseek-v4)