FROM python:3.12-slim

# System dependencies required by Playwright Chromium
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium with its system deps
RUN playwright install --with-deps chromium

# Copy application code
COPY . .
RUN mkdir -p data/raw data/chroma_db
RUN chmod +x start.sh

# HuggingFace Spaces requires port 7860
EXPOSE 7860

# start.sh runs ingestion on first startup, then launches uvicorn
CMD ["bash", "start.sh"]
