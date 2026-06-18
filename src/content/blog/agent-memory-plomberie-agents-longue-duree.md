---
title: "Agent Memory : les agents longue durée ont surtout un problème de plomberie"
description: "Un papier arXiv caractérise dix systèmes de mémoire pour agents LLM et montre que l’accuracy seule masque des écarts massifs de coût, latence, énergie et maintenance."
pubDate: 2026-06-07
category: "veille"
tags: ["agents", "mémoire", "systèmes"]
author: "Veille IA"
draft: false
sources:
  - label: "Article arXiv — Agent Memory"
    url: "https://arxiv.org/abs/2606.06448"
  - label: "Version HTML arXiv"
    url: "https://arxiv.org/html/2606.06448v1"
  - label: "Liste arXiv cs.AI récente"
    url: "https://arxiv.org/list/cs.AI/recent"
---

Les agents IA longue durée ont une promesse séduisante : garder le fil pendant des jours, des semaines, parfois des mois. Se souvenir d’un projet, d’un utilisateur, d’un historique d’outils, d’une base documentaire mouvante. En pratique, cette promesse se heurte à une question beaucoup moins glamour : **où met-on la mémoire, combien coûte-t-elle à construire, et combien de temps faut-il pour la relire ?**

Un papier arXiv publié le 4 juin, **“Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads”**, met enfin des chiffres sur ce problème. Les auteurs — Yasmine Omri, Ziyu Gan, Zachary Broveak, Robin Geens, Zexue He, Alex Pentland, Marian Verhelst, Tsachy Weissman et Thierry Tambe — ne proposent pas seulement un nouveau module mémoire. Ils caractérisent dix systèmes représentatifs et montrent que l’évaluation des agents par simple score de réponse est insuffisante. Deux systèmes peuvent avoir une accuracy proche et pourtant différer par des ordres de grandeur en coût de construction, latence, énergie ou empreinte de stockage.

C’est le genre de papier qui ne fait pas rêver les slides produit, mais qui décide si un agent peut tenir en production. La mémoire, comme souvent en informatique, devient intéressante au moment où elle casse.

## La mémoire d’agent n’est pas juste du RAG

Le papier formule une idée utile : la mémoire d’agent généralise le RAG. Le RAG classique indexe un corpus relativement statique et récupère des passages pertinents. La mémoire d’un agent, elle, doit gérer un **état mutable** : conversations, traces d’outils, décisions précédentes, préférences, faits obsolètes, contradictions, résumés, oublis et mises à jour.

Les auteurs découpent le pipeline en plusieurs phases : ingestion, construction de mémoire, stockage, retrieval, assemblage du prompt, génération, puis maintenance. Cette séparation est importante, car elle évite de tout réduire à la qualité de la réponse finale. Dans un agent réel, le coût d’écriture peut être plus déterminant que le coût de lecture. Construire une mémoire riche à chaque interaction peut sembler intelligent sur un benchmark court ; à l’échelle d’un million d’utilisateurs, cela ressemble vite à une chaudière à tokens.

Le papier compare quatre grandes familles. D’abord la mémoire **long-context**, où l’on remet tout l’historique dans le prompt. Simple, mais le coût de pré-remplissage grimpe avec l’historique. Ensuite le **flat RAG**, avec BM25 ou embeddings, qui indexe des morceaux de conversation sans trop de magie. Puis les systèmes **structure-augmented RAG**, comme GraphRAG ou HippoRAG v2, qui ajoutent des graphes, des structures ou des vues multiples. Enfin les approches à **contrôle agentique**, où le modèle décide lui-même d’écrire, de rechercher ou de modifier des mémoires via des outils.

## Dix systèmes, et aucun vainqueur universel

L’évaluation s’appuie notamment sur un workload LongMemEval : cinq historiques d’environ **360 000 tokens** chacun, avec **300 requêtes** au total. Les auteurs standardisent autant que possible l’environnement, tout en reconnaissant qu’une comparaison parfaitement “apples-to-apples” est difficile : chaque système expose ses propres choix d’implémentation, de modèle, d’index et de récupération.

Les systèmes comparés incluent notamment **BM25**, **embedRAG**, **GraphRAG**, **HippoRAG v2**, **Mem0**, **SimpleMem**, **A-Mem**, **Letta** et **MIRIX**, en plus d’un baseline long-context. Le résultat principal tient en une phrase : **aucun système ne gagne sur tous les axes**.

BM25, par exemple, ressort comme un baseline brutalement efficace. Dans le tableau récapitulatif sur LongMemEval avec Qwen3-32B et 300 requêtes, BM25 atteint **47,0 %** d’accuracy, pour **16,3 minutes** de temps total, **300 appels**, **582 kJ** et environ **4 128 joules par réponse correcte**. GraphRAG est très proche en accuracy (**46,0 %**), mais demande **1,83 heure**, **3 215 appels** et **2 082 kJ**. HippoRAG v2 obtient **44,3 %**, avec **44,2 minutes** et **1 339 kJ**.

Les systèmes plus agentiques ou LLM-heavy ne sont pas automatiquement meilleurs. **A-Mem** atteint **42,7 %**, mais avec **11,76 heures**, **19 230 appels** et **14 864 kJ**. **Letta** est encore plus coûteux dans ce protocole : **27,7 %** d’accuracy, **14,36 heures**, **18 394 appels** et **15 429 kJ**. Ces chiffres ne signifient pas que Letta ou A-Mem seraient “mauvais” partout ; ils disent que sur ce workload et cette configuration, la sophistication de la mémoire peut se payer très cher sans bénéfice proportionnel sur la réponse finale.

Le point est délicieusement inconfortable : parfois, le vieux retrieval lexical fait moins de bruit et rend plus de service. BM25, ce couteau suisse que personne ne met sur les posters, continue de se présenter aux réunions avec un tableur et des résultats.

## Le vrai coût se cache dans la construction

Un des messages forts du papier est que la **construction** de mémoire domine souvent le cycle de vie. Les systèmes qui extraient des faits, résument, construisent des graphes ou laissent un LLM orchestrer les écritures déplacent une partie du coût hors du moment de la requête. Pour l’utilisateur final, la réponse peut sembler acceptable ; pour l’infrastructure, le coût a simplement été payé ailleurs.

C’est un problème de production classique. Si la construction est synchrone, elle ajoute de la latence visible. Si elle est asynchrone, elle crée un compromis fraîcheur-latence : la mémoire peut ne pas refléter les dernières interactions. Si elle est trop agressive, elle consomme du compute et de l’énergie pour stocker des faits qui ne seront jamais relus. Si elle est trop légère, l’agent oublie ou récupère mal.

Les auteurs insistent aussi sur la maintenance, souvent faible ou absente. Une mémoire append-only finit par accumuler du bruit, des doublons et des faits périmés. Pour un assistant personnel, c’est gênant. Pour un agent d’entreprise qui prend des décisions à partir d’un état métier, c’est franchement dangereux. La mémoire doit oublier, compacter, résoudre les conflits, dater les faits et gérer la fraîcheur. Autrement dit : elle ressemble moins à un bloc-notes magique qu’à une base de données vivante.

## Pourquoi l’accuracy seule trompe les benchmarks d’agents

Le papier tape juste sur un biais courant : classer les agents uniquement par qualité de réponse finale revient à ignorer le système qui rend cette réponse possible. Pour un modèle de chat isolé, l’accuracy est déjà réductrice. Pour un agent longue durée, elle devient presque trompeuse.

Un bon benchmark de mémoire devrait inclure au minimum la qualité de réponse, le temps de construction, la latence de requête, l’énergie, le nombre d’appels modèle, l’empreinte de stockage, la croissance par utilisateur et les queues de latence. Les auteurs soulignent que certains systèmes peuvent avoir des latences avec des queues épaisses, où le p95 devient beaucoup plus élevé que la médiane. En production, ce sont souvent ces queues qui font tomber l’expérience utilisateur, pas la jolie moyenne.

Cette lecture rejoint ce que l’on observe dans les agents de code, les assistants de recherche et les systèmes MCP : l’intelligence apparente dépend de plus en plus d’une couche d’orchestration, de mémoire et d’outils. Évaluer uniquement le modèle revient à noter un pilote sans regarder l’avion, la météo, le carburant et le contrôle aérien.

## Les implications pour les builders

Pour les équipes qui construisent des agents, le papier pousse vers une approche plus sobre. D’abord, commencer par des baselines simples. BM25 ou un RAG plat ne sont pas élégants, mais ils donnent un point de comparaison solide. Ensuite, séparer explicitement les budgets de lecture et d’écriture. Un système qui écrit beaucoup doit justifier cette dépense par un gain mesurable sur des requêtes futures.

Ensuite, traiter la construction comme un pipeline d’infrastructure : batch, priorités, admission control, compaction, validation, politiques de fraîcheur. La mémoire ne doit pas être seulement une fonctionnalité produit, mais un sous-système avec ses propres SLO. Enfin, mesurer la croissance par utilisateur. Un agent qui marche sur 10 sessions de démo peut devenir ingérable quand chaque utilisateur accumule des mois d’historique.

## Le signal à retenir

Ce papier ne dit pas que la mémoire d’agent est une mauvaise idée. Il dit qu’elle est un problème de systèmes, pas seulement de prompt engineering. Les agents longue durée auront besoin de mémoire persistante, mais toutes les mémoires ne se valent pas, et les plus sophistiquées ne sont pas automatiquement les plus efficaces.

La conclusion pratique est simple : avant d’ajouter un graphe, un agent de maintenance et trois couches de résumé, mesurez BM25. Il ne sera peut-être pas assez bon. Mais s’il l’est, il vous épargnera quelques mégajoules et une belle collection de migraines distribuées.

## Sources

- Article arXiv — “Agent Memory: Characterization and System Implications of Stateful Long-Horizon Workloads” : https://arxiv.org/abs/2606.06448
- Version HTML arXiv : https://arxiv.org/html/2606.06448v1
- Liste arXiv cs.AI récente : https://arxiv.org/list/cs.AI/recent
