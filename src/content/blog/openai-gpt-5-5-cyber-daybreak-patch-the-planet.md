---
title: "OpenAI Daybreak : GPT-5.5-Cyber en GA et la course au patch automatique"
description: "Le 22 juin, OpenAI déploie la version complète de GPT-5.5-Cyber (85,6 % CyberGym), Codex Security et le programme Patch the Planet sur plus de 30 projets OSS."
pubDate: 2026-06-24
tags: ["OpenAI", "cybersécurité", "GPT-5.5-Cyber", "Daybreak", "Codex"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "OpenAI — Daybreak: Tools for securing every organization in the world"
    url: "https://openai.com/index/daybreak-securing-the-world/"
  - label: "The Hacker News — OpenAI Expands Daybreak With GPT-5.5-Cyber"
    url: "https://thehackernews.com/2026/06/openai-expands-daybreak-with-gpt-55.html"
---

## La nouvelle

Le **22 juin 2026**, OpenAI a étendu son initiative **Daybreak** au-delà de la simple détection de failles : l’objectif affiché est de **patcher le logiciel vulnérable à la vitesse machine**, avec des humains qui gardent la main sur la validation et le déploiement. Trois briques sortent en même temps : **Codex Security** (plugin mis à jour), la **sortie complète de GPT-5.5-Cyber** (après une preview plus restrictive), et **Patch the Planet** avec Trail of Bits, HackerOne et des mainteneurs OSS.

## Chiffres qui comptent

| Indicateur | Valeur |
|------------|--------|
| CyberGym (reproduction de vulnérabilités connues) | **85,6 %** (GPT-5.5-Cyber) vs **81,8 %** (GPT-5.5) |
| ExploitGym | **39,5 %** vs **25,95 %** |
| SEC-bench Pro | **69,8 %** vs **63,1 %** |
| Depuis mars (preview Codex Security) | **30 M+** commits scannés, **70 k+** findings corrigés (marqués humainement), **500 k+** auto-résolus |

OpenAI insiste : le goulot d’étranglement n’est plus « trouver », c’est **valider, patcher, coordonner la divulgation et déployer**. Les rapports de vulnérabilité seuls ne protègent personne.

## Ce que change GPT-5.5-Cyber

Le modèle est **plus permissif et plus capable** que la preview initiale — volontairement, pour le travail cyber **autorisé** (red team, pentest contrôlé, défense d’infra critique). Il n’est **pas** en accès grand public : distribution via **Trusted Access for Cyber** et partenaires (Cisco, CrowdStrike, Palo Alto, IBM, Fortinet cités dans la presse spécialisée).

**Patch the Planet** engage d’emblée **30+ projets** open source : cURL, Go, Python, noyau Linux, Sigstore, pyca/cryptography, etc. C’est la réponse directe à l’écosystème défensif que Anthropic avait poussé avec Project Glasswing — mais avec un modèle cyber dédié et des métriques publiées.

## Impact industrie

- **SOC et AppSec** : la boucle découverte → preuve → patch devient un produit intégré (SARIF, CodeQL, pipelines Codex CLI), pas un chatbot à côté.
- **Mainteneurs OSS** : volume de PR de sécurité potentiellement énorme — gouvernance et tri humain restent obligatoires.
- **Régulation** : s’aligne avec la logique de l’EO américaine de juin (revue volontaire des modèles frontier) sans attendre une licence obligatoire.

## Limites honnêtes

Les benchmarks CyberGym / ExploitGym mesurent des **environnements contrôlés**. Le risque d’abus dual-use reste réel ; d’où le gating. Pour les équipes sans statut « trusted defender », GPT-5.5 standard reste le seul accès large, avec des refus plus stricts sur le cyber.