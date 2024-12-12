import chromadb
import os
from dotenv import load_dotenv
from jsonschema.exceptions import relevance

from file_parser import get_embedding

load_dotenv()
chroma_host = os.getenv("CHROMA_HOST") or "localhost"
chroma_port = int(os.getenv("CHROMA_PORT") or "8000")
chroma_collection_name = os.getenv("CHROMA_COLLECTION_NAME") or "test"

chroma_client = chromadb.HttpClient(
    host=chroma_host,
    port=chroma_port,
)

my_collection = chroma_client.get_or_create_collection(
    name=chroma_collection_name, metadata={"hnsw:space": "cosine"}
)


def retrieve_file(query_text: str, limit: int = 5):
    """ "将搜索文本转为向量搜素，返回最相关的前n个结果"""

    query_embedding = get_embedding(query_text)
    results = my_collection.query(
        query_embeddings=[query_embedding],
        n_results=limit,
    )
    count = len(results["ids"][0])
    file_list = []
    for i in range(count):
        relevance = 1 - results["distances"][0][i]
        if relevance > 0.5:
            file_list.append(
                {
                    "file_path": results["ids"][0][i],
                    "relevance": 1 - results["distances"][0][i],
                }
            )
    return file_list
