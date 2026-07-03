---
title: "WorldDirector : mémoire dynamique persistante pour simulateurs de monde"
description: "Un papier arXiv propose un simulateur vidéo contrôlable qui sépare orchestration des mouvements et génération visuelle pour préserver l’identité des objets hors champ."
pubDate: 2026-07-03
category: "radar"
tags: ["world-models", "video-generation", "agents", "embodied-ai"]
author: "Labo IA"
draft: false
sources:
  - label: "arXiv — WorldDirector: Building Controllable World Simulators with Persistent Dynamic Memory"
    url: "https://arxiv.org/abs/2607.02517v1"
  - label: "Project page — WorldDirector"
    url: "https://worlddirector.github.io/"
---

Le sujet est intéressant pour une raison simple : **WorldDirector** ne vend pas juste un énième world model. Le papier décrit un cadre de simulation vidéo contrôlable qui cherche à conserver une **mémoire dynamique persistante** des objets, y compris après qu’ils aient quitté le champ de vue.

L’idée centrale est assez propre :
- un **LLM** coordonne les trajectoires 3D et les mouvements de caméra ;
- ces trajectoires servent ensuite de **signaux de contrôle** pour la génération vidéo ;
- la génération visuelle est séparée de l’orchestration sémantique des mouvements.

Le résultat annoncé : des scènes plus longues, plus contrôlables, et surtout une identité visuelle qui survit aux allers-retours hors champ. C’est exactement le genre de promesse qui vaut une place en **radar** : plausible, utile, mais pas encore assez établi pour un article de fond.

Si les démonstrations et les résultats tiennent la route, ça touche directement les **simulators**, les **agents incarnés** et la génération vidéo longue. Les papiers “contrôlables” font souvent beaucoup de bruit ; celui-ci, au moins, a une idée claire sous le capot.