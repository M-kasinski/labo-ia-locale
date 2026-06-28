---
title: "Gemini 3.5 Flash : Computer Use passe en preview publique sur l’API"
description: "Le 24 juin 2026, Google documente Computer Use sur Gemini 3.5 Flash — actions simplifiées, browser/mobile/desktop et détection d’injection dans les captures. Analyse pour les équipes qui branchent des agents sans attendre Pro."
pubDate: 2026-06-28
tags: ["Google", "Gemini", "Computer Use", "agents", "API"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Gemini API — Release notes (24 juin 2026)"
    url: "https://ai.google.dev/gemini-api/docs/changelog"
  - label: "Gemini API — Computer Use"
    url: "https://ai.google.dev/gemini-api/docs/computer-use"
  - label: "Business Insider — Gemini 3.5 Pro reporté (juin 2026)"
    url: "https://www.businessinsider.com/google-3-5-pro-july-release-tokens-ai-agents-model-2026-6"
---

## Le signal

Le **24 juin 2026**, le changelog **Gemini API** acte une étape concrète : **Computer Use** est en **preview publique** sur **`gemini-3.5-flash`**. Ce n’est pas l’annonce de **Gemini 3.5 Pro** en GA — sujet déjà couvert ailleurs sur le labo — mais le moment où Google **shippe l’interface agentique** sur le modèle **rapide** que l’écosystème utilise déjà en production (app Gemini, AI Mode, Antigravity, remplacement des **2.0 Flash** depuis le **1er juin**).

En clair : pendant que Pro termine sa cuisson, **Flash devient le banc d’essai officiel** pour piloter un navigateur, un mobile ou un bureau via le modèle.

## Ce que Computer Use change techniquement

D’après la documentation et les notes de version du **24 juin** :

| Dimension | Détail annoncé |
|-----------|----------------|
| **Modèle cible** | `gemini-3.5-flash` (famille déjà en GA depuis I/O, mai 2026) |
| **Surface** | Browser, mobile, desktop — pas seulement une API « texte + tools » |
| **Actions** | Schéma d’actions **simplifié** avec **intents** (moins de micro-clics à décrire côté client) |
| **Sécurité** | Paramètres de sécurité **configurables** + **détection d’injection** dans les captures (prompt injection visuelle / UI) |

Computer Use n’est pas nouveau comme concept — OpenAI, Anthropic et Cursor l’ont popularisé sur le coding et le desktop — mais l’intérêt ici est **l’alignement produit** : Google ne réserve pas la capacité au flagship retardé ; il la met sur **Flash**, optimisé pour **volume**, **latence** et **boucles agentiques** (multiples appels, tool use, contexte long).

Pour un builder, ça veut dire : tu peux prototyper des workflows « voir l’écran → agir » **sans** attendre Pro, avec une **grille tarifaire Flash** et une **fenêtre de contexte** déjà dimensionnée pour l’agentique (Google communique Flash comme modèle par défaut pour code et agents depuis mai).

## Benchmarks et promesses : rester lucide

Google n’a pas publié, dans cette entrée changelog du **24 juin**, une table de scores type SWE-bench ou OSWorld attachée à Computer Use. Les perfs agentiques dépendent autant du **harness** (sandbox, permissions, replanification) que du modèle — thème déjà visible en juin avec la « convergence » GLM / Opus / GPT et la course au **harness engineering**.

Ce qu’on peut affirmer sans bullshit :

- **Flash bat souvent Pro en tokens/s** sur les slides I/O ; Computer Use sur Flash vise donc des **boucles courtes** et du **parallélisme d’agents**, pas un raisonnement ultra-long unique.
- La **détection d’injection dans les captures** répond à un risque réel : une page web ou une app malveillante peut tenter de détourner l’agent via du texte invisible ou des overlays. C’est un prérequis si tu déploies Computer Use hors labo fermé.

## Impact écosystème et local

### Côté cloud / enterprise

- **Antigravity** et **Managed Agents** (sandbox Linux hébergé, annoncés mai 2026) forment une pile cohérente : modèle rapide + environnement + Computer Use.
- Les équipes qui ont migré de **2.0 Flash** vers **3.5 Flash** le **1er juin** récupèrent Computer Use **sans changer d’ID modèle** — seulement activer la preview et le harness côté client.

### Côté self-hosting

Computer Use **Gemini** reste **API Google**. Ça ne remplace pas **llama-server --agent**, **Codex local**, ou **MLX-LM Server** sur Mac. En revanche, ça fixe le **standard de fonctionnalités** que les runtimes locaux doivent rattraper : intents UI, garde-fous capture, détection d’injection.

Pour le labo **local**, la lecture utile est comparative :

1. **Coût** : Flash + Computer Use = facturation cloud + surface d’attaque élargie.
2. **Contrôle** : local = tu choisis les outils (`exec_shell_command` chez llama.cpp, MCP, etc.) mais tu portes la sécurité toi-même.
3. **Hybride** : orchestrateur local qui appelle Gemini uniquement pour les étapes « vision UI » reste plausible — à condition de tracer données et captures.

## Limites honnêtes

- **Preview publique** ≠ SLA production ; APIs et schémas d’actions peuvent bouger (cf. breaking changes Interactions API en mai 2026).
- **Computer Use** sans gouvernance (RBAC, journalisation, kill switch) reproduit les incidents déjà vus sur les agents desktop : l’agent voit ce que tu vois, y compris secrets à l’écran.
- **Gemini 3.5 Pro** toujours attendu **juillet** selon la presse fin juin — certaines équipes voudront Pro pour le raisonnement et Flash pour l’exécution UI ; Google n’a pas encore documenté un split officiel « planner Pro + executor Flash » dans cette note du 24.

## Sources

- Gemini API changelog — entrée **24 juin 2026** (Computer Use, Gemini 3.5 Flash) : https://ai.google.dev/gemini-api/docs/changelog  
- Documentation Computer Use : https://ai.google.dev/gemini-api/docs/computer-use  
- Contexte calendrier Pro / stratégie Flash : article labo sur le glissement **Gemini 3.5 Pro** (juin 2026)