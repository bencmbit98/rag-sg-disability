#!/bin/bash
set -e

echo "=== Checking ChromaDB ==="
python - <<'EOF'
import chromadb
client = chromadb.PersistentClient(path="./data/chroma_db")
col = client.get_or_create_collection("sg_disability_support")
count = col.count()
print(f"ChromaDB has {count} chunks")
if count == 0:
    print("Running ingestion (first start — this takes ~15 minutes)...")
    import subprocess
    result = subprocess.run(["python", "scripts/ingest.py"], check=True)
    print("Ingestion complete.")
else:
    print("ChromaDB already populated — skipping ingestion.")
EOF

echo "=== Starting FastAPI ==="
exec uvicorn app.main:app --host 0.0.0.0 --port 7860 --workers 1
