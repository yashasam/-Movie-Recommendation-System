# -*- coding: utf-8 -*-
"""Movie Recommendation System.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OVbqCUYLNffqxR_aaizIvF4QjezUYlgf
"""

import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd
import csv

movies_data = pd.read_csv(
    '/content/movies.csv',
    on_bad_lines='skip',         # Skip problematic lines
    engine='python',             # More tolerant parser
    quoting=csv.QUOTE_NONE,      # Prevents quote-related issues
    encoding='utf-8'
)

print(movies_data.head())

# number of rows and columns in the data frame

movies_data.shape

# selecting the relevant features for recommendation

selected_features = ['genres','keywords','tagline','cast','director']
print(selected_features)

# replacing the null valuess with null string

for feature in selected_features:
  movies_data[feature] = movies_data[feature].fillna('')

# combining all the 5 selected features

combined_features = movies_data['genres']+' '+movies_data['keywords']+' '+movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']

print(combined_features)

# converting the text data to feature vectors

vectorizer = TfidfVectorizer()

feature_vectors = vectorizer.fit_transform(combined_features)

print(feature_vectors)

# getting the similarity scores using cosine similarity

similarity = cosine_similarity(feature_vectors)

print(similarity.shape)

"""Getting the movie name from the user

"""

# getting the movie name from the user

movie_name = input(' Enter your favourite movie name : ')

print(movies_data.columns)
# Drop rows with missing titles just in case
clean_movies_data = movies_data.dropna(subset=['title'])

# Create a list of all movie titles
list_of_all_titles = clean_movies_data['title'].tolist()

# Print first 10 titles
print("First 10 movie titles:", list_of_all_titles[:10])

!gdown --id 1u0V2KX95ZV0fO9o-WsF4MF7KaAtb_J9m  # This downloads tmdb_5000_movies.csv

import pandas as pd

# Load the dataset
movies_data = pd.read_csv('/content/tmdb_5000_credits.csv')
credits_data = pd.read_csv('/content/tmdb_5000_credits.csv')

# Display the first few rows
print("Movies Dataset:")
print(movies_data.head())

print("\nCredits Dataset:")
print(credits_data.head())

# Merge both datasets on 'title'
movies_data = movies_data.merge(credits_data, on='title')

# Check merged dataset shape
print("Merged Data Shape:", movies_data.shape)
movies_data.head()

# STEP 1: Import necessary libraries
import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# STEP 2: Load the datasets
movies_data = pd.read_csv('/content/tmdb_5000_movies.csv')
credits_data = pd.read_csv('/content/tmdb_5000_credits.csv')

# STEP 3: Merge on 'title'
credits_data.rename(columns={'movie_id': 'id'}, inplace=True)
movies_data = movies_data.merge(credits_data, on='id')

# STEP 4: Keep relevant columns
movies = movies_data[['id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# STEP 5: Remove rows with nulls
movies.dropna(inplace=True)

# STEP 6: Data cleaning helper functions
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

def convert_cast(obj):
    L = []
    count = 0
    for i in ast.literal_eval(obj):
        if count < 3:
            L.append(i['name'])
            count += 1
        else:
            break
    return L

def fetch_director(obj):
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            return [i['name']]
    return []

# STEP 7: Apply conversions
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(fetch_director)

# STEP 8: Tokenize overview
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# STEP 9: Create 'tags' feature
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
new_df = movies[['id', 'title', 'tags']]
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())

# STEP 10: Vectorization (ML-based text feature extraction)
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# STEP 11: Compute cosine similarity matrix (Machine Learning)
similarity = cosine_similarity(vectors)

# STEP 12: Define recommendation function
def recommend(movie):
    movie = movie.lower()
    if movie not in new_df['title'].str.lower().values:
        print("❌ Movie not found in the dataset. Try another title.")
        return

    index = new_df[new_df['title'].str.lower() == movie].index[0]
    distances = similarity[index]
    recommended = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    print(f"\n🎬 Top 5 movies similar to '{new_df.iloc[index].title}':\n")
    for i in recommended:
        print(f"👉 {new_df.iloc[i[0]].title}")

# STEP 13: Take user input in Colab
print("🔎 Enter a movie name to get recommendations (e.g., Avatar, The Dark Knight, Iron Man):")
movie_input = input("🎥 Movie Title: ")
recommend(movie_input)

import pandas as pd

# STEP 1: Load both CSV files
movies_data = pd.read_csv('/content/tmdb_5000_movies.csv')
credits_data = pd.read_csv('/content/tmdb_5000_credits.csv')

# STEP 2: Merge on 'id' and 'movie_id'
movies_data.rename(columns={'id': 'movie_id'}, inplace=True)
merged_data = movies_data.merge(credits_data, on='movie_id')

# STEP 3: Keep only the required columns
movies = merged_data[['title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# STEP 4: Drop rows with missing values
movies.dropna(inplace=True)

# Show result
movies.head()

import pandas as pd

# Load the datasets (Make sure both are uploaded in Colab)
movies_data = pd.read_csv('/content/tmdb_5000_movies.csv')
credits_data = pd.read_csv('/content/tmdb_5000_credits.csv')

# Print the columns of each file to verify
print("Movies columns:\n", movies_data.columns)
print("\nCredits columns:\n", credits_data.columns)

# Rename 'id' to 'movie_id' in movies_data to match 'credits_data'
movies_data.rename(columns={'id': 'movie_id'}, inplace=True)

# Merge the datasets on 'movie_id'
merged_data = movies_data.merge(credits_data, on='movie_id')

# Print merged columns
print("Merged columns:\n", merged_data.columns)

"""📌 STEP 4: Parse and Extract Meaningful Features"""

# Now we select only the columns we care about
movies = merged_data[['title_x', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Rename 'title_x' to 'title'
movies.rename(columns={'title_x': 'title'}, inplace=True)

# Drop missing values
movies.dropna(inplace=True)

# Display the final dataset
movies.head()

import ast

# Helper function to parse stringified lists of dictionaries
def convert(text):
    try:
        return [i['name'] for i in ast.literal_eval(text)]
    except:
        return []

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(lambda x: [i['name'] for i in ast.literal_eval(x)][:3])
movies['crew'] = movies['crew'].apply(lambda x: [i['name'] for i in ast.literal_eval(x) if i['job'] == 'Director'])

# Remove spaces in names (important for vectorization later)
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

"""📌 STEP 5: Create a Combined "Tag" Column for Each Movie"""

# Combine overview with genres, cast, crew, keywords
movies['overview'] = movies['overview'].apply(lambda x: x.split())
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# Create final DataFrame with just 'title' and 'tags'
new_df = movies[['title', 'tags']]

# Convert list of tags into a single string
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

new_df.head()

"""📌 STEP 6: Vectorization Using CountVectorizer"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Convert text into feature vectors
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# Compute similarity matrix
similarity = cosine_similarity(vectors)



"""📌 STEP 7: Build a Recommendation Function"""

# Recommendation function
def recommend(movie):
    movie = movie.lower()
    if movie not in new_df['title'].str.lower().values:
        return "Movie not found in the dataset."

    index = new_df[new_df['title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[index]))
    movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = [new_df.iloc[i[0]].title for i in movies_list]
    return recommended_movies

"""📌 STEP 8: Try It! Input a Movie and Get Recommendations"""

# Ask the user for input
movie_input = input("Enter a movie name: ")
recommendations = recommend(movie_input)

# Show the recommendations
print("\nTop 5 Recommended Movies:")
if isinstance(recommendations, list):
    for idx, movie in enumerate(recommendations, 1):
        print(f"{idx}. {movie}")
else:
    print(recommendations)

