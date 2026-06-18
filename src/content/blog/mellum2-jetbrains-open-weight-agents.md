---
title: "Mellum2 : JetBrains mise sur un modèle ouvert rapide plutôt qu’un frontier généraliste"
description: "Avec Mellum2, JetBrains publie un MoE 12B open-weight spécialisé software engineering. Le pari : des agents de production rapides, orchestrés, moins chers à servir."
pubDate: 2026-06-01
category: "veille"
tags: ["jetbrains", "mellum2", "open-weight", "agents", "coding", "moe"]
author: "Veille IA"
draft: false
sources:
  - label: "JetBrains AI Blog — Mellum2 Goes Open Source"
    url: "https://blog.jetbrains.com/ai/2026/06/mellum2-goes-open-source-a-fast-model-for-ai-workflows/"
  - label: "arXiv — Mellum2 Technical Report"
    url: "https://arxiv.org/abs/2605.31268"
  - label: "Hugging Face — JetBrains Mellum 2 collection"
    url: "https://huggingface.co/collections/JetBrains/mellum-2"
  - label: "Hugging Face — Mellum2 Thinking model card"
    url: "https://huggingface.co/JetBrains/Mellum2-12B-A2.5B-Thinking"
---

JetBrains a publié **Mellum2**, un modèle open-weight spécialisé pour les workflows logiciels. Ce n’est pas un modèle frontier généraliste qui veut battre tout le monde sur toutes les tâches. C’est plus intéressant que ça : un modèle d’infrastructure, pensé pour les agents, le routage, le RAG, les sous-tâches rapides et les environnements privés.

La thèse est claire : dans les systèmes IA de production, le gagnant n’est pas toujours le modèle le plus massif. C’est souvent celui qui répond assez bien, assez vite, assez souvent, avec un coût que l’on peut supporter. Ce n’est pas très romantique, mais les factures cloud ont rarement lu de poésie.

## Un MoE 12B, mais 2,5B actifs par token

Mellum2 est un **Mixture-of-Experts** de **12B paramètres**, avec environ **2,5B paramètres actifs par token**. Le rapport technique détaille une architecture avec **64 experts**, **8 experts activés**, 28 couches, de la Grouped-Query Attention, du Sliding Window Attention sur trois couches sur quatre, et une extension de contexte jusqu’à **131K tokens**.

Ce choix met Mellum2 dans une zone intermédiaire : plus de capacité totale qu’un petit dense, mais un coût d’inférence plus proche d’un modèle bien plus compact. JetBrains indique avoir visé le budget de latence et de débit d’un **Qwen2.5-7B sur un seul H100**, tout en cherchant à améliorer les tâches de code, d’outils et de raisonnement.

C’est important parce que le marché des modèles se fragmente. Les grands généralistes restent essentiels, mais les produits réels commencent à ressembler à des systèmes : routeurs, validateurs, extracteurs, sous-agents, modèles spécialisés, outils, mémoire, et parfois un gros modèle seulement quand il faut vraiment sortir l’artillerie.

## JetBrains ne vend pas un chatbot, mais une brique de système

Le blog de JetBrains positionne Mellum2 pour des usages très concrets : routage, Q&A, résumés, sous-agents, RAG, déploiement privé, workflows de développement logiciel. Ce vocabulaire compte. Il ne s’agit pas seulement d’avoir “un modèle qui code”. Il s’agit d’avoir un composant capable de vivre dans une chaîne de production.

Le rapport décrit Mellum2 comme un successeur du Mellum 4B dense orienté complétion de code. La nouvelle famille vise beaucoup plus large : génération et édition de code, debugging, tool use, function calling, agentic coding et assistance conversationnelle.

JetBrains publie plusieurs checkpoints : **Base**, **Instruct**, **Thinking**, ainsi que des variantes SFT et pré-long-contexte. Les poids sont disponibles dans une collection Hugging Face, sous licence **Apache 2.0**.

## Instruct contre Thinking : le bon découpage

Mellum2 existe notamment en deux variantes finales :

- **Instruct**, pour les réponses directes, la basse latence, le chat, le code et le tool use ;
- **Thinking**, pour les tâches de debugging complexe, planification multi-étapes, math et workflows agentiques plus lourds.

Ce découpage est plus mature qu’un unique modèle “raisonnant” utilisé partout. Dans un agent logiciel, une grande partie des étapes ne mérite pas une longue chaîne de raisonnement : classifier une tâche, résumer un log, choisir un outil, transformer une réponse en JSON, vérifier une contrainte. Pour ces micro-actions, la vitesse et la fiabilité sont plus importantes que la profondeur.

À l’inverse, certaines tâches exigent un modèle qui accepte de réfléchir plus longtemps : diagnostiquer une suite de tests étrange, planifier une migration, comprendre un bug avec beaucoup de contexte. La séparation Instruct/Thinking permet d’orchestrer ces deux régimes au lieu de les mélanger.

## Les choix techniques racontent une priorité : servir vite

Le rapport technique est intéressant parce qu’il parle beaucoup d’inférence, pas seulement de scores. JetBrains explique avoir testé des architectures denses, des variantes MLA, plusieurs configurations de GQA, et différentes granularités MoE. Le choix final — 64 experts, 8 actifs, 4 KV heads, Sliding Window Attention majoritaire — reflète une obsession assez saine : conserver du débit sous contrainte.

Mellum2 inclut aussi un head **Multi-Token Prediction**. Dans le rapport, il sert à la fois d’objectif auxiliaire de préentraînement et de draft model intégré pour la génération spéculative. Ce genre de détail montre que l’équipe ne pense pas seulement “qualité du modèle”, mais “forme du modèle une fois servi”.

Sur les benchmarks, JetBrains affirme que Mellum2 est compétitif face à des modèles open-weight entre **4B et 14B**, tout en fonctionnant avec le compute par token d’un dense 2,5B. Il faut traiter ces résultats comme des chiffres constructeur, donc utiles mais à vérifier indépendamment. La prudence n’est pas du scepticisme gratuit ; c’est l’hygiène de base dans une industrie où chaque graphique aime porter un smoking.

## Pourquoi c’est un signal pour l’Europe et l’open-weight

Le signal stratégique est double.

D’abord, JetBrains est un acteur très proche du workflow développeur. Publier un modèle ouvert spécialisé software engineering n’est pas un geste abstrait : c’est aligné avec des années d’usage IDE, complétion, refactoring, inspection de code et assistance développeur.

Ensuite, Mellum2 renforce une tendance : les modèles open-weight ne cherchent plus seulement à imiter les chatbots généralistes fermés. Ils se spécialisent dans des niches économiquement utiles : code, agents, long contexte, tool use, déploiement privé, latence. C’est là que l’open peut être compétitif, même sans budgets frontier.

Le fait que les poids, le rapport technique et plusieurs checkpoints soient publiés donne aussi plus de prise aux développeurs : audit, fine-tuning, tests internes, serving privé, comparaison sur ses propres workloads. C’est exactement ce qui manque aux modèles seulement accessibles par API.

## Ce qu’il faut surveiller maintenant

Mellum2 doit encore passer l’épreuve la plus importante : les retours indépendants. Les questions utiles sont simples :

1. Est-il réellement stable en **tool calling** sur des agents de code ?
2. Le contexte 131K est-il exploitable, ou seulement accepté par l’API ?
3. La variante Thinking améliore-t-elle les tâches difficiles sans exploser la latence ?
4. Les gains de throughput tiennent-ils hors des environnements JetBrains ?
5. Les développeurs vont-ils produire des quantizations et runtimes pratiques hors vLLM ?

Si les réponses sont positives, Mellum2 pourrait devenir un modèle de sous-agent très crédible : pas forcément celui qui résout tout, mais celui qui fait tourner beaucoup de petites décisions vite et proprement.

## À retenir

Mellum2 est moins spectaculaire qu’une annonce “frontier”, mais peut-être plus représentatif de la prochaine phase des agents IA : des systèmes composés de modèles spécialisés, rapides, ouverts et orchestrés.

JetBrains ne dit pas “voici le modèle ultime”. Il dit plutôt : voici une brique pour faire fonctionner des workflows IA réels avec moins de latence et moins de coût. Dans le contexte actuel, c’est une annonce sérieuse. Et une bonne nouvelle pour l’open-weight : la compétition ne se joue pas seulement au sommet, elle se joue aussi dans les rouages.
