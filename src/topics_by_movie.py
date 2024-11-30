import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np

file_path = "articles.csv"
data = pd.read_csv(file_path)

article_topics = [
    "Production and Behind-the-Scenes", "Plot and Themes", "Cast and Crew", 
    "Reception and Reviews", "Marketing and Promotion", "Cultural Impact", 
    "Box Office Performance", "Broader Industry Trends"
]

filtered_data = data[data['Article Topic'].isin(article_topics)]

colors = plt.get_cmap('viridis')(np.linspace(0, 1, len(article_topics)))
color_dict = dict(zip(article_topics, colors))

pivot_percentage = (
    filtered_data.pivot_table(index='Movie', columns='Article Topic', aggfunc='size', fill_value=0)
    .apply(lambda x: x / x.sum() * 100, axis=1)  # Convert counts to percentages
)

ax = pivot_percentage.plot(kind='bar', stacked=True, figsize=(12, 8), color=[color_dict[topic] for topic in article_topics])
plt.title('Percentage of Article Topics by Movie')
plt.xlabel('Movie')
plt.ylabel('Percentage of Articles')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("article_topic_percentage_per_movie.png")

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], title='Article Topic', loc='upper right')

plt.show()

summary_percentage_data = pivot_percentage.to_dict()

with open("article_topic_percentage.json", "w") as json_file:
    json.dump(summary_percentage_data, json_file)
