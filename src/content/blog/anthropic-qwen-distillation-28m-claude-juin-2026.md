---
title: "Anthropic accuse Alibaba Qwen : 28,8 M d’échanges Claude — la distillation devient un dossier politique"
description: "Lettre au Congrès rendue publique le 24 juin 2026 : ~25 000 comptes frauduleux, campagne avril–juin, cible Mythos Preview. Ce que ça change pour l’open-weight et l’inférence locale."
pubDate: 2026-06-27
tags: ["Anthropic", "Alibaba", "Qwen", "distillation", "sécurité", "open-weight", "régulation"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Reuters — Anthropic letter on Alibaba distillation (24 juin 2026)"
    url: "https://www.reuters.com/world/china/anthropic-says-alibaba-illicitly-extracted-claude-ai-model-capabilities-2026-06-24/"
  - label: "Anthropic — Detecting and preventing distillation attacks (fév. 2026)"
    url: "https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks"
  - label: "Forbes — Distillation: The New U.S.–China AI Fight (25 juin 2026)"
    url: "https://www.forbes.com/sites/craigsmith/2026/06/25/distillation-the-new-uschina-ai-fight/"
---

## Le signal

Le **24 juin 2026**, **Reuters** publie le contenu d’une **lettre d’Anthropic** adressée au Congrès américain : l’entreprise accuse des opérateurs **affiliés à Alibaba et au lab Qwen** d’avoir mené la **plus grande campagne de distillation** connue contre **Claude** à ce jour. Chiffres cités : **~25 000 comptes frauduleux**, **plus de 28,8 millions d’échanges** avec Claude entre le **22 avril et le 5 juin 2026**, avec un focus sur les capacités **logiciel / agentiques** associées à **Mythos Preview**.

Ce n’est pas un communiqué Twitter. C’est un acte de **diplomatie industrielle** qui tombe la même semaine que le retrait de **Claude Fable 5 / Mythos 5** pour raisons de sécurité nationale et que la montée en puissance de **GLM-5.2** en open-weight MIT.

## Analyse technique

### Qu’est-ce que la distillation « adversariale » ici ?

La **distillation** classique en ML : un petit modèle apprend à imiter un grand via les sorties du professeur. En contexte commercial API, le problème devient **extraction** : un acteur crée des milliers de comptes, envoie des prompts ciblés, collecte les réponses de Claude, et **réentraîne** (ou affine) un modèle concurrent — en contournant le coût d’entraînement frontier.

Anthropic avait déjà documenté en **février 2026** des campagnes attribuées à **DeepSeek, Moonshot et MiniMax** (ordre de grandeur : **>16 millions** d’échanges cumulés, **~24 000** comptes). La campagne Alibaba/Qwen décrite en juin **dépasse seule** cette échelle agrégée, selon la société.

### Pourquoi Mythos Preview ?

Mythos Preview était la vitrine **raisonnement + coding agentique** d’Anthropic avant la bascule politique sur Fable/Mythos. Une distillation réussie sur ce tier vise directement :

- chaînes d’outils longues ;
- qualité de code et debug ;
- comportements « SWE-agent » mesurables sur benchmarks publics.

Pour **Qwen**, aligner ces compétences via extraction API serait un raccourci massif par rapport à un post-training from scratch — **si** les données collectées sont suffisamment diverses et filtrées. Anthropic ne publie pas de preuves techniques reproductibles dans la lettre (pas de hashes de datasets, pas d’évals A/B publiques) : on est sur des **affirmations de détection interne** + communication législative.

### Chronologie qui se recoupe

| Date | Événement |
|------|-----------|
| 22 avr. – 5 juin 2026 | Fenêtre de la campagne selon Anthropic |
| 9 juin 2026 | Lancement puis retrait **Fable 5 / Mythos 5** (Commerce Dept.) |
| 10 juin 2026 | Lettre Anthropic au Sénat (rendue publique le 24) |
| 13–16 juin 2026 | **GLM-5.2** open-weight MIT, comparaisons frontier |
| 26 juin 2026 | Preview **GPT-5.6 Sol** sous accès gouverné |

La distillation n’est pas la cause unique des restrictions gouvernementales, mais elle alimente le récit : **les capacités frontier fuient par l’API** pendant que les modèles les plus puissants sont retirés du marché ouvert.

## Impact pour l’écosystème — y compris local

### 1. Pression sur les API comme « professeurs »

Les équipes qui fine-tunent localement avec des **sorties Claude/GPT** (synthetic data) doivent relire leurs contrats ToS. La frontière entre **recherche légitime** et **extraction industrielle** se durcit. Pour le Labo **local**, la piste saine reste :

- datasets open (Apache/CC) ;
- auto-génération avec modèles **open-weight** sur ton propre GPU ;
- distillation **intra-maison** (professeur = GLM-5.2 local, élève = 7B quantifié).

### 2. Renforcement des modèles open-weight chinois

Ironie timing : pendant qu’Anthropic accuse Qwen, **GLM-5.2** (Zhipu) occupe le haut du **Artificial Analysis Intelligence Index** open-weight. Les marchés actions ont réagi (Knowledge Atlas +30 % à Hong Kong après l’ouverture MIT des poids, selon la presse économique). Pour un lecteur Labo : **le gap open vs fermé se resserre** sur le coding — indépendamment de la validité juridique des accusations.

### 3. Défenses côté fournisseurs fermés

Anthropic liste des leviers : détection de comptes, rate limits, empreintes de prompts, sanctions légales. Conséquence produit probable : **API plus chères**, **KYC renforcé** pour les tiers tiers, et **moins de previews** exposées (déjà visible avec Mythos).

### 4. Ce que ça ne change pas demain matin

- Télécharger **Qwen3.6** ou **GLM-5.2** sur Hugging Face reste légal sous leurs licences respectives.
- **llama.cpp / vLLM / Ollama** ne sont pas dans le viseur de cette affaire.
- Aucune mesure technique automatique n’empêche un particulier de fine-tuner un GGUF chez lui — le conflit est **B2B / géopolitique**, pas anti-self-hosting.

## Limites et lecture critique

- **Preuve publique limitée** : la lettre est rapportée par Reuters ; Alibaba n’a pas (à notre lecture des sources du 27 juin) publié une réfutation détaillée point par point dans les mêmes termes techniques.
- **Chiffres non audités** par un tiers : 28,8 M exchanges = métrique interne Anthropic.
- **Risque de narratif** : lier distillation et retrait Fable peut masquer d’autres motivations (cyber dual-use, jailbreaks publics).
- **Distillation ≠ copie bit-à-bit** : un modèle open-weight « proche » de Claude sur un benchmark peut aussi venir de **convergence d’architecture + data web commune**, sans extraction prouvée.

## Pistes pour les lecteurs du Labo

1. **Documenter la provenance** de tes jeux de fine-tuning (surtout si tu publies un LoRA/GGUF).
2. **Ne pas baser** ta stack locale sur une clé API frontier comme seule source de vérité — coût et disponibilité deviennent politiques.
3. **Tester GLM-5.2 / Qwen3.6** sur *tes* tâches : les leaderboard ne remplacent pas un bench interne.
4. Suivre les évolutions **export control** US : elles affectent déjà **GPT-5.6** et pourraient un jour toucher l’**hébergement** de modèles chinois sur cloud américain (hors téléchargement de poids).

## Sources vérifiées

- [Reuters — Anthropic says Alibaba illicitly extracted Claude capabilities (24 juin 2026)](https://www.reuters.com/world/china/anthropic-says-alibaba-illicitly-extracted-claude-ai-model-capabilities-2026-06-24/)
- [Anthropic — Detecting and preventing distillation attacks (23 fév. 2026)](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks)
- [Forbes — Distillation: The New U.S.–China AI Fight (25 juin 2026)](https://www.forbes.com/sites/craigsmith/2026/06/25/distillation-the-new-uschina-ai-fight/)
- [Fortune — U.S. Anthropic ban and open-source AI context (16 juin 2026)](https://fortune.com/2026/06/16/us-anthropic-ban-open-source-ai-deepseek-zai/)