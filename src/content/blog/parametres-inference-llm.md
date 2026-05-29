---
title: "Temperature, top-p, top-k : régler les paramètres d'inférence d'un LLM local"
description: "Guide concret des paramètres de sampling (temperature, top-p, top-k, repeat penalty, min-p) pour contrôler la génération d'un LLM local via Ollama ou llama.cpp."
pubDate: 2026-05-29
tags: ["ia-locale", "inference", "sampling", "ollama"]
author: "Labo IA Locale"
draft: true
sources:
  - { label: "Ollama — Modelfile Reference", url: "https://docs.ollama.com/modelfile" }
  - { label: "Ollama — API generate endpoint", url: "https://docs.ollama.com/api/generate" }
  - { label: "llama.cpp — Server README (sampling params)", url: "https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md" }
  - { label: "Hugging Face — GenerationConfig documentation", url: "https://huggingface.co/docs/transformers/main_classes/text_generation" }
---

Quand tu lances un modèle local avec Ollama, llama.cpp ou Oobabooga, tu tombes sur une poignée de paramètres : `temperature`, `top_p`, `top_k`, `repeat_penalty`… Des noms techniques, des valeurs par défaut qui varient d'un runtime à l'autre, et un effet pas toujours intuitif sur la sortie.

Cet article décrypte chaque paramètre, explique ce qu'il fait *vraiment* à la distribution de probabilités du modèle, et te donne des réglages concrets selon ton usage.

## Comment un LLM génère du texte

Avant de toucher aux boutons, comprenons le mécanisme de base.

Un LLM ne « choisit » pas un mot — il choisit un **token** (un morceau de texte, parfois une syllabe ou un caractère). À chaque étape, le modèle produit une **distribution de probabilités** sur tout son vocabulaire (des milliers, voire des dizaines de milliers de tokens). Le token le plus probable n'est pas automatiquement sélectionné : c'est là qu'interviennent les paramètres de **sampling** (échantillonnage).

Sans aucun paramètre de sampling, on ferait un tirage aléatoire pondéré sur la distribution brute du softmax. En pratique, on applique une chaîne de filtres et de transformations avant de tirer. L'ordre d'application compte — et il varie selon le runtime.

> **Chaîne par défaut dans llama.cpp** (v2025+) :
> `penalties → dry → top_n_sigma → top_k → typ_p → top_p → min_p → xtc → temperature`
>
> Source : [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)

Chaque paramètre que nous détaillons ci-dessous agit à une étape précise de cette chaîne.

## Temperature

**Ce qu'il fait** : La temperature agit sur les logits bruts du modèle *avant* le softmax. Elle divise les logits par la valeur de la temperature, ce qui aplatit ou accentue la distribution de probabilités.

- **Temperature basse** (0.1–0.3) : la distribution se « pique » — le token le plus probable domine. Sortie plus déterministe, plus factuelle, moins variée.
- **Temperature haute** (1.0–1.5+) : la distribution s'aplatit — les tokens moins probables ont plus de chances d'être tirés. Sortie plus créative, plus diversifiée, potentiellement plus incohérente.
- **Temperature = 0** : le modèle fait du **greedy decoding** — il prend systématiquement le token le plus probable. Résultat entièrement déterministe (si la seed est fixe).

**Valeurs par défaut** :

| Runtime | Défaut |
|---------|--------|
| Ollama | 0.8 |
| llama.cpp (CLI) | 0.80 |
| Hugging Face transformers | 1.0 |

**Exemple Ollama** :

```bash
# Créatif — température élevée
ollama run llama3.2 --options '{"temperature": 1.2}'

# Factuel — température basse
ollama run llama3.2 --options '{"temperature": 0.1}'
```

**Exemple dans un Modelfile** :

```
FROM llama3.2
PARAMETER temperature 0.3
```

## Top-k

**Ce qu'il fait** : Ne conserve que les **k tokens les plus probables** et rejette le reste (leur probabilité est mise à zéro). Le tirage se fait ensuite sur ce sous-ensemble réduit.

- **top_k = 40** : seuls les 40 tokens les plus probables sont considérés. C'est un filtre grossier mais efficace pour éliminer les choix absurdes en queue de distribution.
- **top_k = 1** : équivaut au greedy decoding (toujours le même token).
- **top_k = 0** : désactivé — toute la distribution est prise en compte.

**Valeurs par défaut** :

| Runtime | Défaut |
|---------|--------|
| Ollama | 40 |
| llama.cpp | 40 (0 = désactivé) |
| Hugging Face transformers | 50 |

**Effet concret** : top-k seul peut créer des transitions abruptes. Si les 40 premiers tokens couvrent déjà 99.9% de la masse de probabilité, l'effet est minime. Si la distribution est plate (beaucoup de tokens avec des probabilités proches), top-k coupe radicalement l'espace de choix. C'est pourquoi on le combine généralement avec top-p.

## Top-p (Nucleus Sampling)

**Ce qu'il fait** : Au lieu de garder un nombre fixe de tokens, on garde **le plus petit sous-ensemble de tokens dont la probabilité cumulée atteint p**.

Concrètement : on trie les tokens par probabilité décroissante, on additionne les probabilités jusqu'à atteindre le seuil `p`, et on rejette tout le reste.

- **top_p = 0.9** : on garde les tokens qui couvrent 90% de la masse de probabilité. Le nombre effectif de tokens retenus varie à chaque étape — parfois 5, parfois 200 — selon que la distribution est pointue ou plate.
- **top_p = 1.0** : désactivé — toute la distribution est conservée.
- **top_p = 0.1** : très restrictif — on ne garde que les tokens les plus probables.

**Valeurs par défaut** :

| Runtime | Défaut |
|---------|--------|
| Ollama | 0.9 |
| llama.cpp | 0.95 (1.0 = désactivé) |
| Hugging Face transformers | 1.0 |

**Pourquoi top-p est souvent préféré à top-k seul** : top-p s'adapte automatiquement à la « confiance » du modèle. Quand le modèle est sûr (distribution pointue), top-p retient peu de tokens. Quand il est hésitant (distribution plate), il en retient plus. C'est un filtre qui respire avec le modèle.

**Exemple API Ollama** :

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Explique la relativité restreinte simplement :",
  "options": {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40
  }
}'
```

## Repeat penalty (pénalité de répétition)

**Ce qu'il fait** : Pénalise exponentiellement les tokens qui sont déjà apparus dans les derniers `n` tokens générés. Chaque fois qu'un token est généré, sa probabilité future est divisée par le facteur `repeat_penalty` (si > 1) ou multipliée (si < 1).

- **repeat_penalty = 1.0** : désactivé — aucune pénalité.
- **repeat_penalty = 1.1–1.3** : valeur typique — réduit modérément la probabilité des tokens déjà vus, sans les éliminer.
- **repeat_penalty > 1.5** : effet fort — peut rendre le texte artificiel ou forcer le modèle à chercher des formulations improbables.

**Valeurs par défaut** :

| Runtime | Défaut |
|---------|--------|
| Ollama | 1.0 (désactivé) |
| llama.cpp (CLI) | 1.00 |
| llama.cpp (API `/completion`) | 1.1 |
| Hugging Face transformers | 1.0 |

Le nombre de tokens pris en compte pour la pénalité est contrôlé par `repeat_last_n` (llama.cpp) ou `presence_penalty`/`frequency_penalty` (OpenAI-style). Par défaut dans llama.cpp, `repeat_last_n = 64`.

**Effet concret** : sans pénalité, les petits modèles ont tendance à boucler sur des phrases. Avec une pénalité trop forte, le modèle évite les mots courants (« le », « de », « est ») et produit du texte bizarre. C'est un équilibre délicat.

## Min-p

**Ce qu'il fait** : Garde uniquement les tokens dont la probabilité est supérieure à **p × probabilité du token le plus probable**. C'est un seuil *relatif* — il s'adapte automatiquement à la confiance du modèle à chaque étape.

- **min_p = 0.05** : un token est conservé s'il a au moins 5% de la probabilité du token le plus probable. Si le top token a 0.8, le seuil est 0.04.
- **min_p = 0** : désactivé.

**Valeurs par défaut** :

| Runtime | Défaut |
|---------|--------|
| Ollama | 0 (désactivé dans les versions récentes) |
| llama.cpp | 0.05 |
| Hugging Face transformers | non défini (valeurs typiques : 0.01–0.2) |

**Min-p vs top-p** : min-p est plus strict que top-p dans les cas où la distribution est très plate — il peut éliminer plus de tokens que top-p seul. Certains utilisateurs le combinent avec top-p pour un filtrage en deux étapes. D'autres préfèrent en utiliser un seul.

## Autres paramètres importants

### num_ctx (context length / taille de la fenêtre de contexte)

**Ce qu'il fait** : Détermine combien de tokens le modèle peut « se souvenir » dans la conversation. C'est la taille du KV cache.

- Si tu dépasse cette limite, les tokens les plus anciens sont oubliés (ou tronqués, selon le runtime).
- Augmenter `num_ctx` consomme plus de mémoire — la taille du cache KV croît linéairement avec le nombre de tokens.

**Valeurs par défaut** : dépend du modèle. Ollama charge la valeur par défaut du modèle (souvent 4096 ou 8192). llama.cpp charge depuis le fichier GGUF (`--ctx-size 0`).

```bash
# Ollama — augmenter le contexte à 16k tokens
ollama run llama3.2 --options '{"num_ctx": 16384}'
```

### num_predict / max_tokens (nombre max de tokens générés)

**Ce qu'il fait** : Limite le nombre de tokens que le modèle peut générer en sortie. Utile pour éviter les réponses interminables ou contrôler les coûts.

**Valeurs par défaut** :

| Runtime | Défaut |
|---------|--------|
| Ollama | dépend du modèle |
| llama.cpp | -1 (infini) |
| Hugging Face transformers | non défini (le modèle génère jusqu'au token EOS) |

## Tableau récapitulatif

| Paramètre | Effet | Ollama | llama.cpp | HF transformers |
|-----------|-------|--------|-----------|-----------------|
| `temperature` | Aplatit/pique la distribution | 0.8 | 0.80 | 1.0 |
| `top_k` | Garde les k tokens les plus probables | 40 | 40 | 50 |
| `top_p` | Garde les tokens couvrant p% de la masse | 0.9 | 0.95 | 1.0 |
| `min_p` | Seuil relatif au token le plus probable | 0 | 0.05 | — |
| `repeat_penalty` | Pénalise les répétitions | 1.0 | 1.00 (API: 1.1) | 1.0 |
| `repeat_last_n` | Fenêtre de tokens surveillée | 64 (via `presence_penalty`) | 64 | — |
| `num_ctx` | Taille de la fenêtre de contexte | Modèle | Modèle | Modèle |
| `num_predict` | Max tokens générés | Modèle | -1 (∞) | — |

> **Note** : les valeurs par défaut varient selon le runtime, la version, et parfois le modèle lui-même. Les chiffres ci-dessus reflètent les défauts des runtimes en l'absence de configuration dans le fichier du modèle. Vérifie toujours la doc de ta version.

## En pratique

Voici des réglages qui marchent, testés sur des modèles de 7 à 14B paramètres (Llama 3.2, Mistral, Qwen).

### Chat créatif (rédaction, brainstorming, fiction)

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Écris une courte histoire de science-fiction :",
  "options": {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 50,
    "repeat_penalty": 1.1
  }
}'
```

- Temperature élevée pour la diversité.
- Top-p légèrement plus large (0.95) pour laisser le modèle explorer.
- Top-k à 50 pour ne pas couper trop tôt.
- Pénalité de répétition légère (1.1) pour éviter les boucles sans étouffer le vocabulaire.

### Génération de code

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder:7b",
  "prompt": "Fonction Python pour trier un tableau :",
  "options": {
    "temperature": 0.1,
    "top_p": 0.5,
    "top_k": 10,
    "repeat_penalty": 1.0
  }
}'
```

- Temperature très basse : on veut le code le plus probable, pas des variantes créatives.
- Top-p restrictif : réduit les risques de syntaxe improbable.
- Top-k bas : ne garde que les choix les plus sûrs.
- Pas de pénalité de répétition : le code légitimement répète des mots-clés (`for`, `return`, `def`).

### Extraction factuelle / Q&R

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Quelle est la capitale de l'Australie ?",
  "options": {
    "temperature": 0.0,
    "top_p": 0.1,
    "top_k": 5,
    "repeat_penalty": 1.0
  }
}'
```

- Temperature à 0 : greedy decoding — réponse la plus probable, reproductible.
- Top-p très restrictif : on ne veut qu'une seule réponse claire.
- Top-k à 5 : garde uniquement les choix les plus évidents.

### Usage généraliste (conversation polyvalente)

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Ton prompt ici",
  "options": {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "repeat_penalty": 1.1
  }
}'
```

C'est essentiellement les valeurs par défaut d'Ollama, avec une légère pénalité de répétition ajoutée. Un bon point de départ quand tu ne sais pas quoi toucher.

## Règle d'or

Commence toujours par les défauts du runtime. Modifie **un seul paramètre à la fois** et observe l'effet. La temperature est le bouton le plus impactant — c'est par là qu'il faut commencer. top-p et top-k sont des filtres secondaires qui affinent. La pénalité de répétition est un correctif à activer uniquement si le modèle boucle.

Et n'oublie pas : un bon prompt bien rédigé fait souvent plus pour la qualité de la réponse que n'importe quel réglage de sampling.
