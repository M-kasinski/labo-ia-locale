---
title: "GitHub en crise : Microsoft route le trafic vers AWS après l'effondrement des agents IA"
description: "Avec 88,4 % de disponibilité en juin et 17 millions de pull requests d'agents par mois, GitHub a dû emprunter la capacité cloud d'AWS pour tenir. Un signal fort sur les limites du scale."
pubDate: 2026-06-19
tags: ["GitHub", "Microsoft", "AWS", "infrastructure", "agents IA", "CI/CD"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Tech Times — GitHub's AI Agent Crisis Forces Microsoft to Tap AWS"
    url: "https://www.techtimes.com/articles/318481/20260616/githubs-ai-agent-crisis-forces-microsoft-tap-aws-outages-break-enterprise-slas.htm"
  - label: "AI Weekly — Microsoft Taps AWS to Keep GitHub Running Amid AI Surge"
    url: "https://aiweekly.co/alerts/microsoft-taps-aws-to-keep-github-running-amid-ai-surge"
  - label: "Let's Data Science — GitHub Capacity Surge Pushes Microsoft to AWS"
    url: "https://letsdatascience.com/news/github-capacity-surge-pushes-microsoft-to-aws-13a2ffa4"
  - label: "Business Insider — Microsoft provisions AWS capacity for GitHub"
    url: "https://www.businessinsider.com/microsoft-github-aws-capacity-ai-coding-2026-6"
---

## La nouvelle

Microsoft a confirmé le **16 juin 2026** qu'il provisionne de la capacité cloud chez **Amazon Web Services** — son plus grand concurrent dans le cloud public — pour soutenir GitHub. La cause : une explosion du trafic générée par les agents de codage IA qui a fait chuter la disponibilité de la plateforme à **88,4 % en juin**, bien en dessous du seuil SLA enterprise de 99,9 %.

## Les chiffres qui expliquent le feu

- **Pull requests d'agents** : de 4 millions en septembre 2025 à **plus de 17 millions par mois en mars 2026** — une hausse de 325 % en six mois.
- **Commits hebdomadaires** : 275 millions/semaine, sur les rails pour **14 milliards en 2026** contre 1 milliard pour toute l'année 2025.
- **Compute GitHub Actions** : de 500 millions de minutes/semaine en 2023 à **2,1 milliards en une seule semaine au début 2026**.
- **Incidents service** : 9 incidents en mai 2026, 10 en avril. Disponibilité moyenne juin : **88,4 %**.

Le COO de GitHub, Kyle Daigle, a confirmé en avril que la plateforme avait révisé son objectif de capacité de ×10 à ×30 parce que l'adoption des agents codait plus vite que prévu.

## Pourquoi AWS ? L'ironie architecturale

GitHub migre progressivement vers Azure — 40 % du trafic monolithe était déjà sur Azure en mai, avec un objectif de 50 % d'ici juillet. Mais cette migration ne peut pas absorber les pics générés par les agents. D'où le recours à AWS comme capacité temporaire de burst.

Le paradoxe : Microsoft emprunte l'infrastructure de son concurrent principal pour maintenir la plateforme qu'il possède. Un signal — même non intentionnel — que **la demande IA dépasse la capacité de n'importe quel cloud unique**.

## Impact pour les développeurs et l'écosystème local

Trois conséquences directes :

**1. FIabilité des pipelines CI/CD.** Avec 88,4 % de disponibilité, une entreprise sur cinq voit ses builds échouer ou se dégrader en juin. Pour les équipes qui dépendent de GitHub Actions pour leurs déploiements, c'est un risque opérationnel concret. GitLab et les solutions auto-hébergées (Gitea, Forgejo) gagnent en attractivité.

**2. Le coût caché des agents IA.** Chaque agent qui ouvre une PR, déclenche un workflow, fetch des dépendances et demande une review consomme des ressources bien au-delà d'un commit humain. L'infrastructure n'a pas été conçue pour ce pattern — et personne ne l'a payée.

**3. Signal pour le self-hosting.** Quand la plateforme dominante montre ses limites, l'argument du self-hosting se renforce. Gitea + runner auto-hébergé sur une machine locale = 100 % de disponibilité sans dépendre d'un cloud qui explose. Pour les projets sensibles, c'est un calcul simple.

## Ce qui suit

Microsoft prévoit d'améliorer la situation d'ici **septembre 2026** selon Daigle. Mais le fond du problème est architectural : GitHub repose sur une base Ruby on Rails monolithique où un incident peut cascader simultanément sur Actions, Copilot et l'interface web. La migration Azure ne résout pas ce couplage — elle ne fait que déplacer le problème.

Pour les développeurs locaux et les équipes qui construisent des pipelines d'agents : la leçon est claire. **Ne dépendez pas d'une plateforme dont la disponibilité chute sous 90 % parce que les agents IA l'ont saturée.** Diversifiez, auto-hébergez, planifiez le worst case.

## Sources vérifiées

- [Tech Times — GitHub's AI Agent Crisis Forces Microsoft to Tap AWS](https://www.techtimes.com/articles/318481/20260616/githubs-ai-agent-crisis-forces-microsoft-tap-aws-outages-break-enterprise-slas.htm)
- [AI Weekly — Microsoft Taps AWS to Keep GitHub Running](https://aiweekly.co/alerts/microsoft-taps-aws-to-keep-github-running-amid-ai-surge)
- [Let's Data Science — GitHub Capacity Surge Pushes Microsoft to AWS](https://letsdatascience.com/news/github-capacity-surge-pushes-microsoft-to-aws-13a2ffa4)
