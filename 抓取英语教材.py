from urllib.request import urlopen,Request
from time import sleep
import random
from bs4 import BeautifulSoup
import xlwt

def get_html(html):
    request = Request(html)
    request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    text = urlopen(request).read()
    text = text.decode('utf-8')
    return text

list = []
def htmllist(page):
    soup = BeautifulSoup(page,'html5lib')
    ul = soup.find_all('ul',attrs={'id':'menu-list'})
    list_s = []
    for child in ul:
        for i in child.children:
           try:
                href = i.h2.a.get('href')
                list_s.append(href)
           except:pass
    list.extend(reversed(list_s))

def html_rep(page):
    text = []
    soup = BeautifulSoup(page, 'html5lib')
    qh_en = soup.find_all('div',attrs={'class':'qh_en'})
    title = soup.find('h1',attrs={'id':'nrtitle'}).string
    text.append('\n')
    text.append(title)
    text.append('\n')
    if qh_en:               #页面有“只看中文；只看英文”选项时
        for item in qh_en:
            for i in item.stripped_strings:
                k = '   '+i
                text.append(k)
        return '\n'.join(text)
    else:
        for item in soup.find_all('span',attrs={'id':'article_eng'}):
            x = item.find_all('p')
            for i in x[1].stripped_strings:
                k = '   ' + i
                text.append(k)
        return '\n'.join(text)

list_num = 1
page_num = 1

for i in range(1,16):
    page = get_html('http://www.kekenet.com/Article/15463/List_%d.shtml'%i)
    htmllist(page)
    print('第%s页目录已抓取'%list_num)
    list_num+=1
    sleep(random.random() * 0.4)

page = get_html('http://www.kekenet.com/Article/15463/')
htmllist(page)

for i in list:
    print(i)
    page = get_html(i)
    text = html_rep(page)
    f = open('英语练习.txt','a+',encoding='utf-8') #encoding='utf-8是解决问题的关键
    #text = text.encode('utf-8','ignore')
    try:f.write(text)
    except:
        print(text)
        raise
    print('第%s页页面已抓取'%page_num)
    page_num+=1
    sleep(random.random() * 0.4)

f.close()
