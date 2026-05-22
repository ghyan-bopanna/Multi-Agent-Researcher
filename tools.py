from langchain.tools import tool
import requests #web scraping
from bs4 import BeautifulSoup # scrape
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print # for pretty print

load_dotenv() # Load your environment variables

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
# Let's make tools now

@tool # We'll use LangChain's tool decorator to make the tool
def web_search(query: str) -> str:
    """Search the web for reliable information on a topic. Return Titles, URLs, and snippets."""
    results = tavily.search(query=query, max_results=2) # MAX RESULTS

    out = []
    
    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    return "\n-------\n".join(out)

#test
#print(web_search.invoke("Elephant attacks in India"))

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})  # Disguise as Mozilla user in header
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()  # Remove useless tags
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"

#test
#print(scrape_url.invoke("https://www.kodaguexpress.com/post/kodava-hockey-for-every-goal-at-chenanda-hockey-festival-2026-a-sapling-will-be-planted"))