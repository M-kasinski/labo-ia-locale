---
title: "WWDC 2026 session 232 : MLX-LM Server comme API OpenAI pour agents 100 % Mac"
description: "Apple documente une pile en quatre couches — MLX, MLX-LM, MLX-LM Server, agent — avec tool calling, batching continu et inférence distribuée Thunderbolt pour les gros MoE."
pubDate: 2026-06-24
tags: ["Apple", "MLX", "MLX-LM", "agents", "Apple Silicon", "self-hosting"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "Apple Developer — Run local agentic AI on the Mac using MLX (WWDC26-232)"
    url: "https://developer.apple.com/videos/play/wwdc2026/232/"
  - label: "Apple Machine Learning Research — MLX and Neural Accelerators on M5"
    url: "https://machinelearning.apple.com/research/exploring-llms-mlx-m5"
---

## Le signal

La session **WWDC26-232** (*Run local agentic AI on the Mac using MLX*), diffusée dans le cadre de la conférence développeur juin 2026, ne se contente pas de répéter « MLX est rapide ». Elle pose un **schéma d’architecture** pour faire tourner une boucle agentique complète **sans clé API** : l’utilisateur parle à un agent, l’agent appelle le modèle, le modèle déclenche des outils, les résultats regrossissent le contexte — et tout reste sur la machine.

Le message produit est clair : **MLX-LM Server** expose une API **compatible OpenAI** (chat completions + tool calling structuré). N’importe quel client qui sait pointer un `baseURL` local — OpenCode, scripts maison, certains IDE — peut brancher un agent sur un modèle quantifié Hugging Face sans réécrire la stack.

## Analyse technique

### La pile en quatre couches

| Couche | Composant | Rôle |
|--------|-----------|------|
| 1 | **MLX** | Tableaux, Metal, gestion mémoire unifiée |
| 2 | **MLX-LM** | Chargement, quantification, fine-tuning, milliers de modèles HF |
| 3 | **MLX-LM Server** | HTTP OpenAI-like, tool calling, modèles « reasoning » |
| 4 | **Agent** | Tout client du protocole chat completions |

Apple insiste sur un point que les utilisateurs d’Ollama connaissent sans le formaliser : **Ollama, LM Studio et d’autres outils populaires s’appuient déjà sur MLX ou des chemins proches sur Mac** — la session liste explicitement cet écosystème pour éviter l’illusion « il faut tout réinstaller ».

### Mise en route en trois commandes

La démo officielle propose :

```bash
pip install mlx-lm
mlx_lm.server --model mlx-community/Qwen-3.5-4B-8bit
```

Puis un `curl` sur `http://127.0.0.1:8080/v1/chat/completions` pour valider que le serveur répond. Pour **OpenCode**, la configuration type fixe `baseURL` à `http://127.0.0.1:8080/v1` et déclare un provider `mlx` — le modèle côté agent peut s’appeler `default_model` tant que le serveur l’accepte.

### Performance : le vrai ennemi, c’est le prefill agentique

Dans une boucle outils, **la majorité des tokens sont du prompt** (historique + sorties d’outils), pas de la génération. Apple relie ce constat aux **Neural Accelerators du GPU M5** : multiplication matricielle environ **4× plus rapide que sur M4**, avec des kernels MLX qui sélectionnent automatiquement le meilleur chemin — **sans flag supplémentaire côté utilisateur**.

Traduction terrain : lire un dépôt entier ou digérer un diff de PR avant la prochaine étape agentique devrait être nettement moins pénible sur M5 que sur la génération précédente — sous réserve de modèle et de quantification identiques.

### Concurrence : continuous batching sur MLX-LM Server

Quand un agent parent lance plusieurs sous-agents (doc, tests, recherche), les requêtes arrivent en parallèle. La session met en avant le **continuous batching** du serveur : les nouvelles requêtes peuvent rejoindre un batch GPU déjà en vol, au lieu de sérialiser bêtement la file — pattern proche de ce que vLLM popularise côté NVIDIA, mais ici sur mémoire unifiée.

### Multi-Mac : quand 512 Go ne suffisent pas

Exemple cité : un modèle type **DeepSeek ~1,6T paramètres** (>800 Go de poids) ne tient pas sur une seule machine, même haut de gamme. **MLX distributed inference** shard le modèle sur plusieurs Mac reliés par **Thunderbolt RDMA** (macOS 26.2+) ou Ethernet, avec une commande du type :

```bash
mlx.launch --hostfile hosts.json --backend jaccl \
  /remote/path/to/mlx_lm.server \
  --model mlx-community/Qwen-3.5-122B-A3B-8bit
```

Ce n’est pas du homelab trivial — il faut plusieurs machines, un réseau propre, et de la patience ops — mais c’est la première fois qu’Apple documente aussi explicitement ce scénario dans le fil **agents**, pas seulement « entraînement recherche ».

## Impact pour l’écosystème local

- **Interopérabilité** : un seul `baseURL` local remplace des intégrations propriétaires par outil ; tu peux comparer MLX-LM Server, llama-server `--agent`, ou Ollama MLX preview sur le **même client agent**.
- **Privacy by architecture** : la démo OpenCode + GitHub CLI ne sort que le trafic git vers le réseau ; le raisonnement reste on-device.
- **Pression sur les quantifs HF** : la session pousse des modèles `mlx-community/*` 8-bit — la qualité des conversions communautaires devient un facteur de prod aussi important que le choix du modèle brut.

## Limites honnêtes

- **Modèles tool-capable obligatoires** : un LLM sans function calling fiable fera une boucle agentique frustrante, quel que soit le serveur.
- **Distributed = ops** : Thunderbolt RDMA simplifie la latence, pas la coordination (chemins, versions MLX identiques, sécurité du réseau).
- **Recouvrement avec notre article WWDC du 9 juin** : celui-ci couvrait Core AI et Metal 4 ; ici le focus est **runtime agent HTTP**, pas le framework OS applicatif.

## Sources vérifiées

- [Session 232 — Run local agentic AI on the Mac using MLX](https://developer.apple.com/videos/play/wwdc2026/232/)
- [Apple ML Research — Exploring LLMs with MLX and M5 Neural Accelerators](https://machinelearning.apple.com/research/exploring-llms-mlx-m5)