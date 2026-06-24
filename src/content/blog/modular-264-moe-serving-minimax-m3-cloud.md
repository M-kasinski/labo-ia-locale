---
title: "Modular 26.4 : serving MoE SOTA, agent skills pour le bring-up, et MiniMax M3 dès le jour J"
description: "Le 24 juin 2026, Modular annonce la 26.4 : MoE optimisé sur Modular Cloud, nouveaux modèles open-weight supportés, Mojo 1.0 beta 2 — avec MiniMax M3 en tête d’affiche."
pubDate: 2026-06-24
tags: ["Modular", "MoE", "MiniMax M3", "serving", "open-weight"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "Modular Blog — Modular 26.4"
    url: "https://www.modular.com/blog"
  - label: "Modular Blog — Day Zero: MiniMax M3 Open Weights on Modular Cloud"
    url: "https://www.modular.com/blog"
  - label: "Hugging Face — MiniMaxAI/MiniMax-M3"
    url: "https://huggingface.co/MiniMaxAI/MiniMax-M3"
---

## La nouvelle

**Modular** publie le **24 juin 2026** sa release **26.4**, présentée comme une étape majeure pour le **serving de modèles MoE** (mixture-of-experts) sur **Modular Cloud**, avec extension du support **MAX** aux derniers open-weights, progression vers **Mojo 1.0 Beta 2**, et une nouveauté organisationnelle : le **bring-up de modèles via agent skills** — en clair, accélérer l’intégration de nouvelles architectures avec de l’assistance agentique côté toolchain.

Dans le même mouvement éditorial, Modular met en avant un **Day Zero** pour **MiniMax M3** sur son cloud : les poids open-weight (~428B total, ~23B actifs, contexte jusqu’à 1M annoncé côté MiniMax) deviennent exploitables sur une stack optimisée MoE sans attendre des semaines de portage manuel.

## Analyse technique

### Pourquoi le MoE est le sujet, pas le marketing

Les MoE open-weight récents (GLM-5.x, MiniMax M3, Kimi K2.x, Nemotron 3) partagent un problème de prod : **peu d’experts actifs par token**, mais **énorme empreinte mémoire totale**. Un runtime générique qui traite le modèle comme un dense transformer laisse de la performance sur la table — surtout sur le **routing expert**, le **gather/scatter KV**, et le **batching hétérogène**.

Modular 26.4 revendique un chemin **SOTA pour le serving MoE** sur leur cloud. Sans micro-benchmark public dans le communiqué du 24 juin, l’argument tient surtout sur la **spécialisation stack** (MAX + Mojo) plutôt que sur un simple wrapper vLLM — à valider par des tests indépendants sur ton workload (agents longs vs chat court).

### MiniMax M3 : rappel des specs utiles

D’après la fiche **Hugging Face MiniMaxAI/MiniMax-M3** et la documentation MiniMax :

- Architecture **MoE sparse** avec **MiniMax Sparse Attention (MSA)** pour le long contexte ;
- Positionnement **agentic coding** (scores vendor sur SWE-bench Pro, Terminal-Bench, etc.) ;
- **Multimodalité native** (image/vidéo) dans le pitch produit ;
- Poids disponibles en **Safetensors** — la communauté locale peut quantifier / distiller, mais le serving cloud Modular vise ceux qui veulent **l’API performance sans ops GPU**.

Le billet « Day Zero » insiste sur des optimisations de type **KV outer gather Q** (formulation MiniMax) pour éviter de recharger les mêmes blocs KV quand plusieurs requêtes touchent les mêmes experts — pattern familier des implémentations MoE matures.

### Agent skills pour le bring-up

La 26.4 mentionne l’usage d’**agent skills** pour accélérer l’onboarding de nouveaux modèles dans MAX. Traduction pragmatique : Modular automatise une partie du travail ingrat (mapping ops, tests de shapes, scripts de conversion) avec des agents — réduction du délai entre « poids publiés sur HF » et « endpoint stable en prod ». Pour les équipes self-hosted, l’intérêt est indirect : ce qui est porté en cloud finit souvent par inspirer ou se retrouver dans les runtimes open (recettes, kernels).

## Impact pour l’écosystème local / self-hosting

1. **Référence MoE** : si Modular tient ses promesses, les équipes qui hésitent entre **vLLM 0.23**, **SGLang** et **MAX** ont un nouveau point de comparaison sur **MiniMax M3** et familles proches.
2. **Pression sur vLLM** : notre veille récente couvrait déjà vLLM 0.23 + GLM-5.2 ; la 26.4 rappelle que le marché du serving open-weight est **multi-acteurs**, pas un monopole Berkeley.
3. **Local vs cloud** : M3 reste **trop massif** pour la plupart des homelabs ; la nouvelle du 24 juin concerne surtout **qui sert l’open-weight à l’échelle**, pas qui le fait tourner sur un RTX 4090 seul.

## Limites honnêtes

- **Blog Modular sans tableau tokens/s** dans l’extrait consulté : exiger des benchmarks tiers (Artificial Analysis, tests maison) avant de migrer une prod.
- **MiniMax M3** : scores principalement **vendor-run** ; notre article du 1er juin 2026 le disait déjà — les poids HF ne remplacent pas des évals indépendantes.
- **Modular Cloud ≠ self-host gratuit** : la valeur immédiate est cloud ; le parallèle local dépend de ce que MAX publie en open et de ton matériel.

## Sources vérifiées

- [Modular Blog — annonce 26.4 (24 juin 2026)](https://www.modular.com/blog)
- [Hugging Face — MiniMaxAI/MiniMax-M3](https://huggingface.co/MiniMaxAI/MiniMax-M3)