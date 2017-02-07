#file = open(r'C:\Users\Administrator\Desktop\python\citis.json','w+',encoding= 'utf-8')

import json
from urllib.request import urlopen
from html.parser  import HTMLParser

citis = {}
class Scraper(HTMLParser):
    in_table = False
    in_tbody = False
    in_tr = False
    in_en = False
    in_ch = False
    cunt = 0
    chinese = 0
    english = 0
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag == 'table' and 'class' in attrs:
            if attrs['class'] == 'wikitable sortable selected_now jquery-tablesorter':
                self.in_table = True

        if tag == 'tbody':
            self.in_tbody = True
           # print(2)
        if tag == 'tr':
            self.in_tr = True
           # print(3)
        if tag == 'a':
            self.in_en = True
          #  self.en = []
            self.cunt += 1
            #print(4)
        if tag == 'span' and 'lang' in attrs:
            self.in_ch = True
           # self.ch = []
           # print(5)

    def handle_data(self, data):
        if self.in_en and self.cunt == 1:

            self.en = data
        if self.in_ch :
            #print(data)
            self.ch = data

    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False

        if tag == 'tbody':
            self.in_tbody = False
        if tag == 'a':
            if self.in_table and self.in_tbody and self.in_tr and self.in_en:
                self.english = self.en
                print(self.english)
            self.in_en = False
        if tag == 'span':
            if self.in_table and self.in_tbody and self.in_tr and self.in_ch:
                self.chinese = self.ch
                print(self.chinese)

            self.in_ch = False
        if tag == 'tr':

            citis[self.chinese] = self.english

            self.cunt = 0
            self.in_tr = False





text = open(r'C:\Users\Administrator\Desktop\python\List of cities in China - Wikipedia.html',encoding= 'utf-8').read()
#text = text.decode('utf-8')
parser = Scraper()
parser.feed(text)
parser.close()
#print(citis)
#print(len(citis))
citis.pop(0)
d = {'list':[]}
for key in citis:
    a={}
    a['en'] = citis[key]
    a['ch'] = key
    d['list'].append(a)
with open(r'C:\Users\Administrator\Desktop\python\citis.json','w',encoding= 'utf-8') as f:
    f.write(json.dumps(d,ensure_ascii=False ))
#print(jsr)
#file.write(d)