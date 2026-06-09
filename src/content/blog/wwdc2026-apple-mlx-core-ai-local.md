---
title: "WWDC 2026 : Apple rapproche MLX, Core AI et modèles locaux dans une même pile"
description: "Apple met à jour son histoire IA locale : MLX gagne Metal 4 et le scaling multi-Mac, Core AI devient le runtime OS pour modèles custom, et Foundation Models s’ouvre aux backends locaux."
pubDate: 2026-06-09
tags: ["Apple", "MLX", "Core AI", "Apple Silicon", "WWDC", "IA locale"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Apple Developer — What’s New in AI & Machine Learning"
    url: "https://developer.apple.com/machine-learning/whats-new/"
  - label: "Apple Developer — Meet Core AI, WWDC26"
    url: "https://developer.apple.com/videos/play/wwdc2026/324/"
  - label: "Apple Machine Learning Research — Exploring LLMs with MLX and the Neural Accelerators in the M5 GPU"
    url: "https://machinelearning.apple.com/research/exploring-llms-mlx-m5"
  - label: "MLX documentation"
    url: "https://ml-explore.github.io/mlx/build/html/index.html"
---

Apple a profité de la séquence WWDC 2026 pour clarifier sa pile IA locale. Le message n’est pas seulement “Apple Intelligence dans les apps”. Pour nous, côté **IA locale**, le signal intéressant est ailleurs : **MLX** continue de progresser pour la recherche et l’inférence sur Apple Silicon, **Core AI** devient un framework OS pour embarquer ses propres modèles, et le **Foundation Models framework** s’ouvre à des fournisseurs conformes à un protocole commun — dont des modèles locaux via Core AI ou MLX.

Ce n’est pas une révolution instantanée pour qui lance déjà `llama.cpp` ou Ollama sur un Mac. Mais c’est un vrai mouvement de plateforme. Apple rapproche progressivement trois mondes qui étaient jusque-là assez séparés : la recherche MLX, le déploiement applicatif Swift, et les expériences agentiques avec outils, évaluations et modèles interchangeables.

## MLX gagne du poids dans la pile officielle

La page “What’s New in AI & Machine Learning” d’Apple indique que **MLX**, le framework open-source d’Apple pour Apple Silicon, gagne le support de **Metal 4** et des **GPU Neural Accelerators** pour de meilleures performances. Apple ajoute aussi un point important pour les machines de bureau : la possibilité de faire monter l’entraînement sur plusieurs Macs avec **RDMA over Thunderbolt**.

Il faut être précis : Apple parle explicitement de scaling pour l’entraînement et la recherche, pas d’un bouton magique “cluster local” qui rendrait n’importe quel gros LLM confortable sur deux MacBook. Mais pour les homelabs Apple Silicon, c’est un signal technique sérieux. Le réseau Thunderbolt à faible latence n’est plus juste une curiosité de démo ; il devient une voie assumée dans la documentation développeur Apple.

MLX lui-même reste ce qu’il était : un framework de tableaux NumPy-like pour Apple Silicon, avec API Python et C++, exécution paresseuse, transformations composables, exécution CPU/GPU et surtout **mémoire unifiée**. La documentation officielle rappelle que les arrays MLX vivent en mémoire partagée et peuvent être manipulés par les devices supportés sans copies explicites. C’est précisément ce qui rend Apple Silicon intéressant pour l’IA locale : une grosse mémoire unifiée n’est pas aussi rapide qu’une VRAM haut de gamme, mais elle permet de charger des modèles que beaucoup de GPU grand public ne peuvent pas tenir.

## Les Neural Accelerators du M5 : surtout le premier token

Apple avait déjà publié un papier technique sur MLX et les **Neural Accelerators du GPU M5** en novembre 2025. Les chiffres cités restent utiles pour comprendre la direction : Apple rapporte jusqu’à environ **4× d’accélération du time-to-first-token** face au M4 sur certains tests LLM, et **19 à 27 %** de mieux sur la génération des tokens suivants, principalement grâce à la bande passante mémoire plus élevée. Le même papier indique que les tests utilisaient `mlx_lm.generate`, avec un prompt de **4096 tokens** et une mesure de génération sur **128 tokens**.

La nuance est importante. Le premier token est souvent limité par le calcul : ingestion du prompt, préfill, grosses multiplications. Les tokens suivants sont plus souvent limités par la bande passante mémoire. Donc les accélérateurs matriciels aident beaucoup le démarrage, tandis que le débit soutenu dépend encore fortement de la mémoire. Ce n’est pas une faiblesse honteuse, c’est la physique. Elle est têtue, comme un benchmark lancé sur batterie.

Apple mentionne aussi dans ce papier qu’un MacBook Pro M5 avec **24 Go de mémoire unifiée** peut faire tenir un modèle **8B en BF16** ou un **MoE 30B quantifié 4-bit** sous 18 Go de charge mémoire pour les architectures testées. Ce n’est pas une garantie universelle — chaque architecture, contexte et runtime change la facture — mais c’est un repère crédible pour le local moderne : les petits et moyens modèles deviennent de vrais citoyens de laptop, pas seulement des démos fragiles.

## Core AI : le runtime OS pour modèles custom

La nouveauté la plus structurante côté apps est **Core AI**. D’après la session WWDC “Meet Core AI” et la page développeur, Core AI est un framework intégré à l’OS, conçu pour Apple Silicon, permettant de déployer et exécuter des modèles on-device avec une API Swift moderne. Apple le présente comme la couche qui alimente Apple Intelligence et qui devient disponible pour les développeurs.

Core AI couvre un cycle assez complet : conversion et authoring via outils Python, déploiement dans les apps via Swift, exécution sur CPU, GPU et Neural Engine, profiling avec Xcode et Instruments, compilation ahead-of-time, spécialisation par appareil, gestion d’état et optimisation mémoire. La session montre par exemple la conversion d’un modèle PyTorch en asset `.aimodel`, puis son chargement côté app.

Pour l’IA locale, le point intéressant est le passage de “je lance un serveur local à côté” à “j’intègre un modèle local dans une app native avec les outils système”. Ce n’est pas le même public que llama.cpp en terminal. Core AI vise les développeurs d’applications Apple qui veulent embarquer de l’inférence privée, responsive, sans serveur, avec contrôle de la mémoire et du profilage.

Il faudra voir les limites réelles : formats supportés, taille des modèles, friction de conversion, performances face à MLX direct ou llama.cpp Metal, compatibilité des architectures récentes. Apple a tendance à proposer de très belles autoroutes… avec des péages subtilement dessinés. Mais techniquement, l’existence d’un runtime OS moderne pour modèles custom est une brique majeure.

## Foundation Models : abstraction, outils et modèles locaux interchangeables

Le **Foundation Models framework** gagne aussi une couche d’abstraction. La page Apple indique que les apps peuvent travailler avec Apple Foundation Models, des modèles cloud comme Claude ou Gemini, ou n’importe quel fournisseur conforme au **Language Model protocol**. La session “What’s new in the Foundation Models framework” ajoute que des modèles open-source ou locaux peuvent être branchés via **CoreAILanguageModel** et **MLXLanguageModel**.

C’est subtil, mais très important : Apple ne dit pas seulement “utilisez notre modèle on-device”. Apple crée une interface Swift pour composer des sessions, outils, profils dynamiques, évaluations et modèles interchangeables. Le même code applicatif peut, en théorie, parler à un modèle Apple local, à Private Cloud Compute, à un fournisseur tiers, ou à un modèle local packagé via Core AI / MLX.

Pour les agents locaux, c’est la bonne abstraction. Un agent n’est pas qu’un modèle : c’est une session, des outils, des contraintes, un contexte, des évaluations et un runtime. Si le modèle devient remplaçable derrière une interface stable, les développeurs peuvent tester plusieurs backends sans réécrire toute l’app.

La session WWDC mentionne aussi des améliorations agentiques : meilleur tool calling, vision, inspection du contexte, token counting, Dynamic Profiles, Evaluations framework, CLI `fm` et SDK Python. Attention toutefois à ne pas tout mélanger. Le modèle on-device Apple reste limité par son contexte et ses capacités propres ; Private Cloud Compute est une option serveur avec le modèle Apple plus puissant ; les modèles locaux open-source via MLX ou Core AI dépendront de leurs poids, quantization et conversion.

## Où cela laisse llama.cpp, Ollama et LM Studio ?

Rien ne les remplace immédiatement. Pour télécharger un GGUF, tester dix quants et exposer un endpoint OpenAI-compatible, **llama.cpp**, **Ollama** et **LM Studio** restent souvent plus directs. Ils bougent vite, supportent énormément d’architectures et vivent au rythme du Hub. Apple, lui, construit une pile plus intégrée : meilleure pour les apps natives, le profiling système, la distribution contrôlée, et probablement les usages grand public.

La vraie question n’est donc pas “MLX ou llama.cpp ?”. C’est plutôt : quel niveau d’intégration veux-tu ? Pour un homelab, GGUF reste roi par sa disponibilité. Pour une app macOS/iOS qui veut embarquer un modèle et utiliser les primitives Apple — Vision, Spotlight, Evaluations, Instruments, Swift — Core AI et Foundation Models deviennent difficiles à ignorer.

MLX occupe une position intermédiaire : plus proche de la recherche et de l’expérimentation, mais de plus en plus relié à la pile applicative. Avec Metal 4, les Neural Accelerators et le multi-Mac via Thunderbolt, Apple signale que MLX n’est pas un jouet de labo abandonné après trois démos. C’est peut-être le message le plus rassurant de cette WWDC pour les gens qui ont investi dans un gros Mac Studio.

## À surveiller avant de conclure trop vite

Trois zones restent à vérifier dans la pratique. D’abord, les performances réelles de Core AI sur des modèles open-weight récents : pas seulement des modèles de démo, mais des LLMs et VLMs actuels, quantifiés proprement, avec contexte long. Ensuite, la facilité de conversion : si chaque architecture demande une chirurgie graph-level, l’adoption restera limitée. Enfin, l’interopérabilité avec l’écosystème Hugging Face : MLX a déjà une communauté active de conversions, mais Core AI devra prouver qu’il peut suivre le rythme.

Le bilan provisoire est sobre : **Apple ne remplace pas encore la stack locale existante, mais elle l’encercle par le bas et par le haut**. Par le bas avec MLX, Metal 4, mémoire unifiée et accélérateurs. Par le haut avec Foundation Models, Core AI, Swift, outils, évaluations et intégration OS.

Pour l’IA locale francophone — devs indépendants, homelabs, équipes qui veulent garder les données sur machine — c’est une bonne nouvelle. Pas parce qu’Apple aurait soudain rendu tous les modèles ouverts plus rapides. Parce que l’IA locale cesse d’être seulement une affaire de scripts Python et de serveurs bricolés : elle devient une cible de plateforme. Et quand Apple transforme une bidouille en API système, le marché suit souvent. Lentement, avec des slides pastel, mais il suit.

## Sources

- Apple Developer — What’s New in AI & Machine Learning : https://developer.apple.com/machine-learning/whats-new/
- Apple Developer — Meet Core AI, WWDC26 : https://developer.apple.com/videos/play/wwdc2026/324/
- Apple Machine Learning Research — Exploring LLMs with MLX and the Neural Accelerators in the M5 GPU : https://machinelearning.apple.com/research/exploring-llms-mlx-m5
- MLX documentation : https://ml-explore.github.io/mlx/build/html/index.html
