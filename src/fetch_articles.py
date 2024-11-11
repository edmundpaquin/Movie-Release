import requests
import time
import argparse
import json
import os

def fetch_articles(movie_name, director_name, api_key, page_size=20, max_articles=100):
    url = 'https://newsapi.org/v2/everything'
    headers = {'Authorization': f'Bearer {api_key}'}
    articles = []
    page = 1
    
    while len(articles) < max_articles and page <= 5: # limit to 5 pages (5 * 20 = 100 articles)
        params = {
            'q': movie_name,           # movie keyword
            'language': 'en',          # filter by English articles
            'pageSize': page_size,     # nb articles per page
            'page': page               # page nb
        }
        
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        if response.status_code == 200:
            fetched_articles = data.get('articles', [])

            # filter articles to ensure they mention both the movie and director
            relevant_articles = [
                article for article in fetched_articles
                if (article['title'] and movie_name.lower() in article['title'].lower() or movie_name.lower() in (article['description'] or '').lower())
                and (director_name.lower() in (article['title'] or '').lower() or director_name.lower() in (article['description'] or '').lower())
            ]

            articles.extend(relevant_articles)
            print(f"Fetched {len(relevant_articles)} articles for '{movie_name}' on page {page}")
            
            # stop if no more articles available
            if len(fetched_articles) < page_size:
                break
        else:
            print(f"Error fetching articles for '{movie_name}': {data.get('message')}")
            break
        
        # go to next page
        page += 1
        
        # delay to respect API rate limits!
        time.sleep(1)
    
    # trim articles to max_articles if exceeded
    return articles[:max_articles]

# Function to fetch articles for multiple movies
def fetch_articles_for_movies(movie_list, api_key):
    all_articles = {}
    
    for movie, director in movie_list:
        print(f"\nFetching articles for movie: {movie}")
        articles = fetch_articles(movie, director, api_key)
        all_articles[movie] = articles
    
    return all_articles

def save_to_json(data, filename="movies_articles.json"):
    folder = os.path.join("..", "data")
    os.makedirs(folder, exist_ok=True)  # make sure "data" folder exists
    filepath = os.path.join(folder, filename)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch articles for specified movies.")
    parser.add_argument("-key", "--api_key", required=True, help="API key for NewsAPI")

    args = parser.parse_args()
    api_key = args.api_key
    
    # list of movies and directors for which to fetch articles
    movies = [
        #("Blitz", "McQueen"),
        ("Conclave", ""),
        ("Emilia Pérez", ""),
        ("Juror #2", ""),
        ("Gladiator II", ""),
        ("Joker: Folie à Deux", ""),
        #("Wicked", "Chu"), 
        ("Moana 2", ""),
        ("The Apprentice", ""), 
        ("Megalopolis", ""),
        #("Beetlejuice Beetlejuice", ""),
        ("Deadpool & Wolverine", ""),
        #("Dune: Part Two", ""),
        #("Despicable Me 4", ""),
        #("Inside Out 2", ""),
        #("Kung Fu Panda 4", ""),
        #("Twisters", "Chung"),
        #("Godzilla x Kong: The New Empire", ""),
        #("Bad Boys: Ride or Die", ""),
        #("Kingdom of the Planet of the Apes", ""),
        #("The Piano Lesson", ""),
        ("Venom: The Last Dance", "")
    ]
    
    movie_articles = fetch_articles_for_movies(movies, api_key)

    save_to_json(movie_articles)
    
    # Summary :
    for movie, articles in movie_articles.items():
        print(f"\nTotal articles fetched for '{movie}': {len(articles)}")
