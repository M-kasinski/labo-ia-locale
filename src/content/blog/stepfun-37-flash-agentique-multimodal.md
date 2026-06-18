---
title: "Step 3.7 Flash : le modèle agentique qui mise sur 11B paramètres actifs"
description: "StepFun publie Step 3.7 Flash, un MoE multimodal open-weight conçu pour les workflows agentiques rapides, avec 196B paramètres de backbone et seulement 11B actifs par token."
pubDate: 2026-06-06
category: "veille"
tags: ["stepfun", "open-weight", "agents", "multimodal", "coding"]
author: "Veille IA"
draft: false
sources:
  - label: "StepFun — Step 3.7 Flash official blog"
    url: "https://static.stepfun.com/blog/step-3.7-flash/"
  - label: "MarkTechPost — StepFun releases Step 3.7 Flash"
    url: "https://www.marktechpost.com/2026/05/29/stepfun-releases-step-3-7-flash-a-198b-moe-vision-language-model-for-coding-agents-and-search-workflows/"
  - label: "GitHub — stepfun-ai/Step-3.7-Flash"
    url: "https://github.com/stepfun-ai/Step-3.7-Flash"
---

StepFun a publié **Step 3.7 Flash**, un modèle open-weight multimodal pensé moins comme un chatbot généraliste que comme une brique d’exécution pour agents. Le modèle est annoncé le **29 mai 2026** et se positionne clairement sur un axe devenu central : non pas battre tous les frontier models en score brut, mais faire tourner des boucles agentiques vite, avec vision, outils, recherche et code.

La fiche officielle parle d’un modèle **Flash** pour le monde réel : voir, penser, agir, jusqu’à **400 tokens par seconde** selon StepFun. Sous le capot, Step 3.7 Flash combine un backbone langage de **196B paramètres** et un encodeur vision **ViT de 1,8B paramètres**. MarkTechPost résume l’ensemble comme un modèle MoE vision-langage d’environ **198B paramètres**, avec seulement **~11B paramètres actifs** par token. C’est le cœur du sujet : StepFun essaie d’offrir une capacité de grand modèle avec un coût d’inférence proche d’un modèle dense beaucoup plus petit.

## Le pari : l’efficacité agentique plutôt que la taille décorative

Depuis un an, les modèles « Flash » ne sont plus seulement des versions cheap de modèles plus gros. Ils deviennent parfois les vrais moteurs de workflows : agents de code, analyse visuelle, recherche web, routage d’outils, tâches répétées où le coût total dépend du nombre de tours et pas seulement du prix d’un appel.

Step 3.7 Flash s’inscrit exactement là. StepFun le décrit comme un modèle capable de comprendre des **interfaces produit**, documents, graphiques, captures d’écran, scènes naturelles et tableaux denses, puis d’écrire du code ou d’appeler des outils en conséquence. La nouveauté majeure face à Step 3.5 Flash est le support multimodal natif : la génération précédente était text-only, alors que 3.7 ajoute une pile vision dédiée.

Le choix MoE est pragmatique. Avec **11B actifs**, le modèle ne paie pas tout son budget de **196B+1,8B** à chaque token. Cela ne rend pas l’inférence gratuite, mais cela change le profil coût/latence. Pour un agent qui doit lire un écran, exécuter du Python, chercher une source, revenir sur son plan et produire un correctif, le débit devient une métrique produit, pas un benchmark de salon.

## Vision, recherche et outils : trois briques pour agents réels

L’annonce StepFun insiste sur quatre capacités : compréhension multimodale, recherche web et visuelle, usage d’outils fiable, compatibilité avec les écosystèmes agents. Le modèle n’est pas présenté comme devant tout mémoriser dans ses poids. Au contraire, StepFun écrit que pour un modèle de cette échelle, l’objectif est de mieux **appeler la connaissance** quand elle est nécessaire : planifier la recherche, filtrer les preuves, élargir les requêtes, reconnaître des entités longues traînes ou récentes.

C’est une position saine. Les agents sérieux ne devraient pas inventer une jurisprudence, une version de package ou un tarif cloud à partir de leur mémoire paramétrique. Ils doivent récupérer, vérifier et synthétiser. Step 3.7 Flash est donc évalué sur des tâches avec outils et recherche, pas seulement sur des QCM hors-sol.

La partie multimodale est tout aussi importante. Les workflows agentiques modernes passent de plus en plus par des captures d’écran, GUIs, documents scannés, tableaux et graphiques. Un modèle qui peut lire une interface puis décider quel outil appeler devient plus utile qu’un pur modèle texte, même si ce dernier a un meilleur score académique. Comme toujours, la robustesse réelle dépendra de cas pénibles : formulaires ambigus, tableaux illisibles, icônes non standard, screenshots compressés. Les démos aiment les captures propres ; les back-offices d’entreprise, eux, ont souvent l’élégance graphique d’un fax ressuscité.

## Benchmarks : bons signaux, mais beaucoup de chiffres vendor

StepFun publie plusieurs résultats. Sur **SWE-Bench Pro**, Step 3.7 Flash est annoncé à **56,3**, contre **51,3** pour Step 3.5 Flash. Sur **Terminal-Bench 2.1**, l’annonce indique environ **59,5 / 59,6**, contre **53,4** pour 3.5. Sur **ClawEval-1.1**, StepFun donne **67,1**, et sur **SimpleVQA avec outil**, **79,2**. Le blog mentionne aussi **95,3** sur V* avec Python.

Ces chiffres sont intéressants, mais il faut les traiter avec la bonne température. StepFun précise que certaines comparaisons reposent sur des tests internes, des résultats officiels rapportés par d’autres acteurs, ou des configurations différentes selon les modèles. Ce n’est pas disqualifiant ; c’est habituel dans les sorties de modèles. Mais cela veut dire qu’on ne doit pas lire le tableau comme une vérité gravée dans du silicium.

MarkTechPost reprend également un claim notable : avec **Advisor Mode**, StepFun affirme que Step 3.7 Flash atteindrait **76,3% sur SWE-Bench Verified** à **0,19 dollar par tâche**, contre **78,7%** et **1,76 dollar** pour Claude Opus 4.6 dans cette comparaison. Le ratio affiché — 97% de la performance pour environ un neuvième du coût — est séduisant. Mais il s’agit de chiffres StepFun internes. À ce stade, le claim utile est moins « StepFun bat Claude » que « StepFun teste explicitement des architectures où un modèle Flash gère la boucle courante et escalade seulement aux moments difficiles ».

Ce pattern est probablement plus important que le score exact. Les agents de production ne seront pas toujours mono-modèle. Ils utiliseront des modèles rapides pour l’exécution, des modèles plus forts pour la planification ou la récupération d’échec, et des règles de routage pour contenir le coût. Step 3.7 Flash veut occuper cette place : le moteur qui tourne souvent, pas forcément l’oracle qu’on appelle rarement.

## Compatibilité écosystème : StepFun parle aux builders

Le blog officiel liste une compatibilité avec des environnements comme **Claude Code**, **KiloCode**, **Hermes Agent**, **OpenClaw**, **OpenCode**, **RooCode** et des workflows à base de skills. Cette partie est moins spectaculaire que les paramètres, mais plus révélatrice du marché. Les modèles ne gagnent plus seulement par API chat ; ils gagnent quand ils s’intègrent dans des harnais, schemas d’outils, agents de coding, navigateurs et environnements shell.

StepFun publie aussi des ressources publiques : GitHub, Hugging Face, ModelScope, et accès via ses plateformes, OpenRouter et NVIDIA NIM selon l’annonce. La licence indiquée par MarkTechPost est **Apache 2.0**, ce qui rend le modèle plus facile à intégrer commercialement que des poids à licence restrictive. Il faudra évidemment lire les conditions exactes des artefacts et des fournisseurs, mais le signal est ouvert.

## Ce que Step 3.7 Flash n’est pas

Step 3.7 Flash n’est pas un frontier model généraliste destiné à remplacer GPT, Claude ou Gemini dans tous les cas. Les propres tableaux de StepFun montrent que les modèles fermés restent devant sur plusieurs benchmarks de haut niveau, notamment Terminal-Bench ou GDPval. Ce n’est pas non plus une preuve définitive que les petits actifs MoE résolvent la fiabilité agentique : un modèle rapide peut échouer plus vite, ce qui est une forme de progrès assez discutable.

Mais la sortie est importante parce qu’elle prend au sérieux le coût complet d’un agent : latence, nombre de tours, capacité multimodale, recherche, outils, compatibilité harnais, variance entre scaffolds. Dans les workflows réels, un modèle légèrement moins « intelligent » mais plus prévisible, plus rapide et moins cher peut être meilleur qu’un modèle frontier appelé à chaque micro-décision.

La question à suivre est donc simple : des évaluations indépendantes reproduiront-elles les gains annoncés sur SWE-Bench Pro, Terminal-Bench, ClawEval et les scénarios multimodaux avec outils ? Si oui, Step 3.7 Flash pourrait devenir un modèle de travail très attractif pour les agents open-weight. Pas le plus brillant dans la pièce, peut-être. Mais celui qui fait les tâches sans vider la carte bancaire — ce qui, dans une entreprise, finit souvent par passer pour du génie.

## Sources

- StepFun — Step 3.7 Flash official blog: https://static.stepfun.com/blog/step-3.7-flash/
- MarkTechPost — StepFun releases Step 3.7 Flash: https://www.marktechpost.com/2026/05/29/stepfun-releases-step-3-7-flash-a-198b-moe-vision-language-model-for-coding-agents-and-search-workflows/
- GitHub — stepfun-ai/Step-3.7-Flash: https://github.com/stepfun-ai/Step-3.7-Flash
