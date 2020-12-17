import requests
import re
import os
import json

#获取英雄图片
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
def getLOLImages():
    #获取js源代码
    url_js = requests.get('http://lol.qq.com/biz/hero/champion.js',headers)
    res_js = url_js.content
    html_js = res_js.decode()
    req = '"keys":(.*),"data"'#正则表达式 要提取在keys 和data之间的 （.*的全部内容）
    list_js = re.findall(req,html_js)
    dict_js = json.loads(list_js[0])#默认是list类型因此要提取0第一个放进去

    #获取英雄ID
    #拼接成对应的图片url
    list_ImageUrl = []
    for key in dict_js.keys():
        for i in range(20):
            num = str(i)
            if len(num) == 1:
                hero_num = "00" + num
            elif len(num) == 2:
                hero_num = "0" + num
            numstr = key + hero_num
            url = "https://game.gtimg.cn/images/lol/act/img/skin/big"+numstr+".jpg"
            list_ImageUrl.append(url)

    
    #命名         
    list_ImageName = []
    path = "D:\\爬虫python\\爬取图片\\"
    for name in dict_js.values():
        os.mkdir(path + name)  
        for i in range(20):
            file_path = path + name +"\\"+ name + str(i) + ".jpg"
            list_ImageName.append(file_path)

    #下载图片    
    for i in range(len(list_ImageUrl)):
        res = requests.get(list_ImageUrl[i])
        if res.status_code == 200:#404即不存在 200存在就存储
            print("正在下载" + list_ImageName[i])
            with open(list_ImageName[i],'wb') as f:
                f.write(res.content)
            
getLOLImages()
