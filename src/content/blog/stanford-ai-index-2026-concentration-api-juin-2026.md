---
title: "AI Index 2026 (Stanford HAI) : moins de modèles notables, plus d’accès API et de concentration"
description: "Le rapport Stanford HAI de juin 2026 confirme un ralentissement des sorties « notables », la domination des déploiements via API et la concentration géographique US/Chine — lecture utile pour choisir entre cloud et open-weight local."
pubDate: 2026-06-29
tags: ["Stanford HAI", "AI Index", "régulation", "open-weight", "API", "géopolitique"]
category: "veille"
author: "Labo IA"
draft: false
sources:
  - label: "Stanford HAI — Artificial Intelligence Index Report 2026 (PDF)"
    url: "https://hai.stanford.edu/assets/files/ai_index_report_2026.pdf"
  - label: "Stanford HAI — AI Index hub"
    url: "https://hai.stanford.edu/ai-index"
---

## La nouvelle

Stanford **HAI** publie l’édition **2026** de l’**Artificial Intelligence Index** — un document de **plusieurs centaines de pages** qui sert de référence annuelle pour investisseurs, régulateurs et équipes R&D. Le constat d’ouverture, repris dans la section **Research and Development**, est sans ambiguïté : les ressources derrière l’IA continuent de monter, mais **moins de modèles « notables »** sont sortis en **2025** qu’en **2024**, et les systèmes de frontière se **concentrent** chez un petit nombre d’organisations.

Pour un lecteur qui hésite entre **API frontier** et **GGUF dans le garage**, ce rapport n’est pas du bruit LinkedIn : c’est la photographie institutionnelle de la bascule **open weights (unrestricted)** vs **API-only**.

## Analyse technique

### Production de modèles : qui publie quoi ?

Le rapport s’appuie notamment sur la base **Epoch AI** (mise à jour continue — les totaux année par année peuvent légèrement différer d’une édition à l’autre). Les tendances décrites pour **2025** :

| Indicateur | Lecture |
|------------|---------|
| **Modèles notables US** | **59** releases recensées |
| **Chine** | **35** |
| **Corée du Sud** | **8** (3ᵉ rang) |
| **Dynamique YoY** | Baisse du nombre de nouvelles releases **notables** dans toutes les grandes zones |

La Chine n’a pas « rattrapé » le volume brut US, mais elle reste le **seul autre pôle** à deux chiffres — cohérent avec la pression open-weight (**Qwen**, **DeepSeek**, **GLM**, **Kimi**) observée sur les benchmarks de coding en juin 2026.

### Mode de diffusion : l’API devient la norme

Figure clé du rapport : en **2025**, sur **102** modèles notables, **47** sont sortis en **accès API** — le type de release le plus fréquent. La part **« open weights (unrestricted) »** reste significative mais **n’est plus majoritaire** parmi les modèles que l’Index classe comme structurants.

Traduction opérationnelle :

- Les labs frontier **monétisent et contrôlent** via **endpoints** (tarification token, logs, kill switch export).
- Les poids ouverts existent encore, souvent **en retard** ou en **variante Flash** moins exposée politiquement.
- Juin 2026 illustre la tension : **GPT-5.6** en preview gouvernée, **Mythos/Fable** sous export control, pendant que **llama.cpp b9840** intègre **DeepSeek V4** pour l’auto-hébergement.

### Concentration et « controlled access »

Le chapitre R&D insiste : la frontière est de plus en plus **oligopolistique**. Moins de releases ne signifie pas moins de capacité agrégée — les **clusters**, les **post-training** et les **harness** absorbent le budget qui partait autrefois en « encore un checkpoint open ».

Pour les équipes produit :

- **Dépendance API** = dépendance **politique** (cf. retraits Fable/Mythos, validation client-par-client pour Sol).
- **Dépendance open-weight** = dépendance **ops** (VRAM, quants, sécurité `exec_shell_command` sur agents locaux).

L’Index ne tranche pas morale ; il **documente** que l’industrie a choisi le premier chemin pour le revenue, et le second pour l’**adoption développeur** (GGUF, Hugging Face, Ollama stars).

### Lien avec l’IA locale (lecture Labo IA)

Le rapport n’est pas un guide Ollama, mais trois sections éclairent le self-hosting :

1. **Open weights** — Toujours une part non négligeable des releases ; la Chine y est surreprésentée relativement à sa part closed API.
2. **Compute** — L’essentiel du CAPEX va au **datacenter** ; le hardware **grand public** reste un dérivé — d’où l’intérêt des **MoE quantifiés** et des runtimes **llama.cpp / MLX**.
3. **Policy** — Montée des **export controls** et des **evaluations cyber** ; cohérent avec les system cards allongées (GPT-5.6 preview card, Fable 5 system card).

## Impact pour l’écosystème

### Startups & entreprises

- **Budget modèle** : si ton usage est **80 % tâches standard**, l’Index + travaux type **Intelligence Per Watt** vont dans le même sens — **ne pas sur-payer** le frontier.
- **Compliance** : trajectoire vers plus de **documentation** (safety, evals) même pour modèles open — prépare des **registres d’usage** avant que le Colorado AI Act (30 juin 2026) ne devienne la norme US.

### Recherche open-source

- Moins de « gros noms » open par an ≠ fin de l’open-weight : **2026** compense avec des **MoE massifs** (Nemotron 3 Ultra, Kimi K2.7, GLM-5.2) et des **correctifs runtime** (vLLM MR-V2, llama.cpp agent server).

### Limites du rapport

- **Décalage** : données 2025 dominantes ; la vague **juin 2026** (Sol, Fable shutdown, Corée 880 Md$) arrive **après** la clôture statistique — à croiser avec la presse quotidienne.
- **Définition « notable »** : biais vers l’**anglophone** et le **benchmark public**.
- **PDF de 400+ pages** : synthèse ici volontairement ciblée R&D/diffusion ; lire les chapitres **Policy** et **Technical Performance** pour ton secteur.

## Ce qu’il faut retenir

L’**AI Index 2026** ne annonce pas la fin des modèles open ; il décrit une industrie qui **externalise la frontière** via API tout en laissant une **niche open-weight** porter l’innovation self-host. C’est exactement le schéma où **llama.cpp + GGUF + agents `--agent`** gagnent du terrain quand Washington et les labs ferment les vannes sur les tiers cyber-capables.

## Sources

- [Artificial Intelligence Index Report 2026 (PDF)](https://hai.stanford.edu/assets/files/ai_index_report_2026.pdf)
- [Stanford HAI — AI Index](https://hai.stanford.edu/ai-index)