import os
import json

from collections import defaultdict, Counter

with open("vectors.json") as f:
    vectors = json.load(f)

book_id = {vector["id"]: vector["book_id"] for vector in vectors}

if False:
    for dir_name in sorted(os.listdir("js_scores_filtered/")):
        for file_name in sorted(os.listdir(f"js_scores_filtered/{dir_name}/")):
            with open(f"js_scores_filtered/{dir_name}/{file_name}") as f:
                chunk_scores = json.load(f)

            combined_scores = defaultdict(list)
            for chunk, score in chunk_scores.items():
                combined_scores[book_id[int(chunk)]].append(score)

            with open(f"js_scores_filtered/{dir_name}/{file_name}", "w") as f:
                json.dump(dict(combined_scores), f)
            print(f"{dir_name}/{file_name} completed.")

if False:
    for dir_name in sorted(os.listdir("js_scores_filtered/")):
        combined_score_counts = defaultdict(Counter)
        for file_name in sorted(os.listdir(f"js_scores_filtered/{dir_name}/")):
            with open(f"js_scores_filtered/{dir_name}/{file_name}") as f:
                book_scores = json.load(f)

            for b_id, scores in book_scores.items():
                combined_score_counts[b_id] += Counter(scores)

        with open(f"js_scores_filtered/{dir_name}.json", "w") as f:
            json.dump(
                dict(
                    {
                        b_id: dict(score_counts)
                        for b_id, score_counts in combined_score_counts.items()
                    }
                ),
                f,
            )

average_js_score_by_book = defaultdict(dict)
for dir_name in sorted(os.listdir("js_scores_filtered/")):
    if ".json" not in dir_name:
        continue

    with open(f"js_scores_filtered/{dir_name}") as f:
        value_counts_by_book = json.load(f)

    for b_id, value_counts in value_counts_by_book.items():
        _sum = 0
        _len = 0
        for value, counts in value_counts.items():
            _len += counts
            _sum += counts * float(value)
        average_js_score_by_book[int(dir_name.split(".")[0])][int(b_id)] = _sum / _len

with open(f"average_js_score_by_book.json", "w") as f:
    json.dump(dict(average_js_score_by_book), f)


exit()

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
