---
title: "OpenClaw Research : les agents IA sortent du bac à sable, et les risques avec eux"
description: "Un nouveau survey OpenReview propose un cadre pour étudier les agents LLM en déploiement ouvert : mémoire persistante, MCP, compétences communautaires, populations multi-agents et gouvernance runtime."
pubDate: 2026-06-01
category: "veille"
tags: ["agents", "mcp", "securite", "recherche", "openclaw"]
author: "Veille IA"
draft: false
sources:
  - label: "OpenReview — OpenClaw Research: A Systematic Survey of Large Language Model Agents in Open Deployment"
    url: "https://openreview.net/pdf/a61d0148c193cc1a63b2dc3149b83f1396ee0f76.pdf"
  - label: "GitHub — Awesome-OpenClaw-Research"
    url: "https://github.com/shuolucs/Awesome-OpenClaw-Research"
  - label: "arXiv — Clawed and Dangerous: Can We Trust Open Agentic Systems?"
    url: "https://arxiv.org/html/2603.26221v1"
---

Un nouveau survey publié sur OpenReview, **“OpenClaw Research: A Systematic Survey of Large Language Model Agents in Open Deployment”**, met des mots sur une transition que beaucoup d’équipes sentent déjà : les agents LLM ne sont plus seulement des démos dans des environnements contrôlés. Ils deviennent des processus persistants, connectés à des outils, dotés de mémoire, extensibles par des compétences tierces, parfois branchés à MCP, et capables d’agir dans des espaces numériques qui n’ont rien de propre.

Le papier prend **OpenClaw** comme objet d’étude et comme lentille. D’après le survey, OpenClaw est un middleware open source auto-hébergé qui fait tourner des agents de manière persistante, connecte plus de **50 plateformes de messagerie**, orchestre des backends comme Claude, GPT ou Ollama, et expose une architecture à base de kernel agentique, mémoire, extensions, environnements d’exécution et interfaces humaines. Le dépôt compagnon **Awesome-OpenClaw-Research**, mis à jour fin mai 2026, organise déjà plus de **40 ressources** autour de cet écosystème.

La thèse du papier est plus large qu’OpenClaw : nous avons besoin d’une science des agents **après déploiement**. Pas seulement “le modèle sait-il résoudre la tâche ?”, mais “que se passe-t-il quand l’agent tourne longtemps, apprend de son environnement, installe des outils, interagit avec d’autres agents et opère avec de vrais privilèges ?”. C’est moins glamour qu’une courbe de benchmark. C’est aussi exactement là que les choses cassent.

## Le cadre : A = ⟨π, env, pop, substrate⟩

Le survey propose de formaliser un système agentique ouvert comme un quadruplet :

```text
A = ⟨π, env, pop, substrate⟩
```

Dans cette notation, **π** désigne la politique de l’agent — le modèle, les prompts, la mémoire et les règles qui produisent les actions. **env** représente l’environnement physique ou numérique dans lequel l’agent agit. **pop** désigne la population environnante : humains, autres agents, services, adversaires potentiels. **substrate** désigne l’infrastructure runtime : le processus, les permissions, les logs, les outils, les files d’événements, les garde-fous.

L’intérêt de cette formulation est qu’elle sort du piège “tout est dans le modèle”. Un agent déployé n’est pas seulement un LLM plus une boucle `observe -> plan -> act`. C’est un système logiciel distribué, avec une surface d’attaque, des dépendances, des états persistants et des modes de panne. Si le modèle est stochastique mais l’exécution est déterministe et privilégiée, l’architecture doit absorber l’incertitude au lieu de faire semblant qu’elle n’existe pas.

## Les quatre hypothèses de bac à sable qui sautent

Le papier identifie quatre hypothèses implicites dans beaucoup de recherches sur les agents.

Première hypothèse : la **policy** est contrôlée par le développeur. Dans un labo, les mises à jour sont explicites et hors ligne. En déploiement ouvert, la policy évolue via mémoire, préférences, feedback utilisateur, traces d’outils, compétences installées et parfois apprentissage continu.

Deuxième hypothèse : l’**environnement** est propre. Dans un benchmark, les outils sont prévus, les entrées sont connues, les API sont fiables. Dans le monde réel, l’agent lit des pages web hostiles, des issues GitHub contenant du prompt injection, des documents contradictoires, des réponses d’API partielles, et des fichiers dont la provenance est rarement parfaite.

Troisième hypothèse : la **population** est captive. Les autres agents, quand ils existent, sont souvent homogènes et contrôlés par la même équipe de recherche. En production, un agent dialogue avec des humains, des bots, des services, des adversaires et parfois d’autres agents aux objectifs incompatibles.

Quatrième hypothèse : le **substrate** est jetable. Les expériences se terminent, les environnements se réinitialisent, les logs sont accessoires. Un agent auto-hébergé et persistant a besoin d’observabilité, d’audit, de révocation, de gestion des secrets, d’isolation, de rollback, et d’une politique de permissions compréhensible. Bref : de l’ingénierie système, cette vieille connaissance qu’on redécouvre toujours quand une démo devient un produit.

## MCP, skills et supply chain : l’agent comme surface d’intégration

Le survey décrit OpenClaw comme un système extensible via des **skills**, des **plugins** et des serveurs **MCP**. Il évoque notamment des milliers de modules communautaires et intégrations MCP. Le dépôt Awesome-OpenClaw-Research classe ces travaux sous “Open Environment” et “Open Substrate” : sécurité des outils, interopérabilité, infrastructure agent-as-OS, mémoire persistante, observabilité et gouvernance.

C’est probablement le point le plus important pour l’écosystème agentique. MCP standardise une partie de la connexion entre modèles et outils ; c’est utile, mais cela transforme aussi chaque outil en entrée de contexte, en capacité d’action et en élément de supply chain. Un serveur MCP malveillant ou simplement mal conçu peut injecter des instructions dans le contexte, exposer trop de droits, ou faire croire à l’agent qu’une action dangereuse est normale.

Le papier arXiv **“Clawed and Dangerous: Can We Trust Open Agentic Systems?”**, publié en mars 2026, formule le problème de manière nette : la sécurité des agents n’est pas seulement une affaire de robustesse de prompt, c’est une affaire d’architecture logicielle et de gouvernance du cycle de vie. Les contrôles décisifs sont souvent dans la conception des capacités, l’isolation d’exécution, les contrats d’interface, la provenance des outils et l’audit opérationnel.

## La mémoire persistante est une fonctionnalité — et une dette

Les agents persistants promettent de se souvenir : préférences utilisateur, historique de projets, décisions passées, contraintes, contacts, routines. OpenClaw, selon le survey, inclut une mémoire hiérarchisée : contexte de session, notes quotidiennes, mémoire long terme et recherche sémantique. C’est exactement ce qui rend un assistant utile dans la durée.

Mais la mémoire transforme aussi un incident ponctuel en état durable. Une instruction malveillante, une fausse préférence ou une conclusion erronée peuvent se fossiliser dans la mémoire et influencer les actions futures. Le risque n’est pas seulement l’hallucination instantanée ; c’est la **pollution de trajectoire**. Un agent qui apprend mal peut devenir progressivement moins sûr, sans panne spectaculaire.

Cela impose des mécanismes rarement présents dans les prototypes : inspection de mémoire, provenance des souvenirs, expiration, séparation entre observations et croyances, confirmation humaine pour les règles qui changent les privilèges, et possibilité de revenir à un état antérieur. Un agent sans bouton “oublier proprement” est une base de données sans migrations. On peut vivre avec, mais pas longtemps.

## Multi-agent : plus d’agents ne veut pas dire plus de vérité

Le survey place aussi les populations d’agents au centre. Dans les systèmes multi-agents, on espère souvent obtenir de la robustesse par discussion, vote ou spécialisation. Le papier rappelle une limite : les groupes peuvent amplifier les erreurs. Plusieurs agents qui partagent les mêmes biais, les mêmes sources ou les mêmes incitations peuvent produire une **hallucination de consensus** : tout le monde est d’accord, donc tout le monde a tort avec assurance.

C’est cohérent avec une tendance plus large de la recherche agentique en 2026 : la coordination devient une couche d’architecture à part entière. Il ne suffit pas de lancer trois instances et d’appeler cela une société. Il faut définir les rôles, les canaux, les règles de désaccord, les budgets, les sources d’autorité, les mécanismes d’arrêt et les responsabilités. Sinon, on obtient surtout une réunion de copropriété probabiliste. Le progrès est réel ; l’élégance, pas garantie.

## Ce que les équipes doivent retenir

OpenClaw Research n’est pas un article “nouveau modèle, nouveau score”. C’est un article de cadrage, et c’est précisément pour cela qu’il est utile. Il propose une taxonomie pour discuter des agents tels qu’ils sont en train d’être déployés : ouverts, persistants, connectés, extensibles, sociaux, et difficiles à borner.

Pour les équipes qui construisent des agents, le message est clair : traiter l’agent comme une application LLM est insuffisant. Il faut le traiter comme une plateforme logicielle à privilèges délégués. Cela implique des permissions minimales, des outils signés ou vérifiés, des logs exploitables, une isolation par défaut, une séparation nette entre contenu non fiable et instructions système, une mémoire auditable, et des tests qui couvrent aussi les scénarios adversariaux.

Pour la recherche, le cadre `⟨π, env, pop, substrate⟩` pousse à mesurer autre chose que la réussite ponctuelle d’une tâche. Il faut évaluer la stabilité dans le temps, les effets de population, la résistance aux outils malveillants, la qualité de l’infrastructure, la gouvernance des compétences et la capacité à expliquer après coup pourquoi une action a été prise.

La conclusion sobre : les agents sortent du bac à sable. C’est une bonne nouvelle pour l’utilité, une moins bonne pour la sécurité naïve. La prochaine génération d’agents ne se jouera pas seulement dans les poids des modèles ; elle se jouera dans le runtime, la mémoire, les permissions et la discipline d’ingénierie autour. Comme souvent, l’intelligence arrive en costume, mais la fiabilité entre par la porte de service.
