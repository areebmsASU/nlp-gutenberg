import json
from collections import defaultdict, Counter

import numpy as np


with open("data.json") as f:
    subjects = {
        int(k): (
            "Economics" if "Economics" in " ".join(v["subject"]).split() else "Other"
        )
        for k, v in json.load(f).items()
    }


titles = {}
authors = {}
chunks_by_book = defaultdict(lambda: defaultdict(list))
with open("data_cleaned.json") as f:
    for book_data in json.load(f):
        titles[int(book_data["ebook_no"])] = book_data["title"]
        authors[int(book_data["ebook_no"])] = book_data["author"]
        for chunk in book_data["chunks"]:
            chunks_by_book[int(book_data["ebook_no"])][chunk["chunk_index"]].append(
                chunk["text"]
            )

chunk_texts = []
chunk_id_by_book = defaultdict(list)
book_ids = {}
for book_id, book_chunks in chunks_by_book.items():
    book_chunks = list(book_chunks.values())
    for chunk_i in range(len(book_chunks)):
        chunk_id_by_book[int(book_id)].append(len(chunk_texts))
        book_ids[len(chunk_texts)] = int(book_id)
        chunk_texts.append(
            "\n".join([chunk_text for chunk_text in book_chunks[chunk_i]])
        )


def get_chunk_info(chunk_id, divergence=None):
    info = {
        "chunk_id": chunk_id,
        "book_id": book_ids[chunk_id],
        "title": titles[book_ids[chunk_id]],
        "author": authors[book_ids[chunk_id]],
        #  "subject": subjects[book_ids[chunk_id]],
    }
    if divergence:
        info["divergence"] = divergence

    return info


def get_death_date(book_id):
    try:
        return int(authors[int(book_id)].split("-")[-1])
    except:
        return 3000


def least_divergence(chunk_id):
    with open(f"/mnt/e/js_scores/{chunk_id}.json") as f:
        scores = json.load(f).items()
    total = None
    economics = None
    book = None
    author = None
    most_matched_id = None
    influenced_id = None

    for matched_id, divergence in sorted(scores, key=lambda x: x[1]):
        if 3901 <= book_ids[int(matched_id)] <= 3912:
            continue
        if divergence and not np.isnan(divergence) and int(matched_id) != int(chunk_id):
            if total is None:
                total = divergence
            if book is None and book_ids[int(matched_id)] == book_id:
                book = divergence
            elif (
                author is None
                and authors[book_ids[int(matched_id)]] == authors[book_id]
            ):
                author = divergence
            else:
                if most_matched_id is None:
                    most_matched_id = int(matched_id)
                if influenced_id is None and get_death_date(
                    book_ids[int(chunk_id)]
                ) > get_death_date(book_ids[int(matched_id)]):
                    influenced_id = int(matched_id)

            if economics is None and subjects[book_ids[int(matched_id)]] == "Economics":
                economics = divergence
        if (
            total
            and economics
            and book
            and author
            and most_matched_id
            and influenced_id
        ):
            return total, economics, author, book, most_matched_id, influenced_id
    return total, economics, author, book, most_matched_id, influenced_id


book_summary = []
for book_id, chunk_ids in sorted(chunk_id_by_book.items()):
    if 3901 <= book_id <= 3912:
        continue
    this_book = []
    this_author = []
    total = []
    economics = []
    most_matched_book = []
    most_influenced_authors = []
    for chunk_id in chunk_ids:
        (
            ch_total,
            ch_economics,
            ch_author,
            ch_book,
            ch_most_matched_id,
            ch_influenced_id,
        ) = least_divergence(chunk_id)
        # print(ch_total, ch_economics, ch_author, ch_book)
        if ch_influenced_id is not None:
            most_influenced_authors.append(authors[book_ids[ch_influenced_id]])
        if ch_most_matched_id is not None:
            most_matched_book.append(book_ids[ch_most_matched_id])
        if ch_book is not None:
            this_book.append(ch_book)
        if ch_author is not None:
            this_author.append(ch_author)
        if ch_total is not None:
            total.append(ch_total)
        if ch_economics is not None:
            economics.append(ch_economics)

    most_matched_book_id, most_matched_book_count = Counter(
        most_matched_book
    ).most_common(1)[0]

    if most_influenced_authors:
        most_influenced_author, most_influenced_author_count = Counter(
            most_influenced_authors
        ).most_common(1)[0]
    else:
        most_influenced_author, most_influenced_author_count = 0, 0
    book_summary.append(
        {
            "id": book_id,
            "title": titles[book_id],
            "author": authors[book_id],
            "subject": subjects[book_id],
            "overall_divergence": round(np.mean(total), 3),
            "economics_divergence": round(np.mean(economics), 3),
            "same_author_divergence": round(np.mean(this_author), 3),
            "same_book_divergence": round(np.mean(this_book), 3),
            "matched_count": len(total),
            "chuck_count": len(chunk_ids),
            "matched_book": titles[most_matched_book_id],
            "matched_book_count": most_matched_book_count,
            "influence": most_influenced_author,
            "influence_count": most_influenced_author_count,
        }
    )
    print(book_summary[-1])

with open("book_summary.json", "w") as f:
    json.dump(book_summary, f)
