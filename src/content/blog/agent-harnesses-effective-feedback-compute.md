---
title: "Agents IA : un papier propose de mesurer le feedback utile, pas les tokens brûlés"
description: "Une étude arXiv introduit l’Effective Feedback Compute, une métrique pour expliquer pourquoi certains harnesses d’agents progressent mieux que d’autres à budget égal."
pubDate: 2026-06-04
category: "veille"
tags: ["agents", "scaling-laws", "benchmarks", "research", "tool-use"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — Scaling Laws for Agent Harnesses via Effective Feedback Compute"
    url: "https://arxiv.org/abs/2605.29682"
  - label: "arXiv HTML — Scaling Laws for Agent Harnesses via Effective Feedback Compute"
    url: "https://arxiv.org/html/2605.29682v1"
  - label: "alphaXiv — audio summary and discussion"
    url: "https://www.alphaxiv.org/audio/2605.29682"
---

Un papier arXiv publié le **28 mai 2026** s’attaque à une question très concrète pour les agents IA : qu’est-ce qui scale vraiment quand on ajoute des outils, de la mémoire, des boucles de vérification et davantage de budget d’inférence ? Pas seulement les tokens. Pas seulement les appels outils. Selon les auteurs de **“Scaling Laws for Agent Harnesses via Effective Feedback Compute”**, la variable utile est plutôt la quantité de feedback réellement exploitable produite pendant la trajectoire de l’agent.

Le papier, signé par Xuanliang Zhang, Dingzirui Wang, Keyan Xu, Qingfu Zhu et Wanxiang Che, introduit une métrique appelée **Effective Feedback Compute** ou **EFC**. L’idée est simple à formuler, moins simple à mesurer : un agent ne progresse pas parce qu’il dépense plus, mais parce que ses interactions avec l’environnement lui apportent des informations valides, nouvelles, pertinentes et effectivement retenues pour la suite. Une boucle d’agent peut brûler 200 000 tokens et tourner en rond avec beaucoup d’élégance. L’élégance, hélas, ne corrige pas les bugs.

## Le problème : le compute brut confond activité et progrès

Dans les discussions sur le test-time scaling, on mesure souvent le coût par des variables faciles à compter : nombre de tokens, nombre d’appels outils, opérations, temps mur, coût en dollars. Pour un chatbot classique, ces métriques donnent déjà une approximation imparfaite. Pour un agent outillé, elles deviennent franchement trompeuses.

Deux trajectoires peuvent avoir le même budget brut et produire des résultats très différents. Dans une tâche de debugging, un agent peut lancer cinquante commandes presque identiques, recevoir cinquante erreurs redondantes, puis échouer. Un autre peut faire cinq appels bien choisis, lire un résultat de test, modifier son hypothèse et converger. Les deux ont “consommé” du compute ; seul le second a converti ce compute en information utile.

C’est ce que le papier formalise. Un **agent harness** désigne ici l’enveloppe système autour du modèle : routage d’outils, feedback, vérification d’états intermédiaires, mémoire, révision de solution, règles d’arrêt. Autrement dit, tout ce qui transforme un LLM en agent opérationnel. Les auteurs soutiennent que la performance de ce harness ne se comprend pas via la dépense brute, mais via sa capacité à convertir cette dépense en feedback durable et suffisant pour la tâche.

## EFC : quatre critères pour créditer un feedback

L’EFC crédite un événement de feedback seulement s’il satisfait quatre dimensions : **informativeness**, **validity**, **non-redundant relevance** et **memory update**. En français : l’observation doit apporter une information nouvelle et utile, être fiable, ne pas simplement répéter ce que l’agent sait déjà, et modifier ensuite le plan, la mémoire, l’état ou la solution de l’agent.

Dans la formulation du papier, chaque événement reçoit quatre facteurs bornés entre 0 et 1 : `I_t`, `V_t`, `R_t` et `M_t`. La contribution est multiplicative : `EFC_t = κ I_t V_t R_t M_t`, avec `κ = 10` dans l’implémentation décrite. Ce choix est important. Si un feedback est informatif mais invalide, ou valide mais jamais retenu, sa contribution s’effondre. Le produit force une lecture “goulot d’étranglement” : pour compter, le feedback doit être utile de bout en bout.

Le papier définit ensuite un EFC de trajectoire en sommant ces contributions, puis une normalisation par la demande de la tâche, notée **EFC / D_task**. Cette normalisation vise à comparer des tâches qui ne nécessitent pas le même volume d’information. Corriger une faute de syntaxe et résoudre un incident Kubernetes multi-service n’ont pas la même demande de feedback ; les mettre sur la même échelle brute serait confortable, donc probablement faux.

## Des résultats qui attaquent directement les métriques paresseuses

Les chiffres rapportés par les auteurs sont nets. Sur des expériences contrôlées, les tokens et les appels outils expliquent peu de variance : respectivement **R² = 0,33** et **0,42**. Une baseline multivariée plus forte, appelée **SAS**, atteint **0,88**. Les variantes Oracle-EFC et Estimated-EFC montent à **0,94**, et **Oracle-EFC / D_task** atteint **0,99** dans ce cadre contrôlé.

Le papier rapporte aussi une intervention à budget fixé : améliorer la qualité du feedback fait passer le succès de **0,27** à **0,90**, alors que le coût brut et le nombre d’appels outils restent constants. C’est probablement le résultat le plus parlant pour les praticiens. Si le budget ne change pas mais que la qualité de feedback change, et que le taux de succès explose, compter seulement les tokens revient à regarder le compteur kilométrique pour diagnostiquer un moteur.

Sur des traces réelles mixtes, la métrique **NRS-EFC / D_task** atteint **R² = 0,92**, tandis que le compute brut a un ajustement proche de zéro ou négatif. Dans une validation prospective, elle reste le meilleur prédicteur avec **R² = 0,85**. Ces chiffres viennent du papier et devront être reproduits, mais ils donnent une direction claire : les benchmarks d’agents doivent instrumenter la qualité des boucles de feedback, pas seulement leur volume.

## Pourquoi c’est utile pour les agents de code et MCP

Cette proposition arrive au bon moment. Les agents de code, les workflows MCP, les assistants capables de lire des fichiers, lancer des tests, ouvrir des tickets et modifier des dépôts sont en train de se multiplier. Mais beaucoup de systèmes restent évalués avec des métriques grossières : coût total, nombre d’étapes, réussite finale. Cela donne peu d’indications sur la cause d’un échec.

EFC pousse à poser de meilleures questions. L’agent reçoit-il des observations fiables ? Les résultats de tests sont-ils lus et intégrés ? La mémoire garde-t-elle les contraintes importantes ? Le harness évite-t-il de répéter les mêmes erreurs ? Les outils sont-ils appelés au bon moment ou parce que le modèle panique en silence ? Pour concevoir un agent robuste, ces questions valent plus qu’une courbe “tokens versus score”.

La métrique peut aussi aider à comparer des architectures. Un agent avec vérification, mémoire compacte et bons critères d’arrêt peut consommer moins qu’un agent bavard tout en générant davantage d’EFC. À l’inverse, un système très sophistiqué sur le papier peut perdre si ses observations ne changent jamais ses décisions. Le papier met donc le projecteur sur le harness, pas uniquement sur le modèle de base.

## Les limites : mesurer l’utile n’est jamais gratuit

Il y a tout de même un point délicat : l’EFC est beaucoup plus riche qu’un compteur de tokens, donc plus difficile à mesurer. Les auteurs distinguent **Oracle-EFC**, utilisable dans des tâches synthétiques où l’état caché et le progrès réel sont connus, **Estimated-EFC**, construit à partir de caractéristiques observables dans les traces, et **NRS-EFC** pour les traces réelles plus bruitées. C’est raisonnable, mais cela introduit de nouveaux choix méthodologiques : quels signaux de trace retient-on, comment les pondère-t-on, et à quel point ces estimateurs généralisent-ils hors des benchmarks utilisés ?

Autre prudence : le papier est une prépublication arXiv. Il propose un cadre intéressant, pas une loi naturelle gravée dans le silicium. Les résultats sont prometteurs, mais il faudra voir comment EFC se comporte sur des agents multimodaux, des environnements longs, des interactions humaines, des outils instables et des tâches où la réussite n’est pas binaire.

## Ce qu’il faut retenir

L’intérêt du papier est de déplacer la conversation. Pour les agents IA, “plus de compute” n’est pas une stratégie si ce compute produit du bruit, des répétitions ou des observations ignorées. Le bon objet de scaling est la boucle perception-action-mémoire : ce que l’agent apprend, vérifie, conserve et réutilise.

Si l’EFC se confirme, il pourrait devenir un outil pratique pour auditer les agents : moins une métrique marketing qu’un diagnostic de plomberie. Et dans les systèmes agentiques, la plomberie est souvent là que se cachent les vraies performances. Glamour ? Non. Décisif ? Très probablement.

## Sources

- arXiv — Scaling Laws for Agent Harnesses via Effective Feedback Compute: https://arxiv.org/abs/2605.29682
- arXiv HTML — version expérimentale: https://arxiv.org/html/2605.29682v1
- alphaXiv — résumé audio et discussion: https://www.alphaxiv.org/audio/2605.29682
