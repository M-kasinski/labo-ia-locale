---
title: "llama.cpp b9784 : la matmul Hexagon passe en tuiles 32×32 — les MoE embarqués respirent"
description: "Sortie du 24 juin 2026 : le build b9784 de llama.cpp refond MUL_MAT et MUL_MAT_ID sur Qualcomm Hexagon (HMX/HVX), avec graphes mis en cache et correctifs OLMoE/LFM."
pubDate: 2026-06-24
tags: ["llama-cpp", "Hexagon", "NPU", "MoE", "GGUF", "edge"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "llama.cpp GitHub Releases — b9784"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9784"
  - label: "PR #24954 — hexagon: MUL_MAT and MUL_MAT_ID rework"
    url: "https://github.com/ggml-org/llama.cpp/pull/24954"
---

## La nouvelle

**llama.cpp b9784**, publié le **24 juin 2026** sur GitHub, est dominé par une refonte profonde du backend **Hexagon** (NPU Qualcomm). Le changelog officiel résume l’enjeu en une ligne : rework de `MUL_MAT` et `MUL_MAT_ID` avec repack de poids en tuiles **32×32**, paramètres de kernels côté hôte, et **mise en cache des graphes** pour éviter de recalculer la configuration à chaque passe.

Ce n’est pas le genre de release qui fait le buzz sur Reddit Mac M4 — c’est du travail de fond pour l’inférence **on-device** (Android, SoC Qualcomm récents). Mais pour l’écosystème local au sens large (tout ce qui n’est pas un pod H100), c’est un signal : llama.cpp continue d’élargir le périmètre matériel au-delà de CUDA/Metal/Vulkan.

## Analyse technique

### Pourquoi les tuiles 32×32 changent la donne

Sur Hexagon, le goulot historique des `MUL_MAT` open-source, c’est l’alignement entre :

- la **mémoire VTCM** (très petite, très rapide sur le NPU) ;
- le **DMA** 2D pour charger les poids ;
- et les chemins **HMX** (matmul accéléré) vs **HVX** (fallback vectoriel).

La PR #24954 introduit un format de poids `_tiled` permanent (l’ancien `x4x2` disparaît), aligne les tuiles sur le DMA, et déplace **la sélection du kernel et tous les paramètres de matmul sur l’hôte**. Résultat annoncé : moins de recomputation, meilleure utilisation des pipelines d’activation, et un solveur qui tient compte du nombre de threads d’activation — détail ingrat, critique quand plusieurs requêtes partagent le même graphe.

### MoE : `MUL_MAT_ID` enfin moins fragile

Les modèles **MoE** (experts sparse) stressent `MUL_MAT_ID` : mauvaise répartition du travail entre threads HVX et traçage HMX, et paramètres kernel incohérents entre hôte et NPU. Cette release cite explicitement des correctifs pour **OLMoE** et **LFM** — deux familles que la communauté edge commence à regarder pour des démos hors datacenter.

Côté quantisation dynamique, les notes mentionnent un **quantizer vectorisé pour q8_1**, des optimisations `dyn.quant` pour `q8_0` / `q8_1`, et des accumulateurs intermédiaires en **fp16** dans les kernels HVX tiled (reconvertis en fp32) pour gagner en précision sans sacrifier le débit annoncé.

### Seuil matériel : arch ≥ v73, HMX requis

Point à noter pour les intégrateurs : le support des architectures Hexagon **antérieures à v73** est retiré pour la plupart des cas d’usage — **HMX devient la condition réaliste** pour exploiter ce chemin. Si tu testes sur un vieux kit de dev, ce build ne t’apportera probablement rien ; si tu cibles des puces récentes avec HMX, c’est là que le diff se joue.

### Ce que b9784 n’est pas

Entre **b9726** (flag `--agent` pour `llama-server`, 19 juin) et **b9784**, la cadence reste d’une dizaine de builds par jour. b9784 n’ajoute pas de nouvelle couche agentique : c’est une release **backend NPU**. Sur Mac Apple Silicon, le binaire `macos-arm64` continue de passer par Metal ; l’intérêt direct pour un homelab M-series est indirect (meilleure parité des modèles MoE testés aussi sur desktop).

## Impact pour l’écosystème local

1. **Parité MoE** : corriger OLMoE/LFM sur Hexagon profite indirectement à tous les runtimes qui suivent ggml — les bugs de routing d’experts sont souvent partagés au niveau graphe.
2. **Edge + confidentialité** : plus le NPU tient des modèles sparse correctement, plus des workflows 100 % locaux deviennent crédibles sur téléphone / tablette / PC ARM Qualcomm — sans passer par une API cloud.
3. **Pinning** : avec cette cadence, **épingler un tag `bNNNN`** reste la seule stratégie sérieuse en production locale ; « j’ai compilé master il y a deux semaines » n’a plus de sens.

## Limites honnêtes

- **Pas de benchmark tokens/s publié** dans la release note : il faudra des mesures communautaires sur un SoC précis (Snapdragon 8 Gen x, etc.).
- **Hexagon ≠ universel** : la majorité des lecteurs du Labo tournent encore sur Apple Silicon ou NVIDIA — ce build les concerne surtout si ils packagent une app mobile.
- **Complexité opérationnelle** : variables comme `GGML_HEXAGON_MM_SELECT` et la profondeur DMA (`n_prefetch`) demandent de la calibration ; ce n’est pas du « télécharger GGUF et go ».

## Comment tester (Android / Hexagon)

```bash
# Exemple générique : récupérer le binaire arm64 Android pour b9784
curl -LO https://github.com/ggml-org/llama.cpp/releases/download/b9784/llama-b9784-bin-android-arm64.tar.gz
tar xzf llama-b9784-bin-android-arm64.tar.gz
# Puis lancer llama-cli ou llama-server selon ton pipeline, avec backend Hexagon activé à la compilation
```

Sur desktop, la voie habituelle reste de **cloner le tag b9784** et de compiler avec les flags backend de ta plateforme (`GGML_CUDA`, `GGML_METAL`, etc.).

## Sources vérifiées

- [Release b9784 — ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp/releases/tag/b9784)
- [PR #24954 — hexagon MUL_MAT / MUL_MAT_ID rework](https://github.com/ggml-org/llama.cpp/pull/24954)