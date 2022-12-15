from bs4 import BeautifulSoup
from requests_html import HTMLSession
import urlcheck

# URL = 'https://eur.shein.com/Women-Jackets-c-1776.html?page=1'
URL = 'https://eur.shein.com/Women-Pants-c-1740.html?page=1'
session = HTMLSession()

r = session.get(URL)
r.html.render(sleep=1, timeout=20)
finaldataforjson = {}

productdetails = r.html.find('.product-list-v2__container')
productsoup = BeautifulSoup(productdetails[0].html, features="html.parser")

cards = productsoup.find_all(class_="S-product-item__name")
urls = []
for i in cards:
    urls.append('https://eur.shein.com' + i.find('a')['href'].split('?')[0])
totalpages = productsoup.find_all(class_="S-pagination__total")[0].string.split()[1]
finaldataforjson['totalpages'] = totalpages
# totalpages = 3
for page in range(2, int(totalpages) + 1):
    URL = URL.split('?')[0] + '?page='+str(page)
    r = session.get(URL)
    r.html.render(sleep=1, timeout=20)
    productdetails = r.html.find('.product-list-v2__container')
    productsoup = BeautifulSoup(productdetails[0].html, features="html.parser")
    cards = productsoup.find_all(class_="S-product-item__name")
    for i in cards:
        urls.append('https://eur.shein.com' + i.find('a')['href'].split('?')[0])
    finaldataforjson['urls'] = urls
    print('Fetched the data from page- ', page)

# with open('totalpages.txt', 'w') as f:
#     f.write(str(finaldataforjson['totalpages']))

for url in urls:
    if(not urlcheck.is_url_present(url)):
        urlcheck.upload_url(url)

print("Mission succesful")