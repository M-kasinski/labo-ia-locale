---
title: "Cosmos 3 : NVIDIA veut un modèle ouvert pour raisonner, simuler et agir dans le monde physique"
description: "Avec Cosmos 3, NVIDIA relie vision reasoning, génération vidéo, audio et actions dans une famille de world models ouverte. Le pari : accélérer robotique, véhicules autonomes et agents physiques."
pubDate: 2026-06-03
category: "veille"
tags: ["nvidia", "world-models", "robotique", "multimodal", "open-weight"]
author: "Veille IA"
draft: false
sources:
  - label: "NVIDIA Newsroom — Cosmos 3 launch"
    url: "https://nvidianews.nvidia.com/news/nvidia-launches-cosmos-3-the-open-frontier-foundation-model-for-physical-ai"
  - label: "NVIDIA Research — Cosmos 3 technical report"
    url: "https://research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf"
  - label: "NVIDIA — Cosmos platform page"
    url: "https://www.nvidia.com/en-us/ai/cosmos/"
---

NVIDIA a lancé **Cosmos 3**, une famille de modèles de fondation pour “physical AI” présentée comme ouverte et conçue pour relier compréhension visuelle, simulation du monde, génération multimodale et prédiction d’actions. L’annonce, publiée par le newsroom NVIDIA autour de GTC Taipei, vise directement la robotique, les véhicules autonomes, les agents visuels, les espaces industriels et la génération de données synthétiques.

La formule marketing parle d’“omnimodel”. Derrière le mot un peu brillant — il fallait bien nourrir le service communication, les pauvres — il y a une idée technique claire : plutôt que d’empiler un VLM pour comprendre, un générateur vidéo pour imaginer, un simulateur pour tester et un modèle de politique pour agir, NVIDIA tente de réunir ces fonctions dans une architecture commune.

## Ce que Cosmos 3 essaie de faire

Selon NVIDIA, Cosmos 3 peut comprendre et générer à travers **texte, image, vidéo, son ambiant et actions**. La page produit le présente comme un modèle de fondation physique capable de **raisonner, simuler, générer et agir** dans des environnements réels. Le communiqué officiel insiste sur trois axes : vision reasoning, world generation et action prediction.

Cette combinaison cible un problème structurel de la physical AI. Pour entraîner un robot ou un véhicule autonome, il faut énormément de données sur des situations physiques : trajectoires, interactions d’objets, erreurs rares, conditions météo, comportements humains, sons, temps de réaction, conséquences d’une action. Capturer tout cela dans le monde réel est lent, coûteux et parfois dangereux. Les simulateurs aident, mais ils restent fragmentés et souvent difficiles à relier directement aux modèles de décision.

Cosmos 3 veut devenir une couche commune : comprendre une scène, générer des futurs plausibles, produire des données synthétiques, post-entraîner un modèle d’action ou servir de simulateur contrôlable. Dans le rapport technique, NVIDIA écrit que la famille Cosmos 3 peut fonctionner, sans changement architectural, comme VLM, générateur texte-image, texte-vidéo, image-vidéo, audio-vidéo, modèle de dynamique directe, modèle de dynamique inverse ou modèle de politique/action.

## Une architecture “Mixture-of-Transformers”

Le cœur technique est une architecture appelée **Mixture-of-Transformers**. D’après le rapport NVIDIA, elle combine deux voies principales : une tour de raisonnement autoregressive pour le langage et la compréhension image/vidéo, et une tour générative de type diffusion pour les tokens image/vidéo, audio et action. Les deux voies partagent le contexte via attention conjointe, tout en conservant des paramètres spécialisés.

C’est différent d’un simple “gros transformer multimodal” qui avalerait tout de la même manière. NVIDIA sépare explicitement les besoins : le langage se génère par prédiction du prochain token, tandis que les modalités non linguistiques passent par débruitage itératif et rectified flow matching. En clair : raisonner sur une scène et générer une vidéo physiquement plausible ne mobilisent pas exactement les mêmes mécanismes, mais ils doivent communiquer.

Le rapport détaille aussi le traitement des actions comme des tokens de première classe. Les actions couvrent plusieurs domaines : véhicules autonomes, robots, mouvements de caméra et mouvements égocentriques humains. Pour unifier ces espaces très différents, NVIDIA utilise des pseudo-actions géométriques : pose ego, pose d’effecteur, état de préhension, avec des projections propres à chaque domaine vers un espace latent commun.

Ce choix est important. Dans beaucoup de systèmes multimodaux, l’action reste une sortie secondaire, ajoutée après coup. Ici, Cosmos 3 essaie de modéliser l’action comme une modalité au même niveau conceptuel que l’image, la vidéo ou l’audio. Pour la robotique, c’est précisément là que se joue la différence entre “décrire une scène” et “faire quelque chose dans cette scène”.

## Les tailles et les données

Le rapport technique décrit trois variantes : **Edge**, **Nano** et **Super**. Edge est annoncé comme un modèle 4B destiné à l’inférence en périphérie, avec disponibilité ultérieure. Nano monte à 16B, et Super à 64B. La page NVIDIA indique que Cosmos 3 Super vise la meilleure qualité de génération et précision physique pour le post-entraînement robotique et véhicule autonome, tandis que Nano cible un raisonnement vidéo/action plus rapide.

Côté données, les chiffres sont massifs. Pour la partie Reasoner, le rapport mentionne **24,2 millions d’échantillons**, dont 22 millions pour le pré-entraînement et 2,2 millions pour le SFT. Pour la partie Generator, NVIDIA indique **767 millions d’images**, **347,7 millions de clips vidéo**, **138,9 millions de clips audio-vidéo**, puis une phase mid-training avec notamment 74,7 millions de vidéos et 8,4 millions d’épisodes d’action représentant **61,3 mille heures**.

Ces chiffres donnent une idée du fossé entre un modèle multimodal de démonstration et un modèle destiné à la physical AI. La difficulté n’est pas seulement d’avoir des pixels ; c’est d’aligner pixels, temps, son, mouvement, action et plausibilité physique. NVIDIA indique utiliser une extension temporelle de MRoPE pour aligner vidéo, audio et actions malgré des fréquences différentes. Le détail est aride, mais central : un robot ne vit pas dans une capture d’écran, il vit dans le temps.

## Ouvert, mais dans quel sens ?

NVIDIA présente Cosmos 3 comme ouvert. La page Cosmos indique que les world foundation models sont disponibles sous licence **Linux Foundation OpenMDW 1.1**, avec modèles, code, cookbook, datasets synthétiques et outils d’évaluation. Le rapport technique mentionne une collection Hugging Face, le dépôt `github.com/nvidia/cosmos`, ainsi que des datasets synthétiques comme SDG-PhyxSim, SDG-RobotSim et SDG-DriveSim.

C’est un point notable : l’open-weight dans la robotique et les world models est potentiellement plus structurant que dans le chatbot généraliste. Les équipes ont besoin de post-entraîner sur leurs capteurs, leurs robots, leurs environnements et leurs contraintes. Un modèle fermé accessible uniquement par API serait beaucoup moins utile pour du contrôle bas niveau, de l’évaluation fermée ou de la simulation industrielle.

Cela dit, “ouvert” ne signifie pas automatiquement reproductible. Les volumes de données, le matériel nécessaire, les pipelines de curation et les dépendances à l’écosystème NVIDIA restent considérables. Cosmos 3 est ouvert dans son usage et son adaptation, pas dans le sens où un petit labo pourra réentraîner proprement l’ensemble depuis zéro sur trois GPU et une machine à café courageuse.

## Benchmarks : à lire avec prudence

NVIDIA affirme que Cosmos 3 obtient des résultats de tête parmi les modèles ouverts sur plusieurs catégories : génération de monde, action policy et vision understanding. Le communiqué cite notamment Artificial Analysis, Physics-IQ, PAI-Bench, R-Bench, RoboLab, RoboArena, VANTAGE-Bench et TAR leaderboard.

Il faut rester prudent. Les benchmarks de physical AI sont plus jeunes et moins stabilisés que les évaluations texte ou code. Ils mélangent parfois perception, génération, simulation, physique, action et préférences humaines. Un modèle peut produire une vidéo convaincante sans être fiable pour contrôler un robot réel. À l’inverse, une politique robuste peut sembler moins spectaculaire qu’une génération vidéo très propre.

La revendication la plus intéressante n’est donc pas “Cosmos 3 est premier”. C’est plutôt : NVIDIA propose une pile cohérente pour évaluer, générer, post-entraîner et déployer des modèles physiques. Dans un domaine où les pipelines sont souvent bricolés à partir de modules spécialisés, l’intégration peut compter autant que le score brut.

## Pourquoi ça compte

Cosmos 3 confirme une tendance : la prochaine bataille des modèles ne se limite pas aux chatbots. Les agents qui interagissent avec le monde physique auront besoin de modèles capables de prédire des conséquences, pas seulement de répondre correctement à une question. Pour un véhicule autonome, un robot d’entrepôt ou un agent vidéo de sécurité, la sortie utile n’est pas seulement une phrase ; c’est une trajectoire, une alerte, une décision, une simulation de futur possible.

NVIDIA est bien placé pour pousser cette direction, parce que l’entreprise contrôle une grande partie du matériel, des outils de simulation, de l’inférence et des bibliothèques utilisées dans ces secteurs. Cosmos 3 n’est donc pas seulement un modèle : c’est une brique dans une stratégie complète qui relie GPU, serveurs RTX/Blackwell, Omniverse, données synthétiques, robotics et inference edge.

## À retenir

Cosmos 3 est une annonce importante parce qu’elle déplace la conversation des modèles multimodaux vers les **modèles actionnables**. Comprendre une vidéo est utile. Générer un futur plausible est plus utile. Relier ce futur à une action robotique ou à une politique d’autonomie, c’est le vrai saut.

Il reste beaucoup d’incertitude : robustesse hors distribution, qualité réelle des données synthétiques, passage de la simulation au monde réel, coûts de post-entraînement, maturité des benchmarks. Mais le cap est net. NVIDIA veut que le world model devienne une infrastructure de base pour la physical AI, pas une curiosité de laboratoire. Et cette fois, le mot “agent” commence à vouloir dire autre chose que “un chatbot avec des outils”.
