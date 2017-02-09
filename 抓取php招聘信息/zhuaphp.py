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
    data = "first=false&pn="+str(page)+"&kd=php"
    data = bytes(data, encoding="utf8")
    request = Request(url=url, data=data, method='POST')
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0')

    #拉钩加了防爬机制，必须加入cookie才能爬
    request.add_header('Cookie', 'user_trace_token=20170209172336-6f3b908a-eea9-11e6-a05e-525400f775ce; LGUID=20170209172336-6f3b92ff-eea9-11e6-a05e-525400f775ce; index_location_city=%E6%88%90%E9%83%BD; TG-TRACK-CODE=search_code; JSESSIONID=0BBCF5B42BA3D916A50AD79DC3CDBD11; SEARCH_ID=c69b1b57758c467fb1b96110feb15797; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486632215; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486651276; _gat=1; _ga=GA1.2.205507885.1486632216; LGSID=20170209224116-cfeed274-eed5-11e6-8f66-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_php%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; LGRID=20170209224116-cfeed3ef-eed5-11e6-8f66-5254005c3644; _putrc=E1508FA9364724D7; login=true; unick=%E8%B5%B5%E9%B8%BF; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0')
    rs = urlopen(request).read().decode('utf-8')
    rs = json.loads(rs)
    # print(rs)
    list_con = rs['content']['positionResult']['result']
    info_list = []

    for i in list_con:
        rm = True
        for c in remove:
            if c == i['companyFullName']:
                print('removed:'+c)
                rm = False
            else:
                pass

        if rm:
            info = []
            info.append(i['positionName'])
            info.append(i['companyShortName'])
            info.append(i['companyFullName'])
            info.append(i['salary'])
            info.append(i['city'])
            info.append(i['education'])
            site = 'https://www.lagou.com/jobs/'+str(i['positionId'])+'.html'
            info.append(site)
            info_list.append(info)

    return info_list


def main():
    lang_name = 'php'
    page = 1
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false'
    info_result = []
    while page < 100:
        info = get_json(url, page, lang_name)
        info_result = info_result + info
        print("page" + str(page))
        page += 1
        sleep(random.random() * 0.4)
        print(info_result)
    wb = Workbook()
    ws1 = wb.active
    ws1.title = lang_name
    for row in info_result:
        ws1.append(row)
    wb.save('职位信息.xlsx')

if __name__ == '__main__':
    main()
