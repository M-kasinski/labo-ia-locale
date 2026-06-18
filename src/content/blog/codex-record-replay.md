---
title: "OpenAI Codex : Le 'Record & Replay' pour enseigner des workflows par la démonstration"
description: "Découvrez la fonctionnalité 'Record & Replay' d'OpenAI Codex, qui permet de transformer une démonstration visuelle sur macOS en une compétence (skill) réutilisable par l'agent."
pubDate: 2026-06-18
category: "veille"
tags: ["openai", "codex", "computer-use", "workflow"]
author: "Labo IA Locale"
draft: false
sources: ["https://developers.openai.com/codex/record-and-replay"]
---

# OpenAI Codex : Enseigner par l'exemple avec "Record & Replay"

L'un des plus grands défis de l'interaction avec les agents IA reste la complexité de la description textuelle pour des tâches visuelles ou procédurales répétitives. OpenAI répond à cette problématique avec la fonctionnalité **Record & Replay** pour Codex.

Plutôt que de rédiger des prompts interminables pour expliquer comment remplir un formulaire spécifique ou extraire des données d'un logiciel métier, l'utilisateur peut désormais simplement **montrer** comment faire.

### Le concept : De l'action à la "Skill"

Le "Record & Replay" permet de transformer une séquence d'actions sur macOS en une compétence (*skill*) structurée. 

Voici comment le processus se déroule :
1. **Enregistrement** : L'utilisateur lance l'enregistrement via l'application Codex.
2. **Démonstration** : L'utilisateur exécute la tâche manuellement sur son Mac (clics, saisies, navigation).
3. **Analyse & Conversion** : L'IA analyse la séquence d'actions et génère un "skill" qui définit :
    * **Le déclencheur** (quand utiliser cette compétence).
    * **Les entrées nécessaires** (quelles données varier, ex: un nom de fichier, une date).
    * **La séquence d'étapes** (la procédure exacte à suivre).
    * **La vérification** (comment confirmer que la tâche est réussie).

### Pourquoi est-ce une révolution pour l'automatisation ?

Jusqu'à présent, l'automatisation via agent demandait une précision chirurgicale dans les instructions. Avec le Record & Replay, on entre dans l'ère de l'**apprentissage par démonstration** (*Learning from Demonstration*).

* **Vitesse d'exécution** : Créer une nouvelle automatisation prend quelques secondes de manipulation plutôt que des heures de rédaction de documentation.
* **Adaptabilité** : En fournissant des variables (ex: "fais la même chose mais pour le fichier X"), l'agent peut appliquer la compétence à une infinité de cas concrets.
* **Complémentarité avec les Plugins** : Là où les plugins servent à distribuer des outils stables à une équipe, le Record & Replay est l'outil de création rapide pour l'utilisateur final.

### Limites et prérequis

* **Platform-specific** : Pour l'instant, la fonctionnalité est exclusivement disponible sur **macOS**.
* **Dépendance au "Computer Use"** : La fonction nécessite que la capacité "Computer Use" soit activée dans les configurations de l'organisation.
* **Confidentialité** : Bien que l'outil soit puissant, OpenAI recommande de ne pas enregistrer de données sensibles (mots de passe, infos privées) pendant la démonstration.

### Verdict de la veille

Le "Record & Replay" est une étape majeure vers des agents capables de s'intégrer de manière fluide dans les workflows métiers existants. On ne demande plus à l'IA de "comprendre" un logiciel ; on lui montre comment l'utiliser. C'est le passage de l'IA "chatter" à l'IA "opératrice".

***
*Article généré pour la veille technologique du Labo IA Locale.*
