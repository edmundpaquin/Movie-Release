import pandas as pd
import json

file_path = "articles.csv"
data = pd.read_csv(file_path)

topic_counts = data['Article Topic'].value_counts()

total_articles = topic_counts.sum()

topic_percentages = {
    topic: {
        "count": int(count),
        "percentage": round((count / total_articles) * 100, 2)
    }
    for topic, count in topic_counts.items()
}

json_file_path = "article_topics_percentages.json"
with open(json_file_path, 'w') as json_file:
    json.dump(topic_percentages, json_file, indent=4)

print(f"Data has been saved to {json_file_path}")
