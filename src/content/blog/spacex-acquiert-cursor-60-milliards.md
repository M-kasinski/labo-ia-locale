---
title: "SpaceX acquiert Cursor pour 60 milliards $ — l'IDE IA dans l'empire Musk"
description: "Quatre jours après son IPO historique, SpaceX signe le rachat d'Anysphere (Cursor) en actions pures. Impact majeur sur l'écosystème du coding assistant."
pubDate: 2026-06-18
tags: ["SpaceX", "Cursor", "xAI", "Grok", "AI coding", "acquisition"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Reuters — SpaceX buys Anysphere for $60 billion"
    url: "https://www.reuters.com/legal/transactional/spacex-buy-anysphere-60-billion-2026-06-16/"
  - label: "CNBC — SpaceX acquires Cursor startup"
    url: "https://www.cnbc.com/2026/06/16/spacex-spcx-cursor-acquisition-ipo.html"
  - label: "TechCrunch — SpaceX to acquire Cursor for $60B"
    url: "https://techcrunch.com/2026/06/16/spacex-to-acquire-cursor-for-60b-in-stock-days-after-blockbuster-ipo/"
  - label: "Go-To Agency — Full breakdown of the deal"
    url: "https://go-to-agency.com/en/blog/spacex-acquires-cursor-60-billion"
---

## La nouvelle

Le 16 juin, SpaceX a signé un accord d'acquisition de **Cursor** (Anysphere Inc.) pour **60 milliards de dollars**, entièrement en actions SpaceX Class A. L'accord est arrivé quatre jours après l'IPO historique de SpaceX au Nasdaq — et moins de deux mois après qu'un partenariat entre les deux entreprises ait été annoncé.

## Les chiffres clés

- **Valorisation** : 60 milliards $, soit 3,4% de dilution à la valorisation IPO de 1,75 billion $.
- **Revenus Cursor** : ~4 milliards $ ARR en juin 2026 (crossé le seuil du milliard en novembre 2025).
- **Croissance fulgurante** : Fondé en 2022 → accélérateur OpenAI (2024) → Série C à 900M$ (valorisation 9,9B$, juin 2025) → 2,3B$ (fin 2025, valorisation 29,3B$) → acquisition SpaceX.
- **Plus rapide acquisition majeure d'un outil développeur** : ~4 ans vs GitHub (7 ans) ou Figma (9 ans).
- **Fermeture prévue** : T3 2026, sous réserve d'approvals réglementaires.

## Ce que ça change concrètement

### Modèles communs SpaceXAI + Cursor
SpaceX a confirmé que **SpaceXAI** (l'ancienne xAI, fusionnée avec SpaceX en février) et Cursor entraînent conjointement un modèle de codage sur le supercalculateur **Colossus**. Ce modèle devrait arriver à la fois dans Cursor et dans Grok Build.

### Trois interfaces IA de codage
L'entité combinée opérera trois surfaces :
1. **Grok Build** — agent terminal
2. **Cursor** — IDE complet
3. Le **modèle joint** SpaceXAI/Cursor

### Impact sur Claude Code et l'écosystème Anthropic
C'est le coup dur. Cursor, qui était un distributeur majeur de modèles tiers dont Claude, va probablement déprécier ou retirer les modèles concurrents au profit du modèle SpaceX par défaut. Pour Anthropic, c'est une perte de canal de distribution critique dans le segment enterprise coding.

### Chute de parts de marché avant l'acquisition
Ironiquement, Cursor perdait du terrain : 41% en juin 2025 → ~26% en mai 2026. Le round de financement de 2 milliards $ prévu était jugé insuffisant par les investisseurs pour atteindre le break-even. L'acquisition SpaceX arrive au moment critique.

## Impact pour l'écosystème local

Pour qui self-host ou utilise des modèles open-weight : l'intégration verticale SpaceX → xAI/Grok → Cursor crée un pipeline fermé de codage IA. Les développeurs qui dépendent de Cursor vont probablement voir leur modèle par défaut basculer vers Grok/SpaceXAI, avec moins de choix.

Cela renforce l'argument en faveur des alternatives open-source (Ollama + modèles GGUF locaux) pour les équipes qui veulent garder le contrôle sur leur stack IA de développement. L'écosystème local reste le seul refuge contre cette concentration verticale.

## À surveiller

- La date exacte de fermeture et les approvals antitrust (60 milliards $ attire l'attention)
- Le modèle conjoint SpaceXAI/Cursor — specs, benchmarks, disponibilité
- La réaction d'Anthropic face à la perte du canal Cursor
- Si les utilisateurs existants de Cursor gardent accès aux modèles tiers
