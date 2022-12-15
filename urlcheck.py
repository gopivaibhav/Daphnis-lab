from pymongo import MongoClient
import os

from dotenv import load_dotenv
load_dotenv()
client = MongoClient(os.getenv('CONNECTION_STRING'))
dbname =  client['shein-urls-prod']
collection_name = dbname["urls-check"]

def is_url_present(URL):
    item_details = collection_name.find()
    for i in item_details:
        if i['link'] == URL:
            print(URL)
            return True
    return False


def upload_url(URL):
    item = {
        "link": URL
    }
    collection_name.insert_many([item])
    print("Uploaded "+ URL)


def get_urls():
    urlList = []
    items = collection_name.find()
    for item in items:
        urlList.append(item['link'])
    return urlList