---
title: "Quantization des LLM en local : GGUF, GPTQ, AWQ, MLX — comprendre et choisir"
description: "Comprendre GGUF, GPTQ, AWQ et MLX pour faire tourner un LLM local sur Mac Apple Silicon ou GPU grand public, sans exploser la mémoire."
pubDate: 2026-05-29
tags: ["ia-locale", "quantization", "gguf", "llama-cpp"]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "Hugging Face — GGUF", url: "https://huggingface.co/docs/hub/gguf" }
  - { label: "Hugging Face — GGUF avec llama.cpp", url: "https://huggingface.co/docs/hub/gguf-llamacpp" }
  - { label: "llama.cpp — quantize README", url: "https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/README.md" }
  - { label: "vLLM — quantization", url: "https://docs.vllm.ai/en/latest/features/quantization/" }
  - { label: "Hugging Face Transformers — GPTQ", url: "https://huggingface.co/docs/transformers/main/en/quantization/gptq" }
  - { label: "MIT Han Lab — AWQ", url: "https://github.com/mit-han-lab/llm-awq" }
  - { label: "MLX — nn.quantize", url: "https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.nn.quantize.html" }
  - { label: "MLX-LM", url: "https://github.com/ml-explore/mlx-lm" }
  - { label: "HF API — Llama-2-7B-Chat-GGUF tree", url: "https://huggingface.co/api/models/TheBloke/Llama-2-7B-Chat-GGUF/tree/main?recursive=true" }
  - { label: "HF API — Llama-2-70B-Chat-GGUF tree", url: "https://huggingface.co/api/models/TheBloke/Llama-2-70B-Chat-GGUF/tree/main?recursive=true" }
---

Faire tourner un LLM chez soi, ce n’est pas seulement choisir “le meilleur modèle”. C’est surtout faire entrer ses poids, son cache de contexte et son runtime dans la RAM ou la VRAM disponible. La quantization est le levier principal : on réduit la précision numérique des poids, typiquement de FP16 vers INT8, INT4 ou des formats mixtes. On perd parfois un peu de qualité, mais on divise la taille du modèle. Sans ça, un 7B reste confortable ; un 70B devient vite une brique de 140 Go en FP16, fort élégante mais peu causante sur un PC normal.

## Ce que fait vraiment la quantization

Un modèle FP16 stocke chaque poids sur 16 bits. En 8-bit, on vise environ moitié moins ; en 4-bit, environ quatre fois moins, plus les métadonnées de groupes, les échelles et parfois les biais. Les méthodes modernes ne se contentent pas de “couper les décimales” : elles quantifient par blocs, gardent certains tenseurs plus précis, ou utilisent un jeu de calibration pour préserver les poids importants.

Point crucial : la taille du fichier n’est pas toute la mémoire nécessaire. Il faut ajouter le runtime, les buffers, et surtout le KV cache, qui grossit avec la longueur de contexte, le batch et le nombre de couches. Une règle saine : garder plusieurs Go de marge, davantage sur 70B.

## GGUF : le choix local par défaut

GGUF est le format de fichier utilisé par llama.cpp et l’écosystème GGML. Hugging Face le décrit comme un format binaire optimisé pour le chargement/sauvegarde rapide et contenant à la fois les tenseurs et des métadonnées. C’est le format le plus simple pour un usage local : llama.cpp, Ollama, LM Studio, GPT4All et d’autres savent le lire.

Sur Mac Apple Silicon, llama.cpp exploite Metal. Sur PC, il peut tourner en CPU pur, CUDA, HIP/ROCm, Vulkan, SYCL selon le build. Il accepte aussi l’offload partiel : si la VRAM manque, une partie du modèle reste en RAM système. Ce n’est pas magique, mais ça sauve des configurations bancales.

Exemple direct depuis Hugging Face :

```bash
brew install llama.cpp
llama-server -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0
```

Ou avec un fichier local :

```bash
llama-cli -m ./mistral-7b-instruct.Q4_K_M.gguf -p "Explique la quantization en 5 lignes"
```

Pour convertir puis quantifier soi-même :

```bash
python3 convert_hf_to_gguf.py ./models/mon-modele --outtype f16
./llama-quantize ./models/mon-modele/ggml-model-f16.gguf \
  ./models/mon-modele/ggml-model-Q4_K_M.gguf Q4_K_M
```

## Lire les niveaux GGUF : Q4_K_M, Q5_K_M, Q8_0

Les suffixes GGUF sont moins ésotériques qu’ils n’en ont l’air. `Q4` signifie quantization autour de 4 bits. `K` désigne les k-quants, une famille plus récente avec super-blocs et précision mixte. `_S`, `_M`, `_L` indiquent en gros small, medium, large : plus c’est haut, plus c’est lourd et généralement meilleur.

Repères simples :

- `Q4_K_M` : le point de départ raisonnable. Bon compromis qualité/taille/vitesse.
- `Q5_K_M` : meilleure qualité, utile pour code, raisonnement, rédaction technique, si la mémoire suit.
- `Q6_K` : confortable mais plus lourd ; intéressant sur 7B/13B avec marge.
- `Q8_0` : proche FP16 côté comportement, mais coûteux ; rarement nécessaire pour du chat courant.
- `Q3_K_M` et dessous : à réserver quand “ça doit rentrer” prime sur la qualité.

D’après les fichiers GGUF Llama-2-7B-Chat publiés sur Hugging Face, `Q4_K_M` pèse 4,08 Go, `Q5_K_M` 4,78 Go et `Q8_0` 7,16 Go. Pour Llama-2-70B-Chat, `Q4_K_M` monte à 41,42 Go, `Q5_K_M` à 48,75 Go, `Q6_K` à 56,59 Go et `Q8_0` à 73,29 Go. En pratique, prévois plus que ça en mémoire disponible à cause du KV cache.

## GPTQ : efficace pour GPU, moins universel

GPTQ est une méthode de post-training quantization : on quantifie les poids après entraînement, souvent en 4-bit, avec calibration. La documentation Transformers indique que GPTQ quantifie les poids ligne par ligne pour réduire la mémoire et accélérer l’inférence ; AutoGPTQ est désormais délaissé côté Transformers au profit de GPTQModel.

GPTQ est surtout pertinent si tu sers des modèles avec Transformers, vLLM, ExLlamaV2 ou un stack GPU NVIDIA. vLLM supporte GPTQ et GPTQModel, avec des kernels comme Marlin ou Machete selon le matériel. C’est moins plug-and-play que GGUF pour une machine familiale, mais très correct pour une carte NVIDIA et du débit.

```bash
pip install -U gptqmodel --no-build-isolation -v
vllm serve ModelCloud/DeepSeek-R1-Distill-Qwen-7B-gptqmodel-4bit-vortex-v2
```

Compromis : très bon usage VRAM, bonnes performances GPU, mais compatibilité plus dépendante du modèle, du kernel et de la version des bibliothèques. Sur Mac, ce n’est pas mon premier choix.

## AWQ : 4-bit orienté activations

AWQ signifie Activation-aware Weight Quantization. L’idée : protéger les poids les plus importants, détectés via les activations, pour obtenir une quantization INT3/INT4 plus stable. Le dépôt MIT Han Lab indique du W4A16 : poids 4-bit, activations 16-bit. vLLM sait charger des modèles AWQ ; AutoAWQ existe encore dans beaucoup de tutos, mais sa documentation vLLM signale qu’il est déprécié au profit des workflows llm-compressor.

```bash
vllm serve TheBloke/Llama-2-7b-Chat-AWQ --quantization awq
```

AWQ est intéressant pour serveur GPU, surtout si tu veux maximiser le débit avec des modèles déjà quantifiés. Pour un usage local individuel, GGUF reste plus tolérant ; pour une API maison sur RTX, AWQ/GPTQ méritent le test.

## MLX : la voie propre sur Apple Silicon

MLX est le framework Apple pour Apple Silicon. `mlx-lm` permet de générer, fine-tuner, convertir et quantifier des LLM. La doc MLX expose `mlx.nn.quantize`, qui quantifie en place les couches compatibles, notamment `Linear` et `Embedding`. `mlx.core.quantize` supporte notamment le mode affine en 2, 3, 4, 5, 6 et 8 bits, ainsi que `mxfp4`, `mxfp8` et `nvfp4`.

```bash
pip install mlx-lm
mlx_lm.generate --model mlx-community/Mistral-7B-Instruct-v0.3-4bit \
  --prompt "Donne-moi trois règles pour choisir une quantization"
```

Pour convertir un modèle Hugging Face en MLX quantifié :

```bash
mlx_lm.convert --model mistralai/Mistral-7B-Instruct-v0.3 -q
```

Si tu as un Mac M1/M2/M3/M4 avec mémoire unifiée, MLX est souvent plus naturel que bricoler CUDA absent. GGUF via llama.cpp reste excellent et plus portable ; MLX est plus intégré au monde Apple.

## Tableau comparatif

| Méthode / format | Runtime typique | Matériel naturel | Points forts | Limites |
|---|---|---|---|---|
| GGUF | llama.cpp, Ollama, LM Studio, vLLM expérimental | CPU, Apple Metal, NVIDIA, AMD, mix CPU/GPU | Simple, portable, énorme choix de modèles | KV cache à prévoir ; vLLM GGUF encore expérimental |
| GPTQ | Transformers, GPTQModel, vLLM, ExLlamaV2 | GPU NVIDIA surtout | Très bon ratio VRAM/perf en 4-bit | Compatibilité kernel/version plus fragile |
| AWQ | vLLM, llm-compressor, anciens modèles AutoAWQ | GPU NVIDIA, certains CPU/Intel selon stack | W4A16 efficace, bon pour serving | AutoAWQ déprécié ; moins universel localement |
| MLX | mlx-lm, MLX | Mac Apple Silicon | Intégré à la mémoire unifiée Apple, CLI simple | Écosystème surtout Apple ; modèles convertis nécessaires |

## Choisir selon ta RAM/VRAM

Sur un 7B :

- 8 Go de RAM/VRAM : `Q4_K_M`, contexte modéré.
- 12 à 16 Go : `Q5_K_M` ou `Q6_K` selon usage.
- 24 Go : 13B en `Q4_K_M` devient réaliste ; 7B en `Q8_0` sans stress.

Sur un 70B :

- 48 Go unifiés ou VRAM cumulée : `Q4_K_M` peut rentrer, mais le contexte long sera serré.
- 64 Go : `Q4_K_M` confortable, `Q5_K_M` possible avec prudence.
- 96 Go et plus : `Q5_K_M`, `Q6_K` ou contexte plus long deviennent agréables.

Attention aux GPU grand public : deux cartes avec 24 Go ne donnent pas automatiquement 48 Go utilisables dans tous les runtimes. Le tensor parallel marche dans certains stacks, l’offload dans d’autres. Lis la doc du runtime, pas la fiche marketing de la carte.

## En pratique

Si tu débutes ou veux juste un assistant local fiable : prends un modèle instruct récent en GGUF `Q4_K_M`, lance-le avec llama.cpp ou Ollama, et augmente vers `Q5_K_M` si tu as de la marge. Sur Mac Apple Silicon, teste aussi `mlx-lm` avec un modèle `mlx-community/*-4bit` : c’est souvent très propre. Sur PC avec NVIDIA et ambition de servir une API rapide, compare GGUF/llama.cpp avec GPTQ ou AWQ dans vLLM sur ton vrai workload. La bonne quantization n’est pas celle qui gagne un benchmark isolé ; c’est celle qui rentre en mémoire, répond vite, et ne massacre pas tes tâches réelles.
