---
title: "Google AI Edge sur Mac : l’IA locale devient une app grand public"
description: "Avec AI Edge Gallery, Eloquent et LiteRT-LM, Google ne se contente pas de publier un modèle : il installe un début d’écosystème d’IA locale sur Mac, entre simplicité grand public et workflows agentiques."
pubDate: 2026-06-05
tags: ["google-ai-edge", "macos", "apple-silicon", "ia-locale", "litert-lm", "ollama", "lm-studio"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Google Developers Blog — Bringing Gemma 4 12B to your Laptop"
    url: "https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/"
  - label: "Google for Developers — AI Edge Gallery"
    url: "https://developers.google.com/edge/gallery"
  - label: "Google for Developers — AI Edge Eloquent"
    url: "https://developers.google.com/edge/eloquent"
  - label: "GitHub — google-ai-edge/LiteRT-LM"
    url: "https://github.com/google-ai-edge/LiteRT-LM"
  - label: "9to5Mac — Google AI Edge Gallery launches on macOS"
    url: "https://9to5mac.com/2026/06/03/google-ai-edge-gallery-launches-to-macos-letting-mac-users-run-gemini-models-locally/"
  - label: "MacGeneration — Gemma 4 : Google lance deux apps IA locales pour Mac"
    url: "https://www.macg.co/intelligence-artificielle/2026/06/gemma-4-google-lance-deux-apps-pour-faire-tourner-ses-ia-directement-sur-mac-308967"
---

Google vient de pousser **Google AI Edge Gallery** et **Google AI Edge Eloquent** sur macOS. À première vue, cela ressemble à deux petites apps de plus dans la pile déjà bien chargée de l’IA locale. En réalité, le signal est plus intéressant : Google commence à emballer son IA embarquée dans des outils accessibles aux utilisateurs Mac, pas seulement dans des dépôts GitHub pour développeurs patients.

On a déjà parlé séparément de **Gemma 4 12B** sur Labo IA Locale. Inutile donc de refaire ici l’article du modèle. Le vrai sujet, cette fois, c’est l’écosystème autour : une app pour tester des modèles localement, une app de dictée offline, et un runtime capable de servir un modèle via une API locale compatible OpenAI. Autrement dit : Google ne vend pas seulement des poids, il prépare le bureau autour.

## AI Edge Gallery : le “double-clic” de l’IA locale Google

**Google AI Edge Gallery** existe déjà côté mobile, mais son arrivée sur macOS change la cible. L’app permet de télécharger et d’exécuter des modèles Google en local sur Mac, avec des usages simples comme la discussion, les questions sur image, et des scénarios plus avancés via la section **Agent Skills** [Google Gallery][source-gallery].

Ce dernier point est le plus important. Dans son billet développeur, Google montre Gallery générer du code Python, l’exécuter localement, analyser des fichiers et produire des visualisations [Google Developers Blog][source-google-blog]. Ce n’est pas encore un agent autonome à la Devin sorti d’un rêve marketing trop caféiné. Mais c’est un pas concret vers des workflows où le modèle ne se contente plus de répondre : il manipule des données sur la machine.

Pour les utilisateurs habitués à **Ollama**, **LM Studio**, **MLX** ou **llama.cpp**, Gallery paraît moins flexible. 9to5Mac souligne notamment que l’app donne accès à un catalogue beaucoup plus limité que les plateformes locales généralistes [9to5Mac][source-9to5mac]. C’est logique : Google privilégie ici son propre écosystème et ses formats optimisés. Moins ouvert, mais plus guidé.

## Le compromis : moins de liberté, plus d’intégration

C’est probablement là que se situe la vraie différence avec Ollama ou LM Studio.

Ollama est excellent si l’on veut tirer vite un modèle GGUF, tester plusieurs familles, exposer une API locale et bricoler un assistant maison. LM Studio est plus confortable pour explorer des modèles, gérer des téléchargements et lancer un serveur local sans écrire de script. MLX, de son côté, reste très intéressant pour Apple Silicon quand on veut optimiser proprement côté Metal et mémoire unifiée.

**Google AI Edge**, lui, prend une autre direction : moins de choix de modèles, mais une intégration plus verticale entre modèle, runtime, apps et cas d’usage. C’est moins séduisant pour les bidouilleurs qui veulent comparer dix quantizations dans la soirée. C’est potentiellement plus séduisant pour un utilisateur Mac qui veut juste lancer une app, charger un modèle et travailler sans ouvrir un terminal.

En clair : Google ne remplace pas Ollama ou LM Studio aujourd’hui. Il construit une voie plus fermée, mais plus intégrée. Apple aurait pu faire ça. Google l’a fait avant — voilà, ça pique un peu.

## Eloquent : la dictée locale comme cas d’usage sérieux

La deuxième app, **Google AI Edge Eloquent**, vise la dictée et l’édition de texte en local. Google décrit une application macOS capable de fonctionner **100 % on-device** : dictée via raccourci clavier, transcription de fichiers audio ou vidéo, réécriture, polissage de texte et commandes vocales d’édition [Google Eloquent][source-eloquent].

Sur le papier, c’est un très bon cas d’usage pour l’IA locale. La voix est personnelle, parfois professionnelle, parfois confidentielle. La faire transiter systématiquement par un cloud n’est pas toujours souhaitable. Une app de dictée capable de nettoyer les hésitations, reformuler un message ou transformer des notes en résumé directement sur le Mac a donc du sens.

Il faut toutefois garder une réserve importante : MacGeneration note qu’Eloquent est encore moins intéressant pour les francophones si la compréhension reste centrée sur l’anglais [MacGeneration][source-macg]. Pour un site francophone, c’est une limite pratique, pas un détail de bas de page. Une dictée locale qui ne comprend pas bien le français reste une très belle voiture… sans volant du bon côté.

## LiteRT-LM : la brique technique à surveiller

La partie la plus discrète est peut-être la plus importante : **LiteRT-LM**. Google présente ce framework comme sa pile open source pour déployer des modèles de langage sur appareils edge, avec accélération CPU/GPU, gestion du cache KV, prompt templating et support de fonctions [GitHub LiteRT-LM][source-litert].

La nouveauté intéressante est le serveur local compatible OpenAI API. Le billet Google montre un endpoint `/v1/chat/completions` servi en local via `litert-lm serve` [Google Developers Blog][source-google-blog]. Pour les agents locaux, c’est crucial : dès qu’un runtime parle le dialecte OpenAI, il peut être branché plus facilement à des outils comme Continue, Aider, Open WebUI, ou des frameworks d’agents.

Ce n’est pas forcément la pile que tout le monde utilisera demain. Mais c’est un signal fort : Google veut que ses modèles locaux ne soient pas seulement utilisables dans une app vitrine. Il veut qu’ils puissent devenir une brique d’infrastructure locale.

## Ce que ça change pour l’IA locale sur Mac

Pour l’instant, l’écosystème local sur Mac est surtout dominé par trois réflexes :

- **Ollama** pour lancer vite des modèles et exposer une API locale ;
- **LM Studio** pour explorer confortablement des modèles open-weight ;
- **MLX / llama.cpp** pour ceux qui veulent optimiser, convertir, quantifier et mesurer sérieusement.

Google AI Edge ajoute une quatrième logique : l’IA locale packagée par un grand acteur, avec des apps de démonstration, des workflows guidés et un runtime maison. Ce n’est pas forcément plus ouvert. Ce n’est pas forcément plus puissant. Mais c’est probablement plus lisible pour un public qui ne sait pas ce qu’est un GGUF et qui n’a aucune envie de le savoir — ce qui, à sa décharge, est une position socialement défendable.

Côté Apple Silicon, le mouvement est intéressant parce que Google semble viser explicitement les machines grand public, pas seulement les stations de travail bardées de mémoire. Là encore, sans refaire l’article sur le modèle lui-même, l’idée importante est simple : les laptops deviennent une cible produit pour l’IA locale, pas seulement un terrain de benchmark.

## Le verdict : prometteur, mais pas encore le centre du village

Il ne faut pas surinterpréter l’annonce. Aujourd’hui, AI Edge Gallery ne remplace pas la souplesse d’Ollama ou LM Studio. Eloquent reste à évaluer sérieusement, surtout en français. LiteRT-LM est prometteur, mais son adoption dépendra de la qualité réelle des performances, de la documentation, du support des modèles et de la facilité d’intégration.

Mais il serait dommage de balayer ça comme “deux apps Google de plus”. Le vrai mouvement est plus profond : Google commence à transformer ses modèles locaux en expérience utilisateur Mac, puis en infrastructure locale compatible avec les outils existants.

Pour Labo IA Locale, la suite utile sera moins de commenter l’annonce que de tester la pile : installation, vitesse sur Apple Silicon, mémoire utilisée, qualité de la dictée, comportement du serveur local, et comparaison propre avec Ollama, LM Studio, MLX et llama.cpp. Là, on saura si Google AI Edge est seulement une vitrine sympathique — ou le début d’un concurrent sérieux dans l’IA locale grand public.

[source-google-blog]: https://developers.googleblog.com/bringing-gemma-4-12b-to-your-laptop-unlocking-local-agentic-workflows-with-google-ai-edge/
[source-gallery]: https://developers.google.com/edge/gallery
[source-eloquent]: https://developers.google.com/edge/eloquent
[source-litert]: https://github.com/google-ai-edge/LiteRT-LM
[source-9to5mac]: https://9to5mac.com/2026/06/03/google-ai-edge-gallery-launches-to-macos-letting-mac-users-run-gemini-models-locally/
[source-macg]: https://www.macg.co/intelligence-artificielle/2026/06/gemma-4-google-lance-deux-apps-pour-faire-tourner-ses-ia-directement-sur-mac-308967
