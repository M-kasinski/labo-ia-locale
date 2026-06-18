---
title: "ITBench-AA : les agents IA échouent encore sur les incidents Kubernetes"
description: "Artificial Analysis et IBM lancent ITBench-AA, un benchmark SRE agentique où les meilleurs modèles restent sous 50 %. Un rappel utile : diagnostiquer un incident réel n’est pas résoudre un puzzle de terminal."
pubDate: 2026-05-30
category: "veille"
tags: ["agents", "benchmark", "sre", "kubernetes", "enterprise-ai"]
author: "Veille IA"
draft: false
sources:
  - label: "IBM Research sur Hugging Face — ITBench-AA announcement"
    url: "https://huggingface.co/blog/ibm-research/itbench-aa"
  - label: "Artificial Analysis — ITBench-AA leaderboard"
    url: "https://artificialanalysis.ai/evaluations/itbench-aa"
  - label: "IBM Research — ITBench publication"
    url: "https://research.ibm.com/publications/developing-ai-agents-for-it-automation-tasks-with-itbench"
  - label: "ITBench-AA dataset"
    url: "https://huggingface.co/datasets/ArtificialAnalysis/ITBench-AA/tree/main/sre"
---

Artificial Analysis et IBM viennent de publier **ITBench-AA**, un benchmark pour agents IA appliqué aux tâches d’IT d’entreprise. Le premier volet cible un cas très concret : le diagnostic d’incidents **SRE sur Kubernetes**. Le résultat est sobre, et assez salutaire : même les meilleurs modèles restent **sous les 50 %** sur la métrique principale.

C’est une nouvelle importante parce qu’elle déplace la discussion agentique hors des démos confortables. On ne demande pas ici au modèle de générer un script isolé ou de résoudre un exercice terminal. On lui donne un instantané d’incident avec logs, traces, métriques, événements, topologie et manifests Kubernetes, puis on lui demande d’identifier les entités réellement responsables. Autrement dit : faire le travail sale d’un diagnostic de production, sans le folklore marketing autour de « l’agent autonome qui répare tout ».

## Ce que mesure ITBench-AA

ITBench-AA est l’implémentation par Artificial Analysis du benchmark ITBench d’IBM, adaptée pour évaluer des modèles et agents sur des tâches d’entreprise. La première release porte sur la **root-cause analysis SRE** : le modèle doit inspecter un snapshot d’incident Kubernetes et produire un diagnostic structuré, au format JSON, listant les entités contributrices.

Les entités possibles incluent des **Deployments**, **Services**, **Pods**, **Namespaces**, **Network Policies**, **ConfigMaps** et autres ressources Kubernetes. Les signaux fournis couvrent les alertes, événements, traces, métriques, logs, topologie applicative et contexte d’infrastructure. C’est exactement le type de surface où un agent peut sembler brillant dans une démo et se tromper lourdement en production.

Le corpus d’évaluation comprend **59 tâches SRE** : **40 tâches publiques** issues de la release ITBench d’IBM, et **19 tâches privées** partagées avec Artificial Analysis par l’équipe ITBench. Chaque tâche est répétée **trois fois**, ce qui permet de lisser une partie de la variabilité des modèles. L’exécution se fait avec **Stirrup**, le harness open-source d’Artificial Analysis, dans un environnement sandboxé avec accès shell au snapshot.

## Une métrique dure, mais pertinente

La métrique principale est l’**average precision at full recall**. Dit simplement : le modèle doit trouver **toutes** les vraies causes pour obtenir du crédit. S’il manque une entité racine, le score de la tentative tombe à **0**. S’il trouve toutes les causes mais ajoute des fausses pistes, il reçoit un score partiel selon sa précision : vrais positifs divisés par vrais positifs plus faux positifs.

Cette règle est sévère, mais elle a du sens. En incident response, un diagnostic qui trouve une partie du problème mais rate la cause indépendante principale peut envoyer l’équipe dans le mur. À l’inverse, un modèle qui liste trop large peut noyer les opérateurs sous des hypothèses inutiles. ITBench-AA pénalise donc les deux travers classiques des LLM : l’oubli discret et la sur-explication confiante.

C’est aussi ce qui rend le benchmark plus intéressant que beaucoup de classements agentiques saturés. Un bon score demande de relier plusieurs signaux, d’éviter les conclusions prématurées, de comprendre les objets Kubernetes, puis de restituer une réponse minimale. Le modèle doit raisonner, mais aussi enquêter proprement.

## Les résultats : sous 50 %, même au sommet

D’après l’annonce IBM/Artificial Analysis et le leaderboard Artificial Analysis, le meilleur score initial est obtenu par **Claude Opus 4.7 en Adaptive Reasoning, Max Effort**, autour de **46,7 %**. **GPT-5.5 xhigh** suit à environ **46 %**. **Qwen3.7 Max** est autour de **42 %**.

Côté modèles ouverts ou open-weight, Artificial Analysis signale des résultats intéressants sur le front coût/performance : **GLM-5.1 Reasoning** atteint environ **40 %**, **DeepSeek V4 Pro Reasoning Max Effort** environ **38 %**, et **Gemma 4 31B Reasoning** environ **37 %**. Le benchmark note notamment que certains modèles ouverts se placent favorablement sur le coût par tâche, même lorsqu’ils ne battent pas les meilleurs modèles fermés.

Le point essentiel n’est pas de déclarer un vainqueur. Le point essentiel est que **tous les modèles frontier échouent encore sur plus de la moitié des cas** selon cette métrique. C’est une douche froide utile pour les promesses d’agents SRE entièrement autonomes. Les modèles savent explorer, lire, formuler des hypothèses. Ils ne savent pas encore diagnostiquer de façon fiable un incident Kubernetes réaliste, sous contrainte de précision et de rappel.

## Pourquoi c’est plus dur que Terminal-Bench

Artificial Analysis souligne que les modèles font beaucoup mieux sur des benchmarks comme Terminal-Bench. Ce n’est pas contradictoire. Terminal-Bench évalue souvent la capacité à utiliser un terminal pour résoudre une tâche relativement bornée. ITBench-AA ajoute la complexité d’un système distribué : dépendances entre services, symptômes indirects, signaux bruités, causes multiples, configuration Kubernetes, temporalité d’un incident.

Un modèle peut être bon pour écrire une commande shell et mauvais pour distinguer un symptôme d’une cause racine. Il peut repérer une erreur dans des logs mais ignorer qu’elle n’est qu’un effet secondaire d’une network policy mal configurée. Il peut aussi confondre le composant qui crashe avec le composant qui déclenche réellement la panne. C’est précisément le genre d’ambiguïté qui sépare l’automatisation utile de l’automatisation dangereuse.

Le benchmark couvre des modes de panne réalistes : épuisement de quotas de ressources, erreurs de rollout, saturation de pools de connexions, partitions réseau, incidents applicatifs, fautes d’infrastructure et scénarios injectés par chaos engineering. Ce sont des problèmes où le contexte compte autant que l’action.

## Ce que cela dit des agents d’entreprise

ITBench-AA arrive à un moment où presque tous les vendeurs d’observabilité et de plateformes cloud promettent des copilotes ou agents d’incident response. Datadog, PagerDuty, AWS, incident.io et d’autres mettent en avant des réductions de MTTR ou des assistants capables de résumer et recommander. Ces outils peuvent être utiles, mais les benchmarks indépendants rappellent une limite : recommander n’est pas diagnostiquer avec certitude.

Le bon usage à court terme n’est probablement pas « laisse l’agent résoudre l’incident ». C’est plutôt : faire collecter les signaux, produire une première hypothèse, proposer une liste de vérifications, générer des commandes de lecture, résumer les traces et réduire le temps humain passé à naviguer dans le bruit. L’agent devient un analyste junior rapide, pas un SRE senior autonome.

La différence est plus qu’une nuance produit. Dans un environnement de production, une mauvaise action peut amplifier l’incident. Même un diagnostic faux mais plausible peut coûter cher s’il détourne l’équipe pendant vingt minutes. Les agents SRE doivent donc être évalués sur le taux de diagnostic correct, mais aussi sur la calibration, l’explicabilité, la capacité à dire « je ne sais pas » et l’intégration avec les garde-fous opérationnels.

## Pourquoi le benchmark est une bonne nouvelle

Le score bas ne signifie pas que les agents sont inutiles. Il signifie qu’on commence enfin à mesurer le bon problème. Les benchmarks faciles créent des illusions de maturité. Les benchmarks durs forcent les fournisseurs à améliorer le harness, la mémoire, l’exploration, les outils, les formats de diagnostic et les mécanismes de vérification.

ITBench-AA est aussi intéressant parce qu’il rend l’environnement partiellement reproductible : dataset publié, harness Stirrup open-source, scoring explicite, snapshots montés dans un workspace. Tout n’est pas ouvert — les 19 tâches privées restent privées, ce qui est normal pour limiter l’overfitting — mais la direction est saine.

La prochaine étape sera de voir si les progrès viennent surtout des modèles ou des systèmes autour des modèles. Mon pari prudent : les gains les plus rapides viendront du **harness** — meilleure recherche dans les logs, outils spécialisés Kubernetes, graphes de dépendances, vérificateurs de diagnostic, mémoire d’incidents — autant que du modèle lui-même. Les agents d’entreprise ne seront pas sauvés par un seul LLM plus gros ; ils seront sauvés, ou non, par des boucles d’enquête mieux instrumentées.

## À retenir

ITBench-AA met une borne réaliste sur l’état des agents IA pour l’IT : prometteurs, mais loin d’être fiables en autonomie. Sous 50 % sur un benchmark SRE sérieux, cela ne veut pas dire « inutilisable ». Cela veut dire « à garder dans la boucle humaine, avec mesure, logs et garde-fous ».

C’est moins spectaculaire qu’une démo qui redémarre un pod toute seule. C’est aussi beaucoup plus proche de ce dont les équipes de production ont besoin : savoir précisément quand l’agent aide, quand il hallucine, et quand il faut lui retirer les clés de la salle machine.
