---
title: "Nemotron 3 Ultra : NVIDIA pousse l’open-weight américain à 550B paramètres"
description: "Avec Nemotron 3 Ultra, NVIDIA publie un MoE hybride Mamba-Attention de 550B paramètres, 55B actifs, pensé pour les agents longs et l’inférence rapide."
pubDate: 2026-06-06
category: "veille"
tags: ["nvidia", "open-weight", "agents", "benchmarks", "llm"]
author: "Veille IA"
draft: false
sources:
  - label: "NVIDIA Research — Nemotron 3 Ultra"
    url: "https://research.nvidia.com/labs/nemotron/Nemotron-3-Ultra/"
  - label: "Artificial Analysis — NVIDIA Nemotron 3 Ultra released"
    url: "https://artificialanalysis.ai/articles/nvidia-nemotron-3-ultra-released"
  - label: "Hugging Face — NVIDIA Nemotron 3 Ultra collection"
    url: "https://huggingface.co/collections/nvidia/nvidia-nemotron-v3"
---

NVIDIA a publié **Nemotron 3 Ultra**, son plus gros modèle open-weight à ce jour : **550 milliards de paramètres au total**, dont **55 milliards actifs** par token. Le modèle est présenté par NVIDIA comme le membre final et le plus capable de la famille Nemotron 3, avec une architecture **Mixture-of-Experts hybride Mamba-Attention**, une fenêtre de contexte pouvant monter à **1 million de tokens**, et des checkpoints publiés en BF16, NVFP4, base et GenRM.

Ce n’est pas juste une annonce de taille. Le message technique est plus précis : NVIDIA veut montrer qu’un modèle open-weight américain peut redevenir compétitif sur les tâches agentiques longues, tout en restant très rapide en inférence. Selon l’évaluation d’Artificial Analysis publiée le **4 juin 2026**, Nemotron 3 Ultra atteint **47,7** sur l’Artificial Analysis Intelligence Index en NVFP4, et **48,2** en BF16. C’est, dans leur classement, le meilleur score pour un modèle open-weight issu d’un laboratoire américain. Ce n’est pas le meilleur open-weight mondial : Artificial Analysis place encore **Kimi K2.6** devant, à **53,9**. Le détail est important, parce qu’il évite de transformer une vraie avancée en slogan patriotique avec GPU autour.

## Un MoE massif, mais pas dense

Le chiffre de **550B** impressionne, mais le point utile est le ratio actif : **55B paramètres actifs** par token. Nemotron 3 Ultra est donc un modèle sparse MoE. L’idée est classique dans sa direction, mais ambitieuse dans son échelle : conserver une grande capacité totale, tout en limitant le coût d’inférence à une fraction des poids. NVIDIA indique utiliser **LatentMoE**, un mécanisme de routage par représentation latente, et une architecture hybride **Mamba-Attention**.

Le choix de Mamba n’est pas cosmétique. Les architectures basées sur des state space models sont souvent explorées pour réduire certains coûts liés au long contexte, tandis que l’attention reste très forte pour les dépendances précises et les tâches de raisonnement. En pratique, Nemotron 3 Ultra ne dit pas « l’attention est morte » — elle a déjà survécu à trop de nécrologies prématurées — mais tente plutôt une combinaison où Mamba, attention et MoE servent des contraintes différentes : longueur, capacité, débit.

NVIDIA annonce aussi des **MTP layers** pour accélérer l’inférence via décodage spéculatif natif, ainsi qu’un contrôle du budget de raisonnement à l’inférence. Ce sont des briques très orientées production. Un agent long ne coûte pas seulement cher parce qu’il « réfléchit » : il multiplie les tours, les appels d’outils, les lectures de contexte et les corrections d’erreurs. À ce niveau, quelques dizaines de tokens par seconde en plus peuvent changer la latence totale d’une tâche.

## Le long contexte comme cas d’usage agentique

La fiche officielle indique un support jusqu’à **1M tokens** et revendique une performance supérieure aux autres open LLMs sur **RULER** à 1M tokens. C’est un claim intéressant, mais à lire correctement. Une fenêtre d’un million de tokens n’est pas automatiquement une mémoire fiable d’un million de tokens. Les modèles peuvent encore perdre de l’information au milieu, confondre des références ou surpondérer les éléments récents.

L’intérêt est ailleurs : pour des agents de code, d’analyse documentaire, de conformité ou de recherche, le long contexte permet de garder dans la même session de larges pans de dépôt, de logs, de contrats, de traces d’exécution et de notes. NVIDIA publie aussi des jeux de données associés, dont **Nemotron-Pretraining-Code-v3**, annoncé comme contenant **173B tokens** de code frais depuis GitHub jusqu’au **30 septembre 2025**, ainsi que des datasets juridiques et spécialisés. C’est cohérent avec le positionnement : l’agent long a besoin de coder, lire, vérifier, relancer et ne pas halluciner au premier formulaire un peu pénible.

La prudence reste nécessaire. Les jeux de données publiés donnent de la transparence utile, mais ne suffisent pas à établir la robustesse en production. Les vrais tests seront dans des harnais agentiques reproductibles : résolution de tickets, workflows shell, navigation longue, vérification documentaire, tâches où l’échec est silencieux plutôt que spectaculaire.

## Les chiffres d’Artificial Analysis : fort en vitesse, pas leader absolu

Artificial Analysis dit avoir évalué Nemotron 3 Ultra en partenariat avec NVIDIA avant la sortie publique. Leur article donne plusieurs repères : **47,7** sur l’Intelligence Index en NVFP4, **48,2** en BF16, **plus de 400 tokens/s** observés sur un déploiement pré-release BlackBox AI, **71%** sur AA-Omniscience Non-Hallucination, et **1378 Elo** sur GDPval-AA.

Le point le plus solide est le positionnement relatif. D’après Artificial Analysis, Nemotron 3 Ultra est nettement devant les autres open-weights américains évalués : **Gemma 4 31B** à **39,2**, **Nemotron 3 Super** à **36,0**, et **gpt-oss-120b** à **33,3**. Mais il reste derrière le frontier open-weight chinois, notamment Kimi K2.6. Dit autrement : NVIDIA reprend la tête américaine de l’open-weight, pas la tête mondiale.

La vitesse est l’autre signal. Artificial Analysis souligne que le modèle est servi à plus de **400 tokens/s** dans leur mesure pré-release, malgré une taille totale supérieure à 500B. NVIDIA, de son côté, revendique des gains de débit sur le scénario **8k tokens en entrée / 64k tokens en sortie** : **5,9×** face à GLM-5.1-754B-A40B, **4,8×** face à Kimi-K2.6-1T-A32B, et **1,6×** face à Qwen-3.5-397B-17B. Ce sont des chiffres fournis par NVIDIA ; ils devront être reproduits sur des déploiements variés. Mais ils indiquent clairement où NVIDIA veut gagner : pas seulement au score, au **temps de tâche**.

## Open-weight, mais infrastructure lourde

NVIDIA publie plusieurs checkpoints : **NVFP4 post-trained**, **BF16 post-trained**, **BF16 base**, et **GenRM** utilisé pour le RLHF. Les modèles et datasets sont accessibles via Hugging Face et la page officielle Nemotron. C’est plus ouvert que beaucoup de sorties industrielles : poids, données et recettes sont au moins partiellement exposés.

Mais « open-weight » ne veut pas dire « modèle de laptop ». Un MoE de 550B avec 55B actifs reste un objet de datacenter. Le format **NVFP4** le rend plus réaliste sur matériel Blackwell, et NVIDIA a tout intérêt à montrer que son stack matériel-logiciel sait servir ce type de modèle efficacement. Pour une équipe sans infrastructure GPU sérieuse, l’accès passera probablement par API, NIM ou fournisseurs tiers. L’ouverture des poids est donc réelle, mais l’autonomie d’exécution reste conditionnée à une facture matérielle assez sportive. Le local souverain, oui ; le MacBook du café, non.

## Pourquoi cette sortie compte

Nemotron 3 Ultra est intéressant pour trois raisons. D’abord, il remet NVIDIA dans la conversation des modèles, pas seulement des accélérateurs. Ensuite, il cible explicitement les agents longs : contexte massif, débit élevé, MoE sparse, datasets code, contrôle du raisonnement. Enfin, il illustre une tendance forte de 2026 : l’open-weight haut de gamme devient une bataille d’infrastructure autant que d’architecture.

La limite est claire : les meilleurs modèles fermés restent devant sur beaucoup de tâches frontier, et les open-weights chinois gardent une avance mesurée dans certains classements indépendants. Mais Nemotron 3 Ultra donne aux entreprises américaines et européennes une option open-weight beaucoup plus sérieuse pour des agents de production, à condition d’avoir le matériel ou le fournisseur d’inférence qui suit.

À court terme, le bon réflexe n’est pas de demander si Nemotron 3 Ultra « bat Claude » ou « bat GPT ». La vraie question est plus sobre : sur une tâche agentique longue, avec budget de latence contraint et données sensibles, est-ce que ce modèle réduit le coût par tâche sans trop dégrader la fiabilité ? Là, la réponse pourrait devenir intéressante.

## Sources

- NVIDIA Research — Nemotron 3 Ultra: https://research.nvidia.com/labs/nemotron/Nemotron-3-Ultra/
- Artificial Analysis — NVIDIA Nemotron 3 Ultra released: https://artificialanalysis.ai/articles/nvidia-nemotron-3-ultra-released
- Hugging Face — NVIDIA Nemotron 3 Ultra collection: https://huggingface.co/collections/nvidia/nvidia-nemotron-v3
