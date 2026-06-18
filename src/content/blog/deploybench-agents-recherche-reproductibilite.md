---
title: "DeployBench : les agents IA échouent encore à reproduire la recherche"
description: "DeployBench teste un angle peu flatteur pour les agents : repartir d’un artefact de papier, installer l’environnement et produire le bon résultat. Même les meilleurs systèmes trébuchent surtout sur leur propre jugement d’achèvement."
pubDate: 2026-06-10
category: "veille"
tags: ["agents", "benchmark", "recherche", "OpenHands", "reproductibilité"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — DeployBench: Benchmarking LLM Agents for Research Artifact Deployment"
    url: "https://arxiv.org/abs/2606.05238"
  - label: "OpenHands benchmarks — dépôt GitHub"
    url: "https://github.com/OpenHands/benchmarks"
  - label: "arXiv PDF — DeployBench"
    url: "https://arxiv.org/pdf/2606.05238"
---

Les agents de code progressent vite sur les issues GitHub, les PR synthétiques et les benchmarks où l’environnement est déjà prêt. **DeployBench** attaque un angle beaucoup moins confortable : prendre un artefact de recherche publié, repartir d’une machine fraîche, installer ce qu’il faut, exécuter l’expérience désignée par le papier, puis vérifier que la sortie correspond vraiment à l’objectif scientifique.

Le papier, soumis sur arXiv le 3 juin 2026 sous l’identifiant **2606.05238**, présente un benchmark de **51 tâches de déploiement d’artefacts de recherche** couvrant l’IA/ML, les systèmes informatiques et le calcul scientifique. Les auteurs évaluent quatre LLMs récents via **OpenHands** et rapportent des taux de succès allant de **7,8 % à 51,0 %**. Ce n’est pas un petit écart de finition. C’est le rappel que « faire tourner le repo » reste souvent plus difficile que « écrire le patch ».

## Ce que DeployBench mesure vraiment

La plupart des benchmarks de software engineering donnent à l’agent un cadre relativement propre : un dépôt, une issue, des tests, parfois une image Docker ou un environnement suffisamment stable. DeployBench part d’un problème plus proche du quotidien de la recherche : un papier prometteur, un dépôt associé, des dépendances vieillissantes, des scripts mal documentés, parfois du CUDA, parfois des configurations système, parfois des hypothèses implicites que seule la personne qui a publié le code connaît vraiment.

Le benchmark inclut des tâches avec piles multi-langages, dépendances système, contraintes GPU/CUDA, configurations kernel et compatibilité avec du code legacy. Chaque tâche est validée par une **pipeline cachée** qui exécute l’expérience prévue par le papier et vérifie les sorties. C’est important : l’agent ne gagne pas simplement parce que `pip install` finit sans erreur ou parce qu’un notebook démarre. Il doit produire le bon artefact expérimental.

Cette conception cible un problème central pour les agents scientifiques. Un assistant de recherche utile ne doit pas seulement lire un PDF ou proposer une hypothèse ; il doit pouvoir reprendre un artefact existant, résoudre les frictions d’environnement, vérifier que le résultat obtenu est celui attendu, et signaler clairement quand il ne peut pas conclure. DeployBench teste exactement cette zone grise entre DevOps, reproductibilité et jugement scientifique.

## Le résultat qui pique : 7,8 % à 51,0 %

Les auteurs indiquent que les quatre modèles évalués avec OpenHands obtiennent entre **7,8 % et 51,0 %** de pass rate. Sans le détail complet de chaque configuration dans l’abstract, il faut éviter d’en faire un classement définitif des modèles. Le signal robuste est ailleurs : même dans le meilleur cas, environ la moitié des tâches échoue. Dans le pire, l’agent réussit moins d’une tâche sur dix.

Ce résultat tranche avec les scores de plus en plus hauts observés sur certains benchmarks de coding agent. Il ne les invalide pas, mais il expose leur périmètre. Réparer un bug dans un environnement déjà instrumenté et reproduire une expérience scientifique depuis un artefact imparfait ne sont pas la même compétence. Le premier valorise l’édition de code et le passage de tests. Le second demande de diagnostiquer l’environnement, comprendre les intentions du papier, choisir les bons scripts, interpréter les sorties et savoir si l’objectif réel est atteint.

DeployBench est donc moins un benchmark de « coding » qu’un benchmark de **déploiement épistémique** : est-ce que l’agent sait transformer une promesse publiée en résultat exécutable et vérifié ? Pour l’instant, la réponse est : parfois, mais pas assez souvent pour dormir tranquille.

## Le vrai bug : l’agent pense avoir fini

Le point le plus intéressant du papier n’est pas seulement le taux d’échec. C’est la nature des échecs. Les auteurs rapportent que **97 échecs sur 154** sont des self-stops déclenchés par l’agent : l’agent s’arrête de lui-même parce qu’il estime que la tâche est terminée. Mais ses vérifications pré-finales valident un objectif différent ou plus faible que celui attendu par le benchmark.

Ce « completion-judgment problem » est un diagnostic sévère. Beaucoup d’agents ne tombent pas seulement parce qu’ils ne savent pas installer une dépendance ou compiler un binaire. Ils tombent parce qu’ils confondent un proxy de réussite avec la réussite. Un script s’exécute ? Très bien. Une sortie est produite ? Encourageant. Mais est-ce la sortie exigée par l’expérience du papier ? Est-ce le bon jeu de données, le bon mode, la bonne graine, la bonne métrique, la bonne configuration matérielle ? Là, l’agent perd pied.

C’est exactement le genre d’erreur qui passe mal en production. Un agent qui échoue bruyamment est pénible ; un agent qui s’auto-déclare victorieux après avoir validé la mauvaise cible est dangereux. En recherche, cela peut produire des reproductions fantômes. En entreprise, cela devient un run CI vert sur une hypothèse fausse. Le voyant est vert, le pont est peut-être ouvert.

## Pourquoi OpenHands compte dans l’histoire

DeployBench utilise OpenHands comme cadre d’évaluation. Le dépôt public **OpenHands/benchmarks** fournit une infrastructure d’évaluation pour agents OpenHands V1, avec des benchmarks actifs comme SWE-Bench, SWE-Bench Pro, GAIA, Commit0, OpenAgentSafety et ProgramBench. Cette plomberie est importante parce qu’elle rend les évaluations plus comparables et plus reproductibles que des démonstrations ad hoc.

Cela dit, il faut séparer deux choses : DeployBench comme proposition scientifique, et OpenHands comme harness d’exécution. Un autre framework agentique pourrait obtenir de meilleurs ou de moins bons résultats. Le mérite de DeployBench est de proposer une tâche qui résiste aux optimisations superficielles : les agents doivent gérer de vrais artefacts de recherche, pas seulement des tickets bien formés.

## Ce que ce benchmark dit sur les agents scientifiques

DeployBench arrive au bon moment. Les laboratoires et startups vendent de plus en plus l’idée d’agents capables d’accélérer la recherche : lire la littérature, générer des hypothèses, écrire du code, lancer des expériences. Mais l’un des goulots les plus concrets reste la reproductibilité. Beaucoup de résultats publiés sont difficiles à relancer, même pour des humains compétents. Les agents héritent donc d’un terrain miné.

Le benchmark montre trois choses utiles. Premièrement, les agents savent parfois réparer des environnements complexes, mais ce n’est pas fiable. Deuxièmement, les validations cachées sont indispensables : sinon, on récompense vite des signaux faibles comme « le script ne plante plus ». Troisièmement, la capacité de juger l’achèvement est une compétence à part entière. Il faudra probablement entraîner et évaluer explicitement des boucles de vérification plus dures, capables de relire l’objectif, comparer les sorties et refuser de conclure trop tôt.

## La suite : moins de bravoure, plus de vérification

DeployBench ne dit pas que les agents de recherche sont inutiles. Il dit qu’ils sont encore mauvais au moment le plus délicat : transformer une installation bricolée en résultat fiable. C’est moins spectaculaire qu’un agent qui écrit 5 000 lignes de code, mais beaucoup plus important pour la science computationnelle.

La prochaine étape devrait être évidente : intégrer des checklists d’achèvement plus strictes, des validateurs externes, des comparaisons automatiques de résultats, et peut-être des agents critiques séparés de l’agent exécutant. Tant que l’agent est à la fois l’opérateur et le juge de sa propre réussite, il aura tendance à s’accorder le bénéfice du doute. Charmant chez un stagiaire enthousiaste, moins chez une machine qui vient de consommer trois heures de GPU.

DeployBench a donc le mérite de déplacer la conversation : les agents ne doivent pas seulement agir, ils doivent savoir quand leur action a réellement atteint la cible. Pour la reproductibilité scientifique, c’est le minimum syndical. Le reste, c’est du théâtre avec des logs.

## Sources

- [arXiv — DeployBench: Benchmarking LLM Agents for Research Artifact Deployment](https://arxiv.org/abs/2606.05238)
- [arXiv PDF — DeployBench](https://arxiv.org/pdf/2606.05238)
- [OpenHands benchmarks — dépôt GitHub](https://github.com/OpenHands/benchmarks)
