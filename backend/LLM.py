from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(query, context):

    context_text = "\n".join(context)

    prompt = f"""
    Use the context below to answer the question.

    Context:
    {context_text}

    Question:
    {query}
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content