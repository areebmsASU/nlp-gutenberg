import os
import json


with open("vectors.json") as f:
    vectors = json.load(f)

book_id = {vector["id"]: vector["book_id"] for vector in vectors}


for b_id in set(book_id.values()):
    os.makedirs(f"js_scores_filtered/{b_id}")

for fname in os.listdir("js_scores_filtered/"):
    print(fname)
    if os.path.isfile(f"js_scores_filtered/{fname}"):
        os.rename(
            f"js_scores_filtered/{fname}",
            f"js_scores_filtered/{book_id[int(fname.rstrip('.json'))]}/{fname}",
        )
