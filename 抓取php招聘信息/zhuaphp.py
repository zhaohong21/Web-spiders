from urllib.request import urlopen,Request
from time import sleep
import random
import re
import json
from openpyxl import Workbook

text = open('remove.txt', encoding='UTF-8')
text = text.read()
pat = '[0-9]+\s+([\u4e00-\u9fa5]+)\n*\s*\r*,*'

remove = re.findall(pat,text)

def get_json(url, page, lang_name):
    data = "{'first': 'true', 'pn': "+str(page)+", 'kd': "+lang_name+"}"
    data = bytes(data, encoding="utf8")
    request = Request(url=url, data=data, method='POST')
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')
    request.add_header('Content-Type', 'application / json;charset = UTF - 8')
    #拉钩加了防爬机制，必须加入cookie才能爬
    request.add_header('Cookie', '_gat=1; user_trace_token=20170209172336-6f3b908a-eea9-11e6-a05e-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=; LGUID=20170209172336-6f3b92ff-eea9-11e6-a05e-525400f775ce; JSESSIONID=0BBCF5B42BA3D916A50AD79DC3CDBD11; _putrc=E1508FA9364724D7; login=true; unick=%E8%B5%B5%E9%B8%BF; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; TG-TRACK-CODE=index_search; SEARCH_ID=c23cac9345f14777af9e4a3d727ea83a; index_location_city=%E6%88%90%E9%83%BD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486632215; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486632638; _ga=GA1.2.205507885.1486632216; LGSID=20170209172336-6f3b918a-eea9-11e6-a05e-525400f775ce; LGRID=20170209173038-6b0efd01-eeaa-11e6-8f66-5254005c3644')

    rs = urlopen(request).read().decode('utf-8')
    print(rs)
    rs = json.loads(rs)
    list_con = rs['content']['positionResult']['result']
    info_list = []

    for i in list_con:
        for c in remove:
            if c == i['companyFullName']:
                pass
            else:
                info = []
                info.append(i['companyShortName'])
                info.append(i['companyFullName'])
                info.append(i['salary'])
                info.append(i['city'])
                info.append(i['education'])
                info.append(i['positionId'])
                info_list.append(info)
    return info_list


def main():
    lang_name = input('职位名：')
    page = 1
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false'
    info_result = []
    while page < 31:
        info = get_json(url, page, lang_name)
        info_result = info_result + info
        page += 1
        print("page"+ str(page))
        sleep(random.random() * 0.4)
    wb = Workbook()
    ws1 = wb.active
    ws1.title = lang_name
    for row in info_result:
        ws1.append(row)
    wb.save('职位信息.xlsx')

if __name__ == '__main__':
    main()
