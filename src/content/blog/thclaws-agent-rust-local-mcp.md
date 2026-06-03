---
title: "thClaws : un agent local en Rust qui prend MCP au sérieux"
description: "Le projet open-source thClaws combine GUI, CLI, mode headless, Ollama local, MCP, skills et équipes d’agents dans un seul binaire Rust."
pubDate: 2026-06-03
tags: ["thclaws", "agents", "rust", "mcp", "ollama", "self-hosting", "local-ai"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub — thClaws repository"
    url: "https://github.com/thClaws/thClaws"
  - label: "thClaws — site officiel"
    url: "https://thclaws.ai/"
  - label: "GitHub — thClaws installation manual"
    url: "https://github.com/thClaws/thClaws/blob/main/user-manual-th/ch02-installation.md"
---

Le paysage des agents IA locaux commence à sortir du duo “chat dans un terminal” et “démo qui modifie trois fichiers avant de s’effondrer”. **thClaws** mérite donc un détour : c’est un **agent harness open-source écrit en Rust**, pensé pour tourner sur ta machine, avec GUI, CLI, mode headless, webapp, support multi-fournisseurs, **MCP**, skills, plugins, équipes d’agents et compatibilité **Ollama**.

Le dépôt GitHub présente thClaws comme un workspace agentique natif Rust : un seul moteur derrière plusieurs interfaces, une configuration portable, des sessions traçables et une logique local-first. Le site officiel insiste sur la même idée : “your machine, your agent”. Ce n’est pas une révolution conceptuelle ; c’est plutôt une tentative sérieuse de mettre de l’ordre dans une zone où beaucoup de projets confondent autonomie et permission de casser ton dépôt.

## Un seul moteur, quatre surfaces

Le README de thClaws décrit quatre modes d’utilisation alimentés par la même boucle `Agent`, les mêmes sessions et le même registre d’outils. D’abord une **GUI desktop** via `thclaws`, avec onglets Terminal, Chat, Files et éventuellement Team. Ensuite une **CLI REPL** avec `thclaws --cli`, utile en SSH ou sur machine headless. Troisième mode : une exécution non interactive avec `thclaws -p "prompt"`, pratique pour scripts et CI. Enfin, un mode **webapp** via `thclaws --serve --port 7878`, exposé en HTTP/WebSocket et tunnelable sans ouvrir un port public.

Cette architecture compte. Beaucoup d’outils agentiques séparent mal l’interface et l’état : ce que tu fais dans le chat n’est pas réutilisable en CLI, le mode batch n’a pas les mêmes outils, l’historique devient opaque. thClaws revendique au contraire des sessions JSONL sous `.thclaws/sessions/`, donc lisibles, versionnables et inspectables. Pour un usage local sérieux, c’est plus important qu’un bouton brillant. Les boutons brillants ont rarement sauvé un audit.

## Local-first, mais pas modèle-local-only

thClaws n’est pas uniquement un wrapper Ollama. Le dépôt liste beaucoup de fournisseurs : Anthropic, OpenAI, Google Gemini/Gemma, Alibaba DashScope/Qwen, DeepSeek, Z.ai, NVIDIA NIM, OpenRouter, Azure AI Foundry, LM Studio, Ollama et un slot générique OpenAI-compatible pour LiteLLM, vLLM ou des proxies internes.

Cela peut sembler contradictoire avec le local-first. En pratique, c’est plutôt sain : un agent local peut garder ses fichiers, sessions, permissions et outils sur la machine tout en alternant entre un modèle local et un modèle cloud selon la tâche. Le point important est que l’infrastructure agentique ne soit pas prisonnière d’un fournisseur. Si tu utilises Ollama avec un modèle local dans l’avion, puis un modèle cloud pour une passe de raisonnement plus lourde, la session et les conventions restent au même endroit.

Le manuel d’installation mentionne explicitement l’usage avec **Ollama** pour fonctionner sans clé API cloud, avec des commandes de pull de modèles locaux. Le README parle aussi d’un mode Ollama natif et Anthropic-compatible. C’est pertinent pour l’écosystème local : beaucoup d’agents attendent un dialecte API particulier, et les modèles locaux ne se comportent pas tous proprement avec le tool calling. Un adaptateur bien placé vaut parfois mieux qu’un nouveau benchmark.

## MCP, AGENTS.md et skills : la portabilité comme principe

Le signal le plus intéressant est peut-être l’insistance sur les standards ouverts. thClaws met en avant le **Model Context Protocol** pour connecter des outils, **AGENTS.md** pour les instructions projet, et des fichiers **SKILL.md** avec frontmatter YAML pour empaqueter des workflows. Le README résume l’objectif : skills, plugins, serveurs MCP et hooks doivent étendre l’agent sans modifier le cœur Rust.

Pour l’auto-hébergement, c’est exactement le bon axe. Les agents locaux ne manquent pas seulement de modèles ; ils manquent de conventions stables. Comment un agent lit-il les règles d’un dépôt ? Comment découvre-t-il les outils autorisés ? Comment partage-t-on un connecteur entre plusieurs clients ? MCP n’est pas magique, mais il remplace une collection de bricolages incompatibles par un protocole identifiable.

thClaws va plus loin en indiquant que les instructions retournées par un serveur MCP lors de l’initialisation peuvent être intégrées au prompt système dans une section dédiée. C’est un détail technique, mais il règle un vrai problème : les outils MCP ne sont pas seulement des fonctions, ils ont souvent des règles d’usage. Si ces règles restent dans une documentation externe, le modèle les ignore au moment précis où il devrait les respecter. Classique. L’agent lit tout, sauf la notice.

## Sécurité : sandbox, approbations et commandes destructives

Le README insiste sur plusieurs garde-fous : sandbox filesystem limité au répertoire de travail, commandes shell destructrices signalées, approbation requise pour les appels d’outils mutatifs sauf configuration d’auto-approval, et demandes de permissions identifiant l’agent concerné lorsqu’il y en a plusieurs.

C’est un point crucial. Un agent local a accès à ce que tu as de plus sensible : code source, clés, fichiers personnels, historique, parfois shell complet. Le fait qu’il tourne “chez toi” ne le rend pas moins dangereux ; cela supprime juste l’intermédiaire cloud. La sécurité d’un agent local se joue donc dans la granularité des permissions, la journalisation et la possibilité de relire les actions.

thClaws n’est pas immunisé contre les problèmes classiques : prompt injection via documents, outil MCP compromis, commande shell trop large, mauvaise interprétation d’une instruction. Mais son positionnement montre au moins qu’il prend ces risques comme des contraintes de conception, pas comme une ligne à ajouter dans une FAQ.

## Rust : distribution et robustesse avant glamour

Le choix de Rust est cohérent avec l’objectif. Un agent harness est une application système : il lance des processus, lit des fichiers, gère des sessions, coordonne des outils, expose éventuellement une interface réseau et doit rester stable. Rust apporte une distribution plus propre qu’un millefeuille Python/Node dans beaucoup de contextes, avec un binaire unique plus facile à installer et à auditer.

Le dépôt GitHub indique une base majoritairement Rust, avec TypeScript pour l’interface. Il affiche aussi une double licence **MIT / Apache-2.0**, ce qui est favorable à l’adoption dans des environnements variés. À la date de l’extraction, le projet revendique de nombreuses releases, un rythme rapide et une communauté encore jeune. Cela signifie deux choses à la fois : l’outil évolue vite, et il faut s’attendre à des changements. Bref, prometteur, pas encore un tournevis Facom transmis par ton grand-père.

## À quoi ça sert concrètement ?

thClaws est intéressant si tu veux un environnement agentique local qui ne soit pas lié à un seul modèle ni à une seule interface. Pour du code, il peut servir de cockpit entre terminal, fichiers, chat et outils. Pour de l’automatisation, le mode `-p` et le mode serveur ouvrent des usages batch ou CI. Pour du self-hosting, le support Ollama et OpenAI-compatible permet de brancher des modèles locaux, tandis que MCP apporte une voie propre vers des outils spécialisés.

Il est moins pertinent si tu veux seulement discuter avec un modèle local. Dans ce cas, Ollama, Open WebUI ou LM Studio suffisent souvent. thClaws vise plus haut : orchestrer actions, mémoire, outils, workflows et équipes d’agents. Plus haut veut aussi dire plus de configuration, plus de surface d’attaque et plus de comportements à tester.

## Verdict provisoire

thClaws coche beaucoup de cases que les agents locaux doivent finir par cocher : **local-first**, sessions lisibles, multi-provider, Ollama, MCP, permissions, sandbox, plusieurs interfaces et packaging open-source. Le projet est jeune et il faudra vérifier sur des tâches réelles : qualité du tool calling avec modèles locaux, robustesse des permissions, stabilité du mode serveur, ergonomie des skills et comportement face aux prompt injections.

Mais la direction est bonne. Le futur de l’agent local ne sera probablement pas un modèle isolé qui parle dans une fenêtre. Ce sera un harness contrôlable, extensible, auditable, capable d’alterner entre local et cloud sans abandonner la souveraineté de l’environnement. thClaws n’a pas encore prouvé qu’il sera ce standard. Il montre en revanche à quoi ce standard devrait ressembler.

## Sources

- [GitHub — thClaws repository](https://github.com/thClaws/thClaws)
- [thClaws — site officiel](https://thclaws.ai/)
- [GitHub — thClaws installation manual](https://github.com/thClaws/thClaws/blob/main/user-manual-th/ch02-installation.md)
