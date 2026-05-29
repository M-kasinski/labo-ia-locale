---
title: "Fine-tuner un LLM en local : LoRA et QLoRA expliqués"
description: "Pourquoi et comment fine-tuner un LLM en local avec LoRA et QLoRA, sans exploser la VRAM, avec les outils utiles et des repères concrets."
pubDate: 2026-05-29
tags: ["ia-locale", "fine-tuning", "lora", "qlora"]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "Hugging Face PEFT", url: "https://huggingface.co/docs/peft/index" }
  - { label: "LoRA dans PEFT", url: "https://huggingface.co/docs/peft/main/en/conceptual_guides/adapter" }
  - { label: "Référence LoRA PEFT", url: "https://huggingface.co/docs/peft/main/en/package_reference/lora" }
  - { label: "TRL SFTTrainer", url: "https://huggingface.co/docs/trl/sft_trainer" }
  - { label: "bitsandbytes", url: "https://huggingface.co/docs/transformers/quantization/bitsandbytes" }
  - { label: "QLoRA paper", url: "https://arxiv.org/abs/2305.14314" }
  - { label: "Axolotl", url: "https://docs.axolotl.ai/docs/models/llama-2.html" }
  - { label: "MLX LM", url: "https://github.com/ml-explore/mlx-lm" }
  - { label: "Unsloth", url: "https://github.com/unslothai/unsloth" }
---

Tu as déjà fait tourner un modèle local. Très bien. Maintenant tu veux qu’il parle comme toi, qu’il suive un format précis, ou qu’il tienne mieux un domaine. C’est là que le fine-tuning devient utile.

Le piège, c’est de croire que tout se règle avec un meilleur prompt. Non. Le prompt modifie la consigne du moment. Le RAG ajoute de la connaissance au contexte. Le fine-tuning change le comportement appris par le modèle. Ce n’est pas le même levier, et ce n’est pas la même facture.

## Prompt, RAG, fine-tuning : qui fait quoi ?

Si tu veux juste changer le ton, le format de sortie, ou quelques habitudes de réponse, un bon prompt suffit souvent. C’est le moins cher, le plus rapide, et le plus facile à corriger.

Si ton problème est documentaire, par exemple répondre à partir d’une base de procédures, de tickets, ou de fiches produit qui changent souvent, le RAG est généralement plus malin. Tu ne rééduques pas le modèle, tu lui donnes les bonnes sources au bon moment.

Le fine-tuning sert quand tu veux ancrer un comportement. Même style de réponse à chaque fois. Même structure. Même manière de raisonner sur ton domaine. Là, le modèle doit apprendre, pas juste lire un contexte plus long.

| Approche | Ce qu’on change | Coût | Idéal pour |
|---|---|---:|---|
| Prompt | La consigne | très faible | ton, format, cadrage simple |
| RAG | Le contexte injecté | faible à moyen | base documentaire, infos à jour |
| LoRA / QLoRA | Le comportement appris | faible | style, domaine, routines stables |
| Fine-tuning complet | Tous les poids | élevé | gros budget, cas extrêmes |

## Fine-tuning complet : la version chère

Le fine-tuning complet met à jour tous les paramètres du modèle. Sur le papier, c’est propre. En pratique, c’est lourd. Tu dois stocker les poids, les gradients, l’état de l’optimiseur, et gérer les activations. La mémoire part vite, puis très vite, puis d’un coup tu regardes un OOM comme un vieux camarade qui te connaissait trop bien.

La doc PEFT résume bien la raison d’être de l’approche légère : adapter un grand modèle sans fine-tuner tous ses paramètres, parce que c’est prohibitif. PEFT existe précisément pour éviter ce scénario.

## LoRA : on gèle la base, on n’entraîne que de petits adaptateurs

LoRA, pour Low-Rank Adaptation, garde les poids du modèle de base gelés. Au lieu de modifier directement une grosse matrice de poids, on apprend deux petites matrices de rang faible qui représentent la mise à jour. C’est le cœur de l’idée.

Dans PEFT, la configuration passe surtout par deux paramètres à connaître : `r`, le rang, et `lora_alpha`, le facteur d’échelle. Plus `r` est bas, plus l’adaptateur est petit. Plus il est haut, plus tu donnes de capacité au modèle, mais tu paies en mémoire et en calcul.

En pratique, LoRA se branche souvent sur les projections d’attention. Tu n’as pas besoin de tout toucher. C’est justement le point.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, TaskType

model_id = "meta-llama/Llama-3.1-8B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
)

tokenizer = AutoTokenizer.from_pretrained(model_id)

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
```

La bonne nouvelle, c’est qu’après entraînement tu peux soit charger l’adaptateur par-dessus le modèle de base, soit le fusionner avec `merge_and_unload()` pour obtenir un modèle standalone. Ça évite d’empiler des briques inutiles à l’inférence.

## QLoRA : la même idée, mais sur une base 4-bit

QLoRA pousse le principe plus loin. Le modèle de base est quantizé en 4 bits, puis on entraîne les adaptateurs LoRA au-dessus. La paper QLoRA décrit trois briques importantes : le format 4-bit NF4, la double quantization, et les paged optimizers pour calmer les pics mémoire.

Le point clé, c’est que tu rétropropages dans des adaptateurs LoRA, pas dans tout le modèle. Le modèle de base reste gelé. Résultat : beaucoup moins de VRAM consommée, et un fine-tuning qui devient crédible sur du matériel grand public.

bitsandbytes est la pièce de quantization la plus visible dans l’écosystème Hugging Face. La doc Transformers explique que la 4-bit sert justement à réduire l’empreinte mémoire, tout en gardant l’entraînement des paramètres ajoutés possible.

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(load_in_4bit=True)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    device_map="auto",
    quantization_config=bnb_config,
)
```

## Repères réalistes de VRAM

Les chiffres bougent selon la longueur de contexte, le batch size et les modules ciblés. Mais on peut donner des repères utiles.

Axolotl documente un exemple Llama 2 clair : la variante 7B tient sur n’importe quel GPU 24 Go, et prend environ 17 Go de VRAM en QLoRA, contre environ 20 Go en LoRA. La même page indique que la 13B passe aussi, à condition de réduire `gradient_accumulation_steps` à 2 et `micro_batch_size` à 1.

| Taille | QLoRA sur GPU 24 Go | Lecture pratique |
|---|---|---|
| 7B | confortable | bon point de départ sur une machine perso |
| 13B | possible, mais plus serré | batch plus petit, contexte plus prudent |
| 70B | hors sujet en solo, sauf bricolage sévère | Axolotl cite FSDP + QLoRA sur deux GPU 24 Go |

Sur Apple Silicon, le sujet n’est pas la VRAM mais la mémoire unifiée. MLX LM est justement pensé pour générer et fine-tuner des LLM sur Apple silicon, et le projet annonce aussi le support du low-rank et des modèles quantizés. En clair : ça marche, mais tu restes limité par la mémoire partagée du Mac, pas par une VRAM séparée comme sur NVIDIA.

## L’écosystème à connaître

- PEFT : la brique Hugging Face pour les méthodes parameter-efficient. C’est la base propre pour LoRA.
- TRL et `SFTTrainer` : la voie simple pour superviser un modèle avec des exemples en `text` ou en format conversationnel.
- bitsandbytes : la quantization 4-bit côté Hugging Face.
- Unsloth : orienté vitesse et économie mémoire, avec une intégration Hugging Face fluide.
- Axolotl : le couteau suisse des configs YAML pour fine-tuning local ou distribué.
- MLX / MLX LM : la piste Apple Silicon quand tu veux rester dans l’écosystème Mac.

Unsloth revendique jusqu’à 2x plus de vitesse et jusqu’à 70% de VRAM en moins selon son dépôt. À prendre comme promesse de projet, pas comme loi de la physique, mais l’orientation est claire.

## Ce que tu récupères à la sortie

Tu ne sors pas un nouveau monstre de 40 Go. Tu sors souvent un adaptateur LoRA léger. C’est ça la vraie élégance de la méthode : tu gardes la base, tu ajoutes une couche fine, et tu peux la fusionner ou la charger à la demande.

Pour le déploiement, ça change tout. Tu peux garder plusieurs adaptateurs pour plusieurs tâches, plusieurs styles, plusieurs clients. Une base, plusieurs comportements. Pas besoin de dupliquer le modèle entier à chaque variation.

## En pratique

Si tu débutes, je ferais simple : d’abord LoRA, ensuite QLoRA si la VRAM manque. Pour un 7B, une machine 24 Go est un vrai point de départ. Pour un 13B, ça passe encore, mais il faut accepter des batchs minuscules et arrêter de rêver à des longueurs de contexte infinies.

Mon conseil net : commence par TRL + PEFT si tu veux comprendre ce que tu fais. Passe à Axolotl si tu veux industrialiser le pipeline. Et sur Mac, regarde MLX si tu veux rester natif Apple Silicon. Le reste, c’est du tuning de confort. Le cœur du sujet, lui, est déjà là.
