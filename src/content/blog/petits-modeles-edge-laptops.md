---
title: "Petits modèles, vrai usage : LLM sur edge et laptops modestes"
description: "Ce qui marche vraiment quand on veut faire tourner un LLM utile sans gros GPU : petits modèles récents, quantization agressive et matériel edge réaliste."
pubDate: 2026-05-29
category: "local"
tags: ["ia-locale", "edge", "minicpm", "jetson", "quantization"]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "OpenBMB MiniCPM5-1B", url: "https://huggingface.co/openbmb/MiniCPM5-1B" }
  - { label: "OpenBMB MiniCPM5-1B GGUF", url: "https://huggingface.co/openbmb/MiniCPM5-1B-GGUF" }
  - { label: "Qwen2.5-3B-Instruct", url: "https://huggingface.co/Qwen/Qwen2.5-3B-Instruct" }
  - { label: "Qwen2.5-3B-Instruct GGUF", url: "https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF" }
  - { label: "Qwen2.5-1.5B-Instruct GGUF", url: "https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF" }
  - { label: "Meta Llama 3.2 1B Instruct", url: "https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct" }
  - { label: "Llama 3.2 1B Instruct GGUF", url: "https://huggingface.co/lmstudio-community/Llama-3.2-1B-Instruct-GGUF" }
  - { label: "Google Gemma 2B IT", url: "https://huggingface.co/google/gemma-2b-it" }
  - { label: "NVIDIA Jetson modules", url: "https://developer.nvidia.com/embedded/jetson-modules" }
  - { label: "NVIDIA Jetson Orin Nano blog", url: "https://developer.nvidia.com/blog/solving-entry-level-edge-ai-challenges-with-nvidia-jetson-orin-nano/" }
  - { label: "JetPack 6.2 release notes", url: "https://docs.nvidia.com/jetson/archives/jetpack-archived/jetpack-62/release-notes/index.html" }
---

## Le vrai plafond n’est pas le paramètre, c’est la mémoire

Le marché adore les gros chiffres. En pratique, sur une machine modeste, la vraie question est beaucoup moins glamour : combien de poids tient dans la RAM, combien de contexte tu peux garder, et à quel moment la machine commence à tousser. Pour un assistant local, une automation privée ou un appareil embarqué, le point de bascule est clair : en dessous de 4B, on commence enfin à parler d’usage quotidien. Pas de benchmark de salon.

Le bon créneau, aujourd’hui, c’est souvent 1B à 3B paramètres. Au-dessus, le saut de qualité existe encore, bien sûr, mais il coûte vite trop cher en mémoire et en confort. En dessous, on peut faire du texte utile, du tool calling basique, du résumé, du tri documentaire, du routage d’automations et parfois un peu de code. Pas des miracles. Des tâches réelles.

## Les petits modèles qui méritent vraiment l’attention

MiniCPM5-1B est probablement le symbole le plus net de cette génération. OpenBMB le présente comme un modèle de 1 080 632 832 paramètres, avec 679 552 512 paramètres non-embedding, 24 couches et une fenêtre de contexte de 131 072 tokens. Surtout, la fiche dit sans détour à quoi il sert : assistants locaux, agents de code, workflows d’outils et scénarios de raisonnement. C’est rare d’avoir un modèle aussi petit qui assume aussi clairement ce terrain.

Dans la même famille d’idées, Qwen2.5-1.5B et Qwen2.5-3B sont intéressants parce qu’ils restent simples à déployer. La fiche du 1.5B annonce 1.54B paramètres, et celle du 3B 3.09B paramètres. Les deux sont pensés pour de longues conversations, la sortie structurée et les tâches d’assistant. Qwen2.5 a aussi un avantage pratique : l’écosystème GGUF est bien fourni, donc on ne dépend pas d’un seul runtime pour l’essayer.

Côté Meta, Llama 3.2 1B et 3B vise clairement les environnements contraints. La fiche officielle parle de modèles en 1B et 3B, optimisés pour la traduction dialogue multilingue, la récupération agentique et le résumé. Elle ajoute un point important : ces modèles sont censés être déployés dans des environnements fortement contraints, type mobile. Traduction : ils acceptent la vie dure.

Gemma 2B reste une option propre si tu veux rester dans l’écosystème Google. La page Hugging Face officielle le positionne pour des tâches de génération de texte, de question answering, de résumé et de raisonnement, avec une phrase utile : sa taille rend le déploiement possible sur des machines à ressources limitées, comme un laptop ou un desktop. C’est exactement le genre de formulation qui évite le bullshit. On ne parle pas d’un monstre, on parle d’un modèle raisonnable.

## La quantization extrême n’est pas un gadget

Le Q4_K_M n’est pas un luxe. C’est souvent le point d’équilibre. En dessous, tu gagnes de la place, mais tu perds de la tenue : plus d’hallucinations, plus de réponses plates, plus de comportements un peu nerveux. Ça peut rester acceptable pour de l’automation privée, du tri de mails ou un assistant qui sert surtout à reformuler et extraire. Pour un assistant conversationnel un peu sérieux, Q4 est généralement le plancher propre.

Les poids GGUF donnent une bonne lecture de la réalité matérielle. MiniCPM5-1B en Q4_K_M fait 688 065 920 octets. Qwen2.5-1.5B en Q4_K_M monte à 1 117 320 736 octets. Qwen2.5-3B en Q4_K_M est à 2 104 932 768 octets. Llama 3.2 1B en Q4_K_M est à 807 690 688 octets, et Llama 3.2 3B en Q4_K_M à 2 019 377 440 octets. Ce n’est pas encore la RAM réelle, parce qu’il faut ajouter le runtime, le cache de contexte et un peu d’air pour le système, mais ça te donne le vrai ordre de grandeur.

| Modèle | Quant | Poids GGUF | Ordre de grandeur RAM/VRAM utile | Usage réaliste |
|---|---:|---:|---:|---|
| MiniCPM5-1B | Q4_K_M | 0,69 Go | 2 à 4 Go | assistant local léger, outils, tri de texte |
| Qwen2.5-1.5B | Q4_K_M | 1,12 Go | 4 à 6 Go | assistant privé, résumé, extraction |
| Llama 3.2 1B | Q4_K_M | 0,81 Go | 2 à 4 Go | dialogue court, récupération, multilingue |
| Qwen2.5-3B | Q4_K_M | 2,10 Go | 8 Go mini, 16 Go mieux | assistant plus solide, contexte plus large |
| Llama 3.2 3B | Q4_K_M | 2,02 Go | 8 Go mini, 16 Go mieux | meilleur compromis quand la RAM suit |

En dessous du Q4, tu as les modes de survie : Q3 et Q2. Ils servent quand la machine est trop juste, pas quand tu cherches la beauté. Q2_K sur un 1.5B ou Q3_K sur un 1B peut sauver un déploiement sur une machine vraiment petite, mais il faut accepter un coût qualité net. Pour du résumé court ou des prompts très cadrés, ça passe. Pour de la conversation fluide, ça devient vite grinçant.

## Jetson, laptop sans GPU et Raspberry Pi : le terrain, pas le rêve

Sur Jetson, le message de NVIDIA est assez clair. Le Jetson Orin Nano existe en 4GB et 8GB, avec jusqu’à 40 TOPS sur la page de lancement, et JetPack 6.2 ajoute des modes 10W, 25W et MAXN SUPER pour le 4GB, puis 15W, 25W et MAXN SUPER pour le 8GB. La page modules NVIDIA met aussi à jour la famille Orin Nano avec jusqu’à 67 TOPS et des options de puissance entre 7W et 25W. Moralité : le Nano est devenu un vrai petit poste d’inférence, pas juste un gadget de salon.

En pratique, je le vois comme ça : Orin Nano 4GB pour du 1B Q4 bien cadré, Orin Nano 8GB pour du 1.5B Q4 plus confortable, et Orin NX 16GB dès que tu veux du 3B Q4 avec un peu de marge pour le contexte et les autres processus. Le SXM de démonstration n’est pas le sujet. Le vrai sujet, c’est de ne pas saturer la mémoire avant d’avoir répondu au premier message.

Pour un laptop sans GPU dédié, le seuil est encore plus simple : 16 Go de RAM, c’est la zone de confort pour du 1B à 1.5B en Q4. 32 Go, c’est mieux si tu veux jouer avec du 3B sans transformer la machine en radiateur philosophique. Le CPU-only n’est pas mort, mais il faut arrêter de lui demander de faire le héros.

Le Raspberry Pi, lui, sert surtout à rappeler une vérité utile : un petit modèle n’est pas magique si le reste de la pile est fragile. Sans accélérateur, un Pi convient mieux à des tâches ponctuelles et courtes qu’à un assistant bavard. C’est très bien pour un kiosque, une passerelle, un petit automate privé ou un contrôleur local. Ce n’est pas l’endroit où tu veux lancer un roman.

## Le verdict simple

Si tu veux quelque chose qui marche vraiment sans gros GPU, mon ordre de priorité est simple : MiniCPM5-1B ou Llama 3.2 1B pour le plus petit matériel ; Qwen2.5-1.5B pour le meilleur compromis général ; Qwen2.5-3B ou Llama 3.2 3B dès que la RAM suit ; Gemma 2B si tu veux une option propre, légère, bien positionnée pour laptop et desktop.

Le vrai bon réflexe, ce n’est pas de demander si le modèle “bat” un cloud géant. C’est de demander s’il fait une chose utile, vite, en privé, sur une machine que tu possèdes déjà. C’est moins spectaculaire. C’est aussi beaucoup plus intéressant.
