---
title: "Gemma 4 QAT : Google réduit le ticket mémoire pour l’IA locale"
description: "Google publie des checkpoints Gemma 4 entraînés pour la quantization : moins de VRAM, un format mobile, et une question centrale pour le local — quelle qualité reste-t-il vraiment ?"
pubDate: 2026-06-06
category: "local"
tags: ["gemma", "quantization", "edge", "llm-local"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Google Blog — Gemma 4 with quantization-aware training"
    url: "https://blog.google/innovation-and-ai/technology/developers-tools/quantization-aware-training-gemma-4/"
  - label: "Google AI for Developers — Gemma 4 model overview"
    url: "https://ai.google.dev/gemma/docs/core"
  - label: "MarkTechPost — Google DeepMind Releases Gemma 4 QAT Checkpoints"
    url: "https://www.marktechpost.com/2026/06/05/google-deepmind-releases-gemma-4-qat-checkpoints-q4_0-and-a-new-mobile-format-cut-on-device-memory/"
---

Google vient d’ajouter une pièce importante à Gemma 4 : des checkpoints optimisés par **Quantization-Aware Training** — QAT pour les intimes, parce que même les acronymes ont besoin d’un acronyme. L’annonce officielle, publiée le **5 juin 2026**, vise explicitement les usages locaux : laptops, appareils edge, mobiles et GPU grand public. Ce n’est pas une nouvelle famille de modèles, mais une nouvelle manière de distribuer Gemma 4 pour qu’il rentre plus facilement dans la mémoire disponible.

Le point clé : Google ne dit pas seulement “voici une quantization après coup”. Le QAT simule la quantification pendant l’entraînement, afin que le modèle apprenne à compenser la perte de précision. En théorie, cela donne une meilleure qualité qu’une **Post-Training Quantization** classique au même format. En pratique, il faut rester prudent : Google affirme une meilleure qualité globale que les baselines PTQ, mais l’annonce ne publie pas de tableau de benchmarks Gemma 4 QAT complet et reproductible. C’est donc une avancée technique sérieuse, pas une permission de jeter vos évaluations internes à la poubelle.

## Ce qui est publié

Google indique avoir appliqué cette recette QAT au format **Q4_0**, un format 4-bit courant dans l’écosystème local. Les checkpoints couvrent la famille Gemma 4, dont les tailles listées dans la documentation développeur : **E2B**, **E4B**, **12B**, **26B A4B** et **31B**. La documentation Google AI for Developers précise aussi que Gemma 4 est distribué en open weights, avec usage commercial permis sous les termes Gemma, et qu’il cible des tâches de question-réponse, résumé, raisonnement, code, multimodalité et agents.

La nouveauté la plus intéressante pour le local n’est pas seulement le Q4_0. Google publie aussi un **format de quantization spécialisé mobile** pour les petits modèles edge, notamment E2B et E4B. D’après l’annonce, ce format réduit l’empreinte mémoire de **Gemma 4 E2B à environ 1 Go**, et la variante **E2B text-only sans Per-Layer Embeddings** peut descendre sous 1 Go. C’est le genre de chiffre qui change la conversation pour les téléphones, les mini-PC, les Raspberry Pi-like musclés et les applications embarquées.

La documentation officielle donne un autre repère utile avec un tableau de mémoire estimée incluant 20 % d’overhead : **Gemma 4 E2B** passe à **2,9 Go en Q4_0**, **1,1 Go en mobile**, et **0,84 Go en mobile text-only** ; **Gemma 4 E4B** est listé à **4,5 Go en Q4_0**, **2,5 Go en mobile**, et **2,2 Go en mobile text-only**. Pour les modèles plus gros, Google liste par exemple **6,7 Go pour Gemma 4 12B en Q4_0**, **14,4 Go pour 26B A4B**, et **17,5 Go pour 31B**. Ces chiffres restent des estimations de chargement, pas une garantie de débit confortable.

## Pourquoi QAT compte plus que “encore une quant”

La quantization classique réduit la précision des poids après entraînement. C’est efficace, mais le modèle n’a pas appris à vivre dans ce régime compressé. Le QAT change le timing : la contrainte de quantization est intégrée pendant l’entraînement, ce qui permet au modèle d’adapter ses représentations. Le résultat attendu n’est pas forcément un fichier plus petit qu’un Q4_0 classique ; c’est plutôt **une meilleure qualité au même budget mémoire**.

C’est un détail souvent mal compris. MarkTechPost le formule proprement : le QAT ne change pas la taille à format identique ; il vise la qualité à cette taille. La réduction supplémentaire vient du format mobile spécialisé, pas d’un sortilège jeté sur Q4_0. Le marketing adore mélanger ces deux niveaux. Ici, il faut les séparer : Q4_0 QAT pour laptop/GPU grand public ; format mobile pour les cas où la mémoire est vraiment le mur.

## Le format mobile : compression sélective, pas hachoir aveugle

Google décrit plusieurs choix techniques pour son format mobile : **activations statiques**, **quantization par canal**, **compression ciblée en 2-bit** sur certaines parties de génération de tokens, et optimisation des embeddings et du KV cache. L’idée est de ne pas compresser tout le modèle de manière uniforme. Les couches critiques pour le raisonnement restent à plus haute précision, tandis que certaines zones moins sensibles sont compressées plus agressivement.

C’est cohérent avec ce que l’on observe côté edge : le problème n’est pas seulement la taille du fichier. Les formats standards peuvent être pénibles pour les accélérateurs mobiles, parce qu’ils imposent des conversions, des accès mémoire ou des calculs peu naturels pour le matériel. Un format mobile utile doit donc viser l’empreinte mémoire **et** le comportement sur les puces réellement utilisées.

Pour une stack IA locale, cela ouvre trois scénarios. D’abord, le modèle assistant léger sur laptop, où E4B ou 12B en Q4_0 peut devenir le choix par défaut. Ensuite, les agents locaux modestes, qui profitent d’une fenêtre de contexte suffisante sans saturer la VRAM. Enfin, les applications mobiles text-only, où un modèle sous le Go devient envisageable sans déléguer tout au cloud.

## Ce qu’il manque encore

La prudence reste nécessaire. L’annonce officielle ne fournit pas de benchmarks indépendants détaillés sur Gemma 4 QAT. On sait que Google revendique une meilleure qualité que PTQ, et la documentation donne des chiffres mémoire. On ne sait pas encore, source indépendante à l’appui, comment ces checkpoints se comportent sur des tâches concrètes : code, RAG local, tool-use, longues conversations, multimodalité, hallucinations en français, ou prompts agentiques avec contraintes strictes.

Autre point : les performances réelles dépendront énormément du runtime. Google mentionne un écosystème large — Hugging Face, llama.cpp, Ollama, LM Studio, vLLM, MLX, LiteRT-LM, Transformers.js — mais “supporté” ne veut pas dire “optimal”. Un même modèle peut être agréable dans llama.cpp sur Metal, décevant dans un backend mal réglé, et excellent dans vLLM avec speculative decoding si le draft model est correctement exploité.

## Verdict local

Gemma 4 QAT est une sortie importante parce qu’elle attaque un problème très concret : la mémoire. Pas le score leaderboard du mois, pas la promesse vague d’un assistant magique, mais le fait brutal qu’un modèle utile doit rentrer dans la machine. Pour les utilisateurs locaux, les chiffres E2B/E4B/mobile sont les plus intéressants. Pour les machines plus costaudes, le Q4_0 QAT sur 12B, 26B A4B ou 31B mérite d’être testé contre les quants communautaires habituels.

Le conseil simple : ne remplacez pas votre modèle local préféré sur annonce. Téléchargez, testez vos prompts réels, mesurez la latence, la mémoire et les erreurs. Mais cette fois, ça vaut clairement le test. Une quantization pensée pendant l’entraînement, c’est moins glamour qu’un nouveau nom de modèle. C’est aussi souvent plus utile.

## Sources

- Google Blog — “Gemma 4 with quantization-aware training” : https://blog.google/innovation-and-ai/technology/developers-tools/quantization-aware-training-gemma-4/
- Google AI for Developers — “Gemma 4 model overview” : https://ai.google.dev/gemma/docs/core
- MarkTechPost — “Google DeepMind Releases Gemma 4 QAT Checkpoints” : https://www.marktechpost.com/2026/06/05/google-deepmind-releases-gemma-4-qat-checkpoints-q4_0-and-a-new-mobile-format-cut-on-device-memory/
