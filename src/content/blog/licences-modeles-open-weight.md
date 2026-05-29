---
title: "Open-weight vs open-source : comprendre les licences des modèles d'IA"
description: "Télécharger gratuitement un modèle d'IA ne signifie pas que tout est permis. Guide pratique des licences Apache 2.0, Llama Community, Gemma et MRL pour les devs et PME."
pubDate: 2026-05-29
tags: ["ia-locale", "licences", "open-source", "open-weight"]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "Apache License 2.0 (texte officiel)", url: "https://www.apache.org/licenses/LICENSE-2.0" }
  - { label: "Llama 3.1 Community License Agreement", url: "https://www.llama.com/llama3_1/license/" }
  - { label: "Gemma Terms of Use (Google)", url: "https://ai.google.dev/gemma/terms" }
  - { label: "Gemma 4 — Apache 2.0", url: "https://ai.google.dev/gemma/apache_2" }
  - { label: "Mistral AI Research License (MRL)", url: "https://mistral.ai/static/licenses/MRL-0.1.md" }
  - { label: "Qwen3 — Apache 2.0 (Hugging Face)", url: "https://huggingface.co/Qwen/Qwen3-32B/blob/main/LICENSE" }
  - { label: "Mistral 3 — Apache 2.0 (annonce officielle)", url: "https://mistral.ai/news/mistral-3/" }
  - { label: "OSI Open Source Definition", url: "https://opensource.org/osd" }
---

## Open-weight ≠ open-source : la confusion qui coûte cher

Tu télécharges un modèle de 7 milliards de paramètres sur Hugging Face. C'est gratuit. Les poids sont là. Tu peux les lancer sur ta machine, les fine-tuner, les distribuer.

**Mais « gratuit à télécharger » ne veut pas dire « tout est permis ».**

C'est la distinction fondamentale entre **open-weight** et **open-source**. Un modèle open-weight, c'est un modèle dont les poids sont accessibles — téléchargeables, utilisables localement. Mais la licence qui l'accompagne peut imposer des restrictions lourdes : pas d'usage commercial, plafond d'utilisateurs, obligation de propagation des restrictions, droit de révocation unilatéral.

Un modèle open-source, au sens de l'[Open Source Initiative](https://opensource.org/osd), respecte 10 critères stricts : redistribution libre, source disponible, dérivés autorisés, pas de discrimination par personne, par domaine d'usage, ni par projet. Apache 2.0 et MIT répondent à ces critères. Les licences « communautaires » de Meta et Google, non.

Pour une PME qui veut intégrer un modèle en production, la différence est cruciale. Décryptage.

## Les vraies licences open-source permissives

### Apache 2.0

C'est la référence. Approuvée par l'OSI. Utilisée par des milliers de projets logiciels et, de plus en plus, des modèles d'IA.

**Ce qu'elle autorise :**
- Usage commercial sans restriction
- Modification, fine-tuning, création de dérivés
- Redistribution libre (avec conservation du NOTICE et des mentions de copyright)
- Licence de brevet explicite (les contributeurs cèdent une licence sur les brevets couvrant leur contribution)

**Ce qu'elle exige :**
- Inclure une copie de la licence dans toute redistribution
- Mentionner les fichiers modifiés
- Conserver les notices de copyright, brevet et marque

**Modèles sous Apache 2.0 :**
- **Qwen3** (Alibaba Cloud) — vérifié sur [Hugging Face](https://huggingface.co/Qwen/Qwen3-32B/blob/main/LICENSE)
- **Mistral 3** (Mistral AI) — Ministral 3B/8B/14B et Mistral Large 3, tous sous Apache 2.0 selon [l'annonce officielle](https://mistral.ai/news/mistral-3/)
- **Mistral Small 3** (Mistral AI) — Apache 2.0, confirmé sur [Hugging Face](https://huggingface.co/mistralai/Mistral-Small-24B-Instruct-2501)
- **Gemma 4** (Google) — passage à Apache 2.0 confirmé sur [ai.google.dev/gemma/apache_2](https://ai.google.dev/gemma/apache_2)

**En résumé :** Apache 2.0 = tu peux faire ce que tu veux, y compris commercialiser, sans plafond d'utilisateurs, sans demande d'autorisation. C'est la licence la plus sereine pour une production.

### MIT

Plus courte, plus simple que Apache 2.0. Même philosophie permissive : usage commercial libre, modification, redistribution. Pas de licence de brevet explicite (contrairement à Apache 2.0).

Quelques modèles de recherche et petits modèles utilisent MIT, mais c'est moins courant dans l'écosystème des LLM grand format.

## Les licences « communautaires » avec restrictions

### Llama Community License (Meta)

Utilisée par Llama 3, 3.1, 3.2, 3.3 (et probablement Llama 4). Texte officiel sur [llama.com](https://www.llama.com/llama3_1/license/).

**Ce qu'elle autorise :**
- Usage commercial **sous condition**
- Modification, fine-tuning, création de dérivés
- Redistribution (avec propagation de la licence)

**Restrictions majeures :**
- **Plafond de 700 millions d'utilisateurs actifs mensuels (MAU)** : si ton produit ou service dépasse ce seuil, tu dois obtenir une licence séparée de Meta, à sa seule discrétion. Ce plafond s'applique au produit/service dans son ensemble, pas uniquement à la fonctionnalité IA.
- **Attribution obligatoire** : mention « Built with Llama » visible sur le site, l'interface, le blog ou la documentation. Si tu crées un modèle dérivé, son nom doit commencer par « Llama ».
- **Politique d'usage acceptable** incorporée par référence : tu ne peux pas enfreindre les règles de Meta sur les usages interdits.
- **Virale** : les dérivés doivent être redistribués sous la même Llama Community License. Tu ne peux pas relicenser en Apache 2.0 ou MIT.
- **Droit de révocation** : Meta peut révoquer ta licence en cas de violation.
- **Juridiction californienne** pour tout litige.

**Qui est touché par le plafond de 700M MAU ?**
En pratique, presque personne. Mais la licence ne définit pas clairement « utilisateur actif mensuel ». Une plateforme B2B dont les clients ont chacun des milliers d'employés pourrait théoriquement franchir le seuil. Une API dont les développeurs construisent des apps utilisées par des millions de personnes — est-ce que les utilisateurs finaux comptent ? L'ambiguïté reste un risque juridique.

### Gemma Terms of Use (Google)

Utilisée par Gemma 1, 1.1, 2, 3, 3n et variantes. **Gemma 4 est passé à Apache 2.0** — c'est une évolution notable. Texte officiel sur [ai.google.dev/gemma/terms](https://ai.google.dev/gemma/terms) (dernière modification : 1er avril 2026).

**Ce qu'elle autorise :**
- Usage commercial
- Modification, fine-tuning, création de modèles dérivés
- Redistribution et mise à disposition via service hébergé (API, SaaS…)

**Restrictions majeures :**
- **Politique d'usage interdit (Prohibited Use Policy)** incorporée : tu dois l'imposer contractuellement à tes propres utilisateurs finaux.
- **Virale** : les « Model Derivatives » (modèles fine-tunés, distillés, ou entraînés sur les sorties de Gemma) restent soumis aux mêmes Terms of Use. Les restrictions suivent le modèle, pas le nom du checkpoint.
- **Obligation de propagation** : si tu redistribues, tu dois inclure les restrictions d'usage comme clause exécutoire dans ton propre contrat, fournir une copie des Terms of Use, et joindre un fichier NOTICE.
- **Google se réserve le droit de restreindre l'usage** des Gemma Services s'il estime raisonnablement qu'il y a violation.
- **Droit de révocation unilatéral** : Google peut résilier en cas de violation. Tu dois alors supprimer et cesser toute utilisation et distribution.
- **Juridiction californienne** (Santa Clara County).

**Ce n'est pas une licence open-source au sens OSI.** L'OSI exige l'absence de discrimination par domaine d'usage et la liberté de redistribution sans condition. Les restrictions d'usage imposées par Google, le droit de révocation unilatéral et l'obligation de propagation contractuelle des restrictions sont incompatibles avec la définition open-source.

### Mistral AI Research License (MRL)

Utilisée par certains modèles Mistral plus anciens (Mistral Large 2, etc.). Texte officiel sur [mistral.ai](https://mistral.ai/static/licenses/MRL-0.1.md).

**Ce qu'elle autorise :**
- Usage **exclusivement pour la recherche** (personnel, scientifique, académique, à but non lucratif)
- Modification et création de dérivés
- Redistribution (avec propagation de la licence)

**Restrictions majeures :**
- **PAS D'USAGE COMMERCIAL** : la licence définit explicitement que « Research Purposes » exclut toute activité connectée directement ou indirectement à des opérations commerciales. Cela inclut les tests, les proofs-of-concept destinés à générer des revenus, et toute distribution par une entité commerciale.
- **Virale** : les dérivés restent soumis aux mêmes restrictions.
- **Droit de révocation** : Mistral AI peut résilier en cas de violation.
- **Juridiction française** (tribunaux de Paris).

**Note importante :** Mistral AI est en train de migrer ses modèles vers Apache 2.0. Mistral 3, Mistral Small 3 et les Ministral sont tous sous Apache 2.0. La MRL ne s'applique plus aux nouveaux modèles grand public.

## Tableau comparatif

| Critère | Apache 2.0 | Llama Community | Gemma Terms (v1-3) | MRL (Mistral) |
|---|---|---|---|---|
| **Éditeur** | Apache Foundation | Meta | Google | Mistral AI |
| **OSI-approved** | Oui | Non | Non | Non |
| **Usage commercial** | Oui, sans condition | Oui, si < 700M MAU | Oui, sous restrictions | Non |
| **Fine-tuning libre** | Oui | Oui | Oui | Oui (recherche uniquement) |
| **Redistribution** | Libre (avec NOTICE) | Virale (même licence) | Virale (mêmes restrictions) | Virale (même licence) |
| **Plafond utilisateurs** | Aucun | 700M MAU | Aucun | N/A (pas commercial) |
| **Attribution requise** | NOTICE + copyright | « Built with Llama » | NOTICE + Terms of Use | « Licensed by Mistral AI » |
| **Révocation possible** | Non (irrévocable) | Oui (en cas de violation) | Oui (unilatérale) | Oui (en cas de violation) |
| **Juridiction** | — | Californie | Californie | Paris |
| **Exemples** | Qwen3, Mistral 3, Gemma 4 | Llama 3/3.1/3.2/3.3 | Gemma 1/1.1/2/3 | Mistral Large 2 |

## En pratique : quel modèle choisir pour ta production ?

**Si tu veux zéro risque juridique :**
Choisis un modèle sous **Apache 2.0**. Qwen3, Mistral 3, ou Gemma 4 te permettent de l'intégrer dans un produit commercial, de le fine-tuner, de le redistribuer, sans plafond d'utilisateurs ni demande d'autorisation. C'est la seule catégorie où tu peux dormir tranquille.

**Si Llama t'intéresse :**
La Llama Community License est raisonnable pour 99% des cas. Le seuil de 700M MAU est conçu pour les GAFAM, pas pour une PME ou même une grande entreprise. Mais lis la licence complète — l'ambiguïté sur la définition de MAU et l'obligation d'attribution « Built with Llama » sont des détails à connaître avant de signer.

**Si tu utilises Gemma (v1-v3) :**
L'usage commercial est autorisé, mais tu dois contractuellement imposer les restrictions d'usage de Google à tes propres utilisateurs. C'est une obligation juridique réelle, pas une formalité. Si tu construis un SaaS autour de Gemma, chaque client final doit être soumis aux mêmes restrictions. Consulte un juriste.

**Évite la MRL pour un usage commercial :**
C'est une licence de recherche pure. Utiliser un modèle MRL dans un produit, même en phase de test, constitue une violation.

> **Avertissement :** cet article est à vocation informative et pédagogique. Il ne constitue pas un conseil juridique. Pour toute décision de production, fais valider la licence par un professionnel du droit. Les licences évoluent — vérifie toujours la version en vigueur au moment de ton déploiement.
