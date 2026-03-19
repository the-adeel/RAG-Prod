import cohere
from dotenv import load_dotenv
import os

load_dotenv()

def rerank(query: str, search_results: list[str], top_k: int = 5) -> list[str]:
    co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

    response = co.rerank(
        model="rerank-v4.0-pro", query=query, documents=search_results, top_n=top_k
    )

    reranked = [result.index for result in response.results]
    print(f"Reranked Results from function : {reranked}")
    return [search_results[i] for i in reranked]