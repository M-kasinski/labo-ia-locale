---
title: "Nex-N2 : l’agent open-weight qui promet le long-horizon, mais pas le laptop magique"
description: "Nex AGI publie Nex-N2-Pro et Nex-N2-mini, deux modèles MoE open-weight sous Apache 2.0 orientés agents, code et tool-use. Le signal est fort, mais les chiffres restent surtout fournisseur."
pubDate: 2026-06-09
category: "local"
tags: ["Nex-N2", "open-weight", "agents", "SGLang", "Qwen", "tool-use"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Hugging Face — nex-agi/Nex-N2-Pro"
    url: "https://huggingface.co/nex-agi/Nex-N2-Pro"
  - label: "Hugging Face — nex-agi/Nex-N2-mini"
    url: "https://huggingface.co/nex-agi/Nex-N2-mini"
  - label: "SiliconFlow — Nex-N2-Pro model card"
    url: "https://www.siliconflow.com/models/nex-n2-pro"
  - label: "Fello AI — Nex-N2-Pro overview, June 9 2026"
    url: "https://felloai.com/nex-n2-pro/"
---

Nex AGI vient d’ajouter un nom de plus à la pile déjà dense des modèles agentiques open-weight : **Nex-N2**. La famille comprend deux variantes, **Nex-N2-Pro** et **Nex-N2-mini**, toutes deux publiées sur Hugging Face et ModelScope, avec un positionnement très clair : code, outils, terminal, recherche web, tâches longues et workflows d’agent plutôt que simple chat de démonstration.

Le point intéressant pour l’IA locale n’est pas seulement “encore un modèle qui bat GPT-machin sur un graphe”. C’est le compromis annoncé : un gros **MoE 397B** pour la qualité, et un **MoE 35B** plus réaliste pour les gens qui ne rangent pas des H100 dans le placard à balais. Les fiches Hugging Face indiquent que les deux modèles sont post-entraînés depuis des bases **Qwen3.5** : **Qwen3.5-397B-A17B** pour Nex-N2-Pro et **Qwen3.5-35B-A3B-Base** pour Nex-N2-mini.

La licence annoncée est **Apache 2.0** côté SiliconFlow et dans la couverture de lancement. C’est un point important : si la licence est bien celle appliquée aux poids et au code associé, elle autorise des usages commerciaux et des dérivés avec beaucoup moins de friction que les licences “open-weight mais pas trop”. Comme toujours, pour un déploiement sérieux, il faut lire la licence du dépôt et de chaque artefact téléchargé. Le mot “open-source” se porte parfois comme un costume trop grand.

## Ce que Nex AGI appelle “Agentic Thinking”

Le concept central de Nex-N2 est **Agentic Thinking**. Sur les fiches modèle, Nex AGI le décrit comme une boucle qui unifie compréhension de la demande, planification, implémentation, exécution dans l’environnement, retour d’erreur, évaluation et itération. En clair : le modèle est entraîné et évalué pour rester utile pendant une tâche qui se déroule, pas seulement pour produire une bonne première réponse.

Deux sous-idées structurent ce discours. **Adaptive Thinking** doit permettre au modèle de décider quand raisonner profondément et quand répondre vite. **Coherent Thinking** vise à garder un même régime de raisonnement entre code, outils, recherche et tâches multimodales. Si cela tient en pratique, c’est exactement le genre de propriété qui manque aux agents locaux actuels : ils savent appeler des outils, puis se perdent, répètent une action inutile, ou changent de stratégie sans bonne raison.

À ce stade, il faut rester sobre : ce sont des claims fournisseur. Ils sont plausibles, ils correspondent aux problèmes réels des agents, mais ils ne remplacent pas des traces reproductibles sur des tâches longues, avec logs d’outils, coûts, temps d’exécution et taux d’échec. Pour un média local-first, la bonne lecture est donc : signal intéressant, validation communautaire encore nécessaire.

## Les deux variantes : Pro pour serveur, mini pour homelab musclé

**Nex-N2-Pro** est le modèle phare. La fiche Hugging Face indique **397 milliards de paramètres** en **BF16**, au format **Safetensors**. SiliconFlow le liste comme une architecture **Transformer MoE**, avec **397B paramètres totaux**, un contexte de **262K tokens** et jusqu’à **256K tokens** de sortie côté service. La couverture de Fello AI précise une activation d’environ **17B paramètres par token**, cohérente avec la base Qwen3.5-397B-A17B mentionnée par Nex AGI.

Soyons nets : ce n’est pas un modèle “local” au sens laptop. En BF16, un 397B est un animal de datacenter. Même en quantization agressive, on parle d’une machine multi-GPU sérieuse, d’un serveur partagé, ou d’un prestataire d’inférence. Nex AGI fournit d’ailleurs des exemples de lancement via **SGLang**, y compris des commandes Docker avec tensor parallelism et des configurations multi-nœuds. C’est utile pour l’auto-hébergement professionnel, beaucoup moins pour le Mac mini sous le bureau.

**Nex-N2-mini** est plus pertinent pour le lectorat local. Sa fiche Hugging Face annonce **35B paramètres**, en **BF16**, également au format Safetensors. La base indiquée est **Qwen3.5-35B-A3B-Base**, donc un MoE avec environ **3B actifs** selon la nomenclature du modèle source. En pratique, 35B reste lourd, mais il devient envisageable sur une station avec gros GPU, plusieurs GPU grand public, ou une quantization bien faite. Ce n’est pas “tout public”, mais ce n’est plus la salle machine.

Le détail qui manque encore : des quants communautaires fiables, des mesures llama.cpp ou vLLM/SGLang sur matériel accessible, et des retours sur le tool-use après quantization. Un modèle agentique peut très bien conserver ses benchmarks généraux et perdre sa discipline JSON, ses appels d’outils ou sa stabilité en contexte long une fois compressé. C’est précisément là que se joue l’intérêt local.

## Benchmarks : impressionnants, mais à lire avec les mains dans les poches

Les fiches Hugging Face publient un tableau de résultats ambitieux. Pour **Nex-N2-Pro**, Nex AGI annonce notamment **80,8 sur SWE-Bench Verified**, **58,8 sur SWE-Bench Pro**, **75,3 sur Terminal-Bench 2.1**, **83,7 sur BrowseComp**, **71,1 sur TAU3**, **51,9 sur Toolathlon** et **53,5 sur WildClawBench**. Pour **Nex-N2-mini**, les scores indiqués sont plus bas mais restent notables : **74,4 sur SWE-Bench Verified**, **50,2 sur SWE-Bench Pro**, **60,7 sur Terminal-Bench 2.1** et **65,9 sur TAU3**.

Ces chiffres placent Pro dans la conversation des modèles fermés et des meilleurs open-weight agentiques, au moins selon les tableaux publiés par Nex AGI. La fiche compare notamment Nex-N2-Pro à GPT-5.5, Opus 4.7, Kimi-K2.6, GLM-5.1, MiniMax M3 et DeepSeek-V4-Pro. Fello AI reprend la même lecture, avec une conclusion raisonnable : le modèle paraît compétitif, pas magiquement dominant.

C’est la bonne nuance. Les benchmarks agentiques sont fragiles : différences de harness, prompts système, budgets de tokens, accès outils, temps autorisé, retry, environnement logiciel. Deux modèles peuvent être comparés sur une ligne de tableau tout en ayant vécu des conditions assez différentes. Les scores sont donc utiles pour décider quoi tester, pas pour décréter un nouveau roi. La monarchie des benchmarks a déjà assez de courtisans.

## Pourquoi c’est important pour l’auto-hébergement

Nex-N2 confirme une tendance nette : les modèles open-weight ne visent plus seulement le chatbot généraliste, mais l’**agent de production**. Les tâches citées — terminal, code, recherche, tool-use, workflows longs — sont exactement celles que les équipes veulent garder près de leurs dépôts, de leurs tickets, de leurs bases internes et de leurs documents sensibles.

Dans une pile auto-hébergée, Nex-N2-mini pourrait devenir intéressant comme moteur d’agent local pour : revue de code interne, scripts d’exploitation, navigation dans un dépôt, génération de tests, tri de tickets, RAG technique avec appels d’outils, ou assistant de recherche qui reste dans le réseau de l’entreprise. Pro, lui, ressemble plutôt à un modèle pour serveur interne haut de gamme ou cloud privé.

Le support SGLang documenté est aussi un signal pratique. Les agents ne sont pas servis comme des chats simples : ils ont besoin de contexte long, streaming, tool calling, parfois raisonnement séparé, batchs irréguliers, reprise après erreur et traces exploitables. Si Nex-N2 fonctionne bien avec SGLang, il peut s’intégrer dans des architectures locales sérieuses plus facilement qu’un checkpoint publié sans chemin d’exécution clair.

## Ce qu’il faut tester avant d’y croire

Trois tests me semblent prioritaires.

D’abord, **la robustesse des outils** : appels de fonctions valides, respect du schéma, récupération après erreur, absence d’appels fantômes. Ensuite, **la tenue en tâche longue** : est-ce que le modèle améliore réellement sa solution après plusieurs cycles terminal/test/correction, ou tourne-t-il en rond élégamment ? Enfin, **l’effet de la quantization** : un agent local utile en BF16 mais instable en 4-bit n’est pas inutile, mais son marché se réduit vite.

Il faudra aussi clarifier les coûts réels. Un 35B MoE peut être confortable si seuls quelques milliards de paramètres sont actifs, mais la mémoire des poids reste là. Le KV cache en contexte long peut devenir le vrai goulet d’étranglement, surtout si l’on pousse les 100K+ tokens. Pour du RAG local, mieux vaut souvent un modèle plus petit, très fiable en tool-use, qu’un grand modèle qui avale tout le contexte et expire bruyamment.

Nex-N2 mérite donc clairement un banc d’essai local. Pas parce qu’il “remplace GPT-5.5” — ce genre de phrase devrait déclencher un extincteur automatique — mais parce qu’il met l’accent sur le bon problème : faire travailler un modèle ouvert dans une boucle d’agent réelle, avec code, outils et feedback. Si Nex-N2-mini tient après quantization, il pourrait devenir une brique très sérieuse pour les agents auto-hébergés.

## Sources

- Hugging Face — nex-agi/Nex-N2-Pro : https://huggingface.co/nex-agi/Nex-N2-Pro
- Hugging Face — nex-agi/Nex-N2-mini : https://huggingface.co/nex-agi/Nex-N2-mini
- SiliconFlow — Nex-N2-Pro model card : https://www.siliconflow.com/models/nex-n2-pro
- Fello AI — Nex-N2-Pro overview, June 9 2026 : https://felloai.com/nex-n2-pro/
