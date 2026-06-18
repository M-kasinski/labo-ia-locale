---
title: "Consilium : utiliser le désaccord entre modèles comme signal, pas comme bug"
description: "Un préprint propose un protocole de délibération multi-modèles inspiré de la tolérance aux fautes byzantines. Prometteur sur le papier, mais à lire comme une piste de recherche, pas comme un arbitre de vérité."
pubDate: 2026-06-03
category: "veille"
tags: ["recherche", "multi-agents", "evaluation", "raisonnement", "alignment"]
author: "Veille IA"
draft: false
sources:
  - label: "arXiv — Emergent Collaborative Deliberation in Multi-Model AI Systems"
    url: "https://arxiv.org/abs/2606.00005"
  - label: "Zenodo — Consilium Protocol preprint record"
    url: "https://doi.org/10.5281/zenodo.19229039"
  - label: "arXiv PDF — Consilium Protocol"
    url: "https://arxiv.org/pdf/2606.00005"
---

La plupart des systèmes multi-modèles cherchent à faire disparaître le désaccord. On demande plusieurs réponses, on vote, on agrège, on choisit la sortie majoritaire ou la plus confiante. C’est pratique, mais cela suppose que la divergence entre modèles est surtout du bruit. Le préprint **“Emergent Collaborative Deliberation in Multi-Model AI Systems”**, disponible sur arXiv sous l’identifiant **2606.00005**, propose l’inverse : traiter le désaccord comme un **signal épistémique**.

Le protocole décrit, nommé **Consilium**, s’inspire de la tolérance aux fautes byzantines — les protocoles distribués qui cherchent à produire un accord malgré des nœuds défaillants ou adversariaux. Mais l’objectif n’est pas de faire voter des modèles jusqu’à produire une vérité officielle. L’auteur, VD Doske, présente plutôt une architecture de délibération structurée : plusieurs modèles, plusieurs “personas” cognitives, des phases d’attaque et de défense de claims, puis une validation out-of-sample par recherche de preuves externes.

C’est une proposition intéressante, mais il faut poser le cadre tout de suite : il s’agit d’un **préprint**, avec une seule signature, sans validation indépendante évidente à ce stade. Les chiffres rapportés sont donc à lire comme des résultats expérimentaux à vérifier, pas comme une loi générale sur les LLM. L’idée mérite toutefois qu’on s’y arrête, parce qu’elle touche un point central de l’IA actuelle : comment auditer une réponse quand tous les modèles ont potentiellement appris des corpus convergents, synthétiques et partiellement contaminés ?

## Le désaccord comme spread informationnel

L’intuition de Consilium est simple : une sortie unique de modèle ressemble à un prix de clôture. Elle donne une réponse, mais elle masque l’incertitude, les conflits d’interprétation et les zones où le modèle récite un consensus mou. En finance, un marché n’est pas seulement défini par son dernier prix ; le spread bid-ask, la profondeur et la liquidité disent aussi quelque chose sur l’état de l’information.

Consilium transpose cette idée aux modèles. Au lieu de demander “quel modèle a raison ?”, le protocole observe où et comment les modèles divergent. Un désaccord robuste peut signaler une question mal posée, un manque de données, une ambiguïté normative, ou un biais introduit par l’alignement et les données d’entraînement. C’est plus subtil qu’un vote majoritaire. Parfois, la minorité modèle-persona contient justement la partie intéressante.

Le papier insiste sur une formule prudente : le protocole ne prétend pas produire “la vérité”. Il produit une **chaîne de claims testée**, où chaque assertion passe par challenge, défense et recherche de preuves. Cette nuance compte. Dans un écosystème saturé de contenu généré, vouloir un ministère algorithmique de la vérité serait aussi élégant qu’un pare-feu en papier. Cartographier les désaccords est une ambition plus modeste, et probablement plus utile.

## Modèles et personas : séparer ce qui raisonne de comment ça raisonne

L’un des choix les plus discutables — mais aussi les plus stimulants — du papier est la séparation entre le modèle sous-jacent et la **persona cognitive** qui lui est assignée. En clair, un même LLM peut jouer un rôle de critique adversarial, de synthétiseur, d’empiriste prudent, de scout chargé de chercher des preuves externes, etc.

Le préprint affirme que, dans les expériences rapportées, la persona explique davantage le comportement épistémique que l’identité du modèle. C’est fort. Selon le résumé arXiv et l’enregistrement Zenodo, des modèles edge gratuits coûtant environ **0,0002 dollar par batch** auraient produit une sortie analytique comparable à celle de modèles frontier coûtant **10,69 dollars** dans certaines conditions du protocole.

Il faut être précis : “comparable” ne veut pas dire “équivalent sur toutes les tâches”. Cela signifie que dans cette architecture particulière, avec ces métriques et ces sujets, la structure de délibération et le rôle assigné peuvent réduire l’écart apparent entre modèles. Si ce résultat se réplique, l’implication est importante : pour certaines tâches d’analyse, le **protocole d’orchestration** pourrait compter autant que le choix du modèle le plus cher.

Mais c’est exactement le type de claim qui demande réplication. La qualité d’une persona dépend du prompt, de la tâche, du modèle, du juge et de la méthode d’évaluation. On connaît la chanson : avec assez de variables, un benchmark peut vite devenir un costume sur mesure. Beau costume, certes. Mais à reprendre aux épaules.

## Les chiffres rapportés

Le papier revendique une batterie de **1 478 sessions de délibération**, couvrant **32 sujets** dans **10 catégories**. Le PDF mentionne aussi **17 modèles actifs**, **29 personas**, **8 990 claims** dans le registre, **239 claims out-of-sample validés** et **167 découvertes de blind spots**. Le coût total annoncé est d’environ **217 dollars**, overhead compris.

Deux résultats attirent particulièrement l’attention.

Le premier concerne les effets de l’alignement RLHF. Le préprint rapporte que les sujets politiques contestés reçoivent **12,3 points de pourcentage** de challenge adversarial en moins que des sujets scientifiques stabilisés. Sur les sujets liés à la sûreté de l’IA, il rapporte aussi une asymétrie : les modèles contesteraient plus vigoureusement les claims disant que “l’IA est dangereuse” que les claims disant que “le risque IA est exagéré”, avec un delta annoncé de **11,6 %**.

Le deuxième concerne la robustesse du protocole lui-même. L’auteur indique que Consilium ne montre pas de biais directionnel marqué sur des paires non liées à l’IA, avec des deltas annoncés de **2,3 %** sur l’immigration et **1,2 %** sur les renouvelables. La reproductibilité run-to-run sur assignations aléatoires modèle × persona serait autour de **±2,2 %** d’écart-type moyen.

Ces chiffres sont suffisamment précis pour être intéressants, mais pas suffisamment indépendants pour être conclusifs. Ils ouvrent une piste : les modèles alignés pourraient avoir des “angles morts épistémiques” mesurables, non pas seulement des refus ou des biais de surface. Mais la conclusion solide, pour l’instant, est plus sobre : le protocole fournit une manière structurée de chercher ces effets.

## Out-of-sample : la partie la plus saine du protocole

Le composant le plus important de Consilium est peut-être l’**In-Sample / Out-of-Sample validation**, empruntée à la logique quantitative. Le protocole distingue ce qui ressemble à un consensus issu des données d’entraînement de ce qui peut être validé par des preuves externes retrouvées après coup.

Dans les expériences rapportées, la phase out-of-sample aurait validé **239 claims** avec **100 % de retrieval evidence** et révélé **167 blind spots** invisibles pendant la délibération sur données internes. Là encore, le “100 %” demande prudence : il dépend de ce qui est compté comme evidence retrieval et de la sélection des claims. Mais le principe est bon. Sans validation externe, un panel de modèles peut simplement amplifier le même corpus latent. Cinq LLM qui répètent la même page web oubliée ne font pas une triangulation ; ils font une chorale.

Cette distinction est particulièrement pertinente pour les workflows agentiques. Un agent de recherche utile ne doit pas seulement produire une réponse convaincante. Il doit maintenir un registre de claims, expliciter le statut de preuve, identifier les désaccords et déclencher des recherches externes quand la délibération interne devient circulaire.

## Ce que Consilium dit de l’avenir des agents

Consilium n’est pas un produit prêt à intégrer tel quel dans un assistant de bureau. C’est une architecture de recherche. Mais elle pointe vers une tendance plus large : les systèmes agentiques vont devoir apprendre à gérer l’incertitude autrement que par “répondre avec confiance” ou “demander à un modèle plus gros”.

Dans les workflows complexes — due diligence, veille scientifique, analyse réglementaire, sécurité, stratégie produit — la réponse finale compte moins que le chemin de vérification. Quels claims ont été contestés ? Par quels rôles ? Avec quelles preuves externes ? Où le système a-t-il trouvé un consensus faible, et où a-t-il identifié une vraie contradiction ?

C’est là que le désaccord devient une ressource. Un système multi-modèles bien conçu ne devrait pas effacer les divergences trop tôt. Il devrait les instrumenter, les classer, les tester. Le vote majoritaire est utile pour certaines décisions rapides. Pour comprendre un sujet instable, il peut être trop brutal.

## Les limites à surveiller

Les limites sont nettes. Le préprint n’est pas, à ma connaissance, évalué par les pairs. Les résultats viennent d’un protocole conçu par l’auteur. Les métriques de qualité analytique restent difficiles à objectiver. Les personas peuvent introduire leurs propres biais. Et la validation externe dépend fortement des outils de retrieval et des critères de preuve.

Il faut aussi éviter une confusion classique : une architecture inspirée de la BFT n’hérite pas automatiquement des garanties formelles de la BFT. Les nœuds ne sont pas des processus déterministes dans un réseau distribué ; ce sont des modèles probabilistes, sensibles aux prompts, aux contextes et aux politiques d’alignement. L’analogie est utile, mais elle ne doit pas devenir un vernis mathématique.

Malgré cela, Consilium est une piste intéressante parce qu’elle déplace la question. Au lieu de demander quel modèle est “le plus intelligent”, elle demande comment structurer une conversation entre modèles pour exposer les zones de fragilité. Dans un monde où les réponses IA deviennent abondantes, ce genre de protocole d’audit pourrait valoir plus qu’un point de benchmark supplémentaire.

Le désaccord n’est pas toujours une panne. Parfois, c’est le seul endroit où le système commence à dire quelque chose d’utile.
