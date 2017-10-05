import bs4
import requests
import os
import django


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

            comics = ComicsBook(title=title,image_url=image_url,price=int(price),href=href,source='Labirint')
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
            
            comics = ComicsBook(title=title,image_url=image_url,price=int(price),href=href,source='Ozon')
            comics.save()
             
        except AttributeError as e:
            print(e)


def crawl():
    crawl_ozon()
    crawl_labirint()