---
title: "LFM2.5-VL-Extract : Liquid AI pousse l’extraction JSON vers le très petit VLM local"
description: "Liquid AI publie deux VLM open-weight spécialisés dans l’extraction structurée depuis images. Le sujet n’est pas le chat multimodal, mais le JSON fiable sur machine modeste."
pubDate: 2026-06-08
tags: ["Liquid AI", "VLM", "JSON", "edge AI", "open-weight", "Hugging Face"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Hugging Face — LiquidAI/LFM2.5-VL-450M-Extract"
    url: "https://huggingface.co/LiquidAI/LFM2.5-VL-450M-Extract"
  - label: "Hugging Face — LiquidAI/LFM2.5-VL-1.6B-Extract"
    url: "https://huggingface.co/LiquidAI/LFM2.5-VL-1.6B-Extract"
  - label: "Liquid AI — Introducing LFM2.5: The Next Generation of On-Device AI"
    url: "https://www.liquid.ai/blog/introducing-lfm2-5-the-next-generation-of-on-device-ai"
---

Liquid AI vient d’ajouter deux modèles qui méritent plus d’attention que le buzz habituel autour des « grands » VLM : **LFM2.5-VL-450M-Extract** et **LFM2.5-VL-1.6B-Extract**. Leur promesse est étroite, donc intéressante : prendre une image, recevoir une liste de champs à extraire, et répondre avec un **objet JSON plat** plutôt qu’un paragraphe vaguement utile. Pour l’IA locale, c’est exactement le genre de spécialisation qui compte.

Les deux fiches Hugging Face présentent ces modèles comme des variantes de la collection **Liquid Nanos**, des modèles compacts et orientés production. Le 450M combine un backbone langage d’environ **350M paramètres** avec un encodeur vision **SigLIP2 d’environ 100M paramètres**. Le 1.6B monte à un backbone langage d’environ **1.2B** avec un encodeur vision SigLIP2 plus large, autour de **400M paramètres**. Les deux sont publiés en **bfloat16**, sous **LFM Open License v1.0**, avec un contexte annoncé à **128 000 tokens** sur les fiches modèles.

## Le détail important : le modèle ne prétend pas tout faire

La plupart des VLM open-weight sont évalués et marketés comme des assistants multimodaux généralistes : décrire une scène, répondre à des questions, lire des documents, parfois raisonner sur un graphe ou un tableau. Ici, Liquid AI cible un flux beaucoup plus industriel : **image + schéma de champs → JSON**.

Le schéma est fourni sous forme de liste YAML dans le prompt système. Exemple simplifié : `wood_color`, `wood_texture`, `wood_pattern`, chacun accompagné d’une description. Le modèle doit renvoyer seulement les valeurs correspondantes dans un JSON strict. Les fiches Hugging Face documentent aussi un comportement de type **enum**, où les choix possibles sont inclus dans la description du champ. C’est moins glamour qu’un chatbot qui commente une photo. C’est aussi beaucoup plus proche des besoins réels : catalogage e-commerce, inspection visuelle, extraction depuis formulaires, vidéos découpées en frames, alertes de sécurité.

Ce choix éditorial est sain. En local, un modèle spécialisé qui tient son format vaut souvent mieux qu’un gros modèle généraliste qui parle joliment mais casse le parseur une requête sur cinq. La poésie est charmante ; en production, elle coûte des tickets Jira.

## Les chiffres publiés : bons, mais à lire comme benchmark maison

Liquid AI annonce avoir évalué ces modèles sur un benchmark de **2 000 triplets image, schéma, JSON**, avec labels de référence générés par un ensemble de modèles multimodaux frontier. Trois métriques sont mises en avant : validité JSON, cohérence avec le schéma et score de juge VLM.

Pour **LFM2.5-VL-450M-Extract**, la fiche indique **98,9 %** de validité JSON, **98,8** en F1 de cohérence de schéma et **84,5** au score de juge VLM. Liquid AI le compare notamment à SmolVLM-500M-Instruct, FastVLM-0.5B, Qwen3.5-0.8B et InternVL3.5-1B. Le claim officiel : le modèle dépasse les VLM open-source de taille similaire sur ce benchmark et devient compétitif avec des modèles environ quatre fois plus grands.

Pour **LFM2.5-VL-1.6B-Extract**, les chiffres montent à **99,6 %** de validité JSON, **99,6** en F1 de schéma et **90,6** au score juge. Liquid AI le compare à FastVLM-1.5B, SmolVLM2-2.2B-Instruct, Qwen3.5-2B, Gemma-4-E2B-it et InternVL3.5-2B. Là encore, il faut garder la tête froide : c’est un benchmark publié par l’éditeur, sur une tâche précisément alignée avec l’entraînement du modèle. Ce n’est pas une preuve universelle de supériorité multimodale. Mais c’est une indication utile si ton besoin réel est l’extraction structurée.

## Pourquoi c’est pertinent pour le local

Liquid AI positionne LFM2.5 comme une famille conçue pour l’**on-device AI** : appareils mobiles, laptops, véhicules, IoT, edge hardware. Le billet de lancement LFM2.5 mentionne une disponibilité open-weight, des optimisations pour l’inférence locale, et un support annoncé côté **llama.cpp**, **NexaSDK**, **MLX** et **vLLM** pour la famille LFM2.5. Les fiches Extract, elles, montrent surtout des exemples via Transformers avec `trust_remote_code=True`, ce qui implique que l’intégration pratique dépendra encore de l’état des runtimes et de leurs convertisseurs.

Le 450M est le plus intéressant pour les machines modestes. Même en BF16, il reste dans une taille réaliste pour laptop ou petit GPU, et sa tâche est naturellement compatible avec des pipelines batch : analyser des images produit, des captures caméra ou des pages numérisées, puis injecter le JSON dans une base, un moteur de règles ou un RAG.

Le 1.6B vise plutôt le compromis qualité/poids. Il est encore petit par rapport aux VLM généralistes actuels, mais assez gros pour absorber des cas visuels plus ambigus. Dans un workflow auto-hébergé, il pourrait servir de premier étage d’extraction avant validation humaine ou contrôle par règles.

## Ce qu’il manque encore

Je n’ai pas trouvé, au moment de cette veille, d’analyse indépendante solide reproduisant les résultats sur un corpus public standardisé. Les chiffres doivent donc être traités comme **des résultats fournisseur vérifiés à la source, pas comme un classement neutre**. Il faudra aussi vérifier la facilité réelle de conversion vers GGUF, MLX ou autres formats, parce qu’un modèle « local » qui ne tourne proprement que dans un script Transformers expérimental reste un modèle local avec une petite astérisque.

La bonne nouvelle : le format de tâche est suffisamment simple pour être benchmarké par n’importe quelle équipe. Il suffit de constituer un jeu d’images, de définir des champs, puis de mesurer validité JSON, respect du schéma et exactitude métier. Si Liquid AI tient ses chiffres hors benchmark maison, ces modèles peuvent devenir des briques très pratiques pour de l’extraction visuelle privée.

## Sources

- Hugging Face — LiquidAI/LFM2.5-VL-450M-Extract : https://huggingface.co/LiquidAI/LFM2.5-VL-450M-Extract
- Hugging Face — LiquidAI/LFM2.5-VL-1.6B-Extract : https://huggingface.co/LiquidAI/LFM2.5-VL-1.6B-Extract
- Liquid AI — Introducing LFM2.5: The Next Generation of On-Device AI : https://www.liquid.ai/blog/introducing-lfm2-5-the-next-generation-of-on-device-ai
