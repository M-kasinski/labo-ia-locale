---
title: "llama.cpp 2026 : llama.app, MTP et WebGPU — le projet se réinvente"
description: "llama.cpp lance llama.app, son nouveau site officiel avec un CLI unifié. MTP pour Qwen3.6, WebGPU en production, et une intégration agents. Tour complet."
pubDate: 2026-05-30
category: "local"
tags: ["llama.cpp", "llama.app", "MTP", "WebGPU", "Qwen", "infrastructure locale"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "llama.app — site officiel"
    url: "https://llama.app/"
  - label: "llama.cpp — docs officielles"
    url: "https://llama-cpp.com/"
  - label: "GitHub — PR MTP Support #22673"
    url: "https://github.com/ggml-org/llama.cpp/pull/22673"
  - label: "Reddit LocalLLaMA — MTP benchmarks"
    url: "https://www.reddit.com/r/LocalLLaMA/comments/1tckzy2/multitoken_prediction_mtp_for_qwen_on_llamacpp/"
  - label: "DataCamp — Tutoriel MTP complet"
    url: "https://www.datacamp.com/tutorial/multi-token-prediction-llama-cpp"
  - label: "Unsloth — Guide Qwen3.6 local + MTP"
    url: "https://unsloth.ai/docs/models/qwen3.6"
  - label: "Wikipedia — llama.cpp"
    url: "https://en.wikipedia.org/wiki/Llama.cpp"
---

## Le projet qui a tout changé sort de l'ombre

Lancé en mars 2023 par Georgi Gerganov, **llama.cpp** est devenu le moteur d'inférence locale le plus utilisé au monde. Avec plus de 109 000 étoiles sur GitHub en mai 2026, c'est la colonne vertébrale invisible de la plupart des outils d'IA locale — Ollama, LM Studio, et bien d'autres reposent dessus.

En 2026, le projet fait un bond en avant avec trois évolutions majeures : un site officiel (**llama.app**), le support de la **prédiction multi-token (MTP)**, et un backend **WebGPU** en production. Décryptage.

## llama.app : un visage public pour le moteur invisible

Jusqu'ici, llama.cpp vivait principalement sur GitHub. Le projet lance maintenant **llama.app**, un site officiel avec une proposition claire :

> "AI that lives on your computer. Open-source, private, always local."

L'installation se réduit à une ligne :

```bash
curl -LsSf https://llama.app/install.sh | sh
```

### Un CLI unifié

Le gros changement : **`llama`**, une commande unifiée qui remplace l'ancien paysage fragmenté de binaires (`llama-cli`, `llama-server`, `llama-quantize`, etc.). La même commande gère :

- Lancement de modèles (`llama serve`)
- API compatible OpenAI
- Intégration avec les frameworks d'agents

### Intégration native avec Pi

llama.app met en avant **Pi**, un agent de codage local développé par badlogic. Le flux est simple :

```bash
# 1. Servir un modèle
llama serve

# 2. Installer le plugin Pi
pi install git:github.com/huggingface/pi-llama

# 3. Lancer Pi — il découvre automatiquement le modèle local
pi
```

Aucune configuration, aucune clé API, les données ne quittent jamais la machine. C'est le modèle de l'agent local privé, poussé à son极致.

### Modèles recommandés

Le site propose une sélection de modèles optimisés pour l'exécution locale :

| Modèle | Paramètres | Profil |
|---|---|---|
| **Qwen3.6-27B** | 27B | Sweet spot GPU unique |
| **Qwen3.6-35B-A3B** | 35B MoE · 3B actifs | Qualité 35B, vitesse 3B |
| **Gemma-4-26B-A4B** | 26B MoE · 4B actifs | MoE desktop de Google |
| **Gemma-4-E4B** | 4B effectifs | Ultra-léger, mobile |
| **gpt-oss-20b** | 20B | OpenAI open weights |
| **Step-3.5-Flash** | Flash | Généraliste rapide |

## MTP : le décodage spéculatif intégré au modèle

La **Multi-Token Prediction (MTP)** est l'une des avancées les plus pratiques de 2026 pour l'inférence locale. Contrairement au décodage spéculatif classique qui nécessite un second modèle "draft", MTP intègre les têtes de prédiction directement dans le modèle principal.

### Comment ça marche

Les modèles Qwen3.6 disposent de têtes MTP supplémentaires qui prédisent plusieurs tokens en parallèle à chaque étape. Le modèle vérifie ensuite ces prédictions et n'exécute le calcul complet que pour les tokens rejetés. Résultat : moins d'appels GPU, plus de vitesse.

### Les chiffres

Selon la PR #22673 de llama.cpp, testée sur Qwen3.6 27B et 35B-A3B :

- **Taux d'acceptation** : ~75% avec 3 tokens draft
- **Accélération** : >2x par rapport au baseline
- **Précision** : identique au modèle sans MTP (vérifié sur AIME2026)

Un benchmark indépendant (DataCamp, RTX 3090) confirme : **38 tok/s → 65 tok/s** avec le même Qwen3.6 27B, soit **+71%**.

### Activation

```bash
./llama-server -m "Qwen3.6-27B-Q4_K_M-mtp.gguf" \
  --spec-type draft-mtp --spec-draft-n-max 3 \
  --cache-type-k q8_0 --cache-type-v q8_0 \
  -ngl 99 -c 100000 -fa on
```

Note : le flag a changé de `--spec-type mtp` à `--spec-type draft-mtp` le 13 mai 2026.

## WebGPU : inférence dans le navigateur, zéro installation

Le backend **WebGPU** de llama.cpp est maintenant en production. Il permet de faire tourner des modèles GGUF directement dans un navigateur moderne, avec accélération GPU, sans que les données ne quittent la machine.

C'est le résultat d'un effort multi-années. Les implications sont significatives :

- **Zéro installation** : un lien web suffit pour lancer un modèle
- **Confidentialité totale** : tout reste dans le navigateur
- **Accessibilité** : les utilisateurs non techniques peuvent tester des modèles sans configurer CUDA, Metal ou ROCm

La limitation principale reste la puissance du GPU intégré du navigateur (généralement inférieur à un GPU dédié), mais pour des modèles de 3–8B en quantisation Q4, les vitesses sont déjà honorables.

## Compatibilité hardware

llama.app affiche une matrice de support impressionnante :

- **Apple Silicon** : M1, M2, M3, M4, M5 (Pro/Max/Ultra)
- **NVIDIA** : RTX 3090, RTX 4090, RTX 5090, A100, H100, B200
- **AMD** : MI300, Radeon RX
- **Intel** : Arc
- **Edge** : Jetson, DGX Spark
- **CPU pur** : supporté, avec AVX/AVX2/AVX512

Même le petit DGX Spark de NVIDIA (24 Go, conçu pour le développement) est dans la liste — preuve que llama.cpp vise vraiment tous les segments.

## Verdict

llama.cpp n'est plus seulement un repo GitHub — c'est un produit. llama.app apporte une expérience utilisateur cohérente à un projet qui a toujours été le moteur sous le capot. Le trio MTP + WebGPU + CLI unifié positionne llama.cpp comme la référence absolue pour l'inférence locale en 2026.

Si vous faites tourner des modèles localement et que vous n'avez pas encore testé Qwen3.6 avec MTP, vous manquez probablement un facteur 2 de performance gratuit.
