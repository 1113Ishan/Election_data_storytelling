import pandas as pd
import re


# -----------------------------
# 1. Load raw dataset
# -----------------------------
def load_data(path):
    df = pd.read_csv(path, encoding="utf-8")
    return df


# -----------------------------
# 2. Keep only needed columns
# -----------------------------
def select_columns(df):
    cols = [
        "CandidateName",
        "PoliticalPartyName",
        "DistrictName",
        "StateName",
        "TotalVoteReceived",
        "Rank",
        "Remarks",
        "Age",
        "Gender"
    ]
    return df[cols].copy()


# -----------------------------
# 3. Clean text fields
# -----------------------------
def clean_text(df):

    text_cols = [
        "CandidateName",
        "PoliticalPartyName",
        "DistrictName",
        "StateName",
        "Gender",
        "Remarks"
    ]

    for col in text_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    return df


# -----------------------------
# 4. Clean votes
# -----------------------------
def clean_votes(df):

    df["TotalVoteReceived"] = (
        df["TotalVoteReceived"]
        .astype(str)
        .str.replace(",", "")
        .str.extract(r"(\d+)", expand=False)
    )

    df["TotalVoteReceived"] = pd.to_numeric(df["TotalVoteReceived"], errors="coerce")

    return df


# -----------------------------
# 5. Winner flag
# -----------------------------
def create_winner_flag(df):

    df["is_winner"] = (
        df["Remarks"]
        .str.lower()
        .str.contains("elected", na=False)
    )

    return df


# -----------------------------
# 6. Standardize party names
# -----------------------------
def standardize_party(df):

    mapping = {
        "नेपाल कम्युनिष्ट पार्टी (एमाले)": "CPN-UML",
        "नेपाल कम्युनिष्ट पार्टी (माओवादी केन्द्र)": "CPN-Maoist Centre",
        "नेपाल कम्युनिष्ट पार्टी (माओवादी केन्द्र)(एकल चुनाव चिन्ह)": "CPN-Maoist Centre",
        "नेपाली काँग्रेस": "Nepali Congress",
        "जनता समाजवादी पार्टी, नेपाल": "Janata Samajwadi Party Nepal",
        "जनसमाजवादी पार्टी नेपाल": "Janata Samajwadi Party Nepal",
        "राष्ट्रिय प्रजातन्त्र पार्टी": "Rastriya Prajatantra Party",
        "राष्ट्रिय स्वतन्त्र पार्टी": "Rastriya Swatantra Party",
        "संघीय लोकतान्त्रिक राष्ट्रिय मञ्च": "Federal Democratic National Forum",
        "स्वतन्त्र": "Independent",
        "हाम्रो नेपाली पार्टी": "Hamro Nepali Party",
        "लोकतान्त्रिक समाजवादी पार्टी, नेपाल": "Loktantrik Samajbadi Party"
    }

    df["PoliticalPartyName"] = df["PoliticalPartyName"].replace(mapping)

    return df


# -----------------------------
# 7. Clean geography
# -----------------------------
def clean_geo(df):

    df["CandidateName"] = df["CandidateName"].str.replace(r"\s+", " ", regex=True)
    df["DistrictName"] = df["DistrictName"].str.replace("-", " ").str.strip()
    df["StateName"] = df["StateName"].str.strip()

    return df


# -----------------------------
# 8. Rename for SQL
# -----------------------------
def rename_columns(df):

    df = df.rename(columns={
        "CandidateName": "candidate",
        "PoliticalPartyName": "party",
        "DistrictName": "district",
        "StateName": "province",
        "TotalVoteReceived": "votes",
        "Rank": "rank",
        "Age": "age",
        "Gender": "gender"
    })

    return df


# -----------------------------
# 9. Final cleanup
# -----------------------------
def finalize(df):

    df = df.drop(columns=["Remarks"])

    df = df[
        [
            "candidate",
            "party",
            "district",
            "province",
            "votes",
            "rank",
            "is_winner",
            "age",
            "gender"
        ]
    ]

    return df


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def clean_2079(path):

    df = load_data(path)
    df = select_columns(df)
    df = clean_text(df)
    df = clean_votes(df)
    df = create_winner_flag(df)
    df = standardize_party(df)
    df = clean_geo(df)
    df = rename_columns(df)
    df = finalize(df)

    return df


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":

    df = clean_2079("election_2079_raw.csv")

    print("Rows:", len(df))
    print(df.head())

    df.to_csv("election_2079_clean.csv", index=False)
    print("Saved: election_2079_clean.csv")