# main.py
from dotenv import load_dotenv
load_dotenv()

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
        if text.strip():
            chunks = chunk(text)
            all_chunks.extend(chunks)

    all_chunks = [c for c in all_chunks if c.strip()]

    print("📦 Storing in vector DB...")
    if all_chunks:
        store_chunks(all_chunks)
    else:
        print("⚠️ No content scraped, skipping vector DB storage.")

    print("🧠 Retrieving relevant chunks...")
    docs = retrieve(query)

    print("🤖 Generating answer...\n")
    answer = generate_answer(query, docs)

    print(answer)


if __name__ == "__main__":
    run("tell me some backend engineer jobs in banglore")