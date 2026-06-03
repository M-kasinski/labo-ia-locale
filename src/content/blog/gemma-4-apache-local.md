---
title: "Gemma 4 passe à Apache 2.0 : le vrai signal pour l’IA locale"
description: "Google publie Gemma 4 en open-weight sous Apache 2.0, avec des modèles edge, un MoE 26B et un dense 31B. Intéressant, mais pas magique côté matériel."
pubDate: 2026-06-02
tags: ["gemma", "open-weight", "local-ai"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Annonce officielle Google DeepMind — Gemma 4"
    url: "https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/"
  - label: "Google Cloud — déploiement Gemma 4 sur Vertex AI, Cloud Run et TPUs"
    url: "https://cloud.google.com/blog/products/ai-machine-learning/gemma-4-available-on-google-cloud"
  - label: "Ars Technica — analyse licence Apache 2.0 et matériel local"
    url: "https://arstechnica.com/ai/2026/04/google-announces-gemma-4-open-ai-models-switches-to-apache-2-0-license/"
---

Google a publié Gemma 4, sa nouvelle famille de modèles open-weight, et le point le plus important n’est pas seulement le score de benchmark affiché dans les slides. Le vrai changement, pour les gens qui veulent faire tourner l’IA chez eux ou dans leur propre infra, c’est la licence : Gemma 4 passe sous Apache 2.0, une licence commercialement permissive, au lieu de la licence Gemma spécifique des générations précédentes [Google][source-google].

C’est un signal assez net. Google ne donne pas son modèle frontier propriétaire, évidemment. Mais il rend une famille Gemma plus simple à intégrer dans des produits, des outils internes, des runtimes locaux ou des stacks d’agents sans devoir relire trois fois une licence maison avec un café trop fort. Pour un écosystème open-weight, ce détail juridique compte presque autant que les tokens par seconde.

## Une famille en quatre formats

Gemma 4 arrive en quatre variantes : Effective 2B, Effective 4B, 26B Mixture of Experts et 31B Dense [Google][source-google]. Les deux petits modèles ciblent l’edge : smartphones, objets connectés, Raspberry Pi, Jetson et machines modestes. Les deux gros modèles visent plutôt les postes de travail, les serveurs locaux musclés et les déploiements cloud contrôlés.

Google positionne le 26B MoE comme le modèle de latence. Il contient 26 milliards de paramètres au total mais n’active qu’environ 3,8 milliards de paramètres pendant l’inférence [Google][source-google]. En pratique, l’intérêt d’un MoE est simple : essayer d’obtenir une qualité proche d’un modèle plus gros, avec un coût de calcul plus proche d’un modèle beaucoup plus petit. Ce n’est pas gratuit — il faut toujours charger les experts et gérer la mémoire — mais c’est une architecture intéressante pour les assistants locaux rapides.

Le 31B Dense, lui, est le modèle de qualité brute. Google le décrit comme une base plus adaptée au raisonnement, au code et au fine-tuning [Google][source-google]. Dense veut dire que tous les paramètres participent à chaque passe d’inférence : plus prévisible, souvent plus simple à servir, mais plus coûteux à faire tourner.

## Long contexte, multimodal et agents

La fiche officielle met l’accent sur trois axes : raisonnement avancé, multimodalité et workflows agentiques [Google][source-google]. Tous les modèles acceptent image et vidéo ; les variantes E2B et E4B ajoutent aussi l’audio natif selon Google. Côté contexte, les modèles edge montent à 128K tokens, tandis que les grands modèles vont jusqu’à 256K tokens [Google][source-google].

Pour l’IA locale, ces chiffres ouvrent des usages concrets : analyse d’un gros dépôt de code, RAG avec moins de découpage agressif, agent qui garde davantage d’historique, ou assistant documentaire capable de traiter des fichiers volumineux. Mais il faut rester sobre : un contexte de 256K tokens ne veut pas dire “gratuitement utilisable sur laptop”. Le KV cache grossit avec la longueur de contexte. Sur une machine locale, la mémoire devient vite le vrai patron. Et le patron n’aime pas qu’on ignore le budget VRAM.

Google met aussi en avant la prise en charge des appels de fonctions, des sorties JSON structurées et des instructions système pour outils et API [Google][source-google]. C’est important parce que les agents locaux ne meurent pas seulement par manque de QI : ils meurent souvent parce qu’ils produisent un JSON bancal, appellent le mauvais outil ou oublient une étape. Un modèle mieux entraîné à ces formats réduit la casse, même si une couche de validation reste nécessaire.

## Le matériel : local, oui, mais pas toujours léger

Le mot “local” est parfois utilisé un peu généreusement. Ars Technica rappelle que les deux grands modèles — 26B MoE et 31B Dense — sont conçus pour tenir en bfloat16 sur une seule NVIDIA H100 de 80 Go [Ars Technica][source-ars]. Techniquement, c’est local. Psychologiquement, pour ton MacBook ou ta RTX de salon, c’est une autre ambiance.

La bonne nouvelle, c’est que les versions quantifiées devraient être beaucoup plus praticables sur des GPU consommateurs [Ars Technica][source-ars]. Mais il faudra attendre des retours solides sur GGUF, MLX, AWQ, GPTQ ou autres formats avant de conclure. Le 26B MoE peut être très séduisant sur le papier grâce à ses 3,8B paramètres actifs, mais la mémoire totale, le routage des experts et la qualité des kernels feront la différence.

Google Cloud indique aussi que Gemma 4 est disponible ou déployable via Vertex AI, Cloud Run, GKE, TPUs et offres souveraines, avec des guides pour fine-tuner et servir Gemma 4 31B sur Vertex AI [Google Cloud][source-cloud]. Ce n’est pas “local” au sens hors-ligne dans un placard, mais c’est pertinent pour les équipes qui veulent garder un contrôle fort sur l’infrastructure et éviter une API fermée unique.

## Pourquoi Apache 2.0 change la donne

La licence Apache 2.0 est le passage le plus concret pour l’écosystème. Ars Technica note que Google abandonne la licence Gemma personnalisée, qui créait des frictions pour certains développeurs, au profit d’un cadre plus standard et permissif [Ars Technica][source-ars].

Pour les projets locaux, ça simplifie beaucoup de choses : intégration dans un produit commercial, distribution dans un runtime, fine-tuning interne, packaging avec un outil desktop, ou hébergement dans une appliance d’entreprise. Les licences ne font pas tourner les matrices plus vite, mais elles déterminent si tu peux réellement utiliser le modèle sans appeler ton juriste à chaque `git push`.

Il faut cependant éviter le raccourci “Apache 2.0 = open-source complet”. Gemma 4 est un modèle open-weight : les poids sont disponibles, mais cela ne signifie pas que toute la recette d’entraînement, les données et l’infrastructure sont publiées. C’est mieux qu’un modèle fermé, mais ce n’est pas équivalent à un projet entièrement reproductible.

## À surveiller pour le local

Le potentiel local de Gemma 4 dépendra maintenant de trois choses.

D’abord, les quantizations. Les petits E2B/E4B devraient vite devenir intéressants pour les machines modestes, les téléphones et les usages embarqués. Le 26B MoE est probablement la variante la plus excitante pour les workstations si les conversions sont propres.

Ensuite, les runtimes. llama.cpp, Ollama, MLX, vLLM et les backends spécialisés devront gérer correctement le MoE, le long contexte et la multimodalité. Un modèle peut être bon sur fiche technique et désagréable à servir si le runtime n’est pas mûr.

Enfin, les benchmarks indépendants. Les classements officiels sont utiles, mais il faut des tests reproductibles : tokens/s, mémoire réelle, qualité en quantization, comportement en tool-use, stabilité sur 64K ou 128K de contexte, et performances sur Apple Silicon ou GPU grand public.

## Verdict provisoire

Gemma 4 n’est pas une baguette magique pour faire tourner un modèle frontier sur un laptop de base. Les grands modèles restent lourds, et les promesses de long contexte devront être vérifiées en usage réel.

Mais la combinaison d’un MoE 26B, de petits modèles edge, de capacités multimodales, de fonctions agentiques et surtout d’une licence Apache 2.0 en fait une release importante pour l’IA locale. Pas parce qu’elle écrase forcément tout le monde aujourd’hui, mais parce qu’elle enlève plusieurs freins pratiques à l’adoption.

À ce stade, le bon réflexe est simple : attendre les conversions sérieuses, tester sur son matériel, et ne pas confondre “open-weight” avec “facile à faire tourner”. Le labo reste ouvert, les ventilateurs aussi.
