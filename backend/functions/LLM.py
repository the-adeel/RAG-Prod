from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(query: str, context: list):
    if not context:
        prompt = f"""
You are a helpful AI assistant.
Answer the following question clearly and naturally.

Question: {query}
"""
    else:
        context_text = "\n\n".join([f"Source: {c.get('document', 'Unknown')}\n{c['content']}" for c in context])
        
        prompt = f"""
Use the context below to answer the question.
If the context doesn't contain the answer, say so — don't make things up.

Context:
{context_text}

Question:
{query}

At the end, list the sources you used.
"""
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt.strip()}]
    )

    return completion.choices[0].message.content