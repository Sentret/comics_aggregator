import bs4
import requests
import os
import re
import django
from django.db import IntegrityError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comics_aggregator.settings")
django.setup()


from app.models import ComicsBook



def get_plain_html(url):
    r = requests.get(url)
    plain_html = r.text
    return plain_html


def crawl_labirint():
    
    plain_html = get_plain_html('https://www.labirint.ru/genres/2993/')
    soup = bs4.BeautifulSoup(plain_html)

    for book in soup.find_all('div', class_='product'):

        try:    
            title = book.find('span', class_='product-title').string        
            image_url = book.find('img', class_='book-img-cover')['data-src']
            price = int(book.find('span', class_='price-val').find('span').string.replace(' ',''))
            href = 'https://www.labirint.ru'+book.find('a', class_='cover')['href']

            comics = ComicsBook(title=title,image_url=image_url,price=int(price),href=href,source='labirint')
            comics.save()

        except AttributeError as e:
            print(e)


def crawl_ozon():
    plain_html = get_plain_html('https://www.ozon.ru/catalog/1140886/?russianlanguage=1&sort=new')
    soup = bs4.BeautifulSoup(plain_html)

    for book in soup.find_all('div', class_='bOneTile inline jsUpdateLink mRuble '):
        
        try: 
            title = book.find('div', class_='eOneTile_ItemName').string
            image_url = book.find('img')['src']
            price = int(book.find('span', class_='eOzonPrice_main').string.replace(' ',''))
            href = 'https://www.ozon.ru'+ book.find('a',class_='eOneTile_image_link jsUpdateLink jsPic')['href']
            
            comics = ComicsBook(title=title,image_url=image_url,price=int(price),href=href,source='ozon')
            comics.save()
             
        except AttributeError as e:
            print(e)


def crawl_chookandgeek():
    plain_html = get_plain_html('http://www.chookandgeek.ru/')
    soup = bs4.BeautifulSoup(plain_html)

    for book in soup.find_all('div', class_='product_preview'):
        
        try: 
            title = book.find('a', class_='product_preview-link').string
            image_url = book.find('img')['src']
            price_match = re.findall('\d+',book.find('div',class_='prices-current').string)[0]
            price = int(price_match)
            href = 'http://www.chookandgeek.ru/'+ book.find('a')['href']
            comics = ComicsBook(title=title,image_url=image_url,price=int(price),href=href,source='chookandgeek')
            comics.save()
             
        except :
            pass



def crawl_lavkaapelsin():
    plain_html = get_plain_html('http://www.lavkaapelsin.ru/comics/rusbook/')
    soup = bs4.BeautifulSoup(plain_html)
    
    for book in soup.find_all('div', class_='tov_block tv_pad'):
        
        try: 

            title = book.find('div', class_='tov_link').find('a').string
            image_url = 'http://www.lavkaapelsin.ru' + book.find('img')['src']          
            price_match = re.findall('\d+',book.find('div',class_='tov_price').string)[0]
            price = int(price_match)
            href = 'http://www.lavkaapelsin.ru'+ book.find('div', class_='tov_link').find('a')['href']
            comics = ComicsBook(title=title,image_url=image_url,price=int(price),href=href,source='lavkaapelsin')
            comics.save()

        except IntegrityError as e:
            pass


def crawl():
    crawl_ozon()
    crawl_labirint()
    crawl_chookandgeek()
    crawl_lavkaapelsin()



