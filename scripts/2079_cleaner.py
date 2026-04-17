import pandas as pd



def load_data(path):
    return pd.read_csv(path, encoding="utf-8")


def select_columns(df):
    return df[
        [
            "CandidateName",
            "PoliticalPartyName",
            "DistrictName",
            "StateName",
            "TotalVoteReceived",
            "Rank",
            "Remarks",
            "Age",
            "Gender",
            "SCConstID"   
        ]
    ].copy()



def clean_text(df):

    cols = [
        "CandidateName",
        "PoliticalPartyName",
        "DistrictName",
        "StateName",
        "Gender",
        "Remarks"
    ]

    for col in cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    return df



def clean_votes(df):

    df["TotalVoteReceived"] = (
        df["TotalVoteReceived"]
        .astype(str)
        .str.replace(",", "")
        .str.extract(r"(\d+)", expand=False)
    )

    df["TotalVoteReceived"] = pd.to_numeric(df["TotalVoteReceived"], errors="coerce")

    return df


def create_winner_flag(df):

    df["is_winner"] = df["Remarks"].str.lower().str.contains("elected", na=False)

    return df



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
        "स्वतन्त्र": "Independent"
    }

    df["PoliticalPartyName"] = df["PoliticalPartyName"].replace(mapping)

    return df

def standardize_province(df):
    mapping = {
        "कोशी प्रदेश": "Koshi",
        "मधेश प्रदेश": "Madhesh",
        "बागमती प्रदेश": "Bagmati",
        "गण्डकी प्रदेश": "Gandaki",
        "लुम्बिनी प्रदेश": "Lumbini",
        "कर्णाली प्रदेश": "Karnali",
        "सुदूरपश्चिम प्रदेश": "Sudurpaschim"
    }
    df["province"] = df["province"].replace(mapping)
    return df


def clean_geo(df):

    df["DistrictName"] = df["DistrictName"].str.replace("-", " ").str.strip()
    df["StateName"] = df["StateName"].str.strip()

    return df

def handle_constituency(df):

    df["SCConstID"] = pd.to_numeric(df["SCConstID"], errors="coerce")
    df = df.rename(columns={"SCConstID": "constituency"})

    return df


def rename_columns(df):

    return df.rename(columns={
        "CandidateName": "candidate",
        "PoliticalPartyName": "party",
        "DistrictName": "district",
        "StateName": "province",
        "TotalVoteReceived": "votes",
        "Rank": "rank",
        "Age": "age",
        "Gender": "gender"
    })


def finalize(df):

    df = df.drop(columns=["Remarks"])

    df = df.rename(columns={
        "district": "district_name",
        "is_winner": "winner"
    })

    df = df[
        [
            "province",
            "district_name",
            "constituency",
            "party",
            "votes",
            "winner"
        ]
    ]

    return df


def clean_2079(path):

    df = load_data(path)
    df = select_columns(df)
    df = clean_text(df)
    df = clean_votes(df)
    df = create_winner_flag(df)
    df = standardize_party(df)
    df = clean_geo(df)
    df = handle_constituency(df)
    df = rename_columns(df)
    df = standardize_province(df)
    df = finalize(df)
    return df


if __name__ == "__main__":

    df = clean_2079("data/2079/election_2079_raw.csv")

    df["election_year"] = 2079

    print("Rows:", len(df))
    print(df.head())

    df.to_csv("data/2079/election_2079_clean.csv", index=False)
    print("Saved: election_2079_clean.csv")