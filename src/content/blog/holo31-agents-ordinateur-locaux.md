---
title: "Holo3.1 : H Company pousse les agents d’ordinateur vers le local"
description: "H Company publie Holo3.1, une famille de VLM pour computer-use agents avec tailles de 0.8B à 35B-A3B, function calling et checkpoints quantifiés pour l’inférence locale."
pubDate: 2026-06-03
tags: ["hcompany", "agents", "computer-use", "vlm", "local-ai", "gguf", "qwen"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "H Company — Holo3.1: Fast & Local Computer Use Agents"
    url: "https://hcompany.ai/holo3.1"
  - label: "Hugging Face Blog — Holo3.1: Fast & Local Computer Use Agents"
    url: "https://huggingface.co/blog/Hcompany/holo31"
  - label: "Hugging Face — Hcompany/Holo-3.1-4B model card"
    url: "https://huggingface.co/Hcompany/Holo-3.1-4B"
---

H Company a publié **Holo3.1**, une nouvelle génération de modèles pour **computer-use agents** : des agents capables de lire une interface, comprendre une capture d’écran, cliquer, naviguer, remplir des formulaires et piloter des applications. Ce n’est pas un chatbot généraliste de plus. Le sujet, ici, est plus concret : faire tourner des agents qui interagissent avec des environnements graphiques — web, desktop et mobile — avec une trajectoire assumée vers l’inférence locale.

La sortie mérite l’attention parce qu’elle coche plusieurs cases rarement réunies dans ce domaine : une famille de tailles allant de **0.8B à 35B-A3B**, une base issue de la famille **Qwen**, du **function calling natif**, des sorties structurées, et surtout des checkpoints quantifiés annoncés pour le local : **FP8**, **NVFP4** et **Q4 GGUF**. Le détail n’est pas cosmétique. Pour un agent d’ordinateur, le coût ne se résume pas au nombre de tokens par seconde : chaque étape implique perception, raisonnement, action, attente de l’interface, correction éventuelle. Si le modèle est trop lent ou trop cher, l’agent devient vite un stagiaire sous sédatif. Charmant, mais peu rentable.

## Ce qui change avec Holo3.1

H Company présente Holo3.1 comme une réponse aux limites observées après Holo3. Le constat est assez sain : une bonne performance sur un benchmark ou dans un harness interne ne garantit pas une robustesse en production. Les interfaces varient, les workflows changent, les frameworks d’agents n’appellent pas tous les modèles de la même manière, et le passage du desktop au mobile peut casser des comportements apparemment solides.

La promesse de Holo3.1 se structure donc autour de trois axes : **environnements**, **frameworks d’agents**, et **cibles de déploiement**. Côté environnements, H Company parle explicitement de web, desktop et mobile. Côté framework, Holo3.1 ajoute le **function calling** en plus des sorties JSON structurées déjà utilisées par Holo3. Côté déploiement, la nouveauté importante est l’arrivée de checkpoints optimisés pour l’inférence locale, notamment en **Q4 GGUF**.

La famille publiée couvre plusieurs tailles : **0.8B**, **4B**, **9B** et **35B-A3B**. Le modèle card Hugging Face du 4B décrit Holo3.1 comme une famille de VLM pour agents d’usage d’ordinateur, avec support de l’automatisation web, desktop et mobile, et indique une licence **Apache 2.0** pour cette variante. Les pages officielles relient aussi ces modèles à l’écosystème Hugging Face et à des outils locaux comme llama.cpp, LM Studio, Jan ou Ollama pour certaines variantes quantifiées.

## Les chiffres publiés : utiles, mais à lire froidement

Sur AndroidWorld, H Company annonce une progression forte : le **35B-A3B** passerait de **67 % avec Holo3 à 79,3 % avec Holo3.1**, tandis que les variantes **4B / 9B** seraient autour de **71–72 %**, contre **58 %** pour Holo3 selon les pages officielles. C’est significatif, surtout parce que le mobile est souvent plus instable que le navigateur : densité visuelle, gestes, états d’interface, transitions et composants natifs ne pardonnent pas beaucoup.

H Company affirme aussi que le function calling et l’exécution native atteignent désormais une quasi-parité de performance, et que Holo3.1 améliore de plus de **25 %** les résultats dans le harness produit Holotab. Sur la partie quantization, la société indique que **FP8** et **NVFP4** restent à environ **deux points** du checkpoint BF16 sur OSWorld, et que les optimisations développées avec NVIDIA peuvent réduire le temps moyen d’étape sur DGX Spark de **6,8 s à 3,3 s** dans leur configuration.

Il faut toutefois garder une lecture prudente. Ces chiffres viennent des sources officielles de H Company. Ils sont intéressants, mais pas encore équivalents à une validation indépendante sur des machines de développeurs, des workflows variés, des prompts malpropres et des interfaces capricieuses. Pour le local, le vrai test sera simple : combien d’actions correctes par minute sur un Mac, une RTX grand public ou une petite station Linux, avec un agent qui doit vraiment terminer une tâche ?

## Pourquoi le Q4 GGUF est le signal important

Le détail le plus intéressant pour l’IA locale n’est pas forcément le score AndroidWorld. C’est la disponibilité de formats quantifiés, en particulier **Q4 GGUF**, parce que cela ouvre la porte aux runtimes utilisés par le public local-first. Un modèle de computer-use qui reste coincé dans une API distante peut être utile, mais il perd une partie de son intérêt pour les usages sensibles : automatisation d’outils internes, manipulation de documents privés, accès à des applications métier, données clients, captures d’écran de machines personnelles.

H Company insiste d’ailleurs sur la possibilité d’exécuter localement certains scénarios sans que les données quittent le réseau de l’utilisateur. C’est le cœur du sujet : un agent d’ordinateur voit tout. Il peut lire des fenêtres, des fichiers, des pages internes, des tokens temporaires, des erreurs, parfois des secrets affichés par accident. Le modèle local ne règle pas tout — il faut aussi du sandboxing, des permissions, des journaux d’action et des limites explicites — mais il évite au moins de diffuser les captures et instructions vers un service externe à chaque étape.

La famille multi-tailles est également pertinente. Un **0.8B** ou un **4B** ne remplacera pas un gros modèle sur des workflows complexes, mais peut servir de brique rapide : grounding, classification d’état d’interface, sous-agent spécialisé, pré-filtrage d’actions. Le **35B-A3B** vise plutôt la performance maximale. Le compromis le plus intéressant pourrait se trouver entre les deux, selon la qualité réelle des variantes 4B et 9B une fois quantifiées.

## Les questions encore ouvertes

Première question : la qualité réelle du **grounding**. Un agent d’ordinateur ne doit pas seulement “comprendre” une interface ; il doit cliquer au bon endroit, distinguer deux boutons proches, gérer les états intermédiaires et reconnaître quand une action a échoué. Les benchmarks donnent une indication, mais la robustesse se mesure sur la durée.

Deuxième question : la qualité après quantization. H Company affirme que certaines quantizations restent proches du BF16 sur OSWorld, mais il faudra vérifier la perte sur des tâches longues, avec des captures bruitées et des outils réels. Les modèles GUI peuvent être plus sensibles à la précision que les modèles texte classiques, notamment quand la perception fine est en jeu.

Troisième question : l’orchestration. Holo3.1 est un modèle, pas un système complet de sécurité. Pour un agent local utile, il faut un harness qui contrôle les permissions, demande confirmation avant actions risquées, limite les zones de clic, conserve les traces, et empêche le modèle d’improviser des opérations destructrices. L’agent autonome sans garde-fous reste une excellente manière d’automatiser une catastrophe, avec une interface plus moderne.

## À surveiller maintenant

Holo3.1 est une sortie sérieuse parce qu’elle prend le computer-use par le bon bout : pas seulement le score, mais le déploiement, les formats, les tailles et l’intégration. Pour le Labo, les tests prioritaires seront les variantes quantifiées, surtout en **Q4 GGUF**, sur des workflows simples mais réels : navigation web, manipulation de formulaires, extraction depuis interfaces métier, et tâches mobiles si un harness local fiable existe.

Le résumé honnête : **Holo3.1 ne prouve pas encore que les agents d’ordinateur locaux sont mûrs, mais il rapproche clairement le domaine d’un usage praticable hors cloud**. Et pour une technologie qui voit littéralement ton écran, ce n’est pas un détail. C’est peut-être même le détail principal.

## Sources

- H Company — Holo3.1: Fast & Local Computer Use Agents: https://hcompany.ai/holo3.1
- Hugging Face Blog — Holo3.1: Fast & Local Computer Use Agents: https://huggingface.co/blog/Hcompany/holo31
- Hugging Face — Hcompany/Holo-3.1-4B model card: https://huggingface.co/Hcompany/Holo-3.1-4B
