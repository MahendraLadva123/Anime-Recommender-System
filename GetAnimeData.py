import requests
import time
import json

base_url = "https://api.jikan.moe/v4/anime"
all_anime = []
page = 1
max_pages = 10000  # safe upper limit

while True:
    print(f"📄 Fetching page {page}...")
    url = f"{base_url}?page={page}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Error on page {page}: {response.status_code}")
        break

    try:
        data = response.json()
        anime_list = data.get("data", [])
    except Exception as e:
        print(f"⚠️ JSON parsing error on page {page}: {e}")
        break

    if not anime_list:
        print("✅ No more data.")
        break

    for anime in anime_list:
        aired = anime.get("aired", {})
        broadcast = anime.get("broadcast", {})

        entry = {
            "id": anime.get("mal_id"),
            "title": anime.get("title"),
            "type": anime.get("type"),
            "episodes": anime.get("episodes"),
            "score": anime.get("score"),
            "members": anime.get("members"),
            "favorites": anime.get("favorites"),
            "duration": anime.get("duration"),
            "rating": anime.get("rating"),
            "from": aired.get("from"),
            "to": aired.get("to"),
            "season": anime.get("season"),
            "year": anime.get("year"),
            "broadcast_day": broadcast.get("day"),
            "broadcast_time": broadcast.get("time"),
            "broadcast_timezone": broadcast.get("timezone"),
            "broadcast_string": broadcast.get("string"),
            "genres": [g["name"] for g in anime.get("genres", [])],
            "explicit_genres": [g["name"] for g in anime.get("explicit_genres", [])],
            "themes": [t["name"] for t in anime.get("themes", [])],
            "producers": [p["name"] for p in anime.get("producers", [])],
            "licensors": [l["name"] for l in anime.get("licensors", [])],
            "studios": [s["name"] for s in anime.get("studios", [])],
            "synopsis": anime.get("synopsis")
        }

        all_anime.append(entry)

    page += 1
    time.sleep(1)

    if page > max_pages:
        print("⚠️ Reached max page limit.")
        break

print(f"\n🎉 Done! Total anime fetched: {len(all_anime)}")

# Save to JSON
filename = "all_anime_data.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_anime, f, ensure_ascii=False, indent=2)

print(f"💾 Saved to {filename}")
