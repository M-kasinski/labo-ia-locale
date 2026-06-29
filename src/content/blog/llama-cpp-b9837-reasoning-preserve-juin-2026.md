---
title: "llama.cpp b9837 : --reasoning-preserve pour garder la chaîne de pensée en local"
description: "Release du 29 juin 2026 : le flag --reasoning-preserve aligne le chat Jinja sur les modèles reasoning (Qwen, DeepSeek, GLM) sans perdre le thinking entre les tours."
pubDate: 2026-06-29
tags: ["llama.cpp", "reasoning", "GGUF", "serveur local", "agents", "Jinja"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "GitHub Releases — llama.cpp b9837"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9837"
  - label: "PR #25105 — jinja, chat: add --reasoning-preserve flag"
    url: "https://github.com/ggml-org/llama.cpp/pull/25105"
  - label: "Référence — llama.cpp b9726 --agent"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9726"
---

## La nouvelle

**llama.cpp b9837** est publié le **29 juin 2026** (tag `b9837`, commit `b3fed31`, build automatisé vers **00:05 UTC**). La release est dominée par un seul ajout fonctionnel côté **chat / templates Jinja** : le flag **`--reasoning-preserve`**, fusionné via la **PR #25105** après revue de **ggerganov** et **CISC**. Objectif : quand un modèle open-weight expose du **reasoning** ou du **thinking** dans son template, le runtime peut **conserver ce contenu dans l’historique** au lieu de le tronquer silencieusement entre les tours — un détail qui compte énormément pour les agents locaux et les harness type Claude Code branchés sur `llama-server`.

## Analyse technique

### Le problème que ça résout

Sur les modèles **chain-of-thought** ou **thinking blocks** (familles Qwen, DeepSeek, certains GLM quantifiés en GGUF), le **chat template** décide comment sérialiser les messages utilisateur / assistant / tool. Sans option explicite, beaucoup de pipelines :

- **strip** le bloc reasoning à l’affichage ou à la re-soumission ;
- **cassent la continuité** d’un agent multi-étapes qui s’appuie sur sa trace interne ;
- produisent des réponses **moins stables** qu’avec le même modèle chez un hébergeur qui préserve le thinking.

La PR **#25079** (brouillon, « hint preserve_thinking ») a été remplacée par **#25105**, qui expose un flag CLI/serveur clair plutôt qu’un comportement implicite.

### Comportement de `--reasoning-preserve`

- S’applique aux binaires qui utilisent le **parseur Jinja** du module chat (dont **`llama-server`**).
- N’est actif que si le **template du modèle** déclare le support du preserve reasoning ; sinon, rien ne change.
- **Désactivé par défaut** pour tous les templates connus à ce jour — choix conservateur tant que les formats thinking ne sont pas homogènes entre éditeurs.
- Si le template **supporte** la préservation mais que le flag n’est **pas** passé, le serveur peut logger une info du type : *« chat template supports preserving reasoning, consider enabling it via --reasoning-preserve »* (voir `server-context.cpp`).

Exemple d’invocation typique sur une machine de dev :

```bash
llama-server -m /chemin/modele.gguf --agent --reasoning-preserve
```

`--agent` (depuis **b9726**) active outils intégrés + proxy MCP ; `--reasoning-preserve` est **orthogonal** : tu peux l’utiliser avec ou sans mode agent.

### Ce que b9837 n’apporte pas

Pas de nouveau kernel CUDA/Metal, pas de quant GGUF inédite, pas de bump de débit annoncé dans le changelog de ce tag. La chaîne **b9830** (28 juin) avait ajouté `llama download --offline` ; **b9835–b9837** sont surtout consolidation template + correctif d’aide CLI. Pour le throughput pur, les builds récents **OpenCL / ROCm 7.2 / CUDA 13.3** listés dans les assets GitHub restent le levier matériel.

## Benchmarks et validation terrain

Il n’y a **pas** de benchmark officiel lié à ce tag : l’impact se mesure en **qualité agentique** (moins de dérives après 5–10 tours, meilleure reprise après tool call). Méthode honnête pour le Labo :

1. Même prompt + même harness (ex. client OpenAI sur `localhost:8080`).
2. Run A : serveur **sans** `--reasoning-preserve`.
3. Run B : serveur **avec** `--reasoning-preserve`.
4. Comparer taux de succès sur une tâche longue (refactor multi-fichiers, debug avec `grep` + `read_file` via `--agent`).

Les modèles **non-reasoning** ne devraient pas bouger ; ne active le flag que sur des GGUF dont la fiche Hugging Face ou le `tokenizer.chat_template` mentionne thinking/reasoning.

## Impact pour l’écosystème local

### Pourquoi c’est aligné avec juin 2026

- Les **open-weights agentiques** (GLM-5.2, DeepSeek V4 Flash, Kimi K2.7 Code) montent en puissance ; les équipes self-hostent via **llama.cpp**, **Ollama** (submodule llama.cpp, ex. **v0.30.11-rc0** du 24 juin), ou **LM Studio**.
- La course aux **harness** (Claude Code, Codex, agents MCP) a montré que le **scaffold** peut valoir plus qu’un swap de modèle ; préserver le reasoning évite de **casser le scaffold** côté contexte.
- Après **b9726**, llama.cpp se positionne comme **runtime agent + inférence** ; **b9837** complète la couche **mémoire de conversation** pour les modèles qui raisonnent en blocs structurés.

### Cas d’usage concrets

| Profil | Recommandation |
|--------|----------------|
| Dev solo, Qwen/DeepSeek GGUF, agent `--agent` | Tester `--reasoning-preserve` en priorité sur tâches > 8k tokens de contexte |
| Prod interne, modèles sans thinking | Laisser le défaut (off) |
| CI / air-gap | Combiner avec `llama download --offline` (**b9830**) pour figer modèles + binaire |

### Limites honnêtes

- **Interop templates** : chaque famille GGUF peut implémenter le preserve différemment ; un flag global ne garantit pas le même rendu qu’une API cloud calibrée par l’éditeur.
- **Sécurité** : préserver le thinking **augmente la taille du contexte** et peut inclure des traces sensibles dans les logs ; à filtrer si tu exposes le serveur au réseau.
- **Ollama** : tant que le submodule n’embarque pas **b9837**, il faudra compiler **llama.cpp** soi-même ou attendre la prochaine release Ollama pour le flag côté `ollama serve` équivalent.

## Sources vérifiées

- Release **b9837** (29 juin 2026) : https://github.com/ggml-org/llama.cpp/releases/tag/b9837  
- PR **#25105** mergée 28 juin 2026 : https://github.com/ggml-org/llama.cpp/pull/25105  
- Contexte agent **b9726** : article de référence du Labo `llama-cpp-b9726-agent-server-local.md` et release https://github.com/ggml-org/llama.cpp/releases/tag/b9726  

**Verdict** : pas une release « spectacle », mais un **correctif de fidélité** pour quiconque fait tourner des modèles reasoning en local. Si tu self-hostes déjà avec `--agent`, active `--reasoning-preserve` sur un modèle compatible avant de blâmer le GGUF pour une mémoire d’agent défaillante.