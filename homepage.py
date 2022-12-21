from bs4 import BeautifulSoup
from requests_html import HTMLSession
import time, proxy, urlcheck

URLmain = [
            'https://eur.shein.com/Women-Sexy-Lingerie-c-1862.html?page=1',
            'https://eur.shein.com/category/Sexy-Costumes-sc-00855966.html?page=1',
            'https://eur.shein.com/Women-Bras-Bralettes-c-2203.html?page=1',
            'https://eur.shein.com/Women-Panties-c-2205.html?page=1',
            'https://eur.shein.com/Women-Bra-Panty-Sets-c-2270.html?page=1',
            'https://eur.shein.com/Weddings-Events-c-3088.html?page=1',
            'https://eur.shein.com/Women-Suits-c-2036.html?page=1'
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