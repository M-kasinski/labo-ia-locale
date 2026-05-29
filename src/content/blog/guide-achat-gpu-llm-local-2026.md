---
title: "Guide d'achat GPU 2026 : quelle carte pour un LLM en local"
description: "La grille simple pour choisir une carte graphique selon la VRAM, la taille de modèle et les usages agents sans tomber dans le piège du surdimensionnement."
pubDate: 2026-05-29
tags: ["ia-locale", "gpu", "materiel", "vram"]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "Hugging Face — Meta-Llama-3.1-8B-Instruct GGUF", url: "https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF" }
  - { label: "Hugging Face — Qwen2.5-14B-Instruct GGUF", url: "https://huggingface.co/bartowski/Qwen2.5-14B-Instruct-GGUF" }
  - { label: "Hugging Face — gemma-2-27b-it GGUF", url: "https://huggingface.co/bartowski/gemma-2-27b-it-GGUF" }
  - { label: "Hugging Face — Qwen2.5-32B-Instruct GGUF", url: "https://huggingface.co/bartowski/Qwen2.5-32B-Instruct-GGUF" }
  - { label: "Hugging Face — Meta-Llama-3.1-70B-Instruct GGUF", url: "https://huggingface.co/bartowski/Meta-Llama-3.1-70B-Instruct-GGUF" }
  - { label: "llama.cpp README", url: "https://raw.githubusercontent.com/ggml-org/llama.cpp/master/README.md" }
---

En 2026, acheter une carte graphique pour faire tourner des LLM en local, ce n’est plus une question de prestige. C’est une question de marge. La carte la plus chère n’est pas forcément la bonne : celle qui évite les frustrations réelles, c’est celle qui laisse assez de VRAM pour le modèle, le contexte, les outils et un peu d’air.

La règle simple tient en une phrase : 8 Go = apprentissage et petits modèles, 16 Go = entrée sérieuse, 24 Go = seuil de confort, 32 Go = zone où les workflows agentiques cessent de te punir à chaque itération.

Je parle ici de quantifications 4-bit représentatives, parce que c’est le terrain de jeu le plus réaliste pour un achat “grand public” sans te raconter d’histoires. Les tailles ci-dessous viennent de pages Hugging Face réelles, pas d’une nappe de café.

## La grille de décision, sans poudre aux yeux

| VRAM | Ce que tu peux viser | Taille GGUF 4-bit observée | Lecture pratique |
|---|---:|---:|---|
| 8 Go | 7–8B en Q4 | 8B Q4_K_M ≈ 4,92 Go | Correct pour du chat, du résumé et des assistants courts. Les marges s’évaporent vite dès que tu allonges le contexte ou les logs. |
| 16 Go | 13–14B en Q4 | 14B Q4_K_M ≈ 8,99 Go | Le premier achat que je juge vraiment “sérieux”. Bon équilibre pour un assistant local unique, du code et un peu d’outillage. |
| 24 Go | 27B en Q4, 32B possible selon le contexte | 27B Q4_K_M ≈ 16,65 Go ; 32B Q4_K_M ≈ 19,85 Go | Le vrai seuil de confort. Tu arrêtes de regarder le compteur toutes les trente secondes. |
| 32 Go | 32B en Q4 avec marge ; gros contextes plus respirables | 32B Q4_K_M ≈ 19,85 Go | Le palier où les workflows agents, les longues conversations et les sessions multiples deviennent nettement moins pénibles. |

## 8 Go : le ticket d’entrée, pas le paradis

Avec 8 Go, un 8B en Q4 tient. Un Llama 3.1 8B Instruct en Q4_K_M pèse environ 4,92 Go. Ça laisse un peu plus de 3 Go avant même de parler du reste.

Sur le papier, ça passe. Dans la vraie vie, ça veut dire : prompts courts, contexte modeste, peu de marge pour les outils, et zéro fantasme sur les longues chaînes de réflexion, les gros historiques ou les agents qui enchaînent les appels. Pour un usage “je veux apprendre et tester”, c’est acceptable. Pour un usage quotidien confortable, c’est vite serré.

La bonne nouvelle, c’est qu’un 8 Go n’est pas “inutile”. La mauvaise, c’est qu’il faut être discipliné. Si tu veux un modèle local pour résumer, reformuler, faire un peu d’extraction ou aider dans un IDE sans te ruiner, ça se défend. Si tu veux du multi-agent, tu vas surtout apprendre le mot “compromis”.

## 16 Go : le premier vrai achat

En 16 Go, on passe enfin dans une zone utilisable sans gymnastique permanente. Un 14B en Q4_K_M fait environ 8,99 Go : il reste donc environ 7,01 Go de marge théorique pour le reste.

C’est exactement la différence entre “ça marche” et “je peux m’en servir sans réfléchir à chaque interaction”. Tu peux viser des modèles 13–14B pour un assistant local unique, du code, du RAG léger, des résumés un peu sérieux, et des petits workflows agentiques tant que tu ne pousses pas le contexte comme un sauvage.

Le point faible de 16 Go, ce n’est pas le modèle nu. C’est tout ce qui gravite autour : historique, système prompt, appels d’outils, sorties intermédiaires, et parfois plusieurs sessions en parallèle. Dès que tu mélanges “long contexte” + “agents” + “gros modèle”, la marge fond vite.

Bref : 16 Go, c’est le plancher respectable. Pas le meilleur rapport tranquillité/prix à long terme, mais un vrai seuil d’entrée pour quelqu’un qui veut du local sans se raconter qu’il fait du 70B.

## 24 Go : le seuil de confort

C’est ici que la plupart des frustrations cessent.

Pourquoi 24 Go sont si souvent recommandés ? Parce que le palier te met dans une zone où un 27B Q4_K_M, à environ 16,65 Go, laisse encore environ 7,35 Go de marge. Même un 32B Q4_K_M, à environ 19,85 Go, ne te colle pas tout à fait au mur : il reste environ 4,15 Go.

Cette marge, ce n’est pas du luxe décoratif. Elle part dans le cache de contexte, les buffers du runtime, les sorties d’outil, les retraits de token, les prompts système et tout ce qui fait qu’un agent n’est pas juste “une complétion un peu longue”.

C’est aussi le palier où tu peux commencer à faire du travail utile avec des modèles plus costauds sans devoir te battre contre la machine. Codebase analysis, assistants qui lisent des documents longs, orchestration d’outils, sessions plus propres, moins de micro-optimisation manuelle. Tu achètes du calme mental. Et ça, curieusement, on le sous-estime toujours au moment du panier.

## 32 Go : quand le contexte cesse d’être l’ennemi

32 Go ne transforment pas magiquement tout en royaume du 70B. Un 70B Q4_K_M pèse environ 42,52 Go : il dépasse donc clairement cette classe de carte. Il faut arrêter là le storytelling.

En revanche, 32 Go changent vraiment la vie sur les modèles de 27B à 32B. Un 32B Q4_K_M à environ 19,85 Go laisse environ 12,15 Go de respiration. Là, tu ne choisis plus constamment entre “modèle correct” et “contexte honnête”. Tu peux garder plus d’historique, absorber des sorties d’outils plus lourdes et faire tourner des workflows agents avec moins de casse.

Le runtime compte aussi. La documentation de llama.cpp montre par exemple un serveur lancé avec `-c 16384 -np 4`, soit 16K de contexte et jusqu’à 4 requêtes concurrentes avec 4096 max context chacune. C’est précisément le genre d’usage où la VRAM n’est plus seulement “la taille du modèle”, mais la réserve qui empêche le système de s’étouffer à la moindre interaction parallèle.

Si ton travail local ressemble à “un seul prompt de temps en temps”, 32 Go relèvent du confort premium. Si tu fais du vrai agentique — plusieurs boucles, plusieurs outils, du contexte long, des sessions qui vivent — 32 Go deviennent vite la première classe économique.

## Mon verdict simple

- 8 Go : seulement si ton budget est serré et que tu assumes un usage léger.
- 16 Go : bon choix pour un assistant local sérieux en 7–14B.
- 24 Go : meilleur point d’équilibre pour 2026 si tu veux éviter les frustrations.
- 32 Go : à viser si tu fais des agents, du contexte long, ou si tu veux travailler sans surveiller la jauge en permanence.
- 70B en Q4 : oublie 32 Go si tu veux un usage propre ; passe à une classe supérieure ou accepte de gros compromis.

Ma réponse la plus honnête tient en une ligne : si tu peux acheter 24 Go, fais-le. Si tu sais déjà que tu vas faire de l’agentique et du long contexte, prends 32 Go. Le reste, c’est souvent du maquillage de contrainte avec un logo plus cher dessus.
