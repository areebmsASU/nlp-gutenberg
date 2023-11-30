import json

from collections import Counter, defaultdict


with open("stem_data.json") as f:
    stem_data = json.load(f)

stems = stem_data["stems"]
word_to_stem = stem_data["word_to_stem"]
stem_to_words = stem_data["stem_to_words"]


def get_count_vector(text):
    counts = Counter(
        [word_to_stem[word] for word in text.split() if word in word_to_stem]
    )
    return [counts.get(stem, 0) for stem in stems]


js_scores = defaultdict(dict)

with open("lemmatized_data.json") as f:
    data = json.load(f)

vectors = []
for i in range(len(data)):
    vectors.append(
        {
            "id": i,
            "book_id": int(data[i]["ebook_no"]),
            "chunk_id": int(data[i]["chunk_id"]),
            "vector": get_count_vector(data[i]["text"]),
        }
    )
with open(f"vectors.json", "w") as f:
    json.dump(vectors, f)
