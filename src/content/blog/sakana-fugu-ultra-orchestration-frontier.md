---
title: "Sakana Fugu : un seul endpoint, une orchestration multi-modèles frontier"
description: "Sakana AI lance Fugu et Fugu Ultra — un routeur appris qui délègue à un pool d'experts (API compatible OpenAI) pour rivaliser avec Opus 4.8 et GPT-5.5 sans mono-fournisseur."
pubDate: 2026-06-24
tags: ["Sakana AI", "orchestration", "multi-agents", "API", "souveraineté IA"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Sakana AI — Sakana Fugu release"
    url: "https://sakana.ai/fugu-release/"
  - label: "arXiv — Fugu technical report (2606.21228)"
    url: "https://arxiv.org/abs/2606.21228"
---

## Le signal

**22 juin 2026** : Sakana AI met en **GA** **Fugu** (latence basse, coding/review) et **Fugu Ultra** (tâches longues, recherche, cyber défensif). Un seul appel **compatible OpenAI** ; derrière, un **système multi-agents** basé sur la recherche **Trinity** et **Conductor** (ICLR 2026) qui choisit de répondre seul ou de **déléguer, vérifier et synthétiser** dans un pool de modèles — y compris des appels récursifs à Fugu lui-même.

## Pourquoi ce n'est pas « encore un routeur »

Le pitch géopolitique est explicite : après les **coupures d’accès** aux modèles Mythos/Fable d’Anthropic, une dépendance mono-vendeur devient un **risque opérationnel**. Fugu vend l’**interchangeabilité** des agents sous-jacents : restriction d’un fournisseur → le routeur s’adapte.

Techniquement, Sakana compare Fugu Ultra à **Gemini 3.1 Pro (high), Opus 4.8 (max), GPT-5.5 (xhigh)** sur des workflows ouverts (AutoResearch, design mécanique, cyber assessment scoping, etc.) — avec des retours bêta (~500 utilisateurs) du type « **20+ issues** trouvées en review vs ~3 » pour GPT-5.5 sur un même repo.

## Benchmarks (à lire avec prudence)

- Rapport technique : [PDF sur le dépôt GitHub SakanaAI/fugu](https://github.com/SakanaAI/fugu/blob/main/Fugu_technical_report.pdf).
- Les scores des modèles **non accessibles publiquement** (ex. Fable 5 / Mythos Preview) ne sont **pas** dans le pool Fugu ; les comparaisons utilisent les chiffres publiés par les éditeurs.

## Impact pour les builders

- **Plateformes internes** : pattern intéressant si vous avez déjà plusieurs clés API + modèles open-weight — Fugu industrialise l’orchestration apprise plutôt que des règles statiques.
- **Coût / latence** : Fugu standard cible le **quotidien dev** ; Ultra pour les jobs à budget compute plus élevé (pay-as-you-go + abonnements).
- **Compliance** : possibilité d’**exclure** certains agents du pool (données sensibles).

## Limites

Produit **propriétaire** hébergé (console Sakana) — ce n’est pas un poids open à déployer chez soi. Les claims benchmark + témoignages viennent surtout de Sakana et de la bêta ; à croiser avec vos propres harness (Claude Code, Codex, etc.) avant migration.