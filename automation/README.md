# Labo IA Source Radar

Collecteur de signaux IA fiables pour alimenter le cron éditorial sans dépendre de X/Twitter.

## Principe

Le cron doit d'abord lire `automation/latest_signals.json`, puis utiliser `web_search` uniquement pour vérifier un signal déjà identifié. X Search/XUrl ne sont pas utilisés par ce collecteur.

Sources MVP :

- RSS officiels : OpenAI, Hugging Face Blog
- GitHub releases Atom : llama.cpp, Ollama, vLLM, MLX, MLX LM
- Hugging Face Hub API : modèles `text-generation` créés/modifiés récemment
- arXiv API : catégories `cs.CL`, `cs.LG`, `cs.AI`, `cs.CV`

## Commandes

Tester chaque source configurée :

```bash
python3 automation/collect_ai_sources.py --check-sources
```

Générer le radar sans modifier l'état anti-doublons :

```bash
python3 automation/collect_ai_sources.py
```

Générer le radar et marquer les URLs comme vues :

```bash
python3 automation/collect_ai_sources.py --update-state
```

## Sorties runtime

- `latest_signals.json` : shortlist courante pour l'agent éditorial
- `source_state.json` : URLs déjà vues
- `runs/*.json` : snapshots horodatés des collectes

Ces fichiers sont ignorés par Git pour éviter de polluer les commits du site.
