import json
from collections import defaultdict


with open("lemmatized_data.json") as f:
    data = json.load(f)

book_frequency = defaultdict(int)
book_words = defaultdict(set)
document_frequency = defaultdict(int)


# Determine book frequency


for d in data:
    for t in d["text"].split():
        if t and t.isalpha():
            book_words[d["ebook_no"]].add(t.lower())


for book_id, words in book_words.items():
    for word in words:
        book_frequency[word] += 1


keywords = set(
    [
        word
        for word, freq in sorted(
            book_frequency.items(), key=lambda df: df[1], reverse=False
        )
        if 215 > freq > 1
    ]
)


for d in data:
    words = set([t.lower() for t in d["text"].split() if t and t.isalpha()]) & keywords
    for word in words:
        document_frequency[word] += 1


document_frequency = {
    term: freq
    for term, freq in sorted(
        document_frequency.items(), key=lambda df: df[1], reverse=False
    )
    if freq > 2
}


print(document_frequency)
print(len(keywords), len(document_frequency))
