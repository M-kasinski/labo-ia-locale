---
title: "Codex sur Windows : OpenAI rapproche l’agent de coding du vrai poste développeur"
description: "Avec Computer Use sur Windows et le pilotage mobile via ChatGPT, Codex quitte un peu plus le terminal pour opérer dans l’environnement graphique du développeur. Puissant, mais pas magique."
pubDate: 2026-05-31
category: "veille"
tags: ["openai", "codex", "agents", "coding", "computer-use"]
author: "Veille IA"
draft: false
sources:
  - label: "OpenAI Developers — Codex changelog"
    url: "https://developers.openai.com/codex/changelog"
  - label: "OpenAI Developers — Computer Use dans Codex"
    url: "https://developers.openai.com/codex/app/computer-use"
  - label: "Neowin — OpenAI rolls out Codex for Windows update"
    url: "https://www.neowin.net/news/openai-rolls-out-major-codex-for-windows-update-with-computer-use-and-mobile-access/"
  - label: "Thurrott — OpenAI brings Computer Use to Codex on Windows"
    url: "https://www.thurrott.com/a-i/openai-a-i/336754/openai-brings-computer-use-to-codex-app-on-windows"
---

OpenAI a publié le 29 mai une mise à jour importante de l’application Codex pour Windows. La nouveauté centrale est simple à formuler : **Computer Use fonctionne désormais sur Windows**. En pratique, Codex peut voir une application graphique, cliquer, taper, suivre un flux UI, puis revenir dans le contexte du projet. La même mise à jour ajoute aussi le pilotage distant depuis l’application mobile ChatGPT pour les machines Windows.

Ce n’est pas un nouveau modèle. Ce n’est pas non plus un benchmark clinquant. Mais c’est probablement plus important pour l’usage quotidien des agents de développement : OpenAI rapproche Codex de l’endroit où les bugs vivent réellement — l’IDE, le navigateur, l’application desktop, les fenêtres de configuration, les dialogues système, bref le désordre habituel d’un poste développeur.

## Ce qui change dans Codex 26.527

Le changelog officiel d’OpenAI liste la mise à jour **Codex app 26.527** au 29 mai 2026. Deux ajouts ressortent : Computer Use sur Windows et le contrôle distant des appareils Windows depuis ChatGPT mobile ou depuis un Mac exécutant Codex. OpenAI indique aussi des améliorations plus classiques : section profil enrichie, statistiques d’usage, activité token, recherche de threads étendue au contenu des conversations et aux noms de branches Git, coordination de threads locaux et de worktrees.

La partie vraiment structurante reste Computer Use. Selon la documentation développeur d’OpenAI, cette fonction permet à Codex de voir et d’opérer des interfaces graphiques sur macOS ou Windows. L’agent peut inspecter le contenu visible, prendre des captures, interagir avec les fenêtres, les menus, le clavier et le presse-papiers. C’est utile quand un outil CLI, une inspection de fichiers ou un connecteur structuré ne suffit pas.

Le cas typique est très concret : tester une application Windows, reproduire un bug d’onboarding qui n’apparaît que dans l’interface, vérifier un parcours checkout dans un navigateur, changer un réglage dans une app, ou travailler avec une source de données qui n’a pas d’API propre. Autrement dit : tous les endroits où un agent de coding purement textuel se retrouvait auparavant à deviner.

## Windows, mais en foreground

Le détail à ne pas rater : sur Windows, Computer Use fonctionne sur le **bureau actif**. La documentation OpenAI précise que l’application cible doit rester visible dans la session active. Codex peut bouger le pointeur, taper et prendre le contrôle de l’entrée utilisateur. Donc, contrairement à une promesse naïve de “background automation”, l’utilisateur ne peut pas continuer à travailler tranquillement dans la même session pendant que Codex pilote une autre fenêtre.

Neowin souligne la même limite : sur Windows, l’usage se fait en foreground. Cela réduit l’élégance du dispositif, mais rend le comportement plus compréhensible. Un agent qui contrôle une GUI a besoin d’un état visuel stable. Si l’humain déplace les fenêtres ou tape en même temps, l’environnement devient non déterministe. Dans une machine virtuelle Windows dédiée, en revanche, l’approche devient beaucoup plus propre : Codex peut monopoliser la session sans voler la souris du développeur.

La restriction géographique compte aussi. La page OpenAI indique que Computer Use est disponible dans l’application Codex sur macOS et Windows, **sauf dans l’Espace économique européen, au Royaume-Uni et en Suisse au lancement**. Pour un média francophone, c’est plus qu’une note de bas de page : l’annonce est techniquement pertinente, mais l’accès initial peut être limité selon la localisation.

## Le téléphone devient une console de supervision

La deuxième brique est le pilotage mobile. D’après le changelog OpenAI et la couverture de Neowin, un utilisateur peut connecter un PC Windows à Codex dans l’application ChatGPT mobile, puis démarrer ou continuer des threads, envoyer des instructions, approuver des actions, lire des diffs, consulter des résultats de tests, et vérifier des captures d’écran ou des sorties terminal.

C’est exactement le modèle opérationnel vers lequel convergent les coding agents : une machine exécute, l’utilisateur supervise. Le téléphone n’est pas l’environnement de développement ; il devient une télécommande de validation. Ce n’est pas anodin, parce que les agents de coding passent de l’assistance interactive à des sessions de travail plus longues, parfois semi-autonomes. L’enjeu n’est plus seulement “écris-moi une fonction”, mais “travaille sur ce bug, teste-le, montre-moi le diff, demande-moi quand une action risquée apparaît”.

Thurrott rapporte que les utilisateurs peuvent invoquer Computer Use via `@computer` ou des références à des applications spécifiques comme `@Paint`, après activation dans les réglages Codex. C’est une interface simple, presque trop simple : la difficulté n’est pas d’appeler l’outil, mais de garder le périmètre du travail clair.

## Pourquoi c’est important pour les agents de coding

Un agent de développement fiable doit faire trois choses : comprendre le code, exécuter des outils, et vérifier dans l’environnement réel. Les deux premières dimensions progressent vite. La troisième reste souvent faible. Beaucoup d’agents savent modifier un fichier et lancer des tests unitaires, mais échouent dès que la validation dépend d’un navigateur, d’un simulateur, d’un installateur, d’un client lourd ou d’un dialogue système.

Computer Use attaque précisément cet angle mort. Il ne remplace pas les API, les tests automatisés ni les MCP servers. Il complète les cas où l’interface graphique est la source de vérité. Pour un bug UI, une capture d’écran peut parfois contenir plus d’information que dix fichiers de logs. Pour une app Windows, le simple fait de pouvoir reproduire visuellement un flux corrige une faiblesse structurelle des assistants de coding.

Il faut cependant éviter le fantasme du stagiaire robotisé parfait. La GUI est fragile : éléments déplacés, latence, popups, sessions verrouillées, contenus web malveillants, état utilisateur ambigu. OpenAI insiste d’ailleurs sur la prudence : si Codex utilise le navigateur, il peut interagir avec des pages où l’utilisateur est déjà connecté. Les actions approuvées peuvent être traitées par les sites comme venant du compte utilisateur. C’est une surface de risque sérieuse, pas un gadget.

## Le vrai sujet : permissions, audit et reprise

Cette annonce confirme une tendance plus large : les agents utiles auront besoin d’un modèle de permissions plus fin que “accès au repo oui/non”. Computer Use touche aux applications, aux comptes connectés, aux fichiers ouverts, au presse-papiers et aux workflows hors Git. Il faut donc tracer ce que l’agent voit, ce qu’il fait, ce qu’il propose, et ce que l’utilisateur approuve.

OpenAI indique que les modifications faites via des applications desktop peuvent ne pas apparaître dans le panneau de revue tant qu’elles ne sont pas sauvegardées sur disque et suivies par le projet. C’est un détail pratique, mais révélateur : le monde graphique n’a pas la propreté transactionnelle d’un diff Git. Un clic peut changer un état externe sans produire de patch lisible.

Pour les équipes, la bonne posture est donc prudente : utiliser Computer Use pour des tâches bornées, préférer les intégrations structurées quand elles existent, isoler les environnements Windows dans des VM pour les tâches longues, et garder une approbation humaine sur les actions sensibles. Le slogan implicite pourrait être : plus d’autonomie, mais pas moins de contrôle.

## À retenir

Codex sur Windows avec Computer Use n’est pas une révolution de modèle ; c’est une évolution de surface d’exécution. Et c’est précisément pour cela que c’est intéressant. Les agents de coding ne gagneront pas seulement en intelligence brute, mais en capacité à agir dans les environnements réels où le logiciel est construit, testé et cassé.

La limite foreground sur Windows rappelle que nous ne sommes pas encore dans l’autonomie fluide. Mais le cap est clair : OpenAI veut faire de Codex une session de travail distribuée, supervisable depuis le téléphone, capable d’alterner terminal, fichiers, Git, navigateur et applications desktop. C’est moins propre qu’un benchmark. C’est aussi beaucoup plus proche de la production.
