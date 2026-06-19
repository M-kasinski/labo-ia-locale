---
title: "Claude Fable 5 : le shutdown imposé par Washington et la guerre des jailbreaks"
description: "La Maison Blanche a forcé la suspension de Claude Fable 5 le 12 juin. Six jours après, les négociations s'enlisent entre Anthropic et le gouvernement américain."
pubDate: 2026-06-18
tags: ["Anthropic", "Claude Fable 5", "export controls", "jailbreak", "géopolitique IA"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Annonce officielle Anthropic — Suspension de Fable 5 et Mythos 5"
    url: "https://www.anthropic.com/news/claude-fable-5-mythos-5"
  - label: "AI News Today — June 19, 2026 (BuildFastWithAI)"
    url: "https://www.buildfastwithai.com/blogs/ai-news-today-june-19-2026"
  - label: "Analyse détaillée — When Will Claude Fable 5 Return?"
    url: "https://pasqualepillitteri.it/en/news/5180/claude-fable-5-when-will-it-return"
  - label: "Polymarket — Fable 5 restoration predictions"
    url: "https://polymarket.com/event/claude-fable-5-restored-for-us-customers-by-20260613193753196"
---

## La nouvelle

Le 12 juin 2026, Anthropic a suspendu l'accès à **Claude Fable 5** et **Claude Mythos 5** suite à une directive des export controls du gouvernement américain. Six jours plus tard (18 juin), aucune date de réactivation n'a été confirmée. Les ingénieurs d'Anthropic sont à Washington pour des négociations en face-à-face avec le Département du Commerce, mais le ton de la Maison Blanche s'est durci.

## La séquence des événements

### Double déclencheur (12 juin)

1. **SK Telecom signalée :** Le gouvernement américain a identifié SK Telecom — principal opérateur sud-coréen, investisseur d'Anthropic à hauteur de 100 M$ depuis 2023 et partenaire Project Glasswing — comme soupçonnée de liens avec la Chine. Anthropic a immédiatement révoqué l'accès Mythos de SK Telecom.

2. **Rapport de vulnérabilité Amazon :** Des chercheurs d'Amazon ont séparément identifié des vulnérabilités dans Fable 5. La Maison Blanche a conclu qu'elle « ne pouvait pas faire confiance à Anthropic pour protéger sa technologie IA la plus avancée ». Directive d'export control reçue le 12 juin à 17h21.

**Résultat :** Le filtrage en temps réel par nationalité étant techniquement irréalisable, Anthropic a désactivé les deux modèles **mondialement**.

### L'ultimatum de David Sacks (13 juin)

David Sacks, co-président du Conseil présidentiel des conseillers en sciences et technologie (PCAST), a révélé que l'administration proposait à Anthropic un choix : **corriger le jailbreak identifié ou déployer volontairement le modèle**.

Dario Amodei a refusé les deux options. L'équipe technique d'Anthropic a examiné la technique et n'a trouvé que des vulnérabilités mineures connues. Les corriger nuirait aux capacités de recherche en sécurité légitime ; déployer le modèle validerait un précédent techniquement infondé.

### « Zéro jailbreak » — une exigence techniquement impossible (17 juin)

La Maison Blanche exige désormais qu'Anthropic **élimine tous les jailbreaks** avant toute relance et teste/provoque proactivement les vulnérabilités.

Le consensus de la communauté de sécurité est clair : Katie Moussouris, Stanford HAI, et les signataires de la lettre `freefable.org` affirment qu'une prévention complète des jailbreaks est **techniquement impossible** avec les méthodes actuelles. La sécurité IA est un problème de défense en profondeur — les nouvelles techniques adversariales dépassent toujours les blocages.

### Situation au 18 juin

- Fox Business rapporte que la Maison Blanche accuse Anthropic de « négligence » et dit que l'entreprise n'a pas pris suffisamment au sérieux la demande de correction avant le lancement.
- Chris Ciauri (Managing Director International d'Anthropic), lors de l'ouverture du bureau de Séoul, a déclaré : « Nous sommes très confiants que les modèles seront disponibles à nouveau dans les jours à venir. »
- Anthropic a confirmé un **modèle d'accès basé sur des crédits** pour Fable 5 à partir du 23 juin (après la période gratuite se terminant le 22).

## Impact pour l'écosystème

C'est le premier cas documenté où le gouvernement américain force la suspension mondiale d'un modèle IA frontier en production. Les précédents sont généralement des restrictions d'exportation ciblées (comme celles sur les GPU vers la Chine), pas un shutdown total d'un produit grand public.

Pour les développeurs qui dépendaient de Fable 5 via l'API : le modèle reste disponible sur l'API et les plans Enterprise à consommation, mais les abonnements Pro/Max/Team sont impactés. Les requêtes dans les domaines cybersécurité/biologie sont automatiquement redirigées vers Opus 4.8 (sans frais Fable).

Le précédent est inquiétant : si la Maison Blanche peut invoquer des « jailbreaks » pour suspendre un modèle, d'autres modèles pourraient suivre — surtout si la définition de « jailbreak » reste floue. La réponse de la communauté sécurité (`freefable.org`) est une tentative de cadrer le débat sur des bases techniques plutôt que politiques.
