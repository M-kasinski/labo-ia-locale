---
title: "LFM2.5-230M : 230 millions de paramètres pour l’agent sur Raspberry Pi et humanoïde"
description: "Liquid AI publie le 25 juin 2026 son plus petit LFM2.5 — tool calling crédible, 42 tok/s sur Pi 5, démo Unitree G1 sur Jetson. Analyse pour l’inférence locale et les pipelines d’extraction."
pubDate: 2026-06-27
tags: ["Liquid AI", "LFM2.5", "edge", "llama.cpp", "MLX", "agents locaux", "MoE"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "Liquid AI — LFM2.5-230M blog"
    url: "https://www.liquid.ai/blog/lfm2-5-230m"
  - label: "Hugging Face — LiquidAI/LFM2.5-230M"
    url: "https://huggingface.co/LiquidAI/LFM2.5-230M"
  - label: "Référence Labo — LFM2.5-8B-A1B"
    url: "https://www.liquid.ai/blog/lfm2-5-8b-a1b"
---

## La nouvelle

**Liquid AI** a annoncé **LFM2.5-230M** le **25 juin 2026** : le plus petit membre de la famille **LFM2.5**, pensé comme **socle fine-tunable** pour workflows **agentiques** et **extraction de données**, pas comme mini-encyclopédie. Le message marketing tient en deux chiffres de débit annoncés : **213 tok/s** en décodage sur **Galaxy S25 Ultra**, **42 tok/s** sur **Raspberry Pi 5** — avec des scores BFCL et IFEval qui visent des modèles **2× plus gros**.

Le Labo avait déjà couvert **LFM2.5-8B-A1B** (MoE 8B / 1,5B actifs, laptop et MCP). Le 230M complète l’échelle vers le **ultra-edge** : capteurs, robots, téléphones, gateways IoT — partout où un 8B reste hors budget mémoire ou latence.

## Analyse technique

### Entraînement et recette post-training

Liquid décrit un pipeline en quatre temps :

1. **Pré-entraînement** sur **19T tokens**, avec phase d’**extension de contexte à 32K**.
2. **SFT** avec **distillation depuis LFM2.5-350M** (le petit apprend des traces du plus grand).
3. **DPO** (Direct Preference Optimization).
4. **RL multi-domaines** pour stabiliser tool use et extraction.

La distillation depuis **350M** est le choix intéressant : au lieu de pousser uniquement la taille, Liquid **transfère des comportements** (format d’appel d’outil, structure de réponse) vers un modèle qui tient dans quelques centaines de Mo une fois quantifié.

### Benchmarks annoncés (à lire avec les bonnes lunettes)

Sur **IFEval**, LFM2.5-230M affiche **71,71 %** — au-dessus de Gemma 3 1B IT et proche de Granite 4.0-H-350M. Sur **BFCLv3**, **43,26 %** : dans le peloton des modèles sub-billion, avec un écart notable vs LFM2-350M (**22,95 %**), signe que la recette 2.5 change surtout les **outils**, pas le savoir brut.

Sur **GPQA Diamond** (**25,41 %**), le modèle reste faible — et Liquid l’assume : **pas** recommandé pour maths avancées, génération de code lourde ou création littéraire. Le positionnement est honnête : **extraction + tools + instruction following**, pas reasoning frontier.

| Axe | LFM2.5-230M (annoncé) | Limite |
|-----|----------------------|--------|
| Tool calling (BFCLv3) | ~43 % | Derrière 350M/8B de la même famille |
| Instruction (IFEval) | ~72 % | Bon pour la taille |
| Raisonnement scientifique | GPQA ~25 % | Volontairement secondaire |
| τ² Retail / Telecom | modeste | Agents multi-tours encore fragiles |

### Démo robotique Unitree G1

Liquid montre un **G1** humanoïde avec inférence **on-device** sur **NVIDIA Jetson Orin** : le 230M sert de **couche de sélection de compétences** — langage naturel → séquence d’**appels d’outils** vers les primitives **SONIC** (NVIDIA). Exemple de prompt décomposé : marche avant à vitesse donnée, genou sur une jambe, retour arrière.

Ce n’est pas de l’AGI domestique ; c’est un **parseur de plan motorisé** fine-tuné rapidement. Pour le Labo, l’enseignement est général : à 230M, le modèle n’est pas le cerveau du mouvement, il est le **traducteur intention → API de bas niveau** — exactement le rôle qu’on donne à un routeur dans une stack Hermes/Ollama, mais avec des contraintes temps réel.

## Inférence locale : runtimes et réglages

Liquid annonce le support **jour 0** de :

- **llama.cpp** (GGUF edge),
- **MLX** (Apple Silicon),
- **vLLM** / **SGLang** (débit GPU),
- **ONNX** (accélérateurs variés).

Notes pratiques citées par Liquid pour le CPU :

- **Raspberry Pi 5** : flash-attention `-fa 1` pour maximiser le prefill.
- **Snapdragon Gen4** : `-fa 0` selon le profil mesuré (le meilleur réglage dépend du SoC).

Comparé à **LFM2.5-8B-A1B**, le 230M change de classe de machine :

- **8B-A1B** : agent desktop, dizaines d’outils MCP, laptop M-series.
- **230M** : **wake word → action**, OCR+slot filling, routeur dans un pipeline multi-modèles (gros VLM + petit LLM pour JSON).

Sur Mac, le chemin MLX reste le plus simple pour prototyper ; sur Linux ARM, **llama.cpp** GGUF est le dénominateur commun — cohérent avec la trajectoire **Ollama 0.30.x** qui remonte llama.cpp chaque semaine (voir article Labo sur v0.30.11).

## Impact pour l’écosystème local

1. **Preuve de concept « agent sous le watt »** : si BFCL tient en quantifié sur Pi 5, les intégrateurs domotique / industrie peuvent envisager des **LLM locaux** sans GPU datacenter.
2. **Complémentarité avec gros MoE** : pattern **230M routeur + 30B worker** (ou API cloud ponctuelle) pour garder la confidentialité sur l’intent et déléguer le code lourd.
3. **Concurrence Qwen3.5-0.8B / Gemma 3 1B** : la bataille sub-1B se joue sur **BFCL et latence**, pas sur MMLU — aligné avec les besoins agents 2026.
4. **Licence** : comme le 8B, vérifier **LFM Open License v1.0** (`lfm1.0` sur Hugging Face) — ce n’est pas Apache/MIT ; important pour redistribution produit.

## Limites honnêtes

- Les **42 tok/s** sur Pi 5 sont des chiffres constructeur ; ta charge (contexte long, batch, température) peut diviser par deux.
- **τ² Telecom / Retail** restent bas : ne pas attendre un agent commercial autonome sur 230M seul.
- La démo **G1** est un **fine-tune ciblé**, pas un modèle généraliste prêt pour n’importe quel robot.
- **Reproductibilité** : attendre les GGUF communautaires et les premiers retours `ollama pull` avant de figer une archi prod.

## Comment tester (sans blabla)

```bash
# Exemple llama.cpp — après publication du GGUF officiel ou communautaire
llama-cli -m LFM2.5-230M-Q4_K_M.gguf -p "Extract fields as JSON: ..." -n 256
```

Sur Apple Silicon :

```bash
pip install mlx-lm
# Charger le dépôt MLX quand disponible sur Hugging Face LiquidAI
```

Comparer toujours **latence p95** et **taux de JSON valide** sur *tes* prompts, pas sur la démo blog.

## Sources

- Liquid AI — LFM2.5-230M: Built to Run Anywhere (25 juin 2026) : https://www.liquid.ai/blog/lfm2-5-230m
- Hugging Face — LiquidAI/LFM2.5-230M : https://huggingface.co/LiquidAI/LFM2.5-230M
- Liquid AI — LFM2.5-8B-A1B (contexte famille) : https://www.liquid.ai/blog/lfm2-5-8b-a1b