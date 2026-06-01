import asyncio
import logging

from app.config import settings
from app.retrieval.vector_store import RetrievedChunk

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """\
You are a helpful assistant for persons with disabilities, \
students with special educational needs, and caregivers in Singapore.

You MUST answer using ONLY the information in the CONTEXT section below.
Do not use any outside knowledge. Do not make up information.

If the CONTEXT does not contain enough information to answer the question, \
you MUST respond with exactly this text and nothing else:
[OUT_OF_SCOPE]

Keep answers clear, warm, and jargon-free.
Cite the source name at the end of your answer.

CONTEXT:
{context}"""


def _build_context(chunks: list[RetrievedChunk]) -> str:
    parts = [
        f"[Source: {c.source_label} | {c.page_title}]\n{c.text}"
        for c in chunks
    ]
    return "\n\n---\n\n".join(parts)


async def generate_answer(
    query: str,
    chunks: list[RetrievedChunk],
    history: list[dict],
    groq_client,
) -> str:
    context = _build_context(chunks)
    system = _SYSTEM_PROMPT.format(context=context)

    messages = [{"role": "system", "content": system}]
    messages.extend(history[-6:])  # last 3 exchanges
    messages.append({"role": "user", "content": query})

    response = await asyncio.to_thread(
        groq_client.chat.completions.create,
        model=settings.groq_model,
        messages=messages,
        temperature=0.1,
        max_tokens=1024,
    )

    return response.choices[0].message.content
