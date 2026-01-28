
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load Chroma DB once
chroma_db = Chroma(
    persist_directory="../web-scraper/dekai_vector_db",  
    embedding_function=embedding_model
)
print("Loading Chroma from:", os.path.abspath("./vDekai/web-scraper/dekai_vector_db"))
print("Docs in Chroma:", chroma_db._collection.count())