import requests
from bs4 import BeautifulSoup
import csv
import time
 
BASE_URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_soup(url):
    """Download a webpage and return its parsed HTML."""
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20
    )
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_categories():
    """Collect category names and their URLs."""
    soup = get_soup(BASE_URL)
    categories = {}

    links = soup.select(
        "div.side_categories ul li ul li a"
    )

    for link in links:
        name = link.get_text(strip=True)
        url = BASE_URL + link["href"]
        categories[name] = url

    return categories


def scrape_category(category, category_url):
    """Scrape all books in one category."""
    books = []
    next_page = category_url

    while next_page:
        print(f"Scraping {category}: {next_page}")

        soup = get_soup(next_page)

        for item in soup.select("article.product_pod"):
            title = item.h3.a["title"]

            price_text = item.select_one(
                ".price_color"
            ).get_text(strip=True)

            # Convert price from GBP text to float
            price_gbp = float(
                price_text.replace("£", "").replace("Â", "")
            )

            rating_tag = item.select_one(
                "p.star-rating"
            )
            rating_word = rating_tag["class"][1]

            rating_map = {
                "One": 1,
                "Two": 2,
                "Three": 3,
                "Four": 4,
                "Five": 5
            }

            rating = rating_map.get(rating_word, 0)

            availability_text = item.select_one(
                ".availability"
            ).get_text(" ", strip=True)

            availability = (
                "In stock" in availability_text
            )

            book_url = item.h3.a["href"]

            books.append({
                "title": title,
                "category": category,
                "price_gbp": price_gbp,
                "rating": rating,
                "availability": availability,
                "book_url": book_url
            })

        # Find next page
        next_link = soup.select_one(
            "li.next a"
        )

        if next_link:
            from urllib.parse import urljoin
            next_page = urljoin(
                next_page,
                next_link["href"]
            )
        else:
            next_page = None

        time.sleep(0.2)

    return books


def main():
    categories = get_categories()

    # Use the first three categories
    selected_categories = list(
        categories.items()
    )[:3]

    all_books = []

    for category, url in selected_categories:
        books = scrape_category(category, url)
        all_books.extend(books)

    # Save the scraped records
    with open(
        "books.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "title",
                "category",
                "price_gbp",
                "rating",
                "availability",
                "book_url"
            ]
        )

        writer.writeheader()
        writer.writerows(all_books)

    print(f"Total books scraped: {len(all_books)}")
    print("Saved data to books.csv")


if __name__ == "__main__":
    main()
