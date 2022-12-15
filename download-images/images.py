import image, os, json
from pymongo import MongoClient

from dotenv import load_dotenv
load_dotenv()

with open('image.json', 'r') as myfile:
    data=myfile.read()
obj = json.loads(data)



print(obj['uniquesku'])

if ('image' in obj['model']):
    image.upload_file(obj['model']['image'], obj['uniquesku'] + '/model.webp')

for index, img in enumerate(obj['images'], start=1):
    image.upload_file(img, obj['uniquesku'] + '/image'+ str(index) +'.webp')

for outer, r in enumerate(obj['reviews'], start=1):
    if(len(r['reviewpictures']) != 0):
        for inner, img in enumerate(r['reviewpictures'], start=1):
            image.upload_file(img, obj['uniquesku'] + '/reviewimage'+ str(outer) + '-' + str(inner) +'.webp')