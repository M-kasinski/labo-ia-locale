---
title: "Codex sort du terminal : OpenAI en fait une plateforme d’agents pour cols blancs"
description: "OpenAI ajoute à Codex six plugins métiers, Sites et Annotations. Le signal est clair : l’agent de coding devient un agent de workflow d’entreprise, avec les risques que cela implique."
pubDate: 2026-06-03
category: "veille"
tags: ["openai", "codex", "agents", "enterprise", "workflows"]
author: "Veille IA"
draft: false
sources:
  - label: "OpenAI — Codex for every role, tool, and workflow"
    url: "https://openai.com/index/codex-for-every-role-tool-workflow/"
  - label: "TechCrunch — OpenAI launches new Codex tools for white-collar work"
    url: "https://techcrunch.com/2026/06/02/openai-launches-new-codex-tools-for-white-collar-work/"
  - label: "VentureBeat — Codex update, Sites and role-specific plugins"
    url: "https://venturebeat.com/orchestration/openais-codex-update-lets-agents-build-interactive-enterprise-workspaces-via-sites-and-role-specific-plugins/"
---

OpenAI veut que Codex cesse d’être perçu comme un simple agent de développement. Le 2 juin, l’entreprise a présenté une extension nette de son périmètre : **six plugins métiers**, une fonction **Sites** pour publier des sorties interactives, et **Annotations** pour modifier plus finement des documents ou feuilles de calcul. TechCrunch résume le mouvement sans détour : Codex vise désormais le “white-collar work”, pas seulement le code.

Le point important n’est pas que Codex sache générer un rapport ou manipuler un tableur. Beaucoup d’outils IA le promettent déjà, avec une régularité presque comique. Le point important est architectural : OpenAI transforme Codex en couche agentique branchée sur des applications métier, des instructions spécialisées et des contextes persistants. Autrement dit, l’agent sort du repo Git et entre dans la tuyauterie de l’entreprise.

## Six plugins pour approximer des rôles

Selon OpenAI et la couverture de TechCrunch, les six plugins ciblent : **data analytics**, **creative production**, **sales**, **product design**, **public equity investing** et **investment banking**. Chaque plugin regroupe des intégrations, des instructions et du contexte pour permettre à Codex d’exécuter des tâches proches d’un rôle précis.

La liste des connecteurs donne une idée du positionnement. VentureBeat rapporte que les plugins agrègent **62 applications d’entreprise** et **110 skills automatisées**, avec des intégrations citées comme Snowflake, Databricks Genie, Hex, Tableau, Salesforce, HubSpot, Slack, Figma, Canva, FactSet ou PitchBook. Ce n’est pas un assistant générique qui répond dans une boîte de chat ; c’est un orchestrateur qui tente de se placer au milieu des outils déjà utilisés par les équipes.

Le plugin data analytics doit aider à explorer des données, expliquer les variations de métriques, créer des rapports ou dashboards. Le plugin sales se branche sur la pile CRM et communication pour générer des suivis, plans de closing ou analyses de risque de compte. Les plugins finance s’attaquent à des tâches plus sensibles : comparables, analyse de marché, diligence, pitch materials. Sur le papier, c’est séduisant. En production, cela exigera une gouvernance très propre. Un agent qui se trompe dans un fichier Markdown est pénible ; un agent qui se trompe dans un modèle financier ou une communication client devient franchement intéressant, au sens chinois du terme.

## Sites : la sortie devient un artefact utilisable

La fonction **Sites** est probablement plus stratégique qu’elle n’en a l’air. D’après TechCrunch, elle permet à Codex de produire un résultat sous forme de site interactif hébergé, plutôt que de laisser l’utilisateur avec un fichier local ou un bout de code. VentureBeat précise que Sites est disponible depuis l’application Codex, le CLI et l’application desktop, avec des permissions contrôlées côté admin dans un cadre entreprise.

C’est une évolution logique : si un agent produit une analyse, un prototype, un dashboard ou un workspace, il faut pouvoir le partager, l’ouvrir, le commenter, le tester. Le résultat doit devenir un artefact collaboratif, pas seulement une réponse longue dans un thread. OpenAI cite aussi un écosystème de partenaires autour de Sites, avec des noms comme Wix, Base44, Replit, Lovable, Figma et Emergent rapportés par TechCrunch.

Le risque évident est la prolifération de micro-apps internes semi-validées. Les entreprises ont déjà connu les feuilles Excel critiques envoyées par mail, les Notion bricolés qui deviennent systèmes de production, les dashboards Looker jamais maintenus. Sites peut accélérer le même phénomène avec une interface plus moderne. Utile, oui. À condition que les admins sachent qui publie quoi, avec quelles données, et pour combien de temps.

## Annotations : moins de régénération, plus de précision

La nouveauté **Annotations** répond à un problème concret des outils génératifs appliqués aux documents : ils refont trop souvent tout le fichier pour modifier une petite zone. Dans une feuille de calcul, cela peut casser des formules, écraser du formatage ou introduire des erreurs invisibles. VentureBeat décrit Annotations comme un mécanisme de contexte localisé : l’utilisateur désigne une zone, et Codex limite son opération à ce périmètre.

Cette granularité est essentielle si OpenAI veut aller au-delà des démonstrations. Les workflows d’entreprise ne sont pas des pages blanches. Ils sont remplis de dépendances, de conventions, de macros, de styles, de commentaires, de données partielles et de contraintes implicites. Un agent utile doit savoir toucher une zone sans ruiner le reste. C’est moins spectaculaire qu’un score de benchmark, mais c’est exactement le genre de détail qui détermine si un outil survit au contact du quotidien.

## Un signal sur l’usage réel de Codex

OpenAI affirme, cité par TechCrunch et VentureBeat, que Codex dépasse désormais **5 millions d’utilisateurs actifs hebdomadaires**, soit plus de **6×** depuis le lancement de l’application desktop en février. L’entreprise indique aussi que les non-développeurs représentent environ **20 %** des utilisateurs et croissent **plus de trois fois plus vite** que les développeurs.

Ces chiffres viennent d’OpenAI ; ils ne sont pas audités publiquement. Il faut donc les lire comme des indicateurs directionnels, pas comme une mesure indépendante du marché. Mais même avec cette prudence, le signal est intéressant : Codex n’est plus seulement vendu comme compagnon de programmation. OpenAI observe ou veut provoquer une migration vers les analystes, designers, marketers, opérateurs, chercheurs, investisseurs et banquiers.

C’est cohérent avec le reste de la stratégie entreprise. TechCrunch rappelle qu’OpenAI a lancé récemment l’OpenAI Deployment Company, une joint-venture orientée clients entreprise, avec plus de 4 milliards de dollars de financement annoncés par des investisseurs globaux. Le message est simple : OpenAI ne veut pas seulement vendre des tokens ou une app grand public ; elle veut s’insérer dans les processus opérationnels.

## Le vrai concurrent : l’organisation interne

La comparaison avec Anthropic est évidente. TechCrunch note qu’Anthropic a déjà poussé des agents entreprise et des agents financiers. Microsoft, de son côté, possède l’avantage naturel de la suite Office, de Teams, de GitHub et d’Azure. OpenAI doit donc construire une couche transversale capable de fonctionner au-dessus des applications, plutôt que de compter sur un système d’exploitation bureautique maison.

Mais le concurrent le plus dur n’est peut-être pas un autre modèle. C’est l’organisation interne des entreprises : permissions incohérentes, données mal classées, processus non documentés, responsabilité floue, audit insuffisant. Les plugins métiers ne résolvent pas ces problèmes ; ils les exposent. Un agent qui a accès à Salesforce, Slack, Snowflake et des données financières peut produire de la valeur. Il peut aussi amplifier une mauvaise permission, une hypothèse fragile ou une donnée obsolète.

## À retenir

Cette annonce n’est pas une simple extension produit. Elle marque le glissement de Codex vers une **plateforme d’exécution agentique pour le travail de connaissance**. Le modèle n’est plus seulement “écrire du code puis lancer des tests”, mais “connecter des outils, manipuler des artefacts, publier des sorties, agir dans des workflows métier”.

C’est puissant, mais ce n’est pas magique. Les plugins métiers auront besoin de permissions fines, de logs lisibles, d’environnements de test, de validations humaines et d’une vraie politique de données. Sans cela, Codex risque de devenir très vite ce que tous les DSI redoutent : un stagiaire brillant, branché à tous les outils, et convaincu d’avoir compris le contexte. Charmant. Légèrement radioactif.
