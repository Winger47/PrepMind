from app.rag.embedder import get_embedding

text = "Design a distributed cache system"
vector = get_embedding(text)

print(f"Text: {text}")
print(f"Vector length: {len(vector)}")
print(f"First 5 numbers: {vector[:5]}")