import requests
import json
import re
import base64
import time
import os
from PIL import Image
from lxml import etree
ansWord = [' ','A','B','C','D','E','F','G','H','I','J','K']
# client_id 为官网获取的AK， client_secret 为官网获取的SK
client_id = "gab52985wt0xNWtKU5OlH8ra"
client_secret = "9phufY3SOZVkVU9ZkuSkQwddfuLkoz8A"
access_token = ""

def downloadUrl(IMAGE_URL,name):
    localUrl = './image/img'+name+'.png';
    if os.path.exists(localUrl):
        print(localUrl+"已存在")
    else:
        r = requests.get(IMAGE_URL,timeout = 500)
        with open(localUrl, 'wb') as f:
            f.write(r.content)
        print(localUrl)

def toJson(res):
    return json.loads(res.text)

def getAccessToken():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
    response = requests.get(host)
    if response:
        res = toJson(response)
        print(res['access_token'])
        global access_token
        access_token = res['access_token']
       
#1 直接识别网路url
#2 识别本地图片
#2 下载url到本地图片再识别
def getWords(name,url,turn = 3):
    '''
    通用文字识别
    '''
    #print(url)
    
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    if turn == 1:
        params = {"url":url}
    elif turn == 2:
        params = {"image":url}
    else :
        downloadUrl(url,name);

        #将图片透明度改成白色
        name = './image/img'+name+'.png'
        img=Image.open(name)
        img=transparence2white(img)
        # img.show()  # 显示图片
        img.save(name)  # 保存图片
        with open(name, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            s = base64_data.decode()
        params = {"image":s}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'text/html; charset=utf-8'}
    response = requests.post(request_url, data=params, headers=headers)
    ans = ""
    if response:
        #防止过快百度直接给你挤出来
        res = toJson(response)
        while ('words_result'not in res):
            response = requests.post(request_url, data=params, headers=headers)
            res = toJson(response)
            time.sleep(0.5)
        for words in res['words_result']:
            ans += words['words']
    print(ans)
    return ans

def pa(text,texti):
    endAns = []
    html = etree.HTML(text)
    answers = html.xpath("/html/body/div[2]/div/div[@class='quiz-answer']/div[@class='answer sheet-answer']/p/text()");
    i = 0
    flag = 1;
    name = str(texti) + str(flag)
    for ans in answers:
        if ans.find("正确答案")!=-1:
            dict = {}
            divId = 'answersheet_link' + str(i+1)
            print("问题"+str(i+1))
            i += 1;
            imgUrls = html.xpath("/html/body/div[2]/div/div[@id='"+divId+"']/div[@class='pptimg']/@style")
            question = re.findall(r"background: url\((.+?)\) ", imgUrls[0])
            name = str(texti) + str(flag)
            flag+=1
            dict.setdefault('题目',getWords(name,question[0]))
            time.sleep(0.3)
            #print(question)
            for index in range(1,len(imgUrls)):
                #print(re.findall(r"background: url\((.+?)\) ", imgUrls[index]))
                name = str(texti) + str(flag)
                flag+=1
                dict.setdefault('选项'+ansWord[index],getWords(name,re.findall(r"background: url\((.+?)\) ", imgUrls[index])[0]))
                time.sleep(0.3)
                #print((re.findall(r"background: url\((.+?)\) ", imgUrls[index]))[0])
            dict.setdefault('答案',ans)
            endAns.append(dict)
    print(endAns)
    json_str = json.dumps(endAns,indent=4,ensure_ascii=False)

    # Open new json file if not exist it will create
    with open('test_data'+str(texti)+'.json', 'w',encoding = 'utf-8') as json_file:
        json_file.write(json_str)
                #填充进去
            #A = re.findall(r"background: url\((.+?)\) ", imgUrls[i*5+1])
            #B = re.findall(r"background: url\((.+?)\) ", imgUrls[i*5+2])
            #C = re.findall(r"background: url\((.+?)\) ", imgUrls[i*5+3])
            #D = re.findall(r"background: url\((.+?)\) ", imgUrls[i*5+4])
            #i = i + 1
            #question1 = getWords(question)
            #time.sleep(0.5)
            #AA = getWords(A)
            #time.sleep(0.5)
            #BB = getWords(B)
            #time.sleep(0.5)
            #CC = getWords(C)
          #time.sleep(0.5)
            #DD = getWords(D)
            #time.sleep(0.1)
            #endAns[i] = {'题目': question1,
            #                    '选项A': AA,
            #                    '选项B': BB,
            #                    '选项C': CC,
            #                    '选项D': DD,
            #                    '答案': ans}
            #填充进去
            
    

def transparence2white(img):
#   img=img.convert('RGBA')  # 此步骤是将图像转为灰度(RGBA表示4x8位像素，带透明度掩模的真彩色；CMYK为4x8位像素，分色等)，可以省略
    sp=img.size
    width=sp[0]
    height=sp[1]
    print(sp)
    for yh in range(height):
        for xw in range(width):
            dot=(xw,yh)
            color_d=img.getpixel(dot)  # 与cv2不同的是，这里需要用getpixel方法来获取维度数据
            if(color_d[3]==0):
                color_d=(255,255,255,255)
                img.putpixel(dot,color_d)  # 赋值的方法是通过putpixel
    return img

getAccessToken()
#url0 = "https://qn-st0.yuketang.cn/FuUwOoiiY8kgYNqSrKHqkzO8NMS7"
#print(getWords(url0))

for i in range(6,7):
    with open("C:\\Users\\404name\\Desktop\\马原\\saved_resource"+str(i)+".html", "r",encoding = 'utf-8') as f:  # 打开文件
        text = f.read()
    pa(text,i)




