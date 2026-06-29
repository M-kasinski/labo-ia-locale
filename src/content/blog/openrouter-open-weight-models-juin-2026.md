---
title: "OpenRouter dresse la carte des open-weights qui comptent en juin 2026"
description: "Le billet du 27 juin 2026 de Chris Clark (OpenRouter) classe DeepSeek V4 Flash, GLM 5.2, MiniMax M3 et Nemotron 3 Ultra — avec prix, licences et cas d’usage pour basculer hors des APIs fermées."
pubDate: 2026-06-29
tags: ["open-weight", "OpenRouter", "DeepSeek", "GLM-5.2", "MiniMax", "Nemotron", "coût"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "OpenRouter Blog — The Open Weight Models that Matter: June 2026"
    url: "https://openrouter.ai/blog/insights/the-open-weight-models-that-matter-june-2026/"
  - label: "OpenRouter — DeepSeek V4 Flash"
    url: "https://openrouter.ai/deepseek/deepseek-v4-flash"
  - label: "OpenRouter — Z.AI GLM 5.2"
    url: "https://openrouter.ai/z-ai/glm-5.2"
---

## Le signal

Le **27 juin 2026**, **OpenRouter** publie une synthèse rarement aussi actionnable : *« The Open Weight Models that Matter »*. Chris Clark y pose une thèse simple — l’écart d’intelligence entre poids ouverts et labs US **ne se creuse pas** comme prévu (~3–6 mois de retard), mais **chaque point fixe du leaderboard devient moins cher** avec le temps. Quatre modèles sortent du bruit de fond pour les équipes qui veulent **réduire la facture API** sans retomber sur un MoE qui ne sait que réciter des benchmarks.

Ce n’est pas une release technique d’inférence locale, mais c’est **directement utile au Labo** : beaucoup de lecteurs self-hostent **et** routent une partie du trafic via OpenRouter / Fireworks / Together pour comparer avant de télécharger 400 Go de GGUF.

## Analyse : les quatre piliers

### 1. DeepSeek V4 Flash — agentique à prix cassé

OpenRouter le présente comme le **premier open-weight crédible en pipeline agentique** face à des modèles Anthropic/OpenAI « classe frontier ».

| Indicateur | Valeur citée |
|------------|----------------|
| Architecture | ~284B total / ~13B actifs MoE, **1M contexte** |
| SWE-bench Verified | **79,0 %** (Pro à 80,6 %) |
| Licence | MIT |
| Prix API first-party (indicatif) | ~0,14 $ / 0,28 $ par M tokens in/out ; cache ~0,029 $/M input |

**Lecture Labo** : pour du **coding agent** à volume, Flash est le **premier essai** ; Pro seulement si le delta ~1,6 point SWE vaut le premium. Attention : route first-party = **rétention données pour entraînement** ; OpenRouter documente des hôtes **no-train** occidentaux (~2× le prix first-party, toujours bien en dessous de GPT-5.5).

### 2. GLM 5.2 — planning long horizon (contexte Fable)

Sorti mi-juin (**Zhipu / Z.ai**), GLM 5.2 est positionné sur la **qualité de planification** et le **coding agentique long**, pas sur le record de prix.

| Indicateur | Valeur citée |
|------------|----------------|
| AA Intelligence Index v4.1 | **#1 open à 51** (Nemotron 48, Kimi K2.6 43) |
| GDPval-AA v2 (agentique) | **niveau GPT-5.5 xhigh** côté open |
| Prix moyen OpenRouter | ~0,447 $ / 3,31 $ par M in/out |
| Licence | MIT (poids) |

Le billet relie explicitement GLM 5.2 au **blackout Fable 5 / Mythos 5** (contrôles export US mi-juin) : pour les entreprises, un MoE MIT **téléchargeable + routable** devient un **plan de continuité**, pas seulement un choix économique.

**Limite** : modèle **text-only**, **verbeux** (tokens de sortie chers), très récent → variance entre providers (~78 tok/s annoncés).

### 3. MiniMax M3 — seul multimodal de la liste

~428B / ~23B actifs, **1M contexte**, **MiniMax Sparse Attention (MSA)** : attention sparse par blocs sur le vrai KV-cache, pas une couche retrieval séparée.

| Indicateur | Valeur citée |
|------------|----------------|
| AA Index v4.1 | 44 (tied V4 Pro) |
| GDPval-AA | ~niveau Claude Sonnet 4.6 |
| Prix OpenRouter | ~0,098 $ / 1,21 $ par M in/out (hausse au-delà de 512k) |

**Cas d’usage** : screenshots, UI, diagrammes, vidéo — workflows **vision + agent** où GLM ou DeepSeek text-only ne suffisent pas. Licence **MiniMax Community** (pas MIT) : attribution requise, gros déploiements commerciaux → autorisation écrite.

### 4. NVIDIA Nemotron 3 Ultra — pari US + stack NVIDIA

550B / 55B actifs, hybride **Mamba-2 + Transformer MoE**, NVFP4, 1M contexte, MTP. Index open **48** (#2 derrière GLM). OpenRouter mentionne une route **`:free`** populaire mais **sans SLA prod**.

Licence **OpenMDW** — pertinent si tu optimises déjà pour **TensorRT / NIM** ; moins « drop-in MIT » que DeepSeek ou GLM.

## Tableau décision rapide (juin 2026)

| Priorité | Modèle à tester en premier |
|----------|----------------------------|
| Coût agent / SWE | DeepSeek V4 Flash |
| Refactor repo, plan multi-étapes | GLM 5.2 |
| UI, captures, vidéo | MiniMax M3 |
| Stack NVIDIA enterprise | Nemotron 3 Ultra |
| 100 % local, zéro API | Télécharger poids + vLLM / llama.cpp (hors scope du billet, mais même hiérarchie qualité) |

## Lien avec l’inférence locale

OpenRouter ne remplace pas **GGUF sur Apple Silicon** ou **vLLM sur RTX**. Il sert de **sonde** :

1. **Comparer** le même harness (Claude Code, Codex, script OpenAI) sur 4 open-weights sans gérer 4 stacks GPU.
2. **Décider** quel checkpoint mériterait un téléchargement (ex. GLM-5.2 MIT si tu as 256 Go unifiés ou un rack GPU).
3. **Filtrer géopolitique** : contrôles pays d’origine et politique de données dans l’UI OpenRouter — utile post-EO US juin sur les modèles **cyber-capables** fermés.

Le site du Labo a déjà couvert **GLM-5.2** (fiche locale), **Z.ai / Reuters** (finance + continuité), et **harness engineering** ; cet article complète avec la **cartographie coût / cas d’usage** côté agrégateur, datée **27 juin 2026**.

## Ce que le billet ne résout pas

- **Benchmarks indépendants** : les chiffres SWE / AA viennent surtout des éditeurs et d’OpenRouter ; à rejouer sur *ton* repo.
- **Latence locale** : 78–84 tok/s cloud ≠ tok/s sur ton M4 ou ta 4090 en Q4_K_M.
- **Régulation** : MIT sur les poids n’efface pas les règles d’**export** ou de **données** de ton secteur.

## Sources vérifiées

- Article OpenRouter, **27 juin 2026** : https://openrouter.ai/blog/insights/the-open-weight-models-that-matter-june-2026/  
- Fiches modèles : https://openrouter.ai/deepseek/deepseek-v4-flash , https://openrouter.ai/z-ai/glm-5.2 , https://openrouter.ai/minimax/minimax-m3 , https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b  

**En bref** : en fin de mois de juin 2026, la question n’est plus « est-ce qu’un open-weight peut tenir la route ? » mais **lequel**, pour **quel layer** (prix, planning, multimodal, NVIDIA), et **avec quelle politique de données**. OpenRouter en fait une grille lisible ; à toi de valider sur ton harness avant de migrer la prod — ou avant de remplir le disque de ton NAS de GGUF.