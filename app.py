import streamlit as st
import pickle
import requests


# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=5b6afc844f5a794b71751b52888997bb&language=en-US"
    data = requests.get(url).json()
    if 'poster_path' in data and data['poster_path']:
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    return None


# Function to fetch movie trailer (YouTube)
def fetch_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=5b6afc844f5a794b71751b52888997bb&language=en-US"
    data = requests.get(url).json()

    if 'results' in data:
        for video in data['results']:
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                return f"https://www.youtube.com/watch?v={video['key']}"

    return "🚫 No Trailer Available"


# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_trailers = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_trailers.append(fetch_trailer(movie_id))

    return recommended_movie_names, recommended_movie_posters, recommended_movie_trailers


# Load similarity matrix and movie data
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pickle.load(open('movies.pkl', 'rb'))

# Streamlit App Title
st.title("🎬 Movie Recommender System 🍿")

# Movie Selection
option = st.selectbox("Select a movie:", movies['title'].values)

# Recommendation Button
if st.button("Recommend"):
    recommended_movie_names, recommended_movie_posters, recommended_movie_trailers = recommend(option)

    col = st.columns(5)  # Create 5 columns for displaying movies
    for i in range(5):
        with col[i]:
            st.text(recommended_movie_names[i])  # Display movie title
            if recommended_movie_posters[i]:
                st.image(recommended_movie_posters[i])  # Display poster

            st.markdown(f"[▶ Watch Trailer]({recommended_movie_trailers[i]})")  # Display trailer link
