---
title: "smolagents 1.26 : Hugging Face muscle les agents locaux sans usine à gaz"
description: "La version 1.26 de smolagents arrive avec une bibliothèque légère, compatible Ollama, transformers et MCP. Une option intéressante pour agents locaux contrôlables."
pubDate: 2026-05-30
tags: ["smolagents", "Hugging Face", "agents locaux", "MCP", "Ollama"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub — smolagents release v1.26.0"
    url: "https://github.com/huggingface/smolagents/releases/tag/v1.26.0"
  - label: "GitHub — huggingface/smolagents"
    url: "https://github.com/huggingface/smolagents"
  - label: "Hugging Face Docs — smolagents"
    url: "https://huggingface.co/docs/smolagents/en/index"
  - label: "Hugging Face Blog — Introducing smolagents"
    url: "https://huggingface.co/blog/smolagents"
---

Hugging Face a publié **smolagents 1.26.0** le 29 mai 2026. La release n’est pas spectaculaire au sens marketing du terme : ajout d’Exa comme moteur possible dans `WebSearchTool`, nettoyage de documentation, mise à jour de tests, suppression du `Remote WasmExecutor`. Mais elle arrive au bon moment, parce que `smolagents` incarne une tendance importante pour l’IA locale : construire des agents utiles avec peu d’abstraction, compatibles avec des modèles locaux, et capables de consommer des outils MCP.

Le projet n’est pas nouveau. Hugging Face l’a présenté fin 2024 comme une bibliothèque minimaliste pour créer des agents dont les actions sont écrites en code. Mais en 2026, l’intérêt change d’échelle : entre Ollama, transformers, MCP, les serveurs locaux et les runtimes open-weight, on a enfin les briques pour faire tourner des agents personnels sans envoyer chaque étape à un fournisseur cloud.

## Ce que contient vraiment la version 1.26

La release officielle `v1.26.0` liste plusieurs changements modestes mais concrets. Le plus visible côté fonctionnalité est l’ajout d’**Exa** comme option de moteur dans `WebSearchTool`. Ce n’est pas une révolution, mais c’est cohérent avec l’usage agentique : un agent a souvent besoin de chercher, lire, filtrer et citer.

La release supprime aussi le **Remote WasmExecutor**. Ce point est moins sexy, mais il touche à un sujet central : l’exécution de code par agents. Quand une bibliothèque permet à un modèle d’écrire et d’exécuter du Python, la surface d’attaque devient réelle. `smolagents` documente plusieurs modes d’exécution sandboxée, notamment Docker, E2B, Modal et Blaxel. Le message implicite est sain : un agent qui exécute du code doit être isolé. Sinon, ce n’est pas un agent, c’est une invitation polie à l’incident.

Les autres changements de 1.26 concernent surtout des tests LiteLLM, des docstrings, des corrections de typos et de sérialisation. Rien qui justifie une migration paniquée. Mais la release confirme que le projet est maintenu, et c’est exactement ce qu’on attend d’une brique d’infrastructure pour agents.

## Pourquoi smolagents est intéressant pour le local

La documentation officielle présente `smolagents` comme une bibliothèque open-source Python pour construire et lancer des agents en quelques lignes. Sa particularité : le **CodeAgent**. Au lieu de demander au modèle de produire uniquement des appels d’outils JSON, l’agent peut exprimer ses actions comme du code Python exécutable.

Ce choix a des avantages pratiques. Le code sait gérer des boucles, des conditions, des calculs intermédiaires, des transformations de données, et des appels de fonctions composables. Pour certains workflows — analyse de fichiers, extraction structurée, RAG maison, manipulation de tableaux, appels API internes — c’est souvent plus naturel qu’une succession de tool calls JSON verbeux.

La contrepartie est évidente : exécuter du code généré par un LLM exige un cadre strict. En local, il faut au minimum un environnement isolé, des permissions limitées, pas de secrets dans le contexte, et une politique claire sur les fichiers accessibles. L’agent local a beau ne pas traverser Internet, il peut quand même supprimer le mauvais dossier avec une confiance admirable. La bêtise automatisée reste automatisée.

## Compatibilité : Ollama, transformers, MCP

Pour notre sujet — l’IA locale — le point fort est la compatibilité. Le README et la documentation indiquent que `smolagents` peut utiliser des modèles via plusieurs backends : Hugging Face inference providers, OpenAI, Anthropic, LiteLLM, mais aussi **transformers en local** et **Ollama**.

Cela ouvre une architecture simple : un modèle open-weight servi par Ollama ou chargé avec transformers, un agent `smolagents`, des outils exposés localement, et éventuellement un serveur MCP pour standardiser l’accès aux ressources. La documentation mentionne explicitement la capacité à utiliser des outils venant de **n’importe quel serveur MCP**, des outils LangChain, des Spaces Hugging Face ou du code Python custom.

MCP est important ici parce qu’il sépare l’agent des outils. Au lieu de recoder un connecteur différent pour chaque framework, on peut exposer une base de documents, un dépôt Git, un calendrier, un navigateur ou une API interne via un protocole commun. Dans un contexte auto-hébergé, c’est une bonne nouvelle : moins de colle propriétaire, plus de composants remplaçables.

## Minimalisme contre frameworks lourds

Le positionnement de `smolagents` est volontairement petit. La documentation indique que la logique agentique tient autour d’un millier de lignes de code, avec des abstractions minimales au-dessus de Python. Ce n’est pas un argument suffisant en soi — petit ne veut pas dire correct — mais c’est une direction intéressante face aux frameworks agentiques tentaculaires.

Pour un agent local, la simplicité a une valeur opérationnelle. On veut comprendre ce que l’agent peut faire, où il stocke sa mémoire, comment il appelle les outils, comment il exécute le code, et comment il échoue. Une pile trop magique devient difficile à auditer. Dans un environnement personnel ou PME, c’est souvent plus dangereux qu’utile.

Le blog de lancement de Hugging Face insistait déjà sur une idée saine : il ne faut pas utiliser un agent quand un workflow déterministe suffit. C’est presque anti-marketing, donc probablement bon signe. Si ta tâche se résume à “chercher dans une base documentaire et répondre”, un RAG classique peut suffire. Si le flux dépend vraiment de décisions successives, d’outils variés et d’un état intermédiaire, un agent devient plus défendable.

## Un exemple d’architecture locale réaliste

Un setup raisonnable pourrait ressembler à ceci : Ollama sert un modèle de code ou de raisonnement quantifié ; `smolagents` orchestre la boucle agentique ; Docker isole l’exécution Python ; un serveur MCP expose un dossier de notes, un dépôt Git ou une base SQLite ; les sorties de l’agent sont validées par tests ou par revue humaine.

Ce n’est pas glamour, mais c’est robuste. Et surtout, chaque brique peut être remplacée. Le modèle local peut changer. Ollama peut être remplacé par vLLM ou transformers selon la machine. MCP évite de lier trop fortement les outils au framework. Docker limite les dégâts. Les tests empêchent l’agent de prendre ses rêves pour une CI verte.

## Les limites actuelles

Il faut éviter de sur-vendre. `smolagents` ne transforme pas un petit modèle local en ingénieur autonome. La qualité dépend fortement du modèle, du prompt système, des outils disponibles, de l’isolation, de la mémoire et des garde-fous. Les modèles locaux de taille raisonnable peuvent très bien gérer des tâches courtes et structurées, mais peinent encore souvent sur des plans longs, ambigus ou multi-fichiers.

La compatibilité MCP est prometteuse, mais elle déplace aussi le problème : un mauvais serveur MCP, trop permissif ou mal documenté, peut rendre l’agent fragile. La standardisation ne remplace pas la conception. Elle rend juste les erreurs plus portables, ce qui est pratique mais légèrement inquiétant.

## Verdict

`smolagents 1.26` n’est pas une release qui change tout du jour au lendemain. C’est plutôt une confirmation : Hugging Face maintient une bibliothèque agentique légère, compatible avec Ollama, transformers et MCP, qui colle bien à l’esprit local-first.

Pour un labo personnel, un développeur indépendant ou une équipe qui veut expérimenter des agents auto-hébergés, c’est une option sérieuse à tester. Pas parce qu’elle promet l’autonomie totale. Parce qu’elle garde la pile lisible, contrôlable, et suffisamment flexible pour brancher des modèles open-weight. Dans le monde des agents, c’est déjà presque une vertu monastique.

## Sources

- [GitHub — smolagents release v1.26.0](https://github.com/huggingface/smolagents/releases/tag/v1.26.0)
- [GitHub — huggingface/smolagents](https://github.com/huggingface/smolagents)
- [Hugging Face Docs — smolagents](https://huggingface.co/docs/smolagents/en/index)
- [Hugging Face Blog — Introducing smolagents](https://huggingface.co/blog/smolagents)
