---
title: "CUA-HandCrafted : les agents navigateur résistent, les agents de code cèdent encore"
description: "Un papier arXiv teste la sécurité des computer-using agents avec 793 épisodes et montre que la robustesse aux injections dépend fortement du domaine : navigateur d’un côté, coding agent de l’autre."
pubDate: 2026-06-06
category: "veille"
tags: ["agents", "sécurité", "benchmark"]
author: "Veille IA"
draft: false
sources:
  - label: "Article arXiv Domain-Conditioned Safety in Frontier Computer-Using Agents"
    url: "https://arxiv.org/abs/2606.05233"
  - label: "Version HTML du papier"
    url: "https://arxiv.org/html/2606.05233"
  - label: "Artifact Zenodo cité par le papier"
    url: "https://doi.org/10.5281/zenodo.20034379"
---

La sécurité des agents IA adore les phrases définitives. “Les prompt injections sont résolues.” “Les agents navigateur sont dangereux.” “Les modèles frontier sont robustes.” Le papier **“Domain-Conditioned Safety in Frontier Computer-Using Agents”**, soumis sur arXiv le 3 juin 2026, propose une lecture moins confortable : la robustesse n’est pas une propriété générale d’un modèle. Elle dépend du **domaine d’action**.

Le papier introduit **CUA-HandCrafted**, un benchmark public de **793 épisodes** pour agents utilisant un navigateur. Il teste des attaques par prompt injection sur des tâches web multi-étapes, puis compare ces résultats avec un benchmark frère côté agent de code. Le résultat est intéressant parce qu’il refuse les deux caricatures : les agents navigateur frontier testés résistent très bien aux attaques manuscrites, mais cette résistance ne se transfère pas proprement aux agents de code utilisant les mêmes familles de modèles.

En clair : le blindage existe, mais il n’est pas uniformément réparti. Comme souvent en sécurité, le diable n’est pas dans le slogan. Il est dans la surface d’attaque.

## Un benchmark navigateur structuré, pas juste trois prompts piégés

CUA-HandCrafted n’est pas un simple recueil de phrases du type “ignore les instructions précédentes”. Le benchmark couvre **24 tâches web multi-étapes**, **6 tâches de lecture single-step**, **56 templates d’attaque**, **8 familles d’attaque**, **5 canaux d’injection** et **4 configurations de prompt système**. Les sites simulés incluent notamment portail RH, dashboard projet, CRM/helpdesk, banque, shopping, email, forum et paramètres.

Les familles d’attaque couvrent des cas classiques mais concrets : déni de service, action non autorisée, exfiltration, hijacking d’objectif, phishing d’identifiants, ingénierie sociale, usurpation d’autorité ou injection multi-étapes. Les canaux testés incluent du texte visible, du texte caché, des popups, des modifications du DOM et des textes d’aide.

Ce point compte. Beaucoup de débats sur les agents restent trop abstraits : on parle de “prompt injection” comme d’un objet unique. En pratique, une instruction malveillante dans un email, un tooltip, un `aria-label`, une popup ou une page de documentation ne touche pas le système de la même façon. Un agent navigateur perçoit l’environnement via capture visuelle, arbre d’accessibilité, DOM partiel, descriptions intermédiaires et historique d’action. La forme de l’injection change donc la menace.

## Le résultat navigateur : 0 succès sur 140 attaques multi-étapes

Contre **Claude Sonnet 4.6** et **GPT-5.4**, le papier rapporte **0 succès sur 140 attaques multi-étapes**, avec une borne supérieure de Clopper-Pearson à **2,60 %** pour l’intervalle de confiance à 95 %. Les auteurs mentionnent aussi un comptage brut initial de **2/158**, attribué à un problème de dérive de cible d’évaluation sur une tâche bancaire obsolète ; après exclusion, le résultat multi-étapes principal reste à zéro succès.

C’est un signal fort, mais il faut le lire correctement. Le papier ne dit pas que les agents navigateur sont sûrs en production. Il dit que, dans ce protocole, des attaques **hand-crafted** reproduisant des catégories connues ne passent pas contre ces modèles frontier récents.

La nuance est importante. Les auteurs opposent leurs résultats à des travaux de red-teaming qui rapportaient des taux de succès élevés, parfois entre **42 % et 98 %**, mais souvent sur des modèles retirés, avec mise en avant du modèle le plus vulnérable du panel, et surtout avec des chaînes d’attaque optimisées par RL qui ne sont pas toujours publiées. Si l’attaque exacte n’est pas publiée, la reproductibilité devient fragile. Une catégorie d’attaque ne suffit pas : le texte optimisé peut faire toute la différence.

## Le prompt système ne suffit pas à expliquer la robustesse

Le papier teste aussi des ablations de prompt système. L’objectif est de savoir si la résistance vient simplement d’instructions de sécurité ajoutées autour du modèle, ou si elle est plus profondément intégrée. Selon les auteurs, même en variant les configurations — jusqu’à des prompts beaucoup moins protecteurs — les attaques navigateur manuscrites restent sans succès dans l’échantillon principal.

Ils en concluent que la résistance observée “vit” probablement dans les poids du modèle, pas seulement dans le texte du system prompt. C’est plausible, mais à manier prudemment : les modèles évalués sont des systèmes complets, avec politiques, entraînement, capacités multimodales et comportements d’agent. Attribuer précisément la robustesse aux poids plutôt qu’à l’ensemble du stack reste délicat sans accès complet aux détails internes.

Ce que l’on peut retenir plus sûrement : dans ce benchmark, enlever ou affaiblir les consignes de sécurité ne suffit pas à faire s’effondrer les agents navigateur testés. C’est déjà une observation utile.

## Le retournement : côté coding agent, les mêmes modèles tombent

La partie la plus intéressante du papier arrive ensuite. Les auteurs comparent avec un benchmark frère côté agent de code, **SkillBench**, sur des attaques de skill injection. Là, le comportement change brutalement : le papier rapporte jusqu’à **40/40 succès**, soit **100 %**, pour Claude Sonnet 4.6 dans une condition, et jusqu’à **79/100**, soit **79 %**, pour GPT-5.4. Les moyennes cross-method citées sont de **33,3 %** pour Sonnet 4.6 et **66,8 %** pour GPT-5.4.

Il ne faut pas mélanger trop vite les protocoles : navigateur et code ne sont pas la même tâche, pas les mêmes outils, pas les mêmes objectifs, pas les mêmes définitions d’échec. Mais c’est précisément le point du papier. La sécurité des agents est **domain-conditioned**. Un modèle peut être durci sur une surface très visible — le navigateur, massivement red-teamé — tout en restant vulnérable sur une autre surface où les patterns d’attaque, les artefacts et les actions autorisées diffèrent.

Pour les équipes qui déploient des agents de code, c’est un rappel assez froid : la robustesse démontrée dans un navigateur ne couvre pas automatiquement un dépôt Git, un système de plugins, un fichier de configuration ou une compétence installée par l’utilisateur.

## Pourquoi les taux d’attaque doivent devenir vectoriels

La proposition implicite du papier est saine : arrêter de parler d’un taux de succès d’attaque unique pour “le modèle”. Un agent a plusieurs surfaces : navigateur, terminal, éditeur, fichiers, outils SaaS, emails, documents, MCP, APIs internes, mémoire persistante. Un seul ASR global masque les différences.

Les auteurs plaident pour des rapports plus précis : ASR par domaine, par canal d’injection, par famille d’attaque, par profondeur de tâche et par configuration système. C’est moins vendeur qu’un gros chiffre, mais beaucoup plus exploitable. Dire “0 % sur attaques navigateur manuscrites multi-étapes dans CUA-HandCrafted” est utile. Dire “modèle sécurisé contre les prompt injections” est trop large, donc probablement faux.

C’est aussi une bonne nouvelle méthodologique : les benchmarks d’agents commencent à ressembler à de vrais bancs d’essai de systèmes, pas seulement à des questionnaires avec un wrapper d’outil. On mesure des trajectoires, des surfaces, des actions et des échecs. C’est plus laborieux. C’est aussi le prix d’une évaluation qui ne raconte pas des histoires.

## Ce qu’il faut retenir

CUA-HandCrafted apporte deux messages. D’abord, les agents navigateur frontier récents semblent beaucoup plus résistants aux attaques manuscrites simples ou semi-structurées que ne le suggèrent certains titres alarmistes. Ensuite, cette robustesse ne doit pas être extrapolée aux autres modalités d’agent, notamment le code.

Le papier ne ferme donc pas le dossier de la sécurité agentique. Il le rend plus précis. La bonne question n’est plus “ce modèle est-il résistant aux prompt injections ?” mais “sur quelle surface, avec quels outils, quelles attaques, quelles traces et quel protocole reproductible ?”

C’est moins confortable qu’un verdict binaire. Mais pour des agents qui vont cliquer, coder, envoyer, modifier et déployer, le confort est une métrique assez médiocre.

## Sources

- [Domain-Conditioned Safety in Frontier Computer-Using Agents sur arXiv](https://arxiv.org/abs/2606.05233)
- [Version HTML du papier](https://arxiv.org/html/2606.05233)
- [Artifact Zenodo cité par le papier](https://doi.org/10.5281/zenodo.20034379)
