---
title: "Harness-1 : sortir la mémoire de recherche du modèle pour entraîner de meilleurs agents"
description: "Un papier arXiv présente un agent de recherche 20B entraîné par RL dans un harness à état externe, avec un gain annoncé de +11,4 points sur les meilleurs subagents ouverts."
pubDate: 2026-06-07
category: "veille"
tags: ["agents", "retrieval", "reinforcement-learning", "search", "research"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — Harness-1: Reinforcement Learning for Search Agents with State-Externalizing Harnesses"
    url: "https://arxiv.org/abs/2606.02373"
  - label: "PDF — Harness-1"
    url: "https://arxiv.org/pdf/2606.02373"
  - label: "GitHub — pat-jj/harness-1"
    url: "https://github.com/pat-jj/harness-1"
---

Les agents de recherche ont un défaut structurel : on leur demande trop souvent de fouiller le web, sélectionner les preuves, vérifier les contraintes, garder le fil des documents consultés et se souvenir de ce qui a déjà été invalidé — le tout dans une conversation qui grossit comme une pâte oubliée près d’un radiateur. **Harness-1**, présenté dans un papier arXiv soumis le **1er juin 2026**, propose une correction nette : sortir le bookkeeping récupérable de la politique du modèle et le confier à un environnement à état explicite.

Le papier, **“Harness-1: Reinforcement Learning for Search Agents with State-Externalizing Harnesses”**, introduit un agent de recherche **20B** entraîné par reinforcement learning dans un **stateful search harness**. La thèse est intéressante parce qu’elle ne dit pas seulement “entraînons un meilleur modèle”. Elle dit : arrêtons de forcer le modèle à être simultanément moteur de recherche, bibliothécaire, greffier, vérificateur et compacteur de contexte.

## Le piège des transcripts qui gonflent

Dans beaucoup de systèmes actuels, un agent de recherche fonctionne comme une politique au-dessus d’un transcript croissant. Chaque recherche, chaque extrait, chaque hypothèse et chaque correction s’ajoute à l’historique. Le modèle doit ensuite décider quoi chercher tout en se souvenant de ce qu’il a déjà vu, de quelles preuves sont fiables, de quelles contraintes restent ouvertes et de quelles affirmations ont été vérifiées.

Ce design a un charme minimaliste : peu d’infrastructure, tout passe par le contexte. Mais il est fragile. Plus la recherche dure, plus le transcript devient bruyant, cher et difficile à exploiter. Les informations importantes se mélangent aux impasses. Les doublons coûtent des tokens. Les vérifications déjà faites peuvent être oubliées ou répétées. Dans un benchmark court, cela passe. Dans une tâche longue, cela devient une taxe permanente.

Harness-1 formalise cette intuition : le reinforcement learning se retrouve à optimiser à la fois des décisions sémantiques — que chercher, quoi garder, quoi vérifier — et des tâches de gestion d’état que l’environnement peut faire plus proprement.

## Ce que le harness prend en charge

Le cœur de Harness-1 est un **harness à état externe**. D’après l’abstract arXiv, cet environnement maintient plusieurs structures : un **candidate pool**, un ensemble curé avec tags d’importance, des liens de preuve compacts, des enregistrements de vérification, des observations compressées et dédupliquées, ainsi qu’un rendu de contexte sensible au budget.

C’est une séparation des responsabilités assez saine. L’environnement garde les objets récupérables : listes de documents, preuves, statuts de vérification, versions compactées. La politique du modèle conserve les décisions qui demandent du jugement : lancer une nouvelle requête, retenir ou rejeter un document, décider quoi vérifier, choisir quand s’arrêter.

On retrouve ici une idée qui revient dans plusieurs travaux agentiques récents : le modèle ne doit pas être le seul lieu de l’état. La fenêtre de contexte est utile, mais ce n’est pas une base de données, encore moins un système de provenance. Quand une information peut être représentée explicitement, vérifiée, compressée et réinjectée à la demande, il vaut souvent mieux la sortir du flux conversationnel.

## Les résultats annoncés

Les auteurs évaluent Harness-1 sur **huit benchmarks de retrieval** couvrant le web, la finance, les brevets et le question answering multi-hop. Le chiffre mis en avant est un **average curated recall de 0,730**. Le papier affirme que Harness-1 dépasse le meilleur subagent de recherche ouvert suivant de **+11,4 points**, tout en restant compétitif avec des searchers basés sur des modèles frontier nettement plus grands.

Autre élément notable : les gains seraient particulièrement forts sur des benchmarks de transfert tenus à l’écart de l’entraînement. Si ce résultat tient, il soutient l’idée que l’apprentissage sur état explicite produit des comportements de recherche plus généralisables que l’apprentissage sur transcripts bruts. C’est plausible : une politique qui apprend à manipuler des structures de preuve et de vérification peut mieux transférer qu’une politique qui apprend surtout à survivre dans son propre historique.

Comme toujours, prudence. Les métriques de retrieval dépendent du protocole, du corpus, du scoring, des baselines et du budget autorisé. “Compétitif avec des frontier-model searchers” ne veut pas dire équivalent dans tous les contextes. Mais le signal est suffisamment intéressant pour mériter attention.

## Pourquoi c’est important pour les agents de recherche

La recherche augmentée par LLM est souvent vendue comme un problème de modèle : meilleur raisonnement, meilleure synthèse, meilleure réponse finale. Harness-1 rappelle que la plomberie compte autant. Pour produire une réponse sourcée fiable, l’agent doit gérer un état de recherche : ce qui a été trouvé, ce qui est pertinent, ce qui est contradictoire, ce qui a été vérifié, ce qui reste incertain.

C’est exactement le type d’état qui se prête mal à un transcript linéaire. Un bon agent de recherche devrait ressembler davantage à un petit système d’investigation : tableau de pistes, preuves attachées, statuts, hypothèses, budget, journal. Le modèle décide ; l’environnement archive et présente.

Cette architecture a aussi un intérêt produit. Elle rend les agents plus auditables. Si le harness conserve des liens de preuve, des enregistrements de vérification et des observations dédupliquées, on peut inspecter pourquoi une réponse a été produite. Ce n’est pas seulement utile pour les benchmarks ; c’est indispensable pour les usages où les citations ne doivent pas être des décorations.

## RL sur comportements, pas sur mémoire improvisée

Le volet reinforcement learning est également important. En entraînant le modèle dans un environnement qui externalise l’état, les auteurs déplacent l’objectif d’apprentissage : la politique n’a plus besoin d’apprendre à compresser mentalement tout l’historique. Elle peut se concentrer sur les décisions de recherche.

Cela rejoint une distinction utile pour les agents : certaines tâches sont **sémantiques**, d’autres sont **mécaniques**. Chercher une source contradictoire est sémantique. Se rappeler qu’une URL a déjà été inspectée est mécanique. Vérifier qu’une claim a une preuve attachée est semi-mécanique. Plus on confond ces couches, plus on gaspille la capacité du modèle.

Harness-1 ne supprime pas le besoin d’un bon modèle. Il redéfinit plutôt ce qu’un bon modèle doit faire dans une architecture de recherche. Ce n’est pas un cerveau solitaire face à un mur de texte ; c’est une politique décisionnelle dans un environnement qui tient les comptes.

## Les limites à surveiller

Le risque principal est l’overfitting architectural. Un harness très structuré peut améliorer les benchmarks ciblés mais devenir rigide hors distribution. Il faut aussi vérifier la qualité des mécanismes de compression et de déduplication : s’ils effacent un signal faible mais décisif, l’agent peut devenir plus propre et moins juste. Le confort de l’état externe ne doit pas masquer les choix de représentation.

Autre limite : l’intégration. Un agent de recherche en production doit interagir avec des moteurs, bases documentaires, permissions, logs, formats hétérogènes, politiques de sécurité. Le papier donne une direction, pas une plateforme prête à brancher partout. Le dépôt GitHub est un bon point de départ pour examiner la reproductibilité, mais les résultats indépendants compteront.

## Ce qu’il faut retenir

Harness-1 est intéressant parce qu’il traite la recherche agentique comme un problème d’architecture, pas seulement de modèle. Son intuition centrale est robuste : un agent ne devrait pas gaspiller sa capacité à maintenir mentalement un carnet de bord que l’environnement peut tenir mieux que lui.

Si les résultats se confirment, l’approche pourrait influencer les futurs agents de recherche, de veille et d’analyse documentaire : moins de transcripts obèses, plus d’état explicite, plus de preuves traçables. C’est moins spectaculaire qu’un nouveau modèle frontier, mais probablement plus utile pour éviter les réponses “sourcées” qui ont l’air sérieuses jusqu’au moment où quelqu’un lit vraiment les sources. Tragique, mais vérifiable.

## Sources

- arXiv — Harness-1: Reinforcement Learning for Search Agents with State-Externalizing Harnesses : https://arxiv.org/abs/2606.02373
- PDF — Harness-1 : https://arxiv.org/pdf/2606.02373
- GitHub — pat-jj/harness-1 : https://github.com/pat-jj/harness-1
