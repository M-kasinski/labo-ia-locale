---
title: "Qwopus3.5-4B-Coder : un agent de code local pour machines modestes"
description: "Qwopus3.5-4B-Coder promet du coding agentique en local avec seulement 4B paramètres. Intéressant pour les laptops 16 Go, mais à lire avec sang-froid."
pubDate: 2026-05-30
tags: ["Qwopus", "modèles locaux", "coding", "agents", "GGUF"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Post X — Kyle Hessling annonce Qwopus3.5-4B-Coder"
    url: "https://x.com/kylehessling1/status/2060428614185955643"
  - label: "Hugging Face — Qwopus3.5-4B-Coder-GGUF"
    url: "https://huggingface.co/Jackrong/Qwopus3.5-4B-Coder-GGUF"
  - label: "Hugging Face — Qwopus3.5-9B-Coder-GGUF"
    url: "https://huggingface.co/Jackrong/Qwopus3.5-9B-Coder-GGUF"
  - label: "GitHub — BenchLocal"
    url: "https://github.com/stevibe/BenchLocal"
  - label: "Hugging Face Space — Neon Snake Qwopus3.5-4B"
    url: "https://huggingface.co/spaces/KyleHessling1/neon-snake-qwopus35-4b"
---

## Le signal faible qui mérite mieux qu'un retweet

Kyle Hessling a publié un signal intéressant pour l'IA locale : **Qwopus3.5-4B-Coder**, un modèle de code compact, orienté agents, disponible en GGUF et pensé pour tourner sur des machines modestes. Le post X parle d'un modèle capable de faire du prototypage HTML/JavaScript très rapide, de servir dans des workflows de nettoyage de données et de tenir des tâches agentiques simples sans sortir l'artillerie lourde.

Le point important n'est pas seulement « encore un modèle 4B ». Des 4B, il y en a déjà une petite ménagerie. Le point intéressant, c'est le positionnement : **un modèle de code local entraîné pour le tool-use, le debugging et les boucles agentiques**, pas juste pour répondre à des exercices de programmation dans un benchmark académique.

Pour Labo IA Locale, c'est exactement le genre de sujet à regarder froidement. Pas parce que Qwopus3.5-4B-Coder va remplacer Claude Code ou Codex demain matin — il ne faut pas vendre des licornes en quantized Q4 — mais parce qu'il illustre une tendance plus importante : les petits modèles spécialisés deviennent assez crédibles pour prendre des micro-tâches locales.

## Ce que revendique le modèle

La fiche Hugging Face décrit Qwopus3.5-4B-Coder comme un modèle dense de **4B paramètres**, basé sur la famille **Qwen3.5 4B**, distribué en **GGUF**. Le modèle cible explicitement l'exécution locale, le debugging, le comportement structuré avec outils, les workflows développeur et les tâches agentiques.

La recette d'entraînement revendiquée combine trois ingrédients :

- **Trace Inversion** : reconstruire des traces de raisonnement apprenables à partir de sorties compressées ;
- **agent trajectories** : exposer le modèle à des boucles avec outils, feedback et corrections ;
- **curriculum SFT** : stabiliser le format et le comportement sous des contextes plus longs.

C'est ce dernier point qui change la lecture. Un modèle de code classique peut écrire une fonction. Un modèle agentique doit aussi comprendre une consigne, choisir une action, produire une sortie exploitable par un outil, lire le résultat, puis corriger. À 4B paramètres, il ne faut pas attendre une autonomie longue sur un gros dépôt. Mais pour des tâches courtes — corriger un snippet, générer une page HTML, manipuler des fichiers structurés, surveiller un service local — c'est beaucoup plus réaliste.

## Pourquoi 4B est un format important

Le format 4B est presque plus intéressant que le modèle lui-même. À cette taille, une quantification GGUF devient manipulable sur des machines ordinaires : laptops 16 Go, vieux GPU, petits serveurs maison, voire certains scénarios mobiles selon runtime et quantization.

La fiche du modèle parle explicitement de **local-first design** pour utilisateurs contraints en ressources. Autrement dit : il ne s'agit pas de battre les gros modèles cloud sur tout, mais d'atteindre un seuil d'utilité où la latence, le coût et la confidentialité deviennent meilleurs que l'appel API.

C'est la promesse la plus crédible : pas « meilleur modèle », mais **modèle assez bon, très proche, très rapide, et privé**. Pour l'IA locale, ce compromis compte plus que le podium absolu.

## Benchmarks : prometteurs, mais à lire avec prudence

Le post de Kyle Hessling met en avant une performance sur **SWE-Bench Mini** : 43,5% de patchs résolus sur les problèmes où le modèle soumet effectivement un patch, et 32,5% si l'on compte aussi les sorties vides ou au mauvais format. C'est un chiffre intéressant pour un 4B, mais il faut garder la nuance : le taux flatteur est conditionné aux cas où le modèle produit une proposition exploitable.

La fiche Hugging Face ajoute aussi des résultats **BenchLocal**. BenchLocal est une application desktop locale, MIT, pensée pour tester des LLM sur des tâches concrètes via des “Bench Packs” comme ToolCall-15, BugFind-15, InstructFollow-15 ou HermesAgent-20. Sur la fiche du 4B, Qwopus3.5-4B-Coder-MTP est annoncé à **82% de moyenne de suite**, contre 74% pour le baseline cité, avec notamment **100/100 sur ToolCall-15** et **71/100 sur BugFind-15**.

Ces chiffres sont encourageants, mais ils ne suffisent pas à conclure que le modèle est robuste en production. Les évaluations locales ont souvent des protocoles spécifiques, des prompts bien cadrés et peu de diversité par rapport au chaos d'un vrai dépôt. C'est un bon signal, pas un tampon ISO 9001 pour agent autonome.

## MTP : la vitesse devient un argument produit

Le post X mentionne aussi une vitesse d'environ **270 tokens/s en Q8 avec MTP** sur RTX 5090, avec possibilité de dépasser 500 tokens/s agrégés en lançant plusieurs requêtes SWE-Bench en parallèle. Ce chiffre dépend évidemment du matériel, du runtime, de la quantization et du contexte. Il ne faut pas le transformer en promesse universelle.

Mais le fond est intéressant : **Multi-Token Prediction** change la sensation d'usage quand le modèle est petit. Sur un gros modèle cloud, on attend parce que le modèle est puissant. Sur un petit modèle local, l'intérêt est inverse : accepter un peu moins d'intelligence pour obtenir des itérations très rapides.

Pour un agent local, la vitesse n'est pas un luxe. Une boucle agentique fait beaucoup d'allers-retours : plan, action, observation, correction. Si chaque tour prend dix secondes, l'expérience devient vite pénible. Si chaque tour est quasi instantané, on peut lancer plusieurs petits agents spécialisés : un pour reformater, un pour tester, un pour extraire, un pour générer des variantes. C'est probablement là que les 4B ont leur carte à jouer.

## Le bon usage : des essaims de petites tâches

Le meilleur angle pour Qwopus3.5-4B-Coder n'est pas “mini développeur autonome”. C'est plutôt : **ouvrier local spécialisé**.

Quelques usages crédibles :

- générer rapidement une petite démo HTML/JS ;
- corriger des erreurs simples dans des scripts ;
- extraire ou transformer des données structurées ;
- produire des patches très courts ;
- aider un agent local à router des outils ;
- faire tourner plusieurs workers sur un serveur personnel.

Le Space Hugging Face partagé autour d'un petit jeu Neon Snake illustre bien cette zone : prototypage visuel rapide, feedback court, résultat inspectable immédiatement. Ce n'est pas de l'ingénierie logicielle profonde. C'est du **temps de cycle compressé**.

## Les limites à ne pas oublier

La fiche Hugging Face précise que Qwopus3.5-4B-Coder est une **release communautaire expérimentale**, destinée à la recherche et aux expériences locales. Elle n'a pas subi une évaluation sécurité complète ni un benchmark généraliste large. C'est important.

Un modèle agentique local peut écrire dans vos fichiers, lancer des commandes, manipuler un dépôt, lire des logs. Même petit, il doit rester confiné : dossier dédié, permissions limitées, validation humaine avant écriture ou push, logs inspectables. Le vrai risque n'est pas qu'un 4B devienne trop intelligent. C'est qu'on lui donne trop de droits parce qu'il paraît inoffensif.

Autre limite : le 4B n'est pas forcément le meilleur choix si vous avez plus de marge mémoire. Dans les réponses autour du post, Kyle Hessling oriente plutôt vers la version **9B** ou vers des variantes plus grosses quand le matériel le permet. Logique : 4B est le format de contrainte, 9B est souvent le meilleur compromis qualité/local.

## Ce que ça annonce

Qwopus3.5-4B-Coder ne révolutionne pas l'IA locale à lui seul. Mais il signale une direction saine : des modèles petits, spécialisés, rapides, capables de suivre un protocole d'outil et de rester utiles dans une boucle courte.

L'avenir local ne sera peut-être pas un seul gros modèle qui fait tout dans un coin du bureau. Ce sera peut-être un **essaim de petits modèles spécialisés**, chacun avec peu de droits, beaucoup de vitesse, et des tâches vérifiables. Moins glamour que “AGI on your laptop”. Beaucoup plus utile.

Et franchement, si un 4B peut déjà écrire un petit jeu, corriger des scripts et aider à piloter des outils sans envoyer chaque prompt dans le cloud, c'est le genre de progrès discret qui finit par compter.

## Sources

- Kyle Hessling — annonce X : https://x.com/kylehessling1/status/2060428614185955643
- Qwopus3.5-4B-Coder-GGUF — Hugging Face : https://huggingface.co/Jackrong/Qwopus3.5-4B-Coder-GGUF
- Qwopus3.5-9B-Coder-GGUF — Hugging Face : https://huggingface.co/Jackrong/Qwopus3.5-9B-Coder-GGUF
- BenchLocal — GitHub : https://github.com/stevibe/BenchLocal
- Neon Snake demo — Hugging Face Space : https://huggingface.co/spaces/KyleHessling1/neon-snake-qwopus35-4b
