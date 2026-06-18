---
title: "MACU : les agents de computer use passent enfin au travail en équipe"
description: "Un papier de CMU propose Multi-Agent Computer Use, une orchestration où un manager découpe les tâches en DAG et lance plusieurs agents en parallèle sur le web et le desktop."
pubDate: 2026-06-05
category: "veille"
tags: ["agents", "multi-agent", "computer-use", "benchmark", "recherche"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — Multi-Agent Computer Use"
    url: "https://arxiv.org/abs/2606.01533"
  - label: "Projet MACU — code et visualisations"
    url: "https://jykoh.com/multi-agent-computer-use/"
  - label: "GitHub — multi-agent-computer-use"
    url: "https://github.com/kohjingyu/multi-agent-computer-use"
---

Les agents de **computer use** sont encore souvent évalués comme des individus très appliqués : un agent unique regarde un écran, clique, lit, tape, attend, recommence. C’est propre pour un benchmark. C’est rarement optimal pour une tâche réelle. Un humain qui doit enquêter sur un site, comparer des documents, remplir un formulaire, vérifier une hypothèse et corriger une erreur ne fait pas tout strictement en série. Il découpe, parallélise, délègue, revient sur ses pas. Bref : il travaille comme un petit système distribué avec du café.

Le papier **Multi-Agent Computer Use**, publié sur arXiv le 1er juin 2026 par Jing Yu Koh, Ruslan Salakhutdinov et Daniel Fried, propose de prendre cette intuition au sérieux. Les auteurs introduisent **MACU**, une architecture générale pour transformer des computer-use agents isolés en système multi-agent coordonné. Pas de nouveau modèle entraîné, pas de promesse de conscience d’équipe : un manager, plusieurs sous-agents, un graphe de tâches, de la replanification. C’est moins romanesque qu’une armée d’agents autonomes, mais nettement plus utile.

## Le problème : l’agent sériel est un mauvais runtime

Les computer-use agents contrôlent des interfaces : navigateur, bureau, applications web, parfois terminal ou IDE. Ils doivent comprendre ce qui est visible, décider d’une action, l’exécuter, observer le résultat, puis continuer. Cette boucle fonctionne sur des tâches courtes. Elle devient fragile sur les tâches longues, surtout quand plusieurs pistes doivent être explorées.

Le papier part d’un constat simple : le mode “un agent, une trajectoire” sous-utilise le parallélisme naturel des problèmes. Chercher une information sur deux sites indépendants, comparer des options, tester plusieurs chemins de navigation, vérifier une hypothèse pendant qu’un autre processus avance : tout cela peut être fait en parallèle. Un agent unique doit arbitrer séquentiellement, et chaque mauvais détour coûte cher.

Il y a aussi un problème de **partial observability**. Dans une interface, certaines informations sont visibles à un moment donné puis disparaissent, changent ou deviennent difficiles à retrouver. Si l’agent ne les note pas correctement, il perd du contexte. Si plusieurs sous-tâches dépendent d’une observation temporaire, il faut la conserver et la transmettre explicitement. MACU traite cette contrainte comme une propriété centrale du système, pas comme un détail de prompt.

## L’architecture : manager, DAG, sous-agents

MACU repose sur une structure assez nette. Un **manager model** reçoit la tâche globale et la décompose en **graphe acyclique dirigé** — un DAG. Chaque nœud correspond à une sous-tâche, chaque arête encode une dépendance. Les nœuds prêts, c’est-à-dire ceux dont les dépendances sont satisfaites, forment une “frontière” que le manager peut distribuer à des sous-agents en parallèle.

Ces sous-agents ne sont pas nécessairement spécialisés. Le papier parle de computer-use agents parallèles qui exécutent les nœuds assignés. Le manager récupère leurs résultats, met à jour l’état du DAG, ajoute des nœuds si une piste nouvelle apparaît, en annule si elle devient inutile, ou en réécrit si les informations changent. L’orchestration ressemble davantage à un chef de projet qui maintient une carte dynamique qu’à un simple “best-of-N” où l’on lance plusieurs tentatives et garde la meilleure.

Ce point est important. Beaucoup de méthodes de test-time scaling consistent à échantillonner plusieurs trajectoires et à sélectionner un résultat. MACU, lui, cherche à faire collaborer les trajectoires. Les agents ne sont pas seulement en compétition ; ils produisent des informations réutilisables par les autres parties du plan.

## Les résultats : gains modestes parfois, massifs sur les tâches longues

D’après l’abstract arXiv, MACU améliore des baselines single-agent fortes sur plusieurs benchmarks de desktop et web navigation : **OSWorld**, **Online-Mind2Web**, **WebTailBench** et **Odysseys**. Les gains rapportés vont de **3,4 % à 25,5 %** selon les environnements. C’est une plage large, mais elle raconte quelque chose de cohérent : plus la tâche est longue, ouverte et propice à la décomposition, plus la coordination multi-agent a de chances d’aider.

Le cas le plus parlant est **Odysseys**, un benchmark de navigation web long horizon. Les auteurs indiquent que MACU réduit le temps médian de complétion d’environ **162 minutes à 110 minutes**, soit environ **1,5x** plus rapide en temps réel. Sur des agents de production, le temps mur compte presque autant que le taux de réussite. Un agent qui termine une tâche trois heures plus tard avec une belle trace de raisonnement reste, techniquement, un stagiaire très cher.

Il faut garder les chiffres à leur place. Ces résultats dépendent du modèle manager, du nombre de sous-agents, de la fréquence de replanification et de la qualité des environnements de benchmark. Ils ne prouvent pas que “multi-agent” bat toujours “single-agent”. Ils montrent plutôt qu’il existe une dimension de scaling encore sous-exploitée : non pas seulement rendre le modèle plus gros, mais mieux organiser son temps et ses copies.

## Pourquoi ce n’est pas juste du parallélisme naïf

Lancer dix agents en parallèle est facile. Les faire converger vers une solution cohérente l’est beaucoup moins. Le risque évident est de multiplier les erreurs, les actions redondantes et les interprétations contradictoires. Un système multi-agent mal conçu peut coûter plus cher, consommer plus de tokens, et produire une synthèse plus confuse qu’un agent unique.

MACU essaie de limiter ce problème avec deux choix structurants. D’abord, le DAG impose des dépendances : tout n’est pas lancé dans tous les sens. Ensuite, le manager sert de mémoire et de point de coordination. Il conserve les observations qui doivent survivre au passage d’un sous-agent à l’autre, et il peut modifier le plan quand un résultat rend une branche inutile.

Cette approche rejoint une tendance plus large dans les agents : l’autonomie n’est pas seulement une propriété du modèle, mais du **runtime**. Les progrès viennent autant de l’orchestration, de la mémoire, du suivi d’état, des permissions, de la reprise d’erreur et de la mesure que du prochain checkpoint frontier. MCP standardise l’accès aux outils ; des travaux comme MACU interrogent la manière d’organiser l’usage de ces outils dans le temps et entre plusieurs exécutants.

## Ce que cela change pour les agents de coding

Même si le papier cible le computer use au sens large, les implications pour les agents de développement sont évidentes. Un agent de coding sérieux ne devrait pas seulement lire un bug, modifier un fichier et lancer les tests. Il devrait pouvoir découper : un sous-agent inspecte l’historique, un autre lit la documentation, un troisième reproduit le bug, un quatrième prépare un correctif, pendant qu’un manager garde la cohérence et décide quand fusionner les pistes.

C’est déjà la direction prise par certains produits : sous-agents spécialisés, exécution parallèle, environnements isolés, relecture croisée. MACU apporte une formulation académique claire et des benchmarks pour mesurer cette intuition. Le détail du DAG est particulièrement utile parce qu’il rend le plan inspectable. Dans un contexte professionnel, savoir pourquoi un agent a lancé trois sous-tâches et pourquoi il en a annulé une n’est pas du confort : c’est de l’auditabilité.

## Les limites à surveiller

La première limite est économique. Plusieurs agents parallèles coûtent plus cher qu’un seul. Si le gain de réussite ou de temps ne compense pas le coût en tokens, en sessions navigateur ou en machines virtuelles, le système sera élégant mais peu rentable. Le papier indique un meilleur test-time scaling, mais chaque équipe devra refaire ce calcul dans son contexte.

La deuxième limite est la sécurité. Plus il y a d’agents capables d’agir sur des interfaces, plus la surface d’erreur s’élargit. Dans un navigateur ou un poste de travail réel, un sous-agent peut cliquer au mauvais endroit, exposer une donnée ou valider une action irréversible. Le manager doit donc aussi devenir un point de contrôle : permissions, sandboxing, validation avant action sensible, journalisation.

La troisième limite est l’évaluation. Les benchmarks actuels capturent une partie du problème, mais les environnements réels sont plus sales : sessions expirées, interfaces instables, notifications, fichiers locaux, droits incomplets, humains qui interrompent la tâche. MACU est une bonne direction, pas une preuve de robustesse industrielle générale.

## À retenir

MACU est intéressant parce qu’il déplace le centre de gravité des agents. Au lieu de demander seulement “quel modèle clique le mieux ?”, il demande “quelle organisation permet à plusieurs agents de travailler plus longtemps, plus vite et avec moins de perte de contexte ?”. C’est probablement une des bonnes questions pour 2026.

La prochaine génération d’agents utiles ne sera pas seulement plus intelligente. Elle sera mieux coordonnée. Et, comme souvent en informatique, le vrai progrès ressemble moins à une révélation mystique qu’à un scheduler correct, une mémoire propre et un graphe de dépendances qui ne ment pas. Ce n’est pas glamour. C’est précisément pour ça que ça peut marcher.

## Sources

- [arXiv — Multi-Agent Computer Use](https://arxiv.org/abs/2606.01533)
- [Projet MACU — code et visualisations](https://jykoh.com/multi-agent-computer-use/)
- [GitHub — multi-agent-computer-use](https://github.com/kohjingyu/multi-agent-computer-use)
