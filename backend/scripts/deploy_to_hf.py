#!/usr/bin/env python3
"""Upload backend to HuggingFace Spaces with SSL bypass for TP network."""
import ssl
import sys
from pathlib import Path

# Must patch BEFORE importing huggingface_hub
ssl._create_default_https_context = ssl._create_unverified_context

import httpx
_orig_client = httpx.Client.__init__
def _patch_client(self, *args, **kwargs):
    kwargs.setdefault("verify", False)
    _orig_client(self, *args, **kwargs)
httpx.Client.__init__ = _patch_client

_orig_async = httpx.AsyncClient.__init__
def _patch_async(self, *args, **kwargs):
    kwargs.setdefault("verify", False)
    _orig_async(self, *args, **kwargs)
httpx.AsyncClient.__init__ = _patch_async

from huggingface_hub import HfApi, login  # noqa: E402

token = input("Paste your HuggingFace WRITE token: ").strip()
repo_id = input("Enter your Space repo ID (e.g. bencmbit98/rag-sg-disability): ").strip()

login(token=token, add_to_git_credential=False)
print("Logged in.")

api = HfApi()
backend_dir = Path(__file__).parent.parent

print(f"Uploading {backend_dir} to {repo_id} ...")
api.upload_folder(
    folder_path=str(backend_dir),
    repo_id=repo_id,
    repo_type="space",
    ignore_patterns=[
        ".venv/**",
        "**/__pycache__/**",
        "**/*.pyc",
        ".env",
        "data/raw/enabling_transport/**",
        "data/raw/enabling_care/**",
        "data/raw/enabling_employment/**",
        "data/chroma_db/**",
        "*.log",
    ],
)
print("Upload complete! HuggingFace will now build your Docker image.")
print(f"Monitor build progress at: https://huggingface.co/spaces/{repo_id}")
