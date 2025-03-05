import streamlit as st
import pandas as pd
import pickle
import requests


# Function to fetch movie posters
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


# Function to get recommendations
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Fetch correct TMDb movie ID
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# Load models and data
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Streamlit UI
#st.title('**Movies Recommender System**')
st.markdown("<h1 style='text-align: center;'>Movies Recommender System</h1>", unsafe_allow_html=True)



selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values)




if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Create 5 equal columns for displaying recommendations
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i], width=150)  # Set a fixed width for uniformity
            st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 16px;'>{names[i]}</p>",
                        unsafe_allow_html=True)  # Centered and bold text