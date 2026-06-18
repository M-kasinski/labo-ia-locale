---
title: "vLLM 0.22.1 : les CPU AMD Zen gagnent un vrai chemin d’inférence quantifiée"
description: "La patch release vLLM 0.22.1 ajoute zentorch pour les linéaires W8A8 et W4A16 sur CPU AMD Zen, tout en corrigeant DeepSeek-V4 et le serving Ray multi-nœud."
pubDate: 2026-06-08
category: "local"
tags: ["vLLM", "AMD", "CPU", "zentorch", "quantization", "inference locale"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub Releases — vLLM v0.22.1"
    url: "https://github.com/vllm-project/vllm/releases/tag/v0.22.1"
  - label: "GitHub Releases — vLLM v0.22.0"
    url: "https://github.com/vllm-project/vllm/releases/tag/v0.22.0"
  - label: "vLLM Blog — DeepSeek V4 in vLLM"
    url: "https://vllm.ai/blog/2026-04-24-deepseek-v4"
---

vLLM vient de publier **v0.22.1**, une patch release datée du **5 juin 2026**. Sur le papier, huit commits, six contributeurs, rien de spectaculaire. En pratique, cette version mérite un arrêt pour l’IA locale et semi-locale : elle ajoute un chemin d’inférence quantifiée accéléré par **zentorch** sur **CPU AMD Zen**, corrige un problème d’initialisation **DeepSeek-V4**, et répare un blocage déterministe en serving **Ray data-parallel multi-nœud**.

Ce n’est pas une release qui promet de transformer un Ryzen en grappe B200. Restons civilisés. Mais elle confirme une tendance utile : vLLM ne se limite plus au gros serving GPU NVIDIA. Le projet continue de descendre dans les couches moins glamour — CPU, quantization, compatibilité de modèles, orchestration — là où les déploiements réels cassent souvent.

## Le changement le plus intéressant : zentorch sur AMD Zen

La note de release officielle indique que vLLM route désormais certaines inférences linéaires quantifiées vers des kernels **zentorch** sur CPU AMD Zen. Les chemins concernés sont **W8A8**, décrit comme de l’`int8 dynamic-symmetric`, et **W4A16**, côté **GPTQ**. Ces kernels sont enregistrés avant les kernels CPU génériques **oneDNN**, avec fallback transparent sur les CPU non-Zen, GPU et XPU.

Le point important n’est pas seulement “AMD va plus vite”. C’est plus précis : vLLM commence à traiter les CPU Zen comme une cible optimisable pour des formats quantifiés concrets. Pour les homelabs, les petites machines de bureau et les serveurs d’inférence de test, cela peut compter. Beaucoup d’utilisateurs locaux ont des Ryzen récents, parfois avec beaucoup de RAM, mais sans GPU capable d’avaler un gros modèle. Sur ce terrain, chaque optimisation CPU est une petite victoire contre le ventilateur inutilement héroïque.

Il faut toutefois éviter de surinterpréter. La release ne publie pas, dans son résumé, de benchmark chiffré global pour ces chemins zentorch. On sait ce qui est routé, on sait où le fallback s’applique, mais on ne peut pas conclure à un multiplicateur universel. Les gains dépendront du modèle, du format de quantization, de la taille du batch, du nombre de threads, de la mémoire et du profil de requêtes. Pour un usage interactif mono-utilisateur, le goulot peut rester ailleurs. Pour du batch CPU quantifié, le gain peut devenir plus visible.

## W8A8 et W4A16 : pourquoi c’est le bon niveau d’abstraction

Les formats cités ne sont pas anecdotiques. **W8A8** réduit poids et activations en 8 bits dans le chemin dynamique symétrique. **W4A16**, lui, correspond à une logique courante des modèles **GPTQ** : poids fortement compressés, activations en précision plus confortable. Dans les deux cas, l’objectif est simple : réduire le coût mémoire et accélérer les opérations linéaires sans exiger une pile GPU spécialisée.

Pour l’IA locale, c’est intéressant parce que le CPU redevient parfois rationnel. Pas pour servir un MoE géant à 100 utilisateurs. Mais pour des modèles petits ou moyens, des tâches batch, de l’embedding, du reranking, ou des environnements où le GPU n’est pas disponible en continu. Les déploiements auto-hébergés ont souvent cette réalité : on veut une machine stable, pas forcément un benchmark qui fait joli sur X.

vLLM garde ici une approche prudente : le fallback transparent évite de casser les environnements qui ne sont pas AMD Zen. C’est un détail d’ingénierie important. Un runtime local utile n’est pas seulement rapide sur la bonne machine ; il doit aussi ne pas exploser sur la mauvaise.

## DeepSeek-V4 : le support continue d’être durci

v0.22.1 corrige aussi une incompatibilité **CUTLASS `fmin`** qui empêchait l’initialisation de **DeepSeek-V4**. Cela arrive juste après vLLM **v0.22.0**, une release beaucoup plus massive publiée fin mai, qui avait déjà consacré un gros bloc à DeepSeek V4 : package dédié `vllm/models/deepseek_v4/`, support **NVFP4 fused MoE**, graphes CUDA complets et partiels, **MTP speculative decoding**, sparse MLA et refactorisation autour du compresseur.

Le blog vLLM sur DeepSeek V4 donne le contexte : la famille comprend **DeepSeek-V4-Pro** et **DeepSeek-V4-Flash**, avec un contexte annoncé jusqu’à **1 million de tokens**. Le billet détaille une attention long contexte reposant notamment sur le partage key/value, la compression du KV cache, **DeepSeek Sparse Attention** et une fenêtre locale courte. Il donne aussi des exemples de serving plutôt costauds : **DeepSeek-V4-Pro** sur **8× B200 ou 8× B300**, et **DeepSeek-V4-Flash** sur **4× B200 ou 4× B300**.

Autrement dit : DeepSeek-V4 n’est pas soudain devenu un modèle de laptop. Mais les corrections vLLM comptent pour les équipes qui veulent l’auto-héberger sur infrastructure musclée, ou simplement tester des chemins compatibles OpenAI sans rester collées à une API distante. Pour le lectorat local, le vrai signal est moins “tu vas le lancer dans ton salon” que “les runtimes open-source absorbent vite les architectures de frontière”.

## Ray multi-nœud : le genre de bug qui coûte une journée

La release corrige également un blocage déterministe avec **Ray data-parallel** en multi-nœud lorsque `num_api_servers > 1`. La cause indiquée touche l’allocation différée de ports assignés par le kernel, introduite précédemment ; vLLM exclut désormais le backend Ray DP de ce comportement.

Ce n’est pas sexy, mais c’est exactement le genre de fix qui fait la différence entre “ça marche dans le notebook” et “le service redémarre en production”. Pour les petits clusters locaux — deux ou trois machines GPU, ou un lab interne — les bugs de coordination sont souvent plus pénibles que les bugs de modèle. Ils ne donnent pas toujours une erreur claire ; ils pendent. Et un serveur qui pend est une forme très raffinée de mépris logiciel.

## Mellum v2 et autres corrections de compatibilité

vLLM 0.22.1 ajoute aussi le support de **JetBrains Mellum v2**, décrit dans la release comme un modèle de code **open-weight Mixture-of-Experts**. Là encore, pas besoin de transformer ça en événement isolé : c’est plutôt la preuve que vLLM reste un runtime de référence pour suivre les modèles récents, notamment ceux orientés code et agents.

La patch release corrige aussi des régressions de chargement, dont **HyperCLOVAX**, après le retrait de remote code côté dépôt Hugging Face amont, et un problème d’initialisation `OlmoHybridForCausalLM` lié à un changement de métadonnées `rope_parameters`. Elle répare enfin des soucis de build Docker, notamment autour de `flashinfer-jit-cache` mis en quarantaine sur PyPI.

Ces détails ont l’air périphériques. Ils ne le sont pas. Dans un environnement auto-hébergé, les cassures viennent souvent de ces frontières : un dépôt Hugging Face modifie son code, une dépendance PyPI change d’état, un champ de config évolue, une image Docker ne build plus. vLLM 0.22.1 est une release de plomberie, et la plomberie est précisément ce qu’on découvre quand elle casse.

## Faut-il mettre à jour ?

Si tu utilises vLLM uniquement sur GPU NVIDIA avec des modèles stables et sans DeepSeek-V4, l’urgence est limitée. Si tu testes **DeepSeek-V4**, si tu fais du serving **Ray multi-nœud**, si tu charges **Mellum v2**, ou si tu exploites des **CPU AMD Zen** pour de l’inférence quantifiée, la mise à jour mérite clairement un test.

Pour les utilisateurs locaux, le message est sobre : vLLM reste une pile plus lourde qu’Ollama ou llama.cpp, mais elle continue de devenir plus intéressante dès qu’on parle de serving, de batching, de modèles récents et de configurations matérielles moins triviales. La v0.22.1 ne change pas la carte du monde. Elle ajoute quelques routes. Et parfois, c’est exactement ce qui évite de finir dans le fossé.

## Sources

- GitHub Releases — vLLM v0.22.1 : https://github.com/vllm-project/vllm/releases/tag/v0.22.1
- GitHub Releases — vLLM v0.22.0 : https://github.com/vllm-project/vllm/releases/tag/v0.22.0
- vLLM Blog — DeepSeek V4 in vLLM : https://vllm.ai/blog/2026-04-24-deepseek-v4
