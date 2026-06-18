---
title: "llama.cpp ajoute le frame merge Qwen-VL : la vidéo locale sort du bricolage pur"
description: "La release b9543 de llama.cpp ajoute le support du frame merge pour les modèles Qwen-VL. Ce n’est pas encore un VLM vidéo universel, mais c’est un pas concret vers l’analyse vidéo locale."
pubDate: 2026-06-07
category: "local"
tags: ["llama.cpp", "qwen-vl", "multimodal", "video", "inference-locale"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Release llama.cpp b9543 — frame merge Qwen-VL"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9543"
  - label: "Qwen3-VL — dépôt officiel QwenLM"
    url: "https://github.com/QwenLM/Qwen3-VL"
  - label: "Qwen3-VL-8B-Instruct — fiche Hugging Face"
    url: "https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct"
  - label: "Discussion llama.cpp — vidéo Qwen3.5 expérimentale"
    url: "https://github.com/ggml-org/llama.cpp/discussions/20965"
---

La vidéo locale a longtemps été le parent pauvre du multimodal open-weight. On pouvait faire tourner un VLM pour décrire une image, parfois envoyer quelques frames à la main, puis appeler ça “analyse vidéo” avec l’optimisme coupable d’un benchmark du vendredi soir. La release **b9543** de `llama.cpp`, publiée le **6 juin 2026**, ajoute un changement plus concret : `mtmd: support "frame merge" for qwen-vl-based models (#21858)`.

La note de release indique explicitement : **“feat: add video support for Qwen3.5”**. Traduction sobre : `llama.cpp` commence à prendre en charge la logique de fusion temporelle nécessaire aux modèles Qwen-VL récents, au lieu de traiter la vidéo comme une simple pile d’images indépendantes.

Ce n’est pas encore “toute la vidéo locale est résolue”. Mais c’est le bon type de progrès : bas niveau, intégré au runtime, utile pour les machines locales.

## Le problème : une vidéo n’est pas juste une liste d’images

Un modèle vision-language peut décrire une image parce qu’il reçoit des patchs visuels, les encode, puis les injecte dans le contexte du modèle texte. Pour la vidéo, faire ça naïvement frame par frame casse vite trois choses : le budget de tokens, la cohérence temporelle et la compréhension du mouvement.

Les modèles Qwen-VL récents sont justement conçus pour aller au-delà de l’image fixe. Le dépôt officiel Qwen3-VL présente la famille comme orientée vision, raisonnement, OCR, compréhension vidéo, perception spatiale et interaction agentique. Il mentionne notamment un contexte natif de **256K tokens**, extensible jusqu’à **1M**, ainsi que la capacité de traiter des vidéos longues avec indexation temporelle. La fiche Hugging Face de `Qwen/Qwen3-VL-8B-Instruct` cite aussi des améliorations comme **Interleaved-MRoPE**, **Text–Timestamp Alignment** et une meilleure modélisation temporelle vidéo.

Autrement dit, côté modèle, la capacité existe. Côté runtime local, il faut encore que l’infrastructure sache préparer et alimenter correctement ces entrées vidéo. C’est là que `llama.cpp` devient intéressant.

## Ce que signifie “frame merge”

La release b9543 ne publie pas un long billet pédagogique, mais le libellé est assez clair : support du **frame merge** pour les modèles basés sur Qwen-VL. Dans les discussions précédentes autour de `llama.cpp`, la logique expérimentale consistait à regrouper des frames consécutives en “super-frames” temporelles, afin de respecter la manière dont Qwen-VL encode le temps et les patchs visuels.

Une discussion GitHub antérieure, autour d’un projet expérimental de captioning vidéo Qwen3.5 via `llama-server`, décrivait une approche proche : associer des frames consécutives, utiliser une forme de Conv3D et calculer des positions temporelles M-RoPE. L’auteur insistait alors sur le caractère expérimental du patch, non générique, limité à la famille Qwen3.5.

La nouveauté de b9543 est que cette direction entre dans la release officielle `llama.cpp` via `mtmd`, le pipeline multimodal du projet. On passe donc d’un patch exploratoire à une fonctionnalité intégrée — avec toutes les réserves habituelles sur une première implémentation.

## Pourquoi c’est important pour l’IA locale

`llama.cpp` reste l’un des runtimes les plus importants pour faire tourner des modèles localement : CPU, Apple Silicon, CUDA, ROCm, Vulkan, Windows, Linux, macOS. La release b9543 fournit d’ailleurs des binaires précompilés pour plusieurs plateformes, dont macOS Apple Silicon, Linux, Android et Windows CUDA/Vulkan.

Ajouter la vidéo dans ce type de runtime change le périmètre des usages locaux :

- résumé de vidéos courtes sans envoyer les frames dans le cloud ;
- analyse de captures d’écran ou de sessions desktop ;
- inspection de vidéos industrielles ou domotiques en local ;
- agents multimodaux capables de raisonner sur une séquence d’actions, pas seulement sur un screenshot ;
- prototypage robotique ou “physical AI” sur matériel contrôlé.

Évidemment, tout dépendra du modèle, de la taille des frames, du nombre d’images échantillonnées et du contexte disponible. Une vidéo longue peut exploser le budget de tokens très vite. Mais la différence entre “je bricole un script Python qui extrait 12 images” et “le runtime comprend la fusion de frames attendue par Qwen-VL” est réelle.

## Qwen3-VL donne le contexte technique

Qwen3-VL est présenté par QwenLM comme une famille multimodale capable de gérer image, vidéo, OCR, spatial reasoning, GUI control et tâches agentiques. Le dépôt officiel mentionne des modèles denses et MoE, des variantes Instruct et Thinking, et une échelle allant de l’edge au cloud.

La fiche Hugging Face du modèle 8B Instruct précise que Qwen3-VL améliore la perception visuelle, le raisonnement, le traitement long contexte, la compréhension spatiale et vidéo, ainsi que les capacités d’agent visuel. Elle indique aussi que les exemples Transformers recommandent FlashAttention 2 pour les scénarios multi-image et vidéo, signe que la vidéo n’est pas un simple accessoire : c’est un cas mémoire et performance sérieux.

Pour l’utilisateur local, la question devient donc : peut-on exploiter cette architecture sans devoir rester dans l’écosystème Python complet ? `llama.cpp` répond progressivement oui, ou au moins “on y arrive, range cette usine à gaz, elle fuit”.

## Ce qu’il ne faut pas sur-vendre

Première limite : ce support vise les modèles **Qwen-VL-based**. Ce n’est pas un support vidéo universel pour tous les VLM open-weight. L’écosystème multimodal reste fragmenté : LLaVA, Qwen-VL, Gemma multimodal, Cosmos, InternVL et autres familles n’ont pas forcément les mêmes encodeurs, formats d’entrée ou conventions temporelles.

Deuxième limite : la qualité finale dépendra fortement du sampling vidéo. Combien de frames ? À quelle résolution ? Avec quel stride temporel ? Sur une vidéo d’une minute, une mauvaise stratégie d’échantillonnage peut rater l’événement important, même si le modèle et le runtime sont bons.

Troisième limite : le coût mémoire ne disparaît pas. Les modèles vidéo exploitent davantage de tokens visuels et de contexte. Sur Apple Silicon ou GPU consumer, il faudra probablement choisir entre résolution, durée, taille du modèle et vitesse. La physique garde son droit de veto, quelle mesquinerie.

## Ce que je testerais en premier

Pour valider l’intérêt réel, je regarderais trois scénarios simples :

1. **Captioning vidéo court** : 10 à 30 secondes, scènes simples, vérifier si le modèle décrit le mouvement plutôt que seulement les objets.
2. **Événement temporel** : demander “à quel moment X se produit-il ?” pour tester la localisation temporelle.
3. **Agent desktop** : enregistrer une courte séquence d’interface et demander au modèle de reconstruire les actions utilisateur.

Il faudra comparer avec une baseline bête : extraire N images et les envoyer comme images séparées. Si le frame merge apporte une meilleure compréhension temporelle à coût raisonnable, alors l’intégration a une vraie valeur.

## Verdict provisoire

La release b9543 de `llama.cpp` n’est pas une révolution marketing. C’est mieux : une petite pièce d’infrastructure qui manquait. Le support du frame merge Qwen-VL rapproche l’analyse vidéo open-weight d’un usage local réaliste, surtout pour les machines qui s’appuient déjà sur `llama.cpp` plutôt que sur un serveur Python lourd.

À court terme, c’est à tester avec prudence. À moyen terme, c’est un signal clair : les runtimes locaux ne se contentent plus du texte et de l’image. Ils commencent à absorber la vidéo, et donc les agents locaux vont pouvoir regarder ce qui se passe dans le temps. Ce qui est pratique. Et légèrement inquiétant si ton bureau est aussi chaotique que le mien.

## Sources

- [Release llama.cpp b9543 — frame merge Qwen-VL](https://github.com/ggml-org/llama.cpp/releases/tag/b9543)
- [Qwen3-VL — dépôt officiel QwenLM](https://github.com/QwenLM/Qwen3-VL)
- [Qwen3-VL-8B-Instruct — fiche Hugging Face](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct)
- [Discussion llama.cpp — vidéo Qwen3.5 expérimentale](https://github.com/ggml-org/llama.cpp/discussions/20965)
