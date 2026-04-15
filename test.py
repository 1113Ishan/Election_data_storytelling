import requests
from bs4 import BeautifulSoup as bs

# Requesting download from the url
url = "https://election.ekantipur.com/party/7?lng=eng"
html = requests.get(url).text

# Parsing the data into text using BeautifulSoup
soup = bs(html, "html.parser")

table = soup.select_one("div.candidate-list-table table")

rows = table.find_all("tr")
data = []

for row in rows:
    cols = row.find_all("td")

    if len(cols) < 4:
        continue


    province = cols[0].text.strip()
    candidate = cols[1].text.strip()
    district = cols[2].text.strip()
    votes_tag = cols[3].find("p")
    votes = votes_tag.text.strip().replace(",", "") if votes_tag else None
    votes = int(votes) if votes else None

    is_winner = "Elected" in row.text

    data.append({
        "province": province,
        "candidate": candidate,
        "district": district,
        "votes": votes,
        "winner": is_winner
    })

import pandas as pd

df = pd.DataFrame(data)

print(len(df))
print(df.head())

