---
title: "TVIR : le benchmark qui demande aux agents de recherche d’arrêter les graphiques décoratifs"
description: "TVIR-Bench évalue les agents Deep Research sur des rapports mêlant texte, images et graphiques sourcés. Une bonne synthèse ne suffit plus si les visuels racontent n’importe quoi."
pubDate: 2026-06-05
category: "veille"
tags: ["agents", "multimodal", "benchmark"]
author: "Veille IA"
draft: false
sources:
  - label: "Article arXiv TVIR"
    url: "https://arxiv.org/abs/2606.02320"
  - label: "Version HTML du papier"
    url: "https://arxiv.org/html/2606.02320"
  - label: "Page projet TVIR"
    url: "https://nju-link.github.io/TVIR/"
---

Les agents de recherche ont beaucoup progressé sur la partie visible du travail : chercher, lire, citer, synthétiser, produire un rapport long et relativement cohérent. Mais il reste une faiblesse très humaine, donc très répandue : ajouter un graphique parce que ça “fait sérieux”, sans vérifier qu’il soutient réellement l’analyse. **TVIR**, pour *Text–Visual Interleaved Report Generation*, attaque précisément ce problème.

Le papier, publié sur arXiv le 1er juin 2026 par une équipe liée à Nanjing University et Alibaba Group, propose à la fois un benchmark et un agent de référence. Son idée centrale est simple : un rapport de recherche professionnel n’est pas seulement du texte avec quelques images posées après coup. Les visuels doivent être des preuves, pas de la décoration PowerPoint. Oui, PowerPoint vient de prendre une balle perdue, mais il l’a cherchée.

## Le problème : les agents Deep Research restent très textuels

Les systèmes de *Deep Research* savent de mieux en mieux orchestrer plusieurs recherches web, produire des plans, comparer des sources et rédiger des analyses longues. Les benchmarks existants évaluent surtout la qualité textuelle : cohérence, profondeur, citations, logique, respect de l’instruction.

TVIR part d’un constat différent : dans de nombreux usages professionnels — finance, politique publique, santé, énergie, tourisme, recherche scientifique — les rapports reposent aussi sur des graphiques, tableaux, images, cartes ou figures. Ces éléments ne sont pas secondaires. Ils structurent la décision, résument des tendances et rendent certains arguments vérifiables.

Or, selon les auteurs, les benchmarks actuels regardent mal trois choses : la factualité des visuels, leur provenance, et leur alignement avec le texte. Un agent peut donc produire un rapport fluide, bien cité, mais accompagné de figures qui ne correspondent pas vraiment aux données ou au raisonnement. C’est le genre de détail qui transforme une synthèse séduisante en instrument de confusion.

## TVIR-Bench : 100 tâches multimodales, pas juste du texte enrichi

TVIR introduit **TVIR-Bench**, un ensemble de **100 tâches de recherche multimodale expert-curated**. La page projet précise une répartition **50 tâches en chinois et 50 en anglais**, couvrant **10 grands domaines** et **3 niveaux de complexité**.

Les tâches ne demandent pas seulement d’insérer une image. Elles exigent que les éléments visuels servent des sous-objectifs analytiques précis. Un graphique doit représenter des données pertinentes ; une image récupérée doit illustrer un point réel ; une légende doit être fidèle ; le texte autour doit expliquer ce que le visuel prouve ou nuance.

Les principes de conception listés sur la page projet sont révélateurs : tâches role-driven, demand-oriented, deep research, frontier-focused et multimodal integration. En clair, le benchmark essaie de reproduire des demandes de rapport plausibles, où l’utilisateur a un rôle, un besoin concret et une attente de synthèse utilisable.

C’est une différence subtile mais importante avec un benchmark multimodal classique. TVIR ne teste pas seulement si un modèle “voit” une image ou génère un graphique. Il teste si un agent peut construire un document où texte et visuels participent à la même argumentation.

## L’évaluation sépare le texte et le visuel

L’autre contribution utile est le cadre d’évaluation en deux chemins : **Textual Assessment** et **Visual Assessment**.

La partie textuelle mesure notamment le support des citations, l’alignement avec l’instruction, la qualité d’écriture, la profondeur analytique, et la cohérence factuelle et logique. Rien de révolutionnaire ici, mais c’est nécessaire.

La partie visuelle est plus intéressante. Elle regarde la qualité des figures, la composition multimodale, la qualité des légendes, l’intégration figure-contexte et la cohérence entre graphiques et sources. La page projet liste notamment les métriques **FQ**, **MC**, **FCQ**, **FCI** et **CSC**. Ce dernier point — *Chart-Source Consistency* — est crucial : un graphique généré par code mais non relié à une source fiable peut être propre visuellement et faux analytiquement. Belle courbe, mauvais monde.

Le papier rapporte des expériences sur **neuf systèmes de Deep Research**. La version arXiv indique que **TVIR-Agent** obtient de bons résultats globaux et que les variantes de l’agent dominent plusieurs agrégats. Elle note aussi un cas révélateur : certains systèmes orientés recherche textuelle ne peuvent pas être évalués sur les dimensions visuelles lorsqu’ils produisent des rapports uniquement textuels. Cela souligne le point de fond : la recherche multimodale ne se résume pas à une option cosmétique.

## TVIR-Agent : un pipeline explicite pour les rapports multimodaux

TVIR ne se contente pas de proposer un benchmark. Les auteurs présentent aussi **TVIR-Agent**, un framework hiérarchique multi-agent destiné à produire des rapports text-visuel interleavés.

La version arXiv décrit plusieurs modules : un planificateur, un module d’instanciation d’assets visuels, un writer et un polisher. La logique est assez saine : d’abord comprendre la tâche et construire le plan ; ensuite récupérer ou produire les éléments visuels nécessaires ; puis rédiger le rapport en tenant compte du contexte ; enfin harmoniser et corriger.

Ce qui compte ici, c’est l’ordre des opérations. Beaucoup de systèmes génèrent d’abord le texte puis ajoutent des visuels. TVIR pousse une approche où les figures font partie du raisonnement dès le départ. Les graphiques doivent venir avec des sources traçables ; les images doivent être sélectionnées pour une fonction analytique ; la rédaction doit intégrer ces éléments au fil du rapport.

C’est exactement ce qu’on attendrait d’un analyste humain sérieux : ne pas coller un graphique après l’avoir trouvé joli, mais l’utiliser parce qu’il répond à une question.

## Pourquoi c’est important pour l’IA agentique

La tendance “Deep Research” est en train de devenir un produit standard : assistants de recherche, agents de veille, copilotes stratégiques, outils d’analyse marché. À mesure que ces systèmes se diffusent, la qualité des rapports ne peut plus être évaluée uniquement au style ou au nombre de citations.

Un rapport peut être dangereux tout en étant bien écrit. Un graphique mal sourcé peut amplifier une erreur plus vite qu’un paragraphe vague, parce qu’un visuel donne une impression d’évidence. TVIR remet donc l’évaluation au bon endroit : l’agent doit produire un artefact multimodal vérifiable.

Pour les éditeurs de systèmes agents, cela implique plusieurs exigences : tracer les sources de données utilisées pour les figures, vérifier automatiquement les légendes, relier chaque visuel à une sous-question, et mesurer l’alignement entre texte et image. Ce n’est pas glamour, mais c’est la différence entre un agent utile et un générateur de rapports impressionnants mais fragiles.

## Les limites à garder en tête

TVIR-Bench reste un benchmark académique de 100 tâches. C’est suffisant pour structurer une comparaison, pas pour couvrir toute la diversité des rapports professionnels. Les résultats dépendent aussi du juge utilisé, des prompts, du budget de recherche et des outils disponibles. Le papier mentionne une évaluation LLM-based pour certaines dimensions ; comme toujours, cela introduit une couche de jugement automatisé qu’il faut interpréter avec prudence.

Il faut aussi distinguer deux capacités : générer un rapport multimodal convaincant et garantir la vérité de toutes les données sous-jacentes. TVIR améliore l’évaluation de la cohérence et de la traçabilité, mais il ne transforme pas magiquement les agents en auditeurs statistiques.

## Ce qu’il faut retenir

TVIR met le doigt sur un angle mort important : les agents de recherche ne doivent pas seulement bien écrire, ils doivent aussi bien montrer. Et “bien montrer” signifie : source claire, figure pertinente, légende fidèle, intégration au raisonnement.

À court terme, ce benchmark servira surtout à comparer des architectures d’agents Deep Research. À moyen terme, il pointe vers une exigence plus large : les rapports générés par IA devront être évalués comme des documents multimodaux complets. Le texte flatteur ne suffira plus à masquer les graphiques creux. Bonne nouvelle : c’est précisément comme ça qu’on rend ces systèmes moins impressionnants en démo, mais plus fiables au travail.

## Sources

- [TVIR sur arXiv](https://arxiv.org/abs/2606.02320)
- [Version HTML du papier](https://arxiv.org/html/2606.02320)
- [Page projet TVIR](https://nju-link.github.io/TVIR/)
