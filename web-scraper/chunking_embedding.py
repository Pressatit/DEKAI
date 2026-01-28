import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import torch

# 1. Load the Markdown files you just scraped
loader = DirectoryLoader(
    './dedan kimathi db', 
    glob="**/*.md",  # The double asterisk searches subdirectories
    recursive=True, 
    loader_cls=TextLoader
)
docs = loader.load()
print("Docs loaded successfully!")

# 2. Chunk the data
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800, 
    chunk_overlap=150,
    separators=["\n## ", "\n# ", "\n", ". ", " "] # Prioritize Markdown headers
)
chunks = text_splitter.split_documents(docs)


# 3. Create Embeddings (using BGE-Small for speed & accuracy)
device = "mps" if torch.backends.mps.is_available() else "cpu"

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={'device': device}
)

# 4. Initialize and persist ChromaDB
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./dekai_vector_db"
)

print(f"✅ Created vector store with {len(chunks)} chunks.")

all_chunks = vector_db.get()

print(f"Sample Content: {all_chunks['documents'][0][:200]}...")
print(f"Metadata check: {all_chunks['metadatas'][0]}")