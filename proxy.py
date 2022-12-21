import urllib.request
import os, bs4 as BeautifulSoup
import dotenv, json, urlcheck

dotenv.load_dotenv()



def fetch_urls(URL):
	username = 'testinglabs'
	password = os.getenv('PASSWORD')
	entry = ('http://customer-%s:%s@pr.oxylabs.io:7777' %
		(username, password))
	query = urllib.request.ProxyHandler({
		'http': entry,
		'https': entry,
	})
	execute = urllib.request.build_opener(query)
	print(execute.open('https://ipinfo.io').read(), '\n\n')
	productsoup = execute.open(URL).read().decode('utf-8')
	soup = BeautifulSoup.BeautifulSoup(productsoup, 'html.parser')
	scripttags = soup.find_all('script')

	dictres = json.loads(scripttags[30].string.split('var gbProductListSsrData =')[1])
	for i in dictres['results']['goods']:
		fetchedurl = 'https://eur.shein.com' + i['detail_url'].split('?')[0]
		if(not urlcheck.is_url_present(fetchedurl)):
        		urlcheck.upload_url(fetchedurl)