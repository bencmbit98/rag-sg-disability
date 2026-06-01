from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # LLM
    groq_api_key: str
    groq_model: str = "llama-3.1-8b-instant"

    # Embeddings
    embedding_model: str = "all-MiniLM-L6-v2"

    # Vector DB
    chroma_persist_dir: str = "./data/chroma_db"
    chroma_collection: str = "sg_disability_support"

    # Ingestion
    chunk_size: int = 512
    chunk_overlap: int = 64
    top_k: int = 5
    max_distance: float = 0.65

    # Guardrails
    out_of_scope_sentinel: str = "[OUT_OF_SCOPE]"

    # App
    app_env: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]


settings = Settings()

CRAWL_SOURCES = [
    {
        "label": "tp_sen",
        "seed_url": "https://www.tp.edu.sg/life-at-tp/special-educational-needs-sen-support.html",
        "allowed_prefix": "https://www.tp.edu.sg/life-at-tp/",
        "max_depth": 2,
        "max_pages": 20,
    },
    {
        "label": "enabling_transport",
        "seed_url": "https://www.enablingguide.sg/im-looking-for-disability-support/transport",
        "allowed_prefix": "https://www.enablingguide.sg/im-looking-for-disability-support/",
        "max_depth": 2,
        "max_pages": 30,
    },
    {
        "label": "enabling_care",
        "seed_url": "https://www.enablingguide.sg/im-looking-for-disability-support/child-adult-care",
        "allowed_prefix": "https://www.enablingguide.sg/im-looking-for-disability-support/",
        "max_depth": 2,
        "max_pages": 30,
    },
    {
        "label": "enabling_employment",
        "seed_url": "https://www.enablingguide.sg/im-looking-for-disability-support/training-employment",
        "allowed_prefix": "https://www.enablingguide.sg/im-looking-for-disability-support/",
        "max_depth": 2,
        "max_pages": 30,
    },
]
