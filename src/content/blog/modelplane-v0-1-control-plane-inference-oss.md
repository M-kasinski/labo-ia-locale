---
title: "Modelplane v0.1 : le control plane open source pour flottes d'inférence"
description: "Upbound publie le 23 juin Modelplane (Apache 2.0) — déploiements déclaratifs, endpoint OpenAI unique, moteur agnostique (vLLM, llama.cpp, etc.) sur K8s."
pubDate: 2026-06-24
tags: ["Modelplane", "Crossplane", "Kubernetes", "vLLM", "self-hosting"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "GlobeNewswire — Upbound Launches Modelplane"
    url: "https://www.globenewswire.com/news-release/2026/06/23/3316226/0/en/upbound-launches-modelplane-the-open-source-control-plane-for-ai-inference.html"
  - label: "GitHub — modelplaneai/modelplane"
    url: "https://github.com/modelplaneai/modelplane"
---

## La nouvelle

Le **23 juin 2026**, **Upbound** (équipe **Crossplane**) sort **Modelplane v0.1.0** : un **control plane** open source (Apache 2.0) pour orchestrer des **flottes d’inférence** — cloud, néocloud ou **on-prem** — avec réconciliation continue (provisionnement, scheduling, scale, cache de poids, routage).

## Architecture en deux rôles

| Rôle | Ressources clés |
|------|-----------------|
| **Plateforme** | `InferenceCluster`, `InferenceClass`, `InferenceGateway` |
| **Développeur** | `ModelDeployment` (réplicas, sélecteurs GPU CEL), `ModelService` |

Exemple documenté : un pod **vLLM 0.23.0** avec `Qwen/Qwen2.5-0.5B-Instruct` sur GPU ≥ 20 GiB, exposé via un **endpoint unique compatible OpenAI** — sans que l’équipe app connaisse le détail du cluster.

## Pourquoi ça intéresse le local / l’hybride

- **Moteur agnostique** : les flags du conteneur portent parallélisme, quantisation, KV — Modelplane ne verrouille pas sur un seul runtime. Vous pouvez mixer **vLLM**, **llama.cpp server**, ou d’autres images sur la même flotte déclarative.
- **Cache de poids par cluster** : évite de retélécharger les mêmes GGUF/Safetensors sur chaque déploiement.
- **Canary / A/B** : routage pondéré au niveau `ModelService` — utile quand vous testez un nouveau quant ou un bump llama.cpp.

## Maturité réaliste

C’est un **v0.1** : APIs `v1alpha1`, comportement susceptible de bouger. La doc propose un démarrage sur **kind** ; la prod demande encore de la prudence. Upbound parle de donation future à une fondation OSS — à suivre.

## Impact écosystème

À mesure que les **modèles open-weight** (GLM-5.2, Kimi K2.7 Code, Nemotron, etc.) se multiplient, le goulot devient l’**exploitation** (GPU, versions moteur, endpoints). Modelplane vise la même couche d’abstraction que Crossplane a apportée à l’infra cloud — appliquée à l’**inférence**. Concurrent conceptuel des stacks « gateway + scripts », mais avec CRD Kubernetes natives.

Pour un labo local déjà sur K8s + GPU, c’est un signal à installer en **sandbox** avant de remplacer Ollama sur le MacBook — la cible, c’est plutôt **équipe plateforme** qui sert des modèles à toute l’orga.