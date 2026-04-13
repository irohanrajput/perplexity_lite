# llm.py
from langchain_groq import ChatGroq

llm = ChatGroq(
    api_key="YOUR_GROQ_KEY",
    model_name="llama3-70b-8192"
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