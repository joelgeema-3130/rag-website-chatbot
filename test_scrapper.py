from app.scraper import RecursiveScraper

if __name__ == "__main__":
    url = "https://docs.python.org/3/"
    scraper = RecursiveScraper(url, max_depth=1, max_pages=5)
    results = scraper.scrape()

    print("Total pages scraped:", len(results))

    for page in results:
        print("=" * 80)
        print("URL:", page["url"])
        print("Content length:", len(page["content"]))
        print(page["content"][:300])