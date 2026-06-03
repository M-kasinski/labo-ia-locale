---
title: "Ollama 0.24 branche Codex App sur les modèles locaux"
description: "Ollama 0.24 permet de lancer Codex App avec des modèles locaux ou auto-hébergés. Pratique pour le code agentique, mais pas magique."
pubDate: 2026-05-30
tags: ["Ollama", "Codex", "coding", "agents locaux", "Apple Silicon"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub — Ollama release v0.24.0"
    url: "https://github.com/ollama/ollama/releases/tag/v0.24.0"
  - label: "GitHub — Ollama releases"
    url: "https://github.com/ollama/ollama/releases"
  - label: "WebsCraft — Ollama + Codex App overview"
    url: "https://webscraft.org/blog/ollama-024-codex-app-yak-zapustiti-lokalniy-ai-coding-agent?lang=en"
---

Ollama 0.24 ajoute une intégration qui mérite l’attention des développeurs qui veulent garder leurs workflows de code plus près de leur machine : le support de **Codex App**, lancé par la commande `ollama launch codex-app`. D’après la release officielle, Ollama décrit Codex App comme l’expérience desktop d’OpenAI pour travailler sur des fils Codex en parallèle, avec support des worktrees et fonctionnalités Git intégrées.

La nouveauté n’est pas simplement “un modèle de code de plus”. C’est plutôt un pont entre une interface d’agent de développement assez structurée — navigateur intégré, revue de code, commentaires, itérations — et des modèles servis par Ollama. Pour l’IA locale, c’est intéressant parce que la bataille se déplace du pur runtime vers l’ergonomie : moins de friction pour passer d’un modèle local à un workflow de correction, inspection et génération de code.

## Ce que fait concrètement Ollama 0.24

La release `v0.24.0`, publiée le 14 mai 2026 sur GitHub, liste explicitement le support de Codex App. La commande documentée est courte :

```bash
ollama launch codex-app
```

La même page indique aussi une commande de restauration :

```bash
ollama launch codex-app --restore
```

Cette seconde commande est utile parce que le lancement modifie la configuration utilisée par Codex App pour pointer vers Ollama. Le détail exact de cette configuration dépend de l’environnement, mais l’intention est claire : permettre à Codex App de parler à un backend local ou compatible, plutôt que de forcer un chemin unique vers une API distante.

Ollama mentionne plusieurs fonctions de Codex App : chargement de serveurs de développement locaux dans un navigateur intégré, annotation visuelle de pages, revue de code dans l’application, commentaires et itération sans quitter l’espace de travail. Dit autrement : on parle d’un outil de coding agentique orienté projet, pas d’un simple chat collé à un éditeur.

## Les modèles recommandés : local ne veut pas dire petit

La release distingue des modèles pour tâches difficiles et des modèles utilisables localement sans abonnement Ollama Cloud. Pour les tâches de code et d’agentique difficiles, Ollama cite notamment **kimi-k2.6** et **glm-5.1**. Pour l’usage local sans abonnement cloud, la release recommande **nemotron-3-super**, **gemma4:31b** et **qwen3.6**.

C’est une information importante : un workflow Codex-like en local n’implique pas forcément un laptop d’entrée de gamme. `gemma4:31b` ou `qwen3.6` peuvent être réalistes sur une machine avec beaucoup de mémoire unifiée ou une grosse carte graphique, mais ce ne sont pas des modèles “ça tourne partout”. Sur un Mac 16 Go, il faudra souvent viser des variantes plus compactes ou quantifiées, au prix d’une baisse de qualité sur les tâches longues et multi-fichiers.

À ce stade, la promesse sérieuse n’est donc pas “tout le monde remplace son abonnement cloud demain”. Elle est plutôt : si tu as déjà une machine capable de servir de bons modèles locaux, Ollama rend l’intégration avec un environnement de code agentique beaucoup plus directe.

## Le point Apple Silicon : le sampler MLX change aussi

La release note ajoute un autre changement, plus discret mais pertinent pour le local : Ollama indique avoir retravaillé le **sampler MLX** pour améliorer la qualité de génération sur **Apple Silicon**. La page officielle ne fournit pas de benchmark détaillé ni de protocole reproductible pour cette amélioration. Il faut donc rester prudent : on peut dire que le changement est listé officiellement, pas qu’il double magiquement les performances ou la qualité.

C’est néanmoins cohérent avec la trajectoire d’Ollama. Depuis plusieurs versions, l’écosystème local ne se contente plus de “faire tourner” des modèles ; il essaie de stabiliser l’expérience sur Mac, machines NVIDIA, stations Linux et, progressivement, workflows d’agents. Un sampler moins capricieux sur MLX peut compter beaucoup dans un contexte Codex App : les agents de code sont sensibles aux petites dérives de génération, surtout quand ils produisent des diffs ou suivent des consignes de revue.

## Pourquoi c’est utile pour l’auto-hébergement

Pour un développeur ou une petite équipe, l’intérêt principal est le contrôle : modèle choisi, logs maîtrisés, données de dépôt moins exposées, coût plus prévisible si l’infrastructure existe déjà. Ce n’est pas une garantie absolue de confidentialité — il faut encore vérifier la configuration réelle, les plugins, les services tiers et les modèles utilisés — mais c’est une meilleure base qu’un workflow entièrement cloud par défaut.

Le second intérêt est l’expérimentation. Ollama donne accès à un catalogue de modèles et à un endpoint local connu. Brancher un outil de coding agentique dessus permet de comparer rapidement plusieurs modèles sur les mêmes tâches : génération de tests, refactor simple, revue de PR, correction d’erreurs TypeScript, migration de composants, etc. Là où un benchmark synthétique donne un signal, un agent dans un vrai dépôt révèle les angles morts : contexte trop court, mauvaise lecture des fichiers, incapacité à maintenir un plan, hallucination de dépendances.

## Les limites à garder en tête

Première limite : Codex App reste une application externe avec son propre comportement. Ollama fournit le pont, pas une garantie que chaque modèle local sera bon en agent de code. Beaucoup de modèles répondent correctement à une question isolée mais s’effondrent quand il faut planifier, modifier plusieurs fichiers, exécuter des tests et revenir sur une erreur.

Deuxième limite : les modèles recommandés pour un usage confortable ne sont pas forcément légers. Le local sérieux demande encore de la mémoire, de bons runtimes et parfois de la patience. Une configuration 32 Go peut être agréable avec des modèles quantifiés de taille moyenne ; les gros modèles de code restent plus à l’aise sur 64, 96, 128 Go de mémoire unifiée ou sur GPU dédié.

Troisième limite : la sécurité. Donner à un agent accès à un dépôt, à Git, à un navigateur local et à des serveurs de dev n’est pas anodin. Même localement, il faut cloisonner : branches dédiées, worktrees, permissions minimales, secrets hors du contexte, tests systématiques. Un agent local peut casser un dépôt aussi efficacement qu’un agent cloud. Il aura juste la courtoisie de le faire chez toi.

## Ce qu’il faut surveiller maintenant

La question décisive sera la qualité des modèles réellement utilisables dans ce workflow. Si `qwen3.6`, `gemma4:31b` ou `nemotron-3-super` tiennent correctement sur des tâches multi-fichiers, l’intégration peut devenir très pratique pour les développeurs local-first. Si les modèles restent instables, l’intérêt sera surtout expérimental.

Il faudra aussi vérifier les prochaines versions d’Ollama : stabilité de `ollama launch`, compatibilité avec les mises à jour Codex App, comportement sur macOS, Windows et Linux, et éventuelles options de configuration plus fines. Pour l’instant, Ollama 0.24 pose une brique intéressante : une interface de coding agentique connue, branchée sur une pile locale. Ce n’est pas encore le majordome autonome qui réécrit ton monorepo sans supervision. Mais c’est une porte de plus hors du tout-API.
