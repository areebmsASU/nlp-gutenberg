import os
import json
from time import time

from collections import defaultdict
from scipy.spatial.distance import jensenshannon


with open("vectors.json") as f:
    vectors = json.load(f)


with open("stem_data.json") as f:
    stem_data = json.load(f)

stems = stem_data["stems"]
word_to_stem = stem_data["word_to_stem"]
stem_to_words = stem_data["stem_to_words"]


import concurrent.futures


def save_scores(i):
    print(i, "started.")
    if i in [int(file.rstrip(".json")) for file in os.listdir("js_scores/")]:
        return
    t0 = time()
    js_scores = {}
    for j in range(len(vectors)):
        js_scores[j] = jensenshannon(vectors[i]["vector"], vectors[j]["vector"])

    with open(f"js_scores/{i}.json", "w") as f:
        json.dump(dict(js_scores), f)
    print(time() - t0, i, len(vectors))


pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)

with concurrent.futures.ThreadPoolExecutor() as pool:
    for i in range(9850, len(vectors)):
        save_scores(i)
        # pool.submit(save_scores, i)

    pool.shutdown(wait=True)
