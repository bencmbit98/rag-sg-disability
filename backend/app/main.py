import asyncio
import logging
import os
import ssl
from contextlib import asynccontextmanager

# Bypass corporate SSL inspection in development
if os.getenv("APP_ENV", "development") == "development":
    ssl._create_default_https_context = ssl._create_unverified_context

    import urllib3
    import requests
    import httpx
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Patch requests (used by older huggingface_hub)
    _orig_request = requests.Session.request
    def _patched_request(self, *args, **kwargs):
        kwargs.setdefault("verify", False)
        return _orig_request(self, *args, **kwargs)
    requests.Session.request = _patched_request

    # Patch httpx (used by newer huggingface_hub and groq)
    _orig_client = httpx.Client.__init__
    def _patched_client(self, *args, **kwargs):
        kwargs.setdefault("verify", False)
        _orig_client(self, *args, **kwargs)
    httpx.Client.__init__ = _patched_client

    _orig_async_client = httpx.AsyncClient.__init__
    def _patched_async_client(self, *args, **kwargs):
        kwargs.setdefault("verify", False)
        _orig_async_client(self, *args, **kwargs)
    httpx.AsyncClient.__init__ = _patched_async_client

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

logger = logging.getLogger(__name__)


async def _load_embedding_model():
    from sentence_transformers import SentenceTransformer

    def _load_in_thread():
        # huggingface_hub 1.x needs an event loop in the thread (Python 3.12 doesn't create one automatically)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return SentenceTransformer(settings.embedding_model)
        finally:
            loop.close()
            asyncio.set_event_loop(None)

    return await asyncio.to_thread(_load_in_thread)


async def _init_chroma():
    import chromadb
    client = await asyncio.to_thread(
        chromadb.PersistentClient, path=settings.chroma_persist_dir
    )
    collection = await asyncio.to_thread(
        client.get_or_create_collection, name=settings.chroma_collection
    )
    return client, collection


async def _verify_groq():
    import httpx
    from groq import Groq
    client = Groq(api_key=settings.groq_api_key, http_client=httpx.Client(verify=False))
    await asyncio.to_thread(client.models.list)
    return client


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=settings.log_level)

    logger.info("Loading embedding model: %s", settings.embedding_model)
    try:
        app.state.embedding_model = await _load_embedding_model()
        logger.info("Embedding model loaded")
    except Exception as exc:
        logger.error("Failed to load embedding model: %s", exc)
        app.state.embedding_model = None

    logger.info("Initialising ChromaDB at %s", settings.chroma_persist_dir)
    try:
        app.state.chroma_client, app.state.chroma_collection = await _init_chroma()
        logger.info("ChromaDB ready")
    except Exception as exc:
        logger.error("Failed to init ChromaDB: %s", exc)
        app.state.chroma_client = None
        app.state.chroma_collection = None

    logger.info("Verifying Groq API key")
    try:
        app.state.groq_client = await _verify_groq()
        logger.info("Groq API key verified")
    except Exception as exc:
        logger.error("Groq verification failed: %s", exc)
        app.state.groq_client = None

    yield

    logger.info("Shutting down")


app = FastAPI(
    title="SG Disability RAG API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app.api.routes import router
app.include_router(router)


@app.get("/health")
async def health(request: Request):
    state = request.app.state
    chunk_count = 0
    chroma_status = "error"

    if getattr(state, "chroma_collection", None) is not None:
        try:
            chunk_count = await asyncio.to_thread(state.chroma_collection.count)
            chroma_status = "ok"
        except Exception:
            chroma_status = "error"

    return {
        "status": "ok",
        "llm": settings.groq_model,
        "embedding_model": settings.embedding_model,
        "embedding_loaded": getattr(state, "embedding_model", None) is not None,
        "chroma_status": chroma_status,
        "chunks_indexed": chunk_count,
        "groq_connected": getattr(state, "groq_client", None) is not None,
    }
