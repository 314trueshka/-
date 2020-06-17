import requests
import json
from bs4 import BeautifulSoup

start_id, end_id = map(int, input().split())


URL = "https://www.timeout.ru/msk/artwork/"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
FILMS_ID = 1000000 + start_id

rev = "/review"
films = []
film ={'id': None, 'name': None, 'year': None, 'description': None, 'duration': None, 'poster': None, 'genres': None }
missed_ids = []


def get_html(url, films_id):
    r = requests.get(url + films_id,headers = HEADERS)
    return r


def get_html_rev(url, films_id):
    r = requests.get(url + films_id + rev,headers = HEADERS)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    category = soup.find_all('dt', class_ = 'details-list__title')
    items = soup.find_all('div', class_ = 'details-list')
    photos = soup.find_all('img', class_ = 'photo__img')
    names = soup.find_all('h1', class_='page-header__title')

    for i in names[0]:
        name = i
        film['name'] = str(name.replace("\n",'').strip())

    photo = str(photos[0])
    image = ''
    K = 0

    for i in range(len(photo)):
        if photo[i-5] + photo[i-4] + photo[i-3] + photo[i-2]  + photo[i-1] == 'src="':
            K = 1;
        if K == 1 and photo[i] != '"':
            image += photo[i]
        elif K == 1 and photo[i] == '"':
            film['poster'] = image
            break
    name_category = []
    for cat in category:
        name_category.append(cat.get_text())

    for item in items:
        for i in range(len(name_category)):
            info = item.find_all('dd', class_="details-list__text")[i].get_text(strip=True).replace(',', ", ")

            if name_category[i] == 'Жанр':
                film['genres'] = [info]
            if name_category[i] == 'Длительность':
                film['duration'] = info
            if name_category[i] == 'Страна':
                film['year'] = info[-7:-3]



def get_review(html_rev):

    soup = BeautifulSoup(html_rev, 'html.parser')
    try:
        items = soup.find('div',class_ = 'article__text').get_text()
    except:
        items = "None"
    film["description"] = items.replace("\xa0"," ").replace('\r\n'," ").replace('\r'," ").replace('\n',' ')
    films.append(film)


def parse():
    global FILMS_ID
    html = get_html(URL,str(FILMS_ID)[1:])
    html_rev = get_html_rev(URL,str(FILMS_ID)[1:])

    if html.status_code == 200:
        film['id'] = str(FILMS_ID)[1:]
        get_content(html.text)
        get_review(html_rev.text)
    else:
        missed_ids.append(str(FILMS_ID)[1:])
    FILMS_ID +=1


while FILMS_ID  < 1000000 + end_id:
        parse()
        film = {'id': None, 'name': None, 'year': None, 'description': None, 'duration': None, 'poster': None,
                'genres': None}

BD = {"start_id": start_id, 'end_id': end_id, 'missed_ids': missed_ids, 'films': films}

with open("data_file.json", "w") as write_file:
    json.dump(BD,write_file,indent=4)
