---
title: "Qwen3.6 et MTP : l'accélération qui rend le local crédible"
description: "Qwen3.6 arrive avec des têtes MTP exploitables par llama.cpp et vLLM : assez pour accélérer l’inférence locale, mais pas dans tous les cas."
pubDate: 2026-05-29
category: "local"
tags: ["ia-locale", "qwen", "mtp", "vllm", "llama-cpp", "performance"]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "Qwen/Qwen3.6-27B — carte modèle Hugging Face", url: "https://huggingface.co/Qwen/Qwen3.6-27B" }
  - { label: "Qwen/Qwen3.6-35B-A3B — carte modèle Hugging Face", url: "https://huggingface.co/Qwen/Qwen3.6-35B-A3B" }
  - { label: "llama.cpp PR #22673 — MTP Support", url: "https://github.com/ggml-org/llama.cpp/pull/22673" }
  - { label: "llama.cpp PR #23198 — optimisation prompt decode MTP", url: "https://github.com/ggml-org/llama.cpp/pull/23198" }
  - { label: "vLLM Recipes — Qwen3.5 & Qwen3.6 Usage Guide", url: "https://docs.vllm.ai/projects/recipes/en/latest/Qwen/Qwen3.5.html" }
  - { label: "Better & Faster Large Language Models via Multi-token Prediction", url: "https://arxiv.org/abs/2404.19737" }
  - { label: "On multi-token prediction for efficient LLM inference", url: "https://arxiv.org/abs/2502.09419" }
---

## Le vrai sujet : moins d’allers-retours, pas de magie

L’inférence d’un LLM causal est bêtement séquentielle : pour générer le token 101, il faut avoir choisi le token 100. Même avec une grosse carte graphique, une partie du temps part donc dans une boucle serrée : calculer, échantillonner, recommencer. Le MTP, pour multi-token prediction, attaque précisément cette boucle.

L’idée n’est pas que le modèle « saute » la génération autoregressive. Il reste vérifié token par token. Mais au lieu de ne produire qu’une distribution pour le prochain token, le modèle dispose de têtes auxiliaires capables de proposer plusieurs tokens futurs. Ces propositions servent de brouillon. Le chemin principal vérifie ensuite lesquelles sont compatibles avec ce que le modèle aurait produit normalement. Quand l’acceptation est bonne, on valide plusieurs tokens pour un coût inférieur à plusieurs pas de décodage complets.

C’est le lien avec le decoding spéculatif : traditionnellement, on utilise un petit modèle draft, rapide mais moins fiable, puis le gros modèle vérifie. Avec MTP, le draft est interne au modèle. Pas besoin de charger un second modèle, mais il faut que le checkpoint expose ces têtes et que le runtime sache les utiliser. Sinon, les têtes MTP restent du poids mort dans le fichier.

## Ce que Qwen3.6 apporte concrètement

Qwen3.6 est intéressant parce que les modèles officiellement publiés cochent plusieurs cases locales à la fois. La carte Hugging Face de Qwen3.6-27B décrit un modèle causal avec encodeur vision, 27 milliards de paramètres, 64 couches, une architecture hybride alternant Gated DeltaNet et attention, un contexte natif de 262 144 tokens, extensible jusqu’à 1 010 000 tokens, et surtout une ligne explicite : « MTP: trained with multi-steps ».

La variante Qwen3.6-35B-A3B pousse l’idée côté MoE : 35 milliards de paramètres au total, environ 3 milliards activés, 40 couches, 256 experts avec 8 experts routés plus 1 expert partagé, le même contexte natif de 262 144 tokens, et là encore MTP entraîné en multi-étapes. Pour une machine locale, cette distinction compte : un 27B dense vise la qualité d’un modèle moyen/haut de gamme, tandis que le 35B-A3B réduit le coût actif par token grâce au MoE.

Le « sweet spot » vient donc de la combinaison, pas d’un seul chiffre. 27B/35B reste gros pour du laptop banal, mais devient crédible sur une station locale musclée, un Mac à mémoire unifiée généreuse, ou une machine GPU 24–48 Go selon quantification et contexte. Ajoutez MTP, et la génération peut passer de « utilisable » à « assez rapide pour coder avec ». C’est exactement la zone où le local cesse d’être une posture idéologique et devient un outil quotidien.

## Ce qui est confirmé côté llama.cpp

Côté llama.cpp, le support MTP est confirmé par la PR ggml-org/llama.cpp #22673, fusionnée le 16 mai 2026. Son résumé est explicite : ajout du support des têtes MTP, testé sur Qwen3.6 27B et Qwen3.6 35B-A3B. La commande documentée utilise `--spec-type draft-mtp` avec `--spec-draft-n-max`, par exemple 2 ou 3 tokens draft.

Les chiffres de cette PR sont utiles, mais il faut les lire comme un benchmark de PR, pas comme une promesse universelle. Sur un test DGX Spark avec Qwen3.6 27B en Q8_0, le baseline sans MTP annonce 1 404 tokens générés en 201,07 s sur 9 requêtes. Avec MTP et `--spec-draft-n-max 3`, la PR rapporte 1 406 tokens en 83,8 s, une acceptation agrégée de 0,7218 et des débits par tâche typiquement autour de 13,9 à 21,6 tok/s contre environ 7 tok/s sans MTP. Le texte de la PR résume cela comme environ 75 % d’acceptation stable avec 3 tokens draft et plus de 2× de speed-up sur son banc.

Autre point confirmé : tout n’est pas gratuit. La PR note que le prompt processing peut ralentir avec MTP, notamment à cause des transferts Device-to-Host des embeddings. Une PR suivante, #23198, fusionnée le 17 mai 2026, optimise ce point en évitant de copier les logits pour chaque token pendant le prompt decode MTP. Moralité : MTP accélère surtout la génération, pas forcément le préremplissage d’un très long prompt.

## Ce qui est confirmé côté vLLM

vLLM documente aussi Qwen3.6 avec MTP. Le guide officiel « Qwen3.5 & Qwen3.6 Usage Guide » montre une commande `vllm serve Qwen/Qwen3.6-35B-A3B` avec `--max-model-len 262144` et, pour activer le spéculatif MTP, `--speculative-config '{"method": "mtp", "num_speculative_tokens": 2}'`.

Le même guide donne la nuance importante : MTP-1 réduit la latence par token, mais peut dégrader le débit texte à haute concurrence, car les tokens spéculatifs consomment de la capacité de KV cache et réduisent le batch effectif. vLLM recommande donc MTP pour les workloads sensibles à la latence et à faible concurrence ; pour du serving massif, il faut mesurer. C’est moins sexy qu’un « 2× partout », mais beaucoup plus vrai.

Je n’ai pas trouvé, dans les sources primaires consultées, de release vLLM stable associant un numéro précis uniquement à « Qwen3.6 MTP support ». Le support est documenté dans les recettes officielles, et des issues/PRs ouvertes mentionnent des cas réels Qwen3.6 + MTP, mais je ne vais pas inventer une version. À ce stade, la formulation propre est : support documenté par vLLM, version exacte à vérifier dans votre environnement ou dans la recette au moment de déployer.

## Quand ça vaut le coup maintenant

Oui, si votre usage est interactif : agent de code, assistant local, complétion longue, rédaction technique, boucle humain-machine où la latence ressentie domine. Là, accepter deux ou trois tokens d’un coup change l’expérience. Les tâches structurées — code, formats répétitifs, raisonnement avec contexte clair — sont de bons candidats, car les drafts ont plus de chances d’être acceptés.

Oui aussi si vous êtes déjà dans llama.cpp ou vLLM et que vous pouvez utiliser un checkpoint MTP compatible. Dans llama.cpp, il faut un GGUF qui conserve les couches MTP et une build récente contenant la PR fusionnée. Dans vLLM, il faut passer par la configuration spéculative documentée et surveiller mémoire, KV cache et concurrence.

Non, ou pas encore, si votre goulot est le prompt processing sur des contextes énormes, si vous servez beaucoup d’utilisateurs en parallèle, ou si vous générez à température élevée avec des sorties très imprévisibles. Dans ces cas, l’acceptation baisse ou le coût mémoire mange le gain. Même punition si vous utilisez une quantification ou un port GGUF qui a perdu les têtes MTP : le modèle peut s’appeler Qwen3.6, mais le runtime n’aura rien à exploiter.

## Le verdict local

Qwen3.6 + MTP ne rend pas l’inférence locale miraculeuse. Ça la rend moins absurde. La différence est importante. On a désormais des modèles dans la zone 27B/35B, avec contexte long, architecture hybride, variantes MoE, et têtes MTP officiellement présentes. En face, llama.cpp a un support fusionné avec des gains mesurés dans sa PR, et vLLM documente l’usage MTP pour Qwen3.6 avec les réserves de concurrence qui vont bien.

La bonne stratégie, maintenant, c’est pragmatique : commencez avec 1 à 3 tokens spéculatifs, mesurez l’acceptation, le débit de génération, le temps de premier token et l’usage mémoire. Si l’acceptation tient et que votre machine ne swap pas, gardez MTP. Sinon, baissez le nombre de tokens ou revenez au décodage classique. Le local avance rarement par révolution propre ; ici, il gagne surtout par petits raccourcis très bien placés.