import os
import re
from os.path import basename

import requests
from bs4 import BeautifulSoup


def getFirstPage():
    req = requests.get('https://www.ptt.cc/bbs/Beauty/index.html')
    soup = BeautifulSoup(req.text, 'html.parser')

    #pages = soup.find_all('a', href=re.compile(r'/bbs/Beauty/index(.+).html'))
    # print(pages[-1]['href'].search(r'index.+html'))

    # print(re.search('/bbs/Beauty/index(\d+).html', str(soup)).group(1))
    firstPage = re.findall('/bbs/Beauty/index(\d+).html', str(soup))[-1]
    firstPage = int(firstPage) + 1
    return firstPage


def crawler(page):
    req = requests.get(page)

    soup = BeautifulSoup(req.text, 'html.parser')

    soupR_ent = soup.select('.r-ent')

    # wait
    excludeTitles = ['[情報]', '[公告]']
    print(len(soupR_ent))
    for line in soupR_ent:
        title = line.select('.title')[0].text
        if '本文已被刪除' in title:
            continue
        name = line.select('a')
        if not name:
            continue
        name = name[0].text
        breakBool = False
        for excludeTitle in excludeTitles:
            if excludeTitle in name:
                breakBool = True
        if breakBool:
            continue
        name = name.replace(':', '').replace(' ', '')
        if not os.path.exists(name):
            os.mkdir(name)
        URL = line.select('a')[0]['href']
        print(URL)
        req2 = requests.get('https://www.ptt.cc'+URL)
        soup2 = BeautifulSoup(req2.text, 'html.parser')
        soup2AAll = soup2.find_all('a', href=re.compile('http://(i.)?imgur.com/.*'))
        for line in soup2AAll:
            link = line['href']
            if link[-4:]!='.jpg':
                link += '.jpg'

            with open(name+'/'+basename(link), "wb") as f:
                f.write(requests.get(link).content)
            f.close()



if __name__ == '__main__':
    firstPage = getFirstPage()
    print(firstPage)

    page = 5 # 3

    for i in range(firstPage, firstPage-page, -1):
        pageURL = 'https://www.ptt.cc/bbs/Beauty/index{0}.html'.format(i)
        print(pageURL)
        crawler(pageURL)




