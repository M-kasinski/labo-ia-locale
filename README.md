# Labo IA Locale

Média tech francophone sur l'**IA locale et open-source** : faire tourner des LLM chez soi, self-hosting, quantization, runtimes, GPU grand public & Apple Silicon, modèles open-weight, fine-tuning, RAG local, agents.

🌐 **En ligne :** https://labo-ia-locale.vercel.app

## Stack

- [Astro 5](https://astro.build) — site statique, content collections (Markdown)
- Déploiement **Vercel** (auto-deploy à chaque push sur `main`)
- Images Open Graph générées au build (`scripts/generate-og-images.mjs`, via `sharp`)

## Développement

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # génère les images OG puis build dans dist/
npm run preview
```

## Structure

```
src/
  content/blog/      # articles (Markdown + frontmatter)
  components/        # Header, Footer, BaseHead, ...
  layouts/           # BlogPost
  pages/             # index, blog, about, rss
  styles/global.css  # design system
scripts/
  generate-og-images.mjs   # images OG par article (build-time)
public/og/           # images OG générées
```

## Ligne éditoriale

Vérifié, sourcé, sans bullshit. Chaque article cite ses **sources primaires** (docs officielles, dépôts, Hugging Face) ; les chiffres (tailles, licences, versions, benchmarks) sont recoupés avant publication.
