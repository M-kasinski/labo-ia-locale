---
title: "DiffusionGemma : Google teste le LLM à diffusion, et vLLM suit déjà"
description: "Google publie DiffusionGemma, un modèle open-weight qui génère par blocs de 256 tokens au lieu du token par token classique. Prometteur pour la latence locale, mais pas sans compromis de qualité."
pubDate: 2026-06-11
tags: ["Gemma", "vLLM", "diffusion", "open-weight", "inférence"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Google Blog — DiffusionGemma: 4x faster text generation"
    url: "https://blog.google/innovation-and-ai/technology/developers-tools/diffusion-gemma-faster-text-generation/"
  - label: "Hugging Face — google/diffusiongemma-26B-A4B-it"
    url: "https://huggingface.co/google/diffusiongemma-26B-A4B-it"
  - label: "vLLM Blog — DiffusionGemma: The First Diffusion LLM natively supported in vLLM"
    url: "https://vllm.ai/blog/2026-06-10-diffusion-gemma"
  - label: "Hugging Face — google/gemma-4-26B-A4B"
    url: "https://huggingface.co/google/gemma-4-26B-A4B"
---

Google DeepMind a publié **DiffusionGemma**, un modèle open-weight qui tente une voie encore rare pour les LLM de production : générer du texte par **diffusion discrète** plutôt que strictement de gauche à droite, token après token. Le signal est intéressant pour l’IA locale, parce qu’il ne s’agit pas seulement d’un nouveau checkpoint : c’est une attaque frontale contre le principal plafond de l’inférence interactive, la latence de décodage.

Le modèle est disponible sur Hugging Face sous le nom `google/diffusiongemma-26B-A4B-it`, avec une licence annoncée Apache 2.0 sur la model card. Google le présente comme un modèle bâti sur l’architecture **Gemma 4 26B A4B**, c’est-à-dire un MoE de 25,2 milliards de paramètres au total, mais seulement **3,8 milliards actifs** pendant l’inférence. Le modèle garde aussi plusieurs attributs de Gemma 4 : contexte jusqu’à **256K tokens**, entrées multimodales texte/image, support vidéo via frames, function calling et mode de raisonnement.

La nouveauté n’est donc pas “un Gemma 4 de plus”. C’est le mode de génération. Et là, la plomberie devient vraiment intéressante.

## Générer par blocs, pas au compte-gouttes

Un LLM autoregressif classique prédit le prochain token, l’ajoute au contexte, puis recommence. C’est simple, robuste, mais profondément séquentiel. Même avec un GPU très rapide, chaque token dépend du précédent. DiffusionGemma contourne partiellement ce goulot en travaillant sur un **canvas de 256 tokens**. Le modèle initialise un bloc bruité, puis le débruite en plusieurs passes. Les positions du bloc peuvent se raffiner en parallèle, avec attention bidirectionnelle à l’intérieur du canvas.

La model card décrit ce mécanisme comme du **block-autoregressive multi-canvas sampling** : à l’intérieur d’un bloc, plusieurs tokens se stabilisent en parallèle ; entre les blocs, la génération reste gauche-droite, car chaque bloc validé est réinjecté dans le cache de contexte. Dit autrement : DiffusionGemma ne supprime pas toute séquentialité, mais il augmente le nombre de tokens produits par cycle utile.

Le modèle utilise aussi un mécanisme d’**entropy-bound denoising**. À chaque étape, il ne garde que les positions où sa distribution est suffisamment confiante ; les positions trop incertaines sont “renoised” et réessayées. La génération s’arrête quand les prédictions deviennent stables et que l’entropie moyenne descend sous un seuil, ou quand la limite de pas de débruitage est atteinte. C’est élégant. C’est aussi plus délicat à servir qu’un simple `generate()` autoregressif, parce que l’état interne du canvas, les masques d’attention et le sampling ne suivent plus le chemin standard.

## Les chiffres : très rapides, mais à lire correctement

Google parle d’une génération jusqu’à **4× plus rapide**. La model card indique plus de **1100 tokens/s** en faible batch sur H100 FP8, avec 15 à 20 tokens générés par forward pass. vLLM, de son côté, annonce dans son billet technique **1 008 tokens/s sur H100** et **1 288 tokens/s sur H200** pour son implémentation FP8 à batch size 1, mesurée avec `vllm bench serve`. vLLM précise que cela représente environ **5× à 6×** un baseline autoregressif standard dans leur configuration, et environ **2,6× à 3×** face à une variante avec multi-token prediction.

Ces chiffres sont sérieux, mais ils ne veulent pas dire que ton laptop va soudainement sortir un roman à 1000 tokens/s. H100 et H200 ne sont pas des cartes de salon ; elles ont surtout assez de bande passante mémoire et de compute pour exploiter ce compromis. Pour le local grand public, le vrai intérêt est ailleurs : si l’architecture se généralise, elle peut mieux utiliser des accélérateurs qui sont souvent sous-exploités pendant le décodage token-par-token. En clair : moins attendre sur la mémoire, plus faire travailler les unités de calcul. Le GPU, cette diva, aime qu’on lui donne enfin quelque chose à faire.

## Le compromis qualité existe

Il faut aussi regarder la table de benchmarks, pas seulement le compteur de tokens. Sur la model card, DiffusionGemma 26B A4B est souvent derrière Gemma 4 26B A4B : **MMLU Pro 77,6 % contre 82,6 %**, **AIME 2026 69,1 % contre 88,3 %**, **LiveCodeBench v6 69,1 % contre 77,1 %**, **GPQA Diamond 73,2 % contre 82,3 %**. Même constat côté vision : **MMMU Pro 54,3 % contre 73,8 %** et **MATH-Vision 70,5 % contre 82,4 %**.

Ce n’est donc pas un remplacement évident de Gemma 4. C’est plutôt un modèle de recherche déjà utilisable, optimisé pour les scénarios où la latence et le débit par utilisateur comptent beaucoup : complétion interactive, édition de texte, génération structurée, assistants rapides, peut-être certains usages de code completion. Pour des tâches de raisonnement lourd ou de vision exigeante, Gemma 4 classique reste, d’après les chiffres publiés par Google, plus solide.

Le point important pour un média local-first : la performance brute ne suffit pas. Un modèle qui répond vite mais perd 10 à 20 points sur certaines évaluations ne gagne pas automatiquement. Il faut choisir selon l’usage, pas selon la bannière marketing.

## Pourquoi le support vLLM compte

La partie la plus rassurante de cette sortie est peut-être le support immédiat dans **vLLM**. Le projet explique avoir intégré DiffusionGemma via la nouvelle abstraction **ModelState** du model runner v2. L’idée : laisser un modèle définir son état par requête, sa préparation d’inputs, ses masques d’attention et son sampler, sans forker tout le runner.

C’est crucial parce qu’un dLLM ne rentre pas proprement dans le chemin autoregressif habituel. vLLM doit gérer des phases différentes : prefill causal, débruitage bidirectionnel du canvas, puis commit causal des tokens acceptés dans le KV cache. Le billet détaille aussi le support d’une causalité dynamique par séquence dans les backends **Triton Attention** et **FlashAttention 4**, ainsi qu’une adaptation de la sliding-window attention pour le mode bidirectionnel.

Traduction pratique : si d’autres modèles de diffusion textuelle arrivent, vLLM a maintenant une route technique pour les accueillir sans réécrire toute la pile. Ce n’est pas une petite note de version ; c’est un changement d’interface entre architecture modèle et moteur de serving.

## Ce que ça change pour l’IA locale

À court terme, DiffusionGemma intéressera surtout les machines sérieuses : gros GPU NVIDIA, FP8/NVFP4, serveurs vLLM, quantizations communautaires à surveiller. Google et vLLM documentent des checkpoints quantifiés, et le modèle est suffisamment ouvert pour que les conversions GGUF/MLX/Autres apparaissent rapidement si la communauté juge le compromis utile.

À moyen terme, le sujet dépasse DiffusionGemma. Les modèles locaux souffrent souvent moins d’un manque de paramètres que d’un mauvais rapport **latence / qualité / mémoire**. Les architectures qui produisent plusieurs tokens utiles par passe peuvent changer ce calcul, surtout pour les agents interactifs où le temps de réponse compte autant que le score académique.

Mon avis provisoire : DiffusionGemma n’est pas “le nouveau meilleur modèle local”. C’est plus intéressant que ça. C’est une démonstration crédible qu’un grand lab peut sortir un modèle open-weight non-autoregressif, avec une intégration de serving sérieuse dès le jour de lancement. Les benchmarks qualité imposent la prudence, mais l’idée technique mérite clairement d’être suivie. Si la prochaine génération réduit l’écart de qualité tout en gardant ce profil de latence, le token-par-token commencera à sentir le vieux monde.

## Sources

- Google Blog — DiffusionGemma: 4x faster text generation : https://blog.google/innovation-and-ai/technology/developers-tools/diffusion-gemma-faster-text-generation/
- Hugging Face — google/diffusiongemma-26B-A4B-it : https://huggingface.co/google/diffusiongemma-26B-A4B-it
- vLLM Blog — DiffusionGemma: The First Diffusion LLM natively supported in vLLM : https://vllm.ai/blog/2026-06-10-diffusion-gemma
- Hugging Face — google/gemma-4-26B-A4B : https://huggingface.co/google/gemma-4-26B-A4B
