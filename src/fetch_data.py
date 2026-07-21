from github import Auth
from github import Github
import json
import os
from dotenv import load_dotenv

load_dotenv()

auth = Auth.Token(os.getenv("GITHUB_API_TOKEN") or "")
g = Github(auth=auth)
repo = g.get_repo(os.getenv("GITHUB_REPO_NAME") or "")
issues = repo.get_issues(state="all")

collected = []
for i, issue in enumerate(issues):
    if issue.parent_issue_url is not None:
        continue

    print(f"Collecting {issue}")

    collected.append({
        "id": issue.number,
        "title": issue.title,
        "body": issue.body,
        "labels": [label.name for label in issue.labels],
        "state": issue.state,
        "created_at": issue.created_at.isoformat(),
        "comments_count": issue.comments
    })

    if i % 500 == 0:
        print(f"Collected {i} issues")

    # rate limit
    if len(collected) >= 6000:
        break

with open("../data/raw_issues.jsonl", "w") as f:
    for item in collected:
        f.write(json.dumps(item) + "\n")

print(f"Done: {len(collected)} issues collected")
