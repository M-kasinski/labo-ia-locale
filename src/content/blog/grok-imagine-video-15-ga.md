---
title: "Grok Imagine Video 1.5 en GA : xAI prend la tête de la génération vidéo IA"
description: "xAI sort Grok Imagine Video 1.5 en version générale : #1 sur l'Arena image-to-video, audio natif synchronisé, et un prix 7x inférieur à Sora 2."
pubDate: 2026-06-19
tags: ["xAI", "Grok", "génération vidéo", "image-to-video", "Aurora"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Annonce officielle xAI"
    url: "https://x.ai/news/grok-imagine-video-1-5"
  - label: "xAI News page"
    url: "https://x.ai/news"
  - label: "ExplainX — analyse détaillée"
    url: "https://explainx.ai/blog/grok-imagine-video-1-5-xai-release-2026"
---

## La nouvelle

Le 16 juin 2026, xAI a sorti **Grok Imagine Video 1.5** en version générale (GA), mettant fin à la phase de preview lancée le 9 juin. Le modèle occupe désormais la première place du classement Image-to-Video Arena avec un bond de **+52 points Elo** par rapport à la version 1.0, devançant Sora, Kling 2.6, Seedance 2.0 et Google Veo en tests aveugles.

Elon Musk a confirmé la « wide release » le 17 juin via X, pointant directement vers grok.com/imagine.

## Analyse technique

### Audio natif synchronisé — une amélioration architecturale

La différence majeure avec la version 1.0 : **l'audio et le discours sont générés dans le même pass que la vidéo**. Ce n'est pas un simple ajout fonctionnel — c'est un changement architectural. Le modèle ne nécessite plus d'étape séparée de génération audio, ce qui réduit la latence et améliore la synchronisation labiale / sonore.

### Spécifications

- **Résolution :** 720p à 24 FPS (plafond actuel ; les concurrents montent à 1080p)
- **Durée maximale :** clips jusqu'à 15 secondes
- **Moteur sous-jacent :** Aurora, un modèle autoregressif entraîné sur un cluster de **110 000 GPU NVIDIA GB200** (Colossus 2)
- **Video 1.5 Fast :** génération d'un clip 6s/720p en ~25 secondes (contre 40+ s pour la version précédente, soit **~40 % plus rapide**)

### Benchmarks

Sur l'Image-to-Video Arena (données de juin 2026), Grok Imagine Video 1.5 Preview se classait déjà #1 avant le passage en GA. Les positions #1 et #2 sur plusieurs benchmarks sont revendiquées par xAI, mais **aucun benchmark tiers indépendant** comparant directement Video 1.5 contre Sora, Kling ou Runway n'a encore été publié à ce jour.

### Prix

- **$4,20 / minute** de vidéo générée via l'API Imagine
- À comparer avec **Sora 2 à $30 / minute** — un écart de prix d'un facteur ~7
- Le modèle preview (`grok-imagine-video-1.5-preview`) a été retiré ; seul `grok-imagine-video-1.5` reste disponible

## Impact pour l'écosystème

Le rapport qualité-prix de Grok Imagine Video 1.5 est le véritable signal ici. Même sans résolution 1080p, un modèle #1 sur l'Arena à $4,20/min contre $30/min pour Sora 2 représente une pression concurrentielle directe. Pour les développeurs d'apps vidéo IA, c'est l'API la plus accessible en termes de coût — ce qui pourrait accélérer l'intégration dans des produits grand public.

Du côté open source / local, aucune implication directe : le modèle n'est disponible qu'en API propriétaire xAI. Mais la démonstration que l'audio natif synchronisé est réalisable à cette échelle devrait inspirer les architectures futures du côté open weight.
