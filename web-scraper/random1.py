# Peek at the first 2 chunks to see if the text is clean
all_chunks = dekai_vector_db.get()

print(f"Sample Content: {all_chunks['documents'][0][:200]}...")
print(f"Metadata check: {all_chunks['metadatas'][0]}")