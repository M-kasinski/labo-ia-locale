---
title: "Code as Agent Harness : le runtime devient le vrai produit des agents IA"
description: "Un survey UIUC, Meta et Stanford formalise une intuition devenue centrale : pour rendre les agents fiables, le modèle compte, mais le harness exécutable, vérifiable et stateful compte autant."
pubDate: 2026-06-10
category: "veille"
tags: ["agents", "harness", "coding", "multi-agents", "recherche"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — Code as Agent Harness"
    url: "https://arxiv.org/abs/2605.18747"
  - label: "Page projet — Code as Agent Harness"
    url: "https://code-as-harness.github.io/code-as-harness-webpage/"
  - label: "GitHub — Awesome Code as Agent Harness Papers"
    url: "https://github.com/YennNing/Awesome-Code-as-Agent-Harness-Papers"
---

Les agents IA sont souvent racontés comme une histoire de modèle : plus de paramètres, plus de raisonnement, plus de contexte, plus de « tool use ». Le survey **Code as Agent Harness**, publié sur arXiv sous l’identifiant **2605.18747**, propose une lecture plus terre-à-terre et probablement plus utile : dans les systèmes agentiques sérieux, le code n’est plus seulement ce que le modèle produit. Il devient le **harness**, c’est-à-dire l’infrastructure exécutable qui permet à l’agent de raisonner, agir, conserver un état, vérifier ses sorties et coordonner plusieurs rôles.

Le papier, signé par Xuying Ning et 41 autres auteurs affiliés notamment à **University of Illinois Urbana-Champaign, Meta et Stanford**, est un survey de **102 pages** qui cite plus de **450 travaux** selon la page projet. Ce n’est pas une nouvelle architecture miracle, mais une tentative de nommer proprement une bascule que l’on voit déjà dans Claude Code, Codex, les agents GUI, les workflows DevOps automatisés et les systèmes multi-agents : la valeur se déplace du prompt isolé vers un environnement programmatique durable.

## Le code comme interface avec le monde

La première couche du cadre proposé est le **harness interface**. L’idée est simple : un LLM brut manipule du texte ; un agent utile doit manipuler un environnement. Le code sert alors d’interface entre l’intention exprimée en langage naturel et des actions vérifiables : scripts, appels API, tests, DOM, simulateurs, fichiers, traces d’exécution, états de dépôt.

C’est une différence plus profonde qu’elle n’en a l’air. Une chaîne de pensée textuelle peut expliquer une stratégie, mais elle reste difficile à exécuter et à vérifier. Un programme, lui, peut être lancé, inspecté, testé, instrumenté, rejoué. Le survey insiste sur ce point : le code rend certaines formes de raisonnement **exécutables**. Ce n’est pas magique ; c’est simplement beaucoup plus contrôlable qu’un paragraphe persuasif.

On retrouve cette logique dans les approches de type program-of-thought, dans les agents de software engineering qui transforment un ticket en patch testé, ou dans les agents GUI qui convertissent une instruction en séquence d’actions sur une interface. Dans tous ces cas, le modèle n’est pas seulement un générateur de réponse. Il écrit ou manipule un artefact qui devient le support de l’action.

## Planning, mémoire, outils : la plomberie qui fait tenir l’agent

La deuxième couche est celle des **harness mechanisms** : planning, mémoire, usage d’outils, feedback, contrôle et optimisation. C’est probablement la partie la plus importante pour l’ingénierie actuelle des agents.

Un agent long-horizon ne peut pas fonctionner comme un chatbot qui recommence à zéro à chaque tour. Il lui faut une mémoire de travail, une mémoire persistante, des traces, des tests, des logs, des validations intermédiaires, parfois des politiques de rollback. Le survey regroupe ces mécanismes sous l’idée que le harness transforme les échecs en signaux de réparation. Un test qui échoue n’est pas juste une mauvaise nouvelle ; c’est une observation exploitable par la boucle agentique.

Cette approche explique pourquoi les agents de code modernes ressemblent de plus en plus à de petits systèmes d’exploitation spécialisés. Ils lisent un dépôt, produisent un plan, modifient des fichiers, lancent des commandes, interprètent les erreurs, révisent le patch, relancent les tests, puis décident s’ils peuvent s’arrêter. La compétence du modèle reste cruciale, mais elle est canalisée par une structure qui impose des points de contrôle.

Le papier pointe aussi un problème souvent sous-estimé : l’évaluation ne devrait pas mesurer seulement le succès final. Si deux agents réussissent la même tâche, mais que l’un y arrive par une trajectoire stable et vérifiable tandis que l’autre accumule des actions risquées avant d’avoir de la chance, le score binaire cache une information importante. Pour des agents déployés en production, la trajectoire compte.

## Multi-agents : le dépôt comme mémoire partagée

La troisième couche concerne le passage du single-agent au **multi-agent**. Là encore, le survey évite le folklore des « équipes d’agents » qui discutent dans le vide. Son point fort est de ramener la coordination à des artefacts partagés : code, fichiers, plans, revues, tests, traces, état de workflow.

Dans un système multi-agent crédible, un planner, un coder, un reviewer et un tester ne devraient pas seulement échanger des messages. Ils doivent opérer sur une représentation commune de la tâche. Un dépôt, un dossier de travail, une suite de tests, un journal d’exécution ou un tableau d’état jouent alors le rôle de mémoire partagée. Le code devient le lieu où les désaccords se matérialisent et se vérifient.

C’est là que le concept de harness devient utile. Sans état partagé robuste, les agents se coordonnent par conversation implicite, avec les bugs classiques : perte de contexte, duplication d’effort, écrasement de modifications, validation contradictoire. Avec un harness explicite, on peut imposer des permissions, des étapes, des revues, des tests et des règles de promotion. Moins sexy qu’un débat entre quatre avatars, mais beaucoup plus proche d’un système qui tient debout.

## Les vrais problèmes ouverts

La page projet résume plusieurs défis : évaluation au-delà du succès final, vérification avec feedback incomplet, amélioration sans régression, état partagé entre agents, supervision humaine pour les actions critiques, extension aux environnements multimodaux. Ce sont des problèmes d’ingénierie dure, pas des détails de packaging.

Le point sur l’amélioration sans régression est particulièrement important. Si un harness apprend de ses échecs et se modifie lui-même, il faut éviter qu’une correction locale casse une capacité existante. C’est le même problème que dans le logiciel classique, mais avec un agent qui propose parfois les changements, les applique et les juge. Autrement dit : la boucle CI/CD doit aussi surveiller la boucle agentique.

La supervision humaine pose le même genre de difficulté. Dire « human in the loop » ne suffit pas. Il faut décider quelles actions doivent être bloquées, lesquelles peuvent être exécutées puis auditées, quels états doivent être visibles, et comment éviter que l’humain ne devienne un simple bouton « approuver » fatigué. Le harness est l’endroit naturel où ces règles peuvent vivre.

## Pourquoi ce survey compte maintenant

Le papier n’annonce pas un nouveau SOTA, et c’est tant mieux. Son intérêt est de formaliser le travail invisible qui sépare une démo d’agent d’un système exploitable. Les prochains gains ne viendront pas seulement de modèles plus forts ; ils viendront aussi de harnesses mieux conçus, plus observables, plus testables, moins amnésiques.

Cela ne veut pas dire que le modèle devient secondaire. Un mauvais modèle dans un bon harness reste un mauvais agent, simplement mieux encadré. Mais l’inverse est tout aussi vrai : un modèle frontier dans un harness fragile peut produire des trajectoires impressionnantes et des erreurs silencieuses. La fiabilité vient de l’ensemble.

**Code as Agent Harness** donne un vocabulaire précis à cette intuition. Pour les équipes qui construisent des agents, le message est net : arrêtez de traiter le runtime, les tests, la mémoire, les logs et les règles d’arrêt comme de la plomberie secondaire. Dans les agents, la plomberie est une partie du produit. Et comme souvent, c’est elle qui fuit en premier.

## Sources

- [arXiv — Code as Agent Harness](https://arxiv.org/abs/2605.18747)
- [Page projet — Code as Agent Harness](https://code-as-harness.github.io/code-as-harness-webpage/)
- [GitHub — Awesome Code as Agent Harness Papers](https://github.com/YennNing/Awesome-Code-as-Agent-Harness-Papers)
