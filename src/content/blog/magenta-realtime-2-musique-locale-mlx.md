---
title: "Magenta RealTime 2 : Google pousse la génération musicale open-weight sur Apple Silicon"
description: "Magenta RealTime 2 apporte deux modèles de musique générative temps réel, une pile MLX/C++ et une cible très claire : faire tourner l'audio génératif localement, pas seulement dans un notebook."
pubDate: 2026-06-04
tags: ["audio", "open-weight", "mlx", "apple-silicon"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Dépôt GitHub Magenta RealTime 2"
    url: "https://github.com/magenta/magenta-realtime"
  - label: "Fiche Hugging Face Magenta RealTime"
    url: "https://huggingface.co/google/magenta-realtime"
  - label: "Article Google Magenta RealTime"
    url: "https://magenta.withgoogle.com/magenta-realtime"
  - label: "Paper Live Music Models"
    url: "https://arxiv.org/abs/2508.04651"
---

La génération musicale open-weight avait un problème assez simple : beaucoup de démos, peu de vraie interaction. Générer trente secondes d'audio en batch, c'est utile. Piloter un flux musical pendant qu'il joue, avec une latence assez basse pour rester musical, c'est une autre affaire. C'est précisément le terrain de **Magenta RealTime 2**, la nouvelle version du projet Magenta de Google, dont le dépôt GitHub a été mis à jour le 4 juin 2026 avec une pile beaucoup plus locale qu'avant.

Le signal intéressant pour le Labo n'est pas seulement “Google sort un modèle audio”. C'est le changement d'architecture de déploiement : **MLX pour Apple Silicon**, une bibliothèque Python, un moteur C++ et des exemples d'applications macOS/DAW. Autrement dit, ce n'est pas pensé uniquement pour une API ou un Colab. C'est pensé pour finir dans une machine personnelle, un plugin, un outil créatif ou un setup live.

## Deux tailles : 230M et 2,4B paramètres

D'après le dépôt officiel, Magenta RealTime 2 propose deux variantes : **`mrt2_small`**, un modèle de **230 millions de paramètres**, et **`mrt2_base`**, un modèle de **2,4 milliards de paramètres**. Le premier est annoncé comme capable de streamer en temps réel sur “n'importe quel Mac Apple Silicon”, y compris les MacBook Air. Le second vise une meilleure qualité, mais demande davantage : le dépôt indique qu'il faut une puce de classe **Max** pour le streaming temps réel, avec quelques modèles Pro compatibles et d'autres non.

C'est une distinction importante. Beaucoup de modèles “locaux” le sont en théorie : ils s'exécutent bien hors cloud, mais seulement sur une carte haut de gamme ou avec une latence qui casse l'usage. Ici, Google documente explicitement le matériel compatible pour le streaming. `mrt2_small` sert de point d'entrée réaliste ; `mrt2_base` est le modèle plus ambitieux pour les machines récentes et musclées.

Le dépôt précise aussi que les deux modèles peuvent fonctionner en inférence non temps réel sur Apple Silicon ou GPU NVIDIA via la bibliothèque Python. Donc, même si ta machine ne tient pas le streaming live, elle peut encore servir pour de la génération offline. Ce n'est pas aussi glamour qu'une performance en direct, mais c'est souvent là que les vrais workflows créatifs commencent.

## MLX, JAX et C++ : la pile locale devient sérieuse

La partie la plus notable pour l'IA locale est le support de **MLX**, le framework Apple conçu pour tirer parti de la mémoire unifiée des puces M-series. Le quickstart officiel passe par `uv`, installe `magenta-rt[mlx]`, initialise les modèles nécessaires puis lance une génération avec une commande du type `mrt mlx generate --prompt "disco funk" --duration 4.0 --model=mrt2_base`.

Le projet ne se limite pas à Python. Le dépôt liste aussi **`magentart::core`**, une bibliothèque C++ conçue pour l'inférence audio en streaming, en particulier sur Mac Apple Silicon. C'est un détail qui compte : pour un plugin audio, une application standalone ou une intégration dans une station de travail musicale, C++ reste souvent le chemin le plus crédible. Python est parfait pour prototyper ; C++ est plus rassurant quand il faut tenir une boucle audio sans bégayer comme un grille-pain nerveux.

Les exemples fournis vont dans ce sens : plugin **AUv3**, application macOS autonome, outils d'exploration de prompts et de contrôle par notes. On est donc plus proche d'un kit de développement musical que d'un simple checkpoint posé sur Hugging Face.

## Ce qui vient de la v1 : SpectroStream, MusicCoCa et génération par blocs

La fiche Hugging Face de Magenta RealTime décrit l'architecture générale : un codec audio **SpectroStream**, un modèle d'embedding audio/texte **MusicCoCa**, puis un transformer encodeur-décodeur qui génère les tokens audio. SpectroStream encode de l'audio **48 kHz stéréo** en tokens, tandis que MusicCoCa projette textes et exemples audio dans un même espace de style.

Le papier *Live Music Models* explique l'idée centrale : produire un **flux continu** de musique, pilotable en temps réel par des prompts texte ou audio. La première version de Magenta RealTime utilisait une génération par blocs : contexte audio précédent, embedding de style, puis génération du bloc suivant. L'article Google indiquait par exemple une génération de **2 secondes d'audio en 1,25 seconde** sur un TPU Colab v2-8, soit un facteur temps réel de 1,6.

Attention cependant : ces chiffres documentés concernent la présentation Magenta RealTime initiale et le papier associé, pas nécessairement les performances exactes de Magenta RealTime 2 sur chaque Mac. Pour MRT2, les informations solides disponibles publiquement sont surtout les tailles de modèles, les backends et la matrice de compatibilité matérielle dans le dépôt GitHub. Les benchmarks détaillés par machine restent à vérifier indépendamment.

## Open-weight, mais avec conditions

La fiche Hugging Face indique une combinaison de licences : code sous **Apache 2.0**, poids sous **Creative Commons Attribution 4.0**, avec des conditions d'usage additionnelles, notamment l'interdiction de générer des contenus qui violent les droits de tiers. Google précise aussi ne pas revendiquer de droits sur les sorties générées, mais laisse la responsabilité juridique aux utilisateurs.

Ce n'est donc pas un “faites absolument n'importe quoi” open-source au sens militant. C'est de l'open-weight utilisable, inspectable et intégrable, mais avec une couche de conditions liées aux risques de copyright musical. Pour un média local-first, c'est exactement le genre de nuance à garder : le poids ouvert ne supprime pas magiquement les contraintes de licence, surtout dans l'audio.

## Pourquoi c'est important pour l'IA locale

Magenta RealTime 2 arrive dans un moment où l'IA locale est encore très centrée sur le texte, le code et l'image. L'audio génératif reste plus délicat : contraintes de latence, qualité de sortie, intégration créative, risques de droits. En visant explicitement Apple Silicon, MLX et les plugins, Google donne un signal : la génération musicale locale peut devenir un usage interactif, pas seulement une curiosité de notebook.

Pour les créateurs, le cas d'usage est clair : générer des textures, improviser des pistes, explorer des styles, construire des instruments hybrides. Pour les développeurs, le plus intéressant est peut-être ailleurs : le projet fournit une base pour intégrer un modèle audio génératif dans des applications natives, sans dépendre d'une API temps réel distante.

Il faudra encore des tests indépendants : latence réelle sur M1/M2/M3/M4/M5, consommation mémoire, stabilité du plugin, qualité comparative entre `small` et `base`, comportement sur prompts atypiques. Mais le socle technique est assez concret pour mériter l'attention. Pour une fois, “temps réel local” ne ressemble pas seulement à une promesse marketing. Disons que le laboratoire peut sortir le casque audio sans honte.

## Sources

- Dépôt GitHub Magenta RealTime 2 : https://github.com/magenta/magenta-realtime
- Fiche Hugging Face Magenta RealTime : https://huggingface.co/google/magenta-realtime
- Article Google Magenta RealTime : https://magenta.withgoogle.com/magenta-realtime
- Paper *Live Music Models* : https://arxiv.org/abs/2508.04651
