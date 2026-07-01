---
title: "Gemini Omni Flash : Google accélère la vidéo générative et enterre Veo 3.0"
description: "Le 30 juin 2026, Google met Gemini Omni Flash en preview publique et Nano Banana 2 Lite en GA, tout en programmant l’arrêt de Veo 3.0 et Veo 2.0."
pubDate: 2026-07-01
tags: ["Google", "Gemini", "Veo", "vidéo générative", "multimodal", "API"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Google Cloud Blog — Nano Banana 2 Lite and Gemini Omni Flash available"
    url: "https://cloud.google.com/blog/products/ai-machine-learning/nano-banana-2-lite-and-gemini-omni-flash-available/"
  - label: "Gemini API Release notes"
    url: "https://ai.google.dev/gemini-api/docs/changelog"
  - label: "Gemini Omni Flash — Google AI for Developers"
    url: "https://ai.google.dev/gemini-api/docs/models/gemini-omni-flash"
---

## La nouvelle

Le 30 juin 2026, Google a poussé une mise à jour assez nette de sa pile créative :

- **Gemini Omni Flash** passe en **preview publique**
- **Nano Banana 2 Lite** devient disponible pour tout le monde
- les anciens modèles vidéo **Veo 2.0** et **Veo 3.0** arrivent au bout de leur cycle de vie

Le signal est simple : Google ne veut plus seulement générer de la vidéo. Il veut que la vidéo soit **éditable par conversation**, au même endroit que le texte et l’image.

Et ça, pour les équipes produit, change beaucoup plus qu’un simple nom de modèle.

## Analyse technique

### Gemini Omni Flash : la vidéo devient conversationnelle

Le modèle **Gemini Omni Flash** est présenté comme un modèle multimodal de preview pour :

- génération vidéo
- édition vidéo conversationnelle
- exploitation conjointe de **texte**, **images** et **vidéo** comme entrées
- génération d’**audio natif** avec les sorties vidéo

Google insiste aussi sur la cohérence :

- cohérence des personnages
- cohérence des objets
- cohérence du style

Ce n’est pas un détail cosmétique. La plupart des outils vidéo échouent encore moins sur le “prompt” que sur la **stabilité inter-plans**. Le fait de pousser un modèle qui promet cette continuité est donc le vrai point technique.

### Le positionnement produit

Omni Flash n’est pas lancé comme un jouet de démo.
Google l’ouvre dans plusieurs surfaces :

- **Google AI Studio**
- **Gemini API**
- **Gemini app**
- **Google Flow**
- **Gemini Enterprise Agent Platform**

C’est important, parce que le modèle quitte le statut de curiosité R&D pour devenir une pièce d’infrastructure créative.

Google annonce aussi que **la provisioned throughput** pour Omni Flash arrivera bientôt. Traduction : la version public preview est là, mais la montée en charge sérieuse reste encore en préparation.

### Ce que Nano Banana 2 Lite raconte du reste du stack

En parallèle, Google pousse **Nano Banana 2 Lite** comme version rapide et peu coûteuse pour la génération d’images.
Le message implicite est bon :

- l’image rapide sert de brique d’amont
- la vidéo conversationnelle sert de brique de finition
- les deux partagent la même logique de pipeline multimodal

Autrement dit : Google construit une chaîne créative cohérente, pas une liste de modèles isolés.

### Les anciens modèles vidéo sont en fin de course

La release notes du 30 juin acte un point très concret :

- **Veo 2.0** est déprécié
- **Veo 3.0** est déprécié
- les versions **3.1 preview** sont les chemins de migration recommandés

La date de shutdown annoncée pour ces modèles est le **30 juin 2026**.

C’est le genre de détail qui casse des pipelines en silence si tu n’as pas de supervision de versions. Les modèles vidéo, contrairement aux chats, se cachent volontiers dans des intégrations créatives où personne ne vérifie la compatibilité avant la prod. Mauvaise habitude, très répandue.

## Chiffres et caractéristiques utiles

D’après les documents publics et les pages produit Google :

- Omni Flash vise des **clips vidéo 720p** de courte durée
- le mode de sortie est pensé pour du **montage conversationnel** plutôt que du simple prompt unique
- la tarification doc indique environ **0,10 $ / seconde** de vidéo en sortie
- SynthID et les content credentials restent au cœur du dispositif

Le dernier point compte : Google essaie de verrouiller le signal d’authenticité en même temps qu’il industrialise la génération.
C’est clairement une réponse à la montée des usages d’édition rapide et aux inquiétudes sur les médias synthétiques.

## Impact pour les équipes produit et les builders

### Ce que ça change concrètement

Pour les équipes qui font :

- pub / marketing
- prototypage créatif
- production de visuels et de clips
- workflows de social content
- assistants internes de media generation

la différence n’est pas juste “un meilleur modèle”.
La vraie différence, c’est le passage à un modèle qui accepte des **itérations conversationnelles** sur un asset vidéo déjà existant.

Ça ouvre trois usages plus solides :

1. **localiser un asset** sans repartir de zéro
2. **réécrire un plan** sans casser le style
3. **enchaîner image → vidéo → édition** sans changer d’outil

### Ce que ça ne résout pas

Il faut garder les pieds sur terre :

- le modèle est en **preview**, donc pas encore une base contractuelle stable
- la disponibilité à haute charge n’est pas encore totale
- les workflows très longs ou très précis peuvent encore produire des résultats incohérents
- l’écart entre “édition assistée” et “post-production fiable” reste réel

En clair : très bon signal produit, pas encore une baguette magique.
Les baguettes magiques sont rares ; les limitations, elles, ont une fréquence admirable.

## Pourquoi l’arrêt de Veo 3.0 compte autant que le lancement d’Omni Flash

Le marché lit souvent les annonces par le prisme du nouveau jouet.
Le vrai changement ici, c’est la **gestion de cycle de vie** : Google pousse l’écosystème vers des IDs plus récents, unification du stack et migration forcée vers les familles 3.1 / Omni.

Pour les développeurs, ça implique :

- vérifier les IDs d’appel
- revalider les intégrations créatives
- surveiller les dates de shutdown
- prévoir des fallbacks propres

Bref : faire du DevOps créatif, ce qui était inévitable, mais pas forcément élégant.

## Ce qu’il faut retenir

Gemini Omni Flash est plus qu’un nouveau modèle vidéo.
C’est une tentative de faire entrer la vidéo générative dans le même mouvement que le texte, l’image et les agents : **un système conversationnel multimodal**.

Et la fin programmée de Veo 3.0 dit le reste :

- Google accélère
- les anciens chemins ferment
- les équipes qui n’ont pas de stratégie de migration vont le découvrir au mauvais moment

C’est rarement joyeux. C’est très souvent réel.

## Sources vérifiées

- [Google Cloud Blog — Nano Banana 2 Lite and Gemini Omni Flash available](https://cloud.google.com/blog/products/ai-machine-learning/nano-banana-2-lite-and-gemini-omni-flash-available/)
- [Gemini API — Release notes](https://ai.google.dev/gemini-api/docs/changelog)
- [Gemini Omni Flash — Google AI for Developers](https://ai.google.dev/gemini-api/docs/models/gemini-omni-flash)
