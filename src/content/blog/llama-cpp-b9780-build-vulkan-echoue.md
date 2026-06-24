---
title: "llama.cpp b9780 : fini les builds Vulkan « verts » mais cassés au runtime"
description: "La release b9780 corrige un bug de vulkan-shaders-gen qui laissait passer des libggml-vulkan invalides — symptômes typiques sur AMD, Intel Arc et builds maison, et ce qu’il faut faire concrètement."
pubDate: 2026-06-24
tags: ["llama-cpp", "Vulkan", "GGUF", "AMD", "GPU local", "build"]
category: "local"
author: "Labo IA"
draft: true
sources:
  - label: "GitHub Release b9780"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9780"
  - label: "Issue #24393 — shader failure did not stop build"
    url: "https://github.com/ggml-org/llama.cpp/issues/24393"
  - label: "PR #24450 — fail the build when a shader fails to compile"
    url: "https://github.com/ggml-org/llama.cpp/pull/24450"
---

## La nouvelle

**llama.cpp b9780**, publié le **24 juin 2026** (commit `1191758`), ne rajoute pas un kernel flashy ni un gain tok/s annoncé. Le changement qui compte pour une partie de l’écosystème local, c’est plus terre-à-terre et plus urgent : **un build Vulkan qui échoue à compiler un shader échoue enfin tout court**.

Jusqu’ici, l’outil **`vulkan-shaders-gen`** pouvait produire une **`libggml-vulkan` partiellement invalide** tout en laissant CMake et la CI afficher un succès. Le plantage arrivait plus tard — au premier `llama-cli`, `llama-server` ou wrapper (Ollama, LM Studio, etc.) qui chargeait le backend GPU. Pour les configs **sans CUDA** (AMD sous Linux ou Windows, **Intel Arc**, certaines machines hybrides), c’était un diagnostic pénible : « ça a compilé, donc le problème vient du modèle / du driver / de moi ».

Cette release aligne le comportement du build sur le bon sens : **pas de backend fantôme**.

## Analyse technique

### Pourquoi Vulkan compte en local

Sur Mac, **Metal** reste le chemin naturel. Sur Linux et Windows, beaucoup de setups « GPU grand public » passent par **Vulkan** ou **ROCm** plutôt que NVIDIA. llama.cpp shippe des binaires précompilés dédiés, dont :

- `llama-b9780-bin-ubuntu-vulkan-x64.tar.gz`
- `llama-b9780-bin-ubuntu-vulkan-arm64.tar.gz`
- `llama-b9780-bin-win-vulkan-x64.zip`

Ces artefacts embarquent des shaders SPIR-V générés à la compilation. Si la génération rate silencieusement, vous obtenez un binaire **apparemment sain** mais **fonctionnellement incomplet**.

### Le bug (issue #24393)

Deux défauts se combinaient dans `ggml/src/ggml-vulkan/vulkan-shaders/vulkan-shaders-gen.cpp` :

| Composant | Comportement avant correctif |
|-----------|------------------------------|
| **`execute_command()`** | Ignorait le code de sortie du sous-processus (`waitpid` sans statut côté POSIX ; pas de `GetExitCodeProcess` sous Windows) |
| **`string_to_spv()`** | Traitait l’échec surtout via **stderr non vide** — un compilateur qui sort en **code ≠ 0** avec stderr vide passait quand même |

Cas particulièrement vicieux : sous-processus qui **ne démarre pas** (`execvp` échoue, `_exit(EXIT_FAILURE)`), stderr vide → succès affiché.

### Le correctif (PR #24450, liminfei-amd)

1. **`execute_command()`** retourne le vrai exit code (`WEXITSTATUS` / `GetExitCodeProcess`).
2. **`string_to_spv()`** marque l’échec si exit ≠ 0, stderr non vide, ou exception au lancement ; flag **`std::atomic<bool> compile_failed`** (plusieurs workers en parallèle dans `process_shaders()`).
3. **`main()`** vérifie le flag **avant** `write_output_files()` et retourne **`EXIT_FAILURE`** — CMake s’arrête, plus de linkage d’un backend Vulkan tronqué.

**Portée :** uniquement **build-time**. Aucun changement annoncé sur les shaders eux-mêmes ni sur le runtime d’inférence une fois un build réussi.

Validation côté auteur : harness sans GPU (fork/exec, exit 3 simulé, binaire manquant), tests Linux **et** Windows (jeffbolznv), message explicite du type *« one or more shaders failed to compile »* quand on force un échec `glslc`.

## Ce que vous voyiez (et ce que vous verrez)

### Symptômes typiques *avant* b9780

- Build Vulkan **OK** en local ou en CI, puis **segfault**, erreur Vulkan obscure, ou backend GPU non utilisé au runtime.
- Écart entre un build **CPU-only** (qui marche) et le même commit en **`-DGGML_VULKAN=ON`** (qui casse à l’usage).
- Tickets du type « Ollama / llama.cpp plante sur RX 7900 / Arc A770 » alors que la compilation n’a jamais signalé d’erreur shader.

Ce n’était pas la seule cause possible (drivers, quant incompatible, VRAM), mais c’était une **cause structurelle** difficile à éliminer sans recompiler avec des logs shader.

### Après b9780

- Échec shader → **build rouge** immédiatement, avec message clair.
- Les binaires **`*-vulkan-*`** de cette release sont censés refléter un pipeline shader réellement passé.
- Si votre build casse maintenant alors qu’il « passait » avant : c’est en général **une bonne nouvelle** — vous découvrez un problème d’outillage (`glslc`, SDK Vulkan, toolchain) au bon moment.

## Impact pour l’écosystème local

### Ce que ça change

1. **Reproductibilité** : moins de « ça marche sur la machine du mainteneur, pas sur la mienne » pour des raisons cachées au link.
2. **Wrappers** : au prochain bump de llama.cpp embarqué dans Ollama ou autre, moins de versions intermédiaires avec Vulkan pourri mais livrées.
3. **Confiance dans les releases officielles** : les 27 assets de b9780 (CPU, CUDA, ROCm, SYCL, OpenVINO, Vulkan…) incluent des variantes Vulkan explicitement reconstruites sous la nouvelle règle.

### Ce que ça ne change pas

- **Pas de boost perf** documenté dans cette release — c’est de la **qualité d’ingénierie**, pas une optimisation de kernels.
- **Apple Silicon** : vous restez sur les builds **macos-arm64** (Metal), pas Vulkan.
- Un build qui **réussit** ne garantit pas que votre GPU/driver gère tous les quants ou toutes les tailles de contexte.

## Mise à jour recommandée

### Binaires précompilés

Télécharger l’artefact **b9780** correspondant à votre OS sur la [page Releases](https://github.com/ggml-org/llama.cpp/releases/tag/b9780). Si vous étiez sur des builds Vulkan custom des dernières semaines, **ce tag vaut le coup** même sans changer de fichier GGUF.

### Compilation maison (rappel)

```bash
cmake -B build -DGGML_VULKAN=ON
cmake --build build --config Release -j
```

Si le build échoue dans `vulkan-shaders-gen` après mise à jour : vérifier **`glslc`** (shaderc), version du **SDK Vulkan**, et les logs complets — le correctif est fait pour **surface** l’erreur, pas pour la contourner.

### Qui peut attendre

- Utilisateur **100 % Metal** (Mac) ou **CUDA** NVIDIA sans toucher Vulkan → impact indirect (meilleure hygiène du projet), pas une urgence personnelle.
- Utilisateur **AMD / Intel GPU via Vulkan** ou mainteneur de builds Linux → **mise à jour prioritaire**.

## Lien avec le reste de la roadmap llama.cpp

La semaine précédente, **b9726** avançait sur la couche **agent** (`--agent`, outils intégrés, MCP). **b9780** consolide la **fondation GPU** pour une partie de la base installée. Les deux ne se concurrencent pas : un agent local sur `llama-server` ne sert à rien si le backend Vulkan charge un binaire menteur. Pour un labo qui mixe **inférence locale + agents**, la combinaison « runtime agent récent + backend GPU fiable » est le minimum viable.

## Sources vérifiées

- [Release b9780](https://github.com/ggml-org/llama.cpp/releases/tag/b9780)
- [Issue #24393](https://github.com/ggml-org/llama.cpp/issues/24393)
- [PR #24450](https://github.com/ggml-org/llama.cpp/pull/24450)