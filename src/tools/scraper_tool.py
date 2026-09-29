import requests
from bs4 import BeautifulSoup


class WebScraperTool:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

    def fetch_and_clean(self, url: str, max_chars: int = 4000) -> str:
        """Fetches page content and extracts cleaned text."""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Remove irrelevant tags
            for script in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
                script.extract()
                
            text = soup.get_text(separator=" ", strip=True)
            return text[:max_chars]
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"
