from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

donation_urls = [
	"donate/990101674782594",
	"donate/1471028846618111",
	"donate/288489982604965",
	"donate/988754068266075",
	"donate/286586375766068",
	"donate/889033311592192",
	"donate/600815963961779",
	"donate/3125911987487049",
	"donate/594422747886277",
]

scraped_data = []

for donate_url in donation_urls:
	url = "https://www.facebook.com/" + donate_url
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find(id='progress_card')

	in_progress_fundraiser = results.find_all('span', class_='_1r05')
	completed_fundraiser = results.find_all('span', class_='_1r08')
	fundraiser = in_progress_fundraiser + completed_fundraiser
	goal = fundraiser[0]

	# money format is: $1,390 AUD of $1,000 AUD
	money = re.findall("\$[\d\,]+", goal.text)	
	
	names = soup.find_all("div", class_ = "_6a _6b")
	for name in names:
		name_span = name.find('span', class_='_21f9 _50f4 _50f7')
		if name_span:
			valid_name = name_span.text

	output = [valid_name, money[0], money[1]]
	scraped_data.append(output)

df_scraped_data = pd.DataFrame(scraped_data)
df_scraped_data.columns = ['name', 'raised', 'goal']
df_scraped_data.to_csv('aycc_speakup_fundraiser_data.csv', index = False)
