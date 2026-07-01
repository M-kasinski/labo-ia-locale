# Labo IA Source Radar

Collecteur de signaux IA fiables pour alimenter le cron éditorial sans dépendre de X/Twitter.

## Principe

Le cron doit d'abord lire `automation/latest_signals.json`, puis utiliser `web_search` uniquement pour vérifier un signal déjà identifié. X Search/XUrl ne sont pas utilisés par ce collecteur.

Sources MVP :

- RSS officiels : OpenAI, Hugging Face Blog
- GitHub releases Atom : llama.cpp, Ollama, vLLM, MLX, MLX LM
- Hugging Face Hub API : modèles `text-generation` créés/modifiés récemment
- arXiv API : catégories `cs.CL`, `cs.LG`, `cs.AI`, `cs.CV`
- Hacker News Algolia : signaux communautaires récents (`openai`, `anthropic`, `claude`, `claude code`, `codex`, `open-weight`, `local LLM`, runtimes)

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

Générer un rapport de prévisualisation éditoriale humainement lisible :

```bash
python3 automation/collect_ai_sources.py --dry-run-editorial
```

Ce mode écrit `automation/editorial_preview.md` en plus de `latest_signals.json`.

## Sorties runtime

- `latest_signals.json` : shortlist courante pour l'agent éditorial
- `editorial_preview.md` : rapport Markdown de dry-run pour revue humaine
- `top_article_candidates` : maximum 5 signaux assez solides pour article après revue éditoriale
- `top_radar_candidates` : maximum 10 signaux intéressants mais à vérifier ou trop faibles pour article long
- `source_state.json` : URLs déjà vues
- `runs/*.json` : snapshots horodatés des collectes

Ces fichiers sont ignorés par Git pour éviter de polluer les commits du site.

## Garde-fous MVP 1.5

Le collecteur applique une revue éditoriale avant de sortir la shortlist :

- ignore les releases GitHub dont le titre est seulement une version (`b9856`, `v0.31.1`) ;
- ignore les sujets probablement déjà couverts dans `src/content/blog/` ;
- limite les modèles Hugging Face aux organisations surveillées dans `sources.json` ;
- classe les papiers arXiv et signaux à vérifier en `radar_candidate` plutôt qu'en article long.

Tests unitaires :

```bash
python3 tests/test_source_radar.py -v
```
