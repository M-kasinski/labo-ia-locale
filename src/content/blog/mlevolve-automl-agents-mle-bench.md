---
title: "MLEvolve : l’agent AutoML qui fait bondir MLE-Bench"
description: "MLEvolve revendique 65,3 % de medal rate moyen sur MLE-Bench en 12 heures, grâce à une recherche en graphe, une mémoire rétrospective et une séparation plus nette entre planification et code."
pubDate: 2026-06-08
category: "veille"
tags: ["agents", "automl", "benchmarks"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — MLEvolve"
    url: "https://arxiv.org/abs/2606.06473"
  - label: "Code — InternScience/MLEvolve"
    url: "https://github.com/InternScience/MLEvolve"
  - label: "OpenAI — MLE-bench"
    url: "https://openai.com/index/mle-bench/"
---

Les agents de coding progressent vite, mais la plupart restent meilleurs pour réparer un bug isolé que pour mener une vraie boucle d’expérimentation machine learning. **MLEvolve**, publié sur arXiv le 4 juin 2026, cible précisément cette zone grise : l’ingénierie ML de bout en bout, avec exploration de données, entraînement, validation, itérations, soumissions et arbitrages de stratégie.

Le résultat revendiqué est difficile à ignorer : **65,3 % de medal rate moyen sur MLE-Bench avec un budget de 12 heures**, d’après le papier et le dépôt GitHub. MLE-Bench, introduit par OpenAI en 2024, regroupe **75 compétitions Kaggle** pour mesurer la capacité d’agents à faire du machine learning engineering réel : préparer les données, entraîner des modèles, lancer des expériences et produire des soumissions notées contre des leaderboards humains. Dans la publication OpenAI initiale, la meilleure configuration mentionnée — o1-preview avec le scaffold AIDE — atteignait au moins le niveau bronze sur **16,9 %** des compétitions.

Comparer directement ces chiffres demande prudence : modèles, budgets, scaffolds, dates et conditions exactes évoluent. Mais même avec cette réserve, MLEvolve signale un changement important. Les agents ML ne sont plus seulement des wrappers de notebooks. Ils deviennent des systèmes de recherche, mémoire et optimisation. Moins sexy qu’une démo de chatbot qui parle avec une voix douce, mais beaucoup plus proche d’un gain industriel.

## Ce que MLEvolve essaie de corriger

Le papier part d’un constat assez juste : les tâches longues comme la découverte scientifique ou l’ingénierie ML ne se résument pas à générer du bon code au premier essai. Elles demandent une capacité à explorer plusieurs pistes, récupérer des informations des échecs précédents, transférer une intuition d’une branche à une autre, et décider quand il faut affiner plutôt que tout réécrire.

Les auteurs identifient trois limites dans les agents MLE existants.

La première est **l’isolation entre branches**. Beaucoup de systèmes explorent plusieurs trajectoires, mais les idées utiles restent coincées dans leur branche. Une expérience qui améliore le prétraitement, un feature engineering prometteur ou une astuce de validation peut ne jamais être réutilisé ailleurs. La recherche parallèle devient alors une collection de solitudes coûteuses. Charmant pour la littérature existentialiste, moins pour les GPU.

La deuxième limite est la **recherche sans mémoire**. Les agents accumulent des logs, mais pas toujours de l’expérience exploitable. Ils oublient pourquoi une tentative a échoué, répètent des variantes inutiles, ou ne savent pas réinjecter une connaissance de domaine au bon moment.

La troisième est le manque de **contrôle hiérarchique**. Beaucoup de boucles agentiques mélangent planification et génération de code : à chaque itération, le modèle peut produire une modification trop large, casser du code qui marchait, ou perdre le fil de la stratégie. En MLE, où les gains viennent souvent d’une série de petits ajustements cohérents, cette instabilité coûte cher.

## Trois briques : MCGS, mémoire, planification adaptative

MLEvolve répond avec trois composants principaux.

Le premier est **Progressive Monte Carlo Graph Search**. L’idée est d’étendre une recherche de type arbre vers une recherche en graphe, où des branches peuvent se référencer entre elles. Au lieu de propager seulement un score ou une récompense, le système peut exploiter des relations entre solutions, favoriser le transfert d’idées, puis faire évoluer l’équilibre exploration/exploitation avec un calendrier progressif inspiré de l’entropie. Dit simplement : au début, on explore large ; ensuite, on concentre le compute sur les directions qui semblent payer.

Le deuxième composant est une **Retrospective Memory**. Elle combine une base de connaissance initiale pour éviter un démarrage à froid et une mémoire dynamique tirée des expériences menées pendant la résolution. C’est un point important : dans une compétition Kaggle, une bonne décision peut venir d’une observation empirique très locale — une fuite de données évitée, une métrique mal comprise, une transformation qui améliore un split mais dégrade un autre. Sans mémoire structurée, l’agent ne capitalise pas.

Le troisième composant est une **planification hiérarchique avec génération de code adaptative**. Le papier insiste sur la séparation entre stratégie et implémentation. L’agent décide d’abord quoi changer : ajouter une feature, modifier un modèle, corriger une validation, ajuster l’ensemble. Ensuite seulement, il choisit comment coder ce changement, avec des modes plus ou moins invasifs. C’est exactement le genre de discipline qui manque aux agents qui réécrivent un pipeline entier pour corriger une virgule.

## Les chiffres : forts, mais à lire correctement

Le dépôt GitHub de MLEvolve donne un tableau de résultats sur le set complet de **75 tâches MLE-Bench**, avec des medal rates rapportés en moyenne ± SEM sur trois seeds. MLEvolve, avec **Gemini-3.1-Pro-preview** et un budget de **12 heures**, revendique :

- **80,3 ± 1,5 %** sur les tâches low complexity ;
- **64,0 ± 0,9 %** sur les tâches medium complexity ;
- **46,7 ± 0,0 %** sur les tâches high complexity ;
- **65,3 ± 0,8 %** en moyenne globale.

Le même tableau le place devant plusieurs méthodes listées, dont des systèmes utilisant des budgets de 24 heures. Le papier affirme aussi que MLEvolve dépasse des méthodes spécialisées comme AlphaEvolve et AlphaEvolve-v2 sur des tâches d’optimisation mathématique, avec une généralisation au-delà du pur MLE.

Ce sont des claims solides à surveiller, pas des vérités gravées dans le silicium. D’abord parce que MLE-Bench est cher et complexe à exécuter ; OpenAI recommande dans son dépôt de répéter les évaluations avec plusieurs seeds, car les agents et les LLM ont une variance importante. Ensuite parce que les comparaisons dépendent beaucoup du modèle sous-jacent, du budget, du scaffold et des conventions de reporting. Enfin parce que les compétitions Kaggle anciennes peuvent devenir plus faciles avec l’amélioration générale des bibliothèques, des recettes publiques et des modèles de langage.

Cela ne retire pas l’intérêt du résultat. Ça évite juste de transformer un tableau en prophétie. On a déjà assez de prophètes dans l’IA ; certains ont même des slides animées.

## Pourquoi MLE-Bench est un bon terrain

MLE-Bench est particulièrement utile parce qu’il teste une compétence intégrée. Il ne demande pas seulement “écris une fonction Python correcte”. Il demande à l’agent de comprendre un problème, manipuler des données, choisir une approche, entraîner, évaluer, itérer, produire une soumission et accepter qu’un leaderboard soit parfois une machine à humilier les intuitions.

OpenAI indique que le benchmark s’appuie sur 75 compétitions Kaggle et établit des baselines humaines via les leaderboards publics. C’est imparfait — les compétitions Kaggle ne représentent pas toute l’ingénierie ML en production — mais c’est beaucoup plus réaliste que des puzzles isolés. Les agents doivent gérer le bruit, les temps d’exécution, les métriques spécifiques, les erreurs de pipeline et la tentation de sur-optimiser un split local.

C’est aussi un bon révélateur de la différence entre “agent de code” et “agent d’ingénierie”. Un agent de code produit des scripts. Un agent d’ingénierie choisit les bonnes expériences, comprend les retours, arbitre le temps, préserve les acquis, et sait quand une amélioration apparente est probablement du surapprentissage. MLEvolve essaie clairement de pousser dans cette deuxième direction.

## Ce que cela dit de l’agentic AI

MLEvolve confirme une tendance : les progrès agentiques viennent souvent moins d’un prompt magique que de l’architecture autour du modèle. Mémoire, recherche, orchestration, validation, sandboxing, stratégie de budget, représentation des expériences : c’est là que se joue une bonne partie de la performance.

Le modèle de base reste central. Ici, MLEvolve utilise Gemini-3.1-Pro-preview dans le résultat principal rapporté sur GitHub. Mais le système montre que la couche agentique peut transformer la façon dont le modèle est exploité. Un frontier model sans bon scaffold peut gaspiller ses capacités ; un scaffold plus discipliné peut convertir les mêmes capacités en itérations utiles.

La conséquence est importante pour les équipes techniques : acheter un modèle performant ne suffit pas. Pour automatiser des workflows longs, il faut concevoir le système comme une boucle d’optimisation, pas comme une interface de chat avec accès au terminal. La différence entre les deux se voit assez vite quand la première expérience échoue — c’est-à-dire presque toujours.

## Les limites à garder en tête

MLEvolve reste un papier jeune, avec un dépôt public mais encore sans release stable mentionnée dans la source extraite. Les résultats doivent être reproduits, comparés dans des conditions harmonisées et observés sur d’autres familles de tâches.

Il y a aussi une limite de domaine. Kaggle mesure très bien certaines formes de machine learning engineering : tabulaire, vision, NLP, métriques de compétition, pipelines de soumission. La production ML ajoute d’autres contraintes : monitoring, dérive de données, sécurité, coûts d’inférence, intégration produit, gouvernance, documentation, responsabilité. Un agent qui gagne une médaille Kaggle ne sait pas automatiquement maintenir un système ML en entreprise. Personne n’a dit que la vie serait élégante.

Enfin, les agents MLE posent des questions de sécurité et de coût. Un système capable de lancer des expériences longues doit être borné : budget compute, accès données, règles d’exécution, interdiction de fuite, audit des artefacts. Plus un agent devient autonome, plus son environnement doit être conçu comme une infrastructure contrôlée.

## Pourquoi on va le suivre

MLEvolve est intéressant parce qu’il ne promet pas seulement “un meilleur assistant de code”. Il propose une architecture où l’agent apprend de ses propres trajectoires, partage des idées entre branches, et sépare mieux la stratégie de l’implémentation. C’est exactement le type de design nécessaire pour passer des tâches courtes aux workflows longs.

Si les résultats se confirment, MLE-Bench pourrait devenir un terrain central pour mesurer la maturité des agents scientifiques et ML. Pas parce qu’il couvre tout, mais parce qu’il force les systèmes à produire des résultats évaluables dans des boucles expérimentales réalistes.

La morale est assez nette : l’avenir des agents ne sera pas seulement dans leur capacité à écrire du code. Il sera dans leur capacité à organiser une recherche, apprendre de leurs échecs, et utiliser le compute comme une ressource stratégique. Là, on commence à parler d’automatisation utile — pas seulement d’un stagiaire numérique très sûr de lui.

## Sources

- arXiv — “MLEvolve: A Self-Evolving Framework for Automated Machine Learning Algorithm Discovery” : https://arxiv.org/abs/2606.06473
- Code — InternScience/MLEvolve : https://github.com/InternScience/MLEvolve
- OpenAI — “MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering” : https://openai.com/index/mle-bench/
