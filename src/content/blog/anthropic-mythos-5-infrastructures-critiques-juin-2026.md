---
title: "Claude Mythos 5 : Washington autorise un redeploy ciblé sur les infrastructures critiques"
description: "Fin juin 2026, Anthropic annonce une exception gouvernementale pour remettre Mythos 5 entre les mains d’opérateurs d’infrastructures critiques — pendant que Fable 5 reste en négociation."
pubDate: 2026-06-27
tags: ["Anthropic", "Mythos 5", "Fable 5", "cybersécurité", "régulation", "infrastructure"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "THE DECODER — US approval to redeploy Mythos 5 (27 juin 2026)"
    url: "https://the-decoder.com/anthropic-has-us-approval-to-redeploy-mythos-5-for-critical-infrastructure-organizations/"
  - label: "Anthropic — annonce X (référencée par THE DECODER)"
    url: "https://x.com/AnthropicAI/status/2070665903440871779"
  - label: "The Verge — Mythos 5 is back, Trump negotiations"
    url: "https://www.theverge.com/ai-artificial-intelligence/958458/anthropic-mythos-5-is-back-trump-negotiations"
---

## La nouvelle

Après la **coupure mondiale** du **12 juin 2026** imposée aux export controls américains sur **Claude Fable 5** et **Claude Mythos 5**, Anthropic obtient fin juin un feu vert **partiel** : le gouvernement US approuve le **redéploiement de Mythos 5** pour les **organisations qui exploitent et protègent des infrastructures critiques**.

L’annonce passe par le compte **Anthropic sur X** (reprise par THE DECODER le **27 juin**). Ce n’est **pas** un retour grand public : **Fable 5** (version « Mythos avec garde-fous ») et l’accès large restent **en négociation**, **sans calendrier**. Le parallèle avec **GPT-5.6 Sol** (preview partenaires validés « client par client ») devient la norme de juin pour les modèles **cyber-capables**.

## Analyse technique

### Mythos vs Fable — rappel utile

| Produit | Positionnement | Statut fin juin 2026 |
|---------|----------------|----------------------|
| **Mythos 5** | Cyber offensif/défensif, garde-fous réduits pour clients approuvés | **Redeploy** infra critique US + employés/orga approuvés **non-US** selon l’exception rapportée |
| **Fable 5** | Même backbone, classifieurs + fallback Opus 4.8 | Toujours **coupé** pour le grand public ; restauration annoncée comme objectif |

Mythos 5 n’est pas un « meilleur chatbot » : c’est un **modèle frontier orienté vulnérabilités**, classé parmi les plus chers et lents du marché (ordre de grandeur **10–12,5 $ / M tokens entrée**, **50 $ / M sortie** selon les fiches tierces).

### Qui peut y accéder

D’après la synthèse presse :

- opérateurs **US** d’**infrastructures critiques** (énergie, telecom, finance systémique — le périmètre exact dépend des contrats et listes gouvernementales) ;
- **employés Anthropic non ressortissants US** et membres d’organisations approuvées **non-US**, dans le cadre de l’exception — un assouplissement par rapport au blocage total du 12 juin.

Anthropic dit travailler avec l’administration pour **élargir** Mythos et **réouvrir Fable** ; OpenAI, de son côté, évoque **quelques semaines** avant élargissement GPT-5.6 Sol.

### Chronologie serrée (juin 2026)

1. **9 juin** — lancement Fable 5 / Mythos 5.
2. **12 juin** — directive Commerce : coupure **mondiale** API.
3. **18 juin** — presse coréenne : optimisme prudents « jours à venir » (Labo : article dédié).
4. **25–26 juin** — pression similaire sur OpenAI GPT-5.6 ; éval **METR** sur triche Sol.
5. **26–27 juin** — **exception Mythos** infra critique.

## Impact pour l’écosystème

### Secteur & géopolitique

- **Dual-use par défaut** : les modèles cyber ne sont plus des produits SaaS classiques ; ils ressemblent à des **licences export contrôlées**.
- **Europe & Asie** : les équipes qui comptaient sur Fable/Mythos pour de la recherche défensive doivent **pivoter** vers API encore disponibles, **open-weight** (GLM-5.2, Kimi K2.7) ou partenariats US — avec risque de **coupure politique** à tout moment.
- **Inde & souveraineté** : le narratif « IA souveraine » gagne du poids quand Washington peut **éteindre** un modèle globalement du jour au lendemain.

### Écosystème local

- **Pas de poids Mythos** : rien à self-hoster ; l’alternative locale reste **Nemotron**, **GLM quantifié**, **Qwen coder** — moins spécialisés cyber, mais **sans kill switch BIS**.
- **Pentest & bug bounty** : les équipes légitimes doivent documenter **usage dual-use** et prévoir des **refus classifieurs** même si l’accès revient — même logique que les faux positifs décrits par OpenAI sur Sol.
- **Agents** : les harness qui chaînent outils shell + scan réseau restent **plus risqués** qu’un frontier API filtré ; la régulation pousse paradoxalement vers **plus de contrôle produit**, pas moins.

## Limites honnêtes

- **Détails contractuels** : la presse ne publie pas la liste des secteurs « infrastructure critique » ni les SLA.
- **Fable 5** : toujours pas de date ; ne pas confondre l’exception Mythos avec une **réouverture chat grand public**.
- **Efficacité réelle** : benchmarks cyber Anthropic vs **METR/OpenAI** sur triche et ExploitBench — comparaison indirecte seulement.
- **Mise à jour** : ce article complète les publications Labo du **12–18 juin** sur la coupure Fable/Mythos ; il documente l’**étape du 27 juin**, pas l’issue finale des négociations.

## Sources

- THE DECODER — Anthropic US approval Mythos 5 critical infrastructure (27 juin 2026) : https://the-decoder.com/anthropic-has-us-approval-to-redeploy-mythos-5-for-critical-infrastructure-organizations/
- Anthropic (X) — statut redeploy : https://x.com/AnthropicAI/status/2070665903440871779
- The Verge — Mythos 5 is back / negotiations : https://www.theverge.com/ai-artificial-intelligence/958458/anthropic-mythos-5-is-back-trump-negotiations