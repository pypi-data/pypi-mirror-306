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
    
def DSCLRMAP():
    print('''
#import lib
import matplotlib.pyplot as plt
import numpy as np
for i in plt.colormaps():
    title =" color map : " +i
    fig=plt.figure(figsize=(10,10))
    plt.title(title)
    imgplot= plt.imshow(np.random.rand(10,10))
    imgplot.set_cmap(i)
    plt.show()
''')

def DSGPMAP():
    print('''
import geopandas as gpd
import matplotlib.pyplot as plt
import fiona
from shapely.geometry import Point
#fiona support read and write permission for ERSI shapefile
fiona.drvsupport.supported_drivers['ERSI shapefile']='rw'
with fiona.Env(SHAPE_RESTORE_SHX='YES'):
    #importing data
    india_gpf=gpd.read_file("")
#plot fig
fig,ax=plt.subplots(1,1,figsize=(10,10))
#plot indian map
india_gpf.plot(ax=ax,color='white',edgecolor='black')
#marking mumbai location
mumbai=gpd.GeoDataFrame([{'City':'Mumbai','geometry':Point(72.88261000,19.07283000)}],crs='EPSG:4326')
#assigning name
mumbai.plot(ax=ax,color='red')
for x,y,label in zip (mumbai.geometry.x,mumbai.geometry.y,mumbai['City']):
    ax.text(x,y,label)
#marking kolkata location
kolkata=gpd.GeoDataFrame([{'City':'Kolkata','geometry':Point(88.33777778,22.54111111)}],crs='EPSG:4326')
#assigning name
kolkata.plot(ax=ax,color='green')
for x,y,label in zip (kolkata.geometry.x,kolkata.geometry.y,kolkata['City']):
    ax.text(x,y,label)
#plotting a line between two states
plt.plot([72.88261000,88.33777778],[19.07283000,22.54111111], linestyle='dotted', marker='o')
plt.title(' Indian states map')
plt.show()
''')


def DSFOLMAP():
    print('''
import folium
#zooms to india longitude and latitude
map=folium.Map(location=[20.5937,78.9629],zoom_start=5)
#marking cities
cities=[
    {"name":"New Delhi","location":[28.70405920,77.10249020],"population":"16.79 million"},
    {"name":"Mumbai","location":[19.07283000,72.88261000],"population":"16.79 million"},
    {"name":"Kolkata","location":[22.54111111,88.33777778],"population":"4.50 million"} 
]
#iteration to add cities in map
for city in cities:       folium.Marker(location=city['location'],popup=f"<b>{city['name']}</b><br>Population:{city['population']}",tooltip=city['name']).add_to(map)
map.save('india_map.html')
map
''')


def DSMOON():
    print('''
from astropy.coordinates import solar_system_ephemeris,get_moon,AltAz,EarthLocation
import astropy.units as u
from astropy.time import Time
import matplotlib.pyplot as plt
#sets the ephemeris (a table of values that gives the positions of astronomical objects) to the built-in data provided by astropy.
solar_system_ephemeris.set('builtin')
#CUURENT TIME
time_utc=Time.now()
# position of the Moon at the current time.
moon=get_moon(time_utc)
#sets the observation location to Kitt Peak, an astronomical observatory in Arizona, USA.
location=EarthLocation.of_site('Kitt Peak')
#transforms the Moon's coordinates to the Altitude-Azimuth (AltAz) coordinate system
moon_altaz=moon.transform_to(AltAz(obstime=time_utc,location=location))

#RA (right ascension) and Dec (declination) are coordinates on the sky that correspond to longitude and latitude on Earth
print(f'moon Cordinates(RA,DEC):{moon.ra},{moon.dec}')

#horizontal coordinate system, also known as the Alt/Az system, 
#is a method for describing the exact position of objects in the sky, such as planets, the Sun, or the Moon.
print(f'Moon Altitude:{moon_altaz.alt}')
print(f'Moon Azimuth:{moon_altaz.az}')

#define figsize
plt.figure(figsize=(10,8))
#define polar projection
plt.subplot(111,projection='polar')
plt.title('Moon Position')
plt.polar(moon.ra.radian,moon.dec.radian,'o',markersize=10)
plt.show()
''')


def DSPLOTLY():
    print('''
import pandas as pd
import plotly.express as px
URL="https://covid.ourworldindata.org/data/owid-covid-data.csv"
df=pd.read_csv(URL)
country='India'
df_country=df[df['location']==country]
df_country=df_country[['date','new_cases']]
fig=px.line(df_country,x='date',y='new_cases',title=f'Corona Cases in {country} overtime')
fig.show()
''')
  
def DSLINREG():
    print('''
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

# Load the diabetes dataset
diabetes = datasets.load_diabetes()

# Use only one feature
diabetes_X = diabetes.data[:, np.newaxis, 2]

# Split the data into training/testing sets
diabetes_X_train = diabetes_X[:-30]
diabetes_X_test = diabetes_X[-50:]

# Split the targets into training/testing sets
diabetes_y_train = diabetes.target[:-30]
diabetes_y_test = diabetes.target[-50:]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)

# Make predictions using the testing set
diabetes_y_pred = regr.predict(diabetes_X_test)
# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(diabetes_y_test, diabetes_y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(diabetes_y_test, diabetes_y_pred))

# Plot outputs
plt.scatter(diabetes_X_test, diabetes_y_test,  color='blue')
plt.plot(diabetes_X_test, diabetes_y_pred, color='red', linewidth=2)

plt.xticks(())
plt.yticks(())

plt.axis('tight')
plt.title("Diabetes")
plt.xlabel("BMI")
plt.ylabel("Age")
plt.show()
''')
 

def DSWRDCLD():
    print('''
import matplotlib.pyplot as plt
from wordcloud import WordCloud 
text ="Creating random text that could be used for hacking purposes is unethical and potentially harmful."
wordcloud=WordCloud().generate(text)
plt.figure(figsize=(12,12))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
''')
    
def DSIMG2VID():
    print('''
import os
import shutil
import cv2
#input Location
sInputFieName =
#Output Location
sDataBaseDir=
if os.path.exists(sDataBaseDir):
    shutil.rmtree(sDataBaseDir)
if not os.path.exists(sDataBaseDir):
    os.makedirs(sDataBaseDir)
print('+++++++++++++++++++++++++++++')
print('start movie to frames')
print('+++++++++++++++++++++++++++++')
vidcap=cv2.VideoCapture(sInputFieName)
success,image=vidcap.read()
count=0
while success:
    success,image=vidcap.read()
    sFrame=sDataBaseDir+str('/pic-frame-'+str(format(count,'04d'))+'.jpg')
    print('Extracted',sFrame)
    cv2.imwrite(sFrame,image)
    if os.path.getsize(sFrame)==0:
        count+=-1
        os.remove(sFrame)
        print('removded',sFrame)
    if cv2.waitKey(10)==27:
        break
    if count > 5000:
        break
    count+=1
print('Generated',count,'Frame')
''')

def DSVID2IMG():
    print('''
import cv2
import numpy as np
import glob
 
img_array = []
for filename in glob.glob(Input File location):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)
 
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
''')
    
def DSPYMONGO():
    print('''
#import library
import pymongo
#creating connection to mongo
#verify if mongod.exe is working in task manger
#if not start it from mongoDB bin folder
myclient= pymongo.MongoClient("mongodb://localhost:27017/")
#create DB
mydb=myclient["KC_DATA"]
print("DB Created")
#create collection it is nothing but a table
mycol=mydb["Part2"]
#check DBs
print(myclient.list_database_names())
#check collection
print(mydb.list_collection_names())
#create document
mydictionary=[
    {"name":"YO","address":"YOYO"},
    {"name":"mirchi","address":"khet"}
          	]
#insert document
x=mycol.insert_many(mydictionary)
''')
    
def DSAUD2CSV():
    print('''
# Utility Start Audio to HORUS ===============================
# Standard Tools
#=============================================================
from scipy.io import wavfile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#=============================================================
def show_info(aname, a,r):
    print ('----------------')
    print ("Audio:", aname)
    print ('----------------')
    print ("Rate:", r)
    print ('----------------')
    print ("shape:", a.shape)
    print ("dtype:", a.dtype)
    print ("min, max:", a.min(), a.max())
    print ('----------------')
    plot_info(aname, a,r)
#=============================================================
def plot_info(aname, a,r):        
    sTitle= 'Signal Wave - '+ aname + ' at ' + str(r) + 'hz'
    plt.title(sTitle)
    sLegend=[]
    for c in range(a.shape[1]):
        sLabel = 'Ch' + str(c+1)
        sLegend=sLegend+[str(c+1)]
        plt.plot(a[:,c], label=sLabel)
    plt.legend(sLegend)
    plt.show()
#=============================================================
#input wav
sInputFileName=
print('=====================================================')
print('Processing : ', sInputFileName)
print('=====================================================')
InputRate, InputData = wavfile.read(sInputFileName)
show_info("4 channel", InputData,InputRate)
ProcessData=pd.DataFrame(InputData)
sColumns= ['Ch1','Ch2''Ch3','Ch4']
ProcessData.columns=sColumns
OutputData=ProcessData
#outputfile csv
sOutputFileName=
OutputData.to_csv(sOutputFileName, index = False)

print('=====================================================')
print('Audio to HORUS - Done')
print('=====================================================')
#=============================================================
# Utility done ===============================================
#=============================================================
''')
    
def DSIMG2CSV():
    print('''from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def image_to_csv_and_show(image_path, csv_output_path):
    # Open and convert image to RGB
    img = Image.open(image_path).convert('RGB')
    # Convert image to NumPy array
    img_array = np.array(img)
    # Print image info
    print(f"Image Path: {image_path}")
    print(f"Shape: {img_array.shape}")
    print(f"Dtype: {img_array.dtype}")
    print(f"Min, Max: {img_array.min()}, {img_array.max()}")
    # Reshape array to 2D (rows of pixel values) and convert to DataFrame
    df = pd.DataFrame(img_array.reshape(-1, 3), columns=['R', 'G', 'B'])
    # Save DataFrame to CSV
    df.to_csv(csv_output_path, index=False, header=False)  # Avoid header and index
    # Show the image
    plt.imshow(img_array)
    plt.title('Image Preview')
    plt.axis('off')  # Hide axis
    plt.show()
def visualize_csv(csv_path, image_shape):
    df = pd.read_csv(csv_path, header=None, names=['R', 'G', 'B'])

    # Reshape DataFrame to image shape (height, width, 3)
    img_array = df.values.reshape(image_shape)
    # Plot a horizontal strip of the image (e.g., the middle row) for each channel
    mid_row = img_array.shape[0] // 2
    plt.figure(figsize=(15, 5))
    # Plot Red channel
    plt.subplot(3, 1, 1)
    plt.plot(img_array[mid_row, :, 0], color='red')
    plt.title('Red Channel Pixel Values')

    # Plot Green channel
    plt.subplot(3, 1, 2)
    plt.plot(img_array[mid_row, :, 1], color='green')
    plt.title('Green Channel Pixel Values')
    # Plot Blue channel
    plt.subplot(3, 1, 3)
    plt.plot(img_array[mid_row, :, 2], color='blue')
    plt.title('Blue Channel Pixel Values')

    plt.tight_layout()
    plt.show()
# Define file paths
#input image location
image_path = 
#output location     
csv_output_path =   
# Get image array and shape
img_array = np.array(Image.open(image_path).convert('RGB'))
shape = img_array.shape
# Process image and save as CSV
image_to_csv_and_show(image_path, csv_output_path)

# Visualize data from CSV
visualize_csv(csv_output_path, shape)
''')
    
def DSBINLOC():
    print('''
#Binning
import pandas as pd
ages=[18,23,22,25,46,34,45,87]
bins=[0,25,50,75,100]
bin_labels=["Young","Middle Aged","Senior","Elderly"]
age_bins=pd.cut(ages,bins=bins,labels=bin_labels)
print(age_bins)
#Location Average
import pandas as pd
import numpy as np

LatitudeData=pd.Series(np.array(range(-90,91,1)))
LongitudeData=pd.Series(np.array(range(-180,181,1)))

LatitudeSet=LatitudeData.sample(10)
LongitudeSet=LongitudeData.sample(10)

LatitudeAverage=np.average(LatitudeSet)
LongitudeAverage=np.average(LongitudeSet)

print("LatitudeSet:\n",LatitudeSet,"\n")
print("LongitudeSet:\n",LongitudeSet,"\n")
print("LatitudeAverage:",LatitudeAverage)
print("LongitudeAverage:",LongitudeAverage)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Generate random latitude and longitude points within India
LatitudeData = pd.Series(np.array(range(8, 38, 1)))  # Latitude range for India
LongitudeData = pd.Series(np.array(range(68, 98, 1)))  # Longitude range for India
LatitudeSet = LatitudeData.sample(10)
LongitudeSet = LongitudeData.sample(10)
LatitudeAverage = np.average(LatitudeSet)
LongitudeAverage = np.average(LongitudeSet)

print('Latitude')
print(LatitudeSet)
print('Latitude (Avg):', LatitudeAverage)
print('##############')
print('Longitude')
print(LongitudeSet)
print('Longitude (Avg):', LongitudeAverage)

# Plotting on an India map
plt.figure(figsize=(8, 8))

# Set India-specific boundaries for Basemap
map = Basemap(projection='mill', llcrnrlat=8, urcrnrlat=38,
              llcrnrlon=68, urcrnrlon=98, resolution='c')

map.drawcoastlines()
map.drawcountries()
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='lightgreen', lake_color='aqua')

# Convert latitude and longitude to map projection coordinates
x, y = map(LongitudeSet.values, LatitudeSet.values)

# Plot the sampled points
map.scatter(x, y, marker='o', color='red', s=100, label='Sampled Points')

# Plot the average point
avg_x, avg_y = map(LongitudeAverage, LatitudeAverage)
map.scatter(avg_x, avg_y, marker='X', color='blue', s=200, label='Average Point')

# Add title and legend
plt.title('Randomly Sampled Latitude and Longitude Points on India Map')
plt.legend()

plt.show()
''')