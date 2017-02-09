import xlrd
import xlwt
from xlutils.copy import copy

class Excel:
    def __init__(self):
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.worksheet = self.workbook.add_sheet('小说')
        first_row = ['序号','书名','作者、出版社、价格','评分','简介','豆瓣链接']
        self.style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'SimSun'  # 指定“宋体”
        self.style.font = font
        for i in range(len(first_row)):
            self.worksheet.write(0,i,first_row[i],self.style)

        self.row_num = 0


    def write_excel(self,data):
        for dict in data:
            self.row_num += 1
            self.worksheet.write(self.row_num,0,self.row_num,self.style )
            for (key,val) in dict.items():
                if key == 'name':
                    self.worksheet.write(self.row_num,1,val,self.style)
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


A = Excel()
A.save_excel()


