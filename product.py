from bs4 import BeautifulSoup
from requests_html import HTMLSession
import urlcheck, os, images, time
from pymongo import MongoClient

from dotenv import load_dotenv
load_dotenv()

# with open('totalpages.txt', 'r') as myfile:
#     data=myfile.read()

# obj = json.loads(data)
session = HTMLSession()


# urlList = ['https://eur.shein.com/Mock-Neck-Puff-Sleeve-Button-Back-Tee-p-11806480-cat-1738.html']
# for URL in urlList:
for obj in urlcheck.get_urls():
    if(not obj['fetched']):
        # urlcheck.update_fetched(obj['link'])
        print('Updated in MongoDB')
        time.sleep(5)
        r = session.get(obj['link'])
        # print(r.status_code, 'r value')
        time.sleep(3)
        r.html.render(sleep=1, timeout=35)
        # print(r.html.find('body'), 'r -> html \n\n\n\n')
        finaldataforjson = {}
        productdetails = r.html.find('.goods-detailv2__media-inner')
        productsoup = BeautifulSoup(productdetails[0].html, features="html.parser")
        # print("Got the product details bro")
        # Content details
        price = productsoup.find_all(class_="product-intro__head-price")[0].find_all('span')[0]
        price = price.string.replace('€','').replace(',', '.').strip()
        title = productsoup.find_all(class_="product-intro__head-name")[0]
        title = title.string.strip()
        uniquesku = productsoup.find_all(class_="product-intro__head-sku")[0]
        uniquesku = uniquesku.string.replace('SKU: ','').strip()
        dsctable = productsoup.find_all(class_="product-intro__description-table-item")
        description = {}
        for ele in dsctable:
            key = ele.find_all(class_='key')[0].string.replace(":", "").strip()
            val = ele.find_all(class_='val')[0].contents[0].strip()
            description[key] = val
        sizes = productsoup.find_all(class_="product-intro__size-radio-inner")
        sizelist = []
        for ele in sizes:
            if(len(ele.contents) == 1):
                sizelist.append(ele.string.strip())
            else:
                newsize=''
                for i in ele.contents:
                    if(i.name == 'span'):
                        newsize += i.string
                sizelist.append(newsize)

        finaldataforjson['title'] = title
        finaldataforjson['uniquesku'] = uniquesku
        finaldataforjson['price'] = price
        finaldataforjson['description'] = description
        finaldataforjson['URL'] = obj['link'].split('?')[0]
        finaldataforjson['sizes'] = sizelist
        brandingdetails ={}
        if(len(productsoup.find_all(class_="product-intro__brand-des")) != 0):
            branddes = productsoup.find_all(class_="product-intro__brand-des")[0].string.replace('"','').strip()
            brandlogo = productsoup.find_all(class_="product-intro__brand-logo")[0]
            imgtag = 'https:' + brandlogo.img['src']
            brandingdetails['logo'] = imgtag
            brandingdetails['description'] = branddes
        finaldataforjson['branding'] = brandingdetails

        modeldetails = {}
        if(len(productsoup.find_all(class_="product-intro__sizeguide-summary-cover")) != 0):
            modelimg = productsoup.find_all(class_="product-intro__sizeguide-summary-cover")[0].contents[0].img
            modeldesc = productsoup.find_all(class_="model-item")[0]
            modeldict = {}
            for i in modeldesc.contents:
                if(i.name == 'div'):
                    key = i['aria-label'].split(':: ')[0]
                    val = i['aria-label'].split(':: ')[1]
                    modeldict[key] = val
            modeldetails['image'] = 'https:' + modelimg['src']
            modeldetails['description'] = modeldict
        finaldataforjson['model'] = modeldetails
        colors = []
        colorlist = productsoup.find_all(class_="product-intro__color_choose")
        if(len(colorlist) != 0):
            for i in colorlist[0].contents:
                if(i.name == 'div'):
                    colors.append(i['aria-label'])
        finaldataforjson['other-colours'] = colors

        categoryfind = productsoup.find_all(class_="bread-crumb__item-link")
        categorylist = []
        for ele in categoryfind:
            categorylist.append(ele.string.strip())
        finaldataforjson['category'] = categorylist

        # Pictures are saved 
        picturesinfo = productsoup.find_all(class_="product-intro__thumbs-item")
        pictures = []
        for element in picturesinfo:
            if(element.img):
                tag = element.img
                imgtag = tag['src'].split('_thumbnail_')[0]
                imgtag = 'https:' + imgtag + '_thumbnail_500x.webp'
                pictures.append(imgtag)
        finaldataforjson['images'] = pictures


        # Review section
        reviews = r.html.find('.j-expose__common-review-container')
        reviewssoup = BeautifulSoup(reviews[0].html, features="html.parser")
        reviewlist= reviewssoup.find_all(class_='common-reviews__list-item she-clearfix j-expose__common-reviews__list-item-con')

        reviewsdata = []
        for ele in reviewlist:
            reviewdict = {}
            left = ele.find_all(class_='common-reviews__list-item-left')[0]
            feedback = ''
            if(ele.find_all(class_='rate-des')[0].string):
                feedback = ele.find_all(class_='rate-des')[0].string.strip()
            name = ''
            if(len(ele.find_all(class_='nikename')) != 0):
                name = left.find_all(class_="nikename")[0].contents[0].string.strip()
            gddetails = left.find_all(class_="gd-detail-item")
            reviewerinfo = []
            for i in gddetails:
                reviewerinfo.append({i.contents[0].string.replace(":", '').strip(): i.contents[1].string.strip()})
            reviewdict['name'] = name
            reviewdict['feedback'] = feedback
            reviewdict['reviewerinfo'] = reviewerinfo
            userpurchased = {}
            userpurchase = ele.find_all(class_="rate-fit__item")
            for i in userpurchase:
                if(i.find('span')):
                    i = i.find('span')
                key = i.contents[0].string.replace(':', '').strip()
                val = i.contents[1].string.strip()
                userpurchased[key] = val
            reviewdict['userproduct'] = userpurchased
            reviewpictures = ele.find_all(class_='j-review-img')
            reviewlistpictures = []
            for i in reviewpictures:
                imgtag = i['data-src'].split('_thumbnail_')[0]
                imgtag = 'https:' + imgtag + '_thumbnail_x500.webp'
                reviewlistpictures.append(imgtag)
            reviewdict['reviewpictures'] = reviewlistpictures
            reviewsdata.append(reviewdict)
        finaldataforjson['reviews'] = reviewsdata

        client = MongoClient(os.getenv('PRODUCT_MONGO'))
        dbname =  client['shein-prod']
        collection_name = dbname["products"]
        checkval = collection_name.find_one({'uniquesku': finaldataforjson['uniquesku']})
        if(checkval == None):
            collection_name.insert_many([finaldataforjson])
        # collection_name.insert_many([finaldataforjson])
        # print(json.dumps(finaldataforjson, indent=3))
        print('Saved data for ', finaldataforjson['uniquesku'])
        images.download_image(finaldataforjson)
        print('Downloaded images for ', finaldataforjson['uniquesku'])
        time.sleep(5)
