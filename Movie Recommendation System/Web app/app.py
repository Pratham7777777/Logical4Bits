import pickle
import streamlit as st
import requests

st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)


# Replace 'YOUR_TMDB_API_KEY' with your actual TMDb API key
api_key = '8df5f5210d56fd729b8ec558df1ad3dc'
base_url = 'https://api.themoviedb.org/3/search/movie'
image_base_url = 'https://image.tmdb.org/t/p/w500'  # You can choose a different image size

def fetch_poster(movie_title):
    params = {
        'api_key': api_key,
        'query': movie_title
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        # Check if there are results
        if 'results' in data and data['results']:
            # Assuming we take the first result
            movie_id = data['results'][0]['id']
            poster_path = data['results'][0]['poster_path']

            # Construct the full poster URL
            poster_url = f'{image_base_url}{poster_path}' if poster_path else None
            return poster_url
    #     else:
    #         return None
    # else:
    #     print(f"Error: {response.status_code}")
    #     return None


# Example usage
# movie_title = 'Inception'
# poster_url = fetch_poster(movie_title)

# if poster_url:
#     print(f"The poster URL for {movie_name} is: {poster_url}")
# else:
#     print(f"Could not find a poster for {movie_name}")


# def fetch_poster(movie_title):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
#         movie_title)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        # movie_id = movies.iloc[i[0]].movieId
        recommended_movie_posters.append(fetch_poster(movies.iloc[i[0]].title))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return (recommended_movie_names,recommended_movie_posters)

if st.button('Show Recommendation'):
    st.text(selected_movie)
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])