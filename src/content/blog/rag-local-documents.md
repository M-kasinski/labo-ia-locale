---
title: "RAG local : faire parler tes documents avec un LLM hors-ligne"
description: "Comprendre et monter un RAG local pour interroger ses fichiers avec un LLM, sans API et sans fuite de données."
pubDate: 2026-05-29
tags: ["ia-locale", "rag", "embeddings", "ollama"]
author: "Labo IA Locale"
draft: false
sources:
  - { label: "Ollama nomic-embed-text", url: "https://ollama.com/library/nomic-embed-text" }
  - { label: "LlamaIndex VectorStoreIndex", url: "https://docs.llamaindex.ai/en/stable/module_guides/indexing/vector_store_index/" }
  - { label: "LangChain RAG tutorial", url: "https://python.langchain.com/docs/tutorials/rag/" }
  - { label: "Chroma introduction", url: "https://docs.trychroma.com/docs/overview/introduction" }
  - { label: "Sentence Transformers STS", url: "https://www.sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html" }
  - { label: "BGE small en v1.5", url: "https://huggingface.co/BAAI/bge-small-en-v1.5" }
  - { label: "E5 small v2", url: "https://huggingface.co/intfloat/e5-small-v2" }
  - { label: "FAISS", url: "https://github.com/facebookresearch/faiss" }
  - { label: "Qdrant", url: "https://github.com/qdrant/qdrant" }
  - { label: "LanceDB", url: "https://github.com/lancedb/lancedb" }
---

Tu as déjà un LLM local. Bien. Le problème n’est pas de lui apprendre “toute ta base de docs” par magie. Le problème, c’est de lui donner le bon passage au bon moment. C’est exactement ce que fait le RAG, Retrieval-Augmented Generation.

L’idée est simple : au lieu de fine-tuner le modèle sur tes fichiers, tu indexes tes documents, puis tu récupères les extraits pertinents au moment de la question. Le modèle répond avec ce contexte injecté dans le prompt. On ne modifie pas les poids du LLM. On lui tend juste les bonnes cartes.

## Pourquoi RAG plutôt que fine-tuning

Le fine-tuning sert à changer le comportement ou le style d’un modèle. Le RAG sert à lui donner de la mémoire externe. Pour des notes perso, des PDF, des procédures internes ou une doc technique qui change souvent, le RAG est plus pratique. Tu mets à jour l’index quand les documents bougent. Pas besoin de réentraîner à chaque fois.

Il y a aussi un avantage très concret : tout peut rester local. Ollama indique explicitement qu’un modèle comme `nomic-embed-text` peut tourner en local et qu’il “can only be used to generate embeddings”, avec un prérequis Ollama 0.1.26 ou plus. Ollama rappelle aussi que ses modèles peuvent tourner entièrement hors ligne et que tes données restent à toi [source](https://ollama.com/library/nomic-embed-text) [source](https://ollama.com).

## Le pipeline, étape par étape

### 1) Ingestion et découpage en chunks

Tu commences par lire tes sources : Markdown, texte, PDF, pages exportées, ce que tu veux. Ensuite tu découpes en chunks. Pourquoi ? Parce qu’un document entier est trop gros, trop bruité, et trop pauvre à rechercher en bloc.

LlamaIndex dit clairement que `VectorStoreIndex` construit un index à partir de `Node` objects et que `from_documents` découpe les documents en chunks avant de les transformer en nodes. LangChain, dans son tutoriel RAG, montre la même logique : ingestion, chunking, puis indexation séparée du runtime de génération [source](https://docs.llamaindex.ai/en/stable/module_guides/indexing/vector_store_index/) [source](https://python.langchain.com/docs/tutorials/rag/).

En pratique, vise des chunks assez petits pour être précis, mais pas ridiculement courts. Le bon réglage dépend de la densité de l’information. Un manuel d’API et un roman ne se découpent pas pareil. Évidemment.

### 2) Embeddings locaux

Chaque chunk est transformé en vecteur numérique. C’est le rôle des embeddings : représenter le sens d’un texte dans un espace où deux passages proches s’alignent.

Sentence Transformers résume bien le principe : on encode les textes en embeddings, puis on compare les embeddings pour mesurer leur similarité. Les docs montrent `SentenceTransformer.encode()` et les fonctions de similarité associées [source](https://www.sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html).

Pour des modèles concrets :
- `nomic-embed-text` via Ollama, qui sert uniquement à générer des embeddings [source](https://ollama.com/library/nomic-embed-text)
- `sentence-transformers/all-MiniLM-L6-v2`, utilisé dans la doc Sentence Transformers [source](https://www.sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html)
- `BAAI/bge-small-en-v1.5`, un modèle BGE dense pour la recherche sémantique [source](https://huggingface.co/BAAI/bge-small-en-v1.5)
- `intfloat/e5-small-v2`, un modèle d’embedding pour retrieval et similarité sémantique [source](https://huggingface.co/intfloat/e5-small-v2)

Tu peux les utiliser localement, une fois les poids téléchargés.

### 3) Stockage dans une base vectorielle locale

Ensuite tu stockes les vecteurs dans une base vectorielle. Le but : retrouver vite les chunks proches d’une requête.

Chroma indique qu’il permet de stocker des embeddings avec métadonnées, de faire de la recherche dense, sparse ou hybride, et qu’il peut tourner localement ou en self-host [source](https://docs.trychroma.com/docs/overview/introduction).

Les autres options citées par les docs et les repos officiels sont :
- FAISS, une bibliothèque pour la recherche de similarité et le clustering de vecteurs denses [source](https://github.com/facebookresearch/faiss)
- Qdrant, une base vectorielle et moteur de recherche de similarité pour points avec payload [source](https://github.com/qdrant/qdrant)
- LanceDB, une bibliothèque de retrieval embarquée open source pour l’IA multimodale [source](https://github.com/lancedb/lancedb)

Le choix dépend de ton besoin. Si tu veux simple et local, Chroma ou FAISS font le travail. Si tu veux plus de filtrage, de payload ou une vraie base serveur, Qdrant devient vite intéressant.

### 4) Requête, récupération et génération

Quand l’utilisateur pose une question, tu fais la même chose que pour les chunks : tu l’embarques en embedding. Puis tu cherches les k voisins les plus proches dans la base. Enfin, tu passes ces passages au LLM local dans le prompt, avec une consigne du genre : “réponds uniquement à partir du contexte fourni”.

Le tutoriel LangChain le décrit clairement : la boucle runtime fait requête → retrieval → génération [source](https://python.langchain.com/docs/tutorials/rag/).

Le point important, c’est qu’on ne demande pas au modèle d’inventer la réponse à partir de rien. On lui donne le morceau de texte qui compte. C’est ça, la différence entre une démo qui hallucine élégamment et un outil vraiment utile.

## Mini flux concret

```bash
# 1) Modèle d'embedding local
ollama pull nomic-embed-text

# 2) Ton LLM local, par exemple via Ollama
ollama run <ton-modele-local>
```

```python
from sentence_transformers import SentenceTransformer
import chromadb

# 1. Charger les chunks de tes documents
chunks = [
    "Le VPN interne est requis pour accéder au dépôt.",
    "La procédure de backup s’exécute tous les soirs à 23h.",
]

# 2. Embeddings locaux
embedder = SentenceTransformer("intfloat/e5-small-v2")
chunk_vectors = embedder.encode([f"passage: {c}" for c in chunks], normalize_embeddings=True)

# 3. Stockage local
client = chromadb.PersistentClient(path="./chroma-db")
col = client.get_or_create_collection("docs")
for i, chunk in enumerate(chunks):
    col.add(ids=[str(i)], documents=[chunk], embeddings=[chunk_vectors[i].tolist()])

# 4. Requête
question = "Quand se lance le backup ?"
q_vec = embedder.encode([f"query: {question}"], normalize_embeddings=True)[0].tolist()
result = col.query(query_embeddings=[q_vec], n_results=2)
context = "\n\n".join(result["documents"][0])

prompt = f"Réponds en français à partir du contexte ci-dessous.\n\nContexte:\n{context}\n\nQuestion: {question}"
print(prompt)
```

Ce code est volontairement simple. En vrai, tu ajoutes le découpage en chunks, les métadonnées, le nettoyage des PDF, et une vraie fonction d’appel au LLM local. Mais le flux est celui-là, et pas un autre.

## Ce qu’il faut garder en tête

Le RAG ne rend pas ton modèle “savant”. Il le rend mieux branché sur tes données. Si le chunking est mauvais, si l’embedding est faible, ou si la recherche ramène les mauvais passages, la réponse sera mauvaise aussi. Le système est aussi bon que sa chaîne d’ingestion et de retrieval.

Et le tout-local n’est pas qu’un argument de vente. C’est une contrainte utile : confidentialité, pas d’API, pas de fuite de documents, pas de surprise sur la facturation. Pour des notes perso, des fichiers clients, ou de la doc interne, c’est souvent la seule option raisonnable.

## En pratique

Si tu veux un point de départ propre, fais simple : Ollama pour le LLM et les embeddings, Chroma pour l’index local, puis un petit pipeline Python qui chunk, embed, recherche et injecte le contexte. Quand ça marche sur 20 notes, tu l’étends à 2 000 docs. Pas avant. C’est rarement la partie glamour, mais c’est celle qui évite de construire une jolie machine à se tromper vite.
