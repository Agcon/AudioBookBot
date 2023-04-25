from bs4 import BeautifulSoup as bs
import requests
import fake_useragent
import urllib.request
from PyBitTorrent import TorrentClient
from txt_to_mp3 import *
from config import *


def avidreaders_parser(user_search): # парсинг сайта авидридерс
    pass

def tululu_parser(user_search): # парсинг сайта тулулу (много новых книг)
    session = requests.Session()
    user = fake_useragent.UserAgent().random
    header = {'user-agent': user}

    us = user_search.strip().replace(" ", "+").lower() # форматирование запроса
    search_url = 'https://tululu.org/search/?q=' + us # поисковая ссылка 
    responce = requests.get(search_url, headers=header).content
    soup = bs(responce, "html.parser") # исходный код

    # создание списка тегов с названием книги и ссылкой внутри
    books = list()
    for li in soup.find_all("li"):
        h = li.find('h3')
        if h:
            books.append(h)
        
    #---------- test output ------------
    print('Список найденных книг:')
    [print(i) for i in books]
    #-----------------------------------

    if len(books) > 5:
        pass # нужно конкретизировать поиск, т.к. слишком много результатов

    books_names = [book.text for book in books] # список названий книг

    # TODO: подключить бота для выбора книги из списка
    book_name = books_names[0] # название выбранной книги

    # ссылка на книгу
    book_url = "tululu.org" + books[books_names.index(book_name)].find('a').get('href')

    # ссылка на скачивание txt
    download_url = 'https://tululu.org/txt.php?id=' + book_url.split('/b')[1].replace('/', '')
    # скачивание txt
    response = requests.get(download_url)
    book_dir = "{}/{}.txt".format(lib_path, book_name.replace(" ", ""))
    open(book_dir, "wb").write(response.content)
    txt_to_mp3_offline(book_dir)
    
'''
def torrent_downloader(path):
    client = TorrentClient(path, output_dir=path[:path.rfind('/')])
    client.start()
'''

if __name__ == "__main__":
    tululu_parser("Бархатный сезон брэдбери")
