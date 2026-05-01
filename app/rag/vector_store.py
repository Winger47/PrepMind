import chromadb
from app.rag.embedder import get_embedding , get_embeddings

client=chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="interview_questions")


def add_questions(questions: list):
    ids = [q["id"] for q in questions]
    texts = [q["text"] for q in questions]
    metadatas = [q["metadata"] for q in questions]
    embeddings = get_embeddings(texts)
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search_similar_questions(query:str,n:int=5):
    query_embedding = get_embedding(query)
    results=collection.query(
        query_embeddings=[query_embedding],
        n_results=n 
    )

    return results