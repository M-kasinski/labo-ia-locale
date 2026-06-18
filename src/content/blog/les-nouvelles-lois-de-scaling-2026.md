---
title: "Les nouvelles lois de scaling : pourquoi « plus grand » ne suffit plus"
description: "En 2025-2026, le scaling des modèles fondation a changé de dimension : compute d'inférence, multi-agents, recherche automatisée, architectures efficaces. Ce qui remplace la course aux paramètres."
pubDate: 2026-05-29
category: "veille"
tags: ["scaling", "architecture", "recherche", "MoE", "multi-agent"]
author: "Veille IA"
draft: false
sources:
  - label: "Paper: Scaling Test-Time Compute (arxiv 2408.03314)"
    url: "https://arxiv.org/abs/2408.03314"
  - label: "Paper: The Art of Scaling Test-Time Compute (arxiv 2512.02008)"
    url: "https://arxiv.org/abs/2512.02008"
  - label: "Concept Paper: Multi-Agent LLM Systems (preprints.org)"
    url: "https://www.preprints.org/manuscript/202511.1370"
  - label: "Paper: Scaling Agent Systems (arxiv 2512.08296)"
    url: "https://arxiv.org/abs/2512.08296"
  - label: "Inference-Time Scaling Update (introl.com)"
    url: "https://introl.com/blog/inference-time-scaling-research-reasoning-models-december-2025"
  - label: "Yi Tay sur le scaling de la recherche IA"
    url: "https://x.com/YiTayML/status/1943392226689929618"
  - label: "Scaling laws multi-agents"
    url: "https://x.com/omarsar0/status/2001321178095382706"
---

Pendant des années, la règle était simple : plus de paramètres, plus de tokens, plus de FLOPs = meilleur modèle. Les lois de scaling de Kaplan et Chinchilla étaient la bible. En 2025-2026, cette équation ne tient plus. Un doublement des performances demande parfois un quintuple du compute, et certains runs massifs de 2025 n'ont pas significativement battu les modèles précédents malgré des ressources colossales.

Le scaling a changé de dimension. Voici les cinq axes qui remplacent la course aux paramètres denses.

## 1. Le compute d'inférence : le « temps de réflexion »

Lancé par OpenAI avec o1 fin 2024, le test-time compute scaling est devenu standard. Les modèles intègrent des routeurs qui allouent dynamiquement entre une réponse rapide et un mode « réflexion profonde » : chain-of-thought étendu, recherche, vérification, utilisation d'outils.

Les lois de scaling classiques ont été étendues pour inclure les FLOPs d'inférence et les tokens de « réflexion », avec un coût 5 à 10 fois plus élevé pour les tâches difficiles — mais des gains disproportionnés là où le pretraining avait atteint un plateau. GPT-5, Claude 4.x, Gemini 2.5 et Grok 4 Heavy intègrent tous cette approche hybride.

## 2. Le scaling de la recherche automatisée

Yi Tay de DeepMind a formulé le concept : 2025, c'est l'année où on scale les **systèmes d'IA qui font de la recherche en IA**. Génération de données synthétiques, proposition d'hypothèses, conception d'architectures, optimisation d'hyperparamètres, exécution d'expériences, itération récursive.

Concrètement : des modèles pilotent des laboratoires robotiques physiques, proposent et exécutent des milliers d'expériences, découvrent des réactions négligées, ferment la boucle avec des données réelles — pour une réduction de coûts d'environ 40 % dans certains domaines. Un modèle MiniCPM-5 de 1 milliard de paramètres a été entraîné avec une infrastructure largement générée par IA.

## 3. Les « sociétés de modèles » — scaling multi-agents

Le prochain frontier dépasse le modèle unique pour aller vers des populations d'agents. Un papier conceptuel de fin 2025 propose d'étendre les lois de scaling selon trois nouveaux axes :

- **Population** : nombre et diversité des agents
- **Organisation** : topologies de connexion, spécialisation, division du travail
- **Institution** : normes, mémoire persistante, artefacts partagés, objectifs collectifs

Les swarms naïfs échouent souvent à cause de l'effet de troupeau ou des chambres d'écho. Le succès exige des régimes délibérés : compétition (débat/self-play), collaboration (expertises complémentaires) ou coordination (hiérarchies de planificateurs).

## 4. Efficacité architecturale et sparsité

Le scaling dense brute-force cède la place à :

- **MoE extrême** : un modèle de 35B paramètres avec ~3B actifs surperforme un prédécesseur de 235B grâce à une attention hybride linéaire+standard, un training de router sur la qualité, et du RL en environnement simulé.
- **Attention sub-quadratique** : des contextes de 1 à 12 millions de tokens à 52x de vitesse et une fraction du coût, brisant le bottleneck O(n²) historique des transformers.
- **Designs inspirés du cerveau** : hiérarchiques, récurrents, compute adaptatif. Un modèle de 27M paramètres surperforme o3-mini en raisonnement.
- **Overtraining** : entraînement multi-epoch sur des données curées/synthétiques. Les nouvelles lois de scaling favorisent des modèles plus petits mais profondément entraînés.

## 5. La convergence et ce qui vient après

Les tiers se dessinent : modèles frontier de raisonnement (Claude/GPT-5/Gemini/Grok, souvent multimodaux avec raisonnement intégré), modèles open-source milieu de gamme (Llama 3/4, Mistral), et modèles edge efficaces (Phi, Gemma, MiniCPM) fonctionnant dans le navigateur ou sur CPU.

L'ingénierie des systèmes (orchestration, évaluation, optimisation du TCO) est devenue aussi importante que le pretraining. On observe une **évolution convergente** : les labs arrivent aux mêmes paradigmes « thinking model + router + tools », ce qui suggère que la recette transformer+scaling a maturé. La différenciation se joue désormais sur la distribution, les produits, les agents et l'intégration dans le monde réel.

## En résumé

2025-2026 marque la transition de l'ère du « modèle géant unique » vers des systèmes composés, efficaces, agentic et auto-accélérants. Les lois de scaling classiques ne sont pas jetées — elles sont augmentées, et parfois remplacées, par de nouvelles pour le compute d'inférence, la coordination multi-agents, l'automatisation de la recherche et les architectures optimisées.

La question n'est plus « combien de paramètres ? » mais « comment orchestrer intelligemment ? ».
