import pandas as pd

# criteria for accepted article topics
accepted_article_topics = [
    "Production and Behind-the-Scenes", "Plot and Themes", "Cast and Crew", 
    "Reception and Reviews", "Marketing and Promotion", "Cultural Impact", 
    "Box Office Performance", "Broader Industry Trends"
]

# Load the data into a DataFrame
file_path = '../data/articles.csv'
data = pd.read_csv(file_path)

# Filter data for accepted and rejected movies
accepted_movies_df = data[data['Article Topic'].isin(accepted_article_topics)]
rejected_movies_df = data[~data['Article Topic'].isin(accepted_article_topics)]

# Count unique movies
accepted_movies_count = accepted_movies_df['Movie'].nunique()
rejected_movies_count = rejected_movies_df['Movie'].nunique()

# Count repetitions of each rejected movie
rejected_movie_repetitions = rejected_movies_df['Movie'].value_counts()

# Count total number of rejected articles
total_rejected_articles = rejected_movies_df.shape[0]

# Display the results
print(f"Number of movies with accepted article topics: {accepted_movies_count}")
print(f"Number of movies with rejected article topics: {rejected_movies_count}")
print(f"Total number of articles related to rejected movies: {total_rejected_articles}")

print("\nRepetition of each accepted movie:")
print(accepted_movies_df['Movie'].value_counts())

print("\nRepetition of each rejected movie:")
print(rejected_movie_repetitions)