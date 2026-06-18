---
title: "AutoRound 0.13 : Intel rend la quantization low-bit plus portable pour vLLM, MLX et GGUF"
description: "La version 0.13 d'AutoRound ajoute MTP, export MLX, model-free quantization et de nouveaux chemins W4A16/W8A16 : une brique discrète, mais utile pour faire tenir les modèles locaux."
pubDate: 2026-06-04
category: "local"
tags: ["quantization", "vllm", "gguf", "mlx"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Release AutoRound v0.13.0"
    url: "https://github.com/intel/auto-round/releases"
  - label: "Dépôt Intel AutoRound"
    url: "https://github.com/intel/auto-round"
  - label: "Documentation vLLM AutoRound"
    url: "https://docs.vllm.ai/en/v0.14.0/features/quantization/auto_round/"
  - label: "Documentation vLLM-Omni AutoRound"
    url: "https://docs.vllm.ai/projects/vllm-omni/en/latest/user_guide/quantization/autoround/"
---

La quantization n'a pas le sex-appeal d'un nouveau modèle MoE à un trillion de paramètres. C'est injuste, mais compréhensible : personne ne rêve en `group_size=128`. Pourtant, pour l'IA locale, c'est souvent là que tout se joue. Un modèle qui ne rentre pas en mémoire est un modèle théorique. **AutoRound 0.13.0**, publié par Intel le 31 mai 2026, mérite donc qu'on s'y arrête : la release ajoute des briques qui touchent directement vLLM, GGUF, MLX, les couches MTP et les déploiements CPU/XPU.

AutoRound est un toolkit de **post-training quantization** pour LLM et VLM. Son objectif : produire des modèles en **2 à 4 bits** avec une perte de précision limitée, en s'appuyant notamment sur une méthode de descente de gradient sur le signe (*sign-gradient descent*). Le projet est sous Apache 2.0, public sur GitHub, et annonce une compatibilité avec Transformers, vLLM, SGLang, LLM-Compressor et des exports comme GGUF. Rien de magique, mais une brique de plomberie qui peut économiser beaucoup de VRAM.

## Ce que change la version 0.13

La page des releases liste plusieurs ajouts notables dans **v0.13.0**. Le premier est le support de la **quantization MTP**. MTP, pour *multi-token prediction*, apparaît de plus en plus dans les modèles récents et les runtimes orientés débit : l'idée est de prédire plusieurs tokens futurs ou d'utiliser des têtes auxiliaires pour accélérer le décodage. Quantifier ces couches sans casser le runtime devient donc important. AutoRound indique un support spécifique, avec des traitements particuliers comme la gestion de `gate_up_proj` et l'évitement de certaines couches `mtp.fc` lorsque vLLM ne les supporte pas.

Deuxième point : un support plus unifié des backends **CPU/XPU**. C'est cohérent avec le positionnement Intel, mais intéressant au-delà des machines Intel. La quantization locale ne doit pas être uniquement une affaire de CUDA. Les laptops, mini-PC, serveurs CPU, iGPU et accélérateurs plus modestes ont aussi besoin d'un chemin viable. AutoRound ne transforme pas un CPU en H100 de poche — on reste dans le monde réel, hélas — mais chaque amélioration de backend réduit la dépendance à une seule pile matérielle.

Troisième ajout : la **model-free weight-only quantization**. Le dépôt indique qu'en mai 2026, `auto-round-rtn` utilise désormais par défaut une approche sans modèle pour les schémas INT weight-only compatibles. En pratique, cela vise à réduire la friction : moins de calibration lourde, plus de chemins rapides pour produire une version quantifiée exploitable. À vérifier modèle par modèle, bien sûr, car “rapide” et “bon” ne se serrent pas toujours la main.

## W4A16, W8A16, GGUF, MLX : l'intérêt local

La release 0.13 mentionne aussi l'export **compressed-tensors** pour **W4A16** et **W8A16**, des corrections autour de GGUF, du GPTQ, ainsi qu'un **export MLX**. Ces trois lettres changent la lecture côté Mac : MLX est devenu l'un des chemins les plus crédibles pour l'inférence locale sur Apple Silicon, grâce à la mémoire unifiée et à des kernels pensés pour les puces M-series.

L'export GGUF reste tout aussi important. GGUF est le format de fait de l'écosystème llama.cpp, et donc d'une partie énorme des usages locaux : serveurs embarqués, wrappers simples, machines sans gros runtime Python, CPU + Metal, etc. AutoRound prend en charge l'export GGUF depuis 2025, mais la release 0.13 corrige encore des bugs liés à Qwen et ajuste les algorithmes de tuning GGUF. C'est moins spectaculaire qu'une annonce de modèle, mais c'est précisément ce qui rend les modèles réellement lançables chez soi.

La documentation vLLM indique de son côté qu'AutoRound peut quantifier un modèle vers un format `auto_round`, mais aussi vers `auto_gptq`, `auto_awq` ou `gguf:q4_k_m`. Elle donne un exemple simple sur `Qwen/Qwen3-0.6B` en 4 bits avec `group_size=128`, puis un exemple d'exécution dans vLLM avec `Intel/DeepSeek-R1-0528-Qwen3-8B-int4-AutoRound`.

## vLLM : quantization statique, chargement plus propre

Côté vLLM, AutoRound est présenté comme une quantization **weight-only** pour modèles transformer, avec des objectifs de réduction mémoire et d'accélération d'inférence tout en gardant une précision proche de l'original. La documentation liste des supports matériels assez larges : CPU, Intel GPU/XPU, HPU et GPU CUDA.

Le point pratique : une fois le checkpoint préparé au format AutoRound, vLLM peut le charger directement. La documentation vLLM-Omni insiste sur un détail utile : lorsque le `config.json` du checkpoint contient une configuration `quantization_config` avec `quant_method: "auto-round"`, AutoRound est détecté automatiquement. Il n'y a pas besoin d'ajouter un flag `--quantization` à l'inférence. C'est une petite chose, mais les petites choses évitent les grandes soirées à insulter un terminal.

vLLM-Omni élargit le sujet au multimodal : AutoRound y est décrit comme capable de produire des checkpoints pré-quantifiés pour **LLM**, **VLM** et modèles de **diffusion**. La documentation cite notamment des exemples autour de FLUX, Wan2.2, Qwen2.5-Omni et Qwen3-Omni, avec des schémas comme **W4A16**. Elle précise aussi que le support dépend du checkpoint : le runtime doit pouvoir mapper correctement les noms de blocs quantifiés vers ses modules internes.

## Les compromis : qualité, vitesse, reproductibilité

AutoRound propose plusieurs recettes. La documentation vLLM distingue notamment un mode “best accuracy”, plus lent, et un mode plus rapide utilisant moins d'itérations. L'exemple commenté indique que le mode le plus précis peut être **4 à 5 fois plus lent**, tandis qu'une configuration plus légère peut apporter **2 à 3 fois** plus de vitesse de quantization avec une légère perte de précision en W4G128. Ces chiffres décrivent le processus de quantification, pas forcément l'accélération finale en inférence.

C'est une nuance capitale. Une quantization 4 bits réduit la mémoire, et peut accélérer certains chemins, mais le résultat dépend du backend, du kernel, du batch, du modèle, du matériel et parfois de l'humeur des dieux de CUDA. Pour publier un benchmark sérieux, il faut mesurer sur une machine donnée, avec prompts, batch, contexte et version de runtime reproductibles. La release AutoRound améliore les possibilités ; elle ne garantit pas automatiquement un modèle deux fois plus rapide dans tous les cas.

## Pourquoi suivre AutoRound maintenant

Pour un usage local, AutoRound 0.13 coche plusieurs cases concrètes : meilleurs chemins pour modèles récents avec MTP, exports utiles pour **MLX** et **GGUF**, intégration vLLM plus propre, support multimodal via vLLM-Omni, et efforts côté CPU/XPU. Cela en fait une brique à surveiller pour ceux qui maintiennent des modèles quantifiés, des serveurs locaux ou des pipelines de conversion.

La recommandation pratique est simple : ne remplace pas aveuglément tes GGUF ou AWQ existants. Mais si tu travailles sur Qwen, DeepSeek, des VLM ou des modèles avec MTP, AutoRound mérite un test comparatif. Mesure la perplexité ou les tâches métier, puis le débit et la mémoire réelle sur ta machine. Si le gain est là, garde-le. Sinon, tu auras au moins gagné une conclusion, ce qui est déjà plus utile qu'un tweet triomphal.

AutoRound n'est pas une révolution visible côté utilisateur final. C'est mieux : c'est une amélioration d'infrastructure. Le genre de pièce qu'on oublie quand elle marche, et qu'on maudit quand elle manque.

## Sources

- Release AutoRound v0.13.0 : https://github.com/intel/auto-round/releases
- Dépôt Intel AutoRound : https://github.com/intel/auto-round
- Documentation vLLM AutoRound : https://docs.vllm.ai/en/v0.14.0/features/quantization/auto_round/
- Documentation vLLM-Omni AutoRound : https://docs.vllm.ai/projects/vllm-omni/en/latest/user_guide/quantization/autoround/
