---
title: "Ollama branche Hermes Desktop : l’agent local sort enfin du terminal"
description: "Ollama documente une intégration directe avec Hermes Desktop : un lancement en une commande pour utiliser un agent Nous Research avec des modèles locaux ou cloud."
pubDate: 2026-06-10
tags: ["Ollama", "Hermes", "agents", "local-first", "self-hosting"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Ollama — Hermes Desktop integration"
    url: "https://docs.ollama.com/integrations/hermes-desktop"
  - label: "Hermes Agent — documentation officielle"
    url: "https://hermes-agent.nousresearch.com/docs"
  - label: "Nous Research — hermes-agent sur GitHub"
    url: "https://github.com/NousResearch/hermes-agent"
  - label: "Ollama — blog et historique des intégrations"
    url: "https://ollama.com/blog"
---

Ollama a ajouté une intégration documentée pour **Hermes Desktop**, l’application native de Nous Research qui sert d’interface graphique à Hermes Agent. Le signal intéressant n’est pas seulement “encore une app de chat”. La documentation Ollama décrit un chemin très court : `ollama launch hermes-desktop`, puis Ollama gère l’installation éventuelle, le choix du modèle, la configuration et le lancement de l’application. Pour l’IA locale, c’est un détail qui compte : l’écosystème commence à traiter les agents comme des applications utilisables, pas comme des piles de variables d’environnement posées sur un autel.

La page officielle d’Ollama présente Hermes Desktop comme une application native capable de piloter Hermes Agent avec des modèles, des outils, des projets, de la mémoire, des skills et des passerelles de messagerie. Elle indique aussi que la commande peut être relancée pour changer de modèle. Ce n’est donc pas une simple entrée de menu : c’est une tentative de rendre la connexion entre runtime local et agent persistant suffisamment banale pour être adoptée par des utilisateurs qui ne veulent pas maintenir une intégration maison.

## Ce que fait réellement `ollama launch hermes-desktop`

D’après la documentation Ollama, la commande suit quatre étapes : installation si Hermes Desktop n’est pas présent, sélection d’un modèle, configuration de l’application pour utiliser le modèle Ollama choisi, puis lancement. Une variante permet de lancer directement avec `ollama launch hermes-desktop --model <model>`. Le point pratique est clair : Ollama devient le point d’entrée pour raccorder un modèle local à une interface agentique complète.

Il faut rester précis. Ollama ne transforme pas magiquement n’importe quel modèle en agent fiable. Le modèle choisi garde ses limites : contexte, tool-use, qualité de raisonnement, capacité à respecter des contraintes, coût mémoire, latence. Mais la friction d’installation baisse. Et dans l’auto-hébergement, la friction est souvent ce qui tue les bonnes architectures avant même le premier benchmark.

Cette intégration s’inscrit dans une stratégie plus large d’Ollama. Son blog récent montre déjà une poussée vers `ollama launch`, les assistants de code, Claude Code, Codex CLI, OpenJarvis, les modèles cloud optionnels, MLX sur Apple Silicon et le retour du GGUF via llama.cpp dans Ollama 0.30. Hermes Desktop ajoute une pièce différente : pas seulement coder dans un dépôt, mais faire tourner un agent généraliste doté de mémoire et de compétences réutilisables.

## Hermes Agent : mémoire, skills et exécution persistante

La documentation officielle de Hermes Agent présente le projet comme un agent autonome “self-improving” : il crée des skills à partir de l’expérience, améliore ces skills pendant l’usage, conserve de la mémoire entre sessions et peut fonctionner au-delà d’une simple fenêtre de chat. Le dépôt GitHub de Nous Research est sous licence MIT et décrit un agent capable de tourner localement, sur VPS, en Docker, en SSH, sur Modal ou Daytona, avec des passerelles vers Telegram, Discord, Slack, WhatsApp, Signal, Email et CLI.

Pour un lecteur de Labo IA Locale, l’élément le plus important est la séparation entre **runtime de modèle** et **runtime d’agent**. Ollama sert le modèle. Hermes gère la boucle agentique : outils, mémoire, skills, sessions, automations, exécution dans un terminal ou un backend distant. Cette séparation est saine. Elle évite de confondre “j’ai un LLM local” avec “j’ai un agent utilisable”. Le premier répond à des prompts. Le second doit planifier, appeler des outils, se souvenir, corriger ses erreurs, et surtout ne pas détruire le mauvais dossier à 2 h du matin. Petit détail, mais les détails ont un casier judiciaire.

Le dépôt Hermes indique aussi une compatibilité avec de nombreux fournisseurs de modèles : Nous Portal, OpenRouter, Novita, NVIDIA NIM, Hugging Face, OpenAI ou endpoints personnels. L’intégration Ollama est donc une voie local-first parmi d’autres, pas un enfermement. C’est utile si l’on veut basculer entre un petit modèle local pour les tâches simples et un modèle distant pour les opérations plus lourdes.

## Pourquoi c’est important pour l’auto-hébergement

Les agents locaux ont longtemps souffert d’un problème simple : ils étaient puissants sur le papier, mais pénibles à installer et à maintenir. Il fallait choisir un modèle, un serveur d’inférence, un format de quantization, une interface, une politique d’outils, une mémoire, parfois un scheduler et une messagerie. Chaque brique fonctionnait séparément ; l’ensemble ressemblait vite à un labyrinthe avec des logs.

Avec `ollama launch hermes-desktop`, Ollama tente de réduire ce câblage pour le cas courant : un utilisateur a Ollama, veut lancer un agent desktop, et souhaite utiliser un modèle local ou cloud sans bricoler la configuration. C’est exactement le type d’intégration qui peut faire passer les agents auto-hébergés d’un public de bidouilleurs à un public de développeurs, d’équipes internes et d’utilisateurs avancés.

La limite reste la sécurité. Un agent avec outils, mémoire et accès projet doit être traité comme un processus capable d’agir, pas comme un chatbot décoratif. La documentation Hermes mentionne des sujets de sécurité, d’autorisations, d’isolation et de backends d’exécution. En pratique, il faut commencer avec des modèles prudents, des répertoires de test, des permissions limitées et des validations humaines sur les commandes destructrices. L’IA locale protège la confidentialité des prompts, mais elle ne protège pas automatiquement contre les mauvaises actions locales.

## Ce qu’il faut surveiller

Trois points méritent des tests indépendants. D’abord, la qualité du tool-use avec des modèles locaux modestes : un agent desktop n’a de valeur que si le modèle suit correctement les appels d’outils. Ensuite, la mémoire : utile si elle est précise, dangereuse si elle accumule des conclusions fausses. Enfin, la portabilité : l’expérience doit rester fluide sur macOS, Windows et Linux, y compris avec des modèles quantifiés et des machines à VRAM limitée.

En l’état, l’intégration Ollama-Hermes Desktop est une bonne nouvelle pragmatique. Elle ne résout pas la fiabilité des agents, mais elle réduit le coût d’entrée pour les tester proprement avec des modèles locaux. C’est souvent comme cela que les vraies piles locales gagnent : moins de promesses métaphysiques, plus de commandes qui marchent.

## Sources

- Ollama — Hermes Desktop integration : https://docs.ollama.com/integrations/hermes-desktop
- Hermes Agent — documentation officielle : https://hermes-agent.nousresearch.com/docs
- Nous Research — hermes-agent sur GitHub : https://github.com/NousResearch/hermes-agent
- Ollama — blog : https://ollama.com/blog
