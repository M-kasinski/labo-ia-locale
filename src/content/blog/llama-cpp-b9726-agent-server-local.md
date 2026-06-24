---
title: "llama.cpp b9726 : le serveur devient un agent local avec --agent"
description: "La version b9726 de llama.cpp consolide les outils MCP et les built-in tools sous un seul flag --agent. Le moteur d'inférence se mue en runtime agentique autonome."
pubDate: 2026-06-19
tags: ["llama-cpp", "agents locaux", "MCP", "serveur", "GGUF", "outils intégrés"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "llama.cpp GitHub Releases — b9726"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9726"
  - label: "PR #24801 — server: add --agent arg, remove redundant webui naming compat"
    url: "https://github.com/ggml-org/llama.cpp/pull/24801"
  - label: "Documentation serveur llama.cpp — outils intégrés et MCP proxy"
    url: "https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md"
---

## La nouvelle

**llama.cpp b9726**, publié ce 19 juin 2026, introduit le flag **`--agent`** pour `llama-server`. Un seul argument active à la fois le proxy CORS MCP et l'ensemble des outils intégrés pour agents IA. C'est un signal clair : llama.cpp ne se veut plus seulement un moteur d'inférence — il devient un runtime agentique complet, exécutable localement sur un seul binaire compilé.

## Analyse technique

### Le flag `--agent` : consolidation de deux fonctionnalités existantes

Avant b9726, l'activation des capacités agentiques nécessitait deux flags séparés :

- **`--webui-mcp-proxy`** (ou `--ui-mcp-proxy`) : active le proxy CORS pour les serveurs MCP externes
- **`--tools TOOL1,TOOL2,...`** : active les outils intégrés pour agents IA

Le PR #24801 fusionne ces deux fonctionnalités sous un seul flag `--agent` (alias `-ag`). L'argument `--webui-mcp-proxy` est marqué comme déprécié mais reste fonctionnel pour la rétrocompatibilité.

### Les outils intégrés — ce que ton serveur peut faire maintenant

Avec `--agent`, le serveur expose directement ces 8 outils :

| Outil | Description | Usage typique |
|-------|-------------|---------------|
| `read_file` | Lecture de fichiers locaux | Analyse de code, lecture de docs |
| `file_glob_search` | Recherche par pattern glob | Navigation dans un dépôt |
| `grep_search` | Recherche regex dans les fichiers | Debug, recherche de motifs |
| `exec_shell_command` | Exécution de commandes shell | Builds, scripts, automatisations |
| `write_file` | Écriture de fichiers | Génération de code, config |
| `edit_file` | Édition ciblée de fichiers | Corrections, modifications |
| `apply_diff` | Application de patches unifiés | Revisions structurées |
| `get_datetime` | Accès à la date/heure système | Contexte temporel pour l'agent |

Ces outils sont marqués comme **expérimentaux** et désactivés par défaut. La [documentation du serveur llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) insiste : ne pas activer dans des environnements non fiables. L'exécution de commandes shell (`exec_shell_command`) est évidemment sensible — le modèle peut exécuter n'importe quelle commande sur ta machine.

### Proxy MCP CORS intégré

Le proxy CORS permet au WebUI de llama.cpp de communiquer avec des serveurs MCP distants qui ne supportent pas les requêtes cross-origin. C'est crucial pour connecter des outils MCP tiers (bases de données, APIs externes, services cloud) à un agent tournant localement.

### Ce qui change par rapport à b9704

La version précédente (**b9704**, 18 juin) apportait :
- Vérification BF16 sur Metal pour les kernels de concatenation
- Support SYCL pour la quantisation Q1_0 (multiplication matricielle et produits externes)
- HTTP 400 sur grammaire invalide dans le serveur
- Correction du forwarding des arguments du routeur

b9726 construit dessus en ajoutant cette couche agentique unifiée. Entre les deux versions, la progression est notable : llama.cpp passe de « moteur d'inférence avec corrections » à « plateforme agentique locale ».

## Impact pour l'écosystème local

### Pourquoi ça compte

1. **Un seul binaire = un agent complet** : Plus besoin de orchestrer séparément llama-server + un framework agent (smolagents, LangGraph, etc.). Le serveur expose directement les outils via son API OpenAI-compatible.

2. **Compatibilité immédiate avec les clients existants** : Tout ce qui parle à l'API OpenAI (Claude Code, Codex CLI, Cursor, ou un simple script Python) peut utiliser ces outils. C'est du function calling standard.

3. **Pas de dépendance cloud** : Contrairement aux agents Anthropic/OpenAI/Google qui nécessitent une connexion API payante, un agent llama.cpp tourne 100% local avec tes propres modèles GGUF.

4. **Sécurité contrôlée** : Les outils sont désactivés par défaut et peuvent être sélectionnés individuellement (`--tools read_file,grep_search` au lieu de `--agent` pour tout activer). Tu décides ce que l'agent peut faire.

### Limites réalistes

- **Qualité du modèle** : Les outils ne compensent pas un modèle faible. Un Qwen3.6-27B en Q4_K_M sur une M3 Max gérera des tâches simples ; pour du coding complexe, il faut monter en puissance (Nemotron-3-Super, GLM-5.2 quantifié si tu as les GPU).
- **`exec_shell_command` est dangereux** : Activé sans réflexion, ton modèle peut faire n'importe quoi sur ta machine. À utiliser avec circonspection.
- **Écosystème MCP encore immature** : Le proxy CORS MCP est utile mais le standard MCP lui-même est en évolution rapide — la compatibilité entre serveurs n'est pas garantie.

## Comment l'utiliser

```bash
# Activer tous les outils + MCP proxy
./llama-server -m ./models/qwen3.6-27b-Q4_K_M.gguf --agent --jinja -c 8192

# Activer seulement certains outils (plus sûr)
./llama-server -m ./models/qwen3.6-27b-Q4_K_M.gguf --tools read_file,grep_search,write_file --jinja -c 8192

# Via variable d'environnement
LLAMA_ARG_TOOLS="all" ./llama-server -m ./models/model.gguf --jinja
```

L'API reste compatible OpenAI — les outils apparaissent dans le champ `tools` de la réponse du serveur et peuvent être appelés via des requêtes `/v1/chat/completions` standard.

## Sources vérifiées

- [llama.cpp Releases — b9726 sur GitHub](https://github.com/ggml-org/llama.cpp/releases/tag/b9726)
- [PR #24801 — add --agent arg](https://github.com/ggml-org/llama.cpp/pull/24801)
- [Documentation serveur — outils intégrés et MCP proxy](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
