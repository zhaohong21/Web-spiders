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

def douban(page):
    shu = []
    soup = BeautifulSoup(page,'html5lib')
    for child in soup.body.children:
        if child.name == 'div' and 'id' in child.attrs:
            if child['id'] == 'wrapper':
                list = child.div.div.div.div.ul #书籍所在目录
                for childs in list.children:
                    a = {}
                    if childs.name == 'li':
                        for child_2 in childs.children:
                            if child_2.name == 'div' and 'class' in child_2.attrs:
                                if child_2['class'] == ['info']:    ##class属性会被判别为多值属性，返回的是list而不是字符串。
                                    if child_2.a.string:
                                        a['name'] = child_2.a.string
                                    elif not child_2.a.string:  #处理副标题
                                        a['name'] = ''
                                        for string in child_2.a.stripped_strings:
                                            a['name'] += string
                                    a['html'] = child_2.a['href']
                                    for divs in child_2.children:
                                        if divs.name == 'div' and 'class' in divs.attrs:
                                            if divs['class'] == ['pub']:
                                                a['author'] = divs.string
                                            if divs['class'] == ['star','clearfix']:    #此处需注意，原HTML中class = "star clearfix"，因为class背判别为多值属性，所以此处应当如此填写。
                                                for span in divs.children:
                                                    if span.name == 'span' and 'class' in span.attrs:
                                                        if span['class'] == ['rating_nums']:
                                                            a['star'] = span.string
                                        if divs.name == 'p':
                                            a['introduce'] = divs.string
                                           # print(a)
                        shu.append(a)
    for dict in shu:   #去除\n和空格
        for (key,val) in dict.items():
            try:dict[key] = val.strip('\n ')
            except:pass

    return shu        ########################################

class Excel:
    def __init__(self):
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.worksheet = self.workbook.add_sheet('小说')
        first_row = ['序号', '书名', '作者、出版社、价格', '评分', '简介', '豆瓣链接']
        self.style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'SimSun'  # 指定“宋体”
        self.style.font = font
        for i in range(len(first_row)):
            self.worksheet.write(0, i, first_row[i], self.style)

        self.row_num = 0

    def write_excel(self, data):
        for dict in data:
            self.row_num += 1
            self.worksheet.write(self.row_num, 0, self.row_num, self.style)
            for (key, val) in dict.items():
                if key == 'name':
                    self.worksheet.write(self.row_num, 1, val, self.style)
                if key == 'author':
                    self.worksheet.write(self.row_num, 2, val, self.style)
                if key == 'star':
                    self.worksheet.write(self.row_num, 3, val, self.style)
                if key == 'introduce':
                    self.worksheet.write(self.row_num, 4, val, self.style)
                if key == 'html':
                    self.worksheet.write(self.row_num, 5, val, self.style)

    def save_excel(self):
        self.workbook.save('书籍.xlsx')


excel =Excel()
conter = 1
for num in range(0,1000,20):
    html = ''.join(['https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=',str(num),'&type=T'])
    page = get_html(html)
    excel.write_excel(douban(page))
    print('已成功抓取第',int(conter),'页')
    conter += 1
    sleep(random.random()*0.5)

excel.save_excel()