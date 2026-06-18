---
title: "MCP sous pression : deux papiers montrent que la sécurité des agents ne se réglera pas par prompt"
description: "Le Model Context Protocol devient l’interface standard des agents avec les outils. Les derniers travaux de recherche rappellent une chose simple : quand un agent peut toucher au shell, au réseau ou aux fichiers, la sécurité doit être architecturale."
pubDate: 2026-06-02
category: "veille"
tags: ["MCP", "agents", "sécurité", "recherche"]
author: "Veille IA"
draft: false
sources:
  - label: "Anthropic — Introducing the Model Context Protocol"
    url: "https://www.anthropic.com/news/model-context-protocol"
  - label: "arXiv — Breaking the Protocol: Security Analysis of MCP"
    url: "https://arxiv.org/abs/2601.17549"
  - label: "arXiv — VIPER-MCP"
    url: "https://arxiv.org/abs/2605.21392"
  - label: "Anthropic Engineering — Code execution with MCP"
    url: "https://www.anthropic.com/engineering/code-execution-with-mcp"
---

Le **Model Context Protocol** est en train de devenir une pièce centrale de l’écosystème agentique. Anthropic l’a présenté fin 2024 comme un standard ouvert pour connecter les assistants IA aux systèmes où vivent les données : dépôts de code, outils métier, environnements de développement, bases documentaires. L’idée est saine : remplacer une jungle de connecteurs spécifiques par une interface commune entre clients MCP et serveurs MCP.

Mais une interface commune devient vite une surface d’attaque commune. Et deux papiers récents sur arXiv donnent une lecture assez nette du problème : avec les agents, la sécurité ne peut pas être principalement une affaire de consignes dans le prompt. Elle doit être portée par le protocole, les permissions, le sandboxing, l’audit et la validation d’exécution.

Le premier papier, **“Breaking the Protocol: Security Analysis of the Model Context Protocol Specification and Prompt Injection Vulnerabilities in Tool-Integrated LLM Agents”**, analyse MCP au niveau protocolaire. Le second, **“VIPER-MCP: Detecting and Exploiting Taint-Style Vulnerabilities in Model Context Protocol Servers”**, descend côté implémentations et cherche des failles dans des serveurs MCP réels. Les deux convergent : si un agent peut appeler des outils privilégiés, alors une instruction malveillante, un serveur compromis ou un handler vulnérable peut transformer une conversation en accès système. Charmant, comme une serrure connectée dont la clé serait un haïku.

## MCP : pourquoi le standard est utile

MCP répond à un vrai problème. Avant ce type de protocole, chaque application agentique devait maintenir ses propres intégrations : GitHub, Slack, navigateur, base SQL, drive documentaire, terminal, etc. Anthropic décrit MCP comme un standard ouvert permettant de construire des connexions bidirectionnelles sécurisées entre des sources de données et des outils alimentés par l’IA.

Dans la pratique, un développeur expose un système via un **serveur MCP** ; un client MCP, par exemple un assistant de code ou un agent de recherche, se connecte à ce serveur et découvre les outils disponibles. Le bénéfice est évident : moins de connecteurs ad hoc, plus de réutilisation, et une manière plus propre de donner du contexte aux modèles.

Anthropic note aussi, dans un billet d’ingénierie sur l’exécution de code avec MCP, que l’adoption a été rapide : serveurs communautaires nombreux, SDKs dans plusieurs langages, et usage croissant avec des agents capables d’accéder à des centaines voire milliers d’outils. Cette croissance crée cependant un second problème : plus il y a d’outils, plus il y a de permissions implicites, de descriptions injectées dans le contexte, et de chemins d’exécution difficiles à auditer.

## Le risque protocolaire : confiance implicite et attestation faible

Le papier **Breaking the Protocol** affirme identifier trois vulnérabilités fondamentales dans la conception MCP : absence d’attestation robuste des capacités, échantillonnage bidirectionnel sans authentification d’origine suffisante, et propagation implicite de la confiance dans les configurations multi-serveurs.

Les auteurs introduisent MCPBench et rapportent des expériences sur **847 scénarios d’attaque** à travers **cinq implémentations de serveurs MCP**. Leur résultat le plus important : selon eux, les choix architecturaux de MCP amplifient les taux de succès d’attaque de **23 à 41 %** par rapport à des intégrations non-MCP équivalentes. Ils proposent une extension, MCPSec, ajoutant attestation de capacités et authentification de messages ; dans leurs expériences, le taux de succès d’attaque passerait de **52,8 % à 12,4 %**, avec une surcharge médiane de **8,3 ms par message**.

Ces chiffres doivent être lus comme des résultats académiques à confirmer, pas comme une mesure universelle de tous les déploiements MCP. Mais le diagnostic est crédible : un protocole qui laisse un serveur déclarer ses capacités sans mécanisme fort de vérification ouvre la porte aux serveurs trop bavards, compromis ou malveillants. Et dans un système multi-serveurs, la confiance implicite peut devenir une chaîne de contamination.

## Le risque d’implémentation : du prompt au sink dangereux

Le papier **VIPER-MCP**, soumis le 20 mai 2026, attaque un autre angle : les vulnérabilités concrètes dans les serveurs MCP open source. Les auteurs partent d’un constat simple : un serveur MCP peut exposer des opérations sensibles — exécution shell, accès réseau, manipulation de fichiers. Si le code du handler laisse une entrée contrôlée par l’utilisateur atteindre un sink dangereux, l’attaque peut être déclenchée en langage naturel.

VIPER-MCP est présenté comme un framework d’audit automatisé qui combine analyse statique et validation dynamique. Il ne se contente pas de signaler une alerte : il cherche à produire des prompts de preuve de concept confirmant l’exploitabilité. D’après l’abstract, les auteurs ont scanné **39 884 dépôts open source de serveurs MCP**, découvert **106 vulnérabilités zero-day confirmées**, et obtenu **67 identifiants CVE** à date.

Là encore, prudence : le papier est récent, les chiffres doivent être relus par la communauté, et tous les serveurs MCP ne se valent pas. Mais le message opérationnel est clair. La vulnérabilité ne ressemble pas toujours à une injection SQL classique. Elle peut être une trajectoire où l’utilisateur formule une demande, l’agent choisit un outil, le handler assemble une commande, et une chaîne non filtrée finit dans le shell.

## Pourquoi les prompts ne suffisent pas

Le réflexe naïf consiste à ajouter dans le prompt système : “ne fais rien de dangereux”. Ce n’est pas inutile, mais ce n’est pas une frontière de sécurité. Un modèle peut être trompé par du contenu récupéré, par une instruction indirecte, par une description d’outil malveillante, ou simplement par un cas ambigu. Surtout, un prompt ne réduit pas les permissions réelles : si l’agent a le droit d’appeler `rm`, d’écrire dans un dépôt ou d’envoyer des requêtes réseau, la capacité existe.

La sécurité agentique doit donc ressembler davantage à de l’ingénierie système : permissions minimales, isolation par projet, confirmations humaines pour les actions destructives, signatures ou attestations des serveurs, allowlists, logs structurés, analyse des flux de données, et séparation stricte entre contexte non fiable et commandes exécutables.

Le billet d’Anthropic sur l’exécution de code avec MCP va dans une direction complémentaire : déplacer une partie du travail dans un environnement d’exécution, plutôt que tout faire transiter dans la fenêtre de contexte du modèle. C’est utile pour réduire les coûts et la fuite de données intermédiaires, mais cela renforce aussi l’idée que l’agent doit être encadré par un runtime, pas seulement par du texte.

## Ce que les équipes devraient retenir

Si MCP entre dans un workflow de développement ou d’entreprise, il faut traiter chaque serveur comme un composant logiciel privilégié. Installer un serveur MCP au hasard parce qu’il promet de connecter “tout ton workspace” est une mauvaise idée. Il faut auditer son code, comprendre ses permissions, limiter ses accès et surveiller ses appels.

Pour les éditeurs d’agents, la priorité est encore plus nette : construire des contrôles au niveau du client et du protocole. Un agent capable de choisir dynamiquement parmi des centaines d’outils doit avoir une politique de permissions explicite. Les confirmations humaines doivent être liées à la gravité de l’action, pas à une popup décorative. Et les logs doivent permettre de reconstruire pourquoi un outil a été appelé, avec quels arguments, et à partir de quel contexte.

MCP reste une bonne idée. Justement parce qu’elle est bonne, elle devient critique. Et une infrastructure critique ne peut pas dépendre de la bonne humeur probabiliste d’un modèle. Le standard doit mûrir vers l’attestation, l’isolation et la vérification. Sinon, les agents autonomes auront une qualité rare : ils automatiseront aussi les incidents.
