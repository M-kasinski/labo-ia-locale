---
title: "Ideogram 4.0 : l’image open-weight s’attaque enfin au design lisible"
description: "Ideogram publie son premier modèle image open-weight : un DiT 9,3B spécialisé dans la typo, les layouts et les prompts JSON structurés. Intéressant pour le local, mais licence non commerciale."
pubDate: 2026-06-03
tags: ["image-generation", "open-weight", "comfyui", "local-ai"]
author: "Labo IA Locale"
draft: false
sources:
  - label: "Ideogram — Ideogram 4.0 Technical Details"
    url: "https://ideogram.ai/blog/ideogram-4.0/"
  - label: "GitHub — ideogram-oss/ideogram4"
    url: "https://github.com/ideogram-oss/ideogram4"
  - label: "ComfyUI Blog — Ideogram 4.0 Day-0 Support"
    url: "https://blog.comfy.org/p/ideogram-4-day-0-support-in-comfyui"
---

Ideogram a publié **Ideogram 4.0**, son premier modèle text-to-image à poids ouverts. Ce n’est pas un énième checkpoint “joli sur trois prompts de démo” : le point intéressant, pour l’IA locale, est ailleurs. Le modèle vise explicitement les usages de design — affiches, compositions, typographie, texte lisible dans l’image — avec une architecture documentée, du code public, des poids disponibles sur Hugging Face et un support ComfyUI dès le jour zéro.

La nuance importante arrive tout de suite : **les poids ne sont pas sous licence libre commerciale**. Le dépôt GitHub du code est en Apache-2.0, mais les poids sont publiés sous licence **Ideogram 4 Non-Commercial**. Pour bidouiller, évaluer, intégrer dans un workflow personnel ou prototyper localement, c’est intéressant. Pour bâtir un produit dessus, il faudra lire la licence plutôt que demander pardon après coup — stratégie rarement optimale quand des avocats savent utiliser Ctrl+F.

## Ce qui est publié

D’après le billet technique officiel d’Ideogram, **Ideogram 4.0 est un modèle text-to-image open-weight de 9,3 milliards de paramètres**. Le dépôt `ideogram-oss/ideogram4` précise qu’il s’agit d’un modèle de fondation entraîné depuis zéro, pas d’un fine-tune d’un modèle existant. Les poids sont proposés notamment en variantes **nf4** et **fp8**, avec un tableau de compatibilité indiquant que la version nf4 vise CUDA et que la version fp8 est plus générale côté matériel.

Le modèle est un **Diffusion Transformer single-stream** de 34 couches. Les tokens texte et image partagent une même séquence d’attention, avec QK-RMSNorm, MRoPE et un MLP SwiGLU. Le billet d’Ideogram indique aussi que le DiT 9,3B est le seul composant entraîné : l’encodeur texte et le VAE restent gelés.

C’est une approche assez moderne dans les modèles image ouverts : au lieu de bricoler autour d’un pipeline figé façon vieux couple CLIP + U-Net, Ideogram assume un gros backbone DiT et une représentation commune texte-image. Pas magique, mais cohérent avec l’évolution récente du secteur.

## Le choix technique le plus intéressant : Qwen3-VL comme encodeur texte

Le détail qui mérite vraiment l’attention : Ideogram 4.0 utilise **Qwen3-VL-8B-Instruct comme encodeur texte**, en mode texte seul, au lieu d’un encodeur text-only classique comme CLIP ou T5. Selon Ideogram, le DiT consomme les états cachés de **13 couches intermédiaires** de Qwen3-VL, concaténés le long de la dimension de features.

Sur le papier, c’est un choix sensé pour un modèle de design. Un VLM encode déjà des relations visuelles, des objets, des styles et des descriptions spatiales d’une manière plus riche qu’un encodeur texte pur. Ideogram parie donc que cet encodeur apporte une meilleure compréhension des concepts visuels et des contraintes de composition.

Il faut rester prudent : les gains exacts attribuables à ce choix ne sont pas isolés publiquement par une ablation exhaustive dans les sources consultées. Mais l’architecture est suffisamment documentée pour être intéressante à reproduire ou à tester par d’autres labs open-weight.

## Les prompts JSON : moins sexy, plus utile

L’autre particularité forte est le **prompting structuré en JSON**. Ideogram explique avoir entraîné le modèle exclusivement sur des captions JSON structurées, incluant description globale, style, éléments individuels, boîtes englobantes optionnelles, palettes de couleurs et textes typés.

Le blog ComfyUI résume bien l’intérêt pratique : un prompt plat donne une image ; le JSON donne du contrôle. Le format permet notamment :

- des **palettes de couleurs** avec jusqu’à 16 couleurs hexadécimales par image et jusqu’à 5 par élément ;
- des **bounding boxes** en coordonnées normalisées `[y_min, x_min, y_max, x_max]` sur une grille 0–1000 ;
- des éléments de type `text` où la chaîne à rendre est séparée de son style visuel ;
- une décomposition de la scène en arrière-plan et éléments.

Pour les workflows locaux, c’est probablement plus important qu’un score de leaderboard. La génération d’image locale souffre souvent d’un problème très concret : obtenir une composition reproductible sans passer vingt minutes à relancer des seeds. Un format structuré ne résout pas tout, mais il rend les contraintes explicites. Pour de la maquette, des couvertures, des visuels de blog ou des affiches, c’est exactement le genre de contrôle qui manque aux pipelines trop “prompt poétique et prière silencieuse”.

## ComfyUI dès le jour zéro

ComfyUI annonce un **support natif day-0** d’Ideogram 4.0. Le billet fournit un workflow `image_ideogram4_t2i.json`, renvoie vers les poids hébergés côté Comfy-Org sur Hugging Face, et décrit l’usage du format JSON dans les nodes.

C’est important parce que ComfyUI est devenu l’un des points d’entrée les plus réalistes pour exécuter des modèles image localement. Un modèle open-weight sans intégration pratique reste souvent un artefact de leaderboard. Ici, l’intégration immédiate rend le test beaucoup plus simple pour les utilisateurs déjà équipés en GPU NVIDIA.

La version nf4 mentionnée dans le dépôt vise CUDA. Pour Apple Silicon, CPU pur ou autres accélérateurs, il faudra probablement attendre des conversions, optimisations ou chemins d’exécution plus mûrs. La source officielle indique aussi une variante fp8, mais cela ne garantit pas une expérience fluide sur toutes les machines. À ce stade, le “local” veut surtout dire : local sur machine correctement dotée, pas forcément sur MacBook Air entre deux cafés.

## Performances : prometteur, mais à lire froidement

Ideogram affirme que son modèle obtient de très bons résultats en rendu de texte et en design, et le dépôt GitHub met en avant des comparaisons avec des modèles ouverts plus grands comme Qwen-Image, FLUX.2 [dev] ou HunyuanImage 3.0. Le README cite aussi Design Arena, LMArena et une évaluation typographique menée par ContraLabs avec des designers professionnels.

Ces éléments sont intéressants, mais ils doivent être lus avec prudence. Une partie des benchmarks est rapportée par Ideogram lui-même ; d’autres reposent sur des arènes ou des préférences humaines, utiles mais sensibles au choix des prompts, au filtrage et au profil des juges. La bonne conclusion n’est donc pas “Ideogram 4.0 écrase tout”. La conclusion raisonnable est : **le modèle semble particulièrement fort sur le rendu de texte et les compositions orientées design, avec assez de matière publique pour être testé sérieusement**.

Et c’est déjà beaucoup. Le rendu de texte reste l’un des talons d’Achille historiques des modèles image locaux. Si Ideogram 4.0 réduit vraiment l’écart avec les systèmes fermés sur ce point, même sous licence non commerciale, il devient un modèle de référence pour les workflows créatifs auto-hébergés.

## Ce que ça change pour l’IA locale

Pour Labo IA Locale, Ideogram 4.0 est intéressant pour trois raisons.

D’abord, il pousse l’open-weight image vers des usages plus professionnels : typographie, layout, palette, contraintes spatiales. Ce sont les détails qui transforment un générateur amusant en outil de production.

Ensuite, il montre que les modèles multimodaux texte-image peuvent aussi bénéficier de briques issues des VLM récents. L’usage de Qwen3-VL comme encodeur texte est une piste technique que d’autres projets vont probablement examiner.

Enfin, il confirme une tendance saine : publier les poids ne suffit plus. Il faut du code, une intégration ComfyUI ou équivalente, des quantizations, une documentation de prompting, et des limites clairement exposées. Ideogram coche beaucoup de cases, sauf la plus frustrante pour l’écosystème libre : la licence commerciale.

## À retenir

Ideogram 4.0 est une sortie solide pour l’IA locale orientée image : **9,3B paramètres, poids ouverts, prompts JSON structurés, support ComfyUI immédiat, focus net sur le texte et le design**. Ce n’est pas un modèle open-source au sens plein côté poids, et il ne faut pas extrapoler les benchmarks officiels sans tests indépendants. Mais pour les utilisateurs qui veulent expérimenter localement avec des visuels structurés et du texte lisible, c’est clairement un modèle à surveiller.

### Sources

- [Ideogram — Ideogram 4.0 Technical Details](https://ideogram.ai/blog/ideogram-4.0/)
- [GitHub — ideogram-oss/ideogram4](https://github.com/ideogram-oss/ideogram4)
- [ComfyUI Blog — Ideogram 4.0 Day-0 Support](https://blog.comfy.org/p/ideogram-4-day-0-support-in-comfyui)
