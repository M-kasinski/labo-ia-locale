---
title: "Search-Time Contamination : quand les agents de recherche trouvent les réponses du benchmark"
description: "Un papier arXiv montre que les agents de deep research peuvent contaminer leurs propres évaluations en retrouvant sur le web les questions, métadonnées ou réponses des benchmarks publics."
pubDate: 2026-06-06
category: "veille"
tags: ["agents", "benchmark", "évaluation"]
author: "Veille IA"
draft: false
sources:
  - label: "Article arXiv Search-Time Contamination"
    url: "https://arxiv.org/abs/2606.05241"
  - label: "Version HTML du papier"
    url: "https://arxiv.org/html/2606.05241"
  - label: "Liste arXiv cs/new du 3 juin 2026"
    url: "https://arxiv.org/list/cs/new"
---

Les benchmarks publics ont longtemps eu un contrat implicite assez simple : on pose une question au modèle, il répond avec ce qu’il a appris pendant l’entraînement et ce qu’il sait raisonner au moment de l’inférence. Ce contrat est en train de casser. Les agents de **deep research** ne répondent plus seulement depuis leurs poids : ils cherchent, ouvrent des pages, citent des sources et construisent leur réponse avec le web sous la main.

Le papier **“Search-Time Contamination in Deep Research Agents”**, soumis sur arXiv le 3 juin 2026, met un nom sur ce nouveau problème : **Search-Time Contamination**, ou STC. L’idée est simple, et légèrement désagréable : un agent évalué sur un benchmark public peut retrouver pendant l’inférence des éléments du benchmark lui-même — métadonnées, contexte de question, voire réponse exacte — et améliorer son score sans vraiment démontrer la compétence que l’on croit mesurer.

Autrement dit, le benchmark devient une chasse au trésor indexée par Google. Élégant, mais pas très scientifique.

## La contamination ne vient plus seulement du pré-entraînement

Jusqu’ici, quand on parlait de contamination de benchmark, on pensait surtout au pré-entraînement : un modèle a peut-être vu des exemples de test dans son corpus, directement ou via des copies sur GitHub, forums, dumps web ou documents d’entraînement. Ce problème reste réel, mais il est statique : il concerne ce qui est déjà dans les poids du modèle.

La STC est différente. Elle se produit **au moment de l’évaluation**, parce que l’agent dispose d’un moteur de recherche ou d’un navigateur. Le papier distingue trois niveaux de gravité :

- **Benchmark Metadata Leakage** : l’agent récupère des informations sur le benchmark lui-même, sa structure ou son origine ;
- **Question-Context Leakage** : il retrouve du contexte fortement lié à une question précise ;
- **Explicit Answer Leakage** : il tombe directement sur la réponse ou une source qui la révèle clairement.

Le troisième cas est évidemment le plus toxique. Si l’agent lit la réponse en ligne, le score ne mesure plus le raisonnement : il mesure la capacité à retrouver une fuite. Pour un système de recherche, c’est presque une compétence ; pour un benchmark censé évaluer le raisonnement, c’est un court-circuit.

## Six benchmarks médicaux passés au crible

Les auteurs évaluent la STC sur six benchmarks publics, principalement médicaux et cliniques, avec des agents de recherche modernes. Le choix du domaine médical est pertinent : les questions y circulent souvent dans des banques d’examen, supports pédagogiques, dépôts de datasets, sites de révision ou pages miroir. Ce sont exactement les environnements où un agent web peut trouver des artefacts proches du benchmark.

Le résultat principal est prudent mais important : selon le papier, la STC est **répandue** et peut gonfler la performance mesurée **jusqu’à 4 %**. Ce chiffre n’a pas l’air spectaculaire à première vue. Mais dans un monde où des modèles se départagent parfois à quelques points, et où les communiqués transforment un delta marginal en révolution industrielle, 4 % peuvent suffire à fausser une comparaison.

Le papier rapporte aussi des cas beaucoup plus parlants. Sur un échantillon de 100 questions MedQA, **Gemini Deep Research** aurait visité des pages contenant explicitement la question et sa réponse dans **60 %** des cas. **Step Deep Research** serait à **9 %** sur le même échantillon. Pour **Valyu**, les auteurs indiquent **0 %** de fuite sur MedQA, mais une forte exposition sur PubMedQA, liée au recouvrement entre son corpus de recherche et la source du benchmark.

Ces chiffres doivent être lus comme des résultats de papier, pas comme un classement général des produits. Ils dépendent du protocole, de l’échantillon, de l’état du web et des systèmes testés au moment de l’expérience. Mais ils suffisent à montrer que le problème n’est pas théorique.

## Pourquoi les agents de recherche amplifient le problème

Un modèle de chat classique peut être contaminé, mais il ne peut pas aller vérifier une réponse en direct. Un agent de deep research, lui, est explicitement optimisé pour décomposer une question, chercher des indices, comparer des pages et citer des sources. C’est sa force en usage réel. C’est aussi ce qui rend les benchmarks publics fragiles.

Le papier insiste sur un point : la contamination peut changer la trajectoire de raisonnement. Lorsqu’une réponse explicite est retrouvée, l’agent peut converger plus vite vers cette réponse, même si sa trajectoire initiale allait ailleurs. Dans ce cas, la trace de recherche devient aussi importante que la réponse finale. Sans logs de navigation et sans inspection des sources consultées, on peut prendre une fuite pour une compétence.

Cela pose un problème particulier pour les évaluations “agentiques”. Plus un benchmark autorise d’outils, plus il ressemble au réel ; mais plus il autorise d’outils, plus il ouvre de canaux de fuite. Le vieux compromis entre réalisme et contrôle devient beaucoup plus brutal.

## Les mitigations : sandbox, logs et benchmarks moins exposés

Les auteurs proposent plusieurs garde-fous. Le premier est l’**isolation** : évaluer les agents dans des environnements de recherche contrôlés, où les pages accessibles ne contiennent pas les réponses ou les artefacts du benchmark. C’est propre, mais coûteux. Cela réduit aussi le réalisme si l’agent est censé opérer sur le web ouvert.

Deuxième piste : exiger des **trajectoires de recherche transparentes**. Un score sans trace de navigation devient insuffisant pour les agents web. Il faut savoir quelles requêtes ont été envoyées, quelles pages ont été ouvertes, et si l’agent a consulté une page contenant une fuite. Sans cette couche d’audit, le benchmark ressemble trop à une boîte noire avec connexion Internet.

Troisième piste : utiliser des jeux de test **privés, dynamiques ou contrôlés**, avec accès limité aux métadonnées et aux réponses. C’est déjà la direction prise par certains évaluateurs, mais elle a un coût : moins de reproductibilité publique, plus de dépendance à l’organisateur, et un risque de transformer les benchmarks en services fermés.

## Ce que ça change pour lire les scores

La conclusion pratique est simple : les scores d’agents de recherche sur benchmarks publics doivent être lus avec un niveau de scepticisme supérieur. Ce n’est pas une raison pour les jeter. C’est une raison pour demander : l’agent avait-il accès au web ? Les traces de recherche sont-elles disponibles ? Les questions sont-elles publiquement indexées ? Le benchmark mesure-t-il le raisonnement, la recherche documentaire, ou la capacité à retrouver une réponse déjà exposée ?

La nuance compte. Dans un usage réel, retrouver une information fiable en ligne est précisément ce qu’on attend d’un agent. Mais dans une évaluation de raisonnement, retrouver l’answer key est une fuite. Même outil, métrique différente.

Le papier ne détruit pas les benchmarks publics ; il rappelle qu’ils ont été conçus pour une époque où les modèles répondaient surtout depuis leurs poids. Les agents de deep research changent la surface d’évaluation. Si on garde les mêmes tests sans contrôler la recherche, on risque de mesurer la propreté de l’index web plutôt que l’intelligence du système.

## Sources

- [Search-Time Contamination in Deep Research Agents sur arXiv](https://arxiv.org/abs/2606.05241)
- [Version HTML du papier](https://arxiv.org/html/2606.05241)
- [Liste arXiv cs/new](https://arxiv.org/list/cs/new)
