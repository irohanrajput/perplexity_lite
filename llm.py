# llm.py
import os
from langchain_groq import ChatGroq

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-120b"
)

def generate_answer(query, docs):
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
    Answer the question using the context below.
    Also cite sources if possible.

    Context:
    {context}

    Question:
    {query}
    """

    res = llm.invoke(prompt)
    return res.content