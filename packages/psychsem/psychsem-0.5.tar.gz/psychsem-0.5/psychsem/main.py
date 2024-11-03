def psych10():
    print("Psych thats a wrong number...again...dammm")

def WMSPAM():
    print('''
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
emails = [ "Buy cheap watches! Free shipping!",
          "Meeting for lunch today?",
           "Claim your prize! You've won $1,000,000!",
           "Important meeting at 3 PM.",
]
Labels = [1, 0, 1, 0]
print(emails)
max_words = 1000
max_len = 50
tokenizer = Tokenizer(num_words=max_words, oov_token="<00V>")
tokenizer.fit_on_texts(emails)
sequences = tokenizer.texts_to_sequences(emails)
x_padded = pad_sequences(sequences, maxlen=max_len, padding='post', truncating="post")
print(x_padded)
print(sequences)
model=tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=max_words, output_dim=16, input_length=max_len),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(6, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
training_data = np.array(x_padded)
training_labels = np.array(Labels)
model.fit(training_data, training_labels, epochs=50)
file_path = "/content/NSpam.txt"
with open(file_path, "r", encoding="utf-8") as file:
  sample_email_text =file.read()
sequences_sample=tokenizer.texts_to_sequences ([sample_email_text])
sample_email_padded=pad_sequences (sequences_sample, maxlen=max_len, padding="post", truncating="post")
prediction= model.predict(sample_email_padded)
threshold = 0.5
if prediction > threshold: 
  print(f"Sample Email ('{file_path}'): The Email is SPAM") 
else:
   print(f"Sample Email ('{file_path}'): NOT SPAM")''')
    

def WMAPALGO():
    print('''
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import pandas as pd
# sample Transaction
dataset= [
    ['milk','bread','nuts'],
    ['milk','bread'],
    ['milk','eggs','nuts'],
    ['milk','bread','eggs'],
    ['bread','nuts'],
    ]
# convert the dataset to pandas dataframe
df=pd.DataFrame(dataset)
print("\n Transaction database:")
print(df)
# coverting items to column
df_encoded=pd.get_dummies(df,prefix='',prefix_sep='')
print("\n Transaction encoded:")
print(df_encoded)
#Find frequent 
frequent_itemsets=apriori(df_encoded,min_support=0.5,use_colnames=True)
print("\n Frequent itemsets:")
print(frequent_itemsets)
#Generate association rules
rules=association_rules(frequent_itemsets,metric='confidence',min_threshold=0.5)
print("\n Association rules:")
print(rules)''')
    

def WMKEYCRAWL():
    print('''
import requests
from bs4 import BeautifulSoup 
import re
def crawl_and_search(url,keyword):
    try:
        response = requests.get(url)
        response.raise_for_status()
        page_content = response.text

        soup = BeautifulSoup(page_content,'html.parser')
        text = soup.get_text()
        if re.search(keyword,text,re.IGNORECASE):
            print(f"keyowrd'{keyword}'found in {url}")
        else:
            print(f"keyowrd'{keyword}'not found in {url}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}:{e}")
url=input("Enter the url to crawl")
keyword=input("Enter the keyword")

crawl_and_search(url,keyword)
''')
    
def WMSENTI():
    print('''
#Sentiment analysis for reviews by customers and visualize the same.
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

# Download VADER lexicon 
nltk.download('vader_lexicon')
# Step 2: Initialize the VADER sentiment intensity analyzer
sia = SentimentIntensityAnalyzer()
# customer reviews
reviews = [
    "The product quality is amazing, I'm very satisfied!",
    "Terrible service, I will never buy from here again.",
    "Decent product, but shipping was too slow.",
    "Absolutely love it! Will recommend to everyone.",
    "Not worth the money, very disappointing.",
    "Great experience overall, but could improve the packaging.",
    "Mediocre, not what I expected.",
    "Excellent value for the price, highly recommended.",
    "Worst purchase I've made this year.",
    "It's okay, nothing special."
]
#Analyze sentiment 
sentiments = []
for review in reviews:
    sentiment_score = sia.polarity_scores(review)
    compound_score = sentiment_score['compound']
    if compound_score >= 0.05:
        sentiments.append('Positive')
    elif compound_score <= -0.05:
        sentiments.append('Negative')
    else: sentiments.append('Neutral')
# Count the occurrences
sentiment_counts = {
    'Positive': sentiments.count('Positive'),
     'Negative': sentiments.count('Negative'),
    'Neutral': sentiments.count('Neutral')
}

#Visualization
sns.set(style="whitegrid")
plt.figure(figsize=(8, 6))
sns.barplot(x=list(sentiment_counts.keys()), y=list(sentiment_counts.values()),
            palette="viridis")
plt.title('Sentiment Analysis of Customer Reviews')
plt.xlabel('Sentiment')
plt.ylabel('Number of Reviews')
plt.show()
''')

def WMRANK():
    print('''
import networkx as nx
G=nx.random_k_out_graph(n=8,k=2,alpha=0.75)
def draw_grapd(G):
  nx.draw(G, with_labels=True, font_weight='bold',node_size=400)
draw_grapd(G)
ranks_pr=nx.pagerank(G)
print("PageRank:")
print(ranks_pr)
''')

def WMSMSCRAPE():
    print('''
import  requests
from bs4 import BeautifulSoup
def check_word_in_webpage(url,word):
    response=requests.get(url)
    if response.status_code==200:
        soup=BeautifulSoup(response.content,'html.parser')
        text_content=soup.get_text()
        if word.lower() in text_content.lower():
            print(f"The word '{word}' is present in the webpage")
        else:
            print(f"The word '{word}' is not present in the webpage")
    else:
        print("Failed to retrieve webpage")
url=input("Enter the url")
word_to_check=input("Enter the word")
check_word_in_webpage(url,word_to_check)
''')
    


def WMINDEX():
    print('''
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import re

#Seed URLs
seed_urls = ['https://indianexpress.com/section/india/', 'https://www.indianretailer.com/restaurant/']
#Keywords to focus on
nltk.download('stopwords')
nltk.download('punkt_tab')
keywords = ['restaurant', 'food', 'local']
# Stop words to filter out common words)
stop_words = set(stopwords.words('english'))

# Visited URLs
visited = set()
def is_relevant(content, keywords):
    #Check if the content is relevant based on the keywords.
    words = word_tokenize(content.lower())
    words = [w for w in words if w.isalnum() and w not in stop_words]
    return any(keyword in words for keyword in keywords)
def crawl(url):
    #Crawl a single webpage.
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
#Check if the content is relevant
        if is_relevant(text, keywords):
            print(f"Relevant content found at: {url}")
            # Here you could save the content to a file or database
# Extract links and follow them
            for link in soup.find_all('a', href=True):
                new_url = urljoin(url, link['href'])
                if new_url not in visited and re.match(r'^https?://', new_url):
                    visited.add(new_url)
                    crawl(new_url)
    except requests.exceptions.RequestException as e:
        print(f"Error crawling {url}: {e}")
# Start crawling from the seed URLs
for url in seed_urls:
    if url not in visited:
        visited.add(url)
        print(crawl(url))
''')
    
def WMFOCUS():
    print('''
#User defined keyword webcrawling- Reddit Subs
import praw
import pandas as pd
reddit = praw.Reddit(client_id='OsKSXBsx11IS_8vpiTMFOQ', client_secret='pYz21tr_tNl074KFKhVlH9n-QxVOMQ', user_agent='psych_webcrawller')
sub_name = input("enter the Keyword")
max_posts = 5
# Enable read-only mode
reddit.read_only = True
title=[]
for submission in reddit.subreddit(sub_name).new(limit=max_posts):
    title.append(submission.title)
print(title)
''')