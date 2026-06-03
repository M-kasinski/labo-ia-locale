---
title: "Ollama 0.30 : llama.cpp revient au centre du jeu local"
description: "La version 0.30 d’Ollama améliore la compatibilité GGUF, élargit le support matériel et accélère NVIDIA en s’appuyant plus franchement sur llama.cpp."
pubDate: 2026-06-03
tags: ["ollama", "llama-cpp", "gguf", "inference", "apple-silicon", "nvidia", "local-ai"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub — Ollama v0.30.0 release"
    url: "https://github.com/ollama/ollama/releases/tag/v0.30.0"
  - label: "GitHub — Ollama releases"
    url: "https://github.com/ollama/ollama/releases"
  - label: "GitHub — ggml-org/llama.cpp releases"
    url: "https://github.com/ggml-org/llama.cpp/releases"
---

Ollama a publié **v0.30.0** le **13 mai 2026**, et la release mérite qu’on s’y arrête même si elle n’a pas le parfum spectaculaire d’un nouveau modèle. Le point important est simple : Ollama renforce son appui sur **llama.cpp** pour améliorer la compatibilité, ouvrir davantage de chemins matériels et mieux gérer les modèles **GGUF**, y compris ceux publiés directement sur Hugging Face ou issus de fine-tuning maison.

Ce n’est pas une petite correction de confort. Pour beaucoup d’utilisateurs locaux, Ollama est la porte d’entrée : une commande, un modèle, une API locale. Quand ce niveau-là absorbe mieux les formats communautaires, c’est tout l’écosystème qui devient moins pénible à brancher. Pas glamour, donc utile.

## Ce que dit officiellement la release

La note de version **v0.30.0** indique qu’Ollama 0.30 apporte une compatibilité et des performances améliorées via **llama.cpp**. Ollama précise que cela vient compléter le moteur **MLX** sur Apple Silicon, avec un support étendu à un plus large éventail de matériels. La même note mentionne aussi un support élargi pour les modèles, notamment les modèles **GGUF** venant de Hugging Face et les modèles fine-tunés par l’utilisateur.

Le message est assez clair : Ollama ne cherche pas à remplacer llama.cpp, mais à mieux l’intégrer dans un produit simple. C’est une position pragmatique. llama.cpp reste la forge basse couche du local : formats GGUF, kernels, quantization, architectures récentes, ports CPU/GPU. Ollama ajoute autour la distribution, le cache de modèles, l’API et l’expérience développeur.

La release mentionne aussi de meilleures performances sur matériel **NVIDIA**. La note officielle ne donne pas de tableau de benchmarks détaillé dans l’extraction disponible ; il faut donc éviter d’en faire une promesse chiffrée. On peut dire qu’Ollama revendique une amélioration de performance, pas que telle carte gagne précisément X %. La nuance est moins sexy qu’un graphique, mais elle a le bon goût d’être honnête.

## Pourquoi le retour de llama.cpp compte

Dans l’IA locale, la compatibilité est souvent plus importante que la nouveauté brute. Un modèle open-weight peut être excellent sur sa fiche Hugging Face et insupportable à faire tourner si le runtime ne comprend pas l’architecture, le tokenizer, le chat template ou la quantization.

Le choix d’Ollama 0.30 de s’appuyer davantage sur llama.cpp a donc trois conséquences pratiques.

D’abord, **GGUF devient encore plus central**. Le format est déjà l’un des standards de fait pour l’inférence locale, surtout côté CPU, Apple Silicon, petites cartes GPU et distributions communautaires. Si Ollama accepte plus facilement des GGUF Hugging Face ou des modèles fine-tunés, le chemin entre “je vois un checkpoint intéressant” et “je le teste localement” se raccourcit.

Ensuite, cela réduit l’écart entre les utilisateurs avancés de llama.cpp et ceux qui veulent une interface plus simple. Tout le monde n’a pas envie de compiler le bon backend, de jongler avec les flags de contexte, de batch et de quantization. Ollama masque une partie de cette complexité, parfois au prix d’un contrôle plus limité. La v0.30 semble assumer ce compromis : profiter de llama.cpp sans exposer toute la salle des machines.

Enfin, cela rend Ollama plus crédible comme runtime de base pour des outils au-dessus : interfaces web, agents locaux, connecteurs OpenAI-compatible, scripts RAG, pipelines de test. Quand le serveur local accepte plus de modèles et casse moins souvent sur les formats récents, tout ce qui parle à son API devient plus stable.

## Apple Silicon : MLX n’est pas remplacé

Un détail important : la note de release dit que l’intégration renforcée de llama.cpp **augmente** le moteur MLX sur Apple Silicon, elle ne dit pas qu’elle le remplace. C’est logique. MLX reste un chemin très intéressant sur Mac récents, notamment parce qu’il colle à l’écosystème mémoire unifiée d’Apple et à ses bibliothèques.

Mais tous les modèles ne sortent pas immédiatement dans un format MLX propre. Les quantizations communautaires GGUF, elles, arrivent souvent vite. Pour un utilisateur Mac, avoir Ollama capable de passer plus naturellement par llama.cpp en complément de MLX donne plus d’options : parfois MLX sera le bon chemin, parfois GGUF via llama.cpp sera simplement le premier chemin disponible.

C’est particulièrement vrai pour les modèles spécialisés ou fine-tunés. Le modèle populaire du mois aura peut-être un packaging parfait. Le checkpoint obscur mais utile pour ton domaine métier, beaucoup moins. Dans ce cas, la compatibilité GGUF vaut plus qu’un communiqué tonitruant.

## NVIDIA : amélioration annoncée, chiffres à mesurer soi-même

Ollama affirme que cette release apporte des performances plus rapides sur matériel **NVIDIA**. La prudence s’impose : sans matrice publique détaillée dans la note extraite, il ne faut pas extrapoler. Les gains peuvent dépendre du modèle, du format, de la taille du contexte, de la quantization, du batch et du backend exact.

La bonne méthode reste banale : tester avant/après sur ta machine, avec les mêmes prompts, les mêmes modèles et les mêmes paramètres. Mesurer le temps de chargement, le prompt processing, le débit de génération et la mémoire utilisée. Ce n’est pas très romantique ; c’est pour ça que ça marche.

Pour les stations locales NVIDIA, l’intérêt d’Ollama 0.30 est surtout opérationnel. Si le backend gère mieux une famille de modèles GGUF ou des checkpoints fine-tunés, on gagne du temps de plomberie. Et dans un labo local, la plomberie est rarement ce qui manque.

## Les limites connues à ne pas ignorer

La release officielle liste aussi des **known issues**. Trois points ressortent : `laguna-xs.2` n’est pas encore supporté sur Windows/Linux ; `llama3.2-vision` n’est pas encore supporté ; `nomic-embed-text` convertit désormais les entrées en minuscules conformément à la model card, alors que les versions précédentes d’Ollama préservaient incorrectement la casse.

Le dernier point est discret mais important. Si tu utilises `nomic-embed-text` dans un pipeline RAG existant, un changement de normalisation peut modifier les embeddings générés. En pratique, cela peut imposer de reconstruire un index vectoriel pour éviter de mélanger des embeddings produits avec des comportements différents. C’est exactement le genre de détail qui transforme une mise à jour “mineure” en après-midi café froid.

Le non-support temporaire de `llama3.2-vision` rappelle aussi une réalité : les modèles multimodaux restent plus fragiles côté runtime local que les modèles texte. Vision, audio, templates multimodaux, encodage des images, projecteurs : les points de rupture sont plus nombreux.

## Faut-il mettre à jour ?

Pour un poste de test ou une machine personnelle, **oui, probablement**. Ollama 0.30 va dans le bon sens : plus de compatibilité GGUF, meilleure intégration llama.cpp, extension matérielle et amélioration revendiquée côté NVIDIA. C’est le genre de release qui ne change pas forcément ton modèle favori, mais qui augmente les chances que le prochain modèle intéressant démarre sans cérémonie vaudoue.

Pour une machine de production locale — RAG interne, agents, endpoint partagé — il faut être plus méthodique. Sauvegarde la configuration, note les versions, teste les modèles critiques, vérifie les embeddings, puis migre. En particulier, si `nomic-embed-text` est dans la boucle, traite le changement de casse comme une vraie modification de comportement.

La lecture éditoriale est simple : Ollama continue de jouer son rôle de couche simple au-dessus du chaos créatif de l’open-weight. La v0.30 ne fait pas disparaître la complexité du local ; elle la rend un peu plus absorbable. Et franchement, dans ce domaine, c’est déjà une forme de progrès civilisationnel.

## Sources

- [GitHub — Ollama v0.30.0 release](https://github.com/ollama/ollama/releases/tag/v0.30.0)
- [GitHub — Ollama releases](https://github.com/ollama/ollama/releases)
- [GitHub — ggml-org/llama.cpp releases](https://github.com/ggml-org/llama.cpp/releases)
