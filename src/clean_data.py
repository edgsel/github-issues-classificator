import json
import pandas as pd

raw_issues = []

with open("../data/raw_issues.jsonl", "r") as f:
    for line in f:
        raw_issues.append(json.loads(line))

print(f"Total issues before cleaning: {len(raw_issues)}")

LABEL_MAP = {
    "bug": "bug",
    "feature-request": "feature-request",
    "under-discussion": "under-discussion",
    "info-needed": "info-needed",
    "ux": "ux"
}

PRIORITY = ["bug", "feature-request", "under-discussion", "info-needed", "ux"]

def extract_label(labels):
    normalized = [LABEL_MAP[l.lower()] for l in labels if l.lower() in LABEL_MAP]

    if not normalized:
        return None

    for p in PRIORITY:
        if p in normalized:
            return p
    return normalized[0]

cleaned = []

for issues in raw_issues:
    # filter out issues with no name and title
    title = (issues.get("title") or "").strip()
    body = (issues.get("body") or "").strip()

    if not title and not body:
        continue

    label = extract_label(issues.get("labels", []))

    # no label, no learning
    if label is None:
        continue

    full_text = f"{title}\n\n{body}"

    # filtering out the noise
    if len(full_text) < 20:
        continue

    cleaned.append({"text": full_text, "label": label})

df = pd.DataFrame(cleaned)
df = df.drop_duplicates(subset="text")

print(f"Total issues after cleaning: {len(df)}")
print(df["label"].value_counts())

df.to_csv("../data/clean_issues.csv", index=False)
