import os


AI_PROVIDER = os.getenv("CONORI_AI_PROVIDER", "demo")
OFFLINE_MODE = os.getenv("CONORI_OFFLINE_MODE", "true").lower() == "true"
MEMORY_PATH = os.getenv("CONORI_MEMORY_PATH", "data/conori_memory.sqlite3")
