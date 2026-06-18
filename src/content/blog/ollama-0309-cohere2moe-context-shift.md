---
title: "Ollama 0.30.9 : support Cohere2Moe et gestion avancée du contexte"
description: "La version 0.30.9 d'Ollama introduit le support de l'architecture Cohere2Moe, un système de context shift pour les fenêtres >8k, et corrige des bugs critiques sur les agents de code."
pubDate: 2026-06-17
tags: ["ollama", "cohere", "moe", "context-shift", "local-inference"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "Ollama GitHub Releases v0.30.9"
    url: "https://github.com/ollama/ollama/releases/tag/v0.30.9"
  - label: "Releasebot — Ollama June 2026 Updates"
    url: "https://releasebot.io/updates/ollama"
---

## La nouvelle

Ollama **v0.30.9**, publiée le 15 juin 2026, apporte deux nouveautés techniques majeures : le support de l'architecture **Cohere2Moe** (Mixture of Experts) et un système de **context shift** pour les fenêtres de contexte supérieures à 8k tokens.

## Analyse technique

### Cohere2Moe — MoE dans Ollama
Cohere a publié des modèles utilisant une architecture Mixture of Experts, où seuls certains « experts » (sous-réseaux) sont activés par token. C'est plus efficace en inference : moins de calcul par token tout en maintenant la capacité du modèle global.

Ollama implémente maintenant le routage d'experts pour cette architecture. Concrètement :
- Les modèles Cohere MoE peuvent tourner localement sans serveur dédié
- Le routage dynamique sélectionne les experts pertinents par token
- Réduction de l'empreinte mémoire par rapport à un modèle dense équivalent

### Context shift pour fenêtres >8k
Nouveau mécanisme qui décale automatiquement la fenêtre de contexte quand elle dépasse 8k tokens. Au lieu de tronquer brutalement ou de tout rejouer, Ollama :
- Identifie les prompts « shiftables » (les parties du contexte qui peuvent être déplacées)
- Décale intelligemment pour garder les informations pertinentes
- Retourne une erreur explicite si un message unique dépasse la fenêtre

C'est important pour les agents de code et les workflows longs où le contexte s'accumule.

### Corrections critiques
- **LFM2 parser** : correction du rendu quand les tags de reasoning ne sont pas émis
- **ollama launch claude** : résolution d'un bug bloquant qui limitait la sortie à un seul token — critique pour les agents de code locaux

## Impact pour l'écosystème local

Le support MoE dans Ollama ouvre la porte à une nouvelle génération de modèles efficaces localement. Les architectures MoE permettent de maintenir des capacités élevées avec moins de FLOPs par inference — exactement ce qu'on veut pour du matériel grand public.

La gestion améliorée du contexte change aussi l'expérience des agents locaux : plus de troncations silencieuses, plus de bugs silencieux sur les longues conversations.

## Sources vérifiées

- [Ollama v0.30.9 sur GitHub](https://github.com/ollama/ollama/releases/tag/v0.30.9)
- [Releasebot — Ollama June 2026](https://releasebot.io/updates/ollama)
