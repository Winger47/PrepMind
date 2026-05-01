from app.rag.vector_store import add_questions, collection


SAMPLE_QUESTIONS = [
    # ─── Google ───────────────────────────────────────────
    {"id": "google_dsa_1", "text": "Find the maximum value in a binary search tree", "metadata": {"company": "Google", "type": "DSA", "topic": "Binary Search Tree", "difficulty": "Medium"}},
    {"id": "google_dsa_2", "text": "Find the kth largest element in an unsorted array", "metadata": {"company": "Google", "type": "DSA", "topic": "Heaps", "difficulty": "Medium"}},
    {"id": "google_dsa_3", "text": "Implement a sliding window maximum algorithm", "metadata": {"company": "Google", "type": "DSA", "topic": "Arrays", "difficulty": "Hard"}},
    {"id": "google_dsa_4", "text": "Detect a cycle in a directed graph", "metadata": {"company": "Google", "type": "DSA", "topic": "Graphs", "difficulty": "Medium"}},
    {"id": "google_sd_1", "text": "Design a distributed cache system handling 1M requests per second", "metadata": {"company": "Google", "type": "System Design", "topic": "Caching", "difficulty": "Hard"}},
    {"id": "google_sd_2", "text": "Design Google Search autocomplete with 100M queries per day", "metadata": {"company": "Google", "type": "System Design", "topic": "Search", "difficulty": "Hard"}},
    {"id": "google_sd_3", "text": "Design a URL shortener like bit.ly with analytics", "metadata": {"company": "Google", "type": "System Design", "topic": "Web Services", "difficulty": "Medium"}},
    {"id": "google_beh_1", "text": "Tell me about a time you disagreed with your manager", "metadata": {"company": "Google", "type": "Behavioural", "topic": "Conflict", "difficulty": "Medium"}},

    # ─── Meta ─────────────────────────────────────────────
    {"id": "meta_dsa_1", "text": "Find the longest substring without repeating characters", "metadata": {"company": "Meta", "type": "DSA", "topic": "Strings", "difficulty": "Medium"}},
    {"id": "meta_dsa_2", "text": "Merge k sorted linked lists efficiently", "metadata": {"company": "Meta", "type": "DSA", "topic": "Linked Lists", "difficulty": "Hard"}},
    {"id": "meta_dsa_3", "text": "Find all paths from source to target in a DAG", "metadata": {"company": "Meta", "type": "DSA", "topic": "Graphs", "difficulty": "Medium"}},
    {"id": "meta_sd_1", "text": "Design Instagram feed system with infinite scroll", "metadata": {"company": "Meta", "type": "System Design", "topic": "Feed Systems", "difficulty": "Hard"}},
    {"id": "meta_sd_2", "text": "Design Facebook Messenger with 1B users supporting real-time chat", "metadata": {"company": "Meta", "type": "System Design", "topic": "Messaging", "difficulty": "Hard"}},
    {"id": "meta_sd_3", "text": "Design news feed ranking algorithm for personalization", "metadata": {"company": "Meta", "type": "System Design", "topic": "Ranking", "difficulty": "Hard"}},
    {"id": "meta_beh_1", "text": "Describe a time you took ownership of a difficult problem", "metadata": {"company": "Meta", "type": "Behavioural", "topic": "Ownership", "difficulty": "Medium"}},

    # ─── Amazon ───────────────────────────────────────────
    {"id": "amazon_dsa_1", "text": "Implement LRU cache with O(1) operations", "metadata": {"company": "Amazon", "type": "DSA", "topic": "Caching", "difficulty": "Medium"}},
    {"id": "amazon_dsa_2", "text": "Find the median of two sorted arrays in O(log(min(m,n)))", "metadata": {"company": "Amazon", "type": "DSA", "topic": "Binary Search", "difficulty": "Hard"}},
    {"id": "amazon_dsa_3", "text": "Serialize and deserialize a binary tree", "metadata": {"company": "Amazon", "type": "DSA", "topic": "Trees", "difficulty": "Hard"}},
    {"id": "amazon_sd_1", "text": "Design Amazon's product search and recommendation system", "metadata": {"company": "Amazon", "type": "System Design", "topic": "Search", "difficulty": "Hard"}},
    {"id": "amazon_sd_2", "text": "Design a distributed inventory management system across warehouses", "metadata": {"company": "Amazon", "type": "System Design", "topic": "Distributed Systems", "difficulty": "Hard"}},
    {"id": "amazon_sd_3", "text": "Design a rate limiter for an API gateway", "metadata": {"company": "Amazon", "type": "System Design", "topic": "Rate Limiting", "difficulty": "Medium"}},
    {"id": "amazon_beh_1", "text": "Tell me about a time you delivered a project under tight deadline", "metadata": {"company": "Amazon", "type": "Behavioural", "topic": "Leadership", "difficulty": "Medium"}},
    {"id": "amazon_beh_2", "text": "Describe a situation where you had to be customer obsessed", "metadata": {"company": "Amazon", "type": "Behavioural", "topic": "Customer Focus", "difficulty": "Easy"}},
    {"id": "amazon_beh_3", "text": "Tell me about a time you had to dive deep into a complex problem", "metadata": {"company": "Amazon", "type": "Behavioural", "topic": "Problem Solving", "difficulty": "Medium"}},

    # ─── Netflix ──────────────────────────────────────────
    {"id": "netflix_sd_1", "text": "Design Netflix video streaming architecture for 200M subscribers", "metadata": {"company": "Netflix", "type": "System Design", "topic": "Streaming", "difficulty": "Hard"}},
    {"id": "netflix_sd_2", "text": "Design a recommendation system based on user watch history", "metadata": {"company": "Netflix", "type": "System Design", "topic": "Recommendations", "difficulty": "Hard"}},
    {"id": "netflix_sd_3", "text": "Design a CDN to deliver video content globally with low latency", "metadata": {"company": "Netflix", "type": "System Design", "topic": "CDN", "difficulty": "Hard"}},

    # ─── Uber ─────────────────────────────────────────────
    {"id": "uber_sd_1", "text": "Design Uber's matching system between riders and drivers", "metadata": {"company": "Uber", "type": "System Design", "topic": "Matching", "difficulty": "Hard"}},
    {"id": "uber_sd_2", "text": "Design a real-time location tracking system for millions of drivers", "metadata": {"company": "Uber", "type": "System Design", "topic": "Geospatial", "difficulty": "Hard"}},
    {"id": "uber_sd_3", "text": "Design a surge pricing algorithm based on demand", "metadata": {"company": "Uber", "type": "System Design", "topic": "Pricing", "difficulty": "Hard"}},

    # ─── Microsoft ────────────────────────────────────────
    {"id": "microsoft_dsa_1", "text": "Reverse a linked list in groups of k nodes", "metadata": {"company": "Microsoft", "type": "DSA", "topic": "Linked Lists", "difficulty": "Hard"}},
    {"id": "microsoft_dsa_2", "text": "Find the lowest common ancestor in a binary tree", "metadata": {"company": "Microsoft", "type": "DSA", "topic": "Trees", "difficulty": "Medium"}},
    {"id": "microsoft_sd_1", "text": "Design Microsoft Teams chat with file sharing and video calls", "metadata": {"company": "Microsoft", "type": "System Design", "topic": "Collaboration", "difficulty": "Hard"}},
    {"id": "microsoft_beh_1", "text": "Describe a time you mentored someone on your team", "metadata": {"company": "Microsoft", "type": "Behavioural", "topic": "Mentorship", "difficulty": "Easy"}},

    # ─── Apple ────────────────────────────────────────────
    {"id": "apple_dsa_1", "text": "Find duplicates in an array using O(1) space", "metadata": {"company": "Apple", "type": "DSA", "topic": "Arrays", "difficulty": "Medium"}},
    {"id": "apple_sd_1", "text": "Design iCloud sync for photos across multiple devices", "metadata": {"company": "Apple", "type": "System Design", "topic": "Sync", "difficulty": "Hard"}},

    # ─── Indian Companies / Startups ──────────────────────
    {"id": "flipkart_sd_1", "text": "Design Flipkart's flash sale system handling 10M concurrent users", "metadata": {"company": "Flipkart", "type": "System Design", "topic": "Flash Sales", "difficulty": "Hard"}},
    {"id": "swiggy_sd_1", "text": "Design Swiggy's food delivery matching system", "metadata": {"company": "Swiggy", "type": "System Design", "topic": "Matching", "difficulty": "Hard"}},
    {"id": "razorpay_sd_1", "text": "Design a payment gateway with idempotency and retry handling", "metadata": {"company": "Razorpay", "type": "System Design", "topic": "Payments", "difficulty": "Hard"}},

    # ─── CS Fundamentals (Generic) ────────────────────────
    {"id": "cs_net_1", "text": "Explain the difference between TCP and UDP protocols", "metadata": {"company": "General", "type": "CS Fundamentals", "topic": "Networking", "difficulty": "Easy"}},
    {"id": "cs_net_2", "text": "Explain how HTTPS works including TLS handshake", "metadata": {"company": "General", "type": "CS Fundamentals", "topic": "Networking", "difficulty": "Medium"}},
    {"id": "cs_net_3", "text": "Explain DNS resolution process step by step", "metadata": {"company": "General", "type": "CS Fundamentals", "topic": "Networking", "difficulty": "Easy"}},
    {"id": "cs_db_1", "text": "Explain ACID properties in database transactions", "metadata": {"company": "General", "type": "CS Fundamentals", "topic": "Databases", "difficulty": "Medium"}},
    {"id": "cs_db_2", "text": "Explain the difference between SQL and NoSQL databases", "metadata": {"company": "General", "type": "CS Fundamentals", "topic": "Databases", "difficulty": "Easy"}},
    {"id": "cs_db_3", "text": "Explain database indexing and B-tree structure", "metadata": {"company": "General", "type": "CS Fundamentals", "topic": "Databases", "difficulty": "Medium"}},
    {"id": "cs_db_4", "text": "Explain CAP theorem with real world examples", "metadata": {"company": "General", "type": "CS Fundamentals", "topic": "Databases", "difficulty": "Hard"}},
    {"id": "cs_os_1", "text": "Describe how virtual memory works in operating systems", "metadata": {"company": "General", "type": "CS Fundamentals", "topic": "OS", "difficulty": "Medium"}},
    {"id": "cs_os_2", "text": "Explain the difference between process and thread", "metadata": {"company": "General", "type": "CS Fundamentals", "topic": "OS", "difficulty": "Easy"}},
    {"id": "cs_os_3", "text": "Explain deadlocks and how to prevent them", "metadata": {"company": "General", "type": "CS Fundamentals", "topic": "OS", "difficulty": "Medium"}},
    {"id": "cs_oop_1", "text": "Explain SOLID principles with examples", "metadata": {"company": "General", "type": "CS Fundamentals", "topic": "OOP", "difficulty": "Medium"}},
    {"id": "cs_oop_2", "text": "Explain the difference between composition and inheritance", "metadata": {"company": "General", "type": "CS Fundamentals", "topic": "OOP", "difficulty": "Easy"}},

    # ─── Language Specific ────────────────────────────────
    {"id": "lang_py_1", "text": "Explain the GIL in Python and its implications", "metadata": {"company": "General", "type": "Language Specific", "topic": "Python", "difficulty": "Medium"}},
    {"id": "lang_py_2", "text": "Explain async/await and how event loop works in Python", "metadata": {"company": "General", "type": "Language Specific", "topic": "Python", "difficulty": "Hard"}},
    {"id": "lang_py_3", "text": "Explain decorators and provide a real use case", "metadata": {"company": "General", "type": "Language Specific", "topic": "Python", "difficulty": "Medium"}},
    {"id": "lang_py_4", "text": "Explain Python's MRO (Method Resolution Order) for multiple inheritance", "metadata": {"company": "General", "type": "Language Specific", "topic": "Python", "difficulty": "Hard"}},
    {"id": "lang_js_1", "text": "Explain closures in JavaScript with practical examples", "metadata": {"company": "General", "type": "Language Specific", "topic": "JavaScript", "difficulty": "Medium"}},
    {"id": "lang_js_2", "text": "Explain how the JavaScript event loop and microtasks work", "metadata": {"company": "General", "type": "Language Specific", "topic": "JavaScript", "difficulty": "Hard"}},
    {"id": "lang_go_1", "text": "Explain goroutines and channels in Go", "metadata": {"company": "General", "type": "Language Specific", "topic": "Go", "difficulty": "Medium"}},
]


def seed_database():
    """Populate ChromaDB with initial questions if empty."""
    if collection.count() > 0:
        print(f"Bank already has {collection.count()} questions. Skipping seed.")
        return
    
    add_questions(SAMPLE_QUESTIONS)
    print(f"Seeded {len(SAMPLE_QUESTIONS)} questions into bank")
    print(f"Total questions in bank: {collection.count()}")


if __name__ == "__main__":
    seed_database()