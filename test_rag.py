from app.rag.vector_store import search_similar_questions

print("=== Test 1: Search 'design a caching system' ===")
results = search_similar_questions("design a caching system", n=3)
for i, doc in enumerate(results["documents"][0]):
    metadata = results["metadatas"][0][i]
    distance = results["distances"][0][i]
    print(f"\n{i+1}. {doc}")
    print(f"   Company: {metadata['company']} | Type: {metadata['type']} | Distance: {distance:.3f}")

print("\n\n=== Test 2: Search 'leadership and conflict resolution' ===")
results = search_similar_questions("leadership and conflict resolution", n=3)
for i, doc in enumerate(results["documents"][0]):
    metadata = results["metadatas"][0][i]
    print(f"\n{i+1}. {doc}")
    print(f"   Company: {metadata['company']} | Type: {metadata['type']}")

print("\n\n=== Test 3: Search 'Python concurrency' ===")
results = search_similar_questions("Python concurrency", n=3)
for i, doc in enumerate(results["documents"][0]):
    metadata = results["metadatas"][0][i]
    print(f"\n{i+1}. {doc}")
    print(f"   Topic: {metadata['topic']} | Difficulty: {metadata['difficulty']}")