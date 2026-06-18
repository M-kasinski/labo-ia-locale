---
title: "COLLEAGUE.SKILL : transformer l’expertise humaine en compétences inspectables pour agents"
description: "Un papier de Shanghai AI Lab propose de distiller documents, traces et feedbacks en packages de skills versionnés pour agents LLM — une alternative plus gouvernable aux prompts opaques."
pubDate: 2026-06-02
category: "veille"
tags: ["agents", "skills", "recherche", "workflows"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — COLLEAGUE.SKILL: Automated AI Skill Generation via Expert Knowledge Distillation"
    url: "https://arxiv.org/abs/2605.31264"
  - label: "Version HTML du papier COLLEAGUE.SKILL"
    url: "https://arxiv.org/html/2605.31264v1"
  - label: "Projet GitHub COLLEAGUE.SKILL"
    url: "https://github.com/titanwings/colleague-skill"
---

Les agents LLM ont un problème très banal : ils oublient mal, apprennent peu, et quand on les “personnalise”, on se retrouve souvent avec un prompt système de 300 lignes qui ressemble à une lettre au Père Noël technique. Le papier **COLLEAGUE.SKILL: Automated AI Skill Generation via Expert Knowledge Distillation**, soumis sur arXiv le 29 mai 2026 par Tianyi Zhou, Dongrui Liu, Leitao Yuan, Jing Shao et Xia Hu, propose une approche plus propre : transformer des traces d’expertise humaine en **packages de compétences inspectables, versionnés et corrigeables**.

L’idée n’est pas de cloner une personne. Les auteurs insistent sur un cadrage plus limité : distiller des pratiques, heuristiques, contraintes et styles d’interaction à partir de traces hétérogènes — documents, revues de code, conversations, décisions, écrits publics ou logs privés — pour produire une compétence qu’un agent peut charger et invoquer.

C’est une direction intéressante parce qu’elle déplace la personnalisation des agents depuis le folklore du prompt vers un artefact gouvernable. Oui, c’est moins magique. C’est précisément pour cela que c’est utile.

## Le problème : l’expertise est dans les traces, pas dans les prompts

Les agents actuels sont de plus en plus utilisés pour des tâches professionnelles longues : revue de code, analyse d’incident, rédaction technique, support interne, génération de plans d’action. Dans ces contextes, la compétence ne se résume pas à “sois expert en Kubernetes” ou “réponds comme un staff engineer”. Elle vit dans des exemples concrets : comment une personne arbitre entre deux risques, quelles erreurs elle surveille, quelles sources elle vérifie, quelles conventions elle applique, comment elle communique une incertitude.

Le papier part de ce constat : cette expertise existe, mais elle est dispersée. Elle se trouve dans des commentaires de pull request, des notes de postmortem, des échanges Slack, des décisions d’architecture, des guides internes. Les systèmes de mémoire capturent parfois des fragments. Les personas capturent parfois un style. Les frameworks de skills fournissent un format de packaging. Mais il manque, selon les auteurs, un workflow bout-en-bout qui transforme ces traces en compétence utilisable par un agent, tout en restant lisible et modifiable.

COLLEAGUE.SKILL formule donc le problème comme une question d’artefact : à partir d’un profil léger, d’un périmètre de sources et d’un ensemble de documents, produire un package de skill avec fichiers, métadonnées et état de cycle de vie.

## Deux pistes : capacité et comportement borné

Le système produit un package à deux “tracks”. Le premier est un **track de capacité** : pratiques, modèles mentaux, heuristiques de décision, méthodes de travail. C’est la partie “comment cette personne ou ce rôle résout un problème”.

Le second est un **track de comportement borné** : style de communication, règles d’interaction, limites d’usage, historique de corrections. C’est la partie “comment l’agent doit se comporter quand il mobilise cette compétence”, sans prétendre incarner complètement la personne source.

Cette séparation est saine. Beaucoup de personnalisations d’agents mélangent compétence et imitation : on veut récupérer le jugement d’un expert, et l’on se retrouve à simuler sa personnalité. COLLEAGUE.SKILL tente de découpler les deux. On peut charger un savoir-faire sans demander à l’agent de jouer quelqu’un. Le mot important est “bounded” : le comportement doit être borné par les sources et les contraintes explicites.

Le package généré est ensuite censé être **portable**, **inspectable**, **composable**, **corrigeable** et **gouvernable**. Ce vocabulaire paraît administratif, mais il touche au cœur du problème. Si une skill influence les décisions d’un agent, il faut pouvoir la lire, la modifier, la versionner, la retirer, la partager ou la limiter. Sinon, on obtient une mémoire opaque qui finit par gouverner l’agent sans être gouvernée elle-même. Ce qui est une manière très moderne de réinventer le classeur Excel critique, mais avec plus de tokens.

## Un workflow de distillation plutôt qu’une mémoire magique

Le pipeline décrit par les auteurs suit une logique assez directe : collecter les traces, les normaliser dans des répertoires de connaissance, analyser les éléments durables de compétence et de style, puis rendre le tout sous forme de Markdown structuré et de métadonnées.

Le système prévoit ensuite des opérations de cycle de vie : installation dans différents hôtes d’agents, invocation, correction en langage naturel, rollback et distribution optionnelle. Le papier mentionne des presets d’application, notamment pour des compétences de collègues, des personnalités publiques et des relations. Le dernier cas est évidemment plus sensible ; il montre aussi pourquoi les auteurs mettent autant l’accent sur la gouvernance, les limites et les disclaimers.

À la date du papier, le dépôt public revendique environ **18,5k étoiles GitHub**, une galerie de **215 skills**, **165 contributeurs**, et plus de **100k étoiles cumulées** sur les cartes de skills listées. Ces chiffres sont utiles pour mesurer une surface d’intérêt public, mais les auteurs reconnaissent qu’ils ne prouvent pas la qualité d’adoption, la fidélité comportementale ni l’impact sur des tâches tenues à l’écart.

C’est une distinction importante : popularité du format ne veut pas dire efficacité du système. La recherche agentique a déjà assez de “leaderboards” qui mesurent parfois le décor plus que la pièce.

## Ce que cela change pour les workflows agentiques

La promesse la plus concrète concerne les organisations qui veulent des agents spécialisés sans transformer chaque poste en prompt artisanal. Une équipe SRE pourrait distiller ses standards d’incident response. Une équipe sécurité pourrait formaliser ses réflexes de revue. Une rédaction technique pourrait capturer ses conventions d’explication, de citation et de vérification. Un agent de coding pourrait charger une skill de revue propre à un dépôt ou à une équipe.

L’intérêt n’est pas seulement de rendre l’agent “meilleur”. C’est de rendre son amélioration **auditable**. Quand un agent se trompe, on peut corriger la skill, conserver l’historique, revenir en arrière, ou limiter son périmètre. Cela rapproche les skills d’un artefact logiciel : versionné, relu, testé, déployé.

Ce mouvement s’inscrit dans une tendance plus large : les agents ne progressent pas seulement grâce à de meilleurs modèles, mais grâce à de meilleurs environnements. MCP standardise l’accès aux outils. Les harnesses de coding structurent les boucles d’action. Les systèmes de skills structurent le savoir procédural. Le modèle reste le moteur ; mais sans transmission, embrayage et frein, le moteur finit généralement dans le mur.

## Les limites : évaluation et consentement

Le papier est intéressant, mais il ne faut pas lui faire dire plus qu’il ne dit. COLLEAGUE.SKILL décrit un système et un contrat d’artefact ; il ne fournit pas, dans l’abstract et les éléments publics consultés, une preuve forte que les skills générées améliorent systématiquement les performances sur des benchmarks tenus à l’écart. Les auteurs reconnaissent d’ailleurs que les métriques publiques du dépôt et de la galerie ne démontrent pas la qualité comportementale.

Deuxième limite : le consentement et la source des traces. Distiller des documents publics d’un expert n’a pas le même statut que distiller des logs privés ou des conversations internes. Le système prévoit des métadonnées, des limites de source, des disclaimers et des décisions de partage, mais la gouvernance réelle dépendra de l’organisation qui l’utilise. Une mauvaise implémentation peut vite dériver vers une forme de “persona extraction” non consentie.

Troisième limite : la correction en langage naturel est séduisante, mais elle devra être testée sérieusement. Corriger une skill ne garantit pas que l’agent appliquera la correction dans tous les contextes. Il faudra probablement des tests de régression de skills, des jeux de cas, et des mécanismes d’évaluation comparables à ce que l’on fait déjà pour du code.

## Pourquoi surveiller ce papier

COLLEAGUE.SKILL mérite l’attention parce qu’il traite un angle souvent sous-estimé : la compétence d’un agent n’est pas seulement dans ses poids ni dans son contexte immédiat. Elle est aussi dans les artefacts qu’on lui donne à charger. Si ces artefacts sont lisibles, versionnés et corrigeables, on gagne un levier de contrôle. S’ils restent opaques, on déplace simplement le risque.

La prochaine étape sera de voir si ce type de package peut être évalué proprement : avant/après sur tâches professionnelles, robustesse aux corrections, conflits entre skills, sécurité des sources, et portabilité réelle entre hôtes. Mais la direction est saine. Les agents ont besoin de moins de mystique et de plus d’ingénierie documentaire. Ce n’est pas aussi vendeur qu’un robot qui clique partout, mais c’est probablement ce qui rendra les agents moins pénibles à vivre en production.
