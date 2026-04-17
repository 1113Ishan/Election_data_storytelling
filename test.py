import pandas as pd

df = pd.read_csv("data/2082/election_2082_results.csv")

total = df[df["party"]=="RSP"]["votes"].sum()

print(total)
