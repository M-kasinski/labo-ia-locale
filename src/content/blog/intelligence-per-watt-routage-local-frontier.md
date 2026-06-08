---
title: "Intelligence per Watt : pourquoi le futur est au routage local + frontier"
description: "Le papier Stanford/Hazy repris par Clément Delangue donne une mesure utile : les modèles locaux couvriraient désormais 71,3% des requêtes chat et raisonnement. Le vrai enjeu n’est pas de tout localiser, mais de router proprement."
pubDate: 2026-06-08
tags: ["ia-locale", "routage", "Hugging Face", "Stanford", "efficacite", "benchmarks"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "X — Clément Delangue sur Intelligence per Watt"
    url: "https://x.com/ClementDelangue/status/2064039913843286318"
  - label: "arXiv — Intelligence per Watt: Measuring Intelligence Efficiency of Local AI"
    url: "https://arxiv.org/abs/2511.07885"
  - label: "Stanford Scaling Intelligence — Intelligence Per Watt"
    url: "https://scalingintelligence.stanford.edu/pubs/ipw/"
  - label: "Hazy Research — Intelligence Per Watt: A Study of Local Intelligence Efficiency"
    url: "https://hazyresearch.stanford.edu/blog/2025-11-11-ipw"
  - label: "GitHub — HazyResearch/intelligence-per-watt"
    url: "https://github.com/HazyResearch/intelligence-per-watt"
---

Clément Delangue a partagé un chiffre qui mérite mieux qu’un simple repost enthousiaste : selon le papier **Intelligence per Watt** de Stanford/Hazy Research, la part de requêtes chat et raisonnement pouvant être correctement traitée par des modèles locaux serait passée de **23,2 % en 2023** à **71,3 % en 2025**. Le message est simple : on n’a pas besoin d’un modèle frontier pour la majorité des tâches.

C’est un bon signal pour l’IA locale. Mais il faut le lire sans transformer le graphique en religion. Le papier ne dit pas que “le local remplace tout”. Il dit plutôt que le compromis a changé : pour une grande partie des demandes courantes, envoyer systématiquement la requête vers une API centrale devient de moins en moins rationnel.

## Ce que mesure vraiment “Intelligence per Watt”

Le papier propose une métrique appelée **IPW**, pour *intelligence per watt* : une façon de relier la qualité d’une réponse à la puissance consommée. L’étude évalue plus de 20 modèles locaux, 8 accélérateurs matériels et environ 1 million de requêtes single-turn de chat et de raisonnement. Les auteurs mesurent notamment l’exactitude, l’énergie, la latence et la puissance.

Trois résultats ressortent :

1. les modèles locaux peuvent répondre correctement à **88,7 %** des requêtes single-turn étudiées, avec des variations selon les domaines ;
2. l’efficacité IPW aurait progressé de **5,3×** entre 2023 et 2025 ;
3. la couverture locale des requêtes serait passée de **23,2 %** à **71,3 %** sur la même période.

Le chiffre de 71,3 % est celui qui accroche l’œil, évidemment. Il raconte une transition : les petits et moyens modèles ne sont plus seulement des jouets pour prompts faciles. Ils deviennent une couche de production crédible pour une partie du trafic réel.

## Le point important : router, pas choisir un camp

La conclusion la plus solide n’est pas “local contre cloud”. C’est **local d’abord, frontier quand nécessaire**.

Un assistant personnel ou un agent de travail devrait pouvoir décider :

- rester local pour reformuler, résumer, classer, extraire, coder sur des tâches simples, manipuler des documents privés ;
- escalader vers un modèle frontier pour les raisonnements longs, les tâches très ouvertes, les problèmes ambigus ou les demandes où l’erreur coûte cher ;
- comparer plusieurs sorties quand le coût d’un mauvais choix dépasse le coût d’inférence.

C’est là que l’article devient vraiment intéressant pour un stack local. Le sujet n’est pas seulement “quel modèle lancer sur mon Mac ou ma machine GPU ?”. C’est : **quel routeur met-on devant les modèles ?**

Un bon routeur devrait tenir compte du type de tâche, de la longueur de contexte, du niveau de confidentialité, du coût, de la latence, de la mémoire disponible, et idéalement d’un score de confiance. En clair : l’intelligence locale devient utile quand elle sait reconnaître ses limites. Un petit modèle qui sait demander de l’aide est souvent plus précieux qu’un gros modèle qui improvise avec aplomb.

## Pourquoi c’est crédible maintenant

La partie matérielle compte autant que la partie modèle. Le billet Hazy Research insiste sur l’arrivée d’accélérateurs locaux capables de faire tourner des modèles à latence interactive : Apple Silicon avec mémoire unifiée, GPU desktop, NPU mobiles, petites stations IA. En parallèle, les modèles ouverts progressent vite : familles Qwen, Gemma, Granite, gpt-oss et autres variantes compactes.

Côté utilisateur, cela change le calcul. Avant, garder l’inférence locale signifiait souvent accepter une baisse de qualité trop visible. Maintenant, pour beaucoup de tâches courantes, le coût d’un aller-retour cloud devient plus difficile à justifier : confidentialité, latence, dépendance réseau, facture API, et énergie côté datacenter.

Ce n’est pas une victoire totale du local. C’est plus subtil — donc plus utile. Le local devient la **couche par défaut** pour ce qu’il sait faire correctement, et le cloud devient une **capacité d’escalade**. L’API frontier n’est plus le marteau universel ; elle devient l’outil cher qu’on sort quand le mur est vraiment porteur.

## Ce que ça change pour les agents locaux

Pour les agents, l’enjeu est encore plus net. Un agent lit des fichiers, appelle des outils, exécute parfois du code, manipule des secrets ou du contexte projet. Plus le workflow est proche de données personnelles ou internes, plus le local a de valeur.

Mais un agent local mal routé peut aussi devenir médiocre : il économise trois centimes et rate la tâche. La bonne architecture ressemble plutôt à ceci :

1. **un modèle local rapide** pour comprendre l’intention, résumer le contexte et faire les opérations simples ;
2. **un mécanisme d’évaluation** pour détecter les tâches incertaines ou critiques ;
3. **un fallback frontier** quand la difficulté dépasse le seuil ;
4. **des journaux de routage** pour savoir pourquoi telle requête est restée locale ou partie dans le cloud ;
5. **des benchmarks maison**, parce que les moyennes globales ne disent pas si ton workflow précis marche.

C’est ici que l’IPW devient plus qu’une métrique académique. Elle pousse à mesurer l’efficacité réelle d’un système, pas seulement son score de benchmark. Pour un agent local, le bon indicateur n’est pas “combien de tokens par seconde ?”, mais “combien de tâches utiles terminées correctement, pour quel coût énergétique et quel niveau de confidentialité ?”.

## La prudence nécessaire

Il y a plusieurs pièges à éviter.

D’abord, les chiffres du papier portent sur des requêtes **single-turn**. Les agents réels sont souvent multi-étapes : recherche, planification, appels d’outils, correction d’erreurs, mémoire, validation. Une requête simple bien couverte localement ne garantit pas qu’un workflow agentique complet sera fiable.

Ensuite, “local” ne veut pas dire “gratuit”. Il faut compter la mémoire, la chauffe, l’usure subjective de la machine, la latence sous charge, et le temps passé à maintenir les modèles. Le cloud est parfois plus cher, mais il évite aussi de transformer son laptop en petit radiateur de bureau avec ambitions philosophiques.

Enfin, la qualité dépend énormément du domaine. Un modèle local peut être excellent pour classer des notes, résumer un document ou écrire du code simple, puis devenir fragile sur une question de droit, de médecine, de maths avancées ou d’architecture logicielle ambiguë. Le routage doit intégrer cette variabilité.

## À retenir

Le post de Clément Delangue est intéressant parce qu’il met le doigt sur la bonne bataille : **la majorité des tâches IA n’ont pas toujours besoin d’un modèle frontier**. Le papier Stanford/Hazy donne une base plus sérieuse à cette intuition, avec une métrique orientée efficacité plutôt que pur prestige de benchmark.

Pour Labo IA Locale, le message est clair : l’avenir n’est pas un assistant 100 % local par dogme, ni un assistant 100 % cloud par paresse. C’est une pile multi-modèle, mesurée, capable de garder local ce qui peut l’être et d’escalader proprement quand il le faut.

Le prochain avantage compétitif ne sera peut-être pas seulement le meilleur modèle. Ce sera le meilleur **routeur**. Moins glamour qu’un leaderboard, oui. Mais beaucoup plus proche de ce qui fait réellement gagner du temps.

## Sources

- [X — Clément Delangue sur Intelligence per Watt](https://x.com/ClementDelangue/status/2064039913843286318)
- [arXiv — Intelligence per Watt: Measuring Intelligence Efficiency of Local AI](https://arxiv.org/abs/2511.07885)
- [Stanford Scaling Intelligence — Intelligence Per Watt](https://scalingintelligence.stanford.edu/pubs/ipw/)
- [Hazy Research — Intelligence Per Watt: A Study of Local Intelligence Efficiency](https://hazyresearch.stanford.edu/blog/2025-11-11-ipw)
- [GitHub — HazyResearch/intelligence-per-watt](https://github.com/HazyResearch/intelligence-per-watt)
