---
title: "LM Studio 0.4.14 : le MTP Speculative Decoding arrive en stable"
description: "LM Studio intègre le Multi-Token Prediction en version stable — un gain de 1,5x à 3x en vitesse de génération, sans ajouter de modèle draft ni surcharger la VRAM."
pubDate: 2026-06-18
category: "local"
tags: ["LM Studio", "MTP", "Speculative Decoding", "llama.cpp", "performances"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "LM Studio Changelog 0.4.14"
    url: "https://lmstudio.ai/changelog/lmstudio-v0.4.14"
  - label: "LM Studio — Speculative Decoding Docs"
    url: "https://lmstudio.ai/docs/app/advanced/speculative-decoding"
  - label: "LocalLLM.in — MTP Tutorial"
    url: "https://localllm.in/blog/mtp-lm-studio"
  - label: "Reddit r/LocalLLaMA — Discussion MTP"
    url: "https://www.reddit.com/r/LocalLLaMA/comments/1ti99an/lm_studio_finally_added_support_for_mtp/"
---

## La nouvelle

LM Studio a publié la **version stable 0.4.14 (Build 4)** le 22 mai 2026, avec le **Multi-Token Prediction (MTP) Speculative Decoding** intégré nativement. Fini le beta, fini les builds expérimentaux — la fonctionnalité est accessible directement depuis l'interface graphique, sans ligne de commande.

### Qu'est-ce que le MTP, concrètement ?

Traditionnellement, un LLM génère **un token à la fois** : il calcule le prochain mot, l'ajoute au contexte, puis recalcul le suivant. C'est correct mais lent — chaque forward pass ne produit qu'un seul token.

Le **speculative decoding classique** contourne ce goulot en chargeant un deuxième modèle — un "draft model" léger — qui prédit plusieurs tokens d'avance. Le modèle principal vérifie ensuite ces tokens en parallèle. Le problème ? Deux modèles en mémoire, plus de VRAM consommée, plus de complexité.

Le **MTP (Multi-Token Prediction)** est différent : le modèle possède ses propres **heads de prédiction intégrés**. Il se sert de lui-même pour deviner plusieurs tokens futurs, puis les vérifie en un seul forward pass. Résultat :

- **Pas de second modèle** — zéro overhead VRAM supplémentaire
- **1,5x à 3x de gain en tokens/sec** selon le modèle et le matériel
- **Qualité identique** — les tokens non validés sont recalculés normalement

## Analyse technique

### Comment ça marche sous le capot

Les modèles avec MTP (Qwen 3.5, Qwen 3.6, DeepSeek R1 et d'autres) entraînent des **auxiliary prediction heads** en plus de la head principale. Chaque head prédit le token à une distance différente (t+1, t+2, t+3…). Pendant l'inférence :

1. Le modèle génère un token principal
2. Les heads MTP prédisent simultanément les N tokens suivants
3. Le modèle principal vérifie tous ces tokens en **un seul forward pass parallèle**
4. Les tokens validés sont acceptés ; le premier rejeté déclenche un recalcul normal

C'est le même principe que le speculative decoding, mais sans le coût mémoire d'un modèle draft séparé.

### Configuration dans LM Studio

Depuis l'interface de LM Studio 0.4.14 :

1. **Activer Developer Mode** dans Settings > Developer pour voir le taux d'acceptation MTP en temps réel
2. **Charger un modèle MTP-compatible** (ex: `unsloth/Qwen3.5-9B-MTP-GGUF`)
3. **Activer MTP Speculative Decoding** dans le panneau Load Model
4. **Ajuster les paramètres** :
   - `Maximum number of MTP draft tokens` : commencez à 2, montez progressivement
   - `Minimum MTP draft length to verify` : commencez à 0

### Benchmarks concrets

Sur une **RTX 4060 8GB** avec `Qwen3.5-9B-MTP-GGUF` (quant Q4_K_XL) :

| Configuration | Tokens/sec |
|---|---|
| Sans MTP | ~15 |
| MTP actif (draft: 2, min: 0) | ~22 |
| **Gain** | **+50%** |

Sur **Apple Silicon M3 Ultra**, le gain peut atteindre 2 à 4,2x selon les benchmarks communautaires. Le taux d'acceptation est la clé : au-delà d'un certain nombre de draft tokens, le modèle rejette trop de prédictions et le recalcul annule le gain.

### Quels modèles sont compatibles ?

Seuls les modèles **explicitemment compilés avec des heads MTP** fonctionnent. Les GGUF standards ne les ont pas. Les familles connues :

- **Qwen 3.5** (2B, 9B) — GGUF MTP disponibles via Unsloth
- **Qwen 3.6** — MTP préservé dans les conversions de llmfan et Unsloth
- **DeepSeek R1** — MTP natif
- **Gemma 3/4** — supporté via Ollama MLX mais pas encore via LM Studio

## Impact pour l'usage local

**C'est l'une des améliorations les plus tangibles de 2026 pour l'inférence locale.** Sans changer de matériel, sans ajouter de GPU, un simple toggle dans LM Studio donne un boost de 50% à 200%+ sur les modèles compatibles.

Pour les sessions de vibe coding, les workflow d'agents multi-tours, ou simplement les conversations longues, la différence entre 15 et 25 tokens/sec change radicalement l'expérience. Moins de temps à attendre, plus de flux.

Le seul bémol : la compatibilité modèle par modèle. Vérifiez que votre GGUF a bien été converti avec les heads MTP préservées — sinon le toggle n'aura aucun effet.
