---
title: "llama.cpp b9830 : llama download --offline pour pipelines air-gap et CI"
description: "Build du 28 juin 2026 : le CLI expose --offline sur llama download pour vérifier le cache GGUF sans réseau, avec correctif use-after-free sur les callbacks URL."
pubDate: 2026-06-28
tags: ["llama.cpp", "GGUF", "self-hosting", "CI", "cache", "ops"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "GitHub Releases — llama.cpp b9830"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9830"
  - label: "PR #25091 — common: allow --offline in llama download"
    url: "https://github.com/ggml-org/llama.cpp/pull/25091"
  - label: "Article de référence Labo — llama.cpp b9726 et --agent"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9726"
---

## La nouvelle

**llama.cpp b9830** est publié le **28 juin 2026** (tag `b9830`, commit `c1a1c8e`, build automatisé vers **11:03 UTC**). La release est dominée par une évolution **opérationnelle** du CLI : **`llama download` accepte désormais `--offline`**, pour qu’un script puisse **vérifier si un modèle est déjà en cache** et prêt à être servi **sans toucher au réseau**. Le même correctif **PR #25091** ferme un **use-after-free** latent dans le callback `on_done` des tâches URL (variable `first_path` capturée par référence après fin de scope).

Ce n’est pas un bump de performance GPU comme **b9828** (Flash Attention OpenCL) ou **b9827** (CUDA GDN) — c’est une brique pour **self-hosting sérieux** : air-gap, CI, démarrage de serveur agentique.

## Analyse technique

### Avant b9830 : téléchargement toujours « online-first »

Le sous-commande `llama download` (famille `common`) gère le pull de poids **Hugging Face** / URLs vers le cache local GGUF. Le flag **`--offline` existait déjà** dans la stack `common`, mais **n’était pas exposé** sur `llama download`. Conséquence :

- Un playbook du type « **démarrer le serveur seulement si le GGUF est présent** » devait bricoler avec `test -f`, parsing de cache, ou accepter un échec réseau ambigu.
- Les environnements **sans egress** (usine, labo, edge) ne pouvaient pas utiliser le même binaire pour **valider** le cache de façon officielle.

**PR #25091** (Adrien Gallouët, Hugging Face) aligne le comportement : `--offline` sur `llama download` = **sonde de readiness** sans fetch.

### Le bug UAF (pourquoi ça compte)

Dans le chemin URL-task, `first_path` était **block-scoped** mais le callback `on_done` la capturait **par référence** et s’exécutait **après** la fin du bloc. En pratique : comportement indéfini possible sur des téléchargements concurrents ou des scripts qui enchaînent plusieurs URLs — exactement le profil **CI / orchestration**.

La correction est dans le même PR que l’exposition `--offline` : une release « petite » mais **sécurité mémoire** réelle, pas du cosmétique.

### Chaîne de releases fin juin (où se place b9830)

| Build | Date (UTC) | Thème principal |
|-------|------------|-----------------|
| **b9827** | 27 juin | CUDA, snapshots GDN récurrents |
| **b9828** | 27 juin | Flash Attention OpenCL (q4/q8, MoE) |
| **b9829** | 28 juin ~06:46 | Réduction logs serveur / common (`COM_` rename) |
| **b9830** | 28 juin ~11:03 | **`download --offline`** + fix UAF |

Le rythme reste **plusieurs builds par jour** sur `master` — pinne un tag `bNNNN` avec binaire pour ta plateforme, pas « latest » flottant en prod.

### Exemple de pipeline (pattern recommandé)

```bash
# 1) En ligne : peupler le cache (une fois)
llama download --model org/model-name-GGUF

# 2) Au boot serveur / job CI : pas de réseau
llama download --offline --model org/model-name-GGUF \
  && llama-server -m /chemin/vers/cache/... --agent
```

L’intérêt se cumule avec **`--agent`** introduit en **b9726** : même binaire pour **vérifier les poids**, lancer **`llama-server`** avec outils intégrés et proxy MCP — stack locale cohérente.

## Impact pour l’écosystème local

### Pour qui c’est utile

1. **Stations GPU partagées** — un admin pré-télécharge les GGUF ; les utilisateurs ne déclenchent pas de pull accidentel au démarrage.
2. **CI/CD** — job « **model cache warm** » séparé du job « **inference smoke test** » en `--offline`.
3. **Ollama / LM Studio** — bénéfice indirect au prochain bump du submodule llama.cpp (Ollama **v0.30.11** du 25 juin embarque déjà une remontée llama.cpp).

### Ce que ça ne résout pas

- **`--offline` ne magique pas un GGUF absent** : il échoue proprement si le cache est incomplet — il faut un run online en amont.
- **Pas de nouveau format de quant** ni de kernel dans b9830 : pour le débit, reste sur **b9828** (OpenCL) ou les builds CUDA récents selon ton hardware.
- **KleidiAI macOS arm64** et builds **openEuler** restent **désactivés** sur la matrice de binaires (PRs #23780 / #23705) — vérifie la page assets avant de migrer.

### Limites honnêtes

- Documentation utilisateur encore **éparse** : le README `common` / `llama` reste la référence ; pas de guide dédié « air-gap » officiel.
- Les **27 assets** précompilés couvrent CUDA 12.4/13.3, Vulkan, ROCm 7.2, SYCL, OpenVINO 2026.2.1 — si tu compiles toi-même, tu récupères surtout le **fix CLI + UAF**.

## En synthèse

**b9830** transforme `llama download` en **sonde de cache offline** pour les déploiements locaux et les pipelines sans réseau, avec un correctif mémoire qui évite des crashs silencieux sur les téléchargements URL. Après une semaine très **GPU/kernel** (OpenCL, CUDA GDN), ggml-org consolide l’**exploitabilité** du runtime — logique quand llama.cpp se vend de plus en plus comme **plateforme agentique** et pas seulement comme moteur de tokens.

## Sources

- GitHub Releases — llama.cpp b9830 : https://github.com/ggml-org/llama.cpp/releases/tag/b9830
- PR #25091 — allow `--offline` in `llama download` : https://github.com/ggml-org/llama.cpp/pull/25091
- Référence agent serveur — b9726 : https://github.com/ggml-org/llama.cpp/releases/tag/b9726