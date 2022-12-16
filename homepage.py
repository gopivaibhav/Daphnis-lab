from bs4 import BeautifulSoup
from requests_html import HTMLSession
import urlcheck, time

URLmain = ['https://eur.shein.com/Women-Blouses-c-1733.html?page=1',
            'https://eur.shein.com/Women-Tank-Tops-Camis-c-1779.html?page=1',
            'https://eur.shein.com/Women-Sweaters-c-1734.html?page=1',
            'https://eur.shein.com/Women-Cardigans-c-2219.html?page=1',
            'https://eur.shein.com/Women-Sweater-Vests-c-3807.html?page=1'
        ]

session = HTMLSession()

for URL in URLmain:
    r = session.get(URL)
    r.html.render(sleep=1, timeout=35)
    # finaldataforjson = {}

    productdetails = r.html.find('.product-list-v2__container')
    productsoup = BeautifulSoup(productdetails[0].html, features="html.parser")

    cards = productsoup.find_all(class_="S-product-item__name")
    # urls = []
    for i in cards:
        # urls.append('https://eur.shein.com' + i.find('a')['href'].split('?')[0])
        fetchedurl = 'https://eur.shein.com' + i.find('a')['href'].split('?')[0]
        if(not urlcheck.is_url_present(fetchedurl)):
            urlcheck.upload_url(fetchedurl)
    totalpages = productsoup.find_all(class_="S-pagination__total")[0].string.split()[1]
    # finaldataforjson['totalpages'] = totalpages
    # totalpages = 3
    for page in range(2, int(totalpages) + 1):
        URL = URL.split('?')[0] + '?page='+str(page)
        r = session.get(URL)
        r.html.render(sleep=1, timeout=35)
        productdetails = r.html.find('.product-list-v2__container')
        productsoup = BeautifulSoup(productdetails[0].html, features="html.parser")
        cards = productsoup.find_all(class_="S-product-item__name")
        for i in cards:
            fetchedurl = 'https://eur.shein.com' + i.find('a')['href'].split('?')[0] 
        # finaldataforjson['urls'] = urls
        if(not urlcheck.is_url_present(fetchedurl)):
            urlcheck.upload_url(fetchedurl)
        print('Fetched the data from page- ', page)
        time.sleep(3)

    print("Mission succesful for", URL)