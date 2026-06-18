---
title: "VSTAT : les modèles multimodaux voient la vidéo, mais suivent mal l’histoire"
description: "Un benchmark NYU/KAIST montre que les MLLM restent loin des humains dès qu’il faut suivre des états visuels dans une vidéo longue."
pubDate: 2026-06-05
category: "veille"
tags: ["multimodal", "benchmarks", "video", "research", "agents"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — Benchmarking Visual State Tracking in Multimodal Video Understanding"
    url: "https://arxiv.org/abs/2606.03920"
  - label: "Project page — VSTAT Visual State Tracking Benchmark"
    url: "https://vision-x-nyu.github.io/vstat-site/"
  - label: "GitHub — vision-x-nyu/vstat"
    url: "https://github.com/vision-x-nyu/vstat"
  - label: "Hugging Face — nyu-visionx/VSTAT"
    url: "https://huggingface.co/collections/nyu-visionx/vstat"
---

Les modèles multimodaux savent décrire une image, résumer une vidéo courte, reconnaître une scène, parfois même produire une analyse convaincante avec le ton assuré d’un expert qui a dormi huit heures. Mais comprendre une vidéo ne consiste pas seulement à reconnaître des moments isolés. Il faut suivre des objets, des états, des positions, des changements et leur ordre. C’est exactement ce que teste **VSTAT**, un nouveau benchmark publié sur arXiv le **2 juin 2026** par des chercheurs de **NYU** et **KAIST**.

Le résultat principal est simple, presque brutal : les meilleurs modèles actuels restent très loin des humains lorsqu’il faut maintenir un état visuel dans le temps. Sur la page projet, les humains atteignent **90,5** de score moyen, tandis que le meilleur modèle listé, **Gemini-3.1 Pro low**, atteint **44,4**. La baseline par fréquence est à **37,8**, la baseline aléatoire à **26,1**. Autrement dit, le meilleur modèle fait mieux que le hasard sophistiqué, mais pas de quoi lui confier le montage d’une armoire sans vérifier les vis une par une.

## Ce que VSTAT mesure vraiment

VSTAT signifie **Visual STAte Tracking**. Le benchmark cherche à diagnostiquer une capacité précise : suivre des états visuels fins au fil d’une vidéo longue. Il ne suffit pas de repérer un objet ou de comprendre une scène globale. Le modèle doit maintenir une représentation dynamique : combien d’objets restent, où se trouve telle entité, quelle couleur ou quel attribut a changé, dans quel ordre les événements se sont produits.

Le dataset contient **834 clips vidéo** et **1 500 questions**. Les vidéos proviennent de trois sources : rendus synthétiques, vidéos enregistrées par les auteurs, et séquences issues de YouTube. Les tâches couvrent **39 types** et sont structurées autour de trois éléments d’état — **count**, **location**, **attribute** — et quatre formes de structure — **atomic**, **sequence**, **set**, **dict**.

La propriété centrale du benchmark est bien choisie : les questions ne peuvent pas être résolues à partir d’une seule frame ou d’un court segment évident. Les événements critiques peuvent être espacés, occultés, visuellement similaires ou distribués entre plusieurs objets. Le modèle doit donc regarder dans la durée, intégrer, mettre à jour, puis répondre. C’est moins spectaculaire qu’une démo de génération vidéo, mais beaucoup plus révélateur pour l’intelligence multimodale réelle.

## Le grand écart humain-modèle

La page projet met en avant un écart de **46 points** entre humains et meilleurs modèles. Les humains obtiennent **90,5** en moyenne, avec **92,8** sur les questions de comptage, **89,9** sur la localisation et **86,4** sur les attributs. Le meilleur score propriétaire listé est **44,4** pour **Gemini-3.1 Pro low**, suivi de **43,9** pour **Gemini-3.1 Pro high**, **39,8** pour **Gemini-3.0 Flash low** et **38,8** pour **Gemini-3.0 Flash high**.

Deux signaux méritent attention. D’abord, les modèles propriétaires plafonnent dans les bas 40, malgré de bonnes performances sur d’autres benchmarks vidéo. Ensuite, augmenter le “thinking budget” ne semble pas aider ici : la page projet indique même que les variantes “high” de Gemini font légèrement moins bien que les variantes “low” sur ce leaderboard. Ce n’est pas une preuve générale contre le raisonnement plus long, mais c’est un rappel utile : si le modèle ne perçoit pas l’événement, réfléchir plus longtemps sur une perception ratée ne crée pas l’information manquante.

Côté open-source, le tableau est encore plus dur. Le meilleur modèle ouvert listé, **LLaVA-OV-2-8B**, atteint **35,1**, sous la baseline par fréquence à **37,8**. Les autres modèles listés — Molmo2, Cambrian, Qwen3VL, InternVL, GLM-4.1V-Thinking — restent majoritairement entre les bas 20 et les mid-30. Là encore, prudence : un leaderboard dépend du protocole d’évaluation, du sampling vidéo, de la résolution, du contexte donné au modèle. Mais l’écart avec les humains est suffisamment massif pour ne pas être un artefact mineur.

## Le problème n’est pas seulement le raisonnement

Le papier arXiv avance une conclusion intéressante : les modèles peuvent souvent raisonner correctement dans leurs traces textuelles, mais échouent à percevoir visuellement les événements nécessaires au suivi. C’est une distinction capitale. Beaucoup de discussions sur les MLLM mélangent perception et raisonnement comme si tout relevait d’une capacité générale appelée “compréhension”. VSTAT force à séparer les deux.

Si un modèle voit correctement qu’un cube est déplacé, il peut souvent suivre la logique : position initiale, déplacement, nouvelle position. Le problème est qu’il rate parfois le déplacement, confond deux objets visuellement proches, ou perd une transition pendant une occlusion. Le raisonnement textuel peut alors être parfaitement cohérent — sur de mauvaises prémisses. C’est le genre d’échec le plus dangereux en production : le système paraît logique, mais son monde interne est faux.

Les exemples mis en avant par la page projet sont parlants. Dans une tâche de type Rubik’s cube, le modèle doit suivre un cubie spécifique même lorsqu’il est occulté par moments. Dans d’autres tâches, il doit compter des changements successifs, mémoriser une séquence, ou associer plusieurs entités à des états finaux. Ce sont des compétences banales pour un humain attentif, mais difficiles pour des modèles qui échantillonnent et compressent la vidéo en représentations partielles.

## Les agents vidéo ne sauvent pas encore la mise

VSTAT ne se contente pas de tester des MLLM “monolithiques”. L’abstract indique que les auteurs ont aussi évalué, de façon préliminaire, des approches agentiques récentes, dont des agents vidéo basés sur MLLM et des coding agents. Leur conclusion : ces approches ne résolvent pas facilement les échecs de visual state tracking et restent en dessous sur VSTAT.

C’est un point important pour l’industrie. La réponse réflexe à une limite de modèle est souvent : “mettons un agent autour”. Parfois, cela marche. Un agent peut découper une tâche, appeler un outil, inspecter plusieurs segments, vérifier une hypothèse. Mais pour le suivi visuel fin, l’agent dépend encore de la qualité perceptive des briques qu’il orchestre. Si chaque inspection rate les micro-événements ou confond les objets, l’orchestration devient surtout une manière plus longue de se tromper.

Cela ne veut pas dire que les agents vidéo sont inutiles. Au contraire, VSTAT pourrait aider à concevoir de meilleurs agents : découpage temporel adaptatif, mémoire d’état explicite, suivi d’entités, vérification croisée entre frames, outils spécialisés de tracking, segmentation ou optical flow. Mais le benchmark montre que l’emballage agentique ne suffit pas. La plomberie doit voir clair.

## Pourquoi ce benchmark compte

VSTAT est intéressant parce qu’il cible une capacité fondamentale pour les futurs usages multimodaux. Un assistant qui analyse une vidéo de maintenance doit suivre l’état d’une pièce. Un système robotique doit savoir où un objet a été déplacé. Un outil de sécurité doit comprendre une séquence d’actions, pas seulement reconnaître “une personne dans une pièce”. Un assistant pédagogique qui regarde une manipulation doit savoir ce qui a changé et quand. Dans tous ces cas, une description globale est insuffisante.

Le benchmark met aussi en évidence une faiblesse des évaluations vidéo actuelles. Si un modèle peut réussir en capturant quelques frames saillantes, il peut donner l’illusion d’une compréhension temporelle. VSTAT empêche cette échappatoire : les questions exigent une intégration continue. C’est moins flatteur pour les modèles, donc plus utile pour les ingénieurs.

Il faut évidemment garder les précautions habituelles. Le papier est une prépublication arXiv, le benchmark est récent, et les résultats devront être reproduits avec d’autres modèles, d’autres réglages et peut-être d’autres politiques d’échantillonnage vidéo. Les scores publics peuvent évoluer rapidement. Mais la direction est saine : arrêter de mesurer seulement “le modèle reconnaît-il la scène ?” et demander “le modèle suit-il ce qui arrive ?”.

## Ce qu’il faut retenir

VSTAT montre que les MLLM actuels ont encore du mal avec une compétence très humaine : maintenir un modèle d’état visuel dans le temps. Ils peuvent décrire, résumer, raisonner en texte, mais perdre la trace des changements qui rendent la réponse correcte. C’est une limite technique profonde, pas un simple problème de prompt.

La prochaine étape ne sera probablement pas un unique modèle plus bavard. Il faudra de meilleures représentations temporelles, des mécanismes de tracking explicite, des outils perceptifs spécialisés, et des agents capables de vérifier leurs propres états intermédiaires. Pour l’instant, les modèles regardent la vidéo. Ils ne suivent pas encore toujours l’histoire.

## Sources

- arXiv — Benchmarking Visual State Tracking in Multimodal Video Understanding: https://arxiv.org/abs/2606.03920
- Project page — VSTAT: https://vision-x-nyu.github.io/vstat-site/
- GitHub — vision-x-nyu/vstat: https://github.com/vision-x-nyu/vstat
- Hugging Face — nyu-visionx/VSTAT: https://huggingface.co/collections/nyu-visionx/vstat
