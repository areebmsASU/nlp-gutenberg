import requests as r
from bs4 import BeautifulSoup
from time import sleep
from collections import defaultdict
import json

BASE_URL = "https://gutenberg.org"
ECONOMICS_BASE_URL = f"{BASE_URL}/ebooks/subject/1301"
MAX_BOOK_IDS_PER_PAGE = 25


def get_metadata(page_content):
    metadata = defaultdict(list)
    for tr in (
        BeautifulSoup(page_content, "html.parser")
        .find("table", class_="bibrec")
        .find_all("tr")
    ):
        key = tr.find("th")
        if key is not None:
            value = tr.find("td")
            a = value.find("a")
            href = a["href"] if a else None
            key = key.text.lower().replace(" ", "-").replace(".", "").replace("-", "_")
            metadata[key].append([_ for _ in tr.find("td").text.split("\n") if _][0])
            if href:
                metadata[key + "_link"].append(href)
    return dict(metadata)


def get_text(page_context):
    lines = []
    for line in BeautifulSoup(page_context, "html.parser").text.split("\r\n"):
        lines.append(line)
    return lines


def get_book_ids(url):
    page_book_ids = []
    num_book_ids = -1
    while num_book_ids == -1 or (
        len(page_book_ids) != num_book_ids
        and len(page_book_ids) % MAX_BOOK_IDS_PER_PAGE == 0
    ):
        sleep(1)
        num_book_ids = len(page_book_ids)
        book_list_page = r.get(url + f"?start_index={num_book_ids+1}")
        print(url + f"?start_index={num_book_ids+1}")
        for link in BeautifulSoup(book_list_page.text, "html.parser").find_all("a"):
            if (
                "ebooks" in link.get("href", "")
                and link["href"].split("/")[2].isdigit()
                and link["href"].split("/")[2] not in page_book_ids
            ):
                page_book_ids.append(link["href"].split("/")[2])

    return page_book_ids


# Economics URL was scraped to get all of the gutenberg book_ids.
subject_book_ids = get_book_ids(ECONOMICS_BASE_URL)

print("subject:", len(subject_book_ids), subject_book_ids)


data = {}
for book_id in subject_book_ids:
    if book_id not in data:
        print("Searching Book ID", book_id, "Total Books Searched", len(data))
        sleep(1)
        # Each gutenberg book_id was then used to scrape the metadata provided within a table on the book summary page inside Gutenberg.
        data[book_id] = get_metadata(
            r.get(f"https://gutenberg.org/ebooks/{book_id}/").content
        )
        # The book was then also used to scrape the book within txt format on Gutenberg.
        data[book_id]["raw_text"] = get_text(
            r.get(f"https://gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt").content
        )

        # The links that were retrieved from the metadata page were then used to scrape all the books available by that author.
        author_links = set()
        for link in data[book_id].get("author_link", []):
            author_links.add(link)

        for link in author_links:
            author_book_ids = get_book_ids(BASE_URL + link)
            for author_book_id in author_book_ids:
                if author_book_id not in data:
                    sleep(1)
                    data[author_book_id] = get_metadata(
                        r.get(f"https://gutenberg.org/ebooks/{author_book_id}/").content
                    )
                    data[author_book_id]["raw_text"] = get_text(
                        r.get(
                            f"https://gutenberg.org/cache/epub/{author_book_id}/pg{author_book_id}.txt"
                        ).content
                    )

        with open("data.json", "w") as f:
            json.dump(data, f)
