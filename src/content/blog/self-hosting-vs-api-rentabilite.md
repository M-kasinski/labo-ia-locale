---
title: "Self-hosting ou API : le vrai calcul de rentabilité"
description: "Une méthode simple pour comparer achat GPU, électricité, temps humain et facture API avant de décider."
pubDate: 2026-05-29
category: "local"
tags: ["ia-locale", "self-hosting", "couts", "decision"]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "OpenAI API pricing", url: "https://developers.openai.com/api/docs/pricing" }
  - { label: "NVIDIA GeForce RTX 4090 (prix public FR)", url: "https://www.nvidia.com/fr-fr/geforce/graphics-cards/40-series/rtx-4090/" }
  - { label: "NVIDIA newsroom RTX 4090 (450W)", url: "https://nvidianews.nvidia.com/news/nvidia-delivers-quantum-leap-in-performance-introduces-new-era-of-neural-rendering-with-geforce-rtx-40-series" }
  - { label: "EDF Tarif Bleu, grille de prix au 1er février 2026", url: "https://particulier.edf.fr/content/dam/2-Actifs/Documents/Offres/Grille_prix_Tarif_Bleu.pdf" }
---

Self-hosting n’est pas une vertu. C’est un achat de capacité.

Et comme pour n’importe quel achat de capacité, la bonne question n’est pas “est-ce que c’est cool ?”, mais “est-ce que ça revient moins cher que de payer à l’usage, sans me rajouter une couche d’ennui”.

Pour une équipe, le calcul propre tient en quatre morceaux : CapEx, OpEx, volume mensuel de tokens, et coût réel du temps humain. Le reste est du bruit.

## Le calcul qu’il faut faire, pas celui qu’on aime raconter

La formule simple est celle-ci :

Coût local mensuel = amortissement du matériel + électricité + maintenance + temps humain

Coût API mensuel = (tokens d’entrée x prix entrée) + (tokens de sortie x prix sortie)

Le point de rupture arrive quand le coût local mensuel passe sous le coût API mensuel pour votre usage réel.

La première erreur, c’est de comparer un GPU “qui peut tourner” à une API “qui tourne vraiment”. Un serveur local coûte aussi quand il dort. L’électricité continue. Le matériel s’use. Et il faut bien quelqu’un pour gérer les drivers, les mises à jour, les OOM, les redémarrages et les petits drames qui ne figurent jamais dans les slides.

La deuxième erreur, c’est d’oublier le mix entrée/sortie. Un million de tokens n’a pas le même prix si c’est surtout du contexte long ou surtout de la génération. Le calcul juste se fait avec votre profil d’usage, pas avec un chiffre rond sorti d’un groupe Telegram.

## Les chiffres de référence que j’utilise ici

Pour garder l’exemple concret, je prends des sources officielles et je pose ensuite des hypothèses explicitement marquées comme telles.

Côté API, OpenAI affiche sur sa page de pricing gpt-4o-mini à 0,15 $ par million de tokens en entrée et 0,60 $ par million de tokens en sortie. La même page donne gpt-4.1-mini à 0,40 $ en entrée et 1,60 $ en sortie.

Côté matériel, NVIDIA affiche la GeForce RTX 4090 à partir de 1 779 € sur sa page française, et sa newsroom indique une consommation de 450 W pour la carte.

Côté électricité, EDF publie pour Tarif Bleu, option Base, 19,40 cts € TTC/kWh pour 3 kVA et 6 kVA, puis 19,27 cts € TTC/kWh à partir de 9 kVA. Pour l’exemple, je prends 19,40 cts/kWh.

## Exemple chiffré, avec hypothèses transparentes

Je pars d’un cas simple. C’est un exemple, pas une vérité universelle.

Hypothèses :
- machine self-hostée à 2 500 € au total, avec une RTX 4090 dans le lot
- amortissement sur 36 mois
- puissance moyenne du serveur à 500 W au mur, donc un peu au-dessus de la seule carte, pour rester prudent côté électricité
- utilisation continue, 24 h/24, 30 jours par mois
- maintenance et temps humain à 75 € par mois, hypothèse modeste pour une équipe qui ne veut pas se transformer en support GPU à plein temps
- par souci de lisibilité, je prends 1 € ≈ 1 $ dans cet exemple. Ce n’est pas un audit comptable, juste un ordre de grandeur pour décider vite
- profil de charge à 50 % d’entrée et 50 % de sortie

Avec ça :
- amortissement matériel : 2 500 / 36 = 69,4 € par mois
- électricité : 0,5 kW x 720 h x 0,194 €/kWh = 69,8 € par mois
- maintenance et temps humain : 75 € par mois

Total local : environ 214 € par mois.

Maintenant la facture API.

Avec un mix 50/50, gpt-4o-mini revient à 0,375 $ par million de tokens, soit environ 0,375 € dans l’hypothèse de parité ci-dessus. Le seuil de rentabilité est donc autour de 214 / 0,375 = 571 millions de tokens par mois.

Avec gpt-4.1-mini, le même mix donne 1,00 $ par million de tokens. Le seuil tombe à environ 214 millions de tokens par mois.

Voilà le vrai point : le local ne devient pas magique au premier million de tokens. Avec une API bon marché, il faut beaucoup de volume. Avec une API plus chère, le seuil descend vite.

## Ce que ça veut dire en pratique

Le local devient rationnel quand trois conditions se rencontrent.

Premièrement, le volume est stable. Si votre usage est irrégulier, l’API garde l’avantage. Vous ne payez pas pour une machine qui attend. C’est trivial, mais c’est souvent là que les équipes se racontent une histoire trop optimiste.

Deuxièmement, le modèle choisi en API n’est pas le moins cher. Si vous passez votre temps sur un modèle “mini” pour des tâches classiques, la facture API reste difficile à battre. Si vous avez besoin d’un modèle plus coûteux, ou si vous envoyez beaucoup de contexte à chaque requête, le calcul change plus vite.

Troisièmement, vous acceptez le coût d’exploitation. Un GPU local qui fait gagner 100 € par mois sur la facture peut très bien être une mauvaise affaire si quelqu’un passe deux heures de plus par mois à le maintenir. À 50 € de l’heure, l’addition est vite faite.

## Tableau de seuils, à partir de l’exemple ci-dessus

Je garde le même cadre : machine à 214 € par mois, mix 50/50, et parité 1 € ≈ 1 $ pour l’illustration.

| Volume mensuel | gpt-4o-mini | gpt-4.1-mini | Lecture |
|---|---:|---:|---|
| 50 M tokens | ~19 € | ~50 € | l’API gagne largement |
| 150 M tokens | ~56 € | ~150 € | l’API reste plus maligne |
| 250 M tokens | ~94 € | ~250 € | zone grise, local possible sur API plus chère |
| 600 M tokens | ~225 € | ~600 € | local pertinent, surtout face aux modèles plus chers |

Le message n’est pas “self-host partout”. Le message est “ne saute pas sur un GPU avant d’avoir fait le compte”.

## Quand l’API reste le meilleur choix

L’API gagne presque toujours si :
- votre usage est sporadique
- vous avez peu de tokens par mois
- vous voulez éviter toute charge ops
- vous changez souvent de modèle
- vous avez besoin de la meilleure qualité disponible sur des tâches difficiles

Dans ce scénario, acheter du matériel est une mauvaise façon d’acheter de la tranquillité. Vous financez un actif qui dort.

## Quand le local devient raisonnable

Le local commence à avoir du sens si :
- vous avez un volume régulier et élevé
- vous pouvez garder la machine occupée
- la confidentialité ou la résidence des données compte vraiment
- vous voulez maîtriser le comportement du modèle, ses versions, sa latence, ses limites
- vous avez déjà une équipe capable d’assumer l’exploitation

À ce stade, la question n’est plus “API ou local ?”. Elle devient “combien de notre volume mérite d’être internalisé, et quelle part reste plus intelligente à déléguer”. Souvent, la bonne réponse est hybride : local pour le flux récurrent, API pour les cas durs. C’est moins sexy qu’un manifeste, mais c’est généralement ce qui tient debout.

## La règle simple à retenir

Si votre facture API mensuelle est encore loin de 200 € à 300 €, n’achetez pas un GPU pour faire des économies. Vous risquez surtout d’acheter de la complexité.

Si vous dépassez plusieurs centaines de millions de tokens par mois, que l’usage est stable, et que vous avez quelqu’un pour opérer le bazar proprement, le local commence enfin à être rationnel.

En dessous, l’API reste souvent plus maligne. Au-dessus, le self-hosting devient un vrai sujet. Entre les deux, il faut compter. Pas espérer.
