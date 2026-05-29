---
title: "Faire tourner un LLM sur Mac Apple Silicon : MLX, llama.cpp et Ollama"
description: "Guide pratique pour lancer un LLM local sur Mac Apple Silicon avec MLX, llama.cpp et Ollama, selon ta RAM et ton usage."
pubDate: 2026-05-29
tags: ["ia-locale", "apple-silicon", "mlx", "ollama"]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "Apple Developer WWDC20 — unified memory", url: "https://developer.apple.com/videos/play/wwdc2020/10686/" }
  - { label: "MLX README", url: "https://github.com/ml-explore/mlx" }
  - { label: "mlx-lm README", url: "https://github.com/ml-explore/mlx-lm" }
  - { label: "llama.cpp install docs", url: "https://github.com/ggerganov/llama.cpp/blob/master/docs/install.md" }
  - { label: "Ollama v0.19.0 release", url: "https://github.com/ollama/ollama/releases/tag/v0.19.0" }
  - { label: "LM Studio system requirements", url: "https://lmstudio.ai/docs/app/system-requirements" }
  - { label: "Hugging Face MLX docs", url: "https://huggingface.co/docs/hub/en/mlx" }
  - { label: "mlx-community sur Hugging Face", url: "https://huggingface.co/mlx-community" }
---

Tu viens de récupérer un MacBook Apple Silicon et tu veux tester un LLM ce soir, pas lire une thèse. Bonne nouvelle : sur Mac, il y a un vrai avantage matériel. La mémoire unifiée change la donne.

Sur un PC classique avec GPU dédié, le modèle vit souvent dans la VRAM, séparée de la RAM système. Sur Apple Silicon, CPU et GPU partagent la même mémoire, sans copie aller-retour permanente. Apple le dit clairement dans sa présentation WWDC20 : le CPU et le GPU travaillent sur la même mémoire, ce qui supprime une partie du coût de transfert. MLX reprend cette idée au niveau framework : les tableaux vivent en mémoire partagée, et les opérations peuvent s’exécuter sur CPU ou GPU sans copie de données.

Le résultat est simple à comprendre : un modèle quantisé peut tenir plus facilement en mémoire, et le GPU y accède directement. Ça ne rend pas les gros modèles gratuits. Ça évite juste une partie du cirque habituel.

## Les trois voies qui comptent vraiment

Si tu veux faire tourner un LLM local sur Mac Apple Silicon, il y a trois chemins utiles.

| Voie | Pour qui | Format de modèle | Point fort | Limite |
|---|---|---|---|---|
| MLX + mlx-lm | Ceux qui veulent la voie la plus native Apple | MLX, souvent via `mlx-community` | Très cohérent avec Apple Silicon, conversion et fine-tuning simples | Écosystème plus jeune que GGUF |
| llama.cpp + Metal | Ceux qui veulent du contrôle et du portable | GGUF | Ultra mature, cross-platform, énorme écosystème | Plus bricolage, moins “Mac natif” |
| Ollama / LM Studio | Ceux qui veulent tester vite avec une UX propre | GGUF, et MLX sur Apple Silicon selon l’outil | Installation facile, catalogue de modèles, API ou GUI | Une couche de plus, donc une couche de problèmes de plus |

## 1. MLX : la voie Apple, sans détour

MLX est le framework d’Apple Machine Learning Research pour Apple Silicon. Le README du projet insiste sur deux choses : les opérations tournent sur CPU ou GPU, et les tableaux partagent la même mémoire. C’est exactement le genre de base qui colle bien aux Mac M-series.

Pour les LLM, le compagnon logique s’appelle `mlx-lm`. C’est le package Python pour générer du texte, faire du fine-tuning, convertir des modèles et les pousser vers Hugging Face.

Installation :

```bash
pip install mlx-lm
```

Lancer un modèle depuis Hugging Face :

```bash
python -m mlx_lm.generate --model mlx-community/Qwen3-4B-Instruct-2507-4bit --prompt "Explique la mémoire unifiée sur Mac."
```

Passer en mode chat :

```bash
python -m mlx_lm.chat
```

Convertir un modèle Hugging Face en MLX quantisé :

```bash
python -m mlx_lm.convert --hf-path mistralai/Mistral-7B-v0.1 -q
```

Le bon réflexe, c’est de regarder `mlx-community` sur Hugging Face. L’organisation décrit elle-même ses poids comme des modèles MLX prêts à l’emploi pour Apple Silicon. En clair : tu n’es pas obligé de convertir toi-même pour essayer un modèle ce soir.

Avantages :
- très bon alignement avec Apple Silicon
- moins de friction si tu travailles en Python
- conversion et fine-tuning intégrés
- source de modèles prête à l’emploi via `mlx-community`

Limites :
- moins universel que GGUF
- certaines références ou scripts changent vite
- le confort dépend du modèle déjà converti

## 2. llama.cpp : la voie robuste, en Metal

`llama.cpp` reste le couteau suisse local. Son objectif affiché est clair : faire tourner des LLM avec un minimum de dépendances, sur un grand nombre de machines. Sur Mac, il s’appuie sur Metal pour accélérer l’exécution sur GPU Apple.

Installation simple sur Mac :

```bash
brew install llama.cpp
```

Lancer un modèle directement depuis Hugging Face :

```bash
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF
```

Ou avec un fichier local GGUF :

```bash
llama-cli -m ./models/mon-modele.gguf
```

Si tu veux exposer une API locale :

```bash
llama-server -hf ggml-org/gemma-3-1b-it-GGUF
```

Pourquoi le choisir ? Parce qu’il est partout, qu’il supporte une foule de quantizations, et qu’il sert de base à plein d’outils grand public. Si tu veux tester des modèles GGUF, profiler, bidouiller les paramètres, ou garder la main sur le runtime, c’est un très bon point d’entrée.

Ce qu’il faut accepter :
- la configuration demande parfois un peu plus de doigté
- l’expérience n’est pas aussi “belle” qu’une app grand public
- tu dois penser en GGUF, backends et quantization

## 3. Ollama et LM Studio : la couche confortable

Ollama et LM Studio ne sont pas des moteurs magiques. Ce sont des couches de confort au-dessus de runtimes locaux.

Ollama a longtemps été associé à `llama.cpp`, puis la branche Apple Silicon a évolué. Dans la release v0.19.0, l’équipe annonce un support MLX en preview sur Apple Silicon, pour profiter de la mémoire unifiée. Son avantage principal reste le même : zéro prise de tête pour démarrer, CLI et API locales, et une énorme facilité d’intégration avec d’autres outils.

Installation Ollama :

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Lancer un modèle :

```bash
ollama run gemma3
```

LM Studio joue la carte GUI. Les docs officielles disent qu’il supporte Apple Silicon, qu’il peut aussi utiliser MLX sur Mac, qu’il fonctionne offline, et qu’il recommande au moins 16 Go de RAM, avec 8 Go seulement pour des modèles plus petits et des contextes modestes. Les mêmes docs précisent aussi que les Mac Intel ne sont pas supportés.

Si tu veux juste télécharger, cliquer, discuter, c’est probablement l’option la plus simple. Si tu veux automatiser, Ollama ou `llama.cpp` seront plus pratiques.

## Ce que ta RAM autorise vraiment

Ici, il faut être honnête : la taille du modèle n’est pas le seul facteur. Le contexte, le runtime et la quantization changent le résultat. Mais pour ne pas te vendre du vent, voilà des repères réalistes.

| RAM unifiée | Repère utile | Commentaire |
|---|---|---|
| 16 Go | modèles 3B à 8B en 4-bit | c’est le terrain de jeu raisonnable pour commencer |
| 32 Go | 7B/8B confortables, 13B possibles selon quantization | le vrai sweet spot pour un Mac portable |
| 48 Go | 13B confortables, 20B envisageables | plus de marge pour le contexte et l’outil |
| 64 Go et plus | 20B à 30B deviennent sérieux, certains 70B quantisés restent tentants | ce n’est pas une machine miracle, mais on commence à jouer dans la cour des grands |

Le piège classique, c’est de regarder seulement les paramètres du modèle. Le cache de contexte prend aussi de la place. Plus tu allonges l’historique, plus tu manges de mémoire. Donc oui, un 13B peut “passer” sur 16 Go dans certains cas. Non, ça ne veut pas dire que c’est agréable.

## Quel outil pour quel usage ?

- Si tu veux la voie la plus cohérente avec Apple Silicon, pars sur MLX + `mlx-lm`.
- Si tu veux le runtime le plus polyvalent et le plus documenté, pars sur `llama.cpp`.
- Si tu veux tester en dix minutes avec une interface propre, prends Ollama ou LM Studio.

Et si tu veux mon avis sans diplomatie : sur un Mac Apple Silicon neuf, le meilleur “premier test” ce soir, c’est un modèle 7B ou 8B quantisé, via Ollama ou LM Studio si tu veux aller vite, ou via MLX si tu veux rester au plus près de l’écosystème Apple.

## En pratique

Si tu as 16 Go, commence avec un 7B/8B quantisé et garde le contexte court. Si tu as 32 Go, tu peux viser plus sereinement un 13B. Si tu as 48 Go ou 64 Go, tu peux t’amuser avec des modèles plus ambitieux, mais il faudra quand même surveiller la quantization et la taille du contexte.

Ma recommandation simple :
- pour découvrir ce soir : Ollama ou LM Studio
- pour travailler proprement en Python sur Mac : MLX + `mlx-lm`
- pour bricoler sérieusement et rester portable : `llama.cpp`

Le Mac a un vrai avantage ici. Pas parce qu’il “fait de l’IA” par magie. Parce que sa mémoire unifiée enlève une bonne partie de la plomberie entre le modèle et le GPU. Et sur un LLM local, ça compte. Beaucoup.
