---
title: "Agentic-MME : le benchmark qui regarde enfin comment les agents multimodaux raisonnent"
description: "Agentic-MME évalue les agents multimodaux sur leurs trajectoires, leurs appels outils et leur efficacité, pas seulement sur la bonne réponse finale."
pubDate: 2026-06-04
category: "veille"
tags: ["agents", "multimodal", "benchmarks", "research", "tool-use"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — Agentic-MME: What Agentic Capability Really Brings to Multimodal Intelligence?"
    url: "https://arxiv.org/abs/2604.03016"
  - label: "Project page — Agentic-MME"
    url: "https://agenticmme.github.io/"
  - label: "GitHub — ChoS3nE11ven/Agentic-MME"
    url: "https://github.com/ChoS3nE11ven/Agentic-MME"
  - label: "Hugging Face Papers — Agentic-MME"
    url: "https://huggingface.co/papers/2604.03016"
---

La plupart des benchmarks multimodaux ont un défaut assez confortable : ils regardent la réponse finale. Bonne réponse, mauvais chemin ? Ça passe souvent. Mauvaise réponse, mais bonne stratégie interrompue par un détail d’outil ? Ça disparaît dans le même zéro. **Agentic-MME** attaque précisément cette zone grise. Le papier, publié sur arXiv sous le titre **“Agentic-MME: What Agentic Capability Really Brings to Multimodal Intelligence?”**, propose un benchmark qui audite la trajectoire d’un agent multimodal : ce qu’il cherche, les outils visuels qu’il appelle, les preuves qu’il extrait, et la quantité de raisonnement inutile qu’il accumule au passage.

Le sujet mérite attention parce que les modèles multimodaux ne sont plus seulement des classifieurs d’images bavards. Ils deviennent des agents capables de recadrer une image, zoomer sur un détail, lancer une recherche web, lire une page, puis revenir à l’image avec une hypothèse. C’est plus proche d’un enquêteur que d’un OCR glorifié. Et, comme souvent avec les agents, le problème n’est pas seulement de savoir s’ils peuvent agir. C’est de savoir s’ils agissent correctement, au bon moment, et sans brûler une forêt de tokens pour redécouvrir l’évidence.

## Ce que mesure Agentic-MME

Agentic-MME est présenté comme un **benchmark process-verified** pour les capacités agentiques multimodales. Le dataset contient **418 tâches réelles**, réparties sur **6 domaines** et **3 niveaux de difficulté**. Les auteurs indiquent aussi plus de **2 000 checkpoints étape par étape**, avec en moyenne **plus de 10 heures-personnes d’annotation par tâche**. Ce n’est donc pas un simple quiz visuel avec une couche cosmétique “agent”.

Le benchmark s’intéresse à deux formes d’expansion. La première est la **Visual Expansion** : utiliser des outils visuels pour transformer ou inspecter l’image — crop, rotation, amélioration, zoom, extraction de détails. La seconde est la **Knowledge Expansion** : aller chercher de l’information externe, notamment via recherche web, pour résoudre des tâches où l’image seule ne suffit pas. Cette distinction est utile : beaucoup d’échecs multimodaux viennent précisément du couplage entre perception et connaissance externe, pas de l’une ou de l’autre isolément.

Chaque tâche inclut une trajectoire humaine de référence et des checkpoints intermédiaires. L’évaluation ne demande donc pas seulement : “la réponse finale est-elle correcte ?” Elle demande aussi : “l’agent a-t-il choisi la bonne stratégie de recherche ?”, “a-t-il utilisé le bon outil visuel ?”, “l’artefact produit par l’outil révèle-t-il réellement la preuve attendue ?”, “a-t-il accumulé des appels redondants ?” Ce dernier point est capturé par une métrique d’**overthinking**, qui compare l’efficacité de la trajectoire du modèle à celle d’un humain.

## S-axis et V-axis : deux manières d’échouer

Le papier formalise l’audit autour de deux axes. Le **S-axis** concerne la stratégie et l’expansion de connaissance : qualité des requêtes, pertinence des sources consultées, progression des hypothèses, correspondance avec les checkpoints. Le **V-axis** concerne l’expansion visuelle : les opérations appelées, leur utilité, et le fait que les transformations produisent ou non une preuve exploitable.

C’est une bonne idée parce qu’un agent multimodal peut échouer de plusieurs façons différentes. Il peut voir le bon détail mais chercher la mauvaise chose. Il peut avoir une bonne hypothèse mais ne jamais zoomer au bon endroit. Il peut appeler un outil correct mais mal interpréter son résultat. Un score final unique écrase ces nuances. Un score de processus donne au contraire une cartographie de panne — moins sexy qu’un leaderboard, mais beaucoup plus utile pour construire des systèmes fiables.

La page projet précise aussi que le benchmark inclut **13 outils visuels** et **4 outils web**. Les tâches sont progressives : le niveau 1 vise souvent une opération visuelle décisive ; le niveau 2 combine visualisation et recherche ; le niveau 3 force des boucles itératives où perception, hypothèse et vérification se répondent. C’est exactement le type de charge où les agents actuels donnent parfois l’impression de travailler dur tout en avançant peu. Le costume est impeccable, le dossier reste vide.

## Les résultats : les modèles restent loin des humains

Les chiffres rapportés sont sobres, et plutôt sévères. Dans l’abstract arXiv, le meilleur modèle, **Gemini3-pro**, atteint **56,3 % d’accuracy globale** et tombe à **23,0 % sur les tâches Level-3**. La page projet présente une lecture proche : **56,3 % global**, **93,8 % pour les humains**, et un meilleur score Level-3 indiqué à **33,3 %** selon le tableau mis en avant. Cette différence entre les formulations n’est pas catastrophique, mais elle rappelle une chose : il faut lire les protocoles et les tables, pas seulement les résumés.

Le signal principal, lui, est clair. Même les meilleurs modèles testés restent très loin du niveau humain lorsque la tâche exige une coordination durable entre outils visuels, recherche externe et planification. Les performances se dégradent fortement avec la difficulté. Autrement dit : avoir un modèle multimodal puissant ne suffit pas à obtenir un agent multimodal fiable.

C’est une conclusion importante pour les produits qui vendent du “visual agent” à coups de démos. Beaucoup de démos fonctionnent parce qu’elles ont un chemin court : une image, une question, une réponse. Les workflows réels sont plus sales. Il faut inspecter une capture, identifier un objet ambigu, retrouver un contexte, comparer plusieurs preuves, puis décider. Agentic-MME pousse justement dans cette direction.

## Pourquoi c’est plus intéressant qu’un benchmark de plus

On peut être lassé des benchmarks IA. Chaque semaine apporte son acronyme, son leaderboard, son “state of the art” temporaire. Agentic-MME est plus intéressant parce qu’il déplace la métrique vers la **trajectoire vérifiable**. C’est la même évolution que l’on voit dans les agents de code : mesurer seulement la PR finale ne suffit plus ; il faut comprendre comment l’agent lit les tests, choisit ses commandes, corrige ses hypothèses et s’arrête.

Pour les équipes qui construisent des agents multimodaux, ce type de benchmark suggère une instrumentation concrète : journaliser les appels outils, annoter les checkpoints critiques, distinguer erreur de perception et erreur de recherche, mesurer les actions redondantes. Cela peut aider à concevoir de meilleurs routeurs d’outils, de meilleurs critères d’arrêt, et des systèmes de vérification intermédiaire. Ce ne sont pas des détails de plomberie. Dans les agents, la plomberie est souvent le produit.

## Les limites à garder en tête

Agentic-MME dépend fortement de trajectoires humaines annotées. C’est une force pour l’interprétabilité, mais aussi une limite : une trajectoire humaine de référence peut biaiser ce qui est considéré comme une “bonne” stratégie. Un modèle pourrait trouver un chemin différent, plus court ou simplement non anticipé. Les auteurs essayent de mesurer le processus, mais l’évaluation du processus est toujours plus normative qu’un simple match de réponse.

Autre prudence : le papier est une prépublication arXiv, avec un dépôt GitHub public mais encore modeste. Il faudra voir comment le benchmark se comporte à grande échelle, comment les outils sont stabilisés, et si les résultats se reproduisent avec d’autres implémentations d’agents. Ce n’est pas une raison de l’ignorer. C’est une raison de ne pas le transformer trop vite en vérité de marché.

## Ce qu’il faut retenir

Agentic-MME dit quelque chose de simple et assez inconfortable : les agents multimodaux actuels savent appeler des outils, mais ne savent pas encore toujours s’en servir comme des enquêteurs efficaces. Le progrès ne viendra pas seulement de meilleurs modèles de vision-langage. Il viendra aussi de meilleures trajectoires, de meilleurs audits, et d’une mesure plus fine de la manière dont un agent transforme une image et quelques recherches en preuve exploitable.

Pour une industrie obsédée par la réponse finale, c’est un rappel salutaire : dans les agents, le chemin compte. Surtout quand il se perd.

## Sources

- arXiv — Agentic-MME: https://arxiv.org/abs/2604.03016
- Project page — Agentic-MME: https://agenticmme.github.io/
- GitHub — ChoS3nE11ven/Agentic-MME: https://github.com/ChoS3nE11ven/Agentic-MME
- Hugging Face Papers — Agentic-MME: https://huggingface.co/papers/2604.03016
