---
title: "whichllm : choisir un modèle local par benchmark, pas au doigt mouillé"
description: "Le CLI whichllm détecte ton matériel, estime ce qui tient en mémoire et classe les modèles Hugging Face avec des benchmarks pondérés et récents."
pubDate: 2026-06-01
tags: ["outil", "benchmark", "local-llm", "huggingface", "gpu"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub — Andyyyy64/whichllm"
    url: "https://github.com/Andyyyy64/whichllm"
  - label: "GitHub Releases — whichllm"
    url: "https://github.com/Andyyyy64/whichllm/releases"
  - label: "Hacker News — Show HN: Find the best local LLM for your hardware"
    url: "https://news.ycombinator.com/item?id=48146369"
---

Choisir un modèle local reste un petit sport de combat. Tu regardes la VRAM, tu compares trois leaderboards, tu ajoutes une couche de quantization, tu lis un thread contradictoire, puis tu télécharges 18 Go “juste pour tester”. **whichllm** essaie de transformer ce rituel en commande reproductible : détecter le matériel, estimer ce qui tient vraiment, puis classer les modèles avec des benchmarks plutôt qu’avec le réflexe paresseux du “plus gros qui rentre”.

Le projet, publié sur GitHub sous licence MIT, se présente comme un CLI Python : **“Find the local LLM that actually runs and performs best on your hardware”**. La promesse est simple et assez saine : recommander le meilleur modèle local pour une machine donnée, réelle ou simulée, en tenant compte de la mémoire, de la vitesse estimée, de la quantification, de l’architecture et de benchmarks récents.

Ce n’est pas un runtime concurrent d’Ollama, llama.cpp ou MLX. C’est plutôt une couche de décision au-dessus du chaos Hugging Face. Et franchement, le chaos avait besoin d’un videur à l’entrée.

## Le problème : “ça rentre” ne veut pas dire “c’est le bon choix”

La plupart des outils de compatibilité répondent à une question utile mais insuffisante : est-ce que ce modèle tient dans ma VRAM ? whichllm part d’une critique correcte : un modèle peut tenir et rester un mauvais choix. Un 32B ancien, mal quantifié ou faible sur les tâches visées peut être inférieur à un 27B plus récent. Un MoE peut être rapide parce que ses paramètres actifs sont modestes, mais sa qualité dépend quand même de sa capacité totale. Un modèle vision peut avoir besoin d’un autre référentiel d’évaluation qu’un LLM texte.

Le README donne un exemple parlant pour une RTX 4090 : le classement peut préférer **Qwen/Qwen3.6-27B en Q5_K_M** à un **Qwen3-32B en Q4_K_M**, malgré la taille supérieure du second, parce que le score de benchmark et la récence changent le résultat. C’est exactement le genre de décision qu’un tableau de VRAM ne sait pas prendre.

Les chiffres précis du README sont évidemment des instantanés : les résultats utilisent des données Hugging Face vivantes et peuvent évoluer. Mais la logique est plus importante que l’exemple : **la sélection d’un modèle local doit être multi-critères**.

## Comment whichllm classe les modèles

D’après le dépôt GitHub, whichllm combine plusieurs dimensions :

- détection du matériel : NVIDIA, AMD, Apple Silicon, CPU-only ;
- estimation de mémoire : poids, KV cache GQA, activations, overhead ;
- prise en compte de la quantization et du backend ;
- estimation de vitesse selon bande passante, architecture et paramètres actifs pour les MoE ;
- récupération de modèles via l’API Hugging Face ;
- fallback de données si l’API est indisponible ou rate-limitée ;
- pondération de benchmarks comme LiveBench, Artificial Analysis, Aider, Chatbot Arena, Open LLM Leaderboard et des sources multimodales.

Le point intéressant est la notion de **confiance de preuve**. Le projet distingue des scores directs, dérivés d’une variante, interpolés ou auto-déclarés, et applique des pénalités. C’est imparfait par construction — fusionner des benchmarks hétérogènes est toujours discutable — mais c’est plus honnête que de mettre tous les scores dans un mixeur et d’appeler ça “intelligence”.

whichllm tient aussi compte de la récence. C’est essentiel en 2026 : un leaderboard de 2024 peut encore contenir des modèles bien classés sur des tests saturés, alors que des familles récentes les dépassent en pratique. Le README indique que les anciens scores sont déclassés le long des lignées de modèles afin d’éviter qu’un vieux résultat très favorable domine une recommandation actuelle.

## Les commandes utiles

Le projet est pensé pour être lancé sans installation lourde :

```bash
uvx whichllm@latest
```

Pour simuler une carte avant achat :

```bash
uvx whichllm@latest --gpu "RTX 4090"
```

Le CLI propose aussi :

```bash
whichllm upgrade "RTX 4090" "RTX 5090" "H100"
whichllm plan "llama 3 70b"
whichllm run "qwen 2.5 1.5b gguf"
whichllm snippet "qwen 7b"
whichllm --top 1 --json
```

Le mode JSON est plus important qu’il n’en a l’air. Pour un labo perso, un NAS ou une machine de benchmark, pouvoir intégrer une recommandation dans un script est utile : choix automatique d’un modèle, génération d’une configuration, comparaison avant téléchargement, ou audit périodique des meilleurs candidats.

## Les dernières releases : plus de matériel, moins de naïveté

La page des releases montre que le projet a beaucoup durci sa gestion matérielle en mai 2026. La version **v0.5.7**, datée du 19 mai, ajoute notamment la détection de **DGX Spark / NVIDIA GB10** comme GPU NVIDIA à mémoire partagée lorsque NVIDIA ne reporte pas `memory.total`, corrige des crashes de gros modèles Transformers via `offload_folder`, respecte `XDG_CACHE_HOME`, traite Apple Silicon comme mémoire partagée pour la détection de fit, et inline des fallbacks LiveBench.

Les versions précédentes ajoutent ou corrigent plusieurs cas très concrets : estimation de vitesse pour MoE, détection AMD/Intel sous Windows, gestion des APU Ryzen AI / Radeon 890M, support Strix Halo / Ryzen AI MAX, détection iGPU Intel sous Linux, fallback `nvidia-smi`, et corrections autour du lancement de modèles GGUF.

Ce sont des détails peu sexy, mais ce sont eux qui font la différence entre un outil utilisable et une démo. Le local est rempli de configurations bizarres : Apple Silicon à mémoire unifiée, iGPU qui emprunte de la RAM, GPU NVIDIA avec VRAM dédiée, APU AMD, CPU-only avec beaucoup de RAM, machines hybrides. Si l’outil suppose “GPU = VRAM dédiée classique”, il se trompe vite.

## Les limites : un classement n’est pas une vérité

whichllm ne résout pas le problème fondamental des benchmarks : ils ne sont jamais exactement ton usage. Aider est pertinent pour le code, LiveBench couvre autre chose, Chatbot Arena mesure une préférence humaine agrégée, Open LLM Leaderboard a ses biais, et les benchmarks multimodaux ne disent pas tout de l’OCR sur tes factures en français.

Il faut donc lire whichllm comme un **filtre de première passe**, pas comme un oracle. Sa recommandation peut éviter trois mauvais téléchargements, mais elle ne remplace pas un test local sur tes prompts, tes documents, ton niveau de quantization et ton runtime.

Autre prudence : le projet dépend de données externes et d’heuristiques. Les estimations de tokens/s sont par nature approximatives. Elles peuvent varier selon les kernels, le système, la température GPU, les drivers, le contexte, le batch, le format GGUF/AWQ/GPTQ, et la version de llama.cpp ou Transformers. Bref : la physique continue de gagner tous ses procès.

## Pourquoi c’est pertinent pour Labo IA Locale

Le marché local manque moins de modèles que de **méthodes de sélection**. Chaque semaine apporte des variantes GGUF, MLX, AWQ, GPTQ, instruct, reasoning, coder, vision, MoE. Sans outil de tri, on finit par suivre la hype ou par utiliser toujours le même modèle par fatigue.

whichllm pousse dans la bonne direction : hardware-aware, benchmark-aware, scriptable, et suffisamment explicite sur ses critères. Même si ses choix doivent être vérifiés, il aide à poser les bonnes questions : quel modèle tient vraiment ? lequel est récent ? quelle preuve soutient son score ? combien de tokens/s attendre ? est-ce que le MoE est évalué par paramètres actifs ou totaux ?

Pour un utilisateur local, c’est une brique pratique. Pour un site comme celui-ci, c’est aussi un rappel éditorial : comparer des modèles sans préciser matériel, quantization, runtime et benchmark ne vaut pas grand-chose. C’est joli en capture d’écran, mais pas très scientifique.

## Verdict provisoire

whichllm n’est pas magique, mais son angle est bon. Il ne promet pas de rendre les benchmarks parfaits ; il les rend exploitables dans une décision locale. C’est déjà beaucoup.

Je le classerais dans les outils à tester avant achat GPU, avant migration de modèle, ou avant de télécharger une nouvelle famille open-weight “parce que tout le monde en parle”. Il faudra surveiller la maintenance, la qualité des sources de benchmark et la robustesse des heuristiques. Mais l’idée centrale — **choisir un modèle local par preuves pondérées plutôt que par taille de fichier** — est exactement celle dont l’écosystème a besoin.

Sources :

- GitHub — Andyyyy64/whichllm : https://github.com/Andyyyy64/whichllm
- GitHub Releases — whichllm : https://github.com/Andyyyy64/whichllm/releases
- Hacker News — Show HN : https://news.ycombinator.com/item?id=48146369
