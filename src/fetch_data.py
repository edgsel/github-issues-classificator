from github import Auth
from github import Github
import json
import os
from dotenv import load_dotenv

load_dotenv()

auth = Auth.Token(os.getenv("GITHUB_API_TOKEN") or "")
g = Github(auth=auth)
repo = g.get_repo(os.getenv("GITHUB_REPO_NAME") or "")

collected = []
relevant_labels = ["bug", "feature-request", "ux"]
ISSUES_LIMIT_PER_LABEL = 5000

for label in relevant_labels:
    issues = repo.get_issues(state="all", labels=[label])

    print(f"Fetching issues for label: {label}")

    for i, issue in enumerate(issues):
        if issue.pull_request is not None:
            continue

        print(f"Collecting {issue}")

        collected.append({
            "id": issue.number,
            "title": issue.title,
            "body": issue.body or "",
            "labels": [l.name for l in issue.labels],
            "state": issue.state,
            "created_at": issue.created_at.isoformat(),
            "comments_count": issue.comments
        })

        if i % 500 == 0:
            print(f"Collected {i} issues")

        # rate limit
        if i >= ISSUES_LIMIT_PER_LABEL:
            break

with open("../data/raw_issues.jsonl", "w") as f:
    for item in collected:
        f.write(json.dumps(item) + "\n")

print(f"Done: {len(collected)} issues collected")
