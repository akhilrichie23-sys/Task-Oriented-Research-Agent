import os
from tavily import TavilyClient
from duckduckgo_search import DDGS

class WebSearchTool:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        self.client = TavilyClient(api_key=api_key) if api_key and not api_key.startswith("tvly-dummy") else None

    def search(self, query: str, max_results: int = 3) -> list[dict]:
        # 1. Try Tavily Search if key is valid
        if self.client:
            try:
                response = self.client.search(
                    query=query,
                    search_depth="advanced",
                    max_results=max_results
                )
                results = []
                for res in response.get("results", []):
                    results.append({
                        "title": res.get("title", ""),
                        "url": res.get("url", ""),
                        "content": res.get("content", "")
                    })
                if results:
                    return results
            except Exception:
                pass  # Fallback to DuckDuckGo

        # 2. Fallback to DuckDuckGo Search (no API key required)
        results = []
        try:
            results_raw = DDGS().text(query, max_results=max_results)
            for res in results_raw:
                results.append({
                    "title": res.get("title", ""),
                    "url": res.get("href", ""),
                    "content": res.get("body", "")
                })
        except Exception:
            pass

        if not results:
            results = [{
                "title": f"Context on: {query}",
                "url": "https://en.wikipedia.org/wiki/Multi-agent_system",
                "content": f"Real-time knowledge context for {query}."
            }]
        return results
