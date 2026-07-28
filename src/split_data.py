import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("../data/clean_issues.csv")
print(f"Number of rows: {len(df)}")


train_val, test = train_test_split(
    df, test_size=0.15, stratify=df["label"], random_state=42
)
train, val = train_test_split(
    train_val, test_size=0.15/0.85, stratify=train_val["label"], random_state=42
)

train.to_csv("../data/train.csv", index=False)
val.to_csv("../data/val.csv", index=False)
test.to_csv("../data/test.csv", index=False)

print(f"Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")
