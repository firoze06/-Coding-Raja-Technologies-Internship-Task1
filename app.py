from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the movies and similarity data
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity_list.pkl", 'rb'))
movies_list = movies['title'].values

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = [movies.iloc[i[0]].title for i in distances[1:9]]
    return recommended_movies

@app.route('/')
def home():
    return render_template('index.html', movies_list=movies_list)

@app.route('/recommend', methods=['POST'])
def recommend_movies():
    selected_movie = request.form['movie']
    recommended_movies = recommend(selected_movie)
    return render_template('index.html', movies_list=movies_list, recommendations=recommended_movies, selected_movie=selected_movie)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
