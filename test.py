import re

import requests
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/Beauty/M.1488596143.A.919.html'

"""
test branch
"""
req2 = requests.get(url)
soup2 = BeautifulSoup(req2.text, 'html.parser')

soup2AAll = soup2.find_all('a', href=re.compile('http://(i.)?imgur.com/.*'))
for line in soup2AAll:
    link = line['href']
    print(link)