---
title: "Google tue Gemini CLI le 18 juin — migration forcée vers Antigravity"
description: "Aujourd'hui, Google coupe l'accès à Gemini CLI pour les utilisateurs individuels et Pro. Le remplacement Antigravity est closed-source et sans parité fonctionnelle."
pubDate: 2026-06-18
tags: ["Google", "Gemini CLI", "Antigravity", "vibe coding", "open source", "migration"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Google Developers Blog — Transitioning Gemini CLI to Antigravity CLI"
    url: "https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/"
  - label: "The Register — Bye-bye Gemini CLI, Google nudges devs toward Antigravity"
    url: "https://www.theregister.com/ai-ml/2026/05/20/bye-bye-gemini-cli-google-nudges-devs-toward-antigravity/5243605"
  - label: "AI Builder Club — Google Kills Gemini CLI June 18"
    url: "https://www.aibuilderclub.com/blog/google-kills-gemini-cli-june-18-2026"
---

## La nouvelle

Aujourd'hui, **18 juin 2026**, Google coupe l'accès à Gemini CLI pour les utilisateurs gratuits, Google AI Pro et Ultra. Le remplacement s'appelle Antigravity CLI — un outil closed-source écrit en Go qui ne propose pas la parité fonctionnelle au lancement. Les pipelines CI/CD qui dépendent de `gemini` dans le terminal cassent sans préavis ni période de grâce.

## Ce qui change concrètement

### Qui est touché
- **Utilisateurs gratuits** : accès coupé immédiatement.
- **Google AI Pro / Ultra** : accès coupé immédiatement.
- **Gemini Code Assist individuel** : accès coupé immédiatement.
- **Gemini Code Assist for GitHub** : plus de nouvelles installations, les requêtes actuelles s'arrêtent dans les semaines à venir.

### Qui n'est PAS touché
- **Enterprise avec licence Standard ou Enterprise** : Gemini CLI continue de fonctionner.
- **Clés API payantes (Gemini / Gemini Enterprise Agent Platform)** : accès maintenu.

### Antigravity CLI — le remplacement
- Outil closed-source en Go, invoqué via `agy` au lieu de `gemini`.
- Fonctionnalités conservées : Agent Skills, Hooks, Subagents, Extensions (renommées « plugins Antigravity »).
- **Pas de parité 1:1** au lancement — Google l'assume explicitement.
- Le projet open-source Gemini CLI (6 000+ contributions) n'est plus maintenu.

## L'impact sur les workflows locaux

Pour qui utilise Gemini CLI dans des pipelines CI/CD, des scripts shell ou des automatisations : c'est un breakage silencieux. Aucune notification proactive de Google, aucune déprecation warning pendant une période de transition. Le jour J, `gemini` renvoie une erreur et c'est tout.

Le passage d'un outil open-source (Gemini CLI) à un outil closed-source (Antigravity) a été largement critiqué par la communauté développeur. The Register note que les contributeurs qui ont construit Gemini CLI n'ont accès ni à l'ancien outil ni au nouveau — sauf avec une licence enterprise.

## Ce qu'il faut faire maintenant

1. **Audit** : lister tous les scripts, Makefiles, pipelines CI/CD qui appellent `gemini`.
2. **Migration** : installer Antigravity CLI (`agy`) et tester chaque workflow critique.
3. **Contournement** : pour les workflows non-entreprise, utiliser une clé API payante Gemini si disponible, ou basculer sur un agent local (Ollama + modèle GGUF).

## Impact pour l'écosystème local

Encore une fois, la tendance est claire : les outils de développement IA se ferment. Gemini CLI était l'un des rares agents de codage open-source majeurs. Sa disparition renforce l'intérêt pour les alternatives locales et souveraines : Ollama avec un modèle de coding (CodeQwen, DeepSeek-Coder), ou LM Studio en mode serveur OpenAI-compatible.

Pour qui self-host, c'est un argument supplémentaire : la dépendance à des outils cloud signifie toujours une exposition au risque de coupure unilatérale.

## À surveiller

- Les mises à jour d'Antigravity CLI — quand arrive la parité ?
- Si la communauté fork Gemini CLI avant qu'il ne soit archivé
- L'évolution de Gemini Code Assist for GitHub (arrêt progressif annoncé)
