from app.scraper import RecursiveScraper

if __name__ == "__main__":
    url = "https://www.samsung.com/in/smartphones/galaxy-s26-ultra/?page=home&msockid=201e750719e268b5322364e5181569b8"
    scraper = RecursiveScraper(url, max_depth=1, max_pages=5)
    results = scraper.scrape()

    print("Total pages scraped:", len(results))

    for page in results:
        print("=" * 80)
        print("URL:", page["url"])
        print("Content length:", len(page["content"]))
        print(page["content"][:300])