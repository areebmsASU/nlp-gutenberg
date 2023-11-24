import os
import json

from collections import defaultdict

js_scores = defaultdict(lambda: defaultdict(dict))

for file_name in sorted(os.listdir("js_scores/"), key=int):
    with open(f"js_scores/{file_name}") as f:
        file_data = json.load(f)
        for i in range(int(max(file_data.keys(), key=int)) + 1):
            for j in range(int(max(file_data.keys(), key=int)) + 1):
                js_scores[int(file_name.rstrip(".json"))][i][j] = file_data[str(i)][
                    str(j)
                ]
    with open(f"js_scores.json", "w") as f:
        json.dump({k: dict(v) for k, v in js_scores.items()}, f)
    print(file_name.rstrip(".json"))


# This file failed do to memory issues.
