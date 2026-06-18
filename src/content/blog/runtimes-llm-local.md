---
title: "Ollama, LM Studio, llama.cpp, vLLM : quel runtime local choisir"
description: "Quatre façons de servir un LLM chez soi ou sur un serveur: Ollama pour démarrer vite, LM Studio pour le bureau, llama.cpp pour le contrôle, vLLM pour la prod."
pubDate: 2026-05-29
category: "local"
tags: ["ia-locale", "ollama", "vllm", "llama-cpp"]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "Ollama API docs", url: "https://docs.ollama.com/api" }
  - { label: "Ollama Modelfile reference", url: "https://docs.ollama.com/modelfile" }
  - { label: "LM Studio home", url: "https://lmstudio.ai" }
  - { label: "LM Studio OpenAI compatibility", url: "https://lmstudio.ai/docs/api/openai-api" }
  - { label: "llama.cpp repository", url: "https://github.com/ggml-org/llama.cpp" }
  - { label: "vLLM online serving docs", url: "https://docs.vllm.ai/en/latest/serving/online_serving/" }
  - { label: "vLLM quickstart", url: "https://docs.vllm.ai/en/latest/getting_started/quickstart.html" }
---

Si tu hésites entre ces quatre outils, commence par cette règle simple: Ollama et LM Studio sont des outils de poste de travail; llama.cpp est le moteur bas niveau; vLLM est une brique de service. Le reste, c'est du marketing ou des discussions de couloir, et ça ne fait pas tourner un modèle.

## Le résumé en une phrase

- Ollama: le plus simple pour lancer un modèle en local avec une API HTTP maison.
- LM Studio: la voie la plus confortable si tu veux une interface graphique et un serveur compatible OpenAI.
- llama.cpp: le moteur brut, en C/C++, avec le plus de contrôle et le plus de terrain couvert.
- vLLM: le choix quand tu veux servir beaucoup de requêtes, sur un vrai serveur GPU, avec du batching continu.

## 1. Ollama: le plus rapide pour démarrer

Ollama vise clairement la simplicité. Le site officiel te propose d'installer avec une seule ligne:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Une fois lancé, l'API locale écoute par défaut sur `http://localhost:11434/api`. Tu peux déjà interroger un modèle avec un simple `curl`.

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Explique la quantization en 2 phrases"
}'
```

Pour le public visé, c'est assez clair: débutant technique, dev solo, data scientist qui veut tester vite, ou quelqu'un qui ne veut pas passer sa soirée à compiler des dépendances. Le bon point, c'est que tu peux aussi personnaliser un modèle avec un `Modelfile`. Le format accepte par exemple `FROM` avec un modèle existant, un dossier de poids Safetensors pour certaines architectures, ou un fichier GGUF.

Côté formats, Ollama est surtout pratique pour consommer des modèles prêts à l'emploi et pour empaqueter ta propre variante. Ce n'est pas l'outil le plus fin pour bricoler l'architecture d'inférence elle-même. C'est exactement pour ça qu'il marche bien: il te cache la plomberie.

## 2. LM Studio: le poste de travail avec une vraie UI

LM Studio est l'option la plus confortable si tu veux une interface graphique. Le site parle explicitement de "local and private" et met en avant le téléchargement de l'app, le catalogue de modèles, et des outils développeur comme un SDK, un CLI et une API.

Son point fort, c'est le serveur compatible OpenAI. La doc officielle liste `/v1/models`, `/v1/responses`, `/v1/chat/completions`, `/v1/embeddings` et `/v1/completions`. En pratique, ça veut dire que beaucoup de clients OpenAI peuvent être branchés dessus en changeant juste le `base_url`.

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama-3.1-8b-instruct",
    "messages": [{"role": "user", "content": "Donne-moi un plan de test"}]
  }'
```

LM Studio est fait pour un usage de bureau: tu télécharges, tu choisis un modèle, tu testes, tu compares. La doc REST expose même des métriques utiles comme les tokens par seconde, le temps avant premier token, l'état chargé ou non chargé, la taille de contexte max et la quantization. C'est nettement plus agréable qu'un terminal quand tu veux explorer plusieurs modèles sans te battre avec la ligne de commande.

Pour les formats, la doc REST montre des modèles en `gguf` et en `mlx`. Donc oui, LM Studio est surtout l'ami du poste Apple Silicon et des modèles déjà préparés pour son écosystème. Ce n'est pas le bon choix si ton objectif est de construire une infra serveur multi-utilisateurs.

## 3. llama.cpp: le moteur sans vernis

`llama.cpp`, c'est le bloc moteur. Le dépôt le décrit comme de l'inférence LLM en C/C++, avec un objectif de setup minimal et de bonnes performances sur beaucoup de machines. Le repo est sous licence MIT.

C'est aussi la base la plus souple si tu veux savoir exactement ce qui se passe. Le projet annonce des quantizations allant de 1.5 à 8 bits, un support Apple Silicon avec Metal, et des backends GPU comme CUDA pour NVIDIA et HIP pour AMD.

```bash
llama-cli -m model.gguf
llama-server -hf ggml-org/gemma-3-1b-it-GGUF
```

Le format central ici, c'est GGUF. C'est le format que tu croises partout dans l'écosystème local parce qu'il est simple à distribuer et facile à charger. Le serveur `llama-server` expose une API compatible OpenAI, avec par exemple un endpoint de chat sur `http://localhost:8080/v1/chat/completions`.

Si tu veux du contrôle, c'est le meilleur terrain. Si tu veux une expérience prête à l'emploi, c'est plus rude. Il faut accepter de mettre les mains dans le cambouis, et le cambouis a parfois raison.

## 4. vLLM: quand tu veux servir du trafic, pas juste discuter avec le modèle

vLLM vise une autre catégorie. Le projet se présente comme un moteur d'inférence et de serving à haut débit, avec gestion mémoire efficace, batching continu et serveur HTTP compatible avec plusieurs interfaces, dont OpenAI. La quickstart officielle parle d'usage offline batched inference et online serving.

C'est le bon outil si tu veux absorber des requêtes en parallèle, servir plusieurs utilisateurs, ou tenir une charge sérieuse sur GPU. En pratique, le chemin principal passe par Linux, Python 3.10 à 3.13, et surtout NVIDIA CUDA. Le guide d'installation couvre aussi AMD ROCm, Intel XPU et Apple Silicon via vLLM-Metal, mais soyons honnêtes: si tu dis "vLLM" dans une équipe, tout le monde pense d'abord à un gros GPU NVIDIA bien nourri.

```bash
uv venv --python 3.12 --seed
source .venv/bin/activate
uv pip install vllm --torch-backend=auto
```

L'API compatible OpenAI couvre `/v1/completions`, `/v1/responses`, `/v1/chat/completions` et `/v1/embeddings`. Côté formats, vLLM travaille surtout avec des modèles Hugging Face, et le projet annonce aussi plusieurs voies de quantization, dont AWQ, GPTQ et GGUF selon le modèle.

La différence avec Ollama et LM Studio est nette: vLLM est fait pour la production et le débit, pas pour le petit test du soir sur le MacBook. Tu peux l'utiliser localement, bien sûr. Mais si tu le choisis, c'est rarement pour le confort. C'est pour encaisser.

## Tableau comparatif

| Outil | Public visé | Matériel cible | Formats / modèles | API compatible OpenAI | Installation |
|---|---|---|---|---|---|
| Ollama | Débutant technique, dev solo, test rapide | Machine perso, local | Modèles de la bibliothèque, Safetensors pour certaines architectures, GGUF via Modelfile | Non, API maison locale | Très simple: script d'installation, puis `ollama run` |
| LM Studio | Utilisateur de bureau, intégration rapide | Poste local, surtout avec UI | GGUF, MLX, catalogue de modèles | Oui | Simple: application desktop + serveur intégré |
| llama.cpp | Utilisateur avancé, bidouilleur, intégrateur | Large spectre CPU/GPU | GGUF au centre, quantization fine | Oui via `llama-server` | Moyenne à difficile: plus bas niveau |
| vLLM | Service, multi-utilisateurs, prod | Serveur GPU, surtout NVIDIA | Modèles Hugging Face, plusieurs quantizations dont AWQ/GPTQ/GGUF selon le modèle | Oui | Plus lourde: Python, environnement propre, dépendances GPU |

## En pratique

Si tu n'as pas encore choisi, installe Ollama en premier. C'est le meilleur moyen de vérifier si ton matériel tient la route, si le modèle te plaît et si ton besoin est vraiment simple ou déjà plus ambitieux.

Prends LM Studio si tu veux une interface graphique et un serveur OpenAI-compatible sans te battre avec le terminal.

Prends llama.cpp si tu veux comprendre, contrôler et intégrer l'inférence au plus près du métal.

Prends vLLM si tu sers plusieurs utilisateurs, que tu as un GPU sérieux, et que ton problème n'est plus "faire marcher un modèle" mais "faire tenir la charge sans tout casser".

En une phrase: pour commencer, Ollama; pour travailler au bureau, LM Studio; pour contrôler la machine, llama.cpp; pour servir du trafic, vLLM. Le reste se discute autour d'un café, pas autour d'un benchmark mal lu.
