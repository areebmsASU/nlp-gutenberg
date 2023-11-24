import os
import json


for file_name in os.listdir("raw/"):
    with open(f"raw/{file_name}") as f:
        file_data = json.load(f)
        for chunk_id, scores in file_data.items():
            with open(f"js_scores/{chunk_id}.json", "w") as f:
                json.dump(dict(scores), f)
