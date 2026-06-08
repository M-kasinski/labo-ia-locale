---
title: "LFM2.5-1.2B-JP-202606 : Liquid AI affine le japonais local en format GGUF, MLX et ONNX"
description: "Liquid AI publie une révision japonaise de son petit modèle LFM2.5. Le signal intéressant n’est pas la taille, mais la disponibilité directe pour llama.cpp, MLX, ONNX et vLLM."
pubDate: 2026-06-08
tags: ["Liquid AI", "LFM2.5", "japonais", "GGUF", "MLX", "edge AI"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Hugging Face — LiquidAI/LFM2.5-1.2B-JP-202606"
    url: "https://huggingface.co/LiquidAI/LFM2.5-1.2B-JP-202606"
  - label: "Hugging Face — LiquidAI/LFM2.5-1.2B-JP-202606-GGUF"
    url: "https://huggingface.co/LiquidAI/LFM2.5-1.2B-JP-202606-GGUF"
  - label: "Liquid AI — Introducing LFM2.5: The Next Generation of On-Device AI"
    url: "https://www.liquid.ai/blog/introducing-lfm2-5-the-next-generation-of-on-device-ai"
---

Liquid AI continue de pousser LFM2.5 dans une direction assez saine pour l’IA locale : des modèles petits, spécialisés, et publiés dans plusieurs formats d’inférence au lieu d’un unique checkpoint difficile à exploiter. La nouveauté du jour est **LFM2.5-1.2B-JP-202606**, une révision du modèle chat japonais **LFM2.5-1.2B-JP**. La fiche Hugging Face le présente comme le dernier modèle généraliste japonais de Liquid AI, avec des progrès en connaissance, suivi d’instructions, maths, code et tool-use par rapport à la version JP précédente et à des modèles de taille comparable.

Ce n’est pas un modèle géant. C’est précisément l’intérêt. À **1,2 milliard de paramètres**, il vise les cas où l’on veut de la langue japonaise correcte sur une machine locale, un laptop, un serveur léger ou un appareil edge, sans basculer vers un 8B ou 14B juste pour répondre à des tickets, extraire des champs ou piloter des outils en japonais.

## Ce que Liquid AI publie réellement

La fiche principale indique que **LFM2.5-1.2B-JP-202606** est un modèle texte, bilingue japonais/anglais, basé sur **LiquidAI/LFM2.5-1.2B-Base**. Le modèle est publié sur Hugging Face avec le tag `transformers`, en `safetensors`, sous **LFM Open License v1.0**. Ce point de licence compte : ce n’est pas une licence OSI classique type Apache 2.0 ou MIT. Pour un usage personnel ou expérimental, cela ne bloque généralement pas grand-chose ; pour une intégration commerciale, il faut lire le texte de licence au lieu de supposer que “open-weight” veut dire “faites ce que vous voulez”. Le vieux piège, avec un ruban neuf.

Le plus utile pour le local est la liste des formats explicitement documentés par Liquid AI. Le checkpoint natif est recommandé pour **Transformers** et **vLLM**. Une version **GGUF** est publiée pour **llama.cpp** et les outils compatibles, avec l’objectif annoncé de réduire l’empreinte mémoire et de faciliter l’inférence CPU. Une version **ONNX** est mentionnée pour l’inférence cross-platform et l’accélération matérielle sur divers environnements. Une version **MLX 8-bit** est indiquée pour Apple Silicon.

La carte GGUF donne même une commande minimale : `llama-cli -hf LiquidAI/LFM2.5-1.2B-JP-202606-GGUF`. C’est le genre de détail qui fait gagner du temps. Un modèle local n’est pas seulement un fichier de poids : c’est un chemin d’exécution reproductible.

## Les chiffres : bons, mais fournisseur

Liquid AI publie un tableau de benchmarks japonais sur la fiche Hugging Face de la version 202606. Le modèle obtient notamment **54,19 sur JMMLU**, **79,08 sur J-MIFEval**, **62,20 sur J-GSM8K**, **62,80 sur J-MATH500**, **49,39 sur JHumanEval+**, **48,00 sur J-BFCLv3**, pour une moyenne de domaine annoncée à **53,11**. Ces chiffres sont comparés à LFM2.5-1.2B-Instruct, LFM2.5-1.2B-JP, Qwen3-1.7B, Qwen3-1.7B-Base, Llama-3.2-1B-Instruct et d’autres petits modèles.

Dans le billet de lancement LFM2.5, Liquid AI donnait déjà des chiffres pour la première version JP : **50,7 sur JMMLU**, **58,1 sur M-IFEval japonais** et **56,0 sur GSM8K japonais**. La révision 202606 semble donc surtout renforcer l’instruction following, les maths et l’usage d’outils selon le tableau publié sur Hugging Face. Je formule volontairement avec prudence : je n’ai pas trouvé d’évaluation indépendante récente reproduisant ces résultats sur un protocole public complet. Les scores sont donc **des résultats fournisseur vérifiés à la source**, pas un classement neutre de l’écosystème japonais.

C’est suffisant pour signaler le modèle, pas suffisant pour déclarer un vainqueur. Nuance ennuyeuse, donc utile.

## Pourquoi c’est intéressant pour l’auto-hébergement

Les modèles japonais locaux ont souvent un problème de compromis : les petits modèles généralistes répondent vite mais perdent les nuances culturelles ou les consignes complexes ; les modèles plus gros s’en sortent mieux mais deviennent moins agréables à servir sur Mac, mini-PC ou GPU modeste. Un 1.2B spécialisé japonais peut occuper une place très pratique : assistant interne, tri de tickets, extraction légère, classification, reformulation, génération contrôlée, ou premier étage d’un pipeline RAG japonais.

La présence de **GGUF** est importante pour les utilisateurs de llama.cpp, Ollama ou LM Studio dès que les intégrations suivent. Sur CPU ou petite machine, le format GGUF reste le chemin le plus simple pour tester rapidement un modèle quantifié. La présence de **MLX** est également pertinente : sur Apple Silicon, MLX donne souvent une expérience plus fluide pour les petits modèles, notamment quand on veut intégrer l’inférence dans une application Python ou un service local. **ONNX**, de son côté, ouvre la porte aux runtimes plus industriels et à certains accélérateurs edge.

La fiche recommande le modèle pour des workflows agentiques, du tool-use, des sorties structurées, des assistants bilingues anglais-japonais et des assistants personnels on-device. Elle précise aussi qu’il n’est **pas recommandé pour les tâches très intensives en connaissances**. C’est une limite honnête. Un 1.2B peut être excellent comme routeur, extracteur ou opérateur linguistique ; il ne remplace pas un modèle plus massif pour du raisonnement long ou de la connaissance encyclopédique.

## Le point à surveiller

La vraie question n’est pas seulement “le modèle est-il bon ?”, mais “reste-t-il bon une fois quantifié et intégré dans les runtimes locaux ?”. La version GGUF indique une orientation claire vers llama.cpp, mais il faudra mesurer les variantes de quantization, la latence en contexte long, la robustesse du tool-use et le respect du format sur des prompts japonais réels. Même chose pour MLX : une version 8-bit est utile, mais les performances dépendront de la machine, du batch, du tokenizer et de l’intégration applicative.

Pour un labo local, le test raisonnable est simple : prendre vingt à cinquante tâches japonaises représentatives — support client, extraction de champs, appels d’outils, résumés courts, consignes ambiguës — puis comparer LFM2.5-1.2B-JP-202606 à Qwen3-1.7B, Llama 3.2 1B et éventuellement un 4B plus robuste. Si le petit Liquid tient mieux le japonais et les formats structurés, il mérite sa place dans une pile auto-hébergée. Sinon, il restera un joli checkpoint de plus dans la ménagerie.

## Sources

- Hugging Face — LiquidAI/LFM2.5-1.2B-JP-202606 : https://huggingface.co/LiquidAI/LFM2.5-1.2B-JP-202606
- Hugging Face — LiquidAI/LFM2.5-1.2B-JP-202606-GGUF : https://huggingface.co/LiquidAI/LFM2.5-1.2B-JP-202606-GGUF
- Liquid AI — Introducing LFM2.5: The Next Generation of On-Device AI : https://www.liquid.ai/blog/introducing-lfm2-5-the-next-generation-of-on-device-ai
