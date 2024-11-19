import json
import csv
import os


data_folder = "../data"
json_file = os.path.join(data_folder, "movies_articles.json")
csv_file = os.path.join(data_folder, "articles.csv")

# Read the JSON
with open(json_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Here is where we can/update our header names
headers = ["Movie", "Article Title", "Description", "URL", "Content", "Article Topic"]

# Set to track unique articles (using URL as a unique identifier!)
seen_articles = set()
duplicate_count = 0

# Write to csv
with open(csv_file, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)

    
    for movie, articles in data.items():
        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")
            url = article.get("url", "")
            content = article.get("content", "").split("\n")[0]  # Take the start of the content
            topic = ""  # THIS IS where we manually write our label so left empty

            # Check if the article is already in the set
            if url not in seen_articles:
                # Add the article to the CSV and mark it as seen
                writer.writerow([movie, title, description, url, content, topic])
                seen_articles.add(url)
            else:
                # Increment the duplicate count if the article has already been seen
                duplicate_count += 1

print(f"Done. Location: {csv_file}")
print(f"Total duplicates found: {duplicate_count}")
