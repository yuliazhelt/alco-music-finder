# alco-music-finder

Веб-приложение, основанное на Flask, в котором пользователь авторизируется через Spotify. Данные пользователя, а именно его сохраненные треки, собираются и обрабатываются. Обработка заключается в подсчете количества треков каждого исполнителя, а на основании этого определяется популярность различных музыкальных жанров у пользователя. Учитывая популярности музыкальных жанров, подбираются подходящие алкогольные базы в рецептах коктейлей, откуда рандомным образом пользователю выдаются конкретные коктейли с изображениями и ссылками на веб-страницу с описанием и рецептом. База алкогольных коктейлей получена веб-скрейпингом сайта ru.inshaker.com с помощью BeautifulSoup и представлена объектом DataFrame.

Запустить локально:
```
python main.py
```

A web application based on Flask, in which the user logs in via Spotify. The user's data, namely his saved tracks, are collected and processed. Processing consists in counting the number of tracks of each artist, and based on this, the popularity of different musical genres among user's tracks is determined. Using the popularity of musical genres, suitable alcoholic bases are selected in cocktail recipes. According to this information the user is randomly given specific cocktails with images and links to a web page with a description and recipe. The base of alcoholic cocktails was obtained by web scraping ru.inshaker.com using BeautifulSoup and is represented by a DataFrame object.

Run locally:
"'
python main.py
``
