---
title: "Anthropic Fable 5 / Mythos 5 : accès « potentiellement restauré dans les jours à venir »"
description: "Cinq jours après la coupure imposée par le gouvernement américain, Anthropic signale une restauration imminente de ses modèles Mythos-class."
pubDate: 2026-06-18
tags: ["Anthropic", "Fable 5", "Mythos 5", "jailbreak", "export control", "régulation IA"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Korea JoongAng Daily — Anthropic confident of re-enabling access"
    url: "https://www.koreajoongangdaily.com/business/anthropic-confident-of-reenabling-mythos-fable-5-access-in-coming-days-executive/12727522"
  - label: "Anthropic — Statement on US government directive"
    url: "https://www.anthropic.com/news/fable-mythos-access"
  - label: "ExplainX.ai — Update June 17, no restoration date yet"
    url: "https://www.explainx.ai/blog/us-government-bans-fable-5-mythos-5-anthropic-export-control-2026"
  - label: "Forbes — US Gov ordered Anthropic to take down Fable 5 and Mythos 5"
    url: "https://www.forbes.com/sites/anishasircar/2026/06/16/anthropic-disabled-fable-5-and-mythos-5-after-a-us-export-control-order-heres-what-happened/"
---

## La nouvelle

Le 18 juin, la Korea JoongAng Daily rapporte qu'Anthropic a indiqué que l'accès à Claude Fable 5 et Mythos 5 pourrait être **restauré dans les jours à venir**. Cinq jours après la coupure mondiale imposée par une directive du département américain du Commerce, le ton d'Anthropic est plus optimiste — mais aucune date officielle n'a été confirmée.

## Le contexte technique

Rappel rapide de la chronologie :
- **9 juin** : Anthropic lance Fable 5 (Mythos-class, au-delà d'Opus) et Mythos 5 (sans garde-fous cyber).
- **12 juin, 17h21 ET** : Le département du Commerce envoie une directive de contrôle des exportations exigeant la suspension d'accès par tout ressortissant étranger. Anthropic coupe les deux modèles pour tous ses clients mondiaux.
- **12–16 juin** : Négociations entre ingénieurs Anthropic et le département du Commerce à Washington. Le PDG Dario Amodei est présent au G7 d'Évian, ajoutant une pression diplomatique.
- **18 juin** : Premier signal public qu'un accord pourrait être proche.

La cause officielle : un « jailbreak étroit » permettant de demander au modèle d'analyser et corriger des vulnérabilités dans une base de code spécifique — une capacité que les équipes de sécurité utilisent normalement en défense. Anthropic conteste que cela justifie une coupure mondiale et maintient sa stratégie de *defense in depth* : aucun garde-fou n'est parfait, donc on les couche.

## Ce qui change concrètement

Trois scénarios possibles pour la restauration, selon l'analyse d'ExplainX.ai :
1. **Accès complet restauré** — le plus improbable sans modification technique du modèle.
2. **Accès partiel avec restrictions géographiques** — plausible si un mécanisme de vérification d'identité est mis en place.
3. **Remplacement par Opus 4.8** — le fallback actuel, déjà disponible pour tous les clients.

Le marché de prédiction Manifold donne 19% de chance que Fable 5 revienne avec un accès universal d'ici fin juin.

## Impact pour l'écosystème local

Pour qui self-host ou utilise des modèles open-weight : cet épisode est une démonstration claire de la vulnérabilité des modèles cloud. Quand le gouvernement américain décide, il coupe — sans préavis, sans détail technique écrit, sans appel possible. Les équipes locales qui dépendent d'API tierces ont vu leurs pipelines casser du jour au lendemain.

Pour les runners locaux (Ollama, llama.cpp, LM Studio) : l'intérêt pour les modèles open-weight capables de remplacer Fable 5 en capacité pure s'accélère. La communauté r/LocalLLaMA a immédiatement pointé cet épisode comme argument central en faveur de l'inférence souveraine.

## À surveiller

- L'annonce officielle d'Anthropic (probablement sur anthropic.com/news)
- Si la restauration est conditionnelle à des restrictions géographiques ou techniques
- La réaction du département du Commerce et si ce précédent s'étend à d'autres modèles
