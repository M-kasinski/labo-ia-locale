---
title: "Open WebUI 0.9.6 transforme ses Knowledge Bases en vrai socle RAG auto-hébergé"
description: "Avec oikb, la synchro incrémentale, les dossiers imbriqués et les outils agentiques de Knowledge, Open WebUI devient plus crédible pour maintenir un RAG local vivant."
pubDate: 2026-06-08
tags: ["Open WebUI", "RAG", "auto-hébergement", "Knowledge Base", "oikb", "MCP"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "GitHub Releases — Open WebUI v0.9.6"
    url: "https://github.com/open-webui/open-webui/releases/tag/v0.9.6"
  - label: "GitHub — open-webui/oikb"
    url: "https://github.com/open-webui/oikb"
  - label: "Open WebUI Docs — Knowledge"
    url: "https://docs.openwebui.com/features/workspace/knowledge/"
---

Open WebUI a publié **v0.9.6** le **1er juin 2026**. La date sort un peu de la fenêtre idéale des 72 heures, mais la release mérite un article parce qu’elle touche un vrai problème de l’IA auto-hébergée : garder une base documentaire utile, synchronisée et exploitable par un modèle local. Pas juste uploader trois PDF dans une interface et appeler ça “RAG enterprise”. Cette fois, le sujet central est plus concret : **Knowledge Bases**, synchro incrémentale, dossiers, outil `oikb`, et exploration agentique des documents.

Open WebUI est déjà très connu comme interface self-hosted pour Ollama, endpoints OpenAI-compatible et workflows locaux. La v0.9.6 ne change pas cette identité. Elle renforce plutôt la partie qui manque souvent aux installations personnelles ou internes : la maintenance continue du contexte. Un RAG qui n’est pas synchronisé devient vite une archive morte. Une archive morte, c’est une hallucination avec une belle arborescence.

## oikb : synchroniser au lieu de ré-uploader

La nouveauté la plus structurante est l’arrivée de **`oikb`**, présenté comme l’outil officiel de synchronisation des Knowledge Bases Open WebUI. Le dépôt `open-webui/oikb` indique qu’il requiert **Open WebUI 0.9.6+**, qu’il est écrit en Python, sous licence **MIT**, et qu’il sert à garder des bases de connaissance synchronisées avec des sources externes.

Le README annonce la couleur : `oikb` peut pointer vers un dossier local, un dépôt GitHub, un espace Confluence, un bucket S3 ou l’un des **44 connecteurs** pris en charge. La synchronisation se fait par diff incrémental **SHA-256** : seuls les fichiers nouveaux ou modifiés sont envoyés, et les fichiers obsolètes peuvent être nettoyés.

C’est exactement le type de fonctionnalité qui sépare un prototype RAG d’un système maintenable. Dans un vrai usage local — notes Obsidian, documentation d’équipe, runbooks, dépôt de code, wiki interne — les documents changent en permanence. Ré-uploader manuellement un corpus complet à chaque modification est lent, fragile et franchement médiéval. `oikb` déplace le problème vers une mécanique plus saine : surveiller, comparer, pousser les changements.

## CLI, daemon, Docker, GitHub Action : le bon niveau d’intégration

`oikb` n’est pas seulement un bouton dans l’interface. Le dépôt décrit plusieurs modes d’exécution : **CLI one-shot**, watch mode, daemon planifié, conteneur Docker, GitHub Action et serveur OpenAPI Tool pour Open WebUI. Le quick start officiel ressemble à ceci : `pip install oikb`, configuration de `OPEN_WEBUI_URL` et `OPEN_WEBUI_API_KEY`, puis `oikb sync ./docs --kb-id ...` ou `oikb sync github:owner/repo --kb-id ...`.

Pour les déploiements persistants, `oikb init` génère un fichier `.oikb.yaml`, puis `oikb daemon` lance un scheduler. Le daemon expose aussi des points utiles : health check, métriques Prometheus, historique de synchronisation, déclenchement à la demande et webhooks pour GitHub, GitLab, Slack ou Confluence. Il peut également être protégé par une clé API.

Ce n’est pas glamour, mais c’est le bon design pour l’auto-hébergement. Un outil RAG doit vivre avec le système qui produit les documents. Si la documentation est dans Git, il faut pouvoir déclencher une synchro à chaque push. Si elle est dans Confluence, il faut un connecteur. Si elle est dans un dossier local, il faut éviter de tout rescanner bêtement sans état. `oikb` semble viser cette couche d’exploitation, pas seulement la démo.

## Smart Directory Sync et dossiers imbriqués

La release v0.9.6 ajoute aussi une **Smart Directory Sync** directement côté Knowledge Bases. D’après les notes officielles, Open WebUI compare les checksums, n’upload que les fichiers ajoutés ou modifiés, nettoie les suppressions et sous-dossiers orphelins, conserve la structure de répertoire, et affiche une progression par fichier.

Les Knowledge Bases gagnent également des **dossiers imbriqués**, une navigation par fil d’Ariane et le renommage direct de fichiers. Cela paraît basique jusqu’au moment où l’on gère plusieurs milliers de fichiers. Sans structure, une base RAG devient un grenier sémantique : le modèle peut parfois retrouver quelque chose, mais l’humain ne sait plus ce qui est censé s’y trouver.

La documentation Open WebUI confirme que la fonctionnalité Knowledge est pensée pour des collections de documents cherchables par IA, avec deux modes : **Focused Retrieval**, le RAG classique, et **Full Context**, qui injecte le document entier. Les docs recommandent le mode retrieval pour les gros corpus, précisément pour éviter de saturer la fenêtre de contexte. C’est un rappel utile : le local ne rend pas les tokens gratuits, il les rend juste plus visibles sur ta facture électrique.

## Un outil filesystem pour les modèles

Autre ajout important : le nouvel outil intégré activable via **`ENABLE_KB_EXEC`**. La release indique qu’il permet aux modèles de parcourir et rechercher les contenus de Knowledge Bases avec des commandes façon système de fichiers : `ls`, `cat`, `grep`, `find`, `head`, `tail`, `sed`, avec support des pipes.

C’est une direction intéressante. Beaucoup de RAG restent enfermés dans une seule opération “question → chunks pertinents → réponse”. Pour des agents locaux, ce n’est pas toujours suffisant. Un agent de code ou de documentation a souvent besoin de naviguer : lister les fichiers, lire un extrait précis, faire une recherche exacte, comparer plusieurs sources. La documentation Knowledge liste justement des outils comme `list_knowledge`, `search_knowledge_files`, `query_knowledge_files`, `grep_knowledge_files`, `view_file` ou `view_knowledge_file`, selon que la base est attachée ou non.

Cette approche est plus proche d’un vrai environnement de travail. Elle apporte aussi des risques : donner à un modèle des outils de lecture puissants nécessite de bien gérer les droits d’accès, le scope des Knowledge Bases et les permissions utilisateur. La release v0.9.6 contient d’ailleurs des correctifs de sécurité et d’access control, avec recommandation de mise à jour rapide des déploiements de production. Le message implicite est clair : plus l’agent peut faire de choses, plus la surface de sécurité grandit.

## MCP, timeouts et sessions : moins de bricolage agentique

La v0.9.6 mentionne aussi des améliorations autour de **MCP**, notamment un nouveau paramètre **`MCP_INITIALIZE_TIMEOUT`** pour laisser aux serveurs MCP lents le temps de terminer leur handshake initial. Les extraits de release signalent également des corrections de sessions MCP OAuth qui ne doivent plus être supprimées par erreur par le gestionnaire de session SSO.

Ce n’est pas le cœur de la release, mais c’est cohérent avec la trajectoire d’Open WebUI : devenir une interface self-hosted capable de brancher modèles, outils, documents et agents. Le projet `mcpo`, autre dépôt Open WebUI, joue aussi dans cette zone en exposant des serveurs MCP sous forme OpenAPI, même si sa dernière release significative date de février 2026. La v0.9.6 montre surtout que l’intégration MCP dans Open WebUI commence à recevoir les petites options d’exploitation qui manquent quand on sort du tutoriel.

## Attention à l’upgrade : migrations et secret obligatoire

La release officielle contient deux avertissements opérationnels importants. D’abord, **v0.9.6 inclut des changements de schéma de base de données**. Open WebUI recommande de sauvegarder la base et les données associées avant upgrade. En configuration multi-worker, multi-server ou load-balanced, les rolling upgrades ne sont pas supportés : toutes les instances doivent être mises à jour simultanément, sous peine d’incompatibilités de schéma.

Ensuite, **`WEBUI_SECRET_KEY` devient une exigence dure** pour les démarrages non supportés, notamment les lancements directs via `uvicorn`. Les méthodes supportées — `start.sh`, `start_windows.bat`, `open-webui serve` — continuent de le définir ou générer automatiquement. C’est une bonne décision côté sécurité, mais elle peut casser des scripts maison. Le genre de script qui “marchait depuis six mois”, donc évidemment personne ne se souvient de son auteur.

## Ce que ça change pour le local

Pour un usage IA locale, Open WebUI v0.9.6 rend le RAG moins décoratif. `oikb` permet de garder un corpus vivant, la Smart Directory Sync évite les réimports absurdes, les dossiers imbriqués rendent les collections navigables, et les outils agentiques donnent aux modèles une manière plus structurée d’explorer les documents.

Ce n’est pas une garantie de qualité des réponses. Il faudra toujours choisir les bons embeddings, régler le chunking, activer ou non la recherche hybride, surveiller les droits et tester les hallucinations. Mais la pile gagne une propriété essentielle : elle devient maintenable. Dans l’auto-hébergement, c’est souvent plus important qu’une nouvelle case “AI-powered” dans une interface.

Si tu utilises Open WebUI comme simple chat local, la v0.9.6 n’est pas forcément urgente hors sécurité. Si tu t’en sers comme hub RAG pour une équipe, une base documentaire ou un homelab sérieux, elle vaut clairement un test — avec backup avant migration, pas après. Le backup après migration, c’est de la poésie tragique.

## Sources

- GitHub Releases — Open WebUI v0.9.6 : https://github.com/open-webui/open-webui/releases/tag/v0.9.6
- GitHub — open-webui/oikb : https://github.com/open-webui/oikb
- Open WebUI Docs — Knowledge : https://docs.openwebui.com/features/workspace/knowledge/
