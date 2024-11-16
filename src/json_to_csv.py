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

            writer.writerow([movie, title, description, url, content, topic])

print(f"Done. Location: {csv_file}")
