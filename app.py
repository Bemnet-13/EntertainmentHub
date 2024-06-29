import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np
from PIL import Image
from io import BytesIO

# Set custom styling

with open( "styles.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

def fetch_movie_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=3a656da52cc4139a9e90f39aa1b6cf0b&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend_movies(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = movie_similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x : x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_movie_poster(movie_id))
    
    return recommended_movies, recommended_movies_posters

def fetch_book_poster(endpoint):
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        return image
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch image: {e}")

def similar_book(book):
    book_index = books[books['original_title'] == book].index[0]
    distances = similarity[book_index]
    books_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x : x[1])[1:6]
    recommended_books = []
    recommended_books_posters = []
    for i in books_list:
        recommended_books.append(books.iloc[i[0]].original_title)
        recommended_books_posters.append(fetch_book_poster(books.iloc[i[0]].image_url))
    return recommended_books, recommended_books_posters

def popular_books():
    group_col = "original_title"
    rating_col = "popularity"
    grouped = popularity_list.groupby(group_col).agg({rating_col: [np.size, np.sum, np.mean]})
    popular = grouped.sort_values((rating_col, "mean"), ascending = False)
    total_sum = grouped[rating_col]["sum"].sum()
    popular["percentage"] = popular[rating_col]["sum"].div(total_sum) * 100

    popular.sort_values(("percentage"), ascending = False)[:10]


# Fetch datasets
books_list = pickle.load(open('./dataset/books_dict.pkl', 'rb'))
books = pd.DataFrame(books_list)
similarity =  pickle.load(open('./dataset/similarity.pkl', 'rb'))
popularity = pickle.load(open('./dataset/popularity.pkl', 'rb'))
popularity_list = pd.DataFrame(popularity)
movies_list = pickle.load(open('./dataset/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
movie_similarity =  pickle.load(open('./dataset/movie_similarity.pkl', 'rb'))

# UI elements

st.image('./images/Entertainment Hub_transparent.png')

entertainment_choice = st.radio('Entertainment Choice', ('Books', 'Movies'))

if entertainment_choice == 'Books':
    recommendation_style = st.radio('Recommend By', ('Popularity', 'Similarity'))
    if recommendation_style == 'Similarity':
        st.write('Using this option, Entertainment Hub provides you with books and movies that are similar with the one you have choosen from collection of entertainment options.')
        selected_book_name= st.selectbox('Movies of your choice', books['original_title'].values)
    
        if st.button('Recommend'):
            names, posters = similar_book(selected_book_name)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(names[0])
                st.image(posters[0])
            with col2:
                st.text(names[1])
                st.image(posters[1])
            with col3:
                st.text(names[2])
                st.image(posters[2])
            with col4:
                st.text(names[3])
                st.image(posters[3])
            with col5:
                st.text(names[4])
                st.image(posters[4])

    elif recommendation_style == 'Popularity':
        st.write("Here are the most Entertainment Hub's popular ten books based on Entertainment Hub's popularty metric")
        popular_books()

elif entertainment_choice == 'Movies':
    selected_movie_name= st.selectbox('Movies of your choice', movies['title'].values)

    if st.button('Recommend') and entertainment_choice == 'Movies':
        names, posters = recommend_movies(selected_movie_name)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])