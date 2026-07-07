---
title: "Les LLMs encodent la longueur restante de réponse"
description: "Un papier arXiv montre qu’on peut décoder linéairement une estimation de la longueur de sortie restante à partir des états cachés de modèles open-weight. Un signal utile pour les agents et le pilotage de budget, à confirmer sur d’autres familles de modèles."
pubDate: 2026-07-07
category: "radar"
tags: ["llm", "probes", "open-weight", "agents", "arxiv"]
author: "Labo IA"
draft: false
sources:
  - label: "arXiv — How Much is Left? LLMs Linearly Encode Their Remaining Output Length"
    url: "https://arxiv.org/abs/2607.05316v1"
---

Le papier est intéressant parce qu’il ne prétend pas que le modèle "compte" exactement ses tokens restants. Il montre quelque chose de plus subtil : une estimation approximative de la longueur de sortie serait **déjà présente dans les représentations internes** et **linéairement décodable**.

Les auteurs testent des **probes linéaires** sur des états cachés gelés de **trois modèles open-weight 7–8B** et sur **sept jeux de données de complétion**. Leur résultat le plus utile pour nous : la longueur totale de réponse semble décodable dès le **dernier état caché du prompt**, donc avant même qu’un token soit généré.

Ce n’est pas encore un article de fond, mais c’est un bon signal radar : si ça se confirme au-delà de ces modèles, on tient un outil potentiel pour mieux estimer le **budget de génération**, surveiller des **agents** en cours d’exécution, ou détecter des comportements de **rétractation / reprise** pendant la sortie. Bref, du signal exploitable, pas du bruit cosmétique — ce qui est déjà une petite victoire.
