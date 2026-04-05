# 📂 RagApp — File Structure

```
RagApp/
├── .git/                          # Git version control
├── .gitignore                     # Git ignore rules
│
└── backend/                       # Backend application (FastAPI + Tortoise ORM)
    ├── .env                       # Environment variables (DB credentials, API keys)
    ├── main.py                    # Application entry point & API route definitions
    ├── tortoise_config.py         # Tortoise ORM & database configuration
    ├── pyproject.toml             # Python project metadata & dependencies
    │
    ├── functions/                 # Core RAG & LLM logic
    │   ├── LLM.py                 # LLM integration & prompt handling
    │   ├── rag_langchain.py       # RAG pipeline using LangChain
    │   ├── rag_langchain_customchunker.py  # RAG with custom document chunking
    │   ├── rag_manual.py          # Manual RAG implementation (without LangChain)
    │   └── rerank.py              # Result re-ranking logic
    │
    ├── helpers/                   # Utility & lifecycle helpers
    │   └── lifespan.py            # App startup/shutdown lifecycle events
    │
    ├── models/                    # Database models
    │   └── doc.py                 # Document model (Tortoise ORM)
    │
    ├── migrations/                # Database migrations (Aerich)
    │   └── models/
    │       └── 0_20260319172720_init.py  # Initial migration
    │
    ├── uploads/                   # Uploaded document storage
    │   └── MuhammadAdeelMughal.pdf       # Example uploaded PDF
    │
    └── venv/                      # Python virtual environment
```
