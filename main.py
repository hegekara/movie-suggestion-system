import tkinter as tk
from tkinter import ttk
import pandas as pd
import ast
import time

root = tk.Tk()


users = pd.read_csv("derivatives/user_id.csv")
user_id = users["userId"].astype(str).tolist()

movie_genres = pd.read_csv("derivatives/movie_genres.csv")
genre_movies_df = movie_genres.groupby('genres')['movieId'].apply(list).reset_index()
genre_list = movie_genres['genres'].unique().tolist()

kisisel_tur_df = pd.read_csv("rules/kisisel_tur_rules.csv")
isim_rule_df  = pd.read_csv("rules/isim_rules.csv")

kisisel_tur_df['antecedents'] = kisisel_tur_df['antecedents'].apply(eval)
kisisel_tur_df['consequents'] = kisisel_tur_df['consequents'].apply(eval)
    
isim_rule_df['antecedents'] = isim_rule_df['antecedents'].apply(eval)
isim_rule_df['consequents'] = isim_rule_df['consequents'].apply(eval)

frequent_itemsets = pd.read_csv("frequent_itemset/9m.csv")
frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(lambda x: eval(x) if isinstance(x, str) else x)


rating_df = pd.read_csv("MovieLens20MDataset/rating.csv")
movies = pd.read_csv('MovieLens20MDataset/movie.csv')

movie_titles = movies["title"].tolist()
    
    
def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()
        
def main_screen_open():
    clear_frame()
    root.title("Film Öneri Uygulaması")
    ekran_genislik = root.winfo_screenwidth()
    ekran_yukseklik = root.winfo_screenheight()

    x = (ekran_genislik // 2) - (900 // 2)
    y = (ekran_yukseklik // 2) - (500 // 2)

    root.geometry(f"{900}x{500}+{x}+{y}")
    
    login_text = tk.Label(root, text="Merhaba, Lütfen Yapmak İstediğiniz İşlemi Seçin!")
    login_text.pack(pady = 30)

    frame = tk.Frame(root)
    frame.pack(padx=50, pady=30)

    birliktelik_button = tk.Button(frame, text="Birliktelik Kurallarına Göre", command=birliktelik_kurali_window_open)
    birliktelik_button.pack(side=tk.LEFT, padx=10)
    specified_button = tk.Button(frame, text="Kişiselleştirilmiş Öneriler", command=kisisellestirilmis_window_open)
    specified_button.pack(side=tk.RIGHT, padx=10)

    quit_button = tk.Button(root, text = "Kapat", command=root.quit)
    quit_button.pack()

    root.mainloop()

def birliktelik_kurali_window_open():
    clear_frame()
    birliktelik_text =  tk.Label(root, text="Birliktelik Kurallarına Göre\n"
                                 "Lütfen Yapmak İstediğiniz İşlemi Seçin")
    birliktelik_text.pack()
    
    frame = tk.Frame(root)
    frame.pack(padx=50, pady = 30)
    
    film_turune_gore_button = tk.Button(frame, text = "Film Türüne Göre", command=birliktelik_tur_window_open)
    film_turune_gore_button.pack(side=tk.LEFT, padx=10)
    
    film_ismine_gore_button = tk.Button(frame, text = "Film İsmine Göre", command=birliktelik_isim_window_open)
    film_ismine_gore_button.pack(side = tk.RIGHT, padx=10)
    
    back_button = tk.Button(root, text="Geri", command=main_screen_open)
    back_button.pack()
    
def kisisellestirilmis_window_open():
    clear_frame()
    
    kisisellestirilmis_text = tk.Label(root, text="Kişiselleştirilmiş Öneriler\n"
                                 "Lütfen Yapmak İstediğiniz İşlemi Seçin")
    kisisellestirilmis_text.pack()
    
    frame = tk.Frame(root)
    frame.pack(padx=50, pady=30)
    
    film_turune_gore_button = tk.Button(frame, text = "Film Türüne Göre", command=kisisel_tur_window_open)
    film_turune_gore_button.pack(side=tk.LEFT, padx=10)
    
    film_ismine_gore_button = tk.Button(frame, text = "Film İsmine Göre", command=kisisel_isim_window_open)
    film_ismine_gore_button.pack(side = tk.RIGHT, padx=10)
    
    back_button = tk.Button(root, text="Geri", command=main_screen_open)
    back_button.pack()
    
def birliktelik_tur_window_open():
    clear_frame()
    
    tur_secenek = ttk.Combobox(root, values=genre_list, state="readonly")
    tur_secenek.pack(pady=10)

    result_button = tk.Button(root, text="Sonuç Getir", command=lambda: birliktelik_tur_hesapla(tur_secenek, output_text))
    result_button.pack(pady=10)

    output_text = tk.Text(root, height=20, width=60)
    output_text.pack(pady=10)
    output_text.config(state="disabled")

    back_button = tk.Button(root, text="Geri", command=birliktelik_kurali_window_open)
    back_button.pack()
    
def birliktelik_isim_window_open():
    clear_frame()
    
    isim_secenek = ttk.Combobox(root, values=movie_titles, width=35)
    isim_secenek.pack(pady=20)
    
    output_text = tk.Text(root, height=20, width=60)
    
    button = tk.Button(root, text="Sonuç Getir", command= lambda: birliktelik_isim_hesapla(isim_secenek, output_text))
    button.pack()
    
    output_text.pack(pady=10)
    output_text.config(state="disabled")
    
    back_button = tk.Button(root, text="Geri", command= birliktelik_kurali_window_open)
    back_button.pack()
    
def kisisel_tur_window_open():
    clear_frame()

    user_secenek = ttk.Combobox(root, values=user_id, state="readonly")
    user_secenek.pack(pady=10)

    tur_secenek = ttk.Combobox(root, values=genre_list, state="readonly")
    tur_secenek.pack(pady=10)

    result_button = tk.Button(root, text="Sonuç Getir", command=lambda: kisisellestirilmis_tur_hesapla(user_secenek, tur_secenek, output_text))
    result_button.pack(pady=10)

    output_text = tk.Text(root, height=20, width=60)
    output_text.pack(pady=10)
    output_text.config(state="disabled")

    back_button = tk.Button(root, text="Geri", command=kisisellestirilmis_window_open)
    back_button.pack()

def kisisel_isim_window_open():
    clear_frame()

    user_secenek = ttk.Combobox(root, values=user_id, state="readonly")
    user_secenek.pack(pady=10)

    result_button = tk.Button(root, text="Sonuç Getir", command=lambda: kisisellestirilmis_isim_hesapla(user_secenek, output_text))
    result_button.pack(pady=10)

    output_text = tk.Text(root, height=20, width=60)
    output_text.pack(pady=10)
    output_text.config(state="disabled")

    back_button = tk.Button(root, text="Geri", command=kisisellestirilmis_window_open)
    back_button.pack()

def birliktelik_tur_hesapla(tur_secenek, output_text):
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)

    try:
        start = time.time()
        genre = tur_secenek.get()
        genre_movies = movies[movies['genres'].str.contains(genre)]
        genre_movie_ids = genre_movies['movieId']
        
        genre_movie_ids_set = set(genre_movie_ids.values)

        single_movie_popularity = frequent_itemsets.explode('itemsets')
        single_movie_popularity = single_movie_popularity[single_movie_popularity['itemsets'].isin(genre_movie_ids_set)]
        
        single_movie_popularity = single_movie_popularity.groupby('itemsets')['support'].max().reset_index()
        single_movie_popularity.columns = ['movieId', 'support']
        top_movies = single_movie_popularity.nlargest(10, 'support')

        recommendations = movies[movies['movieId'].isin(top_movies['movieId'])]['title'].tolist()
        print("birliktelik tur:")
        print(time.time()- start)

        if recommendations:
            output_text.insert(tk.END, "Önerilen Filmler: \n" + '\n'.join(recommendations))
        else:
            output_text.insert(tk.END, "Öneri yok. Lütfen başka bir tür seçin.")
        
        output_text.config(state="disabled")

    except Exception as e:
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Hata: {e}")
        output_text.config(state="disabled")

def birliktelik_isim_hesapla(isim_secenek, output_text):
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)

    try:
        start = time.time()
        selected_movie = isim_secenek.get()
        selected_movie_id = movies[movies['title'] == selected_movie]['movieId'].values[0]

        def get_recommendations(rules, movie_ids, max_recommendations=15):
            recommendations = []

            antecedent_lengths = rules['antecedents'].apply(len)
            
            for length in sorted(antecedent_lengths.unique()):
                filtered_rules = rules[antecedent_lengths == length]
                filtered_recommendations = set()

                for _, row in filtered_rules.iterrows():
                    antecedents = set(row['antecedents'])
                    consequents = set(row['consequents'])

                    if antecedents.issubset(movie_ids):
                        filtered_recommendations.update(consequents)

                recommendations.extend(filtered_recommendations)
                if len(recommendations) >= max_recommendations:
                    recommendations = recommendations[:max_recommendations]
                    break

            return recommendations
        
        
        recommendations = get_recommendations(isim_rule_df, [int(selected_movie_id)])
        recommended_movie_names = movies[movies['movieId'].isin(recommendations)]['title'].tolist()

        print(time.time()-start)
        if recommendations:
            output_text.insert(tk.END, "Önerilen Filmler: \n" + '\n'.join(map(str, recommended_movie_names)))
        else:
            output_text.insert(tk.END, "Öneri yok. Lütfen başka bir tür seçin.")
        
        output_text.config(state="disabled")

    except Exception as e:
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Hata: {e}")
        output_text.config(state="disabled")

def kisisellestirilmis_tur_hesapla(user_secenek, tur_secenek, output_text):
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)

    try:
        selected_user_id = int(user_secenek.get())
        selected_genre = tur_secenek.get()
        
        user_movies = rating_df[rating_df['userId'] == selected_user_id]['movieId'].tolist()

        
        def filter_rules(antecedents, consequents):
            movie_match = all(item in user_movies for item in antecedents)
            genre_match = all(
                selected_genre in movie_genres[movie_genres['movieId'] == item]['genres'].values
                for item in consequents
            )
            return movie_match and genre_match

        recommended_movies = kisisel_tur_df[kisisel_tur_df.apply(lambda row: filter_rules(row['antecedents'], row['consequents']), axis=1)]
        recommended_movies = recommended_movies.sort_values('lift', ascending=False)

        recommendations = set()
        for consequent in recommended_movies['consequents']:
            recommendations.update(movie for movie in consequent if movie not in user_movies)
        
        recommended_movie_names = movies[movies['movieId'].isin(recommendations)]['title'].tolist()


        if recommendations:
            output_text.insert(tk.END, "Önerilen Filmler: \n" + '\n'.join(map(str, recommended_movie_names)))
        else:
            output_text.insert(tk.END, "Öneri yok. Lütfen başka bir tür seçin.")
        
        output_text.config(state="disabled")

    except Exception as e:
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Hata: {e}")
        output_text.config(state="disabled")

def kisisellestirilmis_isim_hesapla(user_secenek, output_text):
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)

    try:
        selected_user_id = int(user_secenek.get())
        
        user_movies = rating_df[rating_df['userId'] == selected_user_id]['movieId'].tolist()

        def get_recommendations(rules, movie_ids, max_recommendations=15):
            recommendations = []

            antecedent_lengths = rules['antecedents'].apply(len)
            
            for length in sorted(antecedent_lengths.unique()):

                filtered_rules = rules[antecedent_lengths == length]
                filtered_recommendations = set()

                for _, row in filtered_rules.iterrows():
                    antecedents = set(row['antecedents'])
                    consequents = set(row['consequents'])
                    
                    if antecedents.issubset(movie_ids):
                        filtered_recommendations.update(consequents)

                recommendations.extend(filtered_recommendations)
                if len(recommendations) >= max_recommendations:
                    recommendations = recommendations[:max_recommendations]
                    break

            return recommendations
        
        
        recommendations = get_recommendations(isim_rule_df, user_movies)
        recommended_movie_names = movies[movies['movieId'].isin(recommendations)]['title'].tolist()

        if recommendations:
            output_text.insert(tk.END, "Önerilen Filmler: \n" + '\n'.join(map(str, recommended_movie_names)))
        else:
            output_text.insert(tk.END, "Öneri yok. Lütfen başka bir tür seçin.")
        
        output_text.config(state="disabled")

    except Exception as e:
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Hata: {e}")
        output_text.config(state="disabled")

    
main_screen_open()