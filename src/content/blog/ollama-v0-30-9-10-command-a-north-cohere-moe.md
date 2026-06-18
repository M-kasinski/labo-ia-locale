---
title: "Ollama v0.30.9/v0.30.10 : Cohere MoE, MLX Command A/North, llama.cpp 9672"
description: "Deux releases en trois jours : support des architectures MoE, extension MLX aux puces Apple récentes, et un update majeur de llama.cpp."
pubDate: 2026-06-18
tags: ["Ollama", "llama.cpp", "MLX", "Apple Silicon", "Cohere MoE", "local inference"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "Releasebot — Ollama Release Notes June 2026"
    url: "https://releasebot.io/updates/ollama"
  - label: "GitHub — ggml-org/llama.cpp releases"
    url: "https://github.com/ggml-org/llama.cpp/releases"
---

## La nouvelle

Ollama a poussé deux versions majeures en trois jours : **v0.30.9** (15–17 juin) et **v0.30.10** (17–18 juin). Ensemble, elles apportent le support de l'architecture Cohere2Moe, l'extension du moteur MLX aux puces Command A et North d'Apple, et un update de llama.cpp au build 9672.

## Détails techniques par release

### v0.30.10 (17–18 juin) — MLX expansion & backend
- **Command A et North sur MLX** : Les nouvelles familles de puces Apple sont maintenant supportées via le moteur MLX d'Ollama. Si tu as un Mac avec M5/M4 Pro, ça devrait fonctionner nativement.
- **llama.cpp build 9672** : Mise à jour du backend C/C++ — inclut les corrections de Metal GPU offload pour les modèles multimodaux (fixé en v0.30.4 mais raffiné ici).
- **Corrections MLX** : Build artifacts brisés réparés, `ollama create --experimental` respecte maintenant `REQUIRES` dans les Modelfiles pour les modèles MLX.

### v0.30.9 (15–17 juin) — MoE, context shift, agent output
- **Cohere2Moe architecture** : Support natif ajouté. Les modèles Mixtures of Experts de Cohere fonctionnent directement sous Ollama sans conversion manuelle.
- **Context shift pour fenêtres > 8k** : Déjà attendu depuis longtemps — les prompts shiftables avec context window étendu sont maintenant gérés proprement.
- **Erreur explicite si message > context window** : Plus de comportement silencieux bizarre, tu sais exactement quand tu dépasses.
- **Fix LFM2 parser** : Rendu correct quand le thinking output n'est pas émis.
- **Fix `ollama launch claude`** : Les agents de codage (Claude Code, Codex) ne sortaient qu'un seul token — réparé.
- **llama.cpp build 9637** → 9672 entre les deux releases.

### v0.30.8 (12 juin) — en bonus car très récent
- **KV cache decoupled from context shift** : Réutilisation de cache significativement améliorée, surtout pour les longues conversations.
- **MLX runner snapshots** : Pendant le prompt processing et le speculative decoding, MLX crée des snapshots pour plus de stabilité.
- **Recurrent models improved** : Support des modèles récurrents avec gated-delta kernels.

## Benchmarks / impact concret

Pas de chiffres officiels dans ces releases, mais les améliorations sont tangibles :
- Le fix KV cache + context shift devrait donner un gain visible sur les workloads avec longs contextes (>32k tokens).
- Le support Cohere MoE ouvre la porte aux modèles Cohere récents sans contorsion.
- Command A/North sur MLX = si Apple a sorti du matériel récent, il est maintenant utilisable pour l'inférence locale.

## Impact pour l'écosystème local

C'est une période dense pour Ollama — trois releases en 6 jours montre une cadence de développement intense. Le support MoE natif est un signal clair : les architectures Mixture of Experts ne sont plus un sujet de niche, elles arrivent dans les runners grand public. Pour qui self-host, ça signifie que les modèles MoE (Cohere et probablement d'autres suivront) deviennent directement utilisables sans bidouillage.

Le fix des agents de codage (`ollama launch claude`) est aussi important : si tu utilises Ollama comme backend pour tes workflows d'agents IA locaux, la version 0.30.9+ est un must-update.

## À surveiller

- Si d'autres architectures MoE (Qwen, DeepSeek) arrivent dans Ollama
- Les performances réelles de Command A/North sur MLX vs M4/M5 actuels
- La roadmap llama.cpp au-delà du build 9672
