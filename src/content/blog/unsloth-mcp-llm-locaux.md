---
title: "Unsloth branche MCP sur les LLM locaux : utile, mais à verrouiller"
description: "Unsloth publie un guide pour connecter des serveurs MCP à des modèles locaux comme Qwen ou Gemma via Unsloth Studio et llama.cpp. Une avancée pratique pour les agents privés, avec quelques garde-fous indispensables."
pubDate: 2026-06-02
tags: ["unsloth", "mcp", "agents", "llama.cpp", "qwen", "gemma", "self-hosting", "local-ai"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Unsloth Documentation — How to Use MCP Servers with Local LLMs"
    url: "https://unsloth.ai/docs/basics/mcp"
  - label: "GitHub — unslothai/unsloth"
    url: "https://github.com/unslothai/unsloth"
  - label: "Unsloth Documentation — How to Run Local LLMs with Claude Code"
    url: "https://unsloth.ai/docs/basics/claude-code"
---

Unsloth a publié une documentation pratique pour connecter des **serveurs MCP** à des **LLM locaux**. Le principe : faire tourner un modèle comme Qwen ou Gemma en local, via **Unsloth Studio** ou **llama.cpp**, puis lui donner accès à des outils externes standardisés par **Model Context Protocol**. Concrètement, le modèle peut interroger Context7, Exa, Hugging Face, Vercel ou d’autres serveurs MCP, selon ce que l’utilisateur autorise.

Ce n’est pas une nouvelle théorie d’agents. C’est mieux : de la plomberie utilisable. Et dans l’IA locale, la plomberie décide souvent si un projet devient un assistant utile ou une démo qui répond “je ne peux pas accéder à vos fichiers” avec une majesté parfaitement inutile.

## Ce que le guide Unsloth permet de faire

La documentation explique comment relier des MCP servers à un modèle local lancé dans **Unsloth Studio**, l’interface web locale d’Unsloth, ou via un chemin plus bas niveau avec **llama.cpp** et `llama-server`. Les exemples citent des modèles comme **Qwen3.6** et **Gemma 4**, et des serveurs MCP comme **Vercel**, **Context7**, **Exa** et **Hugging Face**.

Le flux Unsloth Studio est volontairement simple : installer l’outil, lancer le serveur local sur le port **8888**, ouvrir l’interface, activer MCP, puis ajouter des serveurs avec OAuth ou headers d’authentification. Les serveurs par défaut mentionnés dans la documentation incluent Context7, Exa et Hugging Face. Pour un serveur comme Vercel, l’utilisateur fournit l’URL de base, choisit OAuth ou token, teste la connexion, puis l’ajoute à la session.

La partie llama.cpp est plus intéressante pour les bricoleurs sobres : elle montre comment exposer un modèle local via `llama-server`, puis connecter les outils par un client/hôte MCP. C’est moins confortable qu’une UI, mais plus proche d’un déploiement maîtrisé : ports explicites, modèle GGUF choisi, orchestration contrôlable, logs vérifiables.

## Pourquoi MCP compte pour le local

Un LLM local sans outils est privé, mais limité. Il peut répondre depuis ses poids, reformuler un document que tu lui donnes, ou générer du code. Dès qu’il doit agir — lire un dépôt, chercher une documentation récente, vérifier un déploiement, inspecter des logs, appeler une API — il lui faut une interface avec le monde.

MCP sert précisément à standardiser cette interface. Au lieu de coder un connecteur différent pour chaque agent, chaque runtime et chaque service, on expose des capacités sous forme de serveurs : recherche documentaire, accès fichiers, navigateur, GitHub, base de données, plateforme cloud, etc. Le modèle ne “possède” pas directement ces services ; il propose des appels, que l’orchestrateur exécute ou refuse.

Pour l’IA locale, l’intérêt est double. D’abord, les données sensibles peuvent rester sur la machine si le modèle tourne réellement en local et si les outils sont choisis avec soin. Ensuite, le même agent peut utiliser un petit modèle local pour des tâches répétitives : chercher une doc, résumer un fichier, préparer une commande, valider un format, extraire des métadonnées. Ce sont des tâches où envoyer systématiquement le contexte à une API fermée est souvent exagéré.

## Unsloth Studio devient un hub local, pas juste un outil de fine-tuning

Unsloth est surtout connu pour l’entraînement et le fine-tuning efficace, mais son dépôt GitHub présente désormais **Unsloth Studio** comme une interface locale pour exécuter, entraîner, exporter et déployer des modèles. Le README mentionne le support de modèles GGUF, LoRA adapters et safetensors, l’export vers GGUF ou safetensors 16-bit, le tool calling, la recherche web, l’exécution de code, le multimodal, et un endpoint d’inférence local utilisable par des outils de code.

Ce changement est notable. L’écosystème local se fragmente souvent entre trois mondes : les outils de training, les runtimes d’inférence, et les interfaces d’agents. Unsloth essaie visiblement de rapprocher ces couches. On peut discuter l’ambition — tout faire finit parfois en usine à gaz — mais MCP est justement un bon mécanisme pour éviter que chaque fonction devienne un plugin propriétaire.

La documentation “Claude Code” d’Unsloth va dans le même sens : elle explique comment pointer un outil de coding agent vers un serveur local en configurant des variables comme `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN` et éventuellement `ANTHROPIC_MODEL`. Elle signale aussi un détail de performance très concret : un header d’attribution ajouté par Claude Code peut invalider le KV cache et rendre l’inférence locale beaucoup plus lente selon Unsloth. Ce genre de détail n’a rien de glamour, mais il sépare le “ça marche” du “ça marche sans me donner envie de jeter le laptop par la fenêtre”.

## Les garde-fous : MCP local ne veut pas dire sans risque

Il faut être clair : connecter un modèle local à MCP augmente la surface d’action. Un assistant qui ne peut que répondre du texte peut halluciner. Un assistant qui peut appeler un serveur GitHub, lire des fichiers ou piloter un navigateur peut halluciner **avec conséquences**.

La bonne architecture doit donc limiter les permissions. Quelques règles de base :

- activer uniquement les serveurs MCP nécessaires à la tâche ;
- séparer les environnements personnels, professionnels et expérimentaux ;
- préférer des tokens à privilèges minimaux ;
- journaliser tous les appels d’outils ;
- demander confirmation pour les actions destructrices ;
- filtrer les chemins fichiers accessibles ;
- valider strictement les arguments générés par le modèle ;
- sandboxer l’exécution de code.

MCP ne remplace pas ces règles. Il rend les intégrations plus propres. C’est très différent. Un connecteur standard peut standardiser une erreur aussi efficacement qu’une bonne pratique, avec un petit nœud papillon en plus.

## Quels modèles pour ce type d’usage ?

Le guide cite Qwen et Gemma, ce qui est logique. Pour un agent local outillé, on ne cherche pas forcément le modèle le plus bavard ; on cherche un modèle qui suit les consignes, produit des appels structurés, récupère après erreur et ne transforme pas chaque réponse en dissertation. Les modèles de taille moyenne quantifiés peuvent suffire pour beaucoup de boucles : recherche de documentation, extraction de champs, résumé de logs, génération de commandes proposées, classification d’intentions.

En revanche, pour des tâches de développement complexes, il faut rester prudent. Un petit modèle local peut très bien router un appel Context7 ou Hugging Face, mais échouer à comprendre un bug subtil dans un grand dépôt. La stratégie la plus robuste est hybride : utiliser le local pour la boucle rapide et privée, puis escalader ponctuellement vers un modèle plus fort si nécessaire — ou vers un humain, ce vieux runtime biologique encore étonnamment compétitif sur les edge cases.

## Ce qu’il faut tester avant de l’adopter

Avant de brancher MCP à un agent local en continu, il faut mesurer des choses simples :

- le modèle produit-il des appels d’outils valides après quantization ?
- respecte-t-il les refus et les confirmations ?
- sait-il corriger un appel raté sans inventer un résultat ?
- combien de latence ajoute chaque serveur MCP ?
- les logs contiennent-ils des données sensibles ?
- l’authentification OAuth ou token est-elle correctement isolée ?
- que se passe-t-il si un serveur MCP renvoie une réponse hostile ou ambiguë ?

Cette dernière question est sous-estimée. Un outil web ou documentaire peut ramener du texte qui influence le modèle. Si l’agent lit une page contenant des instructions malveillantes, il doit traiter ce contenu comme une donnée, pas comme un ordre. C’est vrai pour les agents cloud ; c’est vrai aussi en local. Le fait que le modèle tourne sur ta machine ne rend pas Internet poli.

## Verdict provisoire

La documentation MCP d’Unsloth est une avancée pratique pour les agents locaux. Elle ne résout pas la fiabilité des modèles, ni la sécurité des outils, ni la gouvernance des permissions. Mais elle rend beaucoup plus accessible une architecture saine : modèle local, runtime connu, outils déclarés, appels inspectables.

Pour un usage personnel ou self-hosted, c’est probablement la bonne direction. Pas parce qu’Unsloth aurait inventé MCP, mais parce qu’il l’intègre dans un flux que des utilisateurs de modèles locaux peuvent réellement tester, avec Unsloth Studio ou llama.cpp. Le prochain critère ne sera pas “est-ce que ça se connecte ?”, mais “est-ce que ça agit correctement, vite, et sans prendre des initiatives stupides ?”.

Comme souvent avec les agents, la réponse tient moins dans le modèle que dans le harnais. MCP donne une meilleure attache. À nous de ne pas lâcher la laisse.
