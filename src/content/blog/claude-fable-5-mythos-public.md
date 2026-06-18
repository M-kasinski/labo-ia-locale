---
title: "Claude Fable 5 : Anthropic ouvre Mythos au public, mais sous garde-fous"
description: "Anthropic lance Fable 5, première version généralement disponible de sa classe Mythos. Le saut de capacité est réel, mais l’architecture produit impose des fallbacks, de la rétention et un coût élevé."
pubDate: 2026-06-10
category: "veille"
tags: ["Anthropic", "Claude", "modèles frontier", "agents", "sécurité"]
author: "Veille IA"
draft: false
sources:
  - label: "Annonce officielle Anthropic — Claude Fable 5 and Claude Mythos 5"
    url: "https://www.anthropic.com/news/claude-fable-5-mythos-5"
  - label: "TechCrunch — Anthropic’s Claude Fable 5 is a version of Mythos the public can access today"
    url: "https://techcrunch.com/2026/06/09/anthropic-released-claude-fable-5-its-most-powerful-model-publicly-days-after-warning-ai-is-getting-too-dangerous/"
  - label: "Vellum — Claude Fable 5 & Claude Mythos 5 benchmark breakdown"
    url: "https://www.vellum.ai/blog/claude-fable-5-and-mythos-5-benchmarks-explained"
  - label: "Artificial Analysis — Claude Fable 5 performance and price analysis"
    url: "https://artificialanalysis.ai/models/claude-fable-5"
---

Anthropic vient de faire quelque chose de plus intéressant qu’un simple lancement de modèle : l’entreprise met une partie de sa classe **Mythos** entre les mains du public, mais avec une couche de contrôle suffisamment visible pour devenir elle-même le sujet technique. **Claude Fable 5**, annoncé le 9 juin 2026, est présenté par Anthropic comme le premier modèle Mythos « safe for general use ». En parallèle, **Claude Mythos 5** reprend le même modèle sous-jacent, mais avec certains garde-fous levés pour un petit groupe de cyberdéfenseurs et de fournisseurs d’infrastructure via Project Glasswing.

La ligne éditoriale officielle est claire : Fable 5 dépasse tout ce qu’Anthropic avait rendu généralement disponible jusqu’ici, surtout sur les tâches longues, complexes et agentiques. La ligne d’ingénierie produit l’est autant : ce modèle est jugé assez puissant pour que certains domaines — cybersécurité, biologie, chimie, distillation de modèles — soient interceptés par des classifieurs et redirigés vers **Claude Opus 4.8**. Ce n’est donc pas seulement un nouveau Claude. C’est un modèle frontier livré avec un système de délestage de capacité.

## Un modèle Mythos, mais pas toujours le modèle que tu crois appeler

Anthropic indique que Fable 5 et Mythos 5 partagent le même modèle de base. La différence se situe au niveau des politiques d’accès et de sécurité. Fable 5 applique des garde-fous en production ; Mythos 5 lève certains de ces garde-fous pour des utilisateurs approuvés. Dans les sessions Fable, Anthropic dit que les classifieurs déclenchent un fallback vers Opus 4.8 dans moins de 5 % des sessions en moyenne, ce qui signifie aussi qu’une petite fraction des requêtes ne sera pas traitée par le modèle annoncé.

C’est une décision plus honnête que le flou habituel sur les couches de modération, mais elle complique l’évaluation. Si un benchmark, un workflow interne ou un agent d’entreprise touche à des zones sensibles, la performance observée peut être celle d’un système hybride : Fable 5 sur le cœur de la tâche, Opus 4.8 sur certains segments. Vellum résume bien le point : il faut savoir, avant de construire un workflow, qu’environ une session sur vingt peut ne pas tourner entièrement sur le modèle attendu.

Anthropic ajoute une autre contrainte : le trafic des modèles Mythos-class est soumis à une rétention de 30 jours pour surveillance de sécurité, y compris pour des clients business qui bénéficiaient auparavant d’accords de zéro rétention. L’entreprise précise que ces données ne seront pas utilisées pour entraîner de nouveaux modèles Claude. Mais pour certains usages sensibles — code propriétaire, recherche biomédicale, sécurité offensive contrôlée — la nuance entre « non entraîné » et « retenu 30 jours » n’est pas cosmétique.

## Les chiffres : très fort en agentique, très cher en production

Sur le papier, Fable 5 est le modèle public le plus agressif d’Anthropic. L’annonce officielle revendique un avantage particulièrement net lorsque les tâches deviennent longues et complexes. Vellum rapporte notamment un score de **80,3 % sur SWE-Bench Pro** pour Fable 5, devant Mythos Preview à 77,8 %, Opus 4.8 à 69,2 %, GPT-5.5 à 58,6 % et Gemini 3.1 Pro à 54,2 %. Sur FrontierCode, l’analyse de Vellum cite **29,3 % sur le split Diamond**, contre 13,4 % pour Opus 4.8 et 5,7 % pour GPT-5.5.

Ces chiffres doivent être lus avec prudence. Ils proviennent d’abord de comparaisons publiées par Anthropic, puis reprises et structurées par des analyses tierces. Ils ne remplacent pas des évaluations indépendantes sur des charges de travail internes. Mais la direction est cohérente avec le positionnement : Fable 5 n’est pas optimisé pour discuter vite, il vise les projets longs, le code, l’orchestration d’outils, la vérification et le raisonnement avec contexte étendu.

Artificial Analysis classe Fable 5 parmi les modèles les plus intelligents de son panel, avec un **Intelligence Index autour de 65** et une fenêtre de contexte de **1 million de tokens**. Le revers est très concret : le modèle est cher et lent. Artificial Analysis indique un prix de **12,50 $ par million de tokens d’entrée** et **50 $ par million de tokens de sortie** dans sa fiche, tandis que l’annonce Anthropic affiche **10 $ / 50 $** pour Fable 5 et Mythos 5. L’écart peut venir des modalités de fournisseur ou de présentation tarifaire ; dans les deux cas, ce n’est pas un modèle pour remplacer tous les appels routiniers. C’est un modèle pour les tâches où l’échec coûte plus cher que l’inférence.

La latence va dans le même sens. Artificial Analysis rapporte une vitesse de sortie autour de 59 tokens par seconde, mais surtout un temps avant premier token très élevé, attribué au raisonnement. Pour un agent autonome qui planifie une migration ou analyse un dossier complexe, c’est acceptable. Pour une UX conversationnelle classique, c’est moins gracieux. Le frontier a parfois l’élégance d’un compilateur C++ : impressionnant, mais pas pressé de te rassurer.

## Pourquoi cette sortie compte

Fable 5 marque un déplacement important : Anthropic ne vend plus seulement un modèle plus capable, mais une **frontière d’accès différenciée**. Le même cœur de modèle existe en version publique bridée et en version restreinte pour acteurs jugés légitimes. C’est probablement une preview de la manière dont les laboratoires frontier vont distribuer leurs modèles les plus puissants : non pas par un simple bouton API, mais par classes de confiance, domaines d’usage, rétention obligatoire, monitoring et fallbacks.

Cette architecture a un avantage évident : elle permet de rendre disponible une capacité qui serait autrement confinée. Elle a aussi un coût : les développeurs ne contrôlent plus complètement quel modèle répond dans certaines zones, et les entreprises doivent accepter une politique de données plus intrusive. Pour les agents, c’est un point sensible. Un agent de code ou de sécurité peut alterner entre tâches bénignes et opérations proches de la cybersécurité ; si le modèle change silencieusement de comportement au milieu du run, il faut l’observer, le tracer et le tester.

## À surveiller maintenant

Le vrai test ne sera pas la table de benchmarks. Ce sera l’usage prolongé : migrations de code, refactoring multi-repo, analyse scientifique, workflows avec outils, tâches multimodales longues. Les chiffres disponibles suggèrent un saut sérieux, mais les contraintes — prix, latence, fallback, rétention — font de Fable 5 un composant haut de gamme plutôt qu’un modèle généraliste à invoquer partout.

La conclusion provisoire est simple : Anthropic vient d’ouvrir une partie de Mythos au public, mais pas de manière naïve. Fable 5 est puissant, contrôlé, coûteux, et probablement très utile là où l’autonomie vaut vraiment quelque chose. Pour le reste, il faudra résister à la tentation de mettre un moteur de fusée dans une trottinette.

## Sources

- [Anthropic — Claude Fable 5 and Claude Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5)
- [TechCrunch — Anthropic’s Claude Fable 5 is a version of Mythos the public can access today](https://techcrunch.com/2026/06/09/anthropic-released-claude-fable-5-its-most-powerful-model-publicly-days-after-warning-ai-is-getting-too-dangerous/)
- [Vellum — Claude Fable 5 & Claude Mythos 5 benchmark breakdown](https://www.vellum.ai/blog/claude-fable-5-and-mythos-5-benchmarks-explained)
- [Artificial Analysis — Claude Fable 5 performance and price analysis](https://artificialanalysis.ai/models/claude-fable-5)
