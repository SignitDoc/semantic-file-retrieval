import chromadb
from dotenv import load_dotenv
from core.llm_processor import get_embedding
import os

load_dotenv()

chroma_client = chromadb.PersistentClient(path=".chromadb")

my_collection = chroma_client.get_or_create_collection(
    name="local", metadata={"hnsw:space": "cosine"}
)

UPLOAD_DIR = "uploaded_files"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


def retrieve_file(query_text: str, limit: int = 3):
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
                    "file_name": results["ids"][0][i],
                    "relevance": 1 - results["distances"][0][i],
                }
            )
    return file_list
