---
title: "Claude Opus 4.7 s’attaque à la RMN : un vrai test de chimie, pas une démo de chatbot"
description: "Anthropic publie un white paper où Claude Opus 4.7 rivalise avec ChemDraw et MestReNova sur des tâches de RMN, avec des résultats intéressants mais encore à lire comme une évaluation contrôlée."
pubDate: 2026-06-07
category: "veille"
tags: ["modèles", "science", "chimie"]
author: "Veille IA"
draft: false
sources:
  - label: "Anthropic Research — Making Claude a chemist"
    url: "https://www.anthropic.com/research/making-claude-a-chemist"
  - label: "White paper Anthropic sur Claude et la RMN"
    url: "https://www-cdn.anthropic.com/07441e654ad3dfeb0cd090e9361511562825d012.pdf"
  - label: "Annonce Claude Opus 4.7"
    url: "https://www.anthropic.com/news/claude-opus-4-7"
---

Anthropic a publié le 5 juin un billet de recherche intitulé **“Making Claude a chemist”**, accompagné d’un white paper consacré à une tâche très concrète : l’analyse de spectres de **RMN** — résonance magnétique nucléaire, ou NMR en anglais. Ce n’est pas le terrain habituel des annonces de modèles, où l’on jongle avec des scores globaux et des barres de benchmarks plus ou moins digestes. Ici, Anthropic teste Claude Opus 4.7 sur un morceau de travail de laboratoire : prédire des spectres à partir de structures moléculaires, puis faire l’inverse, c’est-à-dire proposer une structure à partir de données spectrales.

C’est intéressant parce que la chimie n’est pas seulement une affaire de texte. Un chimiste navigue entre structures dessinées, noms systématiques, chaînes SMILES, données instrumentales, articles, brevets et résultats d’expériences. Le problème n’est pas de “savoir parler chimie”, mais de traduire correctement entre ces représentations sans perdre le détail qui change tout. En chimie organique, une petite différence de structure peut changer la réactivité, la toxicité ou l’activité biologique. Le modèle n’a donc pas le droit au flou artistique. Même avec un joli raisonnement, une molécule fausse reste une molécule fausse.

## Ce qu’Anthropic a réellement testé

Le white paper compare trois modèles Claude — **Opus 4.7**, **Opus 4.6** et **Sonnet 4.6** — à deux outils spécialisés : **ChemDraw** et **MestReNova**. Le jeu principal porte sur **20 composés** tirés de prépublications ChemRxiv en chimie de synthèse. D’après Anthropic, les composés ont été sélectionnés après la coupure d’entraînement des modèles afin de limiter le risque que Claude ait simplement vu les réponses pendant son pré-entraînement.

La première tâche est la **prédiction directe** : on donne une structure, le système prédit le spectre RMN attendu. C’est le type d’usage où ChemDraw et MestReNova sont déjà des outils de bureau classiques pour beaucoup de chimistes. L’évaluation regarde notamment les déplacements chimiques en ppm pour le proton et le carbone, les multiplicités et les constantes de couplage.

Le résultat mis en avant est net, mais il faut le lire précisément. Sur les déplacements **¹H RMN**, Opus 4.7 obtient dans le white paper une **MAE de 0,079 ppm**, meilleure que les autres outils testés sur cet échantillon. Sur **¹³C RMN**, Anthropic rapporte une performance comparable entre Opus 4.7 et MestReNova : **1,37 ppm** de MAE pour Opus 4.7 contre **1,48 ppm** pour MestReNova sur les 20 composés. Le billet résume cela en disant que, pour la prédiction de routine, Opus 4.7 est “aussi bon ou meilleur” que ChemDraw et MestReNova en moyenne.

Ce n’est pas anodin. ChemDraw et MestReNova ne sont pas des gadgets marketing : ce sont des logiciels spécialisés, conçus pour ce type de travail. Voir un modèle généraliste arriver à ce niveau sur un protocole public mérite attention. Pas de champagne automatique, mais au moins un sourcil levé.

## Le plus intéressant : l’inverse

La partie la plus forte n’est peut-être pas la prédiction directe. Anthropic teste aussi la **structure elucidation**, le problème inverse : on donne des données RMN et HRMS, le modèle doit proposer la structure moléculaire sous forme de SMILES. Cette tâche est plus proche du raisonnement expert. ChemDraw ne fait pas cela. MestReNova aide à assigner des pics à une structure connue, mais ne génère pas simplement la bonne molécule à partir d’une liste de pics comme le ferait un chimiste en train de résoudre un puzzle expérimental.

Sur cette partie, Anthropic évalue Opus 4.7 sur **15 cibles publiées**, issues du même réservoir de prépublications. Le papier indique que, avec les données 1D RMN et HRMS seules, Opus 4.7 récupère la cible publiée à chaque tentative pour les échafaudages les plus simples. Pour les structures plus denses, l’ajout des **SMILES des matériaux de départ**, sans autre contexte réactionnel, suffit au modèle pour atteindre la bonne structure sur la plupart ou toutes les tentatives selon les cas.

C’est probablement le signal le plus important : Claude n’est pas seulement utilisé comme interpolateur de valeurs spectrales, mais comme assistant de raisonnement chimique capable de combiner masse exacte, pics RMN et contraintes de synthèse. En pratique, c’est ce que font les chimistes : ils ne lisent pas un spectre dans le vide, ils le lisent avec l’historique de la réaction, les réactifs, les impuretés plausibles et leur intuition du mécanisme.

## Pourquoi ça compte pour les modèles frontier

Ce papier illustre une tendance plus large : les meilleurs modèles ne cherchent plus seulement à être “bons en science” via des QCM ou des problèmes d’olympiades. Ils commencent à attaquer des interfaces de travail réelles, avec des formats imparfaits et des tâches où la valeur vient de l’intégration.

Anthropic insiste sur un point raisonnable : Claude peut devenir utile dans le travail quotidien de traduction, de rappel et d’intégration qui accompagne le jugement du chimiste. C’est moins spectaculaire que “l’IA découvre un médicament seule”, mais beaucoup plus crédible. Si un modèle peut raccourcir l’analyse de spectres, aider à vérifier une structure ou proposer des hypothèses à tester, il devient un outil de productivité scientifique concret.

Le contexte rend cette direction évidente. Le billet rappelle que le registre CAS dépasse **290 millions de substances divulguées** et croît d’environ **15 000 substances par jour**. Aucun humain ne peut naviguer tout cela manuellement. Les modèles multimodaux et raisonneurs peuvent devenir une couche de traduction entre les bases, les articles, les figures, les instruments et les formats de représentation moléculaire.

## Les limites à garder en tête

Il y a cependant plusieurs précautions. D’abord, l’échantillon est petit : **20 composés** pour la prédiction directe, **15** pour l’inverse. C’est suffisant pour un white paper exploratoire, pas pour déclarer que les logiciels spécialisés sont obsolètes. Ensuite, les composés ont été sélectionnés manuellement et viennent d’un périmètre précis de chimie de synthèse. Le résultat peut ne pas se généraliser à toutes les familles chimiques, à des spectres bruités, à des mélanges, ou à des cas où les données expérimentales sont incomplètes.

Ensuite, le protocole reste publié par Anthropic. Ce n’est pas une critique morale ; c’est juste une hygiène de lecture. Les chiffres importants devront être reproduits par des équipes indépendantes, idéalement avec des jeux de données plus larges, des spectres réels plus sales, et des comparaisons incluant d’autres outils de structure elucidation.

Enfin, l’usage en laboratoire devra intégrer l’auditabilité. Un modèle qui propose une structure plausible mais fausse peut faire perdre du temps, voire orienter une décision expérimentale dans la mauvaise direction. La bonne interface ne sera pas seulement “voici la réponse”, mais “voici les pics qui soutiennent cette structure, les alternatives plausibles, et les points faibles de l’hypothèse”.

## Le signal à retenir

Le résultat ne dit pas que Claude devient chimiste autonome. Il dit quelque chose de plus précis : sur un sous-problème réel, mesurable et pénible de la chimie organique, un modèle généraliste frontier commence à rivaliser avec des outils spécialisés, tout en prenant en charge une partie du raisonnement inverse que ces outils ne couvrent pas directement.

C’est exactement le type d’évaluation qu’il faut surveiller : petite, technique, imparfaite, mais ancrée dans un workflow professionnel. Moins de paillettes, plus de spectres. Franchement, la science y gagne.

## Sources

- Anthropic Research — “Making Claude a chemist” : https://www.anthropic.com/research/making-claude-a-chemist
- White paper Anthropic sur Claude et la RMN : https://www-cdn.anthropic.com/07441e654ad3dfeb0cd090e9361511562825d012.pdf
- Annonce Claude Opus 4.7 : https://www.anthropic.com/news/claude-opus-4-7
