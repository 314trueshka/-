import requests
from bs4 import BeautifulSoup
URL = "https://www.timeout.ru/msk/artwork/"
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
FILMS_ID = 1000000
rev = "/review"
films = []
def get_html(url, films_id):
    r = requests.get(url + films_id,headers = HEADERS)
    return r


def get_html_rev(url, films_id):
    r = requests.get(url + films_id + rev,headers = HEADERS)
    return r

def get_content(html):

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_ = 'details-list')
    photos = soup.find_all('img', class_ = 'photo__img')
    names = soup.find_all('h1', class_='page-header__title')
    name = ''
    for i in names[0]:
        name = i
        films.append([name.replace("\n",'').strip()])
    photo = str(photos[0])
    image = ''
    K = 0
    for i in range(len(photo)):
        if photo[i-5] + photo[i-4] + photo[i-3] + photo[i-2]  + photo[i-1] == 'src="':
            K = 1;
        if K == 1 and photo[i] != '"':
            image += photo[i]
        elif K == 1 and photo[i] == '"':
            films[-1].append(image)
            break
    for item in items:
        get_info(item)


def get_info(item):
    info = []
    for i in item.find_all('dd', class_="details-list__text"):
        info.append(i.get_text(strip=True))
    films[-1].append(info)


def get_review(html_rev):

    soup = BeautifulSoup(html_rev, 'html.parser')
    items = soup.find('div',class_ = 'article__text').get_text()
    films[-1].append(items.replace("\xa0"," ").replace('\r\n'," ").replace('\r'," "))
    print(films[-1])

def parse():
    global FILMS_ID
    html = get_html(URL,str(FILMS_ID)[1:])
    html_rev = get_html_rev(URL,str(FILMS_ID)[1:])
    FILMS_ID +=1
    if html.status_code == 200:
        get_content(html.text)
        get_review(html_rev.text)

while FILMS_ID < 2000000:
        parse()
exit(print("Парсинг завершен"))
