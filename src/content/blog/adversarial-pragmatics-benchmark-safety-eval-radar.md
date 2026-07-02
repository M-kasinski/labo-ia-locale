---
title: "Adversarial Pragmatics : un benchmark pour tester les ambiguïtés des évaluations IA"
description: "Un papier arXiv propose un cadre de benchmark pour distinguer instruction, refus, conformité, risque et confiance du juge. Utile pour les tests de sécurité, sans gonfler le signal artificiellement."
pubDate: 2026-07-02
category: "radar"
tags: ["safety", "benchmarks", "agents", "llm"]
author: "Labo IA"
draft: false
sources:
  - label: "arXiv — Adversarial Pragmatics for AI Safety Evaluation"
    url: "https://arxiv.org/abs/2607.01153v1"
  - label: "arXiv PDF — Adversarial Pragmatics for AI Safety Evaluation"
    url: "https://arxiv.org/pdf/2607.01153v1"
---

Les benchmarks de sécurité IA ont souvent le même défaut : ils compressent trop de choses dans un verdict binaire. Le modèle a-t-il suivi l’instruction ? A-t-il refusé correctement ? A-t-il violé une consigne ? Très bien, mais on perd vite ce qui compte vraiment : l’ambiguïté de l’énoncé, le conflit d’ordres, le rôle d’un commandement imbriqué, ou simplement l’incertitude du juge.

Le papier **"Adversarial Pragmatics for AI Safety Evaluation: A Benchmark for Instruction Conflict, Embedded Commands, and Policy Ambiguity"** propose précisément un cadre pour sortir de ce raccourci. L’idée n’est pas de faire un leaderboard de plus. L’idée est de mieux séparer les causes d’un échec ou d’un succès : **succès de tâche**, **conformité à la politique**, **risque de sécurité**, **résultat de refus** et **confiance de l’évaluateur**.

Le cœur du travail est méthodologique. Les auteurs annoncent :
- une **taxonomie linguistiquement contrôlée** ;
- un **seed benchmark de 18 items** avec métadonnées validées ;
- un **pilot local de 54 lignes** ;
- des métriques pour la **validité du juge**, l’**ambiguïté diagnostique** et la **dérive de taxonomie**.

Les cas ciblés sont très concrets : conflit d’instructions, commandes imbriquées, citation, ambiguïté de portée, deixis, actes de langage indirects, transcripts multi-tours d’agents. Autrement dit, exactement les endroits où un test “réussi/raté” devient presque décoratif.

Pourquoi c’est intéressant ? Parce que ce type de benchmark peut servir à mieux valider des **LLM judges**, des jeux de vérité terrain, des tests de prompt injection et la documentation sécurité. C’est moins spectaculaire qu’un nouveau modèle, mais souvent plus utile. Les lumières clignotent moins, la plomberie avance davantage.

À ce stade, je le classerais en **radar** plutôt qu’en article de fond : le cadre est prometteur, mais on reste sur une prépublication et sur une proposition de benchmark. Si le dépôt et les résultats se confirment bien en pratique, il y a là un vrai sujet de veille pour les équipes qui évaluent des agents ou des systèmes de sécurité.
