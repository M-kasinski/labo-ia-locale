---
title: "Agent Planning Benchmark : isoler le vrai talon d’Achille des agents IA"
description: "APB propose 4 209 cas multimodaux pour diagnostiquer la planification des agents LLM : décomposition, choix d’outils, robustesse au bruit, tâches impossibles et raffinements en cours d’inférence."
pubDate: 2026-06-09
category: "veille"
tags: ["agents", "benchmark", "planning", "tool-use", "research"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — Agent Planning Benchmark"
    url: "https://arxiv.org/abs/2606.04874"
  - label: "GitHub — AgentPlanningBenchmark"
    url: "https://github.com/Mikivishy/AgentPlanningBenchmark"
  - label: "PDF — Agent Planning Benchmark"
    url: "https://arxiv.org/pdf/2606.04874"
---

Les benchmarks d’agents mesurent souvent le résultat final : la tâche est-elle réussie, oui ou non ? C’est utile, mais incomplet. Quand un agent échoue, on ne sait pas toujours s’il a mal planifié, mal choisi un outil, mal exécuté une étape, mal interprété un retour, ou s’il aurait dû refuser une tâche impossible. **Agent Planning Benchmark (APB)**, révisé sur arXiv le **5 juin 2026**, attaque précisément cette zone floue : diagnostiquer la **planification** avant de juger toute la chaîne agentique.

Le papier **“Agent Planning Benchmark: A Diagnostic Framework for Planning Capabilities in LLM Agents”** introduit un benchmark de **4 209 cas multimodaux**, couvrant **22 domaines** et **cinq settings**. Les auteurs évaluent **12 MLLMs** et ciblent plusieurs dimensions : planification holistique, planification étape par étape conditionnée par feedback, robustesse aux outils inutiles, robustesse aux outils cassés, et gestion des tâches insolubles.

La proposition est simple, donc dangereusement pertinente : avant de demander si un agent “réussit”, demandons s’il sait construire un plan qui mérite d’être exécuté.

## Le problème des scores end-to-end

Un score end-to-end mélange tout. Si un agent rate une réservation, une analyse de tableur ou une correction de code, l’échec peut venir de plusieurs couches. Peut-être que le modèle a mal compris l’objectif. Peut-être que le plan était bon mais l’outil a échoué. Peut-être que l’environnement a renvoyé une observation ambiguë. Peut-être que l’agent aurait dû s’arrêter au lieu d’insister.

Cette confusion est un vrai problème pour l’ingénierie. Optimiser un agent sans savoir où il casse revient à réparer une voiture en changeant successivement le moteur, les pneus et l’autoradio. On finit parfois par régler le problème, mais la méthode manque d’élégance. Et d’élégance, certes, les benchmarks n’ont pas besoin ; de diagnostic, oui.

APB se positionne comme un **complément upstream** aux benchmarks d’exécution. Il ne remplace pas les tests en environnement réel. Il cherche à mesurer une compétence préalable : la capacité à décomposer un but, sélectionner les outils pertinents, intégrer des contraintes, réagir à du feedback et reconnaître l’impossible.

## Cinq settings pour tester la planification

Le premier setting est la **planification holistique**. L’agent doit produire un plan global avant l’action. C’est la forme classique : comprendre l’objectif, ordonner les étapes, prévoir les dépendances.

Le deuxième est la **planification step-wise conditionnée par feedback**. Ici, le plan doit évoluer avec les retours. C’est plus proche des agents réels : un outil répond mal, une contrainte apparaît, une hypothèse tombe, et le plan doit être ajusté sans repartir dans le décor.

Le troisième setting teste la robustesse face à des **outils extraneous**, c’est-à-dire des outils présents mais inutiles. Ce point est plus important qu’il n’y paraît. Dans les environnements MCP ou tool-use modernes, un agent peut voir une longue liste d’outils. Le vrai problème n’est pas seulement de savoir appeler un outil, mais de savoir ignorer les mauvais.

Le quatrième setting introduit des **outils cassés**. Un agent fiable doit détecter qu’un outil ne fonctionne pas ou ne convient plus, puis adapter sa stratégie. Beaucoup de démos agentiques supposent des outils dociles. Le monde réel, lui, a des APIs qui expirent, des schémas qui changent et des erreurs 500 qui arrivent avec le timing d’un métronome sadique.

Le cinquième setting concerne les **tâches insolubles**. C’est probablement le plus révélateur. Un agent utile ne doit pas seulement réussir ; il doit savoir refuser, demander une contrainte manquante, ou expliquer pourquoi la tâche est impossible. La “calibrated refusal” est une capacité de sécurité et de qualité, pas une coquetterie de produit.

## Les faiblesses observées

D’après l’abstract, APB met en évidence des faiblesses systématiques chez les 12 modèles multimodaux évalués : **planification longue**, robustesse au bruit d’outils, refus calibré et raffinement en cours d’inférence. Ce sont exactement les points où les agents actuels donnent souvent une impression de compétence intermittente.

La planification longue reste difficile parce qu’elle demande de maintenir des dépendances sur plusieurs étapes. La robustesse au bruit d’outils exige une forme de discipline : ne pas se laisser distraire par une capacité disponible mais non pertinente. Le refus calibré suppose d’estimer ses propres limites et celles de l’environnement. Quant au raffinement en cours d’inférence, il demande de transformer le feedback en correction utile, plutôt qu’en boucle de justification.

Ce diagnostic rejoint une tendance plus large : les agents ne sont pas seulement limités par le modèle de base. Ils sont limités par la qualité de leur **scaffold** — prompts, mémoire, outils, policies de retry, vérification, critères d’arrêt. APB tente d’isoler une partie de ce scaffold : le plan.

## Validation sur ToolSandbox et tau2-bench

Les auteurs ne s’arrêtent pas à APB. Ils indiquent valider le benchmark sur **200 tâches ToolSandbox** et **200 tâches tau2-bench**. Selon l’abstract, un raffinement guidé par APB améliore la correction du plan, la note du plan et des métriques d’exécution downstream sur trois modèles représentatifs.

Il faut rester prudent : l’ampleur exacte des gains dépendra des détails expérimentaux, et la généralisation devra être confirmée par d’autres équipes. Mais l’idée est solide. Si une métrique de planification prédit ou améliore partiellement l’exécution réelle, elle devient utile pour développer des agents. On peut alors détecter des régressions plus tôt, comparer des scaffolds, et comprendre pourquoi une amélioration de modèle ne se traduit pas toujours en meilleur comportement agentique.

## Pourquoi cela compte pour les agents MCP et coding assistants

Les agents modernes vivent dans des environnements de plus en plus riches : navigateurs, terminaux, fichiers, bases de données, APIs, serveurs MCP, outils internes. Cette richesse améliore le plafond de performance, mais augmente aussi la surface d’erreur. Plus l’agent voit d’options, plus la planification devient critique.

Dans un coding assistant, par exemple, un mauvais plan peut lancer des modifications trop larges, ignorer les tests pertinents, utiliser un outil de recherche au mauvais moment, ou persister sur une hypothèse fausse. Dans un agent d’entreprise, un mauvais plan peut appeler la mauvaise source de données, confondre un brouillon et une action irréversible, ou continuer une tâche malgré une permission manquante.

APB est donc intéressant parce qu’il parle à l’ingénierie quotidienne, pas seulement aux leaderboards. Les équipes qui déploient des agents ont besoin de savoir si un changement de prompt améliore réellement la planification, si un nouveau modèle gère mieux les outils cassés, ou si l’ajout de capacités rend l’agent plus distrait.

## Ce qu’il faut retenir

Agent Planning Benchmark met le doigt sur une faiblesse structurelle des évaluations agentiques : on mesure trop souvent le succès final sans diagnostiquer le plan. Avec 4 209 cas multimodaux, 22 domaines et cinq settings, APB propose une grille plus fine pour comprendre où les agents échouent avant même d’agir.

La promesse n’est pas de remplacer les benchmarks d’exécution. Elle est de les rendre moins opaques. Si les agents doivent devenir fiables, ils devront savoir planifier, ignorer les outils inutiles, contourner les outils cassés et reconnaître les tâches impossibles. Autrement dit : moins foncer avec assurance, plus réfléchir avant d’appuyer sur tous les boutons. Révolution discrète, mais bienvenue.

## Sources

- arXiv — Agent Planning Benchmark : https://arxiv.org/abs/2606.04874
- GitHub — AgentPlanningBenchmark : https://github.com/Mikivishy/AgentPlanningBenchmark
- PDF — Agent Planning Benchmark : https://arxiv.org/pdf/2606.04874
