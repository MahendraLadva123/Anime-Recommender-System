import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time
import os

# Setup
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
})

# File paths
userlist_file = "userlist.csv"
output_file = "C:/Users/jayde/Desktop/anime_lists.csv"
checkpoint_file = "checkpoint.txt"

# Load user list
df = pd.read_csv(userlist_file)
df = df.dropna()
# Load checkpoint
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, "r") as f:
        scraped_users = set(line.strip() for line in f)
    print(f"✅ Already scraped {len(scraped_users)} users")
else:
    scraped_users = set()

# Start scraping
for idx, url in df[446200:].iterrows():
    user_id = url["user_id"]
    username = url["username"]

    if username in scraped_users:
        print(f"⏩ Skipping already done user: {username}")
        continue

    try:
        u = session.get(f"https://myanimelist.net/animelist/{username}?status=7", timeout=10)
        print(f"Checking user: {username} - Status: {u.status_code}")
    except Exception as e:
        print(f"Failed to fetch {username}: {e}")
        continue  # Skip if connection fails

    if u.status_code != 200:
        print(f"Skipping user {username} due to status {u.status_code}")
        continue

    soup = BeautifulSoup(u.content, "html.parser")

    table_1 = soup.find("table", {"data-items": True})
    table_2 = soup.find_all("table", {"border": "0", "cellpadding": "0", "cellspacing": "0", "width": "100%"})

    user_data = []  # Data for this user

    if table_1:
        try:
            detail = json.loads(table_1['data-items'])
            for anime in detail:
                score = anime["score"]
                title = anime["anime_title"]
                anime_id = anime["anime_id"]
                if score != '-':
                    user_data.append([user_id, username, anime_id, title, score])
        except Exception as e:
            print(f"Error parsing JSON for {username}: {e}")

    elif table_2:
        for table in table_2:
            row = table.find("tr")
            if row:
                cells = row.find_all("td")
                if len(cells) >= 5:
                    anime_title_cell = cells[1]
                    score_cell = cells[2]

                    anime_title_link = anime_title_cell.find("a", class_="animetitle")
                    anime_id = anime_title_link["href"].split("/")[2] if anime_title_link else ""
                    anime_title = anime_title_link.find("span").text.strip() if anime_title_link else ""

                    score_label = score_cell.find("span", class_="score-label")
                    score = score_label.text.strip() if score_label else "-"

                    if anime_title and score != "-":
                        user_data.append([user_id, username, anime_id, anime_title, score])

    else:
        print(f"No anime list found for {username}")
        continue

    # Save this user's data immediately
    if user_data:
        temp_df = pd.DataFrame(user_data, columns=["user_id", "username", "anime_id", "anime_title", "score"])

        # Check if file exists
        write_header = not os.path.isfile(output_file)

        temp_df.to_csv(output_file, mode='a', header=write_header, index=False)
        print(f"✅ Saved {len(user_data)} anime entries for {username}")

    # Update checkpoint
    with open(checkpoint_file, "a") as f:
        f.write(username + "\n")

    # Sleep lightly every 50 users
    if (idx + 1) % 50 == 0:
        print(f"🛌 Sleeping for 5 seconds after {idx+1} users...")
        time.sleep(5)
    

print("\n🎯 ALL DONE! Scraping completed and saved!")
