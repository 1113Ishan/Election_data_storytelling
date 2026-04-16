import pandas as pd

df_2079 = pd.read_csv("data/2079/election_2079_clean.csv")
df_2082 = pd.read_csv("data/2082/election_2082_results.csv")


def prepare_2082(df):

    df = df.drop(columns=['candidate'])

    df = df[
        [
            "province",
            "district_name",
            "constituency",
            "party",
            "votes",
            "winner",
            "election_year"
        ]
    ]

    return df

def prepare_2079(df):
    df = df[
       [ "province",
        "district_name",
        "constituency",
        "party",
        "votes",
        "winner",
        "election_year"]
    ]

    return df

df_2082 = prepare_2082(df_2082)
df_2079 = prepare_2079(df_2079)

df_final = pd.concat([df_2079, df_2082], ignore_index = True)

df_final.to_csv("data/final_election_dataset.csv", index=False)
print("Final dataset created.")
print("Rows:", len(df_final))
print(df_final.head())