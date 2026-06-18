---
title: "AsyncTool : les agents IA face au vrai poison des outils, la latence"
description: "AsyncTool et AsyncFC déplacent l’évaluation des agents vers un problème très concret : gérer plusieurs tâches et des appels d’outils qui ne répondent pas instantanément."
pubDate: 2026-05-31
category: "veille"
tags: ["agents", "benchmark", "tool-use", "recherche", "mcp"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — AsyncTool: Evaluating the Asynchronous Function Calling Capability under Multi-Task Scenarios"
    url: "https://arxiv.org/abs/2605.27995"
  - label: "OpenReview — AsyncTool submission ICLR 2026"
    url: "https://openreview.net/forum?id=FfedFHs6Tx"
  - label: "arXiv — Concurrency without Model Changes: Future-based Asynchronous Function Calling for LLMs"
    url: "https://arxiv.org/abs/2605.15077"
---

Les agents IA progressent vite sur les benchmarks de coding, de navigation et de tool-use. Mais beaucoup de ces évaluations gardent une hypothèse très confortable : l’agent travaille sur une tâche à la fois, appelle un outil, attend la réponse, puis continue. Dans le monde réel, c’est rarement aussi poli. Un test prend trente secondes, une recherche web arrive en retard, une API ralentit, un job CI bloque, et l’agent devrait pendant ce temps avancer sur autre chose sans perdre le fil.

C’est précisément le problème ciblé par **AsyncTool**, un nouveau benchmark publié sur arXiv le 27 mai 2026 puis révisé le 28 mai. Le papier, signé par Kou Shi, Ziao Zhang, Shiting Huang, Avery Nie, Zhen Fang, Qiuchen Wang, Lin Chen, Huaian Chen, Zehui Chen et Feng Zhao, évalue la capacité des agents LLM à faire du **tool calling asynchrone** dans des scénarios multi-tâches avec retours d’outils retardés. En clair : l’agent doit gérer plusieurs demandes en parallèle, lancer des outils, attendre certains résultats, basculer vers une autre tâche, puis reprendre correctement quand une réponse arrive.

Ce n’est pas un détail d’implémentation. C’est une des conditions minimales pour que les agents sortent du mode démo et deviennent des systèmes de production.

## Le benchmark manquant : la temporalité

Le constat du papier AsyncTool est simple : les benchmarks de tool-use actuels mesurent souvent la bonne capacité, mais dans un environnement trop propre. Ils testent si un modèle sait choisir un outil, produire les bons arguments, interpréter le retour et enchaîner. En revanche, ils négligent deux dimensions très courantes en production : la **latence** et la **concurrence**.

AsyncTool introduit donc des environnements interactifs où plusieurs tâches hétérogènes sont présentées simultanément. Chaque tâche peut comporter plusieurs étapes, avec des dépendances internes strictes. Les appels d’outils ne reviennent pas forcément immédiatement. L’agent doit utiliser les temps morts pour progresser ailleurs, tout en conservant l’état de chaque tâche.

C’est exactement le type de situation que l’on rencontre dans un assistant de développement : lancer une suite de tests, inspecter un autre fichier pendant l’exécution, attendre un retour de build, corriger un second bug, revenir au premier diagnostic. Même chose pour un agent d’entreprise connecté à des outils MCP : CRM, base documentaire, moteur de recherche interne, système de tickets, terminal, navigateur. L’enjeu n’est plus seulement « quel outil appeler ? », mais « que faire pendant que l’outil travaille ? ».

## Ce qu’AsyncTool mesure vraiment

D’après l’abstract arXiv et la page OpenReview, AsyncTool évalue les agents à trois niveaux : **Step Level**, **Sub-Task Level** et **Task Level**. Cette granularité est importante. Un agent peut réussir quelques appels unitaires mais échouer à terminer la tâche globale. Il peut aussi résoudre une sous-tâche tout en mélangeant les résultats entre deux files d’exécution.

Le benchmark ajoute aussi des métriques orientées efficacité. Ce point est bienvenu : en mode agentique, la qualité finale ne suffit pas. Un agent qui attend passivement chaque outil, sans jamais exploiter le parallélisme, peut finir par donner une bonne réponse mais rester inutilisable en pratique. À l’inverse, un agent trop agressif peut lancer des appels prématurés, ignorer des dépendances, ou halluciner un résultat qui n’est pas encore revenu.

Les auteurs indiquent que les retours d’outils retardés provoquent une dégradation claire des performances chez les agents actuels. Le papier insiste sur des modes d’échec assez prévisibles mais rarement mesurés proprement : perte d’état, mauvais suivi des dépendances, reprise au mauvais endroit, confusion entre tâches, et incapacité à coordonner les transitions pendant les périodes d’attente.

La nouveauté n’est donc pas seulement le benchmark. C’est le type d’erreur qu’il force à regarder.

## Pourquoi c’est plus dur qu’un simple appel parallèle

On pourrait croire que le problème se règle avec une file de futures, quelques promesses JavaScript et un orchestrateur. Ce serait trop simple, donc naturellement faux — ou au moins incomplet.

La difficulté est cognitive autant que système. L’agent doit comprendre qu’un résultat est indisponible, représenter ce manque sans l’inventer, décider quelles actions restent valides, puis réintégrer le résultat quand il arrive. Dans un workflow de développement, par exemple, il ne peut pas conclure sur une suite de tests tant que les tests ne sont pas terminés. Mais il peut lire le diff, inspecter les logs précédents ou préparer une hypothèse.

C’est là qu’AsyncTool devient intéressant pour les architectures MCP et multi-agents. MCP standardise la connexion aux outils ; AsyncTool demande si l’agent sait les gérer dans le temps. Ce sont deux couches différentes. Brancher plus de serveurs MCP ne rend pas un agent plus robuste s’il perd le fil dès que trois outils répondent dans le désordre.

## AsyncFC : une piste côté exécution

Un autre papier récent, **Concurrency without Model Changes: Future-based Asynchronous Function Calling for LLMs**, publié sur arXiv le 14 mai 2026, attaque le problème par l’angle système. Les auteurs y présentent **AsyncFC**, un framework d’exécution qui découple le décodage du LLM et l’exécution des fonctions. L’idée est de permettre au modèle de continuer à raisonner pendant que certains appels d’outils s’exécutent, en représentant les résultats non disponibles par des **symbolic futures**.

Le point fort revendiqué par AsyncFC est de ne pas nécessiter de modification du modèle, de fine-tuning, ni de changement du protocole standard de function calling. Le framework se place à la couche d’exécution. Selon l’abstract, les auteurs rapportent des réductions significatives du temps de complétion sur des benchmarks de function calling et des benchmarks logiciels adaptés, tout en préservant l’exactitude.

Il faut rester prudent : l’abstract public ne donne pas, à lui seul, tous les chiffres nécessaires pour juger l’ampleur du gain. Mais l’approche est cohérente avec le diagnostic d’AsyncTool. Une partie du progrès viendra probablement des modèles, une autre des runtimes d’agents capables de gérer proprement les futures, les dépendances et les reprises.

## Ce que cela change pour les agents de production

AsyncTool rappelle une chose que les produits agentiques préfèrent souvent esquiver : l’autonomie n’est pas une propriété magique du modèle. C’est une propriété d’un système complet, avec état, planification, outils, exécution, supervision, reprise d’erreur et mesure.

Pour les équipes qui construisent des agents, les implications sont assez concrètes :

- mesurer la performance sous latence, pas seulement en appels synchrones ;
- journaliser les appels d’outils pendants et leur rattachement à chaque tâche ;
- empêcher l’agent de traiter une valeur future comme une observation réelle ;
- tester les retours d’outils hors ordre ;
- séparer qualité finale, temps de complétion et efficacité d’interleaving ;
- prévoir des garde-fous quand l’agent perd la synchronisation.

C’est aussi une invitation à relativiser certains benchmarks de coding agents. Un assistant peut être excellent sur des tâches bornées et moins fiable dans un IDE réel où plusieurs processus tournent, où les tests sont longs, où les fichiers changent, et où l’utilisateur intervient pendant l’exécution.

## À retenir

AsyncTool est important parce qu’il mesure un angle mort très pratique : la capacité d’un agent à travailler dans le temps, pas seulement dans une séquence idéale d’appels. Les agents actuels savent de mieux en mieux choisir des outils. La prochaine marche consiste à savoir attendre intelligemment.

C’est moins spectaculaire qu’un nouveau score SWE-bench, mais probablement plus proche du quotidien des agents utiles. En production, les outils sont lents, les tâches se chevauchent, les résultats arrivent dans le désordre. Si l’agent ne sait pas vivre dans ce désordre, il n’est pas autonome : il est juste synchrone avec une bonne brochure.
