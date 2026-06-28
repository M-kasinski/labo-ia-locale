---
title: "llama.cpp b9828 : Flash Attention OpenCL pour f16, f32 et quants q4_0/q8_0"
description: "Build du 27 juin 2026 : llama.cpp améliore la Flash Attention côté OpenCL (prépass masques, tuiles q4/q8, MoE SOA) — utile pour GPU Qualcomm/Adreno et autres backends OpenCL en inférence locale."
pubDate: 2026-06-28
tags: ["llama.cpp", "OpenCL", "Flash Attention", "GGUF", "quantization", "inférence locale"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "GitHub Releases — llama.cpp b9828"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9828"
  - label: "PR #25069 — opencl: flash attention improvement"
    url: "https://github.com/ggml-org/llama.cpp/pull/25069"
  - label: "Article de référence Labo — llama.cpp b9726 et --agent"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9726"
---

## La nouvelle

**llama.cpp b9828** est publié le **27 juin 2026** (tag `b9828`, commit `ebd048f`, build automatisé vers 23:15 UTC). La release est entièrement centrée sur **OpenCL** et la **Flash Attention** : refonte des kernels FA pour **f16** et **f32**, ajout de chemins **q4_0** et **q8_0**, prépass de masquage, table de tuning des tuiles, et correction d’un bug d’**infini** avec l’option compilateur `-cl-finite-math-only`.

Ce n’est pas le patch CUDA du **27 juin** (b9827, `cudaMemcpy2DAsync` pour snapshots GDN) — c’est la contrepartie pour les machines qui infèrent via **OpenCL** plutôt que CUDA/Metal/Vulkan.

## Analyse technique

### Pourquoi OpenCL compte encore en local

La plupart des benchmarks « IA locale » parlent NVIDIA ou Apple Silicon. Pourtant une partie non négligeable du parc — **Qualcomm Adreno**, certains iGPU, environnements embarqués, builds ROCm/OpenCL hybrides — passe par **OpenCL**. Sans FA optimisée, ces chemins restent des fallbacks lents : acceptable pour un test, pénible pour un serveur `llama-server` qui tourne la journée.

Le message de **PR #25069** est explicite : améliorer la FA OpenCL pour rapprocher le débit des backends « premium » sur les formats les plus utilisés en GGUF.

### Changements listés dans b9828

| Zone | Détail |
|------|--------|
| Kernels FA | Rework FA **f16** / **f32** |
| Prépass | `flash_attn_kv_pad_f16`, `flash_attn_mask_pad_f16` — padding des tuiles KV/mask au multiple **BLOCK_N** |
| Classification masques | `flash_attn_blk_f16` classe chaque tuile KV par bloc de requête : fully masked / mixed / fully unmasked → le kernel principal peut **sauter** les tuiles 100 % masquées |
| Quants | FA pour **q4_0** et **q8_0** ; `set_rows` f32 → q8_0/q4_0 ; kernels de **dequant** dédiés |
| MoE | Tenseurs **q4_0 MoE** aussi en disposition **SOA** (Structure of Arrays) |
| Host | Câblage côté hôte pour FA + **table de tuning** des tuiles avec override |
| Correctifs | Fix **infini** sous `-cl-finite-math-only` ; cosmétique |

Le co-auteur listé sur la release est **Li He (Qualcomm)** — signal fort que le travail cible du matériel **mobile/edge** avec stack OpenCL mature, pas seulement un hobby kernel.

### Lien avec la stratégie llama.cpp juin 2026

En deux semaines, le projet enchaîne :

1. **b9726** — `--agent` unifie MCP + outils intégrés sur `llama-server`.
2. **b9827** — fast path CUDA pour rollbacks **GDN** multi-slot.
3. **b9828** — FA OpenCL pour quants et MoE.

Lecture d’ensemble : llama.cpp **élargit les backends** et **durcit les chemins stateful/agent**, au lieu de n’optimiser qu’un seul GPU NVIDIA. Pour un labo qui teste « le même GGUF » sur Mac, Linux NVIDIA, AMD ROCm et un laptop Qualcomm, c’est exactement le genre de release qui évite de changer de runtime par machine.

## Benchmarks et résultats

OpenAI n’a pas publié de tableau tokens/s pour b9828. Les releases llama.cpp de ce type sont des **correctifs de kernel** : le gain se mesure sur **ton** modèle, **ta** quant (souvent Q4_K_M ou Q8_0), **ta** longueur de contexte et **ton** backend OpenCL.

Méthode honnête :

```bash
# Avant/après sur la même machine, même modèle, même -ngl
./llama-bench -m model.gguf -p 512 -n 128
```

Si tu sers en multi-utilisateur, ajoute une passe avec **prefill long** et masque causal (chat + RAG) — c’est là que la FA et le prépass de masques devraient se voir.

## Impact pour l’écosystème local

### Qui en profite

- **Self-hosters** avec GPU OpenCL seulement (ou driver CUDA/ROCm instable).
- **Quantizers GGUF** q4_0/q8_0 : moins de raison de rester bloqué en f16 « parce que OpenCL ne suit pas ».
- **MoE quantifiés** : la mention SOA sur q4_0 MoE anticipe des modèles type **Qwen3.5-A3B**, **Ministral**, etc., sans repasser par un serveur vLLM pour un premier test.

### Limites

- OpenCL reste **secondaire** en documentation et en communauté : moins de retours terrain que CUDA.
- Pas de garantie que **tous** les modèles récents (DSA, récurrents GDN, MTP) exposent déjà le chemin FA OpenCL optimal — vérifier le log au chargement.
- Les builds **bNNNN** se succèdent plusieurs fois par jour : épingle un tag (ex. `b9828`) dans tes scripts de prod, pas « latest » aveugle.

### Par rapport à Ollama / vLLM

- **Ollama** embarque llama.cpp mais avec son propre cycle de merge — b9828 peut arriver avec décalage.
- **vLLM** reste le roi du serving multi-GPU NVIDIA ; cette release ne le concurrence pas, elle **complète** le spectre hardware du même écosystème GGUF.

## Mise à jour recommandée

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm use 25.9.0

# Binaire précompilé ou rebuild
# Télécharger b9828 depuis GitHub Releases, ou :
git -C llama.cpp fetch && git -C llama.cpp checkout b9828
cmake -B build -DGGML_OPENCL=ON
cmake --build build -j
```

Si tu compiles pour Qualcomm/Adreno, garde les flags documentés par ton vendeur ; le fix `-cl-finite-math-only` évite des NaN silencieux qui cassent la génération sur certains drivers.

## Sources vérifiées

- [GitHub Releases — llama.cpp b9828](https://github.com/ggml-org/llama.cpp/releases/tag/b9828)
- [PR #25069 — opencl: flash attention improvement](https://github.com/ggml-org/llama.cpp/pull/25069)