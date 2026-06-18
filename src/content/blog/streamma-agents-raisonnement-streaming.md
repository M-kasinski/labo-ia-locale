---
title: "StreamMA : faire raisonner les agents en streaming plutôt qu’en file indienne"
description: "Un papier arXiv propose de réduire la latence des systèmes multi-agents en transmettant les étapes de raisonnement au fil de l’eau, avec des gains annoncés sur huit benchmarks."
pubDate: 2026-06-06
category: "veille"
tags: ["agents", "multi-agent", "research", "latency", "llm"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — Streaming Communication in Multi-Agent Reasoning"
    url: "https://arxiv.org/abs/2606.05158"
  - label: "GitHub — EnVision-Research/StreamMA"
    url: "https://github.com/EnVision-Research/StreamMA"
  - label: "Project page — StreamMA"
    url: "https://zhenyangcs.github.io/StreamMA-website/"
---

Les systèmes multi-agents ont un problème très simple, presque embarrassant : ils aiment se regarder finir leurs phrases. Dans beaucoup d’architectures, un agent produit toute sa chaîne de raisonnement, puis transmet le résultat complet au suivant, qui recommence à zéro avec ce paquet. Le papier **“Streaming Communication in Multi-Agent Reasoning”**, soumis sur arXiv le **3 juin 2026**, propose une alternative : **StreamMA**, un protocole où les agents transmettent leurs étapes de raisonnement au fil de l’eau aux agents en aval.

L’idée paraît évidente une fois formulée. Si l’agent B peut commencer à travailler dès que l’agent A a produit les premières étapes utiles, pourquoi attendre la fin complète ? C’est le même principe que le streaming dans les pipelines logiciels ou les systèmes distribués : on chevauche les traitements au lieu de les empiler. Mais appliqué au raisonnement multi-agents, le papier avance une thèse plus forte : le streaming ne réduirait pas seulement la latence, il améliorerait aussi l’efficacité du raisonnement.

## Le défaut du “generate-then-transfer”

Le paradigme classique décrit par les auteurs est le **generate-then-transfer**. Un agent amont génère toute sa réponse ou toute sa trace de raisonnement. Cette sortie est ensuite envoyée à l’agent suivant. Dans une chaîne de trois, quatre ou cinq agents, la latence de bout en bout augmente mécaniquement avec la profondeur du pipeline. Plus on ajoute de rôles — planificateur, critique, solveur, vérificateur, synthétiseur — plus le système devient lent.

C’est un vrai sujet produit. Les architectures multi-agents promettent souvent plus de robustesse : plusieurs agents se corrigent, se spécialisent, confrontent leurs hypothèses. En pratique, elles paient cette robustesse en temps, en tokens et en complexité. Un système qui donne une meilleure réponse après deux minutes peut être inutile dans un outil interactif. L’utilisateur n’attend pas un comité de sages pour chaque refactor. Même un comité très poli.

StreamMA remplace cette file indienne par un mécanisme de **pipelining**. Chaque étape de raisonnement est transmise dès qu’elle est générée, ce qui permet aux agents aval de commencer plus tôt. Le dépôt GitHub officiel décrit une implémentation où les agents sont organisés dans un **DAG configurable** : chaîne, arbre ou graphe avec raccourcis. Chaque agent dispose de son propre prompt système et d’une liste d’agents destinataires.

## Le point le plus intéressant : moins de latence, mais aussi moins d’erreurs

La réduction de latence est attendue. Le papier affirme toutefois un résultat plus contre-intuitif : StreamMA améliore aussi la performance de raisonnement. L’argument est que la qualité d’une chaîne de raisonnement n’est pas uniforme. Les premières étapes seraient souvent plus fiables que les étapes tardives, qui accumulent davantage de risques d’erreur, de surinterprétation ou de dérive.

Dans un protocole classique, l’agent aval reçoit tout : les bonnes intuitions initiales, mais aussi les conclusions tardives potentiellement contaminées. Dans StreamMA, il peut commencer à exploiter les étapes précoces avant d’être exposé à l’ensemble de la chaîne. Les auteurs présentent cela comme une manière de limiter l’influence des erreurs tardives. C’est plausible, mais à manier avec prudence : selon la tâche, une étape tardive peut aussi contenir la correction décisive. Le streaming n’est pas une baguette magique ; c’est un choix d’architecture qui change la dynamique des erreurs.

Le papier revendique une analyse formelle comparant trois protocoles : **stream**, **serial** et **single**. Il annonce notamment un ordre d’efficacité, une borne supérieure de speedup et un ratio de coût. C’est important parce que beaucoup de travaux multi-agents restent au niveau du design intuitif : “ajoutons un critique”, “ajoutons un planificateur”, “ajoutons un agent de vérification”. StreamMA tente de formaliser les compromis entre profondeur, vitesse, coût et qualité.

## Les résultats annoncés

D’après l’abstract arXiv, StreamMA est évalué sur **huit benchmarks** couvrant les mathématiques, les sciences et le code, avec deux modèles frontier — **Claude Opus 4.6** et **GPT-5.4** — et trois topologies : **Chain**, **Tree** et **Graph**. Les auteurs rapportent que StreamMA dépasse les baselines, avec un gain moyen de **+7,3 points de pourcentage** et un maximum de **+22,4 points** sur **HMMT 2026** avec Claude Opus 4.6-high.

Ces chiffres sont intéressants, mais il faut les lire comme des résultats de papier, pas comme une garantie opérationnelle. La performance dépendra du type de tâche, de la granularité des étapes transmises, de la stabilité des prompts, de la gestion des contradictions et du coût d’orchestration. Le fait que le dépôt GitHub soit public est un bon signal pour la reproductibilité, mais il faudra voir si des équipes indépendantes retrouvent les mêmes gains dans des environnements différents.

Le dépôt officiel donne aussi des indices pratiques. L’implémentation s’appuie sur Python, `asyncio` et l’API compatible OpenAI. La configuration du graphe se fait par dictionnaire : chaque agent a un `system_prompt` et une liste `next` vers ses destinataires. Le logger enregistre des métriques de runtime, de tokens, de cache KV et une timeline des segments streamés. Autrement dit, StreamMA n’est pas seulement une idée de papier ; il existe déjà une base de code expérimentale pour tester l’approche.

## Une “scaling law” pour les étapes, pas seulement pour les agents

L’autre claim notable est la découverte d’une **step-level scaling law**. Les auteurs disent observer qu’augmenter le nombre d’étapes par agent améliore à la fois l’efficacité et l’efficience, et que cette dimension serait orthogonale au scaling par nombre d’agents. C’est une formulation ambitieuse. Si elle tient, elle suggère que l’on ne doit pas seulement demander “combien d’agents ?”, mais aussi “combien d’étapes utiles chaque agent doit-il exposer au reste du système ?”.

C’est une bonne question pour la conception des agents. Ajouter des rôles spécialisés peut améliorer la couverture, mais augmente la latence et le risque de bruit. Ajouter des étapes internes peut améliorer le raisonnement, mais peut aussi accumuler des erreurs. StreamMA propose une troisième voie : rendre ces étapes exploitables par les autres agents en temps réel. Le raisonnement devient une ressource partagée, pas un monologue livré en bloc.

## Pourquoi cela peut compter pour les agents de code

Les agents de code sont un terrain naturel pour ce type d’architecture. Un agent peut analyser une stack trace, un autre inspecter les fichiers, un troisième proposer une hypothèse, un quatrième préparer les tests. Dans une architecture séquentielle, chacun attend trop longtemps. Dans une architecture streamée, le testeur peut commencer dès que l’hypothèse initiale est formulée, pendant que l’analyste continue à lire le contexte.

Mais le risque est réel : plus les agents travaillent en parallèle sur des informations partielles, plus il faut gérer les désaccords et les mises à jour. Si l’agent A change d’avis après trois étapes, que fait l’agent B qui a déjà commencé à construire sur l’hypothèse précédente ? StreamMA rend le système plus fluide, mais exige une meilleure discipline de synchronisation, de versioning des hypothèses et de critères d’arrêt. Le streaming distribué a toujours ce charme : il accélère tout, y compris les malentendus.

## Ce qu’il faut retenir

StreamMA attaque un vrai goulot d’étranglement des architectures multi-agents : la latence imposée par les échanges séquentiels. Son pari est que transmettre les étapes de raisonnement au fil de l’eau peut rendre les agents à la fois plus rapides et plus efficaces, en exploitant les premières étapes avant que les erreurs tardives ne contaminent la suite.

Le papier est récent, les résultats doivent être reproduits, et les conditions exactes d’usage compteront énormément. Mais l’idée est solide : les agents ne doivent pas seulement mieux raisonner, ils doivent mieux **communiquer pendant qu’ils raisonnent**. Pour les workflows longs — code, recherche, résolution scientifique — c’est probablement une direction plus utile que d’empiler encore un agent “critique” à la fin du pipeline et d’espérer qu’il sauve la journée.

## Sources

- arXiv — Streaming Communication in Multi-Agent Reasoning : https://arxiv.org/abs/2606.05158
- GitHub — EnVision-Research/StreamMA : https://github.com/EnVision-Research/StreamMA
- Project page — StreamMA : https://zhenyangcs.github.io/StreamMA-website/
