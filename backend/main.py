from fastapi import FastAPI, UploadFile, File
# from rag_manual import retrieve
from functions.rag_langchain import retrieve
from functions.LLM import generate_answer
from dotenv import load_dotenv
from functions.rag_langchain import add_file_to_vectorstore
from helpers.lifespan import lifespan
import shutil
import os

load_dotenv()
app = FastAPI(lifespan=lifespan)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/ask")
def ask(query: str):

    context = retrieve(query)
    if not context:
        answer = generate_answer(query, context=[])

    else:
        answer = generate_answer(query, context)

    return {
        "query": query,
        "used_rag": bool(context),
        "context_snippets": context,
        "answer": answer
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Overwrite vector store with only this file
    result = add_file_to_vectorstore(file_path)

    return {"message": result}