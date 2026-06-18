---
title: "Puces IA : Washington referme la porte des filiales chinoises hors de Chine"
description: "Le BIS précise que les contrôles américains sur les puces IA avancées s’appliquent aussi aux entités basées hors de Chine si leur siège ou maison mère est chinois. Une clarification juridique, mais un signal stratégique net."
pubDate: 2026-06-03
category: "veille"
tags: ["gpu", "regulation", "nvidia", "chine", "export-controls"]
author: "Veille IA"
draft: false
sources:
  - label: "BIS — Guidance Regarding Enforcement of License Requirements for Advanced Computing Items"
    url: "https://www.bis.gov/media/documents/bis-guidance-may-31-2026.pdf"
  - label: "Al Jazeera — US says ban on AI chip shipments applies to Chinese firms outside China"
    url: "https://www.aljazeera.com/economy/2026/6/1/us-says-ban-on-ai-chip-shipments-applies-to-chinese-firms-outside-china"
  - label: "Reuters — US takes step to halt Nvidia AI chip shipments to Chinese firms outside China"
    url: "https://www.reuters.com/world/china/us-takes-step-halt-nvidia-ai-chip-shipments-chinese-firms-outside-china-2026-05-31/"
---

Le **Bureau of Industry and Security** américain a publié le 31 mai une clarification qui vise directement un angle mort des contrôles export sur les accélérateurs IA : les entités installées hors de Chine, mais contrôlées par des groupes chinois. La note du BIS indique qu’une licence reste requise pour exporter des **advanced computing items** vers des entités dont le siège, ou la maison mère ultime, se trouve dans les pays du **Country Group D:5** ou à Macao, même si ces entités opèrent ailleurs.

Dit plus simplement : une filiale basée à Singapour, en Malaisie ou dans un autre pays ne devient pas automatiquement un client “neutre” si son groupe est chinois. Pour les GPU IA haut de gamme, la nationalité économique du client compte autant que son adresse de livraison. C’est moins photogénique qu’un lancement de modèle, mais dans la course à l’IA, ce genre de PDF peut déplacer plus de puissance de calcul qu’un keynote.

## Ce que dit exactement le BIS

La guidance du 31 mai est courte, mais dense. Le BIS y explique avoir reçu des questions sur l’application des obligations de licence après le non-respect annoncé de certaines exigences du **AI Diffusion Rule**. Sa réponse : **oui**, les exigences préexistantes continuent de s’appliquer pour les puces avancées destinées à des entités liées aux pays D:5 ou à Macao.

Le texte précise que l’obligation de licence concerne les articles de calcul avancé couverts notamment par les classifications **3A090.a**, **3A090.b**, **4A090.a**, **4A090.b** et les paragraphes `.z` associés. Il rappelle que cette exigence avait été introduite en novembre 2023 via le contrôle d’utilisateur final de la section **744.23(a)(3)** de l’EAR, puis déplacée en janvier 2025 dans **742.6** pour certains items `.a` dans le cadre de l’AI Diffusion Rule.

La partie opérationnelle tient en une phrase : une licence continue de s’appliquer “to all destinations outside the United States” pour ces articles lorsqu’ils sont destinés à des entités dont le siège ou la maison mère ultime est dans Country Group D:5 ou à Macao. Le BIS ajoute que les exportateurs doivent continuer à demander des licences, sauf exception applicable.

## Pourquoi cette clarification arrive maintenant

Al Jazeera rapporte que la clarification intervient après des inquiétudes sur une possible utilisation de filiales étrangères pour obtenir des puces soumises à contrôle, notamment des accélérateurs Nvidia de génération Blackwell. Reuters, qui a également couvert le sujet, indique que le département du Commerce cherchait à fermer une voie potentielle par laquelle des filiales de groupes chinois situées hors de Chine auraient pu accéder aux puces IA les plus avancées.

Le point politique est subtil. L’administration Trump a abandonné en mai 2026 le cadre plus large de diffusion de l’IA hérité de l’administration Biden, critiqué par l’industrie pour sa complexité et son impact diplomatique. Mais le BIS rappelle ici que l’abandon ou la non-application de certaines parties de ce cadre ne signifie pas retour à la liberté totale. Les contrôles préexistants sur les entités chinoises et assimilées restent en vigueur.

Cette distinction est importante pour les fournisseurs cloud, intégrateurs, brokers de matériel et opérateurs de data centers. Les règles ne se limitent pas à “où part le colis ?”. Elles demandent une diligence sur “qui contrôle vraiment le destinataire ?”. Dans un marché où les chaînes d’approvisionnement passent par des revendeurs, holdings et filiales, ce n’est pas un détail administratif ; c’est le cœur du contrôle.

## Nvidia au centre, même quand le texte ne parle pas que de Nvidia

Le document du BIS ne nomme pas uniquement Nvidia. Il parle d’articles de calcul avancé soumis à l’EAR. Mais l’enjeu public tourne évidemment autour de Nvidia, parce que ses accélérateurs sont la ressource critique de l’entraînement frontier et des grands clusters d’inférence.

Al Jazeera cite un porte-parole de Nvidia affirmant que la guidance confirme l’approche existante de l’entreprise : des licences sont requises pour expédier des produits contrôlés à des entreprises dont le siège est en République populaire de Chine. Nvidia soutient donc que ses procédures de vente et de vérification sont déjà alignées avec la clarification.

Il faut rester prudent sur l’ampleur réelle du contournement. Les articles de presse mentionnent des préoccupations et des soupçons sur des achats via filiales, mais les volumes exacts ne sont pas vérifiés publiquement. La note du BIS elle-même ne chiffre rien. Elle donne une interprétation de règle et rappelle un devoir de licence ; elle ne constitue pas, à elle seule, une preuve que des centaines de milliers de puces auraient effectivement transité par cette voie.

## Data centers : pas d’arrêt immédiat des équipements déjà utilisés

Un passage de la guidance est particulièrement révélateur. Le BIS indique que les opérateurs bona fide de data centers, engagés par ailleurs dans des activités compatibles avec l’EAR, ne sont pas tenus de cesser l’usage, le stockage, la disposition ou la maintenance des articles de calcul avancé à cause de cette guidance, jusqu’à nouvel ordre.

Cette phrase fait deux choses à la fois. Elle évite de déclencher un chaos opérationnel immédiat pour des infrastructures déjà installées. Mais elle confirme aussi que le régulateur pense à des cas concrets d’équipements déjà en circulation. L’objectif semble être de bloquer ou licencier les flux futurs plutôt que d’ordonner brutalement l’extinction de racks existants.

Pour les clouds et hébergeurs, cela crée une zone de conformité plus exigeante. Il ne suffit plus de vérifier la localisation du data center ou du client contractuel direct. Il faut comprendre la chaîne de propriété, le contrôle ultime et les droits d’usage. Les revendeurs qui vivaient confortablement dans l’ambiguïté vont découvrir les joies de la due diligence renforcée. Ambiance tableur, mais avec géopolitique dedans.

## Effets probables sur la course aux modèles

À court terme, cette clarification ne change probablement pas l’équilibre entre OpenAI, Anthropic, Google, Meta ou xAI : ces acteurs sécurisent leur compute par des accords hyperscale, des clusters dédiés et des partenariats cloud. L’effet se situe plutôt sur les acteurs chinois ou liés à la Chine qui cherchent de la capacité hors territoire, et sur les intermédiaires susceptibles de leur vendre l’accès à des GPU contrôlés.

À moyen terme, le message est plus large : la course aux modèles reste inséparable de la chaîne d’approvisionnement matérielle. Les paramètres, les benchmarks et les agents font les titres ; les licences export décident souvent qui peut acheter combien de compute, où et à quel prix. Les contrôles américains ne stoppent pas l’innovation chinoise, mais ils augmentent le coût, la complexité et l’incertitude de l’accès aux puces les plus avancées.

Cela peut pousser davantage d’efforts vers trois directions : puces domestiques chinoises, architectures plus efficaces et entraînement/inférence distribués hors des GPU américains de pointe. Aucun de ces chemins n’est simple. Les modèles récents montrent qu’on peut extraire plus de performance d’un budget compute donné, mais l’entraînement frontier reste une affaire de densité, réseau, mémoire et énergie.

## Ce qu’il faut retenir

La guidance du BIS n’est pas une nouvelle interdiction spectaculaire ; c’est une clarification d’application. Mais elle a une portée stratégique nette : les États-Unis veulent empêcher que les contrôles sur les puces IA soient contournés via des filiales étrangères de groupes chinois.

Le point à surveiller maintenant sera l’exécution : licences refusées, contrôles chez les intermédiaires, pressions sur les data centers tiers, et éventuelles réponses chinoises. Les règles export sont rarement propres. Elles avancent par clarification, exceptions, lettres, enforcement et signaux politiques. Mais dans une industrie où le compute est la matière première, même une note de trois pages peut faire beaucoup de bruit.

## Sources

- BIS — Guidance Regarding Enforcement of License Requirements for Advanced Computing Items : https://www.bis.gov/media/documents/bis-guidance-may-31-2026.pdf
- Al Jazeera — US says ban on AI chip shipments applies to Chinese firms outside China : https://www.aljazeera.com/economy/2026/6/1/us-says-ban-on-ai-chip-shipments-applies-to-chinese-firms-outside-china
- Reuters — US takes step to halt Nvidia AI chip shipments to Chinese firms outside China : https://www.reuters.com/world/china/us-takes-step-halt-nvidia-ai-chip-shipments-chinese-firms-outside-china-2026-05-31/
