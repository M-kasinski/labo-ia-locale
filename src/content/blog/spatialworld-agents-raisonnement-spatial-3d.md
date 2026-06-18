---
title: "SpatialWorld : les agents multimodaux restent perdus dans l’espace 3D"
description: "Un benchmark sur 760 tâches et huit simulateurs montre que GPT-5 plafonne à 17,4 % de réussite moyenne en raisonnement spatial interactif."
pubDate: 2026-06-11
category: "veille"
tags: ["agents", "multimodal", "benchmarks", "spatial reasoning", "research"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — SpatialWorld: Benchmarking Interactive Spatial Reasoning of Multimodal Agents in Real-World Tasks"
    url: "https://arxiv.org/abs/2606.09669"
  - label: "HTML arXiv — SpatialWorld"
    url: "https://arxiv.org/html/2606.09669"
  - label: "GitHub — Hongcheng-Gao/SpatialWorld"
    url: "https://github.com/Hongcheng-Gao/SpatialWorld"
  - label: "Project page — SpatialWorld"
    url: "https://spatial-world.github.io/"
---

Les modèles multimodaux savent reconnaître des objets, commenter une image, parfois décrire une scène avec une assurance désarmante. Mais dès qu’on leur demande d’**agir** dans un espace 3D partiellement observable — se déplacer, chercher, manipuler, collaborer, terminer une tâche — le vernis craque vite. **SpatialWorld**, publié sur arXiv le **8 juin 2026**, met des chiffres précis sur ce problème.

Le benchmark évalue le raisonnement spatial interactif d’agents multimodaux à travers **760 tâches annotées par des humains**, réparties sur **huit backends de simulation** : **AI2-THOR**, **ProcTHOR**, **VirtualHome**, **CARLA**, **EmbodiedCity**, **Multi-AI2THOR**, **Multi-ProcTHOR** et des **jeux 3D**. Les agents reçoivent une instruction en langage naturel et des observations RGB égocentriques. Ils n’ont pas accès à une carte globale, à une profondeur privilégiée ou à l’état complet du simulateur. Bref : ils doivent se débrouiller avec ce qu’ils voient, comme tout le monde. Quelle cruauté.

Le résultat principal est rude : selon le papier, le meilleur modèle évalué, **GPT-5**, atteint seulement **17,4 %** de taux moyen de réussite de tâche (**TSR**) sur l’ensemble du benchmark. Le meilleur modèle ouvert cité, **Qwen-3.5-397B-A17B**, atteint **14,1 %**. Ce ne sont pas des écarts de leaderboard à la troisième décimale ; ce sont des scores qui rappellent que le raisonnement spatial actif reste un gouffre technique.

## Ce que SpatialWorld mesure

SpatialWorld cible une limite fréquente des benchmarks multimodaux : beaucoup testent une compréhension passive. On montre une image, on pose une question, le modèle répond. C’est utile, mais insuffisant pour juger un agent. Un agent qui travaille dans un monde doit décider quoi regarder, où aller, quoi manipuler et quand s’arrêter.

Le papier formalise les tâches comme des problèmes partiellement observables. À chaque étape, l’agent reçoit une observation RGB égocentrique et doit produire une action textuelle dans une interface unifiée. Cette interface masque les différences entre simulateurs, ce qui permet de comparer les modèles sur des environnements très variés sans réécrire toute l’évaluation à chaque fois.

Les tâches couvrent plusieurs domaines : routines domestiques, travail, divertissement, voyage, collaboration sociale. Le dépôt GitHub détaille la répartition : **311** tâches pour AI2-THOR, **127** pour ProcTHOR, **38** pour VirtualHome, **80** pour CARLA, **53** pour EmbodiedCity, **29** pour Multi-AI2THOR, **17** pour Multi-ProcTHOR et **105** pour les jeux 3D. Les auteurs distinguent aussi des niveaux de complexité comme la navigation, l’interaction objet et les tâches hybrides mêlant déplacement long-horizon et manipulation.

Chaque tâche inclut un état initial validé humainement, une trajectoire de référence et un vérificateur d’état terminal. C’est un détail important : l’évaluation ne repose pas seulement sur un modèle juge qui lit une réponse textuelle. Elle cherche à vérifier si le monde final correspond vraiment à l’objectif. Pour les agents, c’est le bon réflexe : le discours compte moins que l’état atteint.

## Le score global est bas, mais le détail compte encore plus

Le chiffre **17,4 %** pour GPT-5 est la partie la plus visible. Il signifie que même le meilleur modèle testé échoue sur la grande majorité des tâches. Mais SpatialWorld est surtout intéressant parce qu’il montre que les erreurs ne sont pas uniformes.

Le papier rapporte trois constats. D’abord, les agents restent loin d’une résolution fiable des tâches 3D. Ensuite, le succès et l’efficacité ne vont pas forcément ensemble : un modèle peut finir une tâche, mais au prix d’une exploration redondante ou d’une trajectoire peu efficace. Enfin, les classements changent selon les domaines. GPT-5 mène sur des tâches de type quotidien, voyage et collaboration sociale ; **Qwen-3.5-397B-A17B** rivalise ou mène sur certains segments comme Work & Study ou le divertissement physique ; **Gemini-3.1-Pro** obtient les meilleurs scores sur les jeux numériques 3D, d’après l’analyse rapportée par les auteurs.

Ce point est essentiel. Un score unique écrase des capacités différentes : exploration active, mémoire spatiale, planification, manipulation d’objet, navigation extérieure, coordination multi-agent. Deux modèles proches en TSR peuvent avoir des profils très différents. Pour choisir un modèle ou concevoir un agent, le classement global est une mauvaise boussole s’il n’est pas accompagné d’une analyse par domaine.

Le dépôt met aussi en avant un chiffre plus ciblé : sur le “Physical Overall TSR”, GPT-5 atteint **14,4 %** et Qwen-3.5-397B-A17B **12,2 %**. Là encore, prudence : ce sont des résultats dans le protocole des auteurs, sur des modèles et réglages précis. Mais la tendance est claire : dès qu’on sort du texte et de l’image statique, les agents perdent beaucoup de leur superbe.

## Pourquoi les agents échouent

SpatialWorld pointe plusieurs goulets d’étranglement. Le premier est l’**exploration active**. Un modèle peut comprendre l’objectif mais ne pas savoir recueillir l’information nécessaire. Il tourne, regarde au mauvais endroit, se bloque sur une zone, ou répète des actions peu utiles. Dans un benchmark passif, l’information est déjà dans l’entrée. Ici, il faut aller la chercher.

Le deuxième est la **planification longue**. Beaucoup de tâches exigent une séquence : trouver un objet, se déplacer, manipuler, vérifier, corriger. Une erreur au début peut rendre la suite incohérente. Les modèles de langage sont souvent bons pour produire un plan verbal plausible ; ils sont moins robustes quand chaque étape doit être ancrée dans une observation visuelle partielle et un état du monde changeant.

Le troisième est la **mémoire spatiale**. Les agents doivent maintenir une carte implicite : où sont les objets, quelles portes ont été explorées, quelle route mène à la cible, ce qui a déjà été tenté. Sans représentation spatiale stable, l’agent peut “raisonner” correctement localement tout en se comportant globalement comme quelqu’un qui cherche ses clés dans la même poche depuis dix minutes. Nous avons tous nos jours ProcTHOR.

Le quatrième est la **coordination**. Les backends multi-agent ajoutent une couche de difficulté : partage d’état, rôle, progression commune, évitement des actions redondantes. Le papier note que les performances changent fortement selon les environnements multi-agent, avec des layouts procéduraux beaucoup plus durs que des scènes intérieures plus familières.

## Une évaluation plus proche des usages réels

SpatialWorld est pertinent parce qu’il rapproche l’évaluation de plusieurs usages industriels et scientifiques : assistants robotiques, navigation, contrôle d’interface 3D, simulation urbaine, agents de maintenance, systèmes d’assistance en environnement physique ou virtuel. Dans tous ces cas, reconnaître une image ne suffit pas. Il faut construire une représentation du monde, choisir une action, observer les effets, puis recommencer.

Le benchmark évite aussi une tentation classique : donner aux modèles des signaux trop propres. Ici, les agents fonctionnent sous **observabilité partielle**, avec des observations RGB égocentriques. C’est plus difficile, mais plus honnête. Beaucoup d’agents paraissent compétents quand on leur donne l’état complet du monde ; ils deviennent beaucoup moins brillants quand il faut ouvrir les yeux au bon moment.

Cela dit, SpatialWorld reste une prépublication et un benchmark synthétique. Les simulateurs ne sont pas le monde réel. Les scores dépendront des prompts, du contrôleur, de la résolution, du budget d’étapes et des intégrations modèle. Les auteurs publient un dépôt avec code et données, ce qui permettra normalement de mieux auditer les résultats. Pour l’instant, il faut considérer les chiffres comme un signal fort, pas comme une vérité gravée dans le silicium.

## Le message pour les builders d’agents

La leçon pratique est assez nette : un bon agent spatial ne sera pas seulement un meilleur VLM. Il lui faudra une architecture autour du modèle : mémoire topologique, représentation d’état, historique exploitable, exploration guidée, vérification terminale, peut-être outils de perception spécialisés. Les modèles multimodaux généralistes peuvent fournir le raisonnement sémantique, mais ils ne remplacent pas toute la boucle de contrôle.

SpatialWorld montre aussi que l’efficacité doit devenir une métrique de premier rang. En production, réussir en cinquante actions quand cinq suffisent peut être inacceptable : coût, temps, sécurité, usure, latence. Le papier souligne justement le décalage entre réussite et efficacité. C’est un rappel utile pour les leaderboards d’agents : atteindre l’état final est nécessaire, mais pas suffisant.

## Ce qu’il faut retenir

SpatialWorld met un chiffre inconfortable sur une intuition : les agents multimodaux actuels comprennent parfois les scènes, mais ils ne savent pas encore très bien **habiter** l’espace. Avec **760 tâches**, **huit simulateurs** et une évaluation fermée sur l’état terminal, le benchmark expose des faiblesses concrètes en exploration, planification et mémoire spatiale.

Le score de GPT-5 à **17,4 %** de réussite moyenne n’est pas une condamnation définitive des modèles multimodaux. C’est plutôt une carte routière. Pour progresser, il ne suffira pas d’ajouter quelques tokens de pensée. Il faudra construire des agents qui perçoivent, mémorisent, vérifient et agissent avec une représentation spatiale plus solide. Le futur robot majordome attendra encore un peu ; il risquerait de ranger les assiettes dans le garage.

## Sources

- arXiv — SpatialWorld: Benchmarking Interactive Spatial Reasoning of Multimodal Agents in Real-World Tasks: https://arxiv.org/abs/2606.09669
- HTML arXiv — SpatialWorld: https://arxiv.org/html/2606.09669
- GitHub — Hongcheng-Gao/SpatialWorld: https://github.com/Hongcheng-Gao/SpatialWorld
- Project page — SpatialWorld: https://spatial-world.github.io/
