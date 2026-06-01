import asyncio
import logging
from dataclasses import dataclass

from app.config import settings

logger = logging.getLogger(__name__)


@dataclass
class RetrievedChunk:
    text: str
    source_label: str
    source_url: str
    seed_url: str
    page_title: str
    distance: float
    chunk_index: int


@dataclass
class RetrievalResult:
    chunks: list[RetrievedChunk]
    top_distance: float
    in_scope: bool


def is_in_scope(distances: list[float]) -> bool:
    return bool(distances) and min(distances) < settings.max_distance


async def retrieve(query: str, model, collection) -> RetrievalResult:
    embedding = await asyncio.to_thread(model.encode, query)

    results = await asyncio.to_thread(
        collection.query,
        query_embeddings=[embedding.tolist()],
        n_results=settings.top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    chunks = [
        RetrievedChunk(
            text=doc,
            source_label=meta.get("source_label", ""),
            source_url=meta.get("source_url", ""),
            seed_url=meta.get("seed_url", ""),
            page_title=meta.get("page_title", ""),
            distance=dist,
            chunk_index=int(meta.get("chunk_index", 0)),
        )
        for doc, meta, dist in zip(documents, metadatas, distances)
    ]

    top_distance = min(distances) if distances else 1.0
    logger.debug("Top distance: %.4f (threshold: %.2f)", top_distance, settings.max_distance)

    return RetrievalResult(
        chunks=chunks,
        top_distance=top_distance,
        in_scope=is_in_scope(distances),
    )
