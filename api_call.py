# Import the libraries that we will use throughout the project
import os
import requests
import json
from dotenv import load_dotenv

# Getting the api token stored in our .env file
load_dotenv()
TOKEN = os.getenv("API_READ_ACCESS_TOKEN")
# incase the token is missing:
if not TOKEN:
    raise ValueError("API_READ_ACCESS_TOKEN is missing from your .env file.")

# Collection of movie ids whose data we will use for the project
movie_collection = [
    299534, 19995, 140607, 299536, 597, 135397,
    420818, 24428, 168259, 99861, 284054, 12445,
    181808, 330457, 351286, 109445, 321612, 260513
]

movies = []

# Loop through the api url using each "movie id"
for movie_id in movie_collection:
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US&append_to_response=credits"
    try:
        # The header where the token is applied
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TOKEN}"
        }
        # the response from the api
        response = requests.get(url, headers=headers)
        # convert the response to json
        movie_data = response.json()
        # save the data to our list
        movies.append(response.json())
        print(f"Fetched: {movie_data.get('title', movie_id)}")
        
    except requests.exceptions.HTTPError as error:
        print(f"Could not fetch movie ID {movie_id}: {error}")

    except requests.exceptions.RequestException as error:
        print(f"Request failed for movie ID {movie_id}: {error}")

# Save the response to json file:
with open("tmdb_movies_raw.json", "w", encoding="utf-8") as file:
    json.dump(movies, file, ensure_ascii=False, indent=2)

print(f"Saved {len(movies)} API responses to tmdb_movies_raw.json")
