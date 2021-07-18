from bs4 import BeautifulSoup
import requests
import pandas as pd

drinks_names = []
drinks_bases = []  # базы в рецепте коктейля
drinks_urls = []
drinks_imgs = []

# на данном сайте каждая следующая страница содержит все результаты предыдущей, поэтому рассматриваем  последнюю страницу, содержащую все результаты
url = f'https://ru.inshaker.com/cocktails?random_page=59'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
drinks_soups = soup('div', 'cocktail-item')
for drinks_soup in drinks_soups:
    drink_name = drinks_soup('div', 'cocktail-item-name')[0].text.replace('\xa0', ' ').replace('\xad', ' ')
    drink_url = f'https://ru.inshaker.com{drinks_soup.a["href"]}'
    drink_img = drinks_soup.img["src"]
    drinks_names.append(drink_name)
    drinks_urls.append(drink_url)
    drinks_imgs.append(drink_img)

# записываем все варианты в фильтре по базе
html_blocks = soup.find_all('div', 'filter filter-select')[2]
bases = []
for elem in html_blocks.find_all('div', 'item')[1:]:
    bases.append(elem.text[3:])

# заводим словарь "база: коктейли"
drinks_by_bases = {}
for base in bases:
    drinks_by_bases[base] = []

# словарь "коктейль: базы"
bases_by_drinks = {}
for base in bases:
    url = f'https://ru.inshaker.com/cocktails?q=На+{base}&search_page=59'
    response = requests.get(url)
    base_soup = BeautifulSoup(response.content, 'html.parser')
    drinks_soups = base_soup('div', 'cocktail-item')
    for drinks_soup in drinks_soups:
        drink_name = drinks_soup('div', 'cocktail-item-name')[0].text.replace('\xa0', ' ').replace('\xad', ' ')
        drink_url = f'https://ru.inshaker.com{drinks_soup.a["href"]}'
        drink_img = drinks_soup.img["src"]
        drinks_by_bases[base].append(drink_name)
        if drink_name not in bases_by_drinks:
            bases_by_drinks[drink_name] = []
        bases_by_drinks[drink_name].append(base)

# заполняем drinks_bases (список баз коктейлей)
for drink_name in drinks_names:
    if drink_name in bases_by_drinks:
        drinks_bases.append(bases_by_drinks[drink_name])
    else:
        drinks_bases.append([])

df = pd.DataFrame(
    {
        'drinks_names': drinks_names,
        'drinks_bases': drinks_bases,
        'drinks_urls': drinks_urls,
        'drinks_imgs': drinks_imgs
    }
)
