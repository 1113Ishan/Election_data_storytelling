import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import re


def clean_votes(text):

    if not text:
        return None

    # take first line only
    first_line = text.split("\n")[0]

    # remove commas and spaces
    first_line = first_line.replace(",", "").strip()

    # extract number safely using regex
    match = re.search(r"\d+", first_line)
    if match:
        return int(match.group())

    return None


def scrape_party(url, party_name):

    data = []

    html = requests.get(url).text
    soup = bs(html, "html.parser")

    table = soup.select_one("div.candidate-list-table")
    rows = table.find("tbody").find_all("tr")

    bad_rows = 0

    for row in rows:
        cols = row.find_all("td")

        if len(cols) < 4:
            bad_rows += 1
            continue

        try:
            province = cols[0].get_text(strip=True)
            candidate = cols[1].get_text(strip=True)
            district = cols[2].get_text(strip=True)

            # extract vote container safely
            vote_cell = cols[3]

            # prefer <p>, fallback to full text
            p_tag = vote_cell.find("p")
            if p_tag:
                votes = clean_votes(p_tag.get_text())
            else:
                votes = clean_votes(vote_cell.get_text())

            # winner detection
            span_tag = vote_cell.find("span")
            is_winner = False
            if span_tag and "Elected" in span_tag.get_text():
                is_winner = True

            data.append({
                "province": province,
                "candidate": candidate,
                "district": district,
                "votes": votes,
                "winner": is_winner
            })

        except Exception:
            bad_rows += 1
            continue

    df = pd.DataFrame(data)

    # --- FIX district parsing safely ---
    df[["district_name", "constituency"]] = df["district"].str.split("-", n=1, expand=True)

    df["district_name"] = df["district_name"].str.strip()
    df["constituency"] = df["constituency"].str.strip()

    # remove rows where constituency failed parsing
    df = df[df["constituency"].notna()]

    df["constituency"] = df["constituency"].astype(int)

    df["party"] = party_name
    df["election_year"] = 2082

    df = df.drop(columns=["district"])

    print(f"{party_name} scraped rows: {len(df)}, bad rows: {bad_rows}")

    return df


# -------------------------
# RUN SCRAPER
# -------------------------

party_urls = {
    'RSP': "https://election.ekantipur.com/party/7?lng=eng",
    'Nepali Congress': "https://election.ekantipur.com/party/2?lng=eng",
    'CPN-UML': "https://election.ekantipur.com/party/1?lng=eng",
    "Nepal Communist Party": "https://election.ekantipur.com/party/9?lng=eng",
    "Shram Sanskriti Party": "https://election.ekantipur.com/party/11?lng=eng",
    "Rastriya Prajatantra Party":"https://election.ekantipur.com/party/3?lng=eng",
    "Janata Samjbadi Party-Nepal": "https://election.ekantipur.com/party/6?lng=eng",
    "Rastriya Pariwartan Party":"https://election.ekantipur.com/party/16?lng=eng"
}

all_dfs = []

for party, url in party_urls.items():
    df_party = scrape_party(url, party)
    all_dfs.append(df_party)

final_df = pd.concat(all_dfs, ignore_index=True)

final_df.to_csv("data/2082/election_2082_results.csv", index=False)

print("Final rows:", len(final_df))