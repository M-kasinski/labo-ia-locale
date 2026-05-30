---
title: "iPhone et LLM locaux : le benchmark qui remet MLX, LiteRT-LM et CoreML à leur place"
description: "Un benchmark reproductible compare MLX Swift, llama.cpp, LiteRT-LM et CoreML sur iPhone 17 Pro. Résultat : le meilleur runtime dépend du modèle et de la contrainte mémoire."
pubDate: 2026-05-30
tags: ["Apple Silicon", "MLX", "llama.cpp", "LiteRT-LM", "CoreML", "benchmarks"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub — john-rocky/apple-silicon-llm-bench"
    url: "https://github.com/john-rocky/apple-silicon-llm-bench"
  - label: "Qiita — benchmark iPhone MLX / llama.cpp / LiteRT-LM / CoreML"
    url: "https://qiita.com/john-rocky/items/800bb43b21f9f6da44c4"
  - label: "GitHub — Apple MLX"
    url: "https://github.com/ml-explore/mlx"
---

Un nouveau benchmark publié par John Rocky compare plusieurs runtimes de LLM locaux sur **iPhone 17 Pro / A19 Pro** : **MLX Swift**, **llama.cpp**, **LiteRT-LM** et **CoreML / ANE**. Le dépôt `apple-silicon-llm-bench`, aussi présenté sous le nom `yardstick`, se veut reproductible et orienté vrais appareils Apple Silicon : iPhone, iPad et Mac.

Le résultat intéressant n’est pas “MLX gagne tout” ou “llama.cpp est mort”. Ce serait trop simple, donc probablement faux. Le benchmark montre plutôt une chose plus utile : sur mobile Apple, le meilleur runtime dépend du modèle, de la mémoire disponible, de la priorité vitesse/efficacité, et du backend réellement utilisé.

## Le protocole : court, concret, imparfait mais utile

Le benchmark iPhone mis en avant utilise un **iPhone 17 Pro avec puce A19 Pro**, des modèles 4-bit, une tâche `short-chat`, et une génération de 128 tokens pour la plupart des runtimes. Les résultats sont agrégés en médiane de trois runs froids. L’exécution est automatisée depuis un Mac via `devicectl`, ce qui évite de mesurer un bricolage manuel à la main tremblante.

Deux modèles sont comparés dans les résultats principaux : **Gemma 4 E2B** et **Qwen 3.5 2B**. Les runtimes testés sont MLX Swift, llama.cpp, LiteRT-LM et CoreML / ANE. Les métriques affichées sont simples : vitesse de décodage en tokens par seconde et mémoire pic en Mo.

Il y a des limites, documentées par l’auteur. LiteRT-LM génère jusqu’à EOS parce que son API ne propose pas le même plafond de sortie par appel. CoreML / ANE compte des morceaux streamés, approximativement équivalents à des tokens. Les formats de quantization ne sont pas identiques : MLX en 4-bit, llama.cpp en GGUF Q4_K_M, LiteRT-LM en INT4-QAT, CoreML avec formats palettisés ou INT8. Ce n’est donc pas une vérité physique absolue. C’est un benchmark de terrain, et c’est précisément ce qui le rend intéressant.

## Vitesse : MLX gagne Qwen, LiteRT-LM surprend sur Gemma

Sur **Qwen 3.5 2B**, MLX Swift obtient le meilleur débit : **61,2 tokens/s**. llama.cpp est mesuré à **39,1 tokens/s**, et CoreML / ANE à **27,9 tokens/s**. LiteRT-LM n’a pas de ligne Qwen, car son catalogue testé est centré sur Gemma.

Sur **Gemma 4 E2B**, surprise : **LiteRT-LM** arrive en tête avec **55,4 tokens/s**, devant MLX Swift à **47,5 tokens/s**, llama.cpp à **37,8 tokens/s** et CoreML / ANE à **33,4 tokens/s**. L’explication probable est assez directe : LiteRT-LM est un runtime Google optimisé pour les modèles Gemma dans un format `.litertlm` INT4-QAT, avec exécution GPU Metal. Quand le modèle, le format et le runtime viennent du même écosystème, l’avantage peut être net.

La conclusion pratique : si tu veux faire tourner un modèle généraliste comme Qwen sur iPhone, MLX Swift paraît aujourd’hui très solide. Si ton cas d’usage accepte Gemma et que tu veux le meilleur couple vitesse/mémoire, LiteRT-LM mérite d’être testé sérieusement.

## Mémoire : CoreML / ANE change la discussion

Les chiffres mémoire sont encore plus instructifs. Sur **Qwen 3.5 2B**, CoreML / ANE descend à **241 Mo** de mémoire pic, contre **1 279 Mo** pour MLX Swift et **1 479 Mo** pour llama.cpp. C’est environ cinq fois moins que MLX dans ce test. En échange, CoreML est le plus lent en décodage.

Sur **Gemma 4 E2B**, LiteRT-LM est mesuré à **641 Mo**, MLX Swift à **2 900 Mo**, llama.cpp à **3 156 Mo**, et CoreML / ANE à **1 187 Mo**. Là encore, LiteRT-LM profite fortement de son format optimisé pour Gemma.

Ce point est crucial pour le mobile. Sur desktop, on parle souvent tokens/s et taille de contexte. Sur téléphone, la mémoire disponible, la coexistence avec l’application principale, l’impact thermique et la consommation deviennent aussi importants que le débit brut. Un runtime plus lent mais beaucoup plus sobre peut être préférable dans une app réelle, surtout si le LLM tourne en tâche secondaire.

## MLX, llama.cpp, LiteRT-LM, CoreML : quatre philosophies

**MLX Swift** est le choix naturel si l’on veut rester dans l’écosystème Apple avec un runtime rapide et généraliste sur GPU Metal. Le projet MLX d’Apple fournit des APIs Python, C++, C et Swift, et vise explicitement Apple Silicon. Dans ce benchmark, MLX est très fort sur Qwen et reste compétitif sur Gemma.

**llama.cpp** reste le champion de la portabilité. Il ne gagne pas ici, mais il ne s’effondre pas non plus. Son avantage est ailleurs : énorme base de modèles GGUF, compatibilité multiplateforme, communauté massive, intégrations partout. Sur iPhone pur, il peut être moins optimal qu’un runtime taillé pour Apple ou pour un modèle précis ; sur une flotte hétérogène, il reste difficile à ignorer.

**LiteRT-LM** est plus spécialisé. Son score Gemma montre qu’un runtime verticalement optimisé peut battre les solutions généralistes. Mais cette spécialisation limite aussi le choix des modèles. Si ton produit est construit autour de Gemma, c’est un candidat sérieux. Si tu veux tester dix familles de modèles open-weight, ce sera plus contraignant.

**CoreML / ANE** joue une autre partie. Il vise moins le débit maximal que l’usage de l’Apple Neural Engine et l’efficacité mémoire. Dans le benchmark, il est plus lent, mais son résultat à 241 Mo sur Qwen 3.5 2B est remarquable. Pour des apps mobiles où le LLM doit cohabiter avec caméra, UI, réseau, AR ou traitement image, c’est une piste très rationnelle.

## Ce que ça change pour l’IA locale mobile

Ce benchmark rappelle que “faire tourner un LLM localement” n’est plus une question binaire. Oui, un iPhone récent peut exécuter des modèles 2B en local à des vitesses utilisables. Mais le vrai sujet devient : avec quelle mémoire, quelle chaleur, quelle autonomie, quelle latence de premier token, quel impact sur le reste de l’application ?

Pour un assistant local embarqué, MLX peut être le bon choix si la vitesse prime et que le modèle est supporté proprement. Pour un outil Gemma-first, LiteRT-LM peut offrir un excellent rapport performance/mémoire. Pour une app qui doit rester légère et préserver le GPU, CoreML / ANE devient intéressant malgré son débit inférieur. Et pour une stratégie multiplateforme, llama.cpp reste la base la plus pragmatique.

## Prudence sur les chiffres

Il ne faut pas extrapoler trop vite. Le benchmark couvre deux modèles principaux, un appareil, et des conditions précises. Les prochaines versions de MLX, llama.cpp, LiteRT-LM ou CoreML peuvent changer l’ordre. Les résultats peuvent aussi varier avec le contexte, la longueur de génération, la température, la taille du KV cache, l’état thermique du téléphone et la façon dont l’app est empaquetée.

Mais l’existence d’un dépôt reproductible est précieuse. On sort des captures d’écran isolées et des “ça marche chez moi” pour aller vers des mesures comparables. C’est exactement ce dont l’écosystème local a besoin : moins d’anecdotes, plus de protocoles.

## Verdict

Le message à retenir est simple : sur Apple mobile, **MLX n’est pas automatiquement le meilleur partout**, **llama.cpp reste utile mais pas toujours optimal**, **LiteRT-LM peut dominer quand le modèle est Gemma**, et **CoreML / ANE mérite une vraie place quand la mémoire compte plus que les tokens/s**.

Pour les développeurs d’apps locales, ce benchmark donne une bonne grille de décision. Choisir un runtime sans mesurer sur l’appareil cible devient de moins en moins défendable. Le local est en train de mûrir ; il demande maintenant de l’ingénierie, pas seulement de l’enthousiasme avec un logo de lama.

## Sources

- [GitHub — john-rocky/apple-silicon-llm-bench](https://github.com/john-rocky/apple-silicon-llm-bench)
- [Qiita — benchmark iPhone MLX / llama.cpp / LiteRT-LM / CoreML](https://qiita.com/john-rocky/items/800bb43b21f9f6da44c4)
- [GitHub — Apple MLX](https://github.com/ml-explore/mlx)
