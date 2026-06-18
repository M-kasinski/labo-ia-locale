---
title: "llama.cpp b9704 : Metal BF16, SYCL Q1_0 et corrections serveur"
description: "La version b9704 de llama.cpp apporte des améliorations ciblées sur le backend Metal (BF16), le support SYCL pour la quantisation Q1_0, et des corrections importantes du serveur."
pubDate: 2026-06-18
tags: ["llama-cpp", "metal", "sycl", "quantization", "gguf"]
category: "local"
author: "Labo IA"
draft: false
sources:
  - label: "llama.cpp GitHub Releases"
    url: "https://github.com/ggml-org/llama.cpp/releases"
---

## La nouvelle

**llama.cpp b9704**, publié le 18 juin 2026, est la dernière version du moteur d'inférence qui alimente Ollama, LM Studio et une grande partie de l'écosystème GGUF. Trois améliorations techniques méritent attention : validation BF16 sur Metal, multiplication matricielle Q1_0 sur SYCL, et corrections du serveur de routage.

## Analyse technique

### Metal : vérification BF16 dans le kernel concat (b9693)
Le backend Metal inclut maintenant une vérification des capacités matérielles avant d'exécuter les kernels de concatenation en BF16 (Brain Floating Point 16). Avant cette correction, certains GPU Apple Silicon pouvaient rencontrer des erreurs silencieuses ou des artefacts numériques quand le hardware ne supportait pas nativement BF16.

**Pourquoi ça compte :** BF16 offre une précision supérieure à FP16 pour les opérations d'inférence sans les problèmes de sous/dépassement. La vérification garantit que le fallback vers FP32 se fait proprement sur le matériel qui ne supporte pas BF16.

### SYCL : MUL_MAT et OUT_PROD avec Q1_0 (b9699)
Le backend SYCL (OpenCL/Level Zero pour GPU AMD et Intel) supporte maintenant la multiplication matricielle et les produits externes avec la quantisation **Q1_0** — 1 bit par poids.

Q1_0 est extrême : un modèle de 70B params en Q1_0 occupe environ 8,75 Go au lieu de ~140 Go en FP16. La précision chute bien sûr, mais pour certains cas d'usage (embeddings, classification binaire, prototypes), c'est utilisable. L'extension à SYCL signifie que les GPU AMD Radeon et Intel Arc peuvent profiter de cette quantisation.

### Serveur : HTTP 400 sur grammaire invalide (b9704)
Le serveur retourne maintenant une erreur HTTP 400 quand la grammaire Grammar Constraint échoue au parsing, au lieu de laisser passer silencieusement sans contraintes. Un test de régression accompagne cette correction.

### Serveur : router args forwarding (b9702)
Correction d'un bug où les arguments de configuration du routeur n'étaient pas transmis aux instances enfants — critique pour les déploiements multi-modèle avec routing dynamique.

## Impact pour l'écosystème local

Ces changements sont techniques mais importants :
- **Metal BF16** = inférence plus fiable sur Mac, surtout avec les modèles GGUF quantifiés
- **SYCL Q1_0** = ouvre la porte à de l'expérimentation extrême sur GPU AMD/Intel
- **Corrections serveur** = moins de bugs silencieux dans les déploiements multi-modèle

Pour les utilisateurs Ollama/LM Studio, ces améliorations arrivent automatiquement avec les prochaines mises à jour.

## Sources vérifiées

- [llama.cpp Releases — GitHub](https://github.com/ggml-org/llama.cpp/releases)
