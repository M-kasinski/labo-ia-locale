---
title: "llama.cpp b9827 : cudaMemcpy2DAsync débloque les snapshots GDN en multi-slot"
description: "Sortie du 27 juin 2026 : le fast path CUDA pour les copies strided accélère les rollbacks de cache récurrent — un correctif ciblé mais critique pour les modèles GDN servis en local."
pubDate: 2026-06-27
tags: ["llama.cpp", "CUDA", "GGUF", "inférence locale", "GDN", "serveur"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "GitHub Releases — llama.cpp b9827"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9827"
  - label: "PR #25057 — cudaMemcpy2DAsync fast path in ggml_cuda_cpy"
    url: "https://github.com/ggml-org/llama.cpp/pull/25057"
  - label: "Article de référence Labo — llama.cpp b9726 et --agent"
    url: "https://github.com/ggml-org/llama.cpp/releases/tag/b9726"
---

## La nouvelle

**llama.cpp b9827** est publié le **27 juin 2026** (commit `0ed235e`, build `github-actions` à 12:49 UTC). La release ne fait pas le buzz des gros MoE du moment, mais elle corrige un goulot d’étranglement très concret : les **copies strided sur GPU CUDA** passent par **`cudaMemcpy2DAsync`** au lieu d’un kernel scalaire lent. Le cas d’usage documenté par les mainteneurs : la **mise à jour des snapshots récurrents GDN** avec **`-np 4`**, quand les slots de rollback sont séparés par des **écarts de stride** dans le cache.

Pour qui sert des modèles **récurrents / stateful** via `llama-server` sur NVIDIA, c’est le genre de patch qui transforme un scénario « ça rame ou ça plante » en inférence utilisable — sans changer de modèle ni de quantisation.

## Analyse technique

### Le problème : contigu ≠ strided

Dans `ggml`, une copie tensor-to-tensor « même type, même shape » n’est pas toujours un bloc mémoire linéaire. Quand chaque **ligne** reste contiguë mais que le tenseur global a un **pitch** (padding entre lignes ou entre blocs de cache), l’ancien chemin CUDA retombait sur une **copie élément par élément** — correcte, mais coûteuse en bande passante et en latence.

Le PR **#25057** détecte ce motif **2D pitched** et délègue à **`cudaMemcpy2DAsync`**, l’API CUDA prévue pour exactement ce cas. Résultat attendu : moins de temps CPU/GPU gaspillé dans les opérations de **snapshot / rollback** du state récurrent.

### Lien avec GDN et `-np 4`

Les modèles de la famille **GDN** (Generalized Delta Network et dérivés récurrents dans l’écosystème ggml) maintiennent un **état interne** entre tokens. En serving multi-slot (`-np` > 1), le serveur doit parfois **dupliquer ou restaurer** des morceaux de cet état quand un slot fait rollback — d’où des copies entre buffers **non contigus** mais structurés en 2D.

Les mainteneurs indiquent explicitement que **b9827** répare le scénario **GDN recurrent snapshot update with `-np 4`**. Si tu faisais tourner ce type d’architecture en local et que tu voyais des pics de latence inexpliqués dès que tu montais le parallélisme de slots, ce build mérite un test A/B avant de blâmer le modèle ou la quant Q4.

### Tests et backends

La PR ajoute des **tests unitaires** sur le chemin strided optimisé. Côté **OpenVINO**, les copies strided restent **non supportées** — les nouveaux tests ont mis en évidence des échecs sur ce backend, ce qui est documenté plutôt que masqué. En pratique Labo :

| Backend | Impact b9827 |
|---------|----------------|
| **CUDA 12/13 (Windows & Linux)** | Bénéfice direct si tu utilises GDN / copies strided |
| **Vulkan / ROCm / SYCL** | Pas le focus de cette release (voir b9825/b9826) |
| **CPU pur** | Neutre |
| **OpenVINO** | Pas de gain ; limitations strided inchangées |

### Fil des releases du 27 juin

La journée est dense côté tags : **b9825** (fix Vulkan step operator), **b9826** (tests SYCL norm), **b9827** (CUDA strided). Ce n’est pas une refonte agentique comme **b9726** (`--agent`) — c’est de la **maintenance haute fréquence** sur les backends. Pour une stack locale stable, l’habitude « rebuild hebdo » sur llama.cpp reste rationnelle.

## Benchmarks et résultats

Les notes de release **ne publient pas** de tableau tok/s avant/après pour b9827. Les gains sont argumentés par **correction fonctionnelle + suppression d’un kernel lent**, pas par un marketing chiffré. Méthode honnête pour valider chez toi :

1. Même modèle GDN-compatible, même `-np`, même `-c`.
2. Mesurer **latence p95** sur une session avec rollbacks (ou bench interne si tu en as un).
3. Comparer **b9826** vs **b9827** sur la **même** build CUDA (12.4 ou 13.3 selon le zip Windows).

Sans modèle GDN, tu ne verras probablement **aucune** différence mesurable — et c’est normal.

## Impact pour l’écosystème local

1. **Ollama / LM Studio** : bénéfice **indirect** au prochain bump du submodule llama.cpp (Ollama **v0.30.11** du 25 juin annonce déjà une remontée llama.cpp).
2. **Serveurs multi-utilisateurs maison** : les copies strided apparaissent aussi hors GDN (certaines layouts KV / cache custom). Le fast path est générique pour le motif 2D pitched.
3. **Agents locaux** : si tu combines `--agent` (b9726+) et modèles stateful, la stabilité des slots parallèles compte autant que le function calling.

### Limites

- Patch **CUDA-only** : pas d’équivalent Metal/ROCm dans ce tag.
- **Pas de nouveaux modèles** ni de quant novelle — uniquement runtime.
- Les binaires **KleidiAI macOS** et **openEuler** restent **désactivés** (PRs #23780 / #23705), comme sur les releases précédentes.

## Mise à jour pratique

```bash
# Exemple : binaire précompilé Windows CUDA 13.3
# https://github.com/ggml-org/llama.cpp/releases/download/b9827/llama-b9827-bin-win-cuda-13.3-x64.zip
# + pack DLL cudart associé sur la même page release

./llama-server -m ./models/votre-modele.gguf -np 4 -c 8192 --host 127.0.0.1 --port 8080
```

Sur macOS Apple Silicon, prends **`llama-b9827-bin-macos-arm64.tar.gz`** — le correctif CUDA ne s’applique pas, mais tu restes aligné sur le reste du code serveur et des templates.

## Sources vérifiées

- [Release b9827 — ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp/releases/tag/b9827)
- [PR #25057 — cudaMemcpy2DAsync fast path](https://github.com/ggml-org/llama.cpp/pull/25057)
- [Release b9826 — correctif SYCL norm](https://github.com/ggml-org/llama.cpp/releases/tag/b9826)
- [Release b9825 — correctif Vulkan step](https://github.com/ggml-org/llama.cpp/releases/tag/b9825)