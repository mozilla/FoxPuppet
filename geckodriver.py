import requests
import os
from bs4 import BeautifulSoup

r = requests.get('https://github.com/mozilla/geckodriver/releases')
soup = BeautifulSoup(r.text, 'html.parser')
latest = soup.find('div', {'class': 'label-latest'})
for link in latest.find_all('a'):
    if 'linux64' in link.get('href'):
        url = 'https://github.com' + link.get('href')
        os.putenv('GECKODRIVER_URL', url)
        os.system('curl -L -o geckodriver.tar.gz $GECKODRIVER_URL')
