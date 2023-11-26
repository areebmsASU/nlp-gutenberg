import json
from collections import defaultdict

# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")


with open("data_cleaned.json") as f:
    data = json.load(f)

lemmatized_data = []

chunks = defaultdict(lambda: defaultdict(list))
for d in data:
    for chunk in d["chunks"]:
        chunks[d["ebook_no"]][chunk["chunk_index"]].append(chunk["text"])

lemmas = defaultdict(set)
for book_id in chunks:
    for chunk_id in chunks[book_id]:
        doc = nlp(" ".join(chunks[book_id][chunk_id]).lower())
        for token in doc:
            lemmas[token.text].add(token.lemma_)

        lemmatized_data.append(
            {
                "ebook_no": book_id,
                "chunk_id": chunk_id,
                "text": " ".join([token.lemma_ for token in doc]),
            }
        )
    with open("lemmatized_data.json", "w") as f:
        json.dump(lemmatized_data, f)

    with open("lemmas.json", "w") as f:
        lemma_dict = {
            key: sorted(list(value), key=len) for key, value in lemmas.items()
        }
        json.dump(lemma_dict, f)
    print(list(chunks).index(book_id), len(chunks))
