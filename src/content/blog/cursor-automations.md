---
title: "Cursor : L'arrivée des Automations et du Computer Use pour les agents"
description: "Cursor introduit la commande /automate, de nouveaux déclencheurs GitHub/Slack et la capacité pour les agents cloud d'utiliser le Computer Use."
pubDate: 2026-06-18
category: "veille"
tags: ["cursor", "automation", "computer-use", "agents"]
author: "Labo IA Locale"
draft: false
sources: [{ label: "Cursor Changelog", url: "https://cursor.com/changelog/06-18-26" }]
---

# Cursor : L'arrivée des Automations et du Computer Use pour les agents

Cursor continue de transformer l'expérience de développement en intégrant des agents capables de réagir à des événements et d'agir de manière autonome sur le système. La mise à jour du 18 juin 2026 marque un tournant avec l'introduction des **Automations**.

### La commande `/automate` : Créer des workflows en langage naturel

Le cœur de cette mise à jour est la commande `/automate`. Elle permet de configurer une automatisation directement depuis une session d'agent locale en la décrivant simplement en langage naturel. L'agent s'occupe de configurer lui-même les déclencheurs (*triggers*), les instructions et les outils nécessaires pour réaliser la tâche.

### Déclencheurs et intégrations : Slack et GitHub

L'automatisation devient véritablement réactive grâce à de nouveaux points d'entrée :

* **Slack** : Vous pouvez désormais déclencher une automatisation en réagissant à un message avec un emoji spécifique. Un excellent moyen de déléguer des tâches simples sans quitter la discussion.
* **GitHub** : L'intégration est renforcée avec cinq nouveaux déclencheurs, permettant de réagir à des commentaires sur les issues, des soumissions de revue de PR, ou même à la fin d'un workflow GitHub Actions.

### Computer Use : Les agents cloud prennent le contrôle

L'une des nouveautés les plus marquantes est l'activation par défaut du **Computer Use** pour les automatisations lancées dans le cloud. 

Désormais, les agents peuvent utiliser leur propre environnement informatique pour produire des démonstrations ou des artefacts de leur travail. Il suffit de demander à l'agent d'inclure une "démo" dans ses instructions pour qu'il puisse capturer et présenter le résultat de ses actions sur un système.

### Résumé des améliorations
* **Persistance** : Les automatisations peuvent être sauvegardées même si elles sont incomplètes (pratique pour configurer des authentifications MCP).
* **Productivité** : Les agents peuvent désormais ouvrir des Pull Requests par défaut.
* **Gestion de la mémoire** : Possibilité de supprimer des fichiers de mémoire directement depuis l'interface ou via l'agent lui-même.

***
*Article généré pour la veille technologique du Labo IA Locale.*
