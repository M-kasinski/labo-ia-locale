---
title: "Gemini 3.5 Pro : la GA de juin n’arrive pas — Google vise juillet"
description: "Business Insider et Reuters fin juin 2026 : le flagship reasoning de Google glisse en juillet après retours des testeurs et leçons tirées de 3.5 Flash. Impact pour les builders et la course aux agents."
pubDate: 2026-06-28
tags: ["Google", "Gemini", "frontier", "agents", "roadmap"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Business Insider — Google delays Gemini 3.5 Pro to July (24 juin 2026)"
    url: "https://www.businessinsider.com/google-3-5-pro-july-release-tokens-ai-agents-model-2026-6"
  - label: "Investing.com — reprise BI (24 juin 2026)"
    url: "https://www.investing.com/news/stock-market-news/google-delays-gemini-35-pro-model-release-to-july--insider-93CH-4758816"
  - label: "Article Labo — Gemini 3.5 Flash GA et positionnement agentique"
    url: "https://blog.google/products/gemini/gemini-3-5-flash"
---

## La nouvelle

À la fin de **juin 2026**, **Gemini 3.5 Pro** — le flagship annoncé à **Google I/O** le **19 mai** avec la promesse de Sundar Pichai (« *give us until next month* ») — **ne sort pas en disponibilité générale**. **Business Insider**, cité par plusieurs médias le **24 juin**, indique que Google **vise juillet** : plus de temps pour intégrer les retours des testeurs anticipés et **ajuster le modèle**, notamment sur les usages **agentiques** et la **consommation de tokens** observée sur **Gemini 3.5 Flash**.

Ce n’est pas un simple retard de calendrier marketing : c’est le **dernier gros modèle frontier** que le marché attendait encore pour clôturer le mois de juin, au même moment où **OpenAI** limite **GPT-5.6** et où **Anthropic** négocie le retour partiel de **Mythos 5**.

## Analyse technique

### Ce qui était promis à I/O

| Élément | Statut fin juin 2026 |
|--------|----------------------|
| **Gemini 3.5 Flash** | **GA** depuis le 19 mai — API, Gemini app, AI Mode, Antigravity |
| **Gemini 3.5 Pro** | Annoncé, utilisé en interne, **pas d’ID API public** ni fiche modèle complète |
| **Positionnement Pro** | Raisonnement renforcé, rattraper l’écart où Flash « régresse » sur le raisonnement pur |

Le Labo avait déjà couvert **3.5 Flash** comme cheval de bataille **agentique** (vitesse, coût, benchmarks coding). **Pro** devait fermer la boucle : le tier où les équipes acceptent de payer plus pour des tâches **long-horizon** et du **raisonnement lourd**.

### Pourquoi juillet plutôt que juin

Les sources **BI** (personne proche du dossier) mentionnent deux leviers concrets :

1. **Feedback des early testers** — le modèle est en preview limitée (notamment côté **Vertex AI** / entreprises), et Google préfère **itérer** avant une GA large.
2. **Leçons de 3.5 Flash** — plusieurs analyses de marché (dont reprises dans la presse tech fin juin) pointent une **consommation de tokens élevée** sur certains workflows agents ; Pro doit éviter de reproduire ce goulot à l’échelle « flagship ».

Google n’a pas, à ce stade, publié de **date juillet** précise ni un communiqué officiel détaillé — le reportage repose sur des **sources internes**. À traiter comme **signal fort**, pas comme date contractuelle.

### Benchmarks et concurrence (lecture froide)

Sans fiche Pro publiée, les seuls chiffres **vérifiables** restent ceux de **3.5 Flash** (Terminal-Bench, MCP Atlas, etc.) et la comparaison indirecte avec **Claude Opus 4.8**, **GPT-5.5** et **GLM-5.2** open-weight — tous déjà en production ou quasi-production en juin.

Le glissement de Pro change surtout la **fenêtre décisionnelle** :

- Les équipes qui attendaient Pro pour **migrer** depuis 3.1 Pro ou depuis des modèles concurrents doivent **re-baser sur Flash** ou rester sur leur stack actuelle **au moins un mois de plus**.
- Les marchés de prédiction et la presse spéculative avaient **saturé juin** ; un report en juillet **casse la narrative** « tout sort en même temps » (Pro, Sonnet 5, Grok 5, etc.).

### Agents et Computer Use (contexte juin)

Le **24 juin**, le changelog **Gemini API** documente aussi **Computer Use** en preview sur **3.5 Flash** (browser / mobile / desktop, détection d’injection dans les captures). Ce n’est **pas** le lancement de Pro, mais ça confirme la stratégie Google : **shipper les capacités agentiques sur Flash** pendant que Pro termine sa cuisson.

Pour un builder, la conséquence est pragmatique : prototyper agents et **Interactions API** sur **3.5 Flash** maintenant ; traiter Pro comme un **upgrade de raisonnement** à réévaluer à la GA, pas comme un bloquant immédiat.

## Impact pour l’écosystème

### Côté cloud / API

- **Coûts et routage** : Flash reste le **défaut économique** pour les boucles multi-appels ; pas de reset tarifaire Pro avant juillet.
- **Vertex / Enterprise** : les previews Pro continuent probablement pour un cercle restreint ; les contrats « GA juin » doivent être **renégociés** ou assouplis.

### Côté local

Peu d’impact direct sur **llama.cpp / Ollama / vLLM** : Pro est **propriétaire**. En revanche, le retard renforce le récit **open-weight** (GLM-5.2, Nemotron, Kimi K2.x) pour les équipes qui ne peuvent pas dépendre d’un calendrier Google.

### Limites honnêtes

- **Pas d’annonce Google officielle** avec date juillet dans les docs publiques consultées — risque que le calendrier bouge encore.
- **Rumeurs** (fenêtre 2M tokens, « Deep Think », départs de chercheurs vers Anthropic) circulent en parallèle ; ne pas les mélanger avec le report BI **sourcing interne**.
- Un article du **26 juin** sur le retrait **GPT-4.5** et un autre sur **GPT-5.6** couvrent déjà une partie du paysage US ; ici le sujet est **uniquement** le **slip Pro**.

## En synthèse

**Gemini 3.5 Pro** rate la fenêtre **juin 2026** que Pichai avait ouverte à I/O. Google privilégie **qualité agentique et stabilité** sur la date — dans un mois où la régulation et les **export controls** ralentissent déjà d’autres frontières. Pour toi : construis sur **3.5 Flash**, surveille la **page modèles** et le changelog API ; ne bloque pas une roadmap produit sur une GA Pro qui n’est **pas encore signée**.

## Sources

- Business Insider — Google delays Gemini 3.5 Pro launch to July : https://www.businessinsider.com/google-3-5-pro-july-release-tokens-ai-agents-model-2026-6
- Investing.com — reprise du reportage BI (24 juin 2026) : https://www.investing.com/news/stock-market-news/google-delays-gemini-35-pro-model-release-to-july--insider-93CH-4758816
- Google I/O — Gemini 3.5 Flash (19 mai 2026) : https://blog.google/products/gemini/gemini-3-5-flash
- Gemini API — Release notes (Computer Use 24 juin 2026) : https://ai.google.dev/gemini-api/docs/changelog