---
title: "NuExtract3 : un VLM local pour extraire du JSON depuis des documents"
description: "NuMind publie NuExtract3, un modèle vision-langage auto-hébergeable pour OCR, Markdown et extraction structurée."
pubDate: 2026-05-31
tags: ["vlm", "rag", "ocr", "auto-hebergement", "documents"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Model card Hugging Face — numind/NuExtract3"
    url: "https://huggingface.co/numind/NuExtract3"
  - label: "Dépôt GitHub — numindai/nuextract"
    url: "https://github.com/numindai/nuextract"
  - label: "Hugging Face Space — NuExtract 3 demo"
    url: "https://huggingface.co/spaces/numind/NuExtract-3-4B"
---

NuMind a publié **NuExtract3**, un modèle vision-langage spécialisé dans un problème très concret : transformer des documents en données exploitables. Pas “discuter avec un PDF” dans le flou marketing habituel, mais extraire du **JSON structuré**, convertir des images de documents en **Markdown**, et préparer des corpus pour des pipelines RAG ou back-office.

Pour l’IA locale, c’est un sujet plus important qu’il n’en a l’air. Beaucoup d’équipes peuvent déjà faire tourner un LLM local. Beaucoup moins ont une chaîne documentaire locale fiable : OCR, tableaux, formulaires, factures, scans moches, champs absents, sorties JSON valides. NuExtract3 vise précisément ce maillon-là.

## Ce qu’est NuExtract3

La model card Hugging Face décrit NuExtract3 comme un modèle **vision-langage de raisonnement pour la compréhension documentaire**. Le projet le présente comme un modèle **4B**, tandis que les métadonnées Hugging Face affichent une taille de **5B paramètres**. Ce décalage n’est pas rare avec les modèles dérivés ou les arrondis de familles, mais il mérite d’être signalé : pour dimensionner une machine, il faudra se fier aux fichiers réels et aux formats de quantization disponibles plutôt qu’au seul chiffre marketing.

Le modèle est fine-tuné depuis **Qwen/Qwen3.5-4B**, selon la model card. Il accepte plusieurs types d’entrée : texte seul, image seule, ou combinaison texte + image. Les usages annoncés sont :

- extraction structurée vers JSON à partir d’un template ;
- conversion image/document vers Markdown ;
- OCR orienté documents complexes ;
- préparation de données pour RAG ;
- traitement de reçus, formulaires, factures, contrats, tableaux et documents multi-pages ;
- génération de templates depuis une instruction ou un document.

Le dépôt GitHub fournit des exemples d’appel via une API compatible OpenAI servie localement, notamment avec une requête contenant une image encodée en base64, un template JSON et des paramètres de chat template.

## Pourquoi ce n’est pas juste un OCR de plus

L’OCR classique lit du texte. C’est utile, mais insuffisant dès qu’il faut produire une structure stable : lignes de facture, champs optionnels, tableaux imbriqués, sections, signatures, métadonnées. NuExtract3 ajoute une couche de compréhension et de génération structurée.

Le mode typique est simple : on donne un document et un **template JSON** ; le modèle doit remplir les champs en respectant le format. C’est exactement ce qu’il faut pour brancher un modèle local à une base de données, un ERP, un système documentaire ou un pipeline RAG. La différence entre “voici le texte brut” et “voici un JSON valide avec `total`, `date`, `vendor`, `line_items`” est la différence entre une démo et un outil utilisable.

NuExtract3 propose aussi un mode de conversion vers Markdown. L’objectif n’est pas seulement esthétique : un bon Markdown conserve titres, paragraphes, tableaux et parfois formules, ce qui améliore ensuite l’indexation, le chunking et la recherche sémantique.

## Les benchmarks annoncés

NuMind publie sur la model card un benchmark interne d’extraction structurée sur environ **600 documents** variés : factures, affiches, plans, documents longs, sorties longues et cas nécessitant OCR + raisonnement. Les prédictions et références JSON sont comparées comme des arbres ; les feuilles textuelles utilisent une distance de type indel / Levenshtein sans remplacement, tandis que d’autres types reposent sur l’exact match.

Le résultat principal annoncé : **NuExtract3.4_4B-RL obtient 0,651 ± 0,019** de score moyen, devant **gemma-4-E4B-it** à 0,538 ± 0,023, **Qwen3.5-9B** à 0,479 ± 0,030 et **Qwen3.5-4B** à 0,417 ± 0,031. NuMind rapporte aussi le nombre de sorties non désérialisables en JSON : 27 échecs pour NuExtract3.4_4B-RL, contre 170 pour Qwen3.5-9B et 229 pour Qwen3.5-4B dans leur protocole.

Ces chiffres sont intéressants, mais ils restent issus de l’équipe qui publie le modèle. Le benchmark est annoncé comme devant être ouvert avec un leaderboard et une bibliothèque d’évaluation, mais tant que ce n’est pas largement rejoué par des tiers, il faut le lire comme un signal technique, pas comme un verdict définitif.

Le détail le plus utile est peut-être ailleurs : NuMind observe que certains petits modèles de raisonnement entrent dans des boucles de répétition, atteignent la limite de tokens de sortie et produisent des réponses invalides. C’est exactement le genre de panne qu’on rencontre dans l’extraction documentaire réelle. Un modèle qui “comprend” bien mais sort un JSON cassé reste un collègue sympathique, pas un composant de production.

## Modes reasoning et non-reasoning

NuExtract3 supporte des modes avec et sans raisonnement. Pour l’extraction structurée, c’est une distinction importante. Le raisonnement peut aider sur des documents ambigus, mais il coûte des tokens, augmente la latence et peut favoriser les boucles si le modèle hésite trop. Le mode non-reasoning sera probablement préférable pour des flux industriels simples : factures homogènes, reçus, formulaires répétitifs.

Pour des documents plus sales — scans inclinés, tableaux partiels, champs dispersés — le raisonnement peut valoir le coût. La bonne stratégie locale sera donc moins “toujours activer le raisonnement” que “router selon la difficulté du document”. Oui, c’est moins sexy qu’un bouton magique. C’est aussi comme ça qu’on évite de brûler du GPU pour lire trois lignes de TVA.

## Où ça s’insère dans une stack locale

NuExtract3 a une place naturelle dans trois architectures.

Premièrement, le **RAG local**. Avant d’embeddder un PDF, il faut souvent le convertir proprement. Si le modèle produit un Markdown fidèle, les chunks seront plus propres, les titres mieux conservés, et les tableaux moins massacrés.

Deuxièmement, l’**automatisation documentaire**. Une petite entreprise peut auto-héberger un service d’extraction pour factures, bons de commande ou contrats sans envoyer les documents à une API externe. C’est particulièrement pertinent pour les données sensibles.

Troisièmement, les **agents locaux outillés**. Un agent peut recevoir un document, demander à NuExtract3 une extraction selon un schéma, puis transmettre le JSON à un autre outil : base SQLite, tableur, système de ticketing, ou pipeline de validation humaine.

Le dépôt GitHub montre des exemples de requêtes compatibles avec un serveur local de type OpenAI API. C’est le bon niveau d’intégration : le modèle spécialisé reste un service, et l’orchestrateur décide quand l’appeler.

## Points à vérifier avant production

NuExtract3 est prometteur, mais il faut tester avant de lui confier un vrai flux documentaire.

À vérifier :

1. **Licence exacte selon artefact utilisé** : le dépôt GitHub est indiqué MIT, tandis que les fichiers modèles et variantes peuvent avoir leurs propres métadonnées. Avant usage commercial, lire la model card et les fichiers de licence du checkpoint ciblé.
2. **Mémoire réelle** : la taille “4B/5B” ne dit pas combien coûte le modèle en BF16, GGUF, MLX ou autre format.
3. **JSON strict** : taux de sorties invalides sur vos documents, pas seulement sur le benchmark NuMind.
4. **Documents francophones** : accents, formats de date, montants européens, TVA, tableaux scannés.
5. **Champs absents** : un bon extracteur doit retourner `null` ou omettre proprement, pas inventer.

## Ce qu’il faut retenir

NuExtract3 est une release utile parce qu’elle vise un besoin moins glamour mais central : rendre les documents locaux actionnables. Pour beaucoup d’usages, un pipeline IA privé ne commence pas par un LLM bavard, mais par une extraction robuste.

Le modèle ne remplace pas une validation métier, et les benchmarks doivent encore être confirmés indépendamment. Mais comme brique auto-hébergeable pour OCR, Markdown et JSON structuré, NuExtract3 mérite clairement un test dans les stacks RAG et back-office locales.
