import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

file_path = "articles.csv"
data = pd.read_csv(file_path)

emilia_perez_data = data[data['Movie'] == "Emilia Pérez"]

topic_counts = emilia_perez_data['Article Topic'].value_counts()

total = topic_counts.sum()
percentages = (topic_counts / total * 100).round(2)

json_data = {
    topic: {"count": int(count), "percentage": float(percentages[topic])}
    for topic, count in topic_counts.items()
}

json_file_path = "emilia_perez_article_topics.json"
with open(json_file_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

colors = plt.get_cmap('viridis')(np.linspace(0, 1, len(topic_counts)))

plt.figure(figsize=(10, 10))  
plt.pie(topic_counts, labels=[f'{label}: {percent:.1f}%' for label, percent in percentages.items()],
        autopct='%1.1f%%', startangle=140, colors=colors, pctdistance=0.75) 
plt.title('Distribution of Article Topics for "Emilia Pérez"', fontweight='bold') 
plt.axis('equal')  

plt.savefig("emilia_perez_article_topics.png", bbox_inches='tight') 

plt.show()
