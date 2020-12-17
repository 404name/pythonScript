# encoding:utf-8
import requests
import json
import base64
from PIL import Image
import time
# client_id 为官网获取的AK， client_secret 为官网获取的SK
client_id = "gab52985wt0xNWtKU5OlH8ra"
client_secret = "9phufY3SOZVkVU9ZkuSkQwddfuLkoz8A"
access_token = ""

def toJson(res):
    return json.loads(res.text)

def downloadUrl(IMAGE_URL,index):
    r = requests.get(IMAGE_URL)
    print(IMAGE_URL)
    print(r.content)
    with open('./image/img'+str(index)+'.png', 'wb') as f:
        f.write(r.content) 

#获取token
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
def getWords(url,turn):
    '''
    通用文字识别
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    if turn == 1:
        print(url)
        params = {"url":url}
    else:
        params = {"image":url}
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
    return ans

def transparence2white(img):
#     img=img.convert('RGBA')  # 此步骤是将图像转为灰度(RGBA表示4x8位像素，带透明度掩模的真彩色；CMYK为4x8位像素，分色等)，可以省略
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

if __name__ == "__main__":

    getAccessToken()
    
    url0 = "https://qn-st0.yuketang.cn/FmaAF31Hun5UUhxyLoRB4fm44sdG"
    print(getWords(url0,1))
    downloadUrl(url0,1);
    img=Image.open('./image/img1.png')
    img=transparence2white(img)
    # img.show()  # 显示图片
    img.save('./image/img1.png')  # 保存图片
    with open("./image/img1.png", 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
    print(getWords(s,2))

