import requests

# ---------------------------------------------------------
# TMDB API KEY
# ---------------------------------------------------------

API_KEY = "0383b81ddc27b5bf5553774e61ecb3bf"

BASE_URL = "https://api.themoviedb.org/3"

IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

YOUTUBE_SEARCH = "https://www.youtube.com/results?search_query="


# ---------------------------------------------------------
# Get complete movie information
# ---------------------------------------------------------

def get_movie_details(movie_id):

    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

        poster = IMAGE_BASE_URL + data["poster_path"] if data.get("poster_path") else ""

        title = data.get("title", "Unknown")

        rating = data.get("vote_average", 0)

        release = data.get("release_date", "N/A")

        genres = [genre["name"] for genre in data.get("genres", [])]

        overview = data.get("overview", "Overview not available.")

        runtime = data.get("runtime", "N/A")

        return {
            "poster": poster,
            "title": title,
            "rating": rating,
            "release": release,
            "genres": genres,
            "overview": overview,
            "runtime": runtime,
        }

    except Exception:

        return {
            "poster": "",
            "title": "Unknown",
            "rating": 0,
            "release": "",
            "genres": [],
            "overview": "Not Available",
            "runtime": ""
        }


# ---------------------------------------------------------
# Trailer
# ---------------------------------------------------------

def get_trailer(movie_id):

    url = f"{BASE_URL}/movie/{movie_id}/videos?api_key=0383b81ddc27b5bf5553774e61ecb3bf&language=en-US"

    try:

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        results = response.json()["results"]

        for item in results:

            if item["site"] == "YouTube" and item["type"] == "Trailer":

                return f"https://www.youtube.com/watch?v={item['key']}"

    except Exception:

        pass

    return None


# ---------------------------------------------------------
# Search trailer
# ---------------------------------------------------------

def search_trailer(movie_name):

    return YOUTUBE_SEARCH + movie_name.replace(" ", "+")


# ---------------------------------------------------------
# Genre Badge
# ---------------------------------------------------------

def genre_badges(genres):

    return " • ".join(genres)