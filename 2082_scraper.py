import requests
import pandas as pd
from bs4 import BeautifulSoup as bs




def scrape_party(url, party_name):

    # Create an empty dict for data storage
    data = []

    # Request html
    html = requests.get(url).text

    # Parse using BS
    soup = bs(html, "html.parser")

    # Locate table in the webpage
    table = soup.select_one("div.candidate-list-table")
    rows = table.find_all("tr")

    # Loop through each row of table
    for row in rows:
        cols = row.find_all("td")

        if len(cols) < 4:
            continue
        
        province = cols[0].text.strip()
        candidate = cols[1].text.strip()
        district = cols[2].text.strip()

        # clean votes to remove comma
        votes_tag = cols[3].find("p")
        if votes_tag:
            raw_votes = votes_tag.text.strip()
            first_line = raw_votes.split("\n")[0]
            votes = int(first_line.replace(",", ""))
        else:
            votes = None

        # Winner logic
        winner_tag = cols[3].find("span")
        is_winner = True if winner_tag and "Elected" in winner_tag.text else False

        # add everything into data dict
        data.append({
            "province": province,
            "candidate": candidate,
            "district": district,
            "votes": votes,
            "winner": is_winner
        })

    # Convert to dataframe pandas
    df = pd.DataFrame(data)

    # Split disctirct into disctict and constituency
    df[["district_name", "constituency"]] = df["district"].str.split("-", expand=True) 
    df["district_name"] = df["district_name"].str.strip() 
    df["constituency"] = df["constituency"].str.strip().astype(int)

    # Add party name
    df["party"] = party_name

    # drop old columns
    df = df.drop(columns=["district"])
    df["election_year"] = 2082

    return df



party_urls = {
    'RSP': "https://election.ekantipur.com/party/7?lng=eng",
    'NC': "https://election.ekantipur.com/party/2?lng=eng",
    'UML': "https://election.ekantipur.com/party/1?lng=eng",
    "NCP": "https://election.ekantipur.com/party/9?lng=eng"
}

all_dfs = []

for party, url in party_urls.items():
    df_party = scrape_party(url, party)
    all_dfs.append(df_party)

final_df = pd.concat(all_dfs, ignore_index=True)

final_df.to_csv("election_2082_results.csv", index=False)
