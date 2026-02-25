import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time


class RecursiveScraper:
    def __init__(self, base_url, max_depth=2, max_pages=20):
        self.base_url = base_url
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.visited = set()
        self.domain = urlparse(base_url).netloc
        self.results = []

    def scrape(self):
        self._crawl(self.base_url, depth=0)
        return self.results

    def _crawl(self, url, depth):
        url = url.split("#")[0]
        if depth > self.max_depth:
            return

        if url in self.visited:
            return

        if len(self.visited) >= self.max_pages:
            return

        parsed = urlparse(url)
        if parsed.netloc != self.domain:
            return

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = response.apparent_encoding
            if response.status_code != 200:
                return
        except:
            return

        self.visited.add(url)

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text_content = self._extract_text(soup)

        if text_content.strip():
            self.results.append({
                "url": url,
                "content": text_content
            })

        # Find links for recursion
        links = soup.find_all("a", href=True)
        for link in links:
            next_url = urljoin(url, link["href"])
            self._crawl(next_url, depth + 1)

        time.sleep(0.5)  # polite crawling

    def _extract_text(self, soup):
        texts = []

        # Headings
        for tag in soup.find_all(["h1", "h2", "h3"]):
            texts.append(f"\n{tag.get_text(strip=True)}\n")

        # Paragraphs
        for p in soup.find_all("p"):
            texts.append(p.get_text(strip=True))

        # Tables
        for table in soup.find_all("table"):
            for row in table.find_all("tr"):
                cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
                if cells:
                    texts.append(" | ".join(cells))

        return "\n".join(texts)