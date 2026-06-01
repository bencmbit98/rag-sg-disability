import logging

from fastapi import APIRouter, HTTPException, Request

from app.api.schemas import QueryRequest, QueryResponse, SourceInfo
from app.config import CRAWL_SOURCES, settings
from app.llm.groq_client import generate_answer
from app.retrieval.vector_store import retrieve

logger = logging.getLogger(__name__)

router = APIRouter()

_OUT_OF_SCOPE_MESSAGE = """\
I can only answer questions about:
• SEN (Special Educational Needs) support at Temasek Polytechnic
• Disability transport schemes in Singapore
• Child and adult care services for persons with disabilities
• Training and employment support for persons with disabilities

Your question appears to be outside these topics. For other enquiries:
• SG Enable: https://www.sg-enable.org.sg
• Ministry of Social and Family Development: https://www.msf.gov.sg
• TP Student Services: https://www.tp.edu.sg/student-services"""


@router.post("/query", response_model=QueryResponse)
async def query(request: Request, body: QueryRequest):
    state = request.app.state

    if getattr(state, "embedding_model", None) is None or getattr(state, "chroma_collection", None) is None:
        raise HTTPException(status_code=503, detail="Backend not fully initialised")

    # Layer 1 — retrieval gate
    retrieval = await retrieve(body.message, state.embedding_model, state.chroma_collection)

    pages_searched = len({c.source_url for c in retrieval.chunks})

    if not retrieval.in_scope:
        return QueryResponse(
            answer=_OUT_OF_SCOPE_MESSAGE,
            sources=[],
            is_in_scope=False,
            top_similarity_score=retrieval.top_distance,
            refusal_reason="low_similarity",
            pages_searched=pages_searched,
        )

    # Layer 2 — strict system prompt + Layer 3 — sentinel check
    history = [{"role": m.role, "content": m.content} for m in body.history]
    answer = await generate_answer(body.message, retrieval.chunks, history, state.groq_client)

    if settings.out_of_scope_sentinel in answer:
        return QueryResponse(
            answer=_OUT_OF_SCOPE_MESSAGE,
            sources=[],
            is_in_scope=False,
            top_similarity_score=retrieval.top_distance,
            refusal_reason="llm_refusal",
            pages_searched=pages_searched,
        )

    # Deduplicate sources by URL
    seen: set[str] = set()
    sources: list[SourceInfo] = []
    for chunk in retrieval.chunks:
        if chunk.source_url not in seen:
            seen.add(chunk.source_url)
            sources.append(SourceInfo(
                label=chunk.source_label,
                url=chunk.source_url,
                title=chunk.page_title,
                snippet=chunk.text[:200] + "…" if len(chunk.text) > 200 else chunk.text,
            ))

    return QueryResponse(
        answer=answer,
        sources=sources,
        is_in_scope=True,
        top_similarity_score=retrieval.top_distance,
        refusal_reason=None,
        pages_searched=pages_searched,
    )


@router.get("/sources")
async def sources():
    return [{"label": s["label"], "seed_url": s["seed_url"]} for s in CRAWL_SOURCES]
