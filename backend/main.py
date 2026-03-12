from fastapi import FastAPI
# from rag_manual import retrieve
from rag_langchain import retrieve
from LLM import generate_answer
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


@app.get("/ask")
def ask(query: str):

    context = retrieve(query)
    answer = generate_answer(query, context)

    return {
        "query": query,
        "context": context,
        "answer": answer
    }