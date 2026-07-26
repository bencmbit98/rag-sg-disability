#!/bin/bash

echo "=== Checking ChromaDB ==="

CHUNK_COUNT=$(python3 -c "
import chromadb
try:
    client = chromadb.PersistentClient(path='./data/chroma_db')
    col = client.get_or_create_collection('sg_disability_support')
    print(col.count())
except Exception:
    print(0)
" 2>/dev/null || echo 0)

echo "ChromaDB chunk count: ${CHUNK_COUNT:-0}"

# Compute hash of data files + ingestion code to detect content changes
DATA_HASH=$({ find /app/data -type f ! -path '/app/data/chroma_db/*'; \
              find /app/scripts/ingest.py /app/app/ingestion -type f; } 2>/dev/null \
    | sort | xargs md5sum 2>/dev/null | md5sum | cut -d' ' -f1)

STORED_HASH=""
if [ -f /app/data/chroma_db/.data_hash ]; then
    STORED_HASH=$(cat /app/data/chroma_db/.data_hash)
fi

echo "Data hash: ${DATA_HASH} (stored: ${STORED_HASH})"

if [ "${CHUNK_COUNT:-0}" -lt 100 ] || [ "$DATA_HASH" != "$STORED_HASH" ]; then
    echo "=== Running ingestion (new or changed data detected) ==="
    python3 scripts/ingest.py || echo "WARNING: Ingestion failed — starting with empty DB"
    echo "$DATA_HASH" > /app/data/chroma_db/.data_hash
    echo "=== Ingestion complete ==="
else
    echo "=== Skipping ingestion (${CHUNK_COUNT} chunks, data unchanged) ==="
fi

echo "=== Starting FastAPI ==="
exec uvicorn app.main:app --host 0.0.0.0 --port 7860 --workers 1
