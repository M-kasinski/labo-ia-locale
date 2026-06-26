---
title: "Colorado AI Act : dans quatre jours, les systèmes à haut risque entrent dans le vrai monde"
description: "L’application du SB24-205 est fixée au 30 juin 2026. Bilan des obligations pour développeurs et déployeurs d’IA sur décisions « conséquentielles », entre débats législatifs et pression fédérale US."
pubDate: 2026-06-26
tags: ["régulation", "Colorado", "AI Act", "compliance", "États-Unis"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Colorado General Assembly — SB24-205"
    url: "https://leg.colorado.gov/bills/sb24-205"
  - label: "White & Case — State AI laws and federal EO 14365"
    url: "https://www.whitecase.com/insight-alert/state-ai-laws-under-federal-scrutiny-key-takeaways-executive-order-establishing"
  - label: "Drata — State and Federal AI Laws 2026"
    url: "https://drata.com/learn/ai/state-federal-regulations-laws"
---

## La nouvelle

Le **30 juin 2026**, le **Colorado Artificial Intelligence Act** (projet de loi **SB24-205**) entre en vigueur pour les obligations imposées aux **développeurs** et **déployeurs** de systèmes d’IA à **haut risque** utilisés pour des **décisions conséquentielles** (emploi, logement, crédit, éducation, santé, assurance, services publics essentiels, etc.). À la date de publication de cet article (**26 juin 2026**), il reste **quatre jours** avant la date d’application — après plusieurs reports (initialement février 2026, puis repoussé via le « AI Sunshine Act » d’août 2025).

Ce n’est pas une annonce de dernière minute : la loi date de 2024. En revanche, **la fenêtre opérationnelle** se referme maintenant, alors que l’administration fédérale américaine pousse un **cadre national** visant à limiter la fragmentation étatique.

## Analyse technique

### Qui est concerné ?

Le Colorado distingue :

| Rôle | Responsabilité typique |
|------|-------------------------|
| **Developer** | Conçoit ou substantiellement modifie un système IA à haut risque |
| **Deployer** | Utilise un tel système pour influencer une décision conséquentielle |

Les obligations tournent autour du **devoir de reasonable care** pour éviter la **discrimination algorithmique**, avec :

- **Politique et programme de gestion des risques** documentés ;
- **Impact assessments** avant déploiement et après modifications substantielles ;
- **Transparence** envers les consommateurs (notice, explication, parfois opt-out selon le cas d’usage) ;
- Documentation conservée et disponible en cas de contrôle.

Les amendements restent possibles lors de la session législative 2026 — plusieurs sources juridiques signalent des **débats actifs** sur exemptions PME, périodes de cure et définitions — mais **aucun report officiel** n’a été identifié au 26 juin pour repousser à nouveau le 30 juin.

### Sanctions et cure

Les analyses consolidées citent des pénalités pouvant aller jusqu’à **20 000 USD par violation**, avec une **période de cure** (souvent **60 jours**) avant application stricte des sanctions — détail à vérifier sur le texte consolidé et les règles d’agence une fois publiées.

### Le contexte fédéral (juin 2026)

Deux signaux fédéraux encadrent Colorado :

1. **Executive Order du 2 juin 2026** — « Promoting Advanced Artificial Intelligence Innovation and Security » : accent sur la **cyber-défense** et un cadre **volontaire** de revue des modèles frontier (benchmarking, accès gouvernement limité pré-release). Ce n’est pas un préempt direct des lois étatiques.

2. **National Policy Framework (mars 2026)** et **EO 14365 (décembre 2025)** — volonté de **réduire la multiplication** des régimes étatiques jugés contraires à la compétitivité US. Les cabinets d’avocats rappellent : **sans loi fédérale de préemption**, Colorado et Californie (AI transparency, ADMT) restent **applicables** à court terme.

Pour une scale-up qui vend de l’IA B2B aux États-Unis, la conséquence est un **double travail** : modèle de conformité Colorado + veille sur les contentieux fédéraux contre certaines lois étatiques.

### Parallèle UE (pour le lecteur global)

Le **2 août 2026** marque une autre échéance majeure : obligations de transparence **Article 50** du **EU AI Act** (marquage contenu IA générative), avec un **Code of Practice** publié le **10 juin 2026** encore en phase d’évaluation d’adéquation. Colorado et UE ne partagent pas le même texte, mais la même **pression calendaire** sur les équipes produit qui servent les deux marchés.

## Impact pour l’écosystème

### Éditeurs de logiciels IA

- Les **API closed** (OpenAI, Anthropic, Google) poussent déjà des addenda contractuels « high-risk » ; les clients enterprise coloradois vont exiger des **attestations** et des logs d’évaluation.
- Les **modèles open-weight** n’exemptent pas le **déployeur** : si tu fine-tunes Llama ou Qwen pour le recrutement, tu es dans le périmètre deployer/developer selon le degré de modification.

### Self-hosting et « local »

Le Labo local prône l’inférence on-premise ; la conformité Colorado rappelle que **l’emplacement des poids** (Mac M4, serveur Ollama interne) ne supprime pas les **obligations process** si la décision affecte un résident du Colorado. L’avantage du local reste **contrôle des données** et **auditabilité**, pas une exemption automatique.

### Investisseurs et M&A

Les due diligences 2026 intègrent désormais des checklists **AI Act EU + Colorado + Californie** ; un retard sur les impact assessments peut bloquer un contrat public ou une levée série B.

## Limites honnêtes

- **Texte en mouvement** : amendements coloradois possibles ; cet article décrit le cap **30 juin 2026** tel que documenté par les sources compliance au moment de la rédaction.
- **Pas de conseil juridique** : chaque cas d’usage (recrutement vs recommandation marketing) change le périmètre « high-risk ».
- **Enforcement réel** : les premiers mois verront probablement des **mises en demeure** et de la doctrine administrative avant des amendes massives.
- **Friction fédérale** : un changement congressionnel ou judiciaire pourrait rogner l’effet des lois étatiques — à suivre, pas à parier pour ton plan Q3.

## Checklist pragmatique (avant le 30 juin)

1. Inventorier les systèmes IA qui influencent une **décision conséquentielle** pour des utilisateurs au Colorado.
2. Rédiger ou mettre à jour la **politique de gestion des risques** IA (même format que ISO 42001 / NIST AI RMF aide).
3. Produire une **impact assessment** par système à haut risque (données, biais, supervision humaine, recours).
4. Aligner **notices utilisateur** et processus de contestation avec le SB24-205.
5. Documenter la chaîne **fournisseur de modèle → intégration → décision** pour les audits.

## Sources vérifiées

- [SB24-205 — Colorado General Assembly](https://leg.colorado.gov/bills/sb24-205)
- [State AI laws under federal scrutiny — White & Case (janv. 2026)](https://www.whitecase.com/insight-alert/state-ai-laws-under-federal-scrutiny-key-takeaways-executive-order-establishing)
- [Artificial Intelligence Regulations 2026 — Drata](https://drata.com/learn/ai/state-federal-regulations-laws)
- [Executive Order — Promoting Advanced AI Innovation and Security (2 juin 2026)](https://www.whitehouse.gov/presidential-actions/2026/06/promoting-advanced-artificial-intelligence-innovation-and-security/)