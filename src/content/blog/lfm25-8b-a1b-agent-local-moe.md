---
title: "LFM2.5-8B-A1B : Liquid AI compacte l’agent local dans 1,5 milliard de paramètres actifs"
description: "Liquid AI publie un MoE open-weight pensé pour les assistants locaux : 8,3B paramètres au total, 1,5B actifs, contexte 128K et gros progrès annoncés sur le tool calling."
pubDate: 2026-06-03
category: "veille"
tags: ["open-weight", "local-ai", "moe", "agents", "liquid-ai"]
author: "Veille IA"
draft: false
sources:
  - label: "Liquid AI — LFM2.5-8B-A1B release blog"
    url: "https://www.liquid.ai/blog/lfm2-5-8b-a1b"
  - label: "MarkTechPost — Liquid AI releases LFM2.5-8B-A1B"
    url: "https://www.marktechpost.com/2026/05/28/liquid-ai-releases-lfm2-5-8b-a1b-an-on-device-moe-model-with-8-3b-total-and-1-5b-active-parameters/"
  - label: "Hugging Face — LiquidAI/LFM2.5-8B-A1B"
    url: "https://huggingface.co/LiquidAI/LFM2.5-8B-A1B"
---

Liquid AI a publié **LFM2.5-8B-A1B**, un modèle **Mixture-of-Experts** conçu pour tourner localement tout en conservant des capacités de tool calling et d’instruction following crédibles. Le chiffre à retenir n’est pas seulement “8,3 milliards de paramètres”, mais surtout **1,5 milliard de paramètres actifs par token**. C’est ce ratio qui permet à Liquid de viser les laptops, CPU modernes, GPU grand public et même téléphones, sans transformer chaque requête en barbecue de silicium.

La promesse est claire : faire avancer l’agent local. Pas le petit assistant qui résume une note en tremblant, mais un modèle capable d’enchaîner des appels outils, de suivre des instructions complexes, de manipuler un contexte long et de rester interactif. Liquid parle d’un assistant personnel on-device. Le terme est ambitieux, mais l’approche technique mérite attention : sparsité MoE, contexte **128K**, vocabulaire élargi, reinforcement learning à grande échelle et modèle “reasoning-only”.

## Une architecture sparse pensée pour le coût par token

LFM2.5-8B-A1B succède à LFM2-8B-A1B, publié en octobre 2025. Selon Liquid AI, le nouveau modèle conserve la famille architecturale : **Mixture-of-Experts**, **Grouped Query Attention** et blocs de convolution courte gated. MarkTechPost détaille une architecture de 24 couches, avec 18 blocs convolutionnels double-gated et 6 couches GQA.

Le modèle contient **8,3B paramètres** au total mais n’en active qu’environ **1,5B** à chaque token. C’est le cœur du compromis. Un modèle dense de 8B active tout son poids à chaque passe ; un MoE sparse peut stocker plus de capacité totale tout en réduisant le compute effectif. En théorie, cela permet d’obtenir une meilleure spécialisation sans payer le prix complet à l’inférence.

En pratique, les MoE ont leurs propres coûts : routage, mémoire, kernels, efficacité hardware, batch size. Un MoE mal implémenté peut être joli sur le papier et pénible en production. Liquid insiste donc sur le support d’inférence dès le jour un : **llama.cpp**, **MLX**, **vLLM** et **SGLang**. C’est un bon signal. Pour un modèle local, l’écosystème de runtime est presque aussi important que les poids. Un checkpoint inutilisable sur les machines réelles, c’est une sculpture, pas un outil.

## 128K de contexte et 38T tokens de préentraînement

Liquid annonce plusieurs changements majeurs par rapport à LFM2-8B-A1B. La fenêtre de contexte passe de **32 768 tokens** à environ **128K tokens**. Le préentraînement passe de **12T** à **38T tokens**. Le vocabulaire double de **65 536** à **128 000 tokens**. Ces trois mouvements vont dans le même sens : rendre le modèle plus robuste pour des workflows longs, multilingues et orientés outils.

Le contexte 128K est particulièrement pertinent pour un assistant local. Un agent de bureau doit pouvoir charger des documents, tickets, fichiers de configuration, historiques de commandes ou extraits de dépôt. Mais attention : “accepter 128K tokens” ne signifie pas “raisonner parfaitement sur 128K tokens”. La capacité utile dépend de la récupération interne, de la position de l’information, des distracteurs et du comportement du modèle dans les longues chaînes d’outils.

L’élargissement du vocabulaire est plus discret, mais important. Liquid indique avoir amélioré l’efficacité de tokenisation pour les écritures non latines, avec des gains particulièrement forts en hindi, thaï, vietnamien, indonésien et arabe. Le blog officiel mentionne aussi un gain plus modeste mais réel pour le français. Moins de tokens pour exprimer la même information, c’est moins de coût, moins de latence et plus de place utile dans le contexte. Ce n’est pas glamour ; c’est précisément pour ça que c’est sérieux.

## Un modèle “reasoning-only”, choix utile ou pari risqué ?

Liquid décrit LFM2.5-8B-A1B comme un modèle **reasoning-only**, produisant une chaîne de raisonnement explicite avant sa réponse finale. L’argument est que, dans un MoE avec peu de paramètres actifs, les tokens de raisonnement coûtent relativement moins cher. On peut donc dépenser davantage de tokens intermédiaires pour améliorer la qualité, sans exploser le budget comme sur un dense plus lourd.

Cette idée est plausible, surtout pour les tâches agentiques : planifier un appel outil, vérifier une contrainte, reformuler une instruction, comparer des sorties. Mais elle soulève aussi deux questions. Premièrement, l’exposition du raisonnement doit être contrôlée en production : logs, sécurité, informations sensibles, conformité. Deuxièmement, plus de raisonnement ne veut pas dire meilleur raisonnement. Un modèle peut produire une très belle trace intermédiaire et se tromper avec beaucoup d’assurance. La calligraphie de l’erreur reste une erreur.

Pour les développeurs, le bon test sera simple : est-ce que ce raisonnement améliore les résultats dans des boucles réelles ? Par exemple : créer un fichier, appeler une API locale, corriger une commande, maintenir un état utilisateur, refuser une action dangereuse. Les benchmarks donnent un signal, mais les agents locaux gagnent ou perdent dans les coins rugueux du système d’exploitation.

## Benchmarks : les progrès annoncés sont forts

Le blog Liquid publie des gains importants par rapport à LFM2-8B-A1B. Parmi les chiffres notables : **IFEval** passe de 79,44 à **91,84**, **MATH500** de 74,80 à **88,76**, **BFCLv3** de 45,07 à **64,36**, **BFCLv4** de 25,52 à **48,50**. Sur **Tau² Telecom**, Liquid annonce un bond spectaculaire de 13,60 à **88,07**. Le taux de non-hallucination sur AA-Omniscience passerait de 7,46 à **63,47**.

Ces chiffres suggèrent un vrai travail de post-training et de RL sur l’instruction following, la fiabilité et le tool calling. Ils doivent néanmoins être traités comme des chiffres fournisseur jusqu’à confirmation indépendante. Ce n’est pas une critique particulière de Liquid ; c’est l’hygiène minimale en 2026. Les benchmarks agentiques sont sensibles au prompt, au harnais, aux versions d’outils, au parsing et à la définition exacte du succès.

MarkTechPost reprend les caractéristiques clés et souligne que le modèle est open-weight, avec base et post-trained checkpoints disponibles. C’est important : la valeur d’un petit MoE local dépend de la capacité de la communauté à le tester, le quantifier, le profiler et le casser méthodiquement. Les meilleurs reviewers open-source sont impitoyables. C’est leur charme, et accessoirement leur utilité.

## Pourquoi ce modèle compte pour l’IA locale

Les modèles frontier fermés gagnent encore largement sur les tâches les plus difficiles. Mais beaucoup d’usages d’assistant personnel ne demandent pas un modèle à plusieurs centaines de milliards de paramètres. Ils demandent un modèle rapide, privé, peu coûteux, capable d’utiliser des outils locaux et suffisamment fiable pour ne pas inventer une commande destructive.

LFM2.5-8B-A1B cible exactement cet espace. Si les performances annoncées tiennent en quantification et sur machines grand public, il peut devenir une brique intéressante pour des agents locaux : tri de fichiers, automatisation personnelle, RAG privé, contrôle d’applications, assistant de développement léger, workflows hors ligne ou semi-connectés.

Le modèle pose aussi une question plus large : l’agent local a-t-il besoin d’un modèle généraliste énorme, ou d’un modèle compact très bien entraîné pour l’orchestration ? Liquid parie sur la seconde option. Ce n’est pas suffisant pour remplacer Claude, GPT ou Gemini dans tous les usages, mais c’est potentiellement suffisant pour beaucoup de tâches fréquentes. Et dans l’IA locale, “suffisamment bon, instantané et privé” est souvent plus utile que “brillant, distant et cher”.

## Ce qu’il faut surveiller

Les prochains tests devront vérifier trois points. D’abord, la **vitesse réelle** sur laptops courants, pas seulement sur machines de démonstration. Ensuite, la **qualité en quantification**, car beaucoup d’utilisateurs locaux ne feront pas tourner le modèle en pleine précision. Enfin, la **robustesse du tool calling** dans des agents réels : JSON strict, erreurs d’outil, état persistant, permissions, refus de commandes dangereuses.

LFM2.5-8B-A1B n’est pas un modèle frontier généraliste. Ce n’est pas son sujet. Son intérêt est de montrer qu’un MoE compact, open-weight et orienté outils peut rendre l’assistant local moins théorique. Si la communauté confirme les chiffres, Liquid aura livré une pièce sérieuse pour l’agent on-device. Petite, sparse, et potentiellement très agaçante pour les modèles plus lourds. Le meilleur genre de petite machine.

## Sources

- Liquid AI — LFM2.5-8B-A1B release blog : https://www.liquid.ai/blog/lfm2-5-8b-a1b
- MarkTechPost — Liquid AI releases LFM2.5-8B-A1B : https://www.marktechpost.com/2026/05/28/liquid-ai-releases-lfm2-5-8b-a1b-an-on-device-moe-model-with-8-3b-total-and-1-5b-active-parameters/
- Hugging Face — LiquidAI/LFM2.5-8B-A1B : https://huggingface.co/LiquidAI/LFM2.5-8B-A1B
