---
title: "Ollama v0.30.11-rc1 : ollama launch muscle les agents, llama.cpp suit le rythme"
description: "Pré-release du 25 juin 2026 : auto-install des CLIs d’agents, speculative decoding MLX retuné, correctifs Vulkan Windows et bump llama.cpp — Ollama pousse le bouton « agent » plus loin."
pubDate: 2026-06-26
tags: ["Ollama", "agents locaux", "MLX", "llama.cpp", "Vulkan", "Apple Silicon"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "GitHub — Ollama release v0.30.11-rc1"
    url: "https://github.com/ollama/ollama/releases/tag/v0.30.11-rc1"
  - label: "Releasebot — Ollama June 2026 timeline"
    url: "https://releasebot.io/updates/ollama"
  - label: "Ollama Blog — MLX on Apple Silicon"
    url: "https://ollama.com/blog/mlx"
  - label: "Référence — Ollama v0.30 série juin"
    url: "https://github.com/ollama/ollama/releases/tag/v0.30.10"
---

## La nouvelle

**Ollama v0.30.11-rc1**, publiée le **25 juin 2026**, n’est pas une simple mise à jour de dépendances. La pré-release consolide la stratégie **« un binaire, un agent »** lancée avec `ollama launch` en juin : installation automatique de **Claude Code** et **OpenCode** quand les CLIs manquent, détection du niveau de *thinking* côté OpenCode, et correctif du drift de modèle quand l’UI **Codex App** change de checkpoint en cours de session.

En parallèle, l’équipe **remonte le moteur llama.cpp** embarqué (PR #16548) et corrige des bugs qui gênaient les setups hybrides **Windows iGPU/dGPU** et le comptage mémoire dans `ollama ps`.

## Analyse technique

### `ollama launch` : moins de friction, plus de garde-fous

Les changements les plus visibles pour les devs :

| PR / zone | Effet concret |
|-----------|----------------|
| #16802 | `ollama launch` peut **installer Claude Code** si absent |
| #16806 | Idem pour **OpenCode** |
| #15434 | Détection du **niveau thinking** pour OpenCode (évite les prompts mal routés) |
| #16864 | **Codex App** : alerte si l’UI bascule sur un autre modèle que celui servi par Ollama |

Sur le papier, c’est du polish. En pratique, ça réduit le nombre d’échecs silencieux quand on branche un IDE ou une app d’agent sur `localhost:11434` avec un tag local (`qwen3-coder`, `glm-4`, etc.). Le scénario typique — « l’agent répond une phrase puis meurt » — avait déjà été partiellement traité en **v0.30.9** ; cette rc1 pousse la cohérence **modèle affiché ↔ modèle servi**.

### MLX : speculative decoding unifié

Le PR **#16791** (*mlxrunner: unify and tune speculative decoding*) indique qu’Ollama **harmonise** la logique de décodage spéculatif sur le backend MLX. Après les annonces « meilleures perfs Apple Silicon » du **11 juin**, cette couche vise surtout la **stabilité** et le **réglage** plutôt qu’un nouveau record marketing.

Pour les Mac M-series, l’intérêt reste le même : garder des débits élevés sur modèles moyens (Gemma, Qwen, Command A / North sur MLX depuis v0.30.10) sans basculer sur une API cloud.

### llama.cpp embarqué : rattraper ggml-org

Le changelog mentionne explicitement une **mise à jour llama.cpp** (#16548). Ollama n’est plus un fork figé : chaque bump récupère les correctifs **GGUF**, **MoE**, **MTP** et serveur qui arrivent en rafale sur ggml-org (quant MoE+MTP, agent server `--agent`, kernels CUDA, etc.).

**Limite honnête :** en rc1, le tag exact du build llama.cpp n’est pas toujours documenté dans le corps de release — il faudra vérifier le submodule/commit dans le dépôt au moment du passage **stable v0.30.11**.

### Correctifs infra souvent sous-estimés

Plusieurs PRs ciblent la **fiabilité** plutôt que le headline :

- **#16669** — classification Vulkan **iGPU vs dGPU** sur Windows (évite d’offloader sur le mauvais GPU).
- **#16869** — chargeur Vulkan **hôte** sur Windows (meilleure compat pilotes).
- **#16856** — **headroom** de génération quand le contexte est *shifté* (moins de troncatures surprises).
- **#16709** — `ollama ps` ne **double plus** le poids mmap en offload partiel.
- **#16866** — offload **mmproj** dimensionné sur la mémoire du projecteur (VLMs).
- **#16868** — métadonnées **Qwen2.5-VL** fenêtre d’attention par défaut.
- **#16878** — endpoint **generate** aligné sur les **chat templates** natifs.

Pour qui self-host des modèles vision ou des configs multi-GPU Windows, ce sont des correctifs qui évitent des heures de debug « pourquoi mon 27B ne charge qu’à moitié ».

## Benchmarks et résultats

Ollama ne publie pas de tableau tok/s pour cette rc1. Les références utiles restent :

- **Blog MLX (juin)** : gains prompt processing / génération sur Qwen3.5-35B vs backend Metal historique (ordre de grandeur **+50 %** côté prefill dans les tests communautaires cités par Ollama).
- **v0.30.10** : **Command A / North** sur MLX Apple Silicon — pertinent si tu compares familles Cohere locales.

**Recommandation labo :** avant/après sur **ton** modèle (`ollama run` + même prompt 4k tokens, `OLLAMA_DEBUG=1` pour le backend choisi).

## Impact pour l’écosystème local

1. **Ollama comme couche d’onboarding agents** — La concurrence (LM Studio, llama-server `--agent`, MLX-LM Server WWDC) pousse tous les runtimes vers une **API OpenAI + tools**. Ollama mise sur `launch` + auto-install pour ne pas perdre les devs qui ne veulent pas lire trois README.
2. **Double moteur MLX + llama.cpp** — Sur Mac, MLX reste prioritaire quand le modèle est supporté ; ailleurs, llama.cpp élargit le catalogue **GGUF** et le matériel (CUDA, Vulkan, ROCm via binaires upstream).
3. **Pré-release = tester sans paniquer** — rc1 signifie : valider sur une machine de dev avant de déployer sur un serveur partagé. Les changements `launch` touchent l’exécution de binaires tiers (Claude Code, OpenCode).

## Limites

- **Statut rc1** : pas encore la stable ; possible breaking change avant tag final.
- **Agents ≠ sécurité** : auto-install de CLIs facilite l’usage, pas l’isolement. `exec` et tools restent à borner.
- **Pas de nouveau modèle flagship** dans cette release — c’est une release **plateforme**, pas une annonce Moonshot/Zhipu.

## Sources

- [Ollama v0.30.11-rc1 — GitHub Releases](https://github.com/ollama/ollama/releases/tag/v0.30.11-rc1)
- [Releasebot — fil Ollama juin 2026](https://releasebot.io/updates/ollama)
- [Ollama — MLX on Apple Silicon](https://ollama.com/blog/mlx)