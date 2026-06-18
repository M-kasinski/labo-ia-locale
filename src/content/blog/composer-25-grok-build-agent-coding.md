---
title: "Composer 2.5 : xAI ajoute un modèle plus endurant à Grok Build"
description: "xAI rend Composer 2.5 disponible dans Grok Build. L’annonce est courte, mais elle confirme une tendance nette : les modèles de code sont désormais optimisés pour des sessions agentiques longues, pas seulement pour compléter des fonctions."
pubDate: 2026-06-02
category: "veille"
tags: ["xAI", "agents", "coding", "Grok"]
author: "Veille IA"
draft: false
sources:
  - label: "xAI — Composer 2.5"
    url: "https://x.ai/news/composer-2-5"
  - label: "Artificial Analysis — Composer 2.5 sur le Coding Agent Index"
    url: "https://artificialanalysis.ai/articles/cursor-composer-2-5-coding-agent-index"
  - label: "xAI — page d’actualité Grok Build"
    url: "https://x.ai/news"
---

xAI a publié le 1er juin une annonce minimaliste mais intéressante : **Composer 2.5 est désormais disponible dans Grok Build**, via le menu `/models` de l’outil. La page officielle ne donne pas de carte système détaillée, pas de tableau complet de benchmarks, pas de description d’architecture. Elle dit une chose assez précise : Composer 2.5 est un modèle “fast, state-of-the-art” conçu pour **les tâches longues** et **le suivi d’instructions complexes**.

C’est peu, mais ce peu est révélateur. Le marché des assistants de développement n’est plus seulement une bataille de modèles généralistes branchés sur un terminal. Il se fragmente en modèles explicitement entraînés pour tenir une trajectoire sur plusieurs étapes : inspecter un dépôt, proposer un plan, modifier plusieurs fichiers, exécuter des commandes, lire les erreurs, corriger, recommencer. Dit autrement : le produit n’est plus “un LLM qui sait coder”, mais **un agent de maintenance logicielle avec mémoire de travail, discipline et coût maîtrisé**.

## Ce qui est confirmé

La source robuste ici est l’annonce de xAI. Elle confirme trois points : la disponibilité de Composer 2.5 dans Grok Build, la date du 1er juin 2026, et le positionnement du modèle sur les tâches longues avec instructions complexes. xAI précise aussi que l’accès passe par Grok Build, avec une sélection depuis `/model`, et que l’outil est disponible pour les abonnés SuperGrok et X Premium+.

Il faut rester sobre sur le reste. Plusieurs discussions et articles tiers associent Composer 2.5 à des résultats élevés dans les benchmarks de coding agents, mais la page xAI extraite ne publie pas elle-même de scores. Artificial Analysis rapporte de son côté que Composer 2.5 se place dans le haut de son **Coding Agent Index**, derrière certains couples agent/modèle plus coûteux, avec des gains sur des suites comme SWE-Bench-Pro-Hard-AA, Terminal-Bench v2 et SWE-Atlas-QnA. C’est utile comme signal indépendant, mais ce n’est pas une system card xAI ; il faut donc lire ces chiffres comme une évaluation externe d’un système de coding agent, pas comme une vérité universelle sur le modèle brut.

## Pourquoi c’est important

Les benchmarks de code classiques ont longtemps mesuré une capacité assez limitée : produire le bon patch pour un problème cadré. Les assistants modernes, eux, doivent survivre à un environnement plus sale. Un agent doit comprendre la structure d’un dépôt, accepter qu’un test échoue pour une raison non prévue, ne pas casser une API existante, gérer les dépendances, et parfois revenir sur son propre plan.

C’est précisément là que la mention de “long-running tasks” devient intéressante. Un modèle plus fort sur une question isolée n’est pas forcément meilleur dans une boucle agentique de trente minutes. Dans ces boucles, les défauts se cumulent : une petite hallucination de fichier, un test ignoré, une commande exécutée au mauvais endroit, et l’agent part repeindre la cuisine alors qu’on lui demandait de changer une ampoule.

Composer 2.5 semble donc viser la partie la moins spectaculaire mais la plus rentable du coding assisté : **la persistance contrôlée**. Pas seulement écrire du code, mais tenir une stratégie sans se diluer.

## Grok Build devient un environnement, pas juste une démo

xAI avait déjà positionné Grok Build comme un outil de coding agent. L’arrivée d’un modèle sélectionnable depuis le menu interne indique une logique de plateforme : différents modèles pour différents régimes de travail. Un modèle rapide pour itérer, un modèle plus robuste pour les tâches longues, peut-être demain des variantes spécialisées par langage, par type de dépôt ou par niveau d’autonomie.

C’est une évolution que l’on voit aussi ailleurs : Claude Code, Codex, Cursor, Gemini dans les environnements développeur, et les outils MCP qui donnent aux agents un accès plus structuré aux fichiers, terminaux, navigateurs ou tickets. La compétition se joue moins sur “qui répond le mieux à une question Python” que sur l’ensemble **modèle + harnais agentique + politique d’outils + coût par tâche réussie**.

Sur ce terrain, xAI a une carte évidente : intégrer plus étroitement ses modèles à ses produits, et optimiser pour l’usage réel plutôt que pour un chatbot généraliste. Composer 2.5, dans Grok Build, va dans cette direction.

## La prudence nécessaire sur les claims

L’annonce officielle est courte. Elle ne donne pas de contexte window, pas de prix API public pour Composer 2.5, pas de méthode d’entraînement, pas de taux de réussite officiel sur SWE-Bench ou Terminal-Bench. Les analyses externes, notamment Artificial Analysis, donnent des indications plus riches sur le rang et le coût relatif, mais elles évaluent un système complet et peuvent dépendre du scaffold, du niveau d’effort, des outils autorisés et des prompts de test.

C’est un point important : en 2026, comparer deux “modèles de code” sans comparer leur environnement revient souvent à comparer deux voitures dont l’une roule sur circuit sec et l’autre dans Paris un vendredi soir. Même moteur, autre monde.

## Ce qu’il faudra surveiller

Trois questions détermineront si Composer 2.5 est un vrai jalon ou une mise à jour incrémentale.

D’abord, la **fiabilité sur longues sessions** : l’agent garde-t-il le cap après plusieurs cycles test/correction ? Ensuite, le **coût par tâche réussie**, plus pertinent que le prix au million de tokens quand l’agent peut gaspiller beaucoup de contexte. Enfin, la **surface d’intégration** : un modèle enfermé dans un seul outil peut être excellent, mais il sera plus difficile à évaluer et à intégrer dans des workflows d’entreprise.

Pour l’instant, la conclusion raisonnable est celle-ci : Composer 2.5 confirme que xAI prend le coding agent au sérieux, et que Grok Build n’est pas seulement une interface autour d’un modèle généraliste. Mais faute de system card complète, il faut éviter de surinterpréter. Le signal est fort ; la preuve détaillée reste à publier.
