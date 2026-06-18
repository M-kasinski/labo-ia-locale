---
title: "Anthropic ouvre le dossier qui fâche : quand Claude accélère la construction de Claude"
description: "Anthropic publie des données internes sur l’IA qui contribue déjà au développement de futurs modèles, et remet la question de l’auto-amélioration récursive au centre du débat."
pubDate: 2026-06-05
category: "veille"
tags: ["anthropic", "claude", "gouvernance", "agents", "recherche"]
author: "Veille IA"
draft: false
sources:
  - label: "Anthropic Institute — When AI builds itself"
    url: "https://www.anthropic.com/institute/recursive-self-improvement"
  - label: "The Online Citizen — Anthropic urges global AI pause as self-improving systems edge closer"
    url: "https://theonlinecitizen.com/2026/06/05/anthropic-urges-global-ai-pause-as-self-improving-systems-edge-closer-to-autonomous-development"
  - label: "METR — Measuring AI ability to complete long tasks"
    url: "https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/"
---

Anthropic vient de publier un texte qui mérite mieux qu’un titre anxiogène. Dans **“When AI builds itself”**, l’Anthropic Institute ne dit pas que l’auto-amélioration récursive est arrivée. Il dit quelque chose de plus précis, et probablement plus important : les systèmes d’IA participent déjà à une part croissante du travail qui sert à construire les prochains systèmes d’IA. Si cette tendance continue, l’industrie pourrait se retrouver avec des modèles capables de concevoir, coder, tester et entraîner leurs successeurs avec une intervention humaine de plus en plus marginale.

Le sujet est délicat parce qu’il se situe entre deux mauvais réflexes : le rejet immédiat façon science-fiction, et l’emballage marketing façon “regardez comme notre modèle est magique”. Ici, le document d’Anthropic est intéressant justement parce qu’il mélange données internes, prudence méthodologique et implications de gouvernance. Ce n’est pas une preuve que Claude se réécrit tout seul dans une cave avec une musique dramatique. C’est un signal que la boucle de développement de l’IA devient de moins en moins strictement humaine.

## Ce qu’Anthropic affirme réellement

Le cœur de l’argument est simple : historiquement, les humains écrivaient le code, lançaient les expériences, interprétaient les résultats et décidaient quoi tester ensuite. Aujourd’hui, chez Anthropic, Claude intervient déjà dans plusieurs de ces étapes. L’entreprise indique que ses ingénieurs produisent en moyenne **huit fois plus de code par trimestre** qu’entre 2021 et 2025, et que, **en mai 2026, plus de 80 % du code fusionné dans ses systèmes de production était rédigé par Claude**.

Ces chiffres doivent être lus correctement. “Rédigé par Claude” ne veut pas dire “conçu, validé et assumé sans humain”. Dans un workflow moderne, un agent peut générer un patch, modifier plusieurs fichiers, écrire des tests, relancer une commande, puis demander une revue. Le jugement final, l’intégration et la responsabilité restent humains — du moins dans l’état décrit par Anthropic. Mais l’écriture concrète du logiciel, elle, est déjà massivement déléguée.

Anthropic sépare aussi deux niveaux : l’**engineering** et la **recherche**. Le premier recouvre le code, l’infrastructure, le diagnostic de pannes, l’automatisation. Le second est plus subtil : choisir les expériences, interpréter des signaux faibles, décider quelle piste abandonner, formuler une hypothèse. C’est là que la question devient plus sérieuse. Une IA qui code vite est utile. Une IA qui choisit de bonnes expériences pour améliorer une IA commence à modifier la dynamique de la recherche elle-même.

## Le benchmark des 52x : impressionnant, mais cadré

Le chiffre qui va circuler est celui-ci : sur une tâche d’optimisation de code servant à entraîner un petit modèle, Claude Opus 4 atteignait environ **3x** de speedup en mai 2025 ; en avril 2026, **Claude Mythos Preview** atteignait environ **52x**, selon Anthropic. La tâche est conçue comme une mini-boucle de recherche expérimentale : réécrire du code, l’exécuter, mesurer, recommencer.

C’est un résultat frappant, parce qu’il combine code, expérimentation et itération. Anthropic précise qu’un chercheur humain compétent aurait besoin de plusieurs heures pour atteindre environ 4x dans ce cadre. Sur ce segment précis, le modèle n’est donc pas seulement un assistant de complétion : il exécute une boucle d’amélioration technique.

Il faut toutefois éviter une extrapolation trop facile. Une optimisation de code dans un cadre fixé à l’avance n’est pas équivalente à “inventer le prochain paradigme de modèle”. Le benchmark fixe l’objectif, les métriques et l’environnement. Claude cherche dans l’espace des optimisations possibles ; il ne redéfinit pas le programme de recherche. Mais c’est exactement ce qui rend le signal crédible : Anthropic ne prétend pas que la recherche est résolue, seulement que certaines sous-boucles deviennent très automatisables.

## La question du “research taste”

La partie la plus intéressante du texte concerne le jugement de recherche, parfois appelé “research taste”. Anthropic décrit une évaluation interne où les modèles sont confrontés à des moments réels de recherche dans lesquels un humain avait pris une direction perfectible. Le modèle doit proposer la suite. Selon Anthropic, sur cet ensemble de **129 moments**, le meilleur modèle de novembre 2025, Opus 4.5, battait le choix humain **51 %** du temps ; en avril 2026, Mythos Preview montait à **64 %**.

La nuance est essentielle : Anthropic reconnaît que l’échantillon n’est pas une comparaison générale humain contre modèle, puisqu’il a été constitué à partir de situations où le choix humain avait justement de la marge d’amélioration. Ce n’est donc pas un “Claude est meilleur que les chercheurs”. C’est plutôt : dans des moments difficiles mais identifiés comme perfectibles, le modèle devient de plus en plus capable de proposer une meilleure continuation.

Pour une équipe de recherche, c’est déjà beaucoup. Le travail scientifique est une succession de micro-décisions : quelle ablation lancer, quel bug suspecter, quelle hypothèse abandonner, quelle métrique croire. Si les modèles deviennent bons sur ces décisions locales, ils peuvent accélérer fortement la recherche sans être “autonomes” au sens fort.

## Le rôle des horizons de tâche

Anthropic s’appuie aussi sur les travaux de METR sur les **horizons de tâche** : la durée des tâches humaines que les modèles peuvent accomplir de manière fiable. METR a mesuré une croissance rapide de ces horizons, avec des tâches passées de quelques minutes à plusieurs heures, puis jusqu’à des tâches beaucoup plus longues pour les modèles les plus récents. Anthropic cite notamment l’idée que ces horizons doublent désormais à un rythme de l’ordre de quelques mois.

Là encore, ce n’est pas une boule de cristal. Les benchmarks peuvent saturer, les tâches peuvent être mal représentatives, et le passage de “12 heures dans un environnement mesuré” à “deux semaines de recherche ouverte” n’est pas automatique. Mais la direction est claire : plus l’horizon s’allonge, plus les agents peuvent prendre en charge des boucles complètes — pas seulement des fragments.

C’est précisément ce qui rend la notion d’auto-amélioration récursive moins fantaisiste. Il n’est pas nécessaire qu’un modèle comprenne toute la chaîne du premier coup. Il suffit qu’il absorbe progressivement les maillons : coder, tester, diagnostiquer, optimiser, proposer des expériences, comparer des résultats, orchestrer d’autres agents.

## Gouvernance : le passage obligé, pas le décor

Anthropic va plus loin et défend l’idée qu’il faudrait disposer d’un mécanisme international permettant de **ralentir ou suspendre temporairement** le développement frontier si les risques dépassent les capacités de contrôle. The Online Citizen rapporte que l’entreprise insiste sur la nécessité d’une coordination globale, notamment parce qu’une pause unilatérale serait fragile face aux pressions commerciales et géopolitiques.

C’est la partie la plus politique du dossier, et probablement la plus contestée. Vérifier une pause sur des entraînements de frontier models est difficile : les GPU sont généralistes, les runs peuvent être distribués, les incitations à contourner les règles sont fortes. Anthropic le reconnaît implicitement en parlant de mécanismes vérifiables et coordonnés. Autrement dit : un bouton pause sans vérification serait surtout un bouton placebo.

## Pourquoi c’est important

Ce texte compte parce qu’il déplace le débat. La question n’est plus seulement “quel modèle a le meilleur score ?”, mais “quelle fraction de la prochaine génération de modèles est déjà produite par la génération actuelle ?”. C’est une métrique beaucoup plus structurante.

Si l’IA accélère sa propre R&D, les courbes de progrès peuvent changer de régime. Pas forcément vers une explosion incontrôlée ; les goulets d’étranglement restent nombreux : compute, données, alignement, ingénierie de clusters, validation scientifique, organisation humaine. Mais l’hypothèse d’un simple progrès linéaire piloté par des humains devient moins confortable.

La lecture sobre est donc la suivante : Anthropic ne prouve pas l’arrivée de l’auto-amélioration récursive. Il documente les premières briques d’une boucle où les modèles participent au développement de modèles meilleurs. C’est déjà suffisant pour mériter une attention sérieuse. Les machines ne construisent pas encore seules leurs successeurs. Mais elles tiennent de plus en plus souvent la clé de 12, et elles commencent à lire le plan.

## Sources

- [Anthropic Institute — When AI builds itself](https://www.anthropic.com/institute/recursive-self-improvement)
- [The Online Citizen — Anthropic urges global AI pause as self-improving systems edge closer](https://theonlinecitizen.com/2026/06/05/anthropic-urges-global-ai-pause-as-self-improving-systems-edge-closer-to-autonomous-development)
- [METR — Measuring AI ability to complete long tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)
