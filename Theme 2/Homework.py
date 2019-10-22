import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import json

main_url = 'https://geekbrains.ru'
url = '/posts'

#функция для получения супа заданной ссылки
def get_soup(url):
    data = requests.get(url)
    time.sleep(0.5) #Иначе too many requests per second
    if data.text:
        soup = BeautifulSoup(data.text, 'lxml')
        return soup
    else:
        print(f'Cant find text. Status code: {data.status_code}')
        return None


#собственно сам парсер страницы с новостью
def parser(url_list):
    result_data = []
    for url in url_list:
        data_dict = {}
        soup = get_soup(url)
        if soup:
            data_dict['title'] = soup.find('h1', class_='blogpost-title').get_text()
            blog_content = soup.find('div', class_='blogpost-content')
            #В некоторых постах нет картинки, поэтому try
            try:
                data_dict['image'] = blog_content.find('img').get('scr')
            except AttributeError:
                data_dict['image'] = 'None'
            data_dict['text'] = blog_content.get_text()
            time = datetime.strptime(soup.find('time').get('datetime').split('+')[0], '%Y-%m-%dT%H:%M:%S')
            data_dict['pub_date'] = time.timestamp()
            data_dict['autor'] = {}
            data_dict['autor']['name'] = soup.find('div', class_='text-lg').get_text()
            data_dict['autor']['url'] = 'https://geekbrains.ru' + soup.find('div', class_='col-md-5').find('a').get('href')
            result_data.append(data_dict)
        else:
            print(f'Soup not found for url {url}')
    
    return result_data

#функция для получения списка url для парсера
def get_url_list_parser(main_url, url):
    url_list = []
    while url:
        soup = get_soup(main_url + url)
        posts_list = soup.find_all('div', class_='post-item')
        for item in posts_list:
            url_list.append(main_url + item.find('a').get('href'))
        try:
            url = soup.find('li', class_='page', text='›').find('a').get('href')
        except AttributeError:
            break

    return url_list

url_list = get_url_list_parser(main_url, url)
result_data = json.dumps(parser(url_list))

with open(f'posts_data_{datetime.now().date()}.json', 'w') as f:
    f.write(result_data)

