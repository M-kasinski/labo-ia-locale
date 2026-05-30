---
title: "Ollama 0.19 : le backend MLX d'Apple double les performances sur Mac"
description: "Ollama intègre MLX comme backend natif sur Apple Silicon, avec des gains de 1.6x en prefill et 2x en decode. Analyse technique détaillée."
pubDate: 2026-05-30
tags: ["Ollama", "MLX", "Apple Silicon", "Apple", "infrastructure locale"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Annonce officielle Ollama — MLX backend"
    url: "https://ollama.com/blog/mlx"
  - label: "MacRumors — Ollama MLX coverage"
    url: "https://www.macrumors.com/2026/03/31/ollama-now-runs-faster-apple-silicon-macs/"
  - label: "Ars Technica — Analyse approfondie"
    url: "https://arstechnica.com/apple/2026/03/running-local-models-on-macs-gets-faster-with-ollamas-mlx-support/"
  - label: "9to5Mac — Ollama MLX adoption"
    url: "https://9to5mac.com/2026/03/31/ollama-adopts-mlx-for-faster-ai-performance-on-apple-silicon-macs/"
  - label: "Will It Run AI — Benchmarks MLX vs Ollama"
    url: "https://willitrunai.com/blog/mlx-vs-ollama-apple-silicon-benchmarks"
---

## Une rupture pour l'inférence locale sur Mac

Le 30 mars 2026, Ollama a annoncé une modification majeure de son architecture sur Apple Silicon : le passage à **MLX** comme backend natif, remplaçant llama.cpp/Metal pour l'exécution des modèles. Disponible en preview dans **Ollama 0.19**, ce changement promet des gains de performance substantiels sur toute la gamme M1–M5.

Pour les utilisateurs de Mac qui font tourner des modèles localement — agents de code, assistants personnels, expérimentations — c'est probablement la mise à jour la plus significative de l'année.

## Les chiffres

Selon les tests publiés par Ollama (menés le 29 mars 2026 sur un Mac M5 avec Qwen3.5-35B-A3B), les gains sont clairs :

| Métrique | Ollama 0.18 (llama.cpp) | Ollama 0.19 (MLX) | Gain |
|---|---|---|---|
| **Prefill** (tokens/s) | 1 154 | 1 810 | **+57%** |
| **Decode** (tokens/s) | 58 | 112 | **+93%** |

Ollama précise que les performances seront encore supérieures avec la quantisation int4 : **1 851 tok/s en prefill** et **134 tok/s en decode** dans cette configuration.

Ces chiffres concernent un modèle MoE de 35 milliards de paramètres (3 milliards actifs). Sur des modèles plus petits, le gain absolu sera moindre, mais le pourcentage reste comparable.

## Pourquoi MLX change la donne

MLX n'est pas un simple accélérateur : c'est un framework conçu par Apple spécifiquement pour l'architecture unifiée de ses puces. Trois différences fondamentales avec l'approche précédente :

### 1. Mémoire unifiée, zéro copie

Sur un Mac, le CPU, le GPU et le Neural Engine partagent le même pool de mémoire (jusqu'à 128 Go sur M5 Max). MLX exploite cette architecture nativement : les poids du modèle, les activations et le KV cache résident dans la même zone mémoire sans copie explicite CPU ↔ GPU.

Avec llama.cpp + Metal, une double mise en tampon était nécessaire pour transférer les données entre les espaces mémoire. MLX élimine ce goulot d'étranglement.

### 2. Compilation JIT vers Metal

MLX utilise une évaluation paresseuse (lazy evaluation) avec fusion de noyaux : le graphe de calcul est compilé à la volée en shaders Metal optimisés, minimisant les appels de lancement et le trafic mémoire. C'est similaire à la philosophie de JAX, mais cible Metal au lieu de CUDA.

### 3. GPU Neural Accelerators sur M5

Les puces M5, M5 Pro et M5 Max disposent de nouveaux accélérateurs neuronaux intégrés au GPU. Ollama 0.19 les exploite directement via MLX pour accélérer à la fois le temps avant le premier token (TTFT) et la vitesse de génération. C'est la raison pour laquelle les M5 voient les gains les plus importants.

## NVFP4 : un format de quantisation hybride

Ollama 0.19 introduit le support du format **NVFP4** de NVIDIA — une quantisation 4 bits en virgule flottante qui préserve la précision du modèle tout en réduisant drastiquement la bande passante mémoire et le stockage.

Pourquoi c'est pertinent sur Mac ? Parce que les modèles optimisés par NVIDIA Model Optimizer sont de plus en plus déployés en production cloud. Avec NVFP4, Ollama permet d'avoir **parité locale / cloud** : les mêmes modèles, les mêmes résultats, sans dépendre d'une API distante.

## Cache intelligent pour les agents

Au-delà de la vitesse brute, Ollama 0.19 améliore significativement la gestion du cache, ce qui impacte directement les cas d'usage agencés :

- **Réutilisation du cache entre conversations** : moins de mémoire consommée, plus de cache hits quand on branche depuis un system prompt partagé (typique de Claude Code, Codex, etc.)
- **Checkpoints intelligents** : Ollama sauvegarde des snapshots du cache à des points stratégiques dans le prompt, réduisant le re-traitement
- **Éviction plus intelligente** : les préfixes partagés survivent plus longtemps même quand les branches anciennes sont abandonnées

Ces améliorations rendent les agents de code locaux bien plus réactifs sur les sessions longues — un problème chronique jusqu'ici.

## Limitations actuelles

La preview a ses limites, il faut les connaître :

- **Un seul modèle supporté** : Qwen3.5-35B-A3B est le seul modèle disponible pour l'instant. Ollama travaille sur l'expansion des architectures supportées.
- **32 Go de RAM minimum** : la preview nécessite un Mac avec plus de 32 Go de mémoire unifiée. Les Mac 16 Go sont exclus pour le moment.
- **Preview, pas stable** : Ollama signale explicitement qu'il s'agit d'une preview. Des bugs sont possibles.

## Comparaison avec MLX direct

Pour les utilisateurs avancés qui utilisent MLX directement via `mlx-lm`, les benchmarks indépendants (Will It Run AI) montrent que MLX brut reste 15–30% plus rapide qu'Ollama avec backend MLX sur les mêmes configurations. Le compromis : Ollama offre une gestion de modèles, un API OpenAI-compatible et une intégration écosystème bien plus larges.

En pratique, la plupart des utilisateurs tireront profit de passer par Ollama plutôt que de configurer MLX manuellement.

## Comment tester

```bash
# Mise à jour vers Ollama 0.19
brew upgrade ollama

# Lancer avec le modèle Qwen3.5
ollama run qwen3.5:35b-a3b-coding-nvfp4

# Pour Claude Code
ollama launch claude --model qwen3.5:35b-a3b-coding-nvfp4
```

## Verdict

Ollama 0.19 est un tournant pour l'inférence locale sur Mac. Le passage à MLX n'est pas un simple patch de performance — c'est un changement architectural qui aligne Ollama avec les forces spécifiques du hardware Apple. Les gains de ~60% en prefill et ~90% en decode sont réels et mesurables.

La limitation à un seul modèle est légitime pour une preview, mais le signal est clair : Ollama mise gros sur Apple Silicon. Si vous avez un Mac avec 32 Go+ et que vous faites tourner des modèles localement, la mise à jour vaut le coup.
