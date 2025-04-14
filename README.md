# 🎌 Anime Recommender System

A web-based Anime Recommender System built with **Flask**, **HTML/CSS**, and powered by data from the **Jikan API** and custom recommendation logic.

## 🔥 Features

- 🎯 Recommend anime based on anime title (using similarity matrix)
- 🎬 Recommend anime based on genre (sorted by popularity)
- 🧠 Personalized recommendation logic
- 📅 Recently released top-rated anime section
- 📺 Top 30 Anime & Top 30 Movies
- 📄 Individual Anime Detail Page (fetched using Jikan API)
- 📱 Responsive and minimal UI

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, Bootstrap
- **Backend**: Python (Flask)
- **Data**: Cleaned MyAnimeList dataset + Jikan API
- **Storage**: Git Large File Storage (Git LFS) for similarity matrix (or download manually)
- **Deployment**: Localhost (or can use Render/Heroku/Vercel for hosting)

---
## 🧑‍💻 How It Works
🔁 1. Content-Based Recommendation
Calculates similarity between anime titles using a cosine similarity matrix.

Returns the top 30 most similar anime.

## 🎭 2. Genre-Based Recommendation
Searches and ranks anime based on genres.

Filters by highest rating × popularity (score * favorites).
---
## Screenshots
![Screenshot (346)](https://github.com/user-attachments/assets/44555e5a-f3cd-4051-a7f5-6bfe365f8e8e)


![Screenshot (347)](https://github.com/user-attachments/assets/f3c770e3-3d2b-4aea-aec8-b5e4bcbff5a1)

---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/MahendraLadva123/Anime-Recommender-System.git
   cd Anime-Recommender-System
---

