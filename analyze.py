import os
import json
from collections import defaultdict, Counter

import pandas as pd


with open("vectors.json") as f:
    vectors = json.load(f)

book_id = {vector["id"]: vector["book_id"] for vector in vectors}

max_chunk_id = max(
    [int(fname.rstrip(".json")) for fname in os.listdir("/mnt/e/js_scores/")]
)

for chunk_id in range(max_chunk_id + 1):
    with open(f"/mnt/e/js_scores/{chunk_id}.json") as f:
        by_book = defaultdict(list)
        for k, v in json.load(f).items():
            if not pd.isna(v) and v > 0.70:
                by_book[book_id[int(k)]].append(v)
        print({k: sum(vs) / len(vs) for k, vs in by_book.items()})
