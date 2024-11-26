import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

custom_stop_words = {'chars', 's'}
stop_words_combined = list(ENGLISH_STOP_WORDS) + list(custom_stop_words)

# Load the CSV 
filename = 'articles.csv'  
folder = os.path.join("..", "data")
os.makedirs(folder, exist_ok=True)
filepath = os.path.join(folder, filename)
#print(filepath)

data = pd.read_csv(filepath)

#debugging:
#print(data.head())  # Display the first few rows of the DataFrame
#print(data.info())  # Check the structure and presence of columns

# Group articles by the "Article Topic" category
grouped = data.groupby('Article Topic')
#print(grouped.groups.keys())

# Initialize dict
top_words_per_topic = {}

def custom_tokenizer(text):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())  # Keeps only alphabetic words
    return words

for topic, group in grouped:
    #print('test')
    # Combine all content within the topic into a single corpus
    combined_text = " ".join(group['Content'].dropna())
    
    # Compute TF-IDF scores
    vectorizer = TfidfVectorizer(stop_words=stop_words_combined, max_features=1000, tokenizer=custom_tokenizer)
    tfidf_matrix = vectorizer.fit_transform([combined_text])
    
    # Extract feature names and their corresponding scores
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]
    
    # Create a dictionary of words and their scores, sorted by score
    word_scores = {feature_names[i]: scores[i] for i in range(len(feature_names))}
    sorted_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Save the top 10 words for the topic
    top_words_per_topic[topic] = sorted_words

#get rid of the non-categorized stuff
top_words_per_topic.pop('JUNK')
top_words_per_topic.pop('IRRELEVANT')
top_words_per_topic.pop('NOT ENGLISH')

# Display the top words for each topic
for topic, top_words in top_words_per_topic.items():
    print(f"Topic: {topic}")
    for word, score in top_words:
        print(f"  {word}: {score:.4f}")
    print()
