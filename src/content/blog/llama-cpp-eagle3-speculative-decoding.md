---
title: "llama.cpp intègre EAGLE-3 : le speculative decoding qui accélère vraiment en local"
description: "Le PR #18039 a été fusionné le 12 juin : EAGLE-3 arrive dans llama.cpp avec des gains de 2 à 3×. Benchmarks, modèles supportés et limites."
pubDate: 2026-06-18
tags: ["llama.cpp", "EAGLE-3", "speculative decoding", "performance", "open-weight"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "PR #18039 — EAGLE3 speculative decoding support (GitHub)"
    url: "https://github.com/ggml-org/llama.cpp/pull/18039"
  - label: "Discussion #15902 — Support Eagle-3 en llama.cpp"
    url: "https://github.com/ggml-org/llama.cpp/discussions/15902"
  - label: "Issue #15305 — Feature request EAGLE3 draft models"
    url: "https://github.com/ggml-org/llama.cpp/issues/15305"
  - label: "Eagle-3 paper (arXiv)"
    url: "https://arxiv.org/pdf/2503.01840"
  - label: "Spec-bench Leaderboard"
    url: "https://github.com/hemingkx/Spec-Bench/blob/main/Leaderboard.md"
---

## La nouvelle

Le 12 juin 2026, le **PR #18039** a été fusionné dans llama.cpp : **EAGLE-3**, l'algorithme de speculative decoding le plus performant actuellement, est maintenant nativement supporté.

Pour ceux qui tournent des modèles en local, c'est l'une des améliorations de performance les plus concrètes de l'année. Pas de buzz, pas de promesse — des gains mesurés de **2 à 3×** sur des modèles denses, directement dans le binaire que tu utilises déjà.

## Qu'est-ce que le speculative decoding ?

En bref : au lieu de générer un token à la fois (autoregressive decoding classique), le speculative decoding utilise un **modèle draft léger** pour prédire plusieurs tokens d'avance, puis le modèle principal les vérifie en un seul passage avant. Si le draft a bien deviné, tu gagnes plusieurs tokens pour le prix d'un seul forward pass.

Trois approches existent aujourd'hui dans llama.cpp :

1. **n-gram cache** : lookup table basée sur les motifs répétés dans le contexte. Simple, efficace sur le code répétitif et les templates, mais limité.
2. **Draft model classique** (`--model-draft`) : un petit modèle séparé (ex : Llama 3.2 1B) génère les tokens draft. Fonctionne mais les gains sont modestes sur du matériel consumer.
3. **EAGLE-3** : le modèle draft ne prédit pas des tokens — il prédit les **hidden states** du modèle cible, ce qui donne un taux d'acceptation bien supérieur.

## Comment EAGLE-3 fonctionne

L'architecture est élégante dans sa simplicité :

1. **Feature extraction** : pendant le forward pass du modèle cible, on extrait les hidden states à trois niveaux — début, milieu et fin du réseau (`[2, num_layers // 2, num_layers - 3]`).
2. **Compression** : ces trois vecteurs sont concaténés et passés dans une couche FC qui les compresse (`hidden_dim * 3 → hidden_dim`).
3. **Draft generation** : un seul layer transformer + LM head génère `k` tokens draft de manière autoregressive.
4. **Vocabulary mapping** : un tenseur `d2t` (draft-to-target) mappe le vocabulaire du draft vers celui du modèle cible.
5. **Vérification parallèle** : le modèle cible vérifie tous les tokens draft en un seul forward pass. Acceptation ou rejet via Speculative Sampling.

Le résultat : le modèle draft est minuscule (quelques centaines de Mo à quelques Go) et réutilise les calculs déjà faits par le modèle principal. Pas de duplication de VRAM, pas de second modèle lourd à charger.

## Benchmarks officiels (PR #18039)

Les chiffres viennent directement du PR, testés sur une **RTX A6000 / DGX Spark** :

| Modèle & Quantisation | Baseline (t/s) | EAGLE-3 (t/s) | Taux d'acceptation | Gain |
|---|---|---|---|---|
| LLaMA3.1-8B (BF16) | 44.5 | 146.2 | 80,6% | **3,28×** |
| LLaMA3.1-8B (Q4_K_M) | 121,5 | 274,4 | 92,5% | **2,26×** |
| LLaMA3.3-70B (Q4_K_M) | 15,6 | 37,6 | 82,0% | **2,41×** |
| Qwen3-8B (BF16) | 43,6 | 94,8 | 69,8% | **2,17×** |
| Qwen3-32B (Q4_K_M) | 32,0 | 41,5 | 43,3% | **1,30×** |
| GPT-OSS-20B (BF16) | 61,3 | 65,05 | 74,25% | **1,06×** |
| GPT-OSS-120B (BF16) | 48,3 | 52,2 | 85,0% | **1,08×** |

Quelques observations :

- **Les modèles denses gagnent le plus** : LLaMA3.1-8B passe de 44 à 146 t/s en BF16. C'est le gain le plus spectaculaire.
- **La quantisation ne tue pas le gain** : même en Q4_K_M, le 8B reste à 2,26×.
- **Les MoE souffrent** : GPT-OSS-20B et 120B montrent des gains marginaux (1,06× et 1,08×). La raison est technique : la vérification parallèle active plus d'experts qu'un token seul, ce qui annule le gain. C'est un problème connu de l'inférence MoE avec speculative decoding.
- **Les grands modèles denses en Q4 restent intéressants** : LLaMA3.3-70B fait 2,41×, ce qui transforme un modèle quasi inutilisable en local (15 t/s) en quelque chose de fluide (37 t/s).

## Modèles supportés

Le PR couvre déjà une bonne partie de l'écosystème :

| Famille | Modèles draft EAGLE-3 disponibles |
|---|---|
| **Gemma 4** | RedHatAI/gemma-4-31B-it-speculator.eagle3, RedHatAI/gemma-4-26B-A4B-it-speculator.eagle3 |
| **LLaMA** | yuhuili/EAGLE3-LLaMA3.1-Instruct-8B, yuhuili/EAGLE3-LLaMA3.3-Instruct-70B |
| **Qwen3** | Tengyunw/qwen3_8b_eagle3, AngelSlim/Qwen3-8B/14B/32B_eagle3, RedHatAI/Qwen3-30B-A3B |
| **GPT-OSS** | lmsys/EAGLE3-gpt-oss-120b-bf16, nvidia/gpt-oss-120b-Eagle3-long-context |
| **Autres** | Kimi-K2.6-Eagle3, Baichuan-M3-235B |

RedHat et NVIDIA ont été particulièrement actifs dans la publication de checkpoints EAGLE-3, ce qui est un bon signal pour l'écosystème.

## Comment l'utiliser

En pratique, c'est simple si tu as déjà llama.cpp :

```bash
# 1. Compiler la dernière version (main inclut maintenant le PR)
cmake -B build -DGGML_CUDA=ON && cmake --build build --config Release

# 2. Convertir le modèle cible et le draft EAGLE-3 en GGUF
python convert_hf_to_gguf.py "Qwen3-8B" --outtype bf16 --outfile "Qwen3-8B.gguf"
python convert_hf_to_gguf.py "qwen3_8b_eagle3" --outtype f16 \
  --target-model-dir "Qwen3-8B" --outfile "qwen3_8b_eagle3.gguf"

# 3. Lancer avec EAGLE-3
./build/bin/llama-server \
  -m Qwen3-8B.gguf \
  -md qwen3_8b_eagle3.gguf \
  --spec-type draft-eagle3 \
  --spec-draft-n-max 8 \
  --spec-draft-p-min 0.5 \
  -np 1 -c 4096 --port 8080 -ngl 99 -fa on
```

Le flag `--spec-type draft-eagle3` active le mode EAGLE-3. `--spec-draft-n-max` contrôle le nombre de tokens draft (8 par défaut). `--spec-draft-p-min` est le seuil d'acceptation minimum.

## Les limites à connaître

EAGLE-3 n'est pas une baguette magique :

1. **MoE = gains réduits** : comme montré dans les benchmarks, les modèles MoE (GPT-OSS, Qwen3-30B-A3B) ne profitent que marginalement. Le goulot est `mul_mat_id` pour les petits batchs `(1, 8]` pendant la vérification MoE. Un PR #22105 pour DFlash (variante similaire) est en cours et devrait aider.

2. **Le modèle draft est spécifique au modèle cible** : chaque modèle a besoin de son propre checkpoint EAGLE-3 entraîné. Si personne n'a encore publié de draft pour ton modèle préféré, tu ne peux pas utiliser EAGLE-3 dessus.

3. **L'architecture EAGLE-3 actuelle cible les décodeurs LLaMA** : tous les checkpoints connus utilisent l'architecture LLaMA, même pour des modèles comme Gemma ou Qwen. Le PR gère ce cas, mais une refactoring API model-agnostic est en discussion (#18039 comment section) pour supporter d'autres architectures futures.

4. **Les prompts avec raisonnement (reasoning models) voient des gains moindres** : avec le reasoning activé, les gains tombent à ~2× au lieu de 3×. Le reasoning produit des sorties moins prédictibles, ce qui réduit le taux d'acceptation du draft.

## Verdict

EAGLE-3 dans llama.cpp est une vraie avancée, pas un gadget. Pour les modèles denses de taille raisonnable (8B-32B), les gains sont réels et mesurables. Pour les MoE, c'est moins enthousiasmant — pour l'instant.

Si tu tournes un LLaMA 3.1/3.3, un Gemma 4 dense ou un Qwen3 dense en local, c'est le moment de tester. Le gain de 2-3× sur du decode, c'est la différence entre un modèle supportable et un modèle fluide.
