import requests
from pprint import pprint

API_KEY_TMDB = "7f986feba58d744fa85540122b64cd4c"
URL_SEARCH_MOVIE = "https://api.themoviedb.org/3/search/movie"
URL_MOVIE_DETAILS = "https://api.themoviedb.org/3/movie/"
URL_ROOT_IMAGE = "https://www.themoviedb.org/t/p/w1280"

# Classes


class MovieInfo:
    def __init__(self, title, release_date, id, img_url="", description=""):
        super().__init__()
        self.title = title
        self.release_date = release_date
        self.id = id
        self.img_url = img_url
        self.description = description

    def __repr__(self):
        return f"{self.title} - {self.release_date}"

    def year(self):
        if self.release_date:
            return self.release_date[0:4]
        else:
            return ""


def get_movies_by_title(search_text: str) -> list:

    parameters = {
        "api_key": API_KEY_TMDB,
        "language": "en-US",
        "query": search_text,
        "include_adult": False
    }

    response = requests.get(url=URL_SEARCH_MOVIE, params=parameters)
    response.raise_for_status()
    data = response.json()
    result = []

    for movie in data["results"]:
        # pprint(movie)
        # print(movie["id"])
        result.append(MovieInfo(
            title=movie["title"], release_date=movie["release_date"], id=movie["id"]))
    return result


def get_movie_details(movie_id: int) -> MovieInfo:

    parameters = {
        "api_key": API_KEY_TMDB,
        "language": "en-US"
    }
    response = requests.get(
        url=f"{URL_MOVIE_DETAILS}{movie_id}", params=parameters)
    response.raise_for_status()
    data = response.json()
    pprint(data)
    movie_info = MovieInfo(title=data["original_title"],
                           release_date=data["release_date"],
                           id=data["id"],
                           img_url=f"{URL_ROOT_IMAGE}{data['poster_path']}",
                           description=data["overview"])
    return movie_info


if __name__ == "__main__":
    # result = get_movies_by_title("matrix")
    result = get_movie_details(603)
    pprint(result)
