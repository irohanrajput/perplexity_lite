import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS


def search(query):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append(r["href"])
    return results

def scrape(url):
    try:
        html = requests.get(url, timeout=5).text
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()
    except:
        return ""