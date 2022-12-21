# import urllib.request
import os, bs4 as BeautifulSoup
import dotenv, json, urlcheck
from urllib3 import ProxyManager, make_headers

dotenv.load_dotenv()



def fetch_urls(URL):
	password = os.getenv('PASSWORD')
	default_headers = make_headers(proxy_basic_auth='testinglabs:{}'.format(password))
	http = ProxyManager("http://customer-testinglabs:{}@pr.oxylabs.io:7777".format(password), proxy_headers=default_headers)

	print(http.request('GET', 'https://ipinfo.io/').data)
	r = http.request('GET', URL)
	soup = BeautifulSoup.BeautifulSoup(r.data, 'html.parser')
	scripttags = soup.find_all('script')

	dictres = json.loads(scripttags[30].string.split('var gbProductListSsrData =')[1])
	for i in dictres['results']['goods']:
		fetchedurl = 'https://eur.shein.com' + i['detail_url'].split('?')[0]
		if(not urlcheck.is_url_present(fetchedurl)):
        		urlcheck.upload_url(fetchedurl)