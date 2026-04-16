import requests
import json
import pandas as pd


def fetch_2079_data(page=1, rows=100):
    url = "https://result.election.gov.np/JSONFiles/ElectionResultCentral2079.txt"

    params = {
        "_search": "false",
        "rows": rows,
        "page": page,
        "sidx": "_id",
        "sord": "desc"
    }

    res = requests.get(url, params=params)

    # FIX encoding 
    res.encoding = "utf-8"

    return res.text


def parse_json_safe(raw_text):
    """
    Handles broken JSON safely.
    Extracts valid JSON objects even if full payload is corrupted.
    """
    try:
        # first try normal parsing
        return json.loads(raw_text)
    except:
        pass

    # fallback: extract objects manually
    import re

    objects = re.findall(r'\{.*?\}', raw_text)

    clean_data = []

    for obj in objects:
        try:
            clean_data.append(json.loads(obj))
        except:
            continue

    return clean_data


def scrape_all_pages(max_pages=5):
    all_rows = []

    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")

        raw = fetch_2079_data(page=page)
        data = parse_json_safe(raw)

        if not data:
            break

        all_rows.extend(data)

    return pd.DataFrame(all_rows)


# RUN SCRAPER
df = scrape_all_pages(max_pages=10)

print("Total rows:", len(df))
print(df.head())

# Save for SQL later
df.to_csv("election_2079_raw.csv", index=False)
print("Saved to CSV")