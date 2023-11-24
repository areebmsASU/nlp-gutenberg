import os
import json
import math

max_chunk_id = max(
    [int(fname.rstrip(".json")) for fname in os.listdir("/mnt/e/js_scores/")]
)

for chunk_id in range(max_chunk_id + 1):
    with open(f"/mnt/e/js_scores/{chunk_id}.json") as f:
        js_scores = json.load(f)
    with open(f"js_scores_filtered/{chunk_id}.json", "w") as f:
        json.dump(
            dict(
                {
                    ch_id: round(score, 5)
                    for ch_id, score in js_scores.items()
                    if not math.isnan(float(score)) and float(score) > 0.70
                }
            ),
            f,
        )
