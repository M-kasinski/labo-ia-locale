---
title: "LeRobot 0.6 transforme la robotique open source en boucle d'apprentissage"
description: "Hugging Face publie LeRobot 0.6.0 avec world models, VLAs, reward models, nouveaux benchmarks, collecte de corrections et entraînement cloud."
pubDate: 2026-07-07
category: "local"
tags: ["robotique", "hugging-face", "lerobot", "world-models", "vla", "open-source"]
author: "Labo IA"
draft: true
sources:
  - label: "Hugging Face Blog — LeRobot v0.6.0"
    url: "https://huggingface.co/blog/lerobot-release-v060"
  - label: "GitHub — huggingface/lerobot v0.6.0"
    url: "https://github.com/huggingface/lerobot/releases/tag/v0.6.0"
---

Hugging Face a publié **LeRobot v0.6.0** le 7 juillet 2026. Ce n'est pas une petite release de confort. Le projet essaie désormais de fermer une vraie boucle robotique : imaginer, évaluer, déployer, corriger, réentraîner.

L'intérêt pour le Labo IA n'est pas seulement "un framework robotique a une nouvelle version". C'est que LeRobot commence à ressembler à une pile ouverte où les modèles, les datasets, les benchmarks, les politiques d'action et les workflows de déploiement se raccordent. Pour la robotique open source, c'est souvent ce raccord qui manque.

## Des politiques qui apprennent aussi à imaginer

La partie la plus intéressante est l'arrivée de politiques orientées **world models**. LeRobot 0.6.0 met en avant VLA-JEPA, LingBot-VA et FastWAM, trois chemins différents vers la même idée : une politique robotique ne doit pas seulement prédire l'action suivante, elle doit aussi apprendre quelque chose de la dynamique future.

VLA-JEPA utilise un modèle compact basé sur Qwen3-VL-2B pour prédire le futur en espace latent pendant l'entraînement. L'astuce est importante : le world model sert de supervision pendant l'apprentissage, mais disparaît à l'inférence. On essaie donc de gagner une meilleure représentation du monde sans payer un coût supplémentaire au moment où le robot agit.

LingBot-VA pousse l'idée plus loin avec un modèle vidéo-action autoregressif. FastWAM, lui, associe un expert vidéo d'environ 5B paramètres à un expert d'action plus compact, puis évite la génération future à l'inférence. Dans les trois cas, le signal est clair : la robotique ouverte emprunte de plus en plus aux modèles de monde, mais cherche encore le bon compromis entre imagination utile et latence acceptable.

## Le zoo VLA devient plus concret

LeRobot 0.6.0 ajoute aussi plusieurs **Vision-Language-Action models** utilisables dans la pile. GR00T N1.7 remplace N1.5 côté intégration NVIDIA, avec un backbone Cosmos-Reason2-2B construit sur Qwen3-VL et une tête d'action flow-matching. MolmoAct2 arrive avec fine-tuning, évaluation et déploiement réel. EO-1, Multitask DiT et EVO1 complètent la liste.

Le détail pratique compte : MolmoAct2 est présenté avec des checkpoints prêts pour SO-100/101, une inférence autour de 12 Go en bf16, et du LoRA sur un GPU 24 Go. EVO1 est beaucoup plus petit, autour de 0,77B paramètres. Ce ne sont pas des garanties de robustesse en cuisine réelle, mais ce sont des profils matériels que des équipes indépendantes peuvent commencer à tester.

C'est précisément ce qui distingue une annonce intéressante d'une démo inaccessible : peut-on l'installer, la fine-tuner, l'évaluer, la faire échouer, puis corriger ?

## Le chaînon manquant : savoir si le robot réussit

La release introduit une API unifiée pour les **reward models** via `lerobot.rewards`. C'est moins spectaculaire qu'une vidéo de robot qui attrape un cube, mais beaucoup plus structurant.

Un robot qui collecte des données doit savoir si l'épisode a marché. Sinon, toute boucle d'apprentissage devient une pile de vidéos jolies mais difficiles à exploiter. LeRobot ajoute Robometer, un reward model 4B entraîné sur des comparaisons de trajectoires, et TOPReward, une approche zéro-shot qui s'appuie sur un VLM existant pour lire la probabilité d'un succès.

Le vrai sujet est l'annotation opérationnelle : générer des courbes de progrès, inspecter la qualité des datasets, alimenter du behavior cloning avec un signal de réussite. La robotique open source n'a pas seulement besoin de modèles plus malins. Elle a besoin de meilleures boucles de feedback.

## Benchmarks, données et déploiement

LeRobot 0.6.0 ajoute six familles de benchmarks simulés sous une commande commune `lerobot-eval`, dont LIBERO-plus, RoboTwin 2.0, RoboCasa365, RoboCerebra, RoboMME et VLABench. Là aussi, la valeur est dans l'unification. Tester une politique robotique reste pénible ; si chaque benchmark demande son propre rituel, personne ne compare proprement.

Côté datasets, la release ajoute le support de la profondeur, de l'encodage vidéo configurable, des annotations langage riches, et une accélération de chargement annoncée jusqu'à 2x. Les annotations langage sont particulièrement importantes : une tâche robotique longue n'est pas seulement une vidéo et une action, c'est une séquence de sous-tâches, corrections, intentions, observations et erreurs.

Le nouveau CLI `lerobot-rollout` déplace aussi le déploiement dans un workflow explicite. Il permet de faire tourner une politique, de conserver des séquences intéressantes, ou de collecter des corrections de type DAgger quand l'humain reprend la main. C'est exactement la boucle dont la robotique a besoin : déployer, voir l'échec, corriger, transformer la correction en donnée, recommencer.

## Pourquoi c'est une vraie news locale

LeRobot 0.6.0 reste une pile exigeante. On parle de GPU sérieux, de robots physiques, de simulateurs avec dépendances système, et de modèles qui peuvent se tromper avec des conséquences matérielles. Ce n'est pas une extension d'Ollama que l'on teste entre deux cafés.

Mais c'est local au sens le plus intéressant du mot : **contrôlable, reproductible, auto-hébergeable, modifiable**. Une équipe peut garder ses trajectoires, ses vidéos, ses corrections et ses politiques dans son infrastructure. Elle peut tester des modèles ouverts, brancher ses propres datasets, mesurer ses propres erreurs, puis ajuster.

La robotique ne deviendra pas fiable parce qu'un modèle sait mieux décrire une image. Elle progressera quand les équipes auront des boucles complètes : capture, annotation, entraînement, évaluation, déploiement, correction. LeRobot 0.6.0 est important parce qu'il rapproche ces briques dans un même atelier.

Et pour une fois, "atelier" n'est pas une métaphore marketing. Il y a vraiment des bras articulés, des caméras, des câbles USB, des datasets qui gonflent, et des politiques qui ratent encore assez souvent pour nous rappeler que le monde physique ne pardonne pas les benchmarks trop propres.
