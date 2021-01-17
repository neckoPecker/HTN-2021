import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import webbrowser

headers = {"Accept-Language": "en-US,en;q=0.5"}

titles = []
years = []
time = []
imdb_ratings = []
age_limit = []
genre = []

pages = np.arange(1, 1001, 50)

for page in pages:
    page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&start=" + str(page) + "&ref_=adv_nxt", headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')
    movie_div = soup.find_all('div', class_='lister-item-content')

    for container in movie_div:
        name = container.h3.a.text
        titles.append(name)
            
        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)

        runtime = container.p.find('span', class_='runtime') if container.p.find('span', class_='runtime') else ''
        time.append(runtime)

        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        cert = container.find('span', class_='certificate').text if container.find('span', class_='certificate') else ''
        age_limit.append(cert.strip())

        gen = container.find('span', class_='genre').text if container.find('span', class_='genre') else ''
        genre.append(gen.strip())

movies = pd.DataFrame({
'movie': titles,
'year': years,
'imdb': imdb_ratings,
'timeMin': time,
'age_limit': age_limit,
'genre': genre,
})

movies['timeMin'] = movies['timeMin'].astype(str)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
movies['genre'] = movies['genre'].str.replace(',', '')
movies['age_limit'] = movies['age_limit'].str.replace(',', '')

# to move all your scraped data to a CSV file
movies.to_csv('movies.csv')

webbrowser.open_new_tab('userInterface.html')
