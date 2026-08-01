import streamlit as st
import pandas as pd
import pickle
from tmdb import *
import os
import gdown

FILE_ID ="1OirwADjv5MeJBBe1OdisuJihCgtj-Jwt"

if not os.path.exists("similarity.pkl"):
    print("Downloading similarity.pkl...")

    url = f"https://drive.google.com/uc?id={FILE_ID}"

    gdown.download(
        url,
        "similarity.pkl",
        quiet=False
    )
    gdown.download(
            url,
            "movies_dict.pkl",
            quiet=False
        )
    

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

movies = pickle.load(open("movies_list.pkl", "rb"))
movies = pd.DataFrame(movies)

similarity = pickle.load(open("similarity.pkl", "rb"))

movie_titles = movies["title"].values

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
        🎬 Movie Recommender
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-text">

        Discover amazing movies using an
        AI-powered recommendation engine.

        ---
        ✔ 5000+ Movies

        ✔ Content-Based Filtering

        ✔ TMDB Integration

        ✔ Streamlit

        ✔ Machine Learning

        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">

    <h1>🎬 Movie Recommender System</h1>

    <p>
    Discover movies you'll love with Machine Learning.
    Select your favourite movie and receive intelligent recommendations instantly.
    </p>

    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# METRICS
# --------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="metric">
        <h2>5000+</h2>
        <p>Movies</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="metric">
        <h2>AI</h2>
        <p>Recommendation Engine</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="metric">
        <h2>TMDB</h2>
        <p>Movie Database</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# SEARCH SECTION
# --------------------------------------------------

st.subheader("🍿 Select Your Favourite Movie")

selected_movie = st.selectbox(
    "",
    movie_titles,
    index=0,
)

# --------------------------------------------------
# RECOMMENDATION FUNCTION
# --------------------------------------------------

def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1],
    )[1:9]

    recommendations = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        details = get_movie_details(movie_id)

        details["movie_id"] = movie_id

        recommendations.append(details)

    return recommendations
# --------------------------------------------------
# RECOMMEND BUTTON
# --------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

if st.button("✨ Recommend Movies"):

    with st.spinner("Finding movies you'll love... 🍿"):

        recommendations = recommend(selected_movie)

    st.markdown("---")

    st.subheader("🎥 Recommended For You")

    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(4)

    for index, movie in enumerate(recommendations):

        with cols[index % 4]:

            st.markdown('<div class="movie-card">', unsafe_allow_html=True)

            if movie["poster"]:

                st.image(movie["poster"], use_container_width=True)

            st.markdown(
                f"""
                <div class="movie-title">
                {movie['title']}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="movie-info">

                ⭐ <b>{movie['rating']}</b>/10

                <br><br>

                📅 {movie['release']}

                <br><br>

                ⏱ {movie['runtime']} min

                </div>
                """,
                unsafe_allow_html=True,
            )

            if movie["genres"]:

                badge_html = ""

                for genre in movie["genres"]:

                    badge_html += f'<span class="badge">{genre}</span>'

                st.markdown(
                    badge_html,
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)

            overview = movie["overview"]

            if len(overview) > 170:

                overview = overview[:170] + "..."

            st.write(overview)

            trailer = get_trailer(movie["movie_id"])

            if trailer:

                st.link_button(
                    "▶ Watch Trailer",
                    trailer,
                    use_container_width=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)
# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer">

    <h3>🎬 Movie Recommender System</h3>

    <p>
    Powered by Machine Learning • Built with Streamlit
    </p>

    <p>
    Developed by <b>Indrapal Singh </b>
    </p>

    </div>
    """,
    unsafe_allow_html=True,
)