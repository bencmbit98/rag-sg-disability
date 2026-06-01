import logging
from typing import Optional

import chromadb
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.ingestion.chunker import Chunk

logger = logging.getLogger(__name__)

BATCH_SIZE = 64


def embed_and_store(chunks: list[Chunk], model: Optional[SentenceTransformer] = None) -> int:
    if model is None:
        model = SentenceTransformer(settings.embedding_model)

    client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
    collection = client.get_or_create_collection(name=settings.chroma_collection)

    total = 0
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        texts = [c.text for c in batch]
        ids = [c.id for c in batch]
        metadatas = [
            {
                "source_label": c.source_label,
                "source_url": c.source_url,
                "seed_url": c.seed_url,
                "page_title": c.page_title,
                "crawl_depth": c.crawl_depth,
                "chunk_index": c.chunk_index,
                "char_count": c.char_count,
                "fetched_at": c.fetched_at,
            }
            for c in batch
        ]
        embeddings = model.encode(texts, batch_size=32, show_progress_bar=False).tolist()
        collection.upsert(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
        total += len(batch)
        logger.info("Upserted %d / %d chunks", total, len(chunks))

    return total
