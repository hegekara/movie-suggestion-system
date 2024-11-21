import pandas as pd

movies = pd.read_csv('MovieLens20MDataset/movie.csv')
movies = movies[movies['genres'] != "(no genres listed)"]


def test_tur_bulma():
    specified_genres = {
        "Action", "Adventure", "Animation", "Children", "Comedy", "Crime",
        "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "IMAX",
        "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
    }

    all_genres_in_data = set()
    movies['genres'].str.split('|').apply(all_genres_in_data.update)

    extra_genres = all_genres_in_data - specified_genres

    if extra_genres:
        print("Ekstra türler bulundu:", extra_genres)
    else:
        print("Yalnızca belirtilen türler mevcut.")
        
def test_tur_dogruluk():
    csv_df = pd.read_csv("derivatives/movie_genres.csv")
    
    movies['genres'] = movies['genres'].apply(lambda x: set(x.split('|')))
    
    incorrect_movies = []
    for movie_id, group in csv_df.groupby('movieId'):
        csv_genres = set(group['genres'])
        
        movielens_genres = movies.loc[movies['movieId'] == movie_id, 'genres']
        
        if not movielens_genres.empty:
            movielens_genres = movielens_genres.iloc[0]
            if not csv_genres.issubset(movielens_genres):
                incorrect_movies.append((movie_id, csv_genres, movielens_genres))
        else:
            print(f"MovieId {movie_id} MovieLens veri setinde bulunamadı. Türler: {', '.join(csv_genres)}")


test_tur_bulma()
test_tur_dogruluk()