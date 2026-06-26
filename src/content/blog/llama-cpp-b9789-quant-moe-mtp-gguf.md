---
title: "llama.cpp b9789 : la quantisation GGUF des MoE avec MTP ne casse plus silencieusement"
description: "Release du 25 juin 2026 : le build b9789 corrige la quantisation des architectures mixture-of-experts équipées de Multi-Token Prediction — un bug de pipeline qui touchait DeepSeek, GLM et co."
pubDate: 2026-06-26
tags: ["llama-cpp", "GGUF", "MoE", "MTP", "quantization", "DeepSeek"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "llama.cpp GitHub Releases — b9789"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9789"
  - label: "PR #24986 — quant: fix quantizing moe with mtp"
    url: "https://github.com/ggml-org/llama.cpp/pull/24986"
  - label: "Référence éditoriale — llama.cpp b9726 agent server"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9726"
---

## La nouvelle

**llama.cpp b9789**, publié le **25 juin 2026** sur GitHub, ne fait pas la une avec un nouveau backend GPU : le changelog tient en une ligne technique — **« quant : fix quantizing MoE with MTP »** ([PR #24986](https://github.com/ggml-org/llama.cpp/pull/24986)). Pour les équipes qui quantisent en local des **MoE open-weight** récents (DeepSeek V4, GLM-5.x, Kimi, etc.), c’est pourtant une correction de **pipeline** : sans elle, on peut produire des GGUF « valides » qui déraillent à l’inférence ou perdent la tête MTP.

## Analyse technique

### Rappel : MoE + MTP dans l’écosystème 2026

Deux mécanismes se superposent sur les frontier open-weight :

| Mécanisme | Rôle |
|-----------|------|
| **MoE (Mixture of Experts)** | Seule une fraction des experts est activée par token → mémoire et FLOPs réduits à l’inférence |
| **MTP (Multi-Token Prediction)** | Têtes auxiliaires qui prédisent plusieurs tokens en avance → meilleur débit via speculative decoding côté serveur |

Les convertisseurs `llama-quantize` / scripts Hugging Face → GGUF doivent connaître **à la fois** le graphe MoE (experts, routing) et les **têtes MTP** attachées au backbone. Un bug dans cette intersection ne provoque pas toujours un crash explicite : parfois un **écart de perplexité**, des sorties incohérentes après quelques centaines de tokens, ou un refus de charger la tête speculative.

### Ce que corrige b9789

La PR #24986 adresse précisément la **quantisation** (Q4_K_M, Q5_K_S, IQ4_XS, etc.) lorsque le modèle combine **MoE** et **MTP**. Avant ce patch :

- les tenseurs MTP pouvaient être **mal mappés** ou exclus du pass de quant ;
- les experts sparse et les têtes de prédiction multi-token partageaient des hypothèses de layout incorrectes dans ggml.

Après b9789, le chemin « Hugging Face → GGUF quantisé → `llama-cli` / `llama-server` » est aligné pour ces architectures — sous réserve d’utiliser un **convertisseur à jour** sur le même commit.

### Lien avec la cadence llama.cpp

Entre **b9784** (Hexagon, 24 juin) et **b9789** (25 juin), le dépôt reste sur un rythme de **plusieurs builds par jour**. Les binaires précompilés couvrent toujours :

- **macOS arm64/x64**, **CUDA 12.4 / 13.3**, **Vulkan**, **ROCm 7.2**, **SYCL**, **OpenVINO 2026.2**, **Android arm64**.

Les builds **KleidiAI** (macOS arm64) et **openEuler** restent **DISABLED** sur cette release — même statut que b9784.

### MTP en pratique locale

MTP n’est pas magique : il faut un runtime qui **consomme** les têtes (vLLM MTP, llama.cpp speculative, ou serveur custom). La correction de quantisation est la **première étape** : sans GGUF sain, aucun gain de tokens/s. Les lecteurs qui self-host DeepSeek V4 ou GLM-5.2 en GGUF devraient :

1. Re-quantiser depuis les safetensors avec les outils du tag **b9789** ou plus récent.
2. Comparer perplexité ou quelques prompts de référence avant/après.
3. Activer la speculative decoding seulement après validation qualitative.

## Impact pour l’écosystème local

1. **Réduction du risque « GGUF pourri »** — moins de threads Reddit « mon MoE 671B Q4 est stupide » causés par un outil de quant obsolète.
2. **Parité avec vLLM** — vLLM 0.22+ pousse MTP pour DeepSeek V4 ; llama.cpp reste la voie **CPU/GPU unique binaire** pour homelab ; cette fix maintient la crédibilité du format GGUF sur les mêmes modèles.
3. **Pinning obligatoire** — avec des fixes aussi ciblés, **master** ou une build d’il y a 48 h peut être fausse ; épingler `b9789` (ou supérieur) dans les Dockerfiles et scripts CI.

## Limites honnêtes

- **Une seule ligne de changelog** : pas de benchmark tokens/s fourni ; le gain est **correctness**, pas performance brute.
- **Ne remplace pas un convertisseur HF à jour** : si le `convert_hf_to_gguf.py` de ta branche ignore MTP, il faut aussi mettre à jour les scripts Python du repo.
- **Modèles non MoE ou sans MTP** : aucun bénéfice direct — tu peux rester sur ton build précédent si tu ne quantises que des dense classiques (Llama 3, Mistral).
- **b9802** (25 juin, plus tard dans la journée) n’ajoute pas de fonctionnalité documentée dans le corps de release accessible — ne pas confondre « tag plus récent » et « fix MTP ».

## Comment appliquer le correctif

```bash
# Récupérer le binaire macOS Apple Silicon pour b9789
curl -LO https://github.com/ggml-org/llama.cpp/releases/download/b9789/llama-b9789-bin-macos-arm64.tar.gz
tar xzf llama-b9789-bin-macos-arm64.tar.gz

# Ou compiler depuis la source au tag b9789
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp && git checkout b9789
cmake -B build -DGGML_METAL=ON   # ou GGML_CUDA=ON selon la machine
cmake --build build --config Release -j
```

Re-quantisation typique (adapter le modèle et le fichier de sortie) :

```bash
./build/bin/llama-quantize \
  ./models/mon-moe-mtp-f16.gguf \
  ./models/mon-moe-mtp-Q4_K_M.gguf \
  Q4_K_M
```

Puis valider avec `llama-cli` ou `llama-server --agent` si tu enchaînes sur une stack agentique locale (voir l’article **llama.cpp b9726** sur ce site pour le flag `--agent`).

## Sources vérifiées

- [Release b9789 — ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp/releases/tag/b9789)
- [PR #24986 — quant: fix quantizing moe with mtp](https://github.com/ggml-org/llama.cpp/pull/24986)