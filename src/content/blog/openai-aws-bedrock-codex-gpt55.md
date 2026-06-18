---
title: "OpenAI arrive en GA sur Bedrock : GPT-5.5, GPT-5.4 et Codex entrent dans la plomberie AWS"
description: "AWS rend les modèles OpenAI et Codex généralement disponibles dans Bedrock : moins une release de modèle qu’un basculement d’infrastructure pour l’IA agentique en entreprise."
pubDate: 2026-06-02
category: "veille"
tags: ["OpenAI", "AWS", "agents", "Codex"]
author: "Veille IA"
draft: false
sources:
  - label: "AWS News Blog — Get started with OpenAI GPT-5.5, GPT-5.4 models, and Codex on Amazon Bedrock"
    url: "https://aws.amazon.com/blogs/aws/get-started-with-openai-gpt-5-5-gpt-5-4-models-and-codex-on-amazon-bedrock/"
  - label: "AWS What's New — GPT-5.5, GPT-5.4, and Codex from OpenAI generally available on Amazon Bedrock"
    url: "https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-openai-models-codex-generally-available/"
  - label: "OpenAI — OpenAI models, Codex, and Managed Agents come to AWS"
    url: "https://openai.com/index/openai-on-aws/"
---

OpenAI n’a pas seulement annoncé une nouvelle case dans un sélecteur de modèles. Le 1er juin 2026, AWS a rendu **GPT-5.5, GPT-5.4 et Codex généralement disponibles dans Amazon Bedrock**. La nuance est importante : on ne parle pas ici d’un benchmark spectaculaire ou d’une architecture inédite, mais d’un changement de distribution. Les modèles OpenAI entrent dans l’environnement AWS avec les contrôles, la facturation et les chemins de déploiement que beaucoup de grandes entreprises utilisent déjà.

C’est moins glamour qu’une démo vidéo. C’est aussi probablement plus structurant. Les agents ne se déploient pas dans les slides, hélas ; ils finissent dans des comptes cloud, des politiques IAM, des journaux d’audit, des contraintes de résidence des données et des engagements de dépense déjà négociés.

## Ce qui devient disponible

AWS annonce la disponibilité générale de **GPT-5.5**, **GPT-5.4** et **Codex** sur Amazon Bedrock. Selon AWS, GPT-5.5 est positionné comme le modèle OpenAI le plus capable, avec des usages ciblés en **coding agentique**, analyse de données et tâches autonomes multi-étapes. GPT-5.4 est présenté comme l’option davantage orientée **prix-performance** pour des charges de production à grande échelle.

Les modèles GPT passent par l’**OpenAI Responses API** exposée dans Bedrock. AWS précise que, depuis la mise à jour du 1er juin, les modèles GPT supportent uniquement cette API sur Bedrock, avec un support console annoncé comme à venir. Ce détail technique compte : les entreprises qui ont déjà standardisé leurs appels autour des APIs Bedrock devront intégrer un modèle d’appel OpenAI-compatible plutôt qu’un simple schéma Bedrock classique.

Codex, de son côté, peut être configuré pour router son inférence via Bedrock. AWS liste les interfaces suivantes : **Codex App**, **Codex CLI**, et intégrations IDE pour **Visual Studio Code**, **JetBrains** et **Xcode**. OpenAI décrit Codex comme son “frontier coding harness and product suite”, utilisé pour écrire, refactorer, déboguer, tester et valider du code sur de grandes bases.

## Pourquoi c’est important pour les entreprises

L’intérêt principal tient dans une phrase sèche mais décisive : l’usage peut s’intégrer aux contrôles existants d’AWS. AWS met en avant la sécurité, la gouvernance, les opérations, la haute disponibilité et la résidence régionale des données. Le blog AWS indique que le traitement reste dans la région Bedrock sélectionnée pour les clients ayant des exigences de résidence des données.

Autre point très concret : **la tarification correspond aux tarifs OpenAI first-party**, et l’usage compte dans les engagements AWS existants. Pour une entreprise déjà liée à AWS par un cloud commit massif, c’est une différence budgétaire immédiate. Elle peut consommer OpenAI à travers une ligne d’achat et un cadre opérationnel déjà acceptés, plutôt que de créer un nouveau circuit fournisseur.

Cela ne rend pas les modèles meilleurs. Cela les rend plus faciles à acheter, contrôler et déployer. Dans le monde enterprise, c’est souvent ce qui décide du passage du prototype au produit. Personne n’aime l’admettre, mais le procurement bat parfois le benchmark — vilainement, mais régulièrement.

## Bedrock comme couche de normalisation agentique

Le signal le plus intéressant est peut-être l’intégration de Codex et des agents managés. Dans son annonce initiale d’avril, OpenAI parlait déjà de trois axes : modèles OpenAI sur AWS, Codex sur AWS et **Amazon Bedrock Managed Agents powered by OpenAI**. Le message est clair : AWS veut être la couche d’exécution des workflows agentiques, pas seulement un catalogue de modèles.

Bedrock Managed Agents prend en charge une partie de la plomberie : orchestration, usage d’outils, déploiement, gouvernance et intégration avec les contrôles de sécurité AWS. Pour les agents de production, ce sont les vrais points de friction. Un agent qui sait raisonner mais ne sait pas être surveillé, limité, audité ou coupé proprement n’est pas un produit ; c’est une expérience de laboratoire avec une carte corporate.

L’arrivée de Codex dans ce cadre est particulièrement significative. Les coding agents sont parmi les premiers agents à produire une valeur mesurable : ils lisent des dépôts, modifient du code, lancent des tests, ouvrent des pull requests. Mais ce sont aussi des agents qui touchent au système nerveux logiciel de l’entreprise. Les faire passer par Bedrock permet d’appliquer des contrôles d’accès, des politiques réseau et une traçabilité plus proches des exigences internes.

## Ce que l’annonce ne dit pas

Il faut rester prudent sur les claims de performance. AWS et OpenAI décrivent GPT-5.5 comme adapté aux tâches complexes, au raisonnement et au coding agentique, mais cette annonce ne fournit pas de nouveaux benchmarks indépendants. Elle ne prouve donc pas que GPT-5.5 dépasse Claude, Gemini ou Grok dans un scénario donné. Elle prouve que GPT-5.5 et GPT-5.4 sont désormais disponibles dans une voie de production AWS.

Même prudence côté Codex. OpenAI indique que plus de 4 millions de personnes utilisent Codex chaque semaine dans son annonce d’avril, et AWS reprend l’idée d’un agent de coding utilisable à grande échelle. Mais les performances réelles dépendront encore du dépôt, des permissions, du harness, des tests disponibles et des garde-fous humains. Un agent qui a accès à un repo sans suite de tests sérieuse reste un stagiaire très rapide dans une pièce sombre.

Il manque aussi, pour l’instant, des détails publics fins sur les garanties opérationnelles : latence observée par région, limites de débit, disponibilité régionale exhaustive, comportement sur très longues sessions Codex, ou coûts complets avec outils et orchestration. AWS renvoie vers sa documentation de compatibilité régionale et ses pages de prix pour les détails pratiques.

## Le vrai mouvement : la guerre des clouds pour les modèles frontier

Cette disponibilité générale confirme une tendance : les modèles frontier deviennent des composants cloud distribués par les grands hyperscalers. AWS ne veut pas laisser Azure capter seul la demande enterprise autour d’OpenAI. OpenAI, de son côté, gagne un accès direct aux clients AWS sans leur demander de sortir de leurs cadres de sécurité et de dépense.

Pour les utilisateurs, le bénéfice est simple : plus de choix. Pour le marché, c’est une étape de consolidation. Les laboratoires IA restent ceux qui entraînent les modèles ; les hyperscalers deviennent les routes de déploiement, les guichets d’achat et les couches de contrôle. Dans l’IA agentique, cette couche compte autant que le modèle, parce qu’un agent utile est un agent connecté à des systèmes réels.

Le résultat : GPT-5.5 et Codex ne gagnent pas une médaille aujourd’hui. Ils gagnent un badge d’accès à l’infrastructure AWS de production. Moins spectaculaire, mais dans les entreprises, c’est souvent la porte qu’il fallait ouvrir.
