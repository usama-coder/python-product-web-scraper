import time
from typing import List, Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"


def scrape_books(pages: int = 5) -> List[Dict[str, str]]:
    """
    Scrape product data from a demo e-commerce website.

    Args:
        pages: Number of pages to scrape.

    Returns:
        A list of dictionaries containing product information.
    """

    all_books = []

    for page in range(1, pages + 1):
        url = BASE_URL.format(page)
        print(f"Scraping page {page}: {url}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as error:
            print(f"Error fetching page {page}: {error}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text.strip()
            availability = book.find("p", class_="instock availability").text.strip()
            rating = book.find("p", class_="star-rating")["class"][1]

            all_books.append({
                "title": title,
                "price": price,
                "availability": availability,
                "rating": rating,
            })

        time.sleep(1)

    return all_books


def save_to_excel(data: List[Dict[str, str]], filename: str = "output.xlsx") -> None:
    """
    Save scraped data to an Excel file.
    """

    df = pd.DataFrame(data)

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Books")

    print(f"Data saved to {filename}")


def main():
    books = scrape_books(pages=5)

    if books:
        save_to_excel(books)
        print(f"Scraping completed. Total records collected: {len(books)}")
    else:
        print("No data was collected.")


if __name__ == "__main__":
    main()
