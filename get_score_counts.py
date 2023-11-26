import os
import json
from collections import defaultdict, Counter


max_chunk_id = max(
    [int(fname.rstrip(".json")) for fname in os.listdir("/mnt/e/js_scores/")]
)


score_counts = Counter()
for chunk_id in range(max_chunk_id + 1):
    with open(f"/mnt/e/js_scores/{chunk_id}.json") as f:
        score_counts += Counter(list(map(lambda x: round(x, 3), json.load(f).values())))

with open(f"score_counts.json", "w") as f:
    json.dump(dict(score_counts), f)
