---
title: "ARD : Google, Microsoft et huit éditeurs publient un standard de découverte pour agents IA"
description: "Fin juin 2026, Agentic Resource Discovery (ARD) propose des catalogues machine-readable sur le domaine de l’éditeur pour que les agents trouvent APIs, MCP et pairs à l’exécution — sans intégrations pré-câblées."
pubDate: 2026-06-28
tags: ["agents", "interopérabilité", "MCP", "standard", "Google", "Microsoft"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "MarketingProfs — AI Update June 26, 2026 (ARD)"
    url: "https://www.marketingprofs.com/opinions/2026/55130/ai-update-june-26-2026-ai-news-and-views-from-the-past-week"
  - label: "Model Context Protocol — spécification"
    url: "https://modelcontextprotocol.io/"
---

## La nouvelle

**La semaine du 26 juin 2026**, une coalition d’acteurs majeurs — cités dans la presse tech : **Google, Microsoft, GitHub, Hugging Face, NVIDIA, Salesforce, Snowflake** et d’autres — dévoile **Agentic Resource Discovery (ARD)**, spécification ouverte pour la **découverte dynamique** de ressources agentiques.

Le problème visé est concret : aujourd’hui, chaque agent embarque une liste figée d’outils, d’API et de serveurs **MCP**. Dès qu’un service change d’URL, qu’un nouveau serveur MCP apparaît ou qu’un autre agent devient disponible sur le réseau, il faut **reconfigurer** le harness. ARD propose que l’organisation **publie un catalogue** sur **son propre domaine**, indexé par des **registres**, lisible par les agents **au runtime** — avec métadonnées pour **vérifier la propriété** et établir des connexions de confiance.

## Analyse technique

### Modèle de publication

Schéma mental (tel que rapporté fin juin 2026) :

```
Éditeur / entreprise
  └── héberge un catalogue ARD (machine-readable) sur son domaine
         └── registres tiers indexent et référencent
                └── agent au runtime : discover → verify → connect
```

Ce n’est pas un remplacement unique de **MCP** : MCP décrit **comment** parler à un outil une fois qu’on l’a trouvé ; ARD décrit **comment le trouver** et **comment prouver** qu’il appartient bien à l’éditeur annoncé.

### Comparaison avec l’état de l’art juin 2026

| Approche | Force | Faiblesse |
|----------|--------|-----------|
| **Liste d’outils en dur** (JSON config, `.cursor/mcp.json`) | Simple, prévisible | Casse à chaque ajout / rotation |
| **Marketplace fermée** (un vendor) | UX lisse | Lock-in, pas d’agents tiers |
| **ARD + registres** | Interop, découverte à l’exécution | Complexité ops, spam / usurpation si verify faible |

L’écosystème avait déjà des bribes : well-known URLs, docs OpenAPI, annuaires MCP communautaires. ARD tente de **normaliser** ce que les équipes platform font en artisanal.

### Lien avec la vague « agents partout »

La même semaine, on voit :

- **Computer Use** sur **Gemini 3.5 Flash** (24 juin) ;
- **Claude Tag** et mémoire Slack (26 juin) ;
- **llama.cpp** avec **`--agent`** et proxy MCP (b9726, juin).

ARD s’inscrit dans la couche **plomberie** : sans découverte fiable, multiplier les agents = multiplier les configs YAML et les incidents de prod.

## Impact industrie et self-hosting

### Pour les éditeurs SaaS

Salesforce, Snowflake, NVIDIA ont intérêt à être **découvrables** par des agents clients sans passer par dix partenariats bilatéraux. ARD peut devenir le **DNS des capacités agentiques** — si adoption réelle.

### Pour les labos et infra locale

Sur une stack **self-hosted** (vLLM, Ollama, llama-server, n8n, agents maison) :

1. **Court terme** : peu de changement — tu continues à pointer tes serveurs MCP en local.
2. **Moyen terme** : un **registre interne** ARD pourrait recenser :
   - ton `llama-server` avec outils built-in ;
   - tes bases vectorielles ;
   - tes workers Git / CI ;
   - les agents Hermes / Cursor / Codex autorisés.

Avantage : un **seul agent orchestrateur** découvre les briques au runtime au lieu de dupliquer les listes dans chaque client.

### Risques à anticiper

- **Usurpation de catalogue** : métadonnées de verify doivent être robustes (TLS, signatures, rotation).
- **Shadow IT** : des catalogues ARD non gouvernés sur des sous-domaines = fuite d’API keys décrites en clair.
- **Fragmentation** : si chaque hyperscaler ship son registre propriétaire « compatible ARD », on recrée des silos.

## Positionnement par rapport à la régulation (juin 2026)

Juin 2026 est aussi le mois où Washington **gate** des modèles cyber-capables. ARD ne régule pas les **capacités** du modèle ; il **augmente la surface d’action** en facilitant les connexions. Pour les CISO, c’est un signal : la gouvernance agentique doit couvrir **découverte + exécution**, pas seulement le choix du LLM.

## Limites honnêtes

- Annonce **récente** (fin juin 2026) : implémentations de référence, conformité inter-vendors et tooling à suivre — pas encore l’équivalent mûr de HTTP.
- **ARD ≠ sécurité** : découvrir un outil dangereux plus vite n’améliore pas le sandbox.
- Les équipes **petites** n’ont pas besoin d’ARD tant qu’elles ont **< 5 outils** ; le ROI apparaît avec **dizaines d’agents** et **multi-équipes**.

## Sources

- **AI Update, 26 juin 2026** — coalition ARD (Google, Microsoft, GitHub, Hugging Face, NVIDIA, Salesforce, Snowflake, etc.) : https://www.marketingprofs.com/opinions/2026/55130/ai-update-june-26-2026-ai-news-and-views-from-the-past-week  
- Model Context Protocol (contexte outils) : https://modelcontextprotocol.io/