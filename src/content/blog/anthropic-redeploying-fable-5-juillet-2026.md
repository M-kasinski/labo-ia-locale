---
title: "Anthropic redeploye Claude Fable 5 : retour apres la coupure des export controls"
description: "30 juin 2026 — Anthropic remet Fable 5 et Mythos 5 en service apres 18 jours de suspension, avec de nouveaux classificateurs de securite et un retour a un acces mondial sous conditions."
pubDate: 2026-07-01
tags: ["Claude", "Fable 5", "Mythos 5", "export controls", "sécurité", "cybersecurité"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Anthropic — Redeploying Claude Fable 5 (30 juin 2026)"
    url: "https://www.anthropic.com/news/redeploying-fable-5"
  - label: "Anthropic — Claude Fable 5 and Claude Mythos 5 (9 juin 2026)"
    url: "https://www.anthropic.com/news/claude-fable-5-mythos-5"
---

## La nouvelle

Le **30 juin 2026**, Anthropic publie un billet : **Claude Fable 5 et Claude Mythos 5 sont redeployés**. Le modele est de retour, mais pas exactement comme il etait il y a trois semaines. L'incident des **export controls** américains du **12 juin** a été court — 18 jours — mais il a change la donne sur deux fronts : la **securité** et l'**acces**.

Fable 5 est de retour globalement a partir du **1er juillet**, avec des limites d'usage. Mythos 5 reste restreint aux organisations americaines approuvees par le gouvernement.

## Chronologie de l'incident

1. **9 juin** — Lancement de Fable 5 et Mythos 5. Fable 5 avec des safeguards solides pour un usage general. Mythos 5 avec moins de safeguards, reserve aux partenaires du **Project Glasswing** pour la cybersecurité defensive.

2. **12 juin** — Les **export controls** américains s'appliquent. **Amazon** signale une methode pour contourner les safeguards de Fable 5, le poussant a identifier des vulnerabilites logicielles et a produire du code d'exploitation. L'acces est suspendu pour tous les utilisateurs.

3. **26 juin** — Le gouvernement americain approuve la restauration de l'acces a Mythos 5 pour un ensemble d'organisations americaines.

4. **30 juin** — Les export controls sont leves. Fable 5 est redeployé globalement.

## Les conclusions d'Anthropic sur le bypass

Anthropic a teste le bypass sur d'autres modeles : **Claude Opus 4.8**, **GPT-5.5**, **Kimi K2.7**, **Claude Haiku 4.5**, **Sonnet 4.6**, **Opus 4.6/4.7/4.8**, **GPT-5.4/5.5**.

**Resultat** : tous les modeles testes pouvaient identifier les memes vulnerabilites et produire la meme demonstration d'exploitation. Le bypass n'exposait **pas de capacites cyber uniques a Mythos** — c'etait un **cas borderline** pour les safeguards de Fable 5 : du travail de cybersecurité defensive courant bloque par excès de prudence.

C'est une revelation importante : le bypass n'etait pas un **universal jailbreak** (Row E), mais un **narrow harmful jailbreak** (Row D) — il contourne les classificateurs pour debloquer un comportement specifique, mais sans ouvrir une classe entiere de comportements nuisibles.

## Les nouveaux safeguards

Anthropic a entraine un **nouveau classificateur de securité** ciblant le comportement precise decrit dans le rapport Amazon.

- **Efficacite** : le nouveau classificateur bloque la technique specifique dans **plus de 99% des cas**.
- **Fallback** : si une requete est bloque, l'utilisateur est notifie et la requete est envoyee a **Opus 4.8**.
- **Validation** : les chercheurs du **Center for AI Standards and Innovation (CAISI)** du Departement du Commerce americain ont teste les nouveaux safeguards et les jugent **"extraordinarily strong"**.

## Le compromis : plus de faux positifs

Le nouveau classificateur a un cout : il signale plus de requetes bénignes pendant les taches courantes de codage et de debogage. Anthropic s'engage a affiner le classificateur pour mieux distinguer les abus reels des requetes legitimes.

C'est le compromis classique de la **securité par excès de prudence** : on bloque plus de requetes bénignes pour s'assurer de ne pas en manquer une.

## Acces et pricing

### Fable 5

- **Acceès global** a partir du **1er juillet** sur Claude Platform, Claude.ai, Claude Code et Claude Cowork.
- **Limites d'usage (jusqu'au 7 juillet)** : inclus a hauteur de **50% des limites d'usage hebdomadaires** pour les plans Pro, Max, Team et Enterprise select.
- **Apres le 7 juillet** : acces via **credits d'usage**.
- **Enterprise Standard** : pas de quota inclus ; facturation via credits d'usage.
- **Enterprise Premium** : inclus dans l'abonnement jusqu'au 7 juillet ; tire des credits de siege membre sans cout supplementaire.
- **Fournisseurs cloud** : acces sur AWS, Google Cloud et Microsoft Foundry sera réactivé **dans les plus brefs délais**.

### Mythos 5

- **Organisations americaines** : acces restaure pour un ensemble d'organisations americaines suivant l'approbation gouvernementale du **26 juin**.
- **Programme Glasswing** : Anthropic continue de coordonner avec le gouvernement pour élargir l'acces aux partenaires domestiques et internationaux dans le cadre du programme Glasswing.

## Impact pour l'ecosystème local

### Côté praticien

- **Fable 5** reste un modele API — pas de poids téléchargeables. Les modeles locaux (Llama, Qwen, GLM) restent la solution pour l'usage local.
- **Le bypass de la semaine dernière** montre que les safeguards ne sont pas une frontière absolue — mais pour l'usage local, c'est un non-probleme.
- **Opus 4.8** reste un fallback utile : si Fable 5 bloque une requete legitime, Opus 4.8 prend le relais.

### Côté industrie

- **L'incident des export controls** est un rappel que les modeles frontier americains ne sont pas seulement des outils techniques — ils sont aussi des **actifs géopolitiques**.
- **Les safeguards** sont un équilibre constant entre securité et usabilité. Le compromis du nouveau classificateur (plus de faux positifs, moins de vrais risques) est un pattern qu'on reverra probablement avec les modeles futurs.
- **Le programme Glasswing** est un modele intéressant : une version "naked" d'un modele frontier pour des partenaires de confiance, avec des safeguards retirés dans des domaines critiques. C'est un precedent pour la gestion des modeles "trop capables" pour un usage general.

## Ce qu'il faut surveiller en juillet 2026

- **Apres le 7 juillet** : le passage aux credits d'usage pour Fable 5 et son impact sur l'adoption.
- **L'affinement du classificateur** : Anthropic promet de reduire les faux positifs. A suivre.
- **L'expansion du programme Glasswing** : quelles autres organisations seront approuvees ?
- **Les nouvelles vulnérabilités** : si le bypass de la semaine dernière n'était pas un universal jailbreak, d'autres le seront-ils ?

## Sources vérifiées

- [Anthropic — Redeploying Claude Fable 5 (30 juin 2026)](https://www.anthropic.com/news/redeploying-fable-5)
- [Anthropic — Claude Fable 5 and Claude Mythos 5 (9 juin 2026)](https://www.anthropic.com/news/claude-fable-5-mythos-5)
