---
title: "llama.cpp ajoute le MTP pour Gemma 4 : accélération réelle, réglages piégeux"
description: "Le support Gemma 4 MTP dans llama.cpp ouvre la voie au speculative decoding avec modèles assistants, mais les premiers retours montrent aussi des régressions et des paramètres à manier prudemment."
pubDate: 2026-06-10
category: "local"
tags: ["llama.cpp", "Gemma 4", "speculative decoding", "MTP", "GGUF", "inference locale"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub — llama.cpp PR #23398: add Gemma4 MTP"
    url: "https://github.com/ggml-org/llama.cpp/pull/23398"
  - label: "GitHub — llama.cpp issue #24266: Gemma4 MTP regression"
    url: "https://github.com/ggml-org/llama.cpp/issues/24266"
  - label: "GitHub — llama.cpp discussion #22735: Gemma 4 assistant/drafter support"
    url: "https://github.com/ggml-org/llama.cpp/discussions/22735"
---

`llama.cpp` vient de franchir une étape importante pour les utilisateurs de **Gemma 4** en local : le support **MTP** pour le speculative decoding a été ajouté via la PR **#23398**. Sur le papier, c’est exactement le genre d’amélioration qui compte pour l’IA locale : plus de tokens par seconde sans changer de modèle principal, en utilisant un modèle assistant/drafter qui propose des tokens que le modèle cible valide ou rejette.

Dans les premiers résultats publiés dans la PR, l’accélération peut être spectaculaire. Mais les fils GitHub montrent aussi une réalité plus rugueuse : multi-GPU à régler, acceptation sensible à la qualité du drafter, interactions avec le KV cache quantifié, et même régressions avec certains modes de speculative decoding. Bref, c’est prometteur, mais pas encore le bouton “turbo” universel. Les boutons universels n’existent pas ; seulement des paramètres avec une excellente mémoire des erreurs passées.

## MTP, en clair

Le **MTP** — Multi-Token Prediction — permet à un modèle assistant de prédire plusieurs tokens candidats. Le modèle principal vérifie ensuite ces propositions. Si elles sont acceptées, on avance plus vite que dans une génération token-par-token classique. Si elles sont rejetées trop souvent, le surcoût du drafter peut au contraire ralentir l’inférence.

Dans le cas Gemma 4, la discussion `llama.cpp` #22735 montrait déjà le besoin : des utilisateurs voulaient convertir et exécuter les modèles **Gemma 4 Assistant / Drafter** en GGUF, notamment l’architecture `Gemma4AssistantForCausalLM`, pour accélérer les modèles Gemma 4 plus gros comme les variantes **26B** et **31B**. Avant ce travail, le script `convert_hf_to_gguf.py` ne reconnaissait pas correctement cette architecture, avec des tensors spécifiques comme `layer_scalar` non mappés par les classes Gemma existantes.

La PR #23398 répond à ce besoin en ajoutant le support MTP pour Gemma 4. Son auteur indique un support initial pour **Gemma4 31B** et **Gemma4 26B-4B**, avec des variantes **E4B/E2B** qui nécessitaient encore des corrections séparées au moment de la discussion. C’est donc une intégration de runtime et de conversion, pas seulement une option CLI décorative.

## Les chiffres qui rendent le sujet intéressant

Dans la PR, l’auteur publie un benchmark sur un système DGX Spark avec Gemma 4 dense. Sans MTP, un lot de neuf prompts totalise **290,01 secondes** de wall time. Avec `--spec-draft-n-max 4`, le même lot tombe à **120,65 secondes**, avec un taux d’acceptation agrégé de **0,5881**. Cela correspond à environ **2,4×** d’amélioration du temps mural dans ce test.

Un autre retour dans la même PR, après corrections de configuration multi-GPU et placement du drafter sur le bon GPU, passe de **52,52 secondes** sans MTP à **21,05 secondes** avec MTP sur une configuration **RTX 5090 + RTX 4090**, soit environ **2,5×** de gain. Ces chiffres ne sont pas des moyennes universelles, mais ils montrent que l’approche peut vraiment payer quand le couple modèle principal / assistant / matériel / paramètres est bien aligné.

La commande de base donnée dans la PR ressemble à ceci :

```bash
llama-server -hf am17an/Gemma4-31B-it-GGUF \
  --spec-type draft-mtp \
  --spec-draft-n-max 4
```

En multi-GPU, les exemples ajoutent des options de placement du drafter, par exemple `--device-draft CUDA1` ou `--spec-draft-device CUDA1` selon les versions et les noms d’option. Ce détail est important : si le drafter et le modèle principal se marchent dessus côté mémoire ou scheduling, l’accélération théorique peut s’évaporer assez vite.

## Pourquoi ça compte pour les machines locales

Le speculative decoding est particulièrement pertinent pour l’inférence locale parce qu’il attaque directement le problème le plus visible pour l’utilisateur : la latence de génération. Une RTX grand public, une station multi-GPU, ou même un serveur homelab n’ont pas les marges d’un cluster cloud. Si un drafter compact permet de gagner 50 %, 100 % ou plus sur certains prompts, cela change l’expérience d’un assistant local.

Gemma 4 est aussi un bon candidat parce que Google a publié des modèles assistants/drafters associés. Pour l’écosystème GGUF, cela signifie que l’on peut espérer une chaîne plus propre : modèle principal quantifié, modèle assistant compatible, runtime `llama.cpp`, puis intégration downstream dans Ollama, LM Studio ou d’autres interfaces quand elles mettront à jour leur version embarquée de `llama.cpp`.

Mais il faut garder une distinction nette : le support est dans `llama.cpp` mainline, pas automatiquement dans tous les outils qui l’utilisent. Si ton interface bundle une version plus ancienne, tu ne verras rien. Et si elle expose mal les options de speculative decoding, tu auras peut-être les fichiers GGUF sans le vrai contrôle des paramètres. La plomberie, encore elle. Toujours elle.

## Les pièges déjà visibles

Le fil de la PR et l’issue **#24266** rappellent que le MTP n’est pas gratuit. Un utilisateur a signalé une chute de performances sur **Gemma 4 12B** sous Windows/CUDA : environ **40+ tokens/s** sans speculative decoding, mais seulement **4–5 tokens/s** avec `ngram-mod` activé après le merge lié à Gemma4 MTP. En désactivant `ngram-mod`, les performances revenaient autour de **40 tokens/s**. L’issue est étiquetée `bug-unconfirmed`, mais d’autres commentaires évoquent aussi des comportements similaires, y compris sur Intel Mac via Vulkan/MoltenVK.

Ce point est crucial : la régression ne semble pas limitée au mode `draft-mtp` strict. Elle touche potentiellement des chemins de speculative decoding comme `ngram-mod` ou `--spec-default`, selon les environnements. Un commentaire recommande de tester un build plus récent incluant la PR **#24277**, et plusieurs retours suggèrent que `--spec-draft-n-max 1` peut être plus rapide que `2` dans certains cas après les changements Gemma MTP.

Autre piège : la qualité du drafter et la quantization. Des commentaires indiquent que Gemma est sensible à la qualité MTP, et que descendre trop bas en quantization peut réduire fortement le taux d’acceptation. Si le modèle assistant propose des tokens que le modèle principal rejette trop souvent, l’utilisateur paie le coût du drafter sans récolter l’accélération. C’est le speculative decoding dans sa forme la plus honnête : une promesse conditionnelle, pas une subvention cosmique.

## Recommandation pratique

Pour tester proprement, il faut traiter Gemma4 MTP comme une fonctionnalité expérimentale mais sérieuse. D’abord, partir d’un build récent de `llama.cpp`, idéalement postérieur aux correctifs mentionnés dans les discussions. Ensuite, tester avec et sans MTP sur les mêmes prompts, en mesurant le temps mural et les tokens/s, pas seulement “ça semble plus rapide”. Enfin, varier prudemment `--spec-draft-n-max`, en commençant bas : les retours GitHub montrent que `1` peut parfois battre `2` ou plus selon le matériel et le modèle.

Sur multi-GPU, il faut aussi contrôler explicitement où tourne le drafter. Les gains cités dans la PR apparaissent après correction de la configuration multi-GPU ; avant cela, des utilisateurs voyaient le MTP ralentir. Sur contexte long, il faut surveiller le KV cache, les options `-ctk` / `-ctv`, et la mémoire disponible. Les interactions entre long contexte, quantization KV et speculative decoding peuvent vite devenir non intuitives.

Pour un usage quotidien, la prudence est simple : ne remplace pas une configuration stable par MTP sans benchmark local. Sur un modèle et une machine donnés, l’accélération peut être nette. Sur un autre couple modèle/quant/runtime, elle peut être nulle, voire négative. C’est précisément le genre d’optimisation qui mérite un script de test avant d’entrer dans ton alias shell permanent.

## À surveiller

Le prochain signal important sera l’absorption de ce support par les outils en aval : builds `llama.cpp` packagés, Ollama, LM Studio, interfaces serveur, collections GGUF de modèles assistants Gemma 4 et documentation reproductible. Il faudra aussi suivre la résolution de l’issue #24266 et des régressions autour de `ngram-mod` / `--spec-default`.

Pour le moment, Gemma4 MTP dans `llama.cpp` est une vraie avancée : elle montre que les runtimes locaux ne se contentent plus de charger des poids quantifiés, ils intègrent aussi des techniques d’inférence plus sophistiquées. Mais c’est une avancée d’ingénierie, pas une incantation. Les gains existent. Les pièges aussi. Ce qui, dans notre petit monde, est généralement le signe qu’un sujet est enfin devenu intéressant.

## Sources

- GitHub — llama.cpp PR #23398: add Gemma4 MTP : https://github.com/ggml-org/llama.cpp/pull/23398
- GitHub — llama.cpp issue #24266: Gemma4 MTP regression : https://github.com/ggml-org/llama.cpp/issues/24266
- GitHub — llama.cpp discussion #22735: Gemma 4 assistant/drafter support : https://github.com/ggml-org/llama.cpp/discussions/22735
