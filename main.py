# main.py
from scraper import search, scrape
from vector_db import chunk, store_chunks, retrieve
from llm import generate_answer

def run(query):
    print("🔍 Searching...")
    urls = search(query)

    all_chunks = []

    for url in urls:
        print(f"Scraping: {url}")
        text = scrape(url)
        chunks = chunk(text)
        all_chunks.extend(chunks)

    print("📦 Storing in vector DB...")
    store_chunks(all_chunks)

    print("🧠 Retrieving relevant chunks...")
    docs = retrieve(query)

    print("🤖 Generating answer...\n")
    answer = generate_answer(query, docs)

    print(answer)


if __name__ == "__main__":
    run("What is LangGraph?")