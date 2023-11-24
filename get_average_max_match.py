import os
import json
from collections import defaultdict, Counter

import pandas as pd
import numpy as np


with open("vectors.json") as f:
    vectors = json.load(f)

book_id = {vector["id"]: vector["book_id"] for vector in vectors}

max_chunk_id = max(
    [
        int(fname.rstrip(".json"))
        for fname in os.listdir("/mnt/e/js_scores_filtered_only/")
    ]
)

for chunk_id in range(max_chunk_id + 1):
    with open(f"/mnt/e/js_scores_filtered_only/{chunk_id}.json") as f:
        # sorted(json.load(f).items(), key=lambda x: x[1], reverse=True)[:4]
        # print(json.load(f))

        print(book_id[chunk_id], chunk_id, np.mean(list(json.load(f).values())))
        # print(
        #    book_id[chunk_id],
        #    chunk_id,
        #   Counter(
        #        [book_id[int(ch)] for ch, s in json.load(f).items() if s == 0.83255]
        #    ).most_common(5),
        # )
