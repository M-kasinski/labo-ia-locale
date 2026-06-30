---
title: "llama.cpp b9843 : retour arrière sur le split compute, et c’est plutôt sain"
description: "La release b9843 de llama.cpp annule une optimisation de synchronisation sur le chemin split compute. Un correctif de stabilité qui rappelle qu’un bon rollback vaut mieux qu’une micro-révolution bancale."
pubDate: 2026-06-30
tags: ["llama-cpp", "scheduling", "stabilité", "gguf", "inférence locale"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "GitHub Releases — llama.cpp b9843"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9843"
  - label: "GitHub PR #25138 — revert sched : reintroduce less synchronizations during split compute"
    url: "https://github.com/ggml-org/llama.cpp/pull/25138"
---

## La nouvelle

**llama.cpp b9843** a été publié le **30 juin 2026 à 01:17 UTC**. Le changement principal n’ajoute pas une nouvelle fonctionnalité spectaculaire : il **revert** le commit qui avait réintroduit moins de synchronisations pendant le **split compute**.

En clair : l’équipe préfère revenir à un état plus robuste plutôt que laisser une optimisation de scheduling se promener avec des effets de bord. C’est moins sexy qu’un nouveau backend, mais nettement plus utile quand tu fais tourner des modèles lourds sans envie d’aller jouer au pompiers.

## Analyse technique

### Ce que le revert corrige

Le commit annulé venait du PR **#20793** et concernait la gestion des synchronisations pendant le split compute.

Le split compute sert à mieux répartir le calcul entre plusieurs étapes ou unités d’exécution. Quand on touche à la synchronisation dans cette zone, on joue directement avec :

- l’ordonnancement des kernels,
- la stabilité des exécutions parallèles,
- la latence réelle observée sous charge,
- et le risque de régression silencieuse.

Le message du revert est assez clair : la version précédente a probablement trop dégradé un équilibre déjà fragile. Dans ce genre de code, une “optimisation” qui casse la cohérence est une dette, pas un gain.

### Pourquoi c’est important pour les usages locaux

llama.cpp reste le moteur qu’on utilise quand on veut :

- du **GGUF**,
- des exécutions **offline**,
- des déploiements sur **CPU**, **Apple Silicon**, **CUDA**, **ROCm**, **Vulkan** ou **SYCL**,
- et surtout un comportement prévisible sur du matériel réel, pas dans une démo marketing.

Un revert de scheduling peut donc avoir plus d’impact qu’une longue liste de petites features. Si tu sers un modèle avec des charges irrégulières, des batchs variables ou du multi-backend, la priorité n’est pas “aller 2 % plus vite sur un microbench”. La priorité, c’est **ne pas casser la trajectoire d’inférence**.

### Ce que dit la release sur le projet

La release b9843 n’essaie pas de vendre du rêve. Elle fait l’inverse : elle admet qu’une optimisation récente mérite d’être retirée.

C’est un bon signal pour l’écosystème llama.cpp :

- les régressions sont corrigées vite,
- les releases continuent d’être signées et publiées proprement,
- les binaires restent fournis sur une large matrice de plateformes,
- et le projet garde une discipline d’ingénierie très “no bullshit”.

## Impact concret

### Pour les gens qui déploient en local

Si tu utilises llama.cpp comme :

- serveur OpenAI-compatible,
- runtime pour agents locaux,
- moteur GGUF sur machine grand public,
- ou brique d’inférence dans un pipeline plus large,

ce genre de release compte surtout pour une chose : **réduire le risque**.

Ce n’est pas une release pour tester une nouvelle idée. C’est une release pour remettre le moteur dans une zone saine.

### Pour les mainteneurs de stacks plus complexes

Les environnements avec :

- plusieurs GPU,
- du split compute,
- des modèles lourds,
- des backends hétérogènes,

sont précisément ceux où une modification de synchronisation peut devenir pénible à diagnostiquer. Le revert évite de faire traîner un bug perf/stabilité dont le coût humain serait supérieur au gain théorique.

## Limites et lecture honnête

Il n’y a **pas** de nouveau benchmark public dans cette release.

Il n’y a **pas** non plus de nouvelle capacité modèle à annoncer.

Donc il faut lire b9843 pour ce qu’elle est : **une correction de trajectoire**, pas une rupture produit. Et franchement, c’est sain. Les projets sérieux savent parfois reculer d’un pas pour éviter de tomber dans le ravin.

## En bref

- **Date de release :** 30 juin 2026
- **Changement central :** revert du split compute plus agressif
- **Effet attendu :** plus de stabilité, moins de régressions
- **Lecture produit :** entretien technique du moteur, pas feature marketing

## Sources vérifiées

- [GitHub Releases — llama.cpp b9843](https://github.com/ggml-org/llama.cpp/releases/tag/b9843)
- [PR #25138 — revert sched : reintroduce less synchronizations during split compute](https://github.com/ggml-org/llama.cpp/pull/25138)
