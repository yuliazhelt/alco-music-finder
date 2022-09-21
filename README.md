# alco-music-finder

A web application based on Flask, in which the user logs in via Spotify. The user's data, namely his saved tracks, are collected and processed. Processing consists in counting the number of tracks of each artist, and based on this, the popularity of different musical genres among user's tracks is determined. Using the popularity of musical genres, suitable alcoholic bases are selected in cocktail recipes. According to this information the user is randomly given specific cocktails with images and links to a web page with a description and recipe. The base of alcoholic cocktails was obtained by web scraping ru.inshaker.com using BeautifulSoup and is represented by a DataFrame object.

Run locally:
```
python main.py
```
