
import requests
import json
from lxml import etree

def loadhtml(url,header):

    header = {'User-Agent': 'header'}

    r = requests.get(url,headers = header)

    print(r);

    return r.text
    
def pa(text,top):

    html = etree.HTML(text)

    names = html.xpath("//div[@class='board-item-main']/div[@class='board-item-content']/div[@class='movie-item-info']/p[@class='name']/a/text()")

    datas = {};

    b = html.xpath("//div[@class='board-item-main']/div[@class='board-item-content']/div[@class='movie-item-info']/p[@class='releasetime']/text()")


    for num in range(0,len(names)):

        datas["TOP"] = top

        top+=1

        datas["movie"] = names[num]

        datas["data"] = b[num]

        with open('movie.json','a',encoding = 'utf-8') as f:

            temp = json.dumps(datas,ensure_ascii=False) + ",\n"

            f.write(temp)
        

    return top

n = 0

top = 1;

for num in range(0,10):

    url =f'https://maoyan.com/board/4?offset={n}'

    header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"

    text = loadhtml(url,header)

    top = pa(text,top)

    top += 1

    n+=10


