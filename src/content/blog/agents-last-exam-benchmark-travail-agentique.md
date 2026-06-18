---
title: "Agents’ Last Exam : le benchmark qui demande aux agents IA de faire du vrai travail"
description: "ALE évalue les agents sur des tâches professionnelles longues, vérifiables et économiquement utiles. Le résultat initial est brutal : 2,6 % de réussite moyenne sur le niveau le plus dur."
pubDate: 2026-06-08
category: "veille"
tags: ["agents", "benchmarks", "recherche"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — Agents' Last Exam"
    url: "https://arxiv.org/abs/2606.05405"
  - label: "Site officiel — Agents' Last Exam"
    url: "https://agents-last-exam.org/"
  - label: "Code — rdi-berkeley/agents-last-exam"
    url: "https://github.com/rdi-berkeley/agents-last-exam"
---

Les benchmarks d’agents IA ont un problème assez simple : ils vieillissent vite, se saturent vite, et mesurent souvent des tâches trop propres pour ressembler au travail réel. **Agents’ Last Exam**, publié sur arXiv sous l’identifiant 2606.05405, essaie de déplacer le curseur. Le papier présente ALE comme un benchmark pour agents sur des tâches longues, vérifiables et économiquement utiles, construites avec des experts métier plutôt qu’avec une simple collection de puzzles.

Le chiffre qui pique : sur le niveau le plus difficile, les configurations testées affichent une **réussite moyenne complète de 2,6 %**, d’après l’abstract arXiv. En clair, les agents modernes savent impressionner sur des démonstrations courtes, mais échouent encore massivement dès qu’on leur demande d’aller au bout d’un vrai workflow professionnel. L’ego des agents autonomes vient de prendre une petite douche froide. Salutaire.

## Ce qu’ALE mesure vraiment

ALE vise les tâches professionnelles non physiques réalisables sur ordinateur. Le papier indique que le benchmark a été développé avec **250+ experts de l’industrie**, en s’appuyant sur la taxonomie américaine O*NET / SOC 2018. Il organise les tâches en **55 sous-domaines**, regroupés en **13 clusters industriels**, pour plus de **1 000 tâches** dans la version décrite par l’article.

Le site officiel va même plus loin dans la trajectoire : il parle de **1 500+ tâches collectées** vers une cible de **5 000 tâches**, avec une couverture des 55 sous-industries ciblées. Cette différence n’est pas nécessairement une contradiction : le papier arXiv décrit l’état académique soumis, tandis que le site projet met en avant l’évolution du corpus. C’est justement l’un des choix importants d’ALE : ce n’est pas censé être un benchmark figé, mais un **living benchmark**.

La promesse est de tester des tâches à issue vérifiable. Ce point compte. Une bonne évaluation d’agent ne peut pas seulement demander “la réponse a-t-elle l’air plausible ?”. Elle doit pouvoir vérifier un fichier produit, un résultat de simulation, une analyse de données, une modification dans un logiciel, ou une sortie métier attendue. Sinon, on retombe dans le concours de rédaction, version tableur.

## Pourquoi le score de 2,6 % est important

Le score moyen de **2,6 % de full pass** sur le tier le plus dur ne dit pas seulement que les agents sont “mauvais”. Il dit surtout que les benchmarks populaires ne capturent pas encore assez bien la distance entre démonstration et production.

Un agent peut réussir une tâche de coding courte, corriger un bug isolé ou naviguer dans une page web simple. C’est utile. Mais le travail professionnel ressemble rarement à une consigne compacte suivie d’un résultat unique. Il contient des fichiers mal nommés, des logiciels spécialisés, des contraintes implicites, des validations en plusieurs étapes, des erreurs intermédiaires, et parfois une documentation qui semble avoir été écrite comme vengeance personnelle.

ALE essaie de capturer cette friction. Les tâches citées sur le site couvrent par exemple des workflows de motion/VFX dans Adobe After Effects, de modélisation 3D dans Siemens NX, de développement de jeux dans Unreal Engine, d’analyse neuroimagerie avec FSLeyes, ou encore des workflows d’architecture et de simulation. Ce ne sont pas seulement des questions-réponses : ce sont des environnements de travail.

## Le benchmark comme infrastructure, pas seulement leaderboard

Le dépôt GitHub confirme que l’effort ne se limite pas à publier une liste de tâches. Il décrit un framework d’évaluation ouvert autour de l’outil **ale_run**, capable de provisionner des sandboxes, d’exécuter des agents et de les noter. Le dépôt mentionne aussi un sous-ensemble public de **150 tâches de référence** couvrant les 55 industries, avec deux harnesses d’agents de référence.

C’est probablement la partie la plus intéressante techniquement. Les benchmarks d’agents ont besoin de reproductibilité : mêmes environnements, mêmes contraintes, mêmes logs, même logique de grading. Sans cela, comparer deux systèmes revient à comparer deux poissons rouges sur leur aptitude au parapente. On peut le faire, mais il ne faut pas appeler ça de la science.

Le choix des “hidden references” et de graders déterministes, mentionné dans le dépôt, répond aussi à un risque classique : l’overfitting au benchmark. Si les réponses attendues deviennent publiques, les modèles peuvent les absorber indirectement dans les données d’entraînement ou les agents peuvent être réglés contre les cas connus. ALE tente donc de préserver une partie de l’évaluation comme test réellement externe.

## Ce que cela dit des agents en 2026

ALE arrive dans un moment où l’industrie vend les agents comme la prochaine interface du travail. Les assistants de coding deviennent des collègues partiels, les navigateurs se dotent de modes autonomes, les suites bureautiques ajoutent des copilotes, et les plateformes cloud parlent de workflows agentiques comme d’une couche standard.

Le benchmark rappelle une chose moins glamour : **l’autonomie longue durée reste fragile**. Les échecs ne viennent pas seulement de la planification. Ils peuvent venir du manque de connaissance métier, de l’incapacité à manipuler correctement des outils spécialisés, de mauvaises reprises après erreur, ou d’une validation insuffisante du résultat final. Un agent qui “a presque fini” n’est pas un agent productif si le livrable est faux.

Cela ne rend pas les agents inutiles. Au contraire : un score bas sur un benchmark crédible est souvent plus utile qu’un score élevé sur un benchmark saturé. Il indique où investir : meilleures interfaces outils, mémoire de travail plus robuste, exécution vérifiable, capacité à demander ou inférer les contraintes métier, et surtout évaluations plus proches des usages réels.

## Les limites à garder en tête

Il faut rester prudent. ALE est jeune, son corpus complet n’est pas entièrement public, et la qualité d’un benchmark dépendra toujours de la qualité de ses tâches, de ses graders et de sa résistance à la contamination. Le fait qu’il soit “living” est une force, mais aussi une contrainte : les scores devront être datés, les versions clairement suivies, et les comparaisons entre agents devront préciser le corpus exact utilisé.

Autre point : “économiquement utile” est une notion forte. Une tâche peut être représentative d’un métier sans capturer toute la valeur du travail humain : cadrage, responsabilité, relation client, arbitrages, sécurité, et compréhension du contexte organisationnel. ALE mesure mieux le travail que beaucoup de benchmarks, mais il ne mesure pas tout le travail.

## Pourquoi on va le suivre

Agents’ Last Exam a le bon réflexe : déplacer l’évaluation des agents vers des workflows longs, outillés, vérifiables, et liés à des domaines professionnels. Le score initial de 2,6 % n’est pas une condamnation. C’est une ligne de base.

Si les agents progressent vraiment, ils devront monter sur ce type d’évaluation, pas seulement sur des tests de chat ou de code en bac à sable. Le futur des agents ne se jouera pas dans leur capacité à produire une réponse élégante. Il se jouera dans leur capacité à livrer un résultat correct, dans un environnement pénible, avec des contraintes réelles. Bref : au travail.

## Sources

- arXiv — “Agents’ Last Exam” : https://arxiv.org/abs/2606.05405
- Site officiel — Agents’ Last Exam : https://agents-last-exam.org/
- Code — rdi-berkeley/agents-last-exam : https://github.com/rdi-berkeley/agents-last-exam
