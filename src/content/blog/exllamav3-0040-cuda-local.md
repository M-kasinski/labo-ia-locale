---
title: "ExLlamaV3 0.0.40 : le runner NVIDIA local rattrape les modèles multimodaux récents"
description: "La dernière release d’ExLlamaV3 ajoute Gemma4Unified et confirme une trajectoire claire : inference CUDA locale, quantization EXL3, batching et serveur OpenAI-compatible via TabbyAPI."
pubDate: 2026-06-08
category: "local"
tags: ["ExLlamaV3", "CUDA", "quantization", "inference locale", "TabbyAPI", "NVIDIA"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub — turboderp-org/exllamav3"
    url: "https://github.com/turboderp-org/exllamav3"
  - label: "GitHub Releases — ExLlamaV3 v0.0.40"
    url: "https://github.com/turboderp-org/exllamav3/releases"
  - label: "GitHub — TabbyAPI, serveur officiel pour Exllama"
    url: "https://github.com/theroyallab/tabbyAPI/"
  - label: "Startup Fortune — ExLlamaV3 makes local AI infrastructure more practical for founders"
    url: "https://startupfortune.com/exllamav3-makes-local-ai-infrastructure-more-practical-for-founders/"
---

ExLlamaV3 continue d’avancer vite, mais pas sur le même terrain que llama.cpp ou Ollama. La release **v0.0.40**, publiée le **6 juin 2026** sur GitHub, ajoute le support de **`Gemma4UnifiedForConditionalGeneration`** et livre des roues précompilées CUDA pour Linux et Windows. Ce n’est pas une révolution grand public. C’est plutôt un signal pour les machines NVIDIA locales : ExLlamaV3 veut rester le runner spécialisé des modèles quantifiés sur GPU consumer.

Le dépôt officiel décrit ExLlamaV3 comme une bibliothèque d’**inférence et de quantization** pour faire tourner des LLM localement sur des GPU modernes de classe consommateur. Le projet est sous licence **MIT**, écrit principalement en Python avec une part importante de CUDA, et son README met en avant le format **EXL3**, le tensor parallel, l’expert parallel, le dynamic batching, la speculative decoding, la quantization du cache entre **2 et 8 bits**, les LoRA, le multimodal et l’intégration avec Transformers.

## Une release petite, mais bien placée dans le calendrier

La v0.0.40 n’a qu’un changement fonctionnel visible dans la page Releases : le support de `Gemma4UnifiedForConditionalGeneration`. Pris isolément, c’est mince. Mais le contexte compte : Gemma 4 vient d’occuper beaucoup de place dans l’écosystème local, notamment avec des variantes multimodales et quantifiées. Ajouter rapidement l’architecture dans ExLlamaV3 permet aux utilisateurs CUDA de tester ces modèles sans attendre que tout passe par les chemins plus généralistes.

La release fournit des wheels pour **CUDA 12.8** et **Torch 2.10.0**, avec Python **3.10 à 3.14** selon les artefacts listés, sur Linux x86_64 et Windows amd64. C’est très concret : ExLlamaV3 ne cherche pas à être portable partout, il choisit son camp. Si tu as une carte NVIDIA et un environnement Python/CUDA compatible, l’expérience peut être très efficace. Si tu es sur Mac, CPU-only, AMD ou NPU exotique, ce n’est pas ton outil principal. Pour une fois, la segmentation est claire ; presque reposante.

## EXL3 : le cœur du sujet

Le vrai intérêt d’ExLlamaV3 reste son format **EXL3** et son orientation low-bit. Le README présente EXL3 comme un format de quantization basé sur QTIP, pensé pour faire entrer des modèles plus gros dans la VRAM disponible tout en gardant une qualité acceptable. Le projet ajoute autour de ça le tensor parallel et l’expert parallel, utiles quand on répartit un modèle ou des experts MoE sur plusieurs GPU.

Ce positionnement est différent de GGUF. GGUF et llama.cpp sont devenus le socle polyvalent : CPU, GPU, Metal, Vulkan, modèles variés, compatibilité large. ExLlamaV3 est plus étroit, mais plus agressif sur son domaine : **NVIDIA + CUDA + modèles quantifiés Hugging Face**. Pour les stations de travail avec RTX 3090, 4090, 5090 ou petits montages multi-GPU, c’est une niche qui compte.

La quantization du KV cache entre 2 et 8 bits est aussi importante. Sur des contextes longs, la mémoire n’est pas seulement consommée par les poids du modèle ; le cache d’attention devient vite le mur. Réduire ce coût peut permettre plus de contexte, plus de batching ou simplement moins de crashes quand l’application passe du test isolé au vrai usage.

## TabbyAPI : indispensable pour sortir du script de démo

Le README d’ExLlamaV3 indique que le serveur recommandé est **TabbyAPI**. Le dépôt TabbyAPI se présente comme le serveur officiel pour ExllamaV2 et ExllamaV3, basé sur FastAPI, compatible avec l’API OpenAI, et capable de gérer génération, téléchargement de modèles Hugging Face, embeddings, JSON schema, regex, EBNF, speculative decoding et multi-LoRA.

C’est là que le projet devient intéressant pour l’auto-hébergement. Une bibliothèque d’inférence rapide est utile ; un serveur local compatible OpenAI l’est beaucoup plus. Cela permet de brancher des clients existants, des agents, des outils RAG ou des interfaces maison sans réécrire toute la pile. Attention tout de même : le README de TabbyAPI précise que le projet est en **rolling release**, qu’il peut casser, et qu’il n’est pas destiné à des serveurs de production à grande échelle. Pour un homelab ou une équipe technique, très bien. Pour vendre un SLA bancaire, respire deux secondes.

## Les benchmarks : prometteurs, pas encore une vérité générale

Un article de Startup Fortune publié en mai 2026 résume l’intérêt business d’ExLlamaV3 : rendre l’inférence locale plus praticable pour des équipes techniques qui veulent réduire leurs coûts API, garder les données sensibles en interne et contrôler leur matériel. L’article cite aussi des chiffres communautaires autour de **DFlash**, avec un passage de **59,21 à 177,67 tokens/s** sur un benchmark de code et de **55,98 à 140,61 tokens/s** sur une charge agentique de code.

Ces chiffres sont à prendre avec prudence : ils viennent de discussions communautaires rapportées par un média, pas d’un banc d’essai académique ou d’une comparaison indépendante entièrement reproductible dans l’article. Ils restent cohérents avec la trajectoire du projet : optimisation forte pour certains chemins CUDA, modèles quantifiés et workloads de génération locale. Mais il ne faut pas les transformer en promesse universelle. La performance dépendra du modèle, du bitrate EXL3, du GPU, du contexte, du batching et des kernels effectivement utilisés.

## Quand choisir ExLlamaV3 plutôt qu’Ollama ou llama.cpp ?

Le bon cas d’usage est assez net : tu as une machine NVIDIA, tu veux exploiter des modèles Hugging Face quantifiés en EXL3, tu acceptes de gérer CUDA/PyTorch, et tu privilégies débit, mémoire et contrôle fin. ExLlamaV3 devient alors une option sérieuse, surtout avec TabbyAPI devant pour exposer une API plus standard.

Si tu veux une installation simple, des modèles en un `ollama run`, une compatibilité Mac ou CPU, Ollama et llama.cpp restent plus rationnels. Si tu fais du serving multi-utilisateur massif en datacenter, vLLM garde ses arguments. ExLlamaV3 n’a pas besoin de gagner partout. Il doit être excellent dans son couloir.

La v0.0.40 confirme justement cette stratégie : suivre vite les nouvelles architectures, améliorer les chemins CUDA, et donner aux possesseurs de GPU consumer une pile locale crédible. Pas universelle, pas magique, mais efficace. Dans l’IA locale, c’est déjà une très bonne phrase.

## Sources

- GitHub — turboderp-org/exllamav3 : https://github.com/turboderp-org/exllamav3
- GitHub Releases — ExLlamaV3 : https://github.com/turboderp-org/exllamav3/releases
- GitHub — TabbyAPI : https://github.com/theroyallab/tabbyAPI/
- Startup Fortune — ExLlamaV3 makes local AI infrastructure more practical for founders : https://startupfortune.com/exllamav3-makes-local-ai-infrastructure-more-practical-for-founders/
