---
title: "thaw-vllm : le fork() des agents IA s’attaque au vrai coût du branching"
description: "thaw propose de cloner une session vLLM vivante — poids, KV cache, scheduler et prefix-hash — pour lancer des branches d’agents sans refaire le prefill. Prometteur, mais encore à valider hors benchmarks projet."
pubDate: 2026-05-31
tags: ["vLLM", "agents locaux", "KV cache", "inférence", "self-hosting"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub — thaw-ai/thaw"
    url: "https://github.com/thaw-ai/thaw"
  - label: "thaw.sh — fork() for AI agents"
    url: "https://thaw.sh/"
  - label: "GitHub — vLLM"
    url: "https://github.com/vllm-project/vllm"
  - label: "llm-d — KV-Cache Wins You Can See"
    url: "https://llm-d.ai/blog/kvcache-wins-you-can-see"
  - label: "LMCache — An Efficient KV Cache Layer for Enterprise-Scale LLM Inference"
    url: "https://lmcache.ai/tech_report.pdf"
---

Les agents IA ont un problème très concret : dès qu’ils explorent plusieurs pistes à partir d’un même contexte, ils paient souvent plusieurs fois le même coût de **prefill**. Même prompt système, mêmes outils, même historique, même tronc de raisonnement — puis quatre, huit ou seize branches qui repartent chacune comme si rien n’avait jamais été calculé. C’est élégant comme une photocopieuse qui réimprime tout le livre pour corriger une virgule.

Le projet **thaw**, distribué sous forme de paquet `thaw-vllm`, propose une primitive plus radicale : faire un **`fork()` d’une session LLM vivante**. L’idée est de capturer l’état d’un moteur d’inférence — poids, **KV cache**, état du scheduler et table de prefix-hash — puis d’hydrater plusieurs sessions filles qui reprennent au même point et divergent ensuite. Le projet se présente comme “`fork()` for AI agents” ou “`git branch` for live AI agents”. C’est une formule marketing, certes, mais elle décrit assez bien le mécanisme.

## Le coût caché des agents : le préfixe répété

Dans un transformer, la phase de prefill calcule les représentations K/V du prompt d’entrée. Sur des prompts courts, ce coût reste discret. Sur des agents, il devient vite dominant : system prompt, schémas d’outils, consignes, historique d’actions, observations, documents injectés par RAG, contraintes de sortie. Beaucoup de tokens sont identiques d’une branche à l’autre.

Ce n’est pas une intuition isolée. Le billet technique de **llm-d** sur le KV cache rappelle que les workloads agentiques sont très préfixe-lourds, avec parfois des ratios input/output supérieurs à **100:1**. Le même article montre qu’un routage conscient du prefix-cache peut réduire fortement le TTFT en production distribuée : leurs benchmarks annoncent un P90 TTFT **57× plus rapide** que du scheduling approximatif, et **170×** plus rapide que du random scheduling. Ce ne sont pas des chiffres thaw, mais ils vérifient le point de fond : le KV cache est désormais une ressource d’infrastructure, pas un détail d’implémentation.

Le rapport **LMCache** va dans le même sens. Il décrit le KV cache comme une couche de stockage et de communication entre moteurs d’inférence, avec des gains annoncés jusqu’à **15×** en throughput avec vLLM et au moins **2×** de latence en moins dans plusieurs scénarios. Là encore, le message est clair : éviter de recalculer le contexte partagé est une des grandes batailles de l’inférence moderne.

## Ce que thaw ajoute par-dessus vLLM

vLLM sait déjà faire beaucoup : PagedAttention, continuous batching, chunked prefill, prefix caching, speculative decoding, API OpenAI-compatible, quantization, multi-LoRA, tensor/pipeline/data/expert/context parallelism. Le dépôt vLLM se présente comme un moteur d’inférence rapide et efficace, et sa liste de fonctionnalités montre qu’il est devenu une plateforme complète de serving.

thaw ne remplace pas vLLM. Il se greffe dessus comme primitive de snapshot/fork. Selon le dépôt GitHub, le mécanisme capture quatre éléments : les **poids du modèle**, les blocs de **KV cache**, la table **prefix-hash**, et l’état du **scheduler**. La restauration initialise ensuite un moteur enfant, réinjecte ces états, reconstruit la correspondance prefix-cache, et permet aux requêtes compatibles avec ce préfixe de sauter le prefill.

Le projet vise explicitement les cas où l’on a un tronc commun puis plusieurs suites : rollouts RL, tree search, best-of-N, multi-agent reasoning, agents de code parallèles, tool-use branching, revue automatique en branches. Pour un serveur de chat classique — une requête, une réponse, peu de branches — thaw n’apporte probablement pas grand-chose. Le README le dit d’ailleurs assez franchement : pour du single-prompt serving, vLLM ou SGLang suffisent.

## Les chiffres publiés par thaw

Les benchmarks disponibles viennent principalement du projet lui-même. Il faut donc les lire comme des “receipts” utiles, pas comme une validation indépendante.

Le chiffre le plus parlant concerne **ForkPool**, annoncé en avril 2026. Sur **H100 80 GB PCIe** avec **Llama-3.1-8B**, thaw mesure un workload de **5 rounds × 4 branches × 64 tokens**. Le pool préchauffé démarre une fois les workers avec les vrais poids, puis chaque appel `fork_completions()` snapshot seulement le KV. Résultat publié : **22,3 s** d’initialisation une fois, **1,16 s** pour le premier round, puis **0,88 s** de médiane par round. Le projet parle d’un gain amorti d’environ **400×** face à un cold boot répété.

Autre mesure : le sleep/wake avec vLLM. Pour **Llama-3.1-8B** sur H100 SXM, thaw rapporte **3,4 s** de sleep, **11,1 s** de wake, un snapshot de **16 Go**, et une sortie greedy bit-identical après restauration. Pour **Llama-3.1-70B** en TP=2 sur deux H100 SXM, le dépôt mentionne **16,1 s** de sleep, **53,6 s** de wake, et un snapshot de **141 Go**. C’est impressionnant, mais cela reste une mesure très dépendante du stockage, de l’interconnexion, du modèle, du niveau de parallélisme et de la configuration vLLM.

Le site thaw.sh met aussi en avant un hot-swap “slot-warm” : environ **0,29 s** pour recharger entre moteurs 8B après pinning initial, avec **55 Go/s** de transfert DMA et environ **86 %** du plafond PCIe Gen5 revendiqué. La release `v0.5.1` indique une restauration CRC32C parallélisée **2,89×** plus rapide. Tout cela donne une direction technique crédible, mais pas encore une vérité universelle.

## Pourquoi c’est intéressant pour l’auto-hébergement

À première vue, thaw sent le datacenter : H100, snapshots de dizaines ou centaines de Go, vLLM, DMA, buffers pinned. Pas exactement le Raspberry Pi sous l’étagère. Pourtant, le sujet concerne aussi l’IA locale avancée.

D’abord parce que les agents locaux deviennent vite préfixe-lourds. Même sur une workstation, un agent de code qui explore quatre patches, un assistant RAG qui compare plusieurs hypothèses, ou un workflow de revue qui lance plusieurs critiques partagent souvent 80 à 95 % de contexte commun. Si on peut éviter de refaire le prefill, on gagne en latence, en énergie et en capacité de concurrence.

Ensuite parce que la logique de thaw anticipe une évolution plus large : l’inférence locale ne sera pas seulement “un modèle dans un terminal”. Elle va ressembler à une petite infrastructure : cache, routing, outils, workers, snapshots, reprise d’état, orchestration. Ce n’est pas glamour, mais c’est là que se cachent les gains réels. Le modèle compte ; la tuyauterie aussi. Et parfois, la tuyauterie gagne la course pendant que le modèle ajuste sa cravate.

## Les limites à garder en tête

Première limite : thaw est jeune. Le dépôt public affiche peu d’étoiles au moment de la capture, une douzaine de releases et une base de code encore très spécialisée. Ce n’est pas une brique à mettre demain dans une production critique sans tests lourds.

Deuxième limite : les benchmarks principaux sont fournis par le projet. Les “receipts” JSON et scripts reproductibles sont une bonne pratique, mais il manque encore des retours indépendants sur des stacks variées : modèles Qwen récents, contextes longs, quantizations, multi-GPU grand public, SSD plus ordinaires, workloads d’agents réels.

Troisième limite : le snapshot d’état d’un moteur LLM n’est pas neutre côté sécurité et exploitation. On manipule potentiellement de la mémoire contenant du contexte utilisateur, des documents, des sorties intermédiaires et parfois des secrets injectés par erreur. En self-hosting, il faudra penser chiffrement au repos, durée de vie des snapshots, isolation des workers, nettoyage explicite, et permissions de fichiers. Un cache rapide qui fuit vite reste une fuite.

## Verdict

thaw-vllm n’est pas un nouveau runtime local grand public. C’est une primitive bas niveau pour un problème qui devient central : **brancher des agents sans recalculer le même préfixe en boucle**. Pour la plupart des utilisateurs, vLLM, llama.cpp ou Ollama resteront les outils directs. Pour ceux qui construisent des agents parallèles, du best-of-N, des rollouts RL ou des workflows de code multi-branches, thaw mérite une veille attentive.

Le signal technique est solide : le KV cache devient une unité de travail, de stockage et de scheduling. thaw pousse cette logique jusqu’au fork de session. Si les mesures se confirment hors environnement contrôlé, on pourrait voir émerger une nouvelle couche d’infrastructure pour agents auto-hébergés : non pas seulement “servir un modèle”, mais **gérer des états d’inférence vivants**. C’est moins spectaculaire qu’un nouveau 70B. C’est peut-être plus important.
