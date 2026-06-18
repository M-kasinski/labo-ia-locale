---
title: "K-BrowseComp : les agents web trébuchent encore hors du web anglophone"
description: "Un nouveau benchmark coréen montre que les agents de navigation restent fragiles dès qu’il faut suivre une chaîne de preuves locale, multi-étapes et vérifiable."
pubDate: 2026-06-05
category: "veille"
tags: ["agents", "benchmarks", "web", "research", "localisation"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — K-BrowseComp: A Web Browsing Agent Benchmark Grounded in Korean Contexts"
    url: "https://arxiv.org/abs/2606.02404"
  - label: "Version HTML arXiv — K-BrowseComp"
    url: "https://arxiv.org/html/2606.02404"
  - label: "GitHub — prometheus-eval/K-BrowseComp"
    url: "https://github.com/prometheus-eval/K-BrowseComp"
  - label: "Hugging Face — prometheus-eval/k-browsecomp"
    url: "https://huggingface.co/datasets/prometheus-eval/k-browsecomp"
---

Les agents web ont un problème assez simple à formuler, beaucoup moins simple à régler : ils sont souvent bons dans les environnements où les benchmarks les ont entraînés à briller. Dès que l’on sort du web anglophone, des requêtes évidentes, et des pages bien structurées, le vernis se fissure. **K-BrowseComp**, publié sur arXiv le **1er juin 2026**, met précisément le doigt là-dessus avec un benchmark de navigation web ancré dans le contexte coréen.

L’intérêt n’est pas seulement linguistique. Le papier ne demande pas aux modèles de “parler coréen” ou de traduire une page. Il teste leur capacité à chercher, croiser, suivre des indices locaux, préserver une chaîne de preuves, puis répondre court et juste. Autrement dit : il teste une compétence agentique réelle, celle dont dépendent les assistants capables de faire de la veille, de l’administratif, de la recherche documentaire ou du support localisé. Le petit détail charmant : les meilleurs modèles restent très loin d’une maîtrise confortable.

## Un BrowseComp localisé, mais pas un simple clone

K-BrowseComp s’inscrit dans la famille de benchmarks inspirés par BrowseComp, qui évaluent les agents capables de naviguer sur le web pour répondre à des questions factuelles difficiles. La version coréenne contient **400 problèmes** au total. Le cœur du benchmark, **K-BrowseComp-Verified**, regroupe **300 problèmes écrits et validés manuellement par des locuteurs natifs coréens**. Un second split de **100 problèmes synthétiques** sert de diagnostic plus adversarial, généré à partir d’exemples difficiles et de modes d’échec ciblés.

Chaque question vise une réponse courte, unique et stable dans le temps. Les auteurs imposent aussi des contraintes de preuve : les réponses doivent être soutenues par des informations publiques textuelles, accessibles sans login, sans document privé, sans PDF ou artefact non textuel obligatoire. C’est important, parce que l’évaluation d’un agent web devient vite impraticable si la source disparaît derrière un paywall, une image ou une page dynamique impossible à rejouer.

Le benchmark cible deux grands types de raisonnement. Le premier est le **multi-hop** : trouver une information intermédiaire, puis s’en servir pour atteindre la suivante. Le second est la **satisfaction de contraintes parallèles** : croiser plusieurs indices indépendants jusqu’à isoler une réponse unique. Ce sont des tâches très proches de la recherche humaine réelle. On ne tape pas toujours “réponse exacte” dans un moteur. Parfois, on suit une odeur. Les agents, eux, ont encore le nez bouché.

## Pourquoi le contexte coréen compte vraiment

Le papier insiste sur une idée que l’industrie sous-estime souvent : un agent de navigation n’est pas seulement un modèle de langage plus un navigateur. C’est un système plongé dans un écosystème documentaire. Les conventions de recherche, les noms d’institutions, les pages locales, les médias, les formats administratifs, les indices culturels et les entités peu visibles changent selon les pays et les langues.

K-BrowseComp couvre des domaines comme les médias coréens, l’éducation, les transports, la culture, le sport, la littérature, les produits, l’histoire ou les politiques publiques. Ce ne sont pas des curiosités folkloriques. Ce sont exactement les cas où un utilisateur local attend qu’un agent soit utile. Un assistant qui sait synthétiser Wikipédia en anglais mais échoue à retrouver une information administrative ou culturelle locale n’est pas un agent généraliste ; c’est un stagiaire très diplômé qui ne trouve pas la salle de réunion.

Ce point touche aussi à la souveraineté IA. Les grands modèles progressent vite, mais les benchmarks dominants restent souvent centrés sur l’anglais ou sur des environnements où les données sont abondantes, bien indexées et largement reprises. Tester le web coréen force les modèles à généraliser hors de cette zone de confort. C’est utile pour la Corée, évidemment, mais aussi pour tous les marchés non anglophones — France comprise.

## Les résultats : les frontier models ne dominent pas tant que ça

Les chiffres rapportés dans l’abstract sont sévères. Sur le split vérifié de **300 problèmes**, des modèles frontier comme **GPT-5.5**, **DeepSeek-V4-Pro** et **GLM-5.1** atteignent seulement **30,00 % à 45,67 %**. Le papier décrit cela comme une chute substantielle par rapport à BrowseComp. Autrement dit, les mêmes familles de modèles qui paraissent solides sur des évaluations web plus générales perdent beaucoup dès que la tâche exige une navigation locale fine.

Le résultat est encore plus brutal pour les modèles coréens issus du programme **Korea's Proprietary AI Foundation Model** : ils obtiennent **0,00 % à 10,33 %** sur le split vérifié, selon l’abstract. Ce chiffre doit être lu prudemment — il dépend du protocole, des outils de recherche, des prompts, et de l’intégration agentique — mais le signal est clair : être un modèle local ne suffit pas à être un bon agent web local.

Sur le split synthétique adversarial de **100 problèmes**, le meilleur modèle atteint seulement **26,00 %**. Les auteurs le rapportent séparément, à juste titre, car ce split est conçu comme un stress test plutôt que comme un benchmark principal. Mélanger les deux aurait gonflé l’effet dramatique, ce qui est tentant mais peu propre. Ici, la séparation aide à comprendre ce qui est mesuré : performance réaliste d’un côté, résistance aux cas piégeux de l’autre.

## Ce que le dépôt rend inspectable

Le dépôt GitHub public `prometheus-eval/K-BrowseComp` donne un peu plus de substance au papier. Il inclut le framework d’évaluation, des copies JSONL locales des datasets, une pipeline de génération automatique pour le split synthétique, ainsi que des exemples d’usage. Les items contiennent la question, la réponse de référence, la trajectoire attendue, les URLs sources et des valeurs de checklist pour les preuves intermédiaires.

Ce dernier point est précieux. Beaucoup de benchmarks d’agents se contentent d’un score final : bonne réponse ou non. K-BrowseComp permet aussi des diagnostics de trajectoire. On peut donc distinguer un agent qui n’a jamais trouvé la bonne source, un agent qui a trouvé la source mais perdu une contrainte, et un agent qui a fait le bon chemin avant de formater une réponse incorrecte. Pour construire de meilleurs systèmes, c’est nettement plus utile qu’un leaderboard décoratif.

Le dépôt indique aussi que l’évaluation est adaptée de `perplexityai/search_evals` et que les dépendances sont gérées avec `uv`. Ce n’est pas un détail éditorial : la reproductibilité des benchmarks d’agents dépend énormément de l’outillage externe — moteur de recherche, contexte disponible, prompts, modèle utilisé, budget de navigation. Un benchmark web n’est jamais aussi figé qu’un QCM statique.

## La leçon pour les agents généralistes

K-BrowseComp rappelle une chose inconfortable : l’agentic AI ne se réduit pas à “le modèle peut appeler un outil”. Un agent utile doit savoir chercher dans un environnement particulier, reformuler, suivre les preuves, gérer les ambiguïtés locales, et s’arrêter avec une réponse courte. C’est une chaîne complète. Un seul maillon faible suffit à produire une hallucination polie.

Pour les équipes produit, le message est très pratique. Si un agent doit servir des utilisateurs francophones, japonais, coréens ou arabophones, il ne suffit pas de brancher un bon modèle généraliste sur un navigateur. Il faut évaluer sur des tâches locales, avec des sources locales, des noms locaux, des conventions locales et des cas multi-étapes. Sinon, le système sera brillant en démo et médiocre au guichet.

La prépublication reste à confirmer par des reproductions indépendantes. Les performances peuvent changer avec un meilleur moteur de recherche, un agent mieux prompté ou des modèles plus récents. Mais le fond du papier est solide : les évaluations d’agents doivent quitter le salon anglophone. Le web réel est multilingue, mal rangé, contextuel. Les agents qui prétendent y travailler doivent être testés là où ça gratte.

## Sources

- arXiv — K-BrowseComp: https://arxiv.org/abs/2606.02404
- Version HTML arXiv — K-BrowseComp: https://arxiv.org/html/2606.02404
- GitHub — prometheus-eval/K-BrowseComp: https://github.com/prometheus-eval/K-BrowseComp
- Hugging Face — prometheus-eval/k-browsecomp: https://huggingface.co/datasets/prometheus-eval/k-browsecomp
