---
title: "llama.cpp ajoute DFlash : le décodage spéculatif passe au mode bloc"
description: "Le PR #22105 ajoute DFlash à llama.cpp, avec des gains annoncés jusqu’à 8x sur Qwen3 et une implémentation compatible serveur et CLI."
pubDate: 2026-06-30
tags: ["llama.cpp", "dflash", "speculative-decoding", "local-ai", "inference"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "GitHub — llama.cpp PR #22105: add DFlash support"
    url: "https://github.com/ggml-org/llama.cpp/pull/22105"
  - label: "GitHub — Releases · ggml-org/llama.cpp"
    url: "https://github.com/ggml-org/llama.cpp/releases"
---

## La nouvelle

`llama.cpp` vient d’absorber **DFlash**, une variante de décodage spéculatif qui ne fait pas juste “deviner plus vite” : elle génère **un bloc complet de candidats en une seule passe de draft**.

Le PR #22105 a été **fusionné le 28 juin 2026**, donc on est bien dans la fenêtre des 3 jours. Le point marquant n’est pas seulement la nouveauté algorithmique : la feature arrive directement dans **`llama-cli`** et **`llama-server`**, ce qui la rend exploitable sans fork exotique ni bricolage de labo. Enfin.

## Analyse technique

Le décodage spéculatif classique repose souvent sur un petit modèle “draft” qui propose quelques tokens, puis sur un modèle principal qui vérifie.

DFlash change le rythme :
- le draft produit **un bloc** de candidats
- le vérificateur tranche ensuite sur la séquence
- le débit du draft monte, mais le coût du draft devient plus lourd qu’avec des approches type EAGLE3

Autrement dit, on échange une partie de la simplicité contre une meilleure efficacité par itération. Ce n’est pas gratuit ; c’est juste mieux emballé.

Le PR insiste aussi sur un point important : l’implémentation vise la **complète équivalence numérique** avec la référence. C’est un détail qui compte. Beaucoup de “speedups” IA sont de jolies diapositives jusqu’au premier écart silencieux dans les logits.

Le support de conversion GGUF est intégré, avec des commandes dédiées pour fabriquer :
- le **modèle cible**
- le **draft DFlash**
- les artefacts nécessaires au service

La bonne nouvelle pour l’écosystème local, c’est que `llama.cpp` garde son rôle : servir de socle portable, pas de vitrine académique. Quand une idée sort du papier et finit dans `llama-server`, elle devient vraiment intéressante.

## Benchmarks / résultats

Le PR annonce plusieurs ordres de grandeur à retenir.

### Résultat principal
- jusqu’à **8x de speedup** sur **Qwen3** selon les configurations testées

### Exemple Qwen3.6-27B / Qwen3.6-27B-dflash
Sur un scénario **Q4_K_M** avec DGX Spark, le tableau du PR montre :
- **33.76 tokens/s** en moyenne avec DFlash contre **12.57 tokens/s** en base
- **2.69x** de débit moyen sur l’ensemble des catégories
- **2.49x** de baisse de latence moyenne
- taux d’acceptation global autour de **25.16 %**

Le point intéressant : les meilleures hausses apparaissent quand le **taux d’acceptation** est bon. Sur **RAG**, le PR note même un passage à **4.07x** en débit moyen, avec un speedup de latence à **3.65x**.

### Exemple Qwen3-8B
Le PR donne aussi un cas plus lisible pour les usages interactifs :
- prompt “quicksort” en mode code only : **419.3 t/s** contre **51.9 t/s** en base
- soit **8.08x**
- mais sur un prompt de type explication, le gain tombe nettement

Conclusion simple : **DFlash n’est pas un multiplicateur universel**. Son rendement dépend du prompt, du bloc généré, du mode de pensée et de l’acceptation du draft. Là encore, le matériel et le workload font la loi.

## Impact pour l’écosystème local

Pour les gens qui servent des modèles en local, le signal est fort.

1. **`llama.cpp` élargit sa boîte à outils**  
   Le moteur ne se contente plus de l’inférence classique et de quelques optimisations de kernels. Il devient un terrain d’expérimentation concret pour des méthodes de décodage plus agressives.

2. **Le gain va au-delà du benchmark flatteur**  
   Un speedup spéculatif utile, c’est surtout moins de latence perçue dans le chat, le code assisté, le RAG et les agents.

3. **Le support serveur change la donne**  
   Quand la feature est disponible dans `llama-server`, elle peut finir derrière des outils, des interfaces et des proxies existants sans réécriture lourde.

4. **Le coût de qualification reste réel**  
   DFlash demande un draft model adapté, une conversion propre et un réglage honnête. Les gains peuvent s’évaporer si l’acceptation chute ou si le modèle cible n’est pas un bon candidat.

## Limites honnêtes

Il faut éviter le réflexe “8x donc partout”. Ce serait confortable, et donc faux.

Les limites les plus évidentes :
- le gain varie fortement selon le type de tâche
- un draft plus lourd peut rogner l’intérêt sur certaines machines
- la qualité du draft et du verifier conditionne tout
- les configurations multi-backend restent plus fragiles que la moyenne des slides de conférence

En pratique, DFlash ressemble à un bon outil pour les setups où la latence compte vraiment et où l’on peut investir un peu de tuning. Pas un bouton magique. Les boutons magiques n’existent que dans les README trop enthousiastes.

## Ce qu’il faut surveiller maintenant

La vraie question, ce n’est pas “est-ce rapide sur un bench ?”. C’est :
- quels modèles GGUF auront un chemin DFlash propre ?
- quelle sera la stabilité en charge longue ?
- est-ce que l’acceptation reste correcte sur des prompts agents et RAG ?
- est-ce que d’autres runtimes locaux suivent la même voie ?

Si la réponse est oui, DFlash peut devenir une brique utile de plus dans la pile local-first. Sinon, ce sera un bon papier de plus avec un joli tableau et peu d’impact opérationnel. On a déjà connu pire, et plus cher.

## Sources

- PR GitHub `#22105` : https://github.com/ggml-org/llama.cpp/pull/22105
- Releases `ggml-org/llama.cpp` : https://github.com/ggml-org/llama.cpp/releases
