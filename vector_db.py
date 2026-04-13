from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma(persist_directory="./db", embedding_function=embedding)

def store_chunks(chunks):
    db.add_texts(chunks)

def retrieve(query):
    return db.similarity_search(query, k=3)

def chunk(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]