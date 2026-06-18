---
title: "GLM-5.2 : 744B MoE, 1M de contexte et licence MIT — le modèle open-weight qui change l'échiquier"
description: "Zhipu AI (Z.ai) sort GLM-5.2, un modèle MoE de 744B paramètres avec contexte 1M et licence MIT. On décortique l'architecture IndexShare, les benchmarks et la faisabilité locale."
pubDate: 2026-06-18
tags: ["GLM-5.2", "Zhipu AI", "MoE", "open-weight", "contexte long", "MIT", "Z.ai"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Blog officiel GLM-5.2 sur Hugging Face"
    url: "https://huggingface.co/blog/zai-org/glm-52-blog"
  - label: "Page modèle Hugging Face — zai-org/GLM-5.2"
    url: "https://huggingface.co/zai-org/GLM-5.2"
  - label: "Fello AI — What Is GLM 5.2?"
    url: "https://felloai.com/glm-5-2/"
  - label: "TechTimes — GLM-5.2 Open Weights Live"
    url: "https://www.techtimes.com/articles/318543/20260617/glm-52-open-weights-live-top-coding-benchmark-api-use-carries-china-data-risk.htm"
  - label: "VentureBeat (via ECiKS) — GLM-5.2 benchmarks vs GPT-5.5"
    url: "https://eciks.org/9367-25350-glm-5-2-beats-gpt-5-5-coding-benchmarks-cost"
  - label: "Ollama — GLM-5.2 library page"
    url: "https://ollama.com/library/glm-5.2"
  - label: "Unsloth GLM-5.2 GGUF — quantizations locales"
    url: "https://huggingface.co/unsloth/GLM-5.2-GGUF"
  - label: "Latent Space — GLM-5.2 technical analysis"
    url: "https://www.latent.space/p/ainews-glm-52-the-top-frontend-coding"
---

## Le signal

Le 13 juin 2026, Zhipu AI (qui opère désormais sous le nom de **Z.ai**) a lancé GLM-5.2, un modèle de 744 milliards de paramètres avec une fenêtre de contexte d'**un million de tokens**. Les poids complets sont devenus disponibles sous **licence MIT** le 17 juin. En quatre jours, les versions quantifiées GGUF ont fait leur apparition sur Hugging Face et le modèle est intégré à Ollama.

Ce n'est pas juste un nouveau numéro de benchmark. C'est un modèle pensé pour les tâches à long horizon — agents de code, refactoring multi-fichiers, analyse de codebases entières — et il est ouvert au sens le plus large du terme : MIT, pas de restrictions commerciales.

## Architecture : MoE avec IndexShare

GLM-5.2 utilise une architecture **Mixture-of-Experts** : 744B de paramètres au total, mais seulement **40B actifs par token** (8 experts par token). Le coût d'inférence est donc celui d'un modèle ~40B, pas celui d'un 744B dense.

L'innovation architecturale clé s'appelle **IndexShare**. Dans l'attention sparse DSA (DeepSeek Sparse Attention), chaque couche calcule normalement un indexeur pour déterminer quels tokens sont pertinents. IndexShare **réutilise le même indexeur sur quatre couches consécutives** au lieu de le recalculer à chaque couche. Résultat : **réduction de 2,9× des FLOPs par token** à un contexte de 1M, selon le blog officiel de Z.ai.

> "L'indexer est placé au premier des 4 couches et les indices top-k sont réutilisés pour les 4 couches. Cela réduit le calcul du produit scalaire de l'indexer et de l'opération top-k sur 3/4 des couches." — Blog GLM-5.2 (Hugging Face)

Le modèle intègre aussi une couche **MTP (Multi-Token Prediction)** améliorée pour le décodage spéculatif, augmentant la longueur d'acceptation d'**jusqu'à 20 %**.

## Contexte 1M : pas du marketing, de l'usage concret

La fenêtre de contexte de GLM-5.2 est de **1M tokens en entrée** (~750 000 mots), avec un maximum de sortie de **131 072 tokens**. Comparé à GLM-5.1 (~200K tokens), c'est une multiplication par 5.

Concrètement, cela signifie :
- Charger un **entier repository de code moyen** en contexte
- Analyser des **corpus de documentation API** complets sans chunking
- Maintenir l'état d'un **projet complet en mémoire** pour un agent de code multi-étapes

C'est sur cette capacité que le modèle est optimisé : les benchmarks FrontierSWE et SWE-Marathon mesurent précisément la capacité des agents à accomplir des projets techniques ouverts sur des horizons de plusieurs heures.

## Benchmarks : ce qu'on sait et ce qu'on ne sait pas

**Attention** : Zhipu n'a publié **aucun benchmark officiel** au lancement. Les chiffres qui circulent proviennent de sources tierces (Agent Arena, Design Arena, analyses VentureBeat). Les traiter comme des indications, pas comme des vérités absolues.

Voici ce qui est rapporté par plusieurs sources convergentes :

| Benchmark | GLM-5.2 | Opus 4.8 | GPT-5.5 |
|-----------|---------|----------|---------|
| Terminal-Bench 2.1 | **81.0** | 85.0 | ~80.0 |
| SWE-bench Pro | **62.1** | — | — |
| FrontierSWE | ~Opus 4.8 - 1% | référence | ~GLM-5.2 - 1% |
| MCP-Atlas (outils) | **77.0** | — | 75.3 |
| Design Arena (ELO) | **1360** | — | — |

Sur le Design Arena, GLM-5.2 prendrait la première place, devant Claude Fable 5, selon les résultats crowdsourcés. Sur les tâches de code long-horizon, il se positionnerait juste derrière Opus 4.8 — ce qui est notable pour un modèle de 744B MoE face à des modèles fermés supposés deux fois plus grands.

Pour le raisonnement pur (mathématiques, AIME), le modèle reste compétitif mais ne mène pas le classement. Son avantage comparatif est concentré sur **code + contexte long + outils**.

## Faisabilité locale : quel matériel ?

C'est ici que ça se corse. Même avec le MoE (40B actifs), un modèle de 744B total reste **massif** pour le local.

### Versions quantifiées disponibles

**Unsloth** a déjà publié des GGUF avec sa quantization Dynamic 2.0 :
- **UD-IQ2_XXS** (dynamic 2-bit) : ~241 Go
- **UD-Q4_K_XL** (dynamic 4-bit) : taille intermédiaire
- **UD-TQ1_0** (dynamic 1-bit) : ~176 Go

**bartowski** et **ubergarm** ont aussi publié des GGUF standards (Q3_K_XL, Q4_K_M, etc.).

### Matériel requis

| Quantisation | RAM minimale | RAM confortable |
|---|---|---|
| 2-bit (IQ2) | ~256 Go | 384 Go+ |
| 4-bit (Q4_K_M) | ~400 Go+ | 512 Go+ |
| FP8 | ~1,5 To | — |

En pratique, **un Mac Studio M4 Max 128 Go ne suffit pas**. Il faut viser :
- **Mac Studio M4 Ultra 192-384 Go** (unified memory)
- **Cluster multi-GPU NVIDIA** (A100/H100 en tensor parallel)
- **Serveur avec 512 Go+ RAM DDR5** pour CPU-only (lent mais fonctionnel)

Le paging SSD d'Apple aide quand le modèle dépasse la RAM — un Mac Mini M4 16 Go a obtenu ~30 tok/s sur un agent 35B en paging, contre ~1,6 tok/s pour une config NVIDIA équivalente. Mais à l'échelle de 744B, même l'avantage SSD a ses limites.

### Runtimes compatibles

- **Ollama** : `ollama run glm-5.2` (modèle directement dans la bibliothèque)
- **llama.cpp** : GGUF d'Unsloth/bartowski/ubergarm
- **vLLM** : support officiel dans la v0.23.0 (voir notre article dédié)
- **SGLang** : mentionné par la communauté
- **Transformers** : via le repo Hugging Face officiel

## Licence MIT : le vrai coup de force

La licence MIT est le vrai différenciateur. Contrairement aux licences Llama ou Mistral qui imposent des restrictions d'usage (nombre d'utilisateurs, usage commercial conditionnel), **MIT n'a aucune restriction**. Vous pouvez :
- Héberger le modèle en interne sans comptabilité d'utilisateurs
- Le fine-tuner et redistribuer les poids dérivés
- L'utiliser dans un produit commercial sans autorisation
- Le modifier à votre guise

C'est le même niveau d'ouverture que les poids Gemma 4 (Apache 2.0) mais avec une licence encore plus permissive.

## Risques et limites

Soyons clairs sur ce qui fait tilt :

1. **Pas de benchmarks officiels** : Zhipu n'a publié aucune évaluation indépendante. Les scores cités viennent de tierces parties. Vérifier soi-même sur vos workloads.
2. **Origine chinoise** : L'API cloud de Z.ai est soumise à la loi chinoise sur l'intelligence nationale. Les poids locaux téléchargés n'ont pas de telemetry connue, mais c'est un point à vérifier.
3. **Matériel prohibitif** : Même quantifié, ce modèle n'est pas accessible à un particulier standard. Le "local" ici, c'est plutôt "on-prem enterprise".
4. **Contexte 1M ≠ qualité 1M** : La capacité de contexte ne garantit pas la pertinence sur toute la fenêtre. Les modèles ont tendance à perdre en qualité au-delà de certains seuils.

## Ce que ça change

GLM-5.2 n'est pas le modèle que vous allez télécharger ce soir pour le faire tourner sur votre RTX 4090. Mais il envoie un signal clair : **le gap entre open-weight et closed frontier se réduit sur les tâches qui comptent** — code, agents, contexte long.

Pour les équipes qui ont le matériel, c'est une option sérieuse pour remplacer un API fermé par un modèle auto-hébergé, sans compromis sur la licence. Pour le reste de la communauté, c'est un rappel que l'écosystème open-weight avance plus vite que prévu.

## Sources

- [Blog officiel GLM-5.2 — Hugging Face](https://huggingface.co/blog/zai-org/glm-52-blog)
- [Page modèle Hugging Face — zai-org/GLM-5.2](https://huggingface.co/zai-org/GLM-5.2)
- [Fello AI — What Is GLM 5.2?](https://felloai.com/glm-5-2/)
- [TechTimes — GLM-5.2 Open Weights Live](https://www.techtimes.com/articles/318543/20260617/glm-52-open-weights-live-top-coding-benchmark-api-use-carries-china-data-risk.htm)
- [VentureBeat (via ECiKS) — Benchmarks vs GPT-5.5](https://eciks.org/9367-25350-glm-5-2-beats-gpt-5-5-coding-benchmarks-cost)
- [Ollama — GLM-5.2 library](https://ollama.com/library/glm-5.2)
- [Unsloth GLM-5.2 GGUF](https://huggingface.co/unsloth/GLM-5.2-GGUF)
- [Latent Space — GLM-5.2 technical analysis](https://www.latent.space/p/ainews-glm-52-the-top-frontend-coding)
