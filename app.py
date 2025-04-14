from flask import Flask, render_template, request
import pandas as pd
import pickle
import requests

similarity= pickle.load(open('similarity.pkl','rb'))


app = Flask(__name__)
data = pd.read_csv("cleaned_data.csv")

@app.route("/" , methods = ["GET"])
def home():
    temp = data[data['type'] == 'TV'].copy()
    top_tv_anime = temp.sort_values(by='top_metric', ascending=False).head(30)
    top_movies = data[data['type'] == 'Movie'].sort_values(by='top_metric', ascending=False).head(30)
    recent_anime = data.sort_values(by = "year" , ascending = False)[:20].sort_values(by = "top_metric" , ascending=  False).dropna()

    top_anime_list = top_tv_anime[['eng_title', 'Poster', 'score', 'id']].to_dict(orient='records')
    top_anime_moie = top_movies[['eng_title', 'Poster', 'score', 'id']].to_dict(orient='records')
    top_recent_anime = recent_anime[['eng_title', 'Poster', 'score', 'id']].to_dict(orient='records')

    return render_template("index.html" ,  top_anime=top_anime_list , top_movie = top_anime_moie , recent_anime = top_recent_anime)

@app.route('/anime/<int:anime_id>')
def anime_detail(anime_id):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}"
    response = requests.get(url)
    anime = response.json().get('data', {})

    return render_template("anime_detail.html", anime=anime)

@app.route('/recommender')
def recommender():
    return render_template("recommender.html")

@app.route("/recommender/anime", methods=["POST", "GET"])
def recommedAnime():
    if request.method == "GET":
        return render_template("recommed_anime.html", name=[], not_found=False)

    name = request.form.get("anime_name")

    if not name:
        return render_template("recommed_anime.html", name=[], not_found=False)

    if name not in data["title"].values:
        return render_template("recommed_anime.html", name=[], not_found=True, anime_name=name)

    index = data[data["title"] == name].index[0]
    dis = similarity[index]
    movie_list = sorted(list(enumerate(dis)), reverse=True, key=lambda x: x[1])[1:30]

    get_data = []
    for i in movie_list:
        temp = [
            data.iloc[i[0]].id,
            data.iloc[i[0]].title,
            data.iloc[i[0]].Poster,
            data.iloc[i[0]].score
        ]
        get_data.append(temp)

    return render_template("recommed_anime.html", name=get_data, not_found=False)

@app.route("/recommender/genres", methods=["POST", "GET"])
def recommendanime():
    if request.method == "GET":
        return render_template("recommed_by_genres.html", name=[], not_found=False)

    name = request.form.get("anime_name")

    if not name:
        return render_template("recommed_by_genres.html", name=[], not_found=False)
    
    data["high"] = data["score"]*data["favorites"]
    movie_list = data[data["genres"].str.lower().str.contains(name)].sort_values(by = "high"  , ascending = False)[:20]
    movie_data = movie_list[["id" , "title" , "score" , "Poster"]].values


    return render_template("recommed_by_genres.html" , result = movie_data)


if __name__ == "__main__":
    app.run(debug=True)