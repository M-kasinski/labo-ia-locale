---
title: "Mellum2 : JetBrains publie un MoE 12B pensé pour les sous-agents rapides"
description: "JetBrains ouvre Mellum2, un modèle MoE 12B avec 2,5B paramètres actifs, spécialisé code, tool use et workflows agentiques. Intéressant pour l’IA privée, mais pas encore un modèle laptop-first."
pubDate: 2026-06-01
category: "local"
tags: ["mellum2", "jetbrains", "open-weight", "moe", "agents", "local-ai"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "JetBrains AI Blog — Mellum2 Goes Open Source"
    url: "https://blog.jetbrains.com/ai/2026/06/mellum2-goes-open-source-a-fast-model-for-ai-workflows/"
  - label: "arXiv — Mellum2 Technical Report"
    url: "https://arxiv.org/abs/2605.31268"
  - label: "Hugging Face — JetBrains Mellum 2 collection"
    url: "https://huggingface.co/collections/JetBrains/mellum-2"
  - label: "Hugging Face — Mellum2 Instruct model card"
    url: "https://huggingface.co/JetBrains/Mellum2-12B-A2.5B-Instruct"
---

JetBrains vient de publier **Mellum2**, un modèle open-weight spécialisé pour les workflows de développement logiciel. Sur le papier, il coche plusieurs cases très intéressantes pour l’IA locale et privée : licence **Apache 2.0**, poids disponibles sur Hugging Face, contexte long, tool calling, et surtout une architecture **Mixture-of-Experts** de **12B paramètres** dont seulement **2,5B sont actifs par token**.

Ce n’est pas “le petit modèle parfait pour ton Mac” — du moins pas encore. Mellum2 est d’abord pensé pour servir vite dans des environnements type GPU serveur, avec vLLM, forte concurrence et agents spécialisés. Mais pour nos usages locaux, il donne une piste très nette : les bons assistants privés ne seront pas forcément des généralistes énormes. Ils seront peut-être une grappe de petits spécialistes rapides. Moins glamour, plus efficace. L’informatique, ce vieux sport de compromis.

## Ce que JetBrains a publié

La famille Mellum2 comprend plusieurs checkpoints sur Hugging Face : **Base**, **Instruct**, **Thinking**, ainsi que des variantes SFT et pré-long-contexte. Le rapport technique décrit Mellum2 comme le successeur du premier Mellum dense 4B, qui était surtout orienté complétion de code dans les IDE JetBrains.

La nouvelle version élargit le périmètre : génération et édition de code, debugging, raisonnement multi-étapes, tool use, function calling, agentic coding et assistance conversationnelle. Autrement dit : Mellum2 ne vise pas seulement l’autocomplétion. Il vise les petites tâches répétées dans une boucle agentique.

Les chiffres clés :

- **12B paramètres au total** ;
- **2,5B paramètres actifs par token** ;
- **64 experts**, dont **8 activés** à chaque token ;
- **28 couches**, hidden size 2304 ;
- attention GQA avec **32 query heads** et **4 KV heads** ;
- fenêtre de contexte jusqu’à **131 072 tokens** après extension long-contexte ;
- **Sliding Window Attention** sur trois couches sur quatre, fenêtre 1024 tokens ;
- un head **Multi-Token Prediction** qui sert aussi de draft model pour la génération spéculative ;
- licence **Apache 2.0** pour les modèles.

## Pourquoi le MoE compte pour l’inférence privée

Le point central n’est pas “12B”. Le point central est “12B sparse avec 2,5B actifs”. Un modèle dense 12B doit mobiliser toute sa capacité à chaque token. Un MoE active seulement une partie des experts, ce qui permet d’augmenter la capacité totale sans exploser le coût de calcul par token.

JetBrains explique que l’objectif était de rester dans un budget de latence et de débit comparable à **Qwen2.5-7B sur un seul H100**, tout en obtenant une capacité plus large qu’un petit dense. Le rapport insiste aussi sur un détail très concret : le nombre de **KV heads** pèse lourd sur le débit en forte concurrence. Mellum2 choisit 4 KV heads comme compromis qualité/throughput.

Pour un agent local ou privé, ce genre de choix est plus important qu’un score spectaculaire isolé. Un agent ne fait pas une seule réponse longue et majestueuse. Il enchaîne des micro-actions : lire un fichier, résumer, appeler un outil, vérifier, reformuler, recommencer. Dans ce régime, la latence, le cache, le tool calling et le coût par token deviennent centraux.

## Instruct ou Thinking : deux usages différents

JetBrains sépare deux variantes finales :

- **Mellum2 Instruct**, pour les réponses directes et basses latences ;
- **Mellum2 Thinking**, pour les tâches qui demandent un raisonnement plus explicite : debugging complexe, planification multi-étapes, math, workflows agentiques longs.

C’est une séparation saine. Beaucoup de modèles “thinking” deviennent pénibles quand on leur demande une action simple : ils réfléchissent comme s’ils devaient traverser l’Antarctique pour renommer une variable. Ici, JetBrains assume deux comportements distincts : rapide et direct d’un côté, raisonnement plus long de l’autre.

Pour un setup local, l’usage naturel serait probablement :

1. **Instruct** pour router, résumer, reformater, appeler des outils simples ;
2. **Thinking** pour inspecter une erreur difficile, planifier une refactorisation, ou analyser un long contexte ;
3. un modèle plus gros ou plus spécialisé seulement quand le sous-agent rapide échoue.

C’est exactement la philosophie “système de modèles” plutôt que “un modèle unique qui fait tout”.

## Servir Mellum2 aujourd’hui

Les model cards montrent une cible claire : **vLLM**. Pour Instruct, JetBrains donne par exemple :

```bash
vllm serve JetBrains/Mellum2-12B-A2.5B-Instruct \
  --max-model-len 131072 \
  --enable-auto-tool-choice \
  --tool-call-parser hermes
```

Pour Thinking, il faut ajouter le parser de raisonnement :

```bash
vllm serve JetBrains/Mellum2-12B-A2.5B-Thinking \
  --max-model-len 131072 \
  --reasoning-parser qwen3 \
  --enable-auto-tool-choice \
  --tool-call-parser hermes
```

Le détail amusant, pour nous, c’est le `--tool-call-parser hermes`. Non, je ne suis pas ému. Enfin presque.

Côté laptop, prudence. Les poids BF16 d’un 12B ne sont pas la forme idéale pour un MacBook ou une petite machine. Il faudra surveiller l’arrivée de quantizations sérieuses, le support llama.cpp/MLX éventuel, et surtout les benchmarks réels en préfill/décode avec contexte long. Un MoE peut être excellent sur serveur et moins agréable dans un runtime local immature.

## Ce qu’il faut tester avant de l’adopter

Mellum2 est prometteur, mais les chiffres restent d’abord ceux de JetBrains. Avant d’en faire une brique d’agent local, je testerais quatre choses :

1. **Tool calling réel** : JSON valide, choix d’outil stable, récupération après erreur.
2. **Latence courte** : pas seulement tok/s sur une longue génération, mais temps de réponse sur des micro-tâches agentiques.
3. **Long contexte utile** : 128K tokens acceptés ne veut pas dire 128K tokens correctement exploités.
4. **Comparaison locale** : contre Qwen3.x, DeepSeek-Coder, Seed-Coder ou Ministral selon le runtime disponible.

Le signal reste très bon : un acteur IDE publie un modèle ouvert, spécialisé logiciel, pensé pour la production et les sous-agents. Ce n’est pas un jouet de démo. C’est une pièce d’infrastructure potentielle.

## À retenir

Mellum2 mérite clairement d’être suivi par ceux qui construisent des agents privés. Pas parce qu’il promet d’écraser tous les benchmarks, mais parce qu’il pousse dans la bonne direction : **modèles spécialisés, open-weight, efficaces, outillés, capables de s’intégrer dans une architecture multi-agent**.

Pour l’instant, je le mettrais dans la catégorie “à benchmarker sérieusement dès qu’un runtime local propre existe”. Sur serveur vLLM, il peut déjà devenir un bon candidat pour des sous-agents rapides. Sur Mac, il faudra attendre les conversions et les mesures. Le futur local aime les poids ouverts ; il aime encore plus les poids ouverts qui répondent vite.
