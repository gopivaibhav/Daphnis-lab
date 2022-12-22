from bs4 import BeautifulSoup
from requests_html import HTMLSession
import time, proxy, urlcheck

URLmain = [
            'https://eur.shein.com/style/Bodycon-Dresses-sc-00100632.html?page=1',
            'https://eur.shein.com/Series/evoluSHEIN-sc-66672359.html?page=1',
            'https://eur.shein.com/style/Satin-Dresses-sc-00106405.html?page=1',
            'https://eur.shein.com/trends/Prom-Dresses-sc-00673766.html?page=1',
            'https://eur.shein.com/style/Cut-Out-Dresses-sc-00106787.html?page=1',
            'https://eur.shein.com/style/Shirt-Dresses-sc-00101007.html?page=1',
            'https://eur.shein.com/Women-Sweater-Dresses-c-2218.html?page=1',
            'https://eur.shein.com/style/Sweatshirt-Dresses-sc-00101010.html?page=1',
            'https://eur.shein.com/style/Floral-Dresses-sc-00100610.html?page=1',
            'https://eur.shein.com/style/Blazer-Dress-sc-00105522.html?page=1',
            'https://eur.shein.com/trends/Faux-Leather-Dresses-sc-00682809.html?page=1',
            'https://eur.shein.com/style/Velvet-Dresses-sc-00114153.html?page=1',
            'https://eur.shein.com/style/Long-Dresses-sc-00100631.html?page=1',
            'https://eur.shein.com/style/Short-Dresses-sc-00100608.html?page=1',
            'https://eur.shein.com/style/Midi-Dresses-sc-00100629.html?page=1',
            'https://eur.shein.com/style/Maxi-Dresses-sc-00100346.html?page=1',
            'https://eur.shein.com/Plus-Size-Bridesmaid-Dresses-c-3099.html?page=1',
            'https://eur.shein.com/Wedding-Dresses-c-3089.html?page=1',
            'https://eur.shein.com/Bridesmaid-Dresses-c-3091.html?page=1',
            'https://eur.shein.com/Plus-Size-Wedding-Dresses-c-3098.html?page=1',
            'https://eur.shein.com/style/Blue-Dress-sc-00105560.html?page=1',
            'https://eur.shein.com/style/Black-Dresses-sc-00100178.html?page=1',
            'https://eur.shein.com/style/White-Dresses-sc-00100605.html?page=1',
            'https://eur.shein.com/style/Pink-Dresses-sc-00100603.html?page=1',
            'https://eur.shein.com/trends/Brown-Dresses-sc-00682810.html?page=1',
            'https://eur.shein.com/style/Red-Dresses-sc-00100604.html?page=1',
            'https://eur.shein.com/new/New-In-Dresses-sc-00200108.html?page=1',
            'https://eur.shein.com/new/Sweatshirts-New-in-15-Days-sc-00211250.html?page=1',
            'https://eur.shein.com/new/Tops-New-in-15-Days-sc-00204866.html?page=1',
            'https://eur.shein.com/new/Blouses-New-in-15-Days-sc-00204865.html?page=1',
            'https://eur.shein.com/new/Bottoms-New-in-15-Days-sc-00211253.html?page=1',
            'https://eur.shein.com/new/Sweaters-New-in-15-Days-sc-00211251.html?page=1',
            'https://eur.shein.com/new/New-in-Jumpsuits-Bodysuits-sc-00219549.html?page=1',
            'https://eur.shein.com/new/New-in-Twopiece-sc-00222241.html?page=1',
            'https://eur.shein.com/new/Coats-Jackets-New-in-15Days-sc-00211247.html?page=1',
            'https://eur.shein.com/new/Blazers-Suits-New-in-15-Days-sc-00255663.html?page=1',
            'https://eur.shein.com/Women-Boots-c-3180.html?page=1',
            'https://eur.shein.com/Women-Sandals-c-3183.html?page=1',
            'https://eur.shein.com/Women-Sneakers-c-3191.html?page=1',
            'https://eur.shein.com/Women-Flats-c-1881.html?page=1',
            'https://eur.shein.com/Women-Pumps-c-1750.html?page=1',
            'https://eur.shein.com/Women-Wedges-Flatform-c-1749.html?page=1',
            'https://eur.shein.com/Women-Slippers-c-3187.html?page=1',
            'https://eur.shein.com/Women-Water-Shoes-c-3190.html?page=1',
            'https://eur.shein.com/Women-Clogs-c-3189.html?page=1',
            'https://eur.shein.com/Women-Shoes-Accessories-c-3194.html?page=1',
            'https://eur.shein.com/Office-School-Supplies-c-2297.html?page=1',
            'https://eur.shein.com/Automotive-c-3657.html?page=1',
            'https://eur.shein.com/Women-Satchels-c-2155.html?page=1',
            'https://eur.shein.com/Women-Backpacks-c-2151.html?page=1',
            'https://eur.shein.com/Women-Crossbody-c-2152.html?page=1',
            'https://eur.shein.com/Women-Shoulder-Bags-c-1764.html?page=1',
            'https://eur.shein.com/Women-Tote-Bags-c-2844.html?page=1',
            'https://eur.shein.com/Women-Clutches-c-2153.html?page=1',
            'https://eur.shein.com/Women-Purses-c-2154.html?page=1',
            'https://eur.shein.com/Women-Fanny-Packs-c-2156.html?page=1',
            'https://eur.shein.com/Women-Bag-Sets-c-2157.html?page=1',
            'https://eur.shein.com/Bag-Accessories-c-2158.html?page=1',
            'https://eur.shein.com/Women-Evening-Bags-c-3876.html?page=1',
            'https://eur.shein.com/Sports-Equipment-c-2466.html?page=1',
            'https://eur.shein.com/Women-Belts-c-3868.html?page=1',
            'https://eur.shein.com/Glasses-Eyewear-Accessories-c-2841.html?page=1',
            'https://eur.shein.com/Hair-Accessories-c-3013.html?page=1',
            'https://eur.shein.com/Hats-Gloves-c-3630.html?page=1',
            'https://eur.shein.com/Keychains-c-1914.html?page=1',
            'https://eur.shein.com/Face-Coverings-Accs-c-3027.html?page=1',
            'https://eur.shein.com/Scarves-c-1872.html?page=1',
            'https://eur.shein.com/Dickey-Collars-c-3022.html?page=1',
            'https://eur.shein.com/Ties-c-3661.html?page=1',
            'https://eur.shein.com/Wedding-Accessories-c-3279.html?page=1',
            'https://eur.shein.com/Watches-c-3029.html?page=1',
            'https://eur.shein.com/Brands/JMMO-sc-01485775.html?page=1',
            'https://eur.shein.com/Computer-Office-c-2275.html?page=1',
            'https://eur.shein.com/Fine-Jewelry-c-3035.html?page=1',
            'https://eur.shein.com/Earrings-c-4202.html?page=1',
            'https://eur.shein.com/Necklaces-c-4208.html?page=1',
            'https://eur.shein.com/Rings-c-4216.html?page=1',
            'https://eur.shein.com/Bracelets-c-4196.html?page=1',
            'https://eur.shein.com/Piercings-c-1908.html?page=1',
            'https://eur.shein.com/Phone/Pad-Accessories-c-2274.html?page=1',
            'https://eur.shein.com/Audio-Video-c-3645.html?page=1',
            'https://eur.shein.com/Smart-Watches-Accs-c-3337.html?page=1',
            'https://eur.shein.com/trends/SHEIN-IP-Collabs-Accessories-sc-00688242.html?page=1'
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
    if(productsoup.find_all(class_="S-pagination__total")):
        totalpages = productsoup.find_all(class_="S-pagination__total")[0].string.split()[1]
    else:
        totalpages = 1
    for page in range(2, int(totalpages) + 1):
        URL = URL.split('?')[0] + '?page='+str(page)
        proxy.fetch_urls(URL)
        print('Fetched the data from page- ', page)

    print("Mission succesful for", URL)