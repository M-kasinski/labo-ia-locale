---
title: "Step 3.7 Flash : un VLM MoE open-weight taillé pour l’inférence locale musclée"
description: "StepFun publie un modèle vision-langage MoE sous Apache 2.0, avec GGUF, llama.cpp, vLLM et 256K tokens de contexte. Intéressant, mais pas pour toutes les machines."
pubDate: 2026-06-01
tags: ["open-weight", "vlm", "gguf", "llama.cpp", "vllm"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Model card Hugging Face — stepfun-ai/Step-3.7-Flash"
    url: "https://huggingface.co/stepfun-ai/Step-3.7-Flash"
  - label: "Dépôt GitHub — stepfun-ai/Step-3.7-Flash"
    url: "https://github.com/stepfun-ai/Step-3.7-Flash"
  - label: "Quantizations GGUF — stepfun-ai/Step-3.7-Flash-GGUF"
    url: "https://huggingface.co/stepfun-ai/Step-3.7-Flash-GGUF"
---

StepFun a publié **Step 3.7 Flash**, un modèle vision-langage open-weight qui mérite l’attention des gens qui font tourner de l’IA chez eux — à condition d’avoir une machine sérieuse. Ce n’est pas le petit modèle qui va se glisser discrètement sur un laptop 16 Go. C’est plutôt une brique MoE multimodale pour postes de travail, serveurs locaux et machines à mémoire unifiée généreuse.

Le point intéressant : StepFun ne se contente pas de mettre un checkpoint brut sur Hugging Face. Le modèle arrive avec des variantes **BF16**, **FP8**, **NVFP4** et surtout des **quantizations GGUF**, ainsi que des chemins d’exécution via **vLLM**, **SGLang**, **Transformers** et **llama.cpp**. Pour l’écosystème local, c’est souvent la différence entre “joli papier” et “quelqu’un va vraiment l’essayer ce week-end”.

## Un gros MoE, mais seulement 11B actifs par token

D’après la model card Hugging Face et le dépôt GitHub officiel, Step 3.7 Flash est un **Sparse Mixture-of-Experts vision-language model**. StepFun annonce environ **198B paramètres** au total, composés d’un backbone langage de **196B paramètres** et d’un encodeur vision de **1,8B paramètres**. Hugging Face affiche aussi une taille autour de **201B paramètres**, ce qui ressemble à une différence de comptage plutôt qu’à un changement de nature.

Le chiffre qui compte vraiment pour l’inférence est ailleurs : le modèle active environ **11B paramètres par token**. C’est l’intérêt classique du MoE : garder une capacité totale élevée sans payer tout le modèle à chaque token. En local, cela ne supprime pas le problème mémoire — les poids doivent toujours tenir quelque part — mais cela peut rendre le débit de génération moins absurde qu’un dense 200B.

StepFun annonce aussi une fenêtre de contexte de **256K tokens** et trois niveaux de raisonnement : **low**, **medium** et **high**. C’est utile pour router les tâches : réponse rapide quand le problème est simple, mode plus délibéré quand il faut chaîner perception, recherche, code ou tool-use. Comme toujours avec les grands contextes, il ne faut pas confondre “peut charger 256K” et “raisonne parfaitement sur 256K”. Le premier est une capacité technique ; le second doit se vérifier sur tes propres documents.

## La partie locale : GGUF, llama.cpp et 128 Go de mémoire

La page **Step-3.7-Flash-GGUF** est probablement la plus importante pour notre lectorat. Elle liste des fichiers allant du **BF16 à 394 Go** jusqu’à des quantizations plus agressives : **Q8_0 à 209 Go**, **Q4_K_S à 112 Go**, **IQ4_XS à 105 Go**, **Q3_K_M à 94 Go** et **IQ3_XXS à 76 Go**. Le projecteur vision `mmproj-Step-3.7-flash-f16.gguf` ajoute environ **4 Go** pour l’usage multimodal.

StepFun indique qu’avec **128 Go de mémoire unifiée**, des machines comme un **Mac Studio**, un système **DGX Spark** ou une machine **Ryzen AI Max+ 395** peuvent héberger les quantizations Q4 et inférieures avec le contexte complet. C’est crédible en ordre de grandeur, mais cela place clairement Step 3.7 Flash dans la catégorie “station locale haut de gamme”. Sur un MacBook 32 Go ou une carte 24 Go, ce n’est pas le bon cheval. À moins d’aimer regarder swapper une machine comme un grille-pain anxieux.

Le quickstart GGUF passe par un fork/une branche StepFun de **llama.cpp**, avec `llama-batched-bench`, `llama-cli`, `llama-mtmd-cli` pour vision + texte, et `llama-server` pour exposer une API compatible OpenAI. C’est un bon signal : le modèle n’est pas uniquement pensé pour une API cloud propriétaire.

## Benchmarks : bons signaux, prudence habituelle

StepFun met en avant plusieurs résultats. Sur la partie perception et vérification visuelle, la model card annonce **79,2 sur SimpleVQA Search** et **95,3 sur V\* Python**. Sur les workflows agentiques, le dépôt indique **67,1 sur ClawEval-1.1**, avec le concurrent suivant à **59,8**, ainsi que **49,5 sur Toolathlon** et **48,1 sur HLE w. Tool**. Côté code, StepFun revendique **56,3 sur SWE-Bench PRO**, présenté comme une deuxième place, puis **59,5 sur Terminal-Bench 2.1** et **45,8 sur GDPVal-AA**.

Ces chiffres sont intéressants, mais ils viennent principalement des supports officiels de StepFun. Ils doivent donc être lus comme des claims de lancement, pas comme une vérité opérationnelle universelle. Le vrai test pour un déploiement local sera plus banal : est-ce que le modèle tient en mémoire, répond vite, respecte les formats JSON, manipule bien les images, et ne se perd pas dans un agent qui appelle des outils pendant dix tours ? Les benchmarks donnent une direction ; ils ne remplacent pas une recette de prod.

Le dépôt officiel ajoute aussi une variante **NVFP4 avec MTP** pour du décodage spéculatif dans vLLM. Sur un benchmark décrit par StepFun avec matériel **GB200**, **TP=4** et prompts de raisonnement courts mais sorties longues, la variante NVFP4 + MTP atteint **8229 tok/s** à concurrence 64 contre **5667 tok/s** sans MTP, soit **1,45×**. Très bien pour un serveur haut de gamme ; pas exactement le genre de chiffre que tu vas reproduire sur ton Mac mini.

## Pourquoi c’est important pour l’IA locale

Step 3.7 Flash illustre une tendance nette : les modèles open-weight haut de gamme arrivent désormais avec des formats de déploiement concrets. Avant, beaucoup de gros modèles “ouverts” étaient techniquement disponibles mais pratiquement inutilisables hors clusters. Ici, StepFun pousse les chemins **GGUF**, **vLLM**, **SGLang**, **Transformers**, **NVIDIA NeMo** et **llama.cpp** dès le départ.

C’est important pour l’auto-hébergement. Un VLM MoE avec long contexte peut devenir utile pour :

- analyser des documents longs avec graphiques ;
- extraire du code depuis captures ou maquettes UI ;
- faire du RAG multimodal privé ;
- piloter des agents locaux qui ont besoin de vision, tool-use et contexte long ;
- servir une équipe en réseau local sans envoyer les documents à une API externe.

Mais il faut rester lucide : Step 3.7 Flash n’est pas un modèle “local démocratique”. C’est un modèle local **possible** sur matériel haut de gamme. Pour beaucoup d’usages personnels, un VLM plus petit sera plus rationnel. La bonne question n’est pas “peut-on le lancer ?”, mais “est-ce que sa qualité compense le coût mémoire et la complexité d’exploitation ?”.

## À tester avant d’adopter

Si tu veux l’évaluer proprement, je commencerais par quatre tests simples :

1. **Chargement et mémoire réelle** en Q4 ou IQ4 sur ta machine, avec et sans projecteur vision.
2. **Long contexte utile** : retrouver une information précise dans un gros document, pas seulement ingérer 200K tokens.
3. **Vision structurée** : tableaux, captures d’interface, schémas et graphiques, avec sortie JSON contrainte.
4. **Tool-use** : appels d’outils multi-tours, erreurs volontairement injectées, et vérification que le modèle ne “répare” pas les faits au hasard.

Step 3.7 Flash est donc une release solide à surveiller. Pas parce qu’elle va tourner partout, mais parce qu’elle montre à quoi ressemble un gros VLM open-weight pensé dès le départ pour l’inférence locale sérieuse.
