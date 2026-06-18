---
title: "vLLM 0.23.0 : Model Runner V2 par défaut, GLM-5.2 et 408 commits en une release"
description: "La v0.23.0 de vLLM passe Model Runner V2 en défaut pour Llama et Mistral, ajoute le support GLM-5.2, et muscle les kernels NVIDIA et AMD. Décryptage technique."
pubDate: 2026-06-18
category: "veille"
tags: ["vLLM", "Model Runner V2", "GLM-5.2", "DeepSeek-V4", "inference", "serving"]
author: "Veille IA"
draft: false
sources:
  - label: "Release v0.23.0 — GitHub vllm-project/vllm"
    url: "https://github.com/vllm-project/vllm/releases/tag/v0.23.0"
  - label: "Releases vllm-project/vllm — GitHub"
    url: "https://github.com/vllm-project/vllm/releases"
  - label: "vLLM-Omni v0.23 integration — GitHub"
    url: "https://github.com/vllm-project/vllm-omni/releases"
  - label: "NewReleases — vLLM v0.23.0"
    url: "https://newreleases.io/project/github/vllm-project/vllm/release/v0.23.0"
---

## Le signal

Sortie le 15 juin 2026, **vLLM v0.23.0** est une release massive : **408 commits** de **200 contributeurs** (dont 63 nouveaux). C'est la release qui fait passer le Model Runner V2 en mode « par défaut » pour les modèles Llama et Mistral, et qui apporte le support de GLM-5.2 dès le jour zéro.

Si vous servez des LLM en production — ou même en local sur un serveur musclé — cette version mérite une attention particulière.

## Model Runner V2 : le nouveau défaut

Le Model Runner V2 est l'architecture de serving de nouvelle génération de vLLM. Introduit progressivement dans les versions précédentes (défaut pour Qwen3 en v0.22.0), il passe désormais en **défaut pour Llama et Mistral dense**.

### Ce qui change concrètement

- **FlashInfer sampler** : le sampler passe par FlashInfer, réduisant le goulot d'étranglement dans la génération probabiliste.
- **Breakable CUDA graphs** : les graphes CUDA peuvent être interrompus proprement, ce qui améliore la gestion des requêtes longues et les interruptions.
- **Pipeline-parallel bubble elimination** : suppression des bulles d'attente dans le pipeline parallel, réduisant la latence sur les déploiements multi-GPU.
- **Gemma 4 MTP** : support du Multi-Token Prediction pour Gemma 4, permettant le décodage spéculatif natif.
- **Speculator-prefill warmup/capture** : meilleur warmup pour les modèles spéculatifs (EAGLE, MTP).

### Performance

Sur les modèles Llama et Mistral, le Model Runner V2 est sélectionné automatiquement. Si vous avez déjà vLLM en production, la mise à jour devrait activer MRv2 sans changement de configuration. Les gains varient selon la charge, mais les tests communautaires montrent **+10-25% de throughput** en décodage pour les modèles denses.

## DeepSeek-V4 : maturation continue

DeepSeek-V4 a fait son entrée en v0.22.0 et reçoit un **hardening majeur** en 0.23.0 :

- **Sparse MLA metadata découplée** de V3.2, permettant un traitement indépendant des modèles V4.
- **TRTLLM-gen attention kernel** : un kernel d'attention généré par TensorRT-LLM pour une meilleure optimisation matérielle.
- **EPLB support pour Mega-MoE** : meilleur routage des experts.
- **Selective prefix-cache retention** pour le KV cache sliding-window.
- **IndexShare pour DSA MTP** : l'optimisation d'IndexShare (réutilisation d'indexer) est maintenant supportée pour le décodage spéculatif DSA.
- **XPU attention decode path** : support des GPU Intel (XPU) pour le décodage.

Le modèle a été **décorré de `torch.compile`** et les chemins attention/RoPE ont été refactorisés. En pratique, cela signifie moins de surprises et des performances plus stables.

## GLM-5.2 : support day-0

GLM-5.2 est supporté dès cette release. Le modèle MoE de 744B de Z.ai est directement compatible avec le pipeline de serving de vLLM, y compris le contexte 1M.

> Note : le support complet de l'architecture IndexShare de GLM-5.2 est en cours d'intégration. La version 0.23.0 gère le modèle mais certaines optimisations spécifiques à l'attention sparse DSA peuvent nécessiter la prochaine release.

## Frontend Rust : l'API se muscle

Le frontend Rust de vLLM continue de grandir :

- **Streaming `generate` endpoint** : réponse en streaming pour les requêtes de génération.
- **Dynamic LoRA endpoints** : chargement à chaud des adapters LoRA sans redémarrage.
- **`/version` et `/server_info`** : endpoints de diagnostic.
- **Request-ID headers** : traçabilité des requêtes.
- **Nouveaux tool parsers** : InternLM2, hy_v3, Phi-4-mini, Gemma4.

Le frontend Rust n'est plus un prototype. Il devient une alternative sérieuse au serveur Python pour les déploiements où la latence et la stabilité comptent.

## KV Cache multi-tier : object store en second tier

Une amélioration notable pour les déploiements à haute densité : le **KV cache peut maintenant offloader vers un object store** (S3, MinIO, etc.) en second tier.

- **HMA (Hybrid Memory Architecture) activé par défaut** pour les connectors capables.
- **Tiering support pour les modèles HMA**.
- **Politique d'offloading par requête** via le hook `on_new_request`.
- **Token-offset selective offload** : offload ciblé par offset de token.

Pour un serveur local avec des contraintes mémoire, cela signifie qu'on peut garder plus de requêtes concurrentes en offloadant le KV cache des requêtes inactives vers le disque réseau.

## Kernels NVIDIA et AMD

### NVIDIA
- **FP8 FlashInfer attention pour ViT** (modèles vision)
- **Triton MoE backend par défaut sur Hopper**
- **CUTLASS FP8 scaled-mm padding bypass (+20%)**
- **MoE-permute buffer pre-allocation (+9-14%)**
- **Tuned selective_state_update pour H200/RTX PRO**
- **NUMA auto-binding sur DGX B300**

### AMD ROCm
- **ROCm 7.2.3** intégré
- **AITER v0.1.13.post1**
- **W4A16 natif** (quantization 4-bit poids, 16-bit activation)
- Parité croissante avec CUDA sur les modèles supportés

## Compatibilité Transformers v5

vLLM 0.23.0 cible **Transformers v5** avec des corrections de compatibilité :
- Processeurs MiniCPM-V/O vendored
- Compatibilité Sarvam et Voxtral
- Support Voxtral `fetch_audio` pour `transformers≥5.10`

## Modèles ajoutés

En plus de GLM-5.2, cette release ajoute le support de :
- **Step-3.7-Flash**
- **Cosmos3 Reasoner**
- **Gemma 4 Unified** (encoder-free)
- **JetBrains Mellum v2**
- **Granite Speech Plus**
- **Cohere Mini Code**

## Note sur MiniMax M3

La release note précise explicitement que **MiniMax M3 n'est pas encore supporté**. Il faut suivre la recette dédiée sur le site vLLM recipes.

## Mise à jour

```bash
pip install -U vllm==0.23.0
```

Si vous utilisez Docker :
```bash
docker pull vllm/vllm-openai:v0.23.0
```

Pour les déploiements existants, le Model Runner V2 devrait s'activer automatiquement pour vos modèles Llama et Mistral. Vérifiez les logs au démarrage pour confirmer.

## Ce que ça change pour le local

vLLM n'est pas le runtime du laptop. Mais pour les serveurs locaux — un rack avec 2-8 GPU NVIDIA ou un cluster AMD — cette release rend le serving de modèles récents (GLM-5.2, DeepSeek-V4, Gemma 4) plus stable et plus rapide.

Le Model Runner V2 en défaut, c'est du gain de performance sans effort. Le KV cache multi-tier, c'est plus de requêtes concurrentes sans ajouter de RAM. Le frontend Rust, c'est une porte de sortie élégante si le Python devient un goulot.

Pour le reste de la stack locale (Ollama, llama.cpp, MLX), ces améliorations ne s'appliquent pas directement — mais elles rappellent que l'écosystème de serving open-source avance à un rythme soutenu.

## Sources

- [Release v0.23.0 — GitHub vllm-project/vllm](https://github.com/vllm-project/vllm/releases/tag/v0.23.0)
- [Releases vllm-project/vllm — GitHub](https://github.com/vllm-project/vllm/releases)
- [vLLM-Omni v0.23 integration — GitHub](https://github.com/vllm-project/vllm-omni/releases)
- [NewReleases — vLLM v0.23.0](https://newreleases.io/project/github/vllm-project/vllm/release/v0.23.0)
