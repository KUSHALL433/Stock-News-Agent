import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin
import csv

BASE_URL = "https://www.moneycontrol.com"

SECTIONS = {
    "business": "https://www.moneycontrol.com/news/business/",
    "economy": "https://www.moneycontrol.com/news/business/economy/",
    "companies": "https://www.moneycontrol.com/news/business/companies/",
    "ipo": "https://www.moneycontrol.com/news/business/ipo/",
    "startup": "https://www.moneycontrol.com/news/business/startup/",
    "stocks": "https://www.moneycontrol.com/news/business/stocks/",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

# === Step 1: Find Article Links ===
def get_article_links(section_url):
    """Extract article links from a section's first page."""
    print(f"\n[INFO] Scanning: {section_url}")
    try:
        res = requests.get(section_url, headers=HEADERS, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        links = set()
        for a in soup.find_all("a", href=True):
            href = urljoin(BASE_URL, a["href"])
            # Match only proper article URLs
            if "/news/business/" in href and href.endswith(".html"):
                links.add(href)

        print(f"[INFO] Found {len(links)} article links in {section_url}")
        return list(links)[:10]  # Limit to first 10 per section
    except Exception as e:
        print(f"[ERROR] Could not get links from {section_url}: {e}")
        return []


# === Step 2: Scrape Article Details ===
def scrape_article(link, section_name):
    """Extract title, date, and main text from one article."""
    try:
        res = requests.get(link, headers=HEADERS, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "No Title"

        date_tag = soup.find("span", class_="article_schedule")
        date = date_tag.get_text(strip=True) if date_tag else "Unknown Date"

        content_div = (
            soup.find("div", {"class": "article_content_desc"})
            or soup.find("div", {"class": "content_wrapper"})
        )
        content = ""
        if content_div:
            paragraphs = content_div.find_all("p")
            content = " ".join(p.get_text(strip=True) for p in paragraphs)

        return {
            "section": section_name,
            "url": link,
            "title": title,
            "date": date,
            "content": content,
        }
    except Exception as e:
        print(f"[ERROR] Failed to scrape {link}: {e}")
        return None


# === Step 3: Main Orchestration ===
def main():
    all_articles = []

    for section_name, section_url in SECTIONS.items():
        links = get_article_links(section_url)
        time.sleep(random.uniform(1.5, 3.0))

        for link in links:
            article_data = scrape_article(link, section_name)
            if article_data and article_data["content"]:
                all_articles.append(article_data)
            time.sleep(random.uniform(2.0, 4.0))

    # === Step 4: Save to CSV ===
    csv_file = "moneycontrol_articles.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["section", "url", "title", "date", "content"]
        )
        writer.writeheader()
        writer.writerows(all_articles)

    print(f"\n✅ Scraped {len(all_articles)} articles total.")
    print(f"📁 Saved to {csv_file}")


if __name__ == "__main__":
    main()
