---
title: "llama.cpp : le chemin CUDA out_prod passe en GEMM batché (jusqu’à 282×) — et HIP rattrape le train"
description: "Fusion du 26 juin 2026 : PR #24426 batch les broadcasts out_prod via cublasSgemmBatched ; #25033 répare les builds AMD/MUSA. Décryptage pour stations GPU locales."
pubDate: 2026-06-26
tags: ["llama-cpp", "CUDA", "ROCm", "HIP", "performance", "GGUF"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "PR #24426 — CUDA batch out_prod broadcast with cublasSgemmBatched"
    url: "https://github.com/ggml-org/llama.cpp/pull/24426"
  - label: "PR #25033 — cublasSgemmBatched mapping for HIP/MUSA"
    url: "https://github.com/ggml-org/llama.cpp/pull/25033"
  - label: "Release b9810 — llama.cpp"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9810"
  - label: "Issue #25038 — HIP compile bug (closed)"
    url: "https://github.com/ggml-org/llama.cpp/issues/25038"
---

## La nouvelle

Deux PRs enchaînées le **26 juin 2026** illustrent la vélocité — et les risques — du moteur le plus utilisé en inférence locale :

1. **[#24426](https://github.com/ggml-org/llama.cpp/pull/24426)** fusionnée : le backend **CUDA** remplace des boucles de `cublasSgemm` par un seul appel **`cublasSgemmBatched`** pour l’opération **`out_prod`** en mode broadcast (`dps2 > 1`).
2. **[#25033](https://github.com/ggml-org/llama.cpp/pull/25033)** fusionnée le même jour : ajout de l’alias **`hipblasSgemmBatched` / `mublasSgemmBatched`** dans les en-têtes vendeur, car la première PR avait **cassé les builds HIP/MUSA** et bloqué la chaîne de release (**tag b9810**).

Ce n’est pas une feature « agent » visible dans le CLI — c’est du **ggml** sous le capot. Mais sur GPU NVIDIA récents, ce genre de kernel peut se traduire en **latence plus basse** sur des architectures MoE, MTP ou tout graphe qui enchaîne des `out_prod` broadcast.

## Analyse technique

### Contexte : pourquoi `out_prod` ?

Dans **ggml**, `out_prod` (produit extérieur) apparaît dans des graphes de calcul où une dimension est **broadcastée** : une même tranche de `src0` est réutilisée sur plusieurs « slices » (`ne2`, `ne3`). Avant #24426, le chemin CUDA avec `dps2 > 1` lançait **`ne2 × ne3` GEMM séparés** — correct, mais coûteux en overhead driver/API.

La PR [#22651](https://github.com/ggml-org/llama.cpp/pull/22651) avait déjà batché le cas **stride uniforme** (`dps2 == 1`) avec `cublasSgemmStridedBatched`. Il restait le cas broadcast, explicitement marqué dans le code comme nécessitant `cublasSgemmBatched` + tableaux de pointeurs.

### Ce que fait #24426

- Un **petit kernel device** construit les tableaux de pointeurs A/B/C par GEMM, en gérant le broadcast `(i2 / dps2)` et `(i3 / dps3)`.
- Un seul **`cublasSgemmBatched`** remplace la boucle host.
- **Correctness** : `test-backend-ops test -o OUT_PROD` → **71/71** (seuil NMSE existant `5e-4`), plus **memcheck** sans erreur.

### Chiffres publiés (RTX 5090, F32)

Auteur **leonardHONG** — à prendre comme **signal relatif**, pas comme promesse sur ton 3060/4090 :

| Scénario | Avant | Après | Speedup |
|----------|-------|-------|---------|
| `ne2=256`, GEMM 256×16×16 | 2161 µs | 7.7 µs | **~282×** |
| `ne2=32`, GEMM 256×16×16 | 262 µs | 3.3 µs | **~79×** |
| `ne2=2` (petit batch) | 11.2 µs | 3.1 µs | **~3.6×** |
| GEMM 1024³ (compute-bound) | 877 µs | 649 µs | **~1.35×** |

**Lecture honnête :** le gain maximal arrive quand beaucoup de **petits GEMM** sont émis (typique de certains patterns broadcast). Sur un gros cube 1024³, le kernel reste **compute-bound** : le batching aide, mais ne divise pas le temps par 100.

### La chute HIP/MUSA et le fix #25033

Dès le merge de #24426, **CISC** signale la CI **MUSA/HIP** rouge : `cublasSgemmBatched` n’était pas mappé vers **`hipblasSgemmBatched`** dans les headers compat CUDA.

[#25033](https://github.com/ggml-org/llama.cpp/pull/25033) corrige ça — contenu principal du **release b9810** (26 juin, build **Latest** sur GitHub). [#25038](https://github.com/ggml-org/llama.cpp/issues/25038) documente le bug compile côté AMD.

**Leçon infra :** llama.cpp shippe des binaires **ROCm 7.2**, **HIP Radeon Windows**, **SYCL**, etc. Chaque nouveau symbole `cublas*` doit avoir son **alias vendeur** avant merge, sinon la communauté AMD compile depuis des sources cassées pendant des heures.

## Impact pour l’écosystème local

| Profil | Impact attendu |
|--------|----------------|
| **RTX 40/50, CUDA 12/13** | Meilleure efficacité sur graphes touchant `out_prod` broadcast ; utile avec modèles récents (MoE, MTP assistants Gemma, etc.) au fil des merges ggml. |
| **AMD ROCm / HIP Windows** | Sans #25033, **build from source** bloqué après #24426 — b9810 rend la branche **master** à nouveau compilable pour ces backends. |
| **CPU-only / Metal** | Pas d’effet direct ; le projet reste multi-backend par design. |
| **Ollama / LM Studio** | Bénéfice **indirect** au prochain bump du submodule llama.cpp (Ollama 0.30.11-rc1 annonce déjà un update llama.cpp). |

## Comment en profiter

1. **Binaire** : télécharger **b9810** ou plus récent sur [GitHub Releases](https://github.com/ggml-org/llama.cpp/releases) (variante CUDA alignée sur ton driver).
2. **Source** : `git pull` sur `master` après le 26 juin 2026, rebuild avec `GGML_CUDA=1` (ou preset ROCm si AMD).
3. **Mesure** : comparer `llama-bench` ou ton workload agent **avant/après** sur le **même GGUF** — les micro-benchmarks ggml ne se traduisent pas toujours en +X tok/s global.

## Limites

- Pas de benchmark **tok/s end-to-end** publié par les mainteneurs pour un modèle nommé (Llama 4, Qwen3, etc.).
- Les chiffres **282×** concernent un micro-op, pas une session Chat complète.
- **KleidiAI macOS arm64** et builds **openEuler** restent **désactivés** sur b9810 (voir notes de release) — planifier en conséquence.

## Sources

- [PR #24426 — CUDA out_prod batched path](https://github.com/ggml-org/llama.cpp/pull/24426)
- [PR #25033 — HIP/MUSA cublasSgemmBatched mapping](https://github.com/ggml-org/llama.cpp/pull/25033)
- [Release b9810](https://github.com/ggml-org/llama.cpp/releases/tag/b9810)
- [Issue #25038 — compile HIP (fermée)](https://github.com/ggml-org/llama.cpp/issues/25038)