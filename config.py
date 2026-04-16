from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset_2026"
MODELS = ["llama3.2:3b"] #, "llama3.1:8b", "gemma2:2b", "gemma2:9b", "mistral-nemo:12b", "mistral-small:22b"]