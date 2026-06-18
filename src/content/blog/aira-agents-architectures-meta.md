---
title: "AIRA : quand des agents Meta conçoivent eux-mêmes des architectures de modèles"
description: "Le papier AIRA-Compose et AIRA-Design explore une idée explosive mais encore expérimentale : utiliser des agents LLM pour découvrir de nouvelles architectures de fondation."
pubDate: 2026-06-01
category: "veille"
tags: ["recherche", "agents", "meta", "architectures", "nas", "transformers"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — Agentic Discovery of Neural Architectures: AIRA-Compose and AIRA-Design"
    url: "https://arxiv.org/abs/2605.15871"
  - label: "arXiv HTML — AIRA-Compose and AIRA-Design"
    url: "https://arxiv.org/html/2605.15871v1"
  - label: "DOI — 10.48550/arXiv.2605.15871"
    url: "https://doi.org/10.48550/arXiv.2605.15871"
---

Le papier **“Agentic Discovery of Neural Architectures: AIRA-Compose and AIRA-Design”**, signé par des chercheurs FAIR chez Meta, pose une question qui mérite mieux qu’un titre de science-fiction : des agents LLM peuvent-ils aider à concevoir les prochaines architectures de modèles de fondation ?

La réponse du papier est prudente mais réelle : oui, dans des cadres expérimentaux précis, avec des budgets bornés, des primitives définies et beaucoup de validation automatique. Ce n’est pas encore une IA qui réécrit seule la pile complète du deep learning. C’est plus intéressant : une démonstration structurée de recherche agentique appliquée à la **neural architecture search** et à la conception de mécanismes.

Le travail introduit deux frameworks : **AIRA-Compose**, qui explore des combinaisons de blocs architecturaux à haut niveau, et **AIRA-Design**, qui demande à des agents d’écrire des mécanismes ou scripts d’entraînement plus bas niveau. Le tout est présenté comme un pas vers la “recursive self-improvement”. La formule est chargée, presque radioactive. Il faut donc la dégonfler proprement : ici, “auto-amélioration” signifie surtout que des agents participent à la découverte de composants de modèles, pas qu’ils s’échappent du laboratoire avec une roadmap produit.

## AIRA-Compose : chercher au-dessus du Transformer standard

AIRA-Compose attaque un problème classique : les grands modèles restent très souvent organisés autour d’une recette Transformer assez régulière, avec attention et MLP alternés. Or l’espace des variantes est immense : attention, MLP, Mamba/Mamba2, arrangements hybrides, ratios différents, profondeur, largeur, régularités ou ruptures de pattern.

Le papier indique qu’AIRA-Compose utilise **11 agents** pour naviguer dans cet espace combinatoire, sous un budget fixe de **24 heures**. Les agents conçoivent et évaluent d’abord des candidats à l’échelle du million de paramètres, puis les meilleurs designs sont extrapolés et testés à **350M**, **1B** et **3B** paramètres.

Résultat revendiqué : **14 architectures nouvelles**, réparties en deux familles. Les **AIRAformers** restent dans une famille Transformer, tandis que les **AIRAhybrids** combinent Transformer et Mamba/Mamba2. Le papier rapporte qu’à l’échelle **1B**, sous budget fixe de tokens, les meilleures architectures découvertes par agents dépassent des baselines comme Llama 3.2 et des architectures trouvées par Composer.

Les chiffres les plus cités sont parlants : **AIRAformer-D** et **AIRAhybrid-D** amélioreraient la précision downstream de **2,4 %** et **3,8 %** par rapport à Llama 3.2. Côté scaling, **AIRAformer-C** scalerait **54 %** plus vite que Llama 3.2 et **71 %** plus vite que le meilleur Transformer trouvé par Composer ; **AIRAhybrid-C** dépasserait une approximation de Nemotron-2 de **23 %** et le meilleur hybride Composer de **37 %**.

Ce sont de bons résultats, mais ils restent ceux d’un papier de recherche : les conditions de comparaison, les budgets d’entraînement, les approximations de baselines et les choix de métriques comptent énormément. La conclusion raisonnable n’est pas “les agents ont inventé le successeur du Transformer”. La conclusion raisonnable est : ils peuvent explorer efficacement des zones de design que les humains ne testeraient pas toutes manuellement.

## AIRA-Design : du code de mécanisme, pas seulement des blocs

AIRA-Design descend d’un niveau. Au lieu de recombiner des primitives connues, le framework demande à des agents de produire des mécanismes ou optimisations, par exemple des variantes d’attention pour dépendances longues ou des scripts d’entraînement performants.

Le papier mentionne **20 agents** chargés d’écrire des mécanismes d’attention et des scripts, évalués notamment sur **Long Range Arena** et sur un benchmark d’autoresearch. Sur Long Range Arena, les architectures conçues par agents arrivent à **2,3 points** du state of the art humain sur document matching et à **2,6 points** sur text classification. Sur Autoresearch, une configuration “Greedy Opus 4.5” atteint **0,968 validation bits-per-byte** sous budget de temps fixe, au-delà de la référence minimale publiée selon les auteurs.

Ce passage est important parce qu’il montre la différence entre deux niveaux d’automatisation. AIRA-Compose fait de la recherche dans un espace contraint ; AIRA-Design demande au modèle de proposer du code ou des mécanismes. Le second est plus risqué : un agent peut produire du code qui passe un test étroit sans généraliser, exploiter une faiblesse du benchmark ou simplement converger vers une astuce locale. Le papier le sait, et encadre les expériences avec des harnais, des seeds et des validations.

La vraie question est donc moins “l’agent a-t-il eu une idée ?” que “l’idée survit-elle à des évaluations hors distribution, à d’autres tailles, à d’autres budgets et à une implémentation propre ?”. En recherche ML, l’élégance d’une courbe peut parfois cacher une plomberie héroïque. On respecte la courbe, mais on inspecte les tuyaux.

## Pourquoi les agents sont bien adaptés à ce problème

La neural architecture search n’est pas nouvelle. Ce qui change ici, c’est le rôle de l’agent LLM comme opérateur de recherche : il peut lire des résultats, modifier du code, proposer une variation, déboguer, analyser un échec, puis repartir. Le papier décrit notamment un environnement AIRA-dojo avec des opérateurs comme **Draft**, **Debug**, **Improve** et **Analyze**.

Cette boucle ressemble beaucoup aux workflows de coding agent, mais appliquée à la recherche. L’intérêt est évident : beaucoup de recherche expérimentale consiste à formuler une hypothèse, modifier un script, lancer un run, lire une métrique, corriger une erreur triviale, ajuster un paramètre, puis recommencer. C’est précisément le genre de micro-cycle où un agent peut aider, à condition que l’environnement soit bien verrouillé.

Le verrouillage est crucial. Sans contraintes, un agent de recherche devient vite une machine à produire des variantes invérifiables. Avec un harnais robuste, des métriques claires et des budgets stricts, il devient un moteur d’exploration. La nuance est moins spectaculaire, mais nettement plus utile.

## Ce que cela dit sur l’avenir des labos IA

AIRA illustre une tendance plus large : les labos ne construisent plus seulement des modèles, ils construisent des **systèmes de recherche assistée par modèles**. Les agents ne remplacent pas les chercheurs ; ils automatisent des morceaux de l’espace expérimental. La valeur se déplace alors vers la conception des environnements, des évaluations, des contraintes et des méthodes de sélection.

Cela peut accélérer la découverte d’architectures hybrides, notamment dans les zones où l’intuition humaine est moins fiable que l’expérimentation systématique : ordonnancement de blocs, mécanismes long contexte, compromis entraînement/inférence, ou design de petites architectures qui scalent mieux.

Mais il y a un piège évident : si les agents optimisent les benchmarks qu’on leur donne, ils peuvent aussi amplifier les biais de ces benchmarks. Une boucle de recherche automatisée ne rend pas une métrique plus vraie. Elle la rend plus puissante. Si la métrique est pauvre, on obtient rapidement une solution pauvre mais très optimisée. C’est l’équivalent scientifique d’un costume parfaitement taillé pour la mauvaise personne.

## Les limites à garder en tête

Trois limites méritent d’être nettes.

D’abord, le papier reste une prépublication arXiv. Les résultats n’ont pas encore le poids d’une reproduction indépendante large. Les chiffres doivent donc être considérés comme solides à l’intérieur du protocole décrit, pas comme des lois générales.

Ensuite, les gains rapportés sont liés à des budgets, des baselines et des échelles spécifiques. Une architecture meilleure à 1B ou 3B paramètres sous un budget donné n’est pas automatiquement meilleure à 70B, ni nécessairement plus simple à servir en production.

Enfin, la dimension “recursive self-improvement” est conceptuellement importante, mais techniquement limitée. Les agents ne découvrent pas seuls l’objectif, ne choisissent pas librement toute la pile, et ne valident pas dans le monde réel. Ils opèrent dans un bac à sable de recherche. C’est exactement ce qu’il faut pour faire de la science propre, mais cela mérite d’être dit.

## À retenir

AIRA est un papier à suivre parce qu’il déplace les agents IA du simple rôle d’assistants de code vers celui d’**outils de recherche expérimentale**. Les résultats suggèrent que des agents peuvent découvrir des architectures et mécanismes compétitifs, parfois meilleurs que des baselines humaines ou NAS, sous contraintes bien définies.

Le potentiel est réel : accélérer l’exploration architecturale, tester plus de variantes, trouver des hybrides que les humains n’auraient pas priorisés. La prudence l’est tout autant : sans validation indépendante, sans tests à plus grande échelle et sans métriques robustes, on ne sait pas encore si ces designs deviendront des briques de modèles frontier.

La bonne nouvelle, c’est que le sujet devient concret. On n’est plus dans “un jour, les IA amélioreront les IA”. On est dans : voici un harnais, des agents, des budgets, des architectures, des scores, et des limites. C’est beaucoup plus sain. Et légèrement plus inquiétant, ce qui est souvent le signe qu’une ligne de recherche devient intéressante.
