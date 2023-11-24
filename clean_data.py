import json

from unidecode import unidecode

with open("data.json") as f:
    data = json.load(f)


def get_paragraphs(raw_text):
    keep = False
    lines = [[]]
    for line in raw_text:
        if "*** END" in line or "*** START" in line:
            keep = not keep
        elif keep:
            if line == "":
                lines.append([])
            else:
                lines[-1].append(unidecode(line.strip()))

    return [{"index": i, "text": " ".join(lines[i])} for i in range(len(lines))]


def chunk_paras(paragraphs):
    chunks = []
    chunk_index = 0
    for para in paragraphs:
        tokens = list(para["text"].split())
        if len(tokens) > 1000:
            num_splits = len(tokens) // 1000
            if len(tokens) % 1000 > 400:
                num_splits += 1

            length = int(len(tokens) / num_splits)
            for x in range(0, len(tokens), length):
                chunk_index += 1
                if x + 2 * length > len(tokens):
                    break
                chunks.append(
                    {
                        "chunk_index": chunk_index,
                        "paragraph_index": para["index"],
                        "character_index": x,
                        "text": " ".join(tokens[x : x + length]),
                    }
                )

            chunks.append(
                {
                    "chunk_index": chunk_index,
                    "paragraph_index": para["index"],
                    "character_index": x,
                    "text": " ".join(tokens[x:]),
                }
            )

        elif (
            sum(
                [
                    len(chunk["text"].split())
                    for chunk in chunks
                    if chunk["chunk_index"] == chunk_index
                ]
            )
            + len(tokens)
        ) > 1000:
            chunk_index += 1
            chunks.append(
                {
                    "chunk_index": chunk_index,
                    "paragraph_index": para["index"],
                    "character_index": 0,
                    "text": para["text"],
                }
            )
        else:
            chunks.append(
                {
                    "chunk_index": chunk_index,
                    "paragraph_index": para["index"],
                    "character_index": 0,
                    "text": para["text"],
                }
            )
    return chunks


data_cleaned = []
for book_id, book_data in data.items():
    if (
        "author" in book_data
        and book_data["category"][0] == "Text"
        and "Error 404" not in book_data["raw_text"][0]
        and book_data["language"][0] == "English"
        and book_id != "38194"  # DUPLICATED BOOK - Commentary on Weath of Nations
        and len(book_data["author"]) <= 2
    ):
        paragraphs = get_paragraphs(book_data["raw_text"])
        if len("".join([para["text"] for para in paragraphs])) > 17500:
            data_cleaned.append({})
            data_cleaned[-1]["title"] = book_data["title"][0]
            data_cleaned[-1]["ebook_no"] = int(book_data["ebook_no"][0])
            data_cleaned[-1]["author"] = " & ".join(book_data["author"])
            data_cleaned[-1]["paragraphs"] = paragraphs
            data_cleaned[-1]["chunks"] = chunk_paras(paragraphs)


with open("data_cleaned.json", "w") as f:
    json.dump(data_cleaned, f)
