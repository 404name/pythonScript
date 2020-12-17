import os

import xlwt
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool

from pip._vendor import requests

j=1#定义全局变量,从第1行写入数据
def transform(string):#统一单位将单位万转为普通单位
    if string[-1]=='万':
        string1=string.replace('万','')
        return str(float(string1)*10000)
    else:
        return string

def singleweb(url):#爬取单页内容
    global j
    r=requests.get(url,headers=head)
    r.encoding=r.apparent_encoding
    r.raise_for_status()
    soup=BeautifulSoup(r.text,'html.parser')
    soups1=soup.find_all('div',class_='info')
    for soup1 in soups1:
        things=[]
        soup2=soup1.find('span',class_='type avid')
        things.append(soup2.text)
        soup3=soup1.find('span',class_='type hide')
        things.append(soup3.text)
        things.append(soup1.a.get('title'))
        things.append(transform(soup1.find('span',title='观看').text.replace('\n','').replace('\r','').replace(' ',''))) #去掉多余字符
        things.append(transform(soup1.find('span',title='弹幕').text.replace('\n','').replace('\r','').replace(' ','')))#去掉多余字符
        things.append(soup1.find('span',title='上传时间').text.replace('\n','').replace('\r','').replace(' ',''))#去掉多余字符
        things.append(soup1.find('span',title='up主').text.replace('\n','').replace('\r','').replace(' ',''))#去掉多余字符
        for k in range(0,7):
            sheet.write(j,k,things[k])
        print('\r正在爬取第'+str(j)+'条信息',end='')
        j=j+1
if __name__ == "__main__":
    try:
        os.makedirs('D://xlwt')#创早储存地址
    except:
        pass
    keyword=input('输入搜索关键词:')
    urls=[]
    print('爬取的信息将在操作完成后保存在D://xlwt里面')
    header=['av号','类型','标题','观看','弹幕','上传时间','up主']
    for i in range(1,51):#爬取50页，也是上限
        urls.append('https://search.bilibili.com/all?keyword='+keyword+f'&page={i}')
    head={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    book=xlwt.Workbook(encoding='utf-8')#建立excel工作区
    sheet=book.add_sheet('sheet1')
    for i in range(0,7):#写入表头
        sheet.write(0,i,header[i])
    for url in urls:
        singleweb(url)
    book.save('D://xlwt//'+keyword+'.xls')#保存内容
    print('\n操作完成')

