#============================================================
# Create Time:  		2019-07-15 22:48:33
# Writer:				Wenhao	1795902848@qq.com
# File Name:			LOLSpider.py
# File Type:			PY Source File
# Tool:					Mac -- vim & python
# Information:  		爬取LOL官网上的所有英雄皮肤，存到当前文件夹中
#============================================================
#coding=utf-8
import requests
import json
import re
import sys

class LOLSpider():
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    def getHeroDetail(this)->None:
        url = 'https://lol.qq.com/biz/hero/champion.js'
        r = requests.get(url = url, headers = this.headers)
        rawContent = r.content.decode('utf-8')
        this.herosDetail = json.loads(rawContent[50:-1])

    def getSkins(this)->list:
        '''
        返回皮肤的url，以及皮肤的名字
        第一级元素是英雄级别
        第二级元素是单个英雄的皮肤级别
        第三级元素是皮肤url和皮肤名字。比如：(url, 腥红之月 亚托克斯)
        '''
        skinBaseUrl = 'https://ossweb-img.qq.com/images/lol/web201310/skin/big'
        skins = []
        for title in this.herosDetail['keys'].values():
            jsUrl = 'https://lol.qq.com/biz/hero/'+title+'.js'
            r = requests.get(jsUrl, this.headers)
            rawContent = r.content.decode('utf-8')
            hero = json.loads(re.search('(.*?\=){2}(\{.*\})', rawContent).group(2))
            skins.append([(skinBaseUrl+i['id']+'.jpg', i['name'] if i['name'] != 'default' else this.herosDetail['data'][title]['name']) for i in hero['data']['skins']])
        return skins

    def saveSkins(this):
        for aHero in this.getSkins():
            for skinUrl, name in aHero:
                try:
                    name = re.sub('/', '／', name)#文件名中不能有`/`符号，要把半角替换为全角
                    r = requests.get(skinUrl, this.headers)
                    with open(name+'.jpg', 'wb') as f:
                        f.write(r.content)
                    print('Saved', name)
                except(KeyboardInterrupt):
                    sys.exit(0)
                except:
                    print('Filed to save', name)

    def run(this):
        this.getHeroDetail()
        this.saveSkins()

if __name__ == '__main__':
    spider = LOLSpider()
    spider.run()
