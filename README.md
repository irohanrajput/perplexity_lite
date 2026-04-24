# perplexity_lite

A minimal, readable RAG pipeline — a stripped-down reference for how Perplexity-style web answer engines actually work end-to-end. Four Python files, one vector DB on disk, one LLM call at the end.

## What it does

Given a user query, it:

1. Runs a **DuckDuckGo** search and grabs the top 5 URLs.
2. **Scrapes** each page with `requests` + `BeautifulSoup`, pulling plain text.
3. **Chunks** the text into 500-char slices.
4. **Embeds** the chunks with `sentence-transformers/all-MiniLM-L6-v2` and persists them in a local **Chroma** vector DB (`./db`).
5. Retrieves the **top-3 most relevant chunks** for the query.
6. Sends them as context to a **Groq-hosted LLM** (`openai/gpt-oss-120b`) and prints the grounded answer.

That's the whole loop. The goal isn't performance or production readiness — it's showing the moving parts of retrieval-augmented generation without frameworks hiding the plumbing.

## Architecture

```
  query
    │
    ▼
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ DDG srch │ ──▶ │ scrape   │ ──▶ │ chunk +  │ ──▶ │  Chroma  │
│ (ddgs)   │     │ (bs4)    │     │ embed    │     │ (./db)   │
└──────────┘     └──────────┘     │ (MiniLM) │     └──────────┘
                                  └──────────┘           │
                                                         ▼
                                                   ┌──────────┐
                                                   │ retrieve │
                                                   │  top-k   │
                                                   └────┬─────┘
                                                        ▼
                                                   ┌──────────┐
                                                   │ Groq LLM │
                                                   │ (answer) │
                                                   └──────────┘
```

## Stack

- **Python 3.x**
- **LangChain** — orchestration glue (`langchain`, `langchain-chroma`, `langchain-huggingface`, `langchain-groq`)
- **Chroma** — local persistent vector store
- **sentence-transformers** (`all-MiniLM-L6-v2`) — embeddings
- **Groq** — hosted LLM inference (`openai/gpt-oss-120b`)
- **DuckDuckGo** search (`ddgs`)
- **BeautifulSoup + requests** — scraping

## Setup

Requires Python 3.10+ and a Groq API key.

```bash
git clone git@github.com:irohanrajput/perplexity_lite.git
cd perplexity_lite

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env`:

```bash
GROQ_API_KEY=your_key_here
```

Get one at https://console.groq.com.

## Run

Edit the query at the bottom of `main.py`:

```python
if __name__ == "__main__":
    run("your question here")
```

Then:

```bash
python main.py
```

You'll see the search → scrape → embed → retrieve → answer flow print as it goes, and the final grounded answer at the end.

## Files

| File | What it does |
| --- | --- |
| `main.py` | Orchestrates the pipeline end-to-end |
| `scraper.py` | `search(query)` via DuckDuckGo + `scrape(url)` via requests/bs4 |
| `vector_db.py` | Chunk, embed (MiniLM), store, and similarity-search in Chroma |
| `llm.py` | Builds the context prompt and calls the Groq LLM |
| `db/` | Chroma's persisted vector store (grows each run) |

## Notes / limitations

- Single-threaded, synchronous — scraping 5 URLs runs one at a time.
- No deduping; every run appends fresh chunks to the same Chroma collection.
- Chunk size is a naive 500 chars with no overlap; real systems do semantic/token-aware chunking.
- The DB persists between runs. Delete `./db` to start clean.
- No citation extraction beyond asking the LLM nicely in the prompt.

These are all conscious choices for the "lite" framing — the point was to fit a working RAG loop in ~50 lines of code.
