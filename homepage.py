from bs4 import BeautifulSoup
from requests_html import HTMLSession
import time, proxy, urlcheck

URLmain = [
            'https://eur.shein.com/Women-Two-piece-Outfits-c-1780.html?page=1',
            'https://eur.shein.com/Women-Jumpsuits-Bodysuits-c-3287.html?page=1',
            'https://eur.shein.com/Sports-c-3195.html?page=1',
            'https://eur.shein.com/Women-Denim-c-1930.html?page=1',
            'https://eur.shein.com/Women-Beachwear-c-2039.html?page=1',
            'https://eur.shein.com/Women-Sleep-Lounge-c-3626.html?page=1',
            'https://eur.shein.com/Women-Intimates-c-3625.html?page=1',
            'https://eur.shein.com/Cosplay-Costumes-c-3066.html?page=1'
        ]

session = HTMLSession()

for URL in URLmain:
    r = session.get(URL)
    r.html.render(sleep=1, timeout=35)

    productdetails = r.html.find('.product-list-v2__container')
    productsoup = BeautifulSoup(productdetails[0].html, features="html.parser")

    cards = productsoup.find_all(class_="S-product-item__name")
    for i in cards:
        fetchedurl = 'https://eur.shein.com' + i.find('a')['href'].split('?')[0]
        if(not urlcheck.is_url_present(fetchedurl)):
            urlcheck.upload_url(fetchedurl)
    totalpages = productsoup.find_all(class_="S-pagination__total")[0].string.split()[1]
    # totalpages = 3
    for page in range(2, int(totalpages) + 1):
        URL = URL.split('?')[0] + '?page='+str(page)
        proxy.fetch_urls(URL)
        print('Fetched the data from page- ', page)
        time.sleep(6)

    print("Mission succesful for", URL)