---
title: "llama.cpp b9780 : le build Vulkan échoue enfin quand un shader casse"
description: "Sorti le 24 juin, b9780 corrige un bug silencieux de vulkan-shaders-gen qui produisait des binaires cassés tout en affichant succès — critique pour le local GPU AMD/Intel."
pubDate: 2026-06-24
tags: ["llama-cpp", "Vulkan", "GGUF", "build", "GPU local"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "GitHub Release b9780"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9780"
  - label: "PR #24450 — vulkan: fail the build when a shader fails to compile"
    url: "https://github.com/ggml-org/llama.cpp/pull/24450"
---

## La nouvelle

**b9780** est publié le **24 juin 2026** (commit `1191758`). Le changement le plus important pour l’écosystème local n’est pas un nouveau kernel de quantisation : c’est la **fiabilité du build backend Vulkan**.

## Le bug (issue #24393)

`vulkan-shaders-gen` **ignorait le code de sortie** des compilations de shaders (POSIX et Windows). Résultat typique :

1. Build **vert** côté CI ou compilation maison.
2. `libggml-vulkan` **partiellement invalide**.
3. Crash ou comportement bizarre **uniquement au runtime** sur GPU Vulkan (souvent AMD sous Linux/Windows, Intel Arc, etc.).

Pour qui self-host avec Ollama/LM Studio/llama-server sur Vulkan plutôt que CUDA, c’était un cauchemar de diagnostic.

## Le correctif

La PR **#24450** (liminfei-amd) :

- Propage le **exit code** du sous-processus (`WEXITSTATUS` / `GetExitCodeProcess`).
- Considère échec si exit ≠ 0, stderr non vide, ou exception au lancement.
- Flag **atomique** `compile_failed` ; `main()` retourne **`EXIT_FAILURE`** avant d’écrire les artefacts.

En clair : **plus de backend Vulkan fantôme**.

## Impact local concret

- **Reproductibilité** : les binaires précompilés `*-ubuntu-vulkan-*` et `win-vulkan-*` de cette release reflètent un build réellement sain.
- **Ollama / wrappers** : au prochain bump de llama.cpp embarqué, moins de tickets « ça compile mais ça plante à l’inférence ».
- **Pas de gain tok/s annoncé** : c’est de la **qualité d’ingénierie**, pas une optimisation perf — mais ça débloque des configs GPU locales qui étaient instables.

## Mise à jour recommandée

Télécharger les artefacts **b9780** correspondant à votre plateforme sur la page Releases, ou recompiler depuis le tag. Si vous étiez sur des builds Vulkan custom des dernières semaines, ce tag vaut le coup même sans changement de modèle GGUF.