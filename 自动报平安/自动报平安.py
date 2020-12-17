import requests
from bs4 import BeautifulSoup


# ****************��¼*******************

# �Լ����˺�����
# 0��ͷ��Ҫ���ַ���
username = '2019112404'
password = '285017'

logUrl = "http://yiqing.ctgu.edu.cn/wx/index/loginSubmit.do"

header = {
    # origin:http://yiqing.ctgu.edu.cn
    # "Content-Type": "application/json;charset=UTF-8",
    'Referer': "http://yiqing.ctgu.edu.cn/wx/index/login.do?currSchool=ctgu&CURRENT_YEAR=2019",
    # ģ�¹ȸ�������ĵ�¼
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
}

yiqingSession = requests.session()

postData = {
    "username": username,
    "password": password
}

responseRes = yiqingSession.post(logUrl, data=postData, headers=header)

# *******���ύҳ���ȡ ����Ϣ**********

# ��������Ĭ�����彡��)
postData = {
    "ttoken":  '',
    "province":  "",
    "city":      "",
    "district":  "",
    "adcode":    "",
    "longitude": "0",
    "latitude":  "0",
    "sfqz": "��",
    "sfys": "��",
    "sfzy": "��",
    "sfgl": "��",
    "status": "1",
    "sfgr": "��",
    "szdz": "",
    "sjh": "",
    "lxrxm": '',
    "lxrsjh": '',
    "sffr": "��",
    "sffy": "��",
    "sfgr": "��",
    "qzglsj": '',
    "qzgldd": '',
    "glyy": '',
    "mqzz": '',
    "sffx": "��",
    "qt": "",
}

getFormurl = "http://yiqing.ctgu.edu.cn/wx/health/toApply.do"
responseRes = yiqingSession.get(getFormurl)

# ��ȡ��Ҫ��Ϣ�����
soup = BeautifulSoup(responseRes.text, "html.parser")
getFormlist = soup.find_all('input')[0:15]

for Formdata in getFormlist:
    postData[Formdata.attrs['name']] = Formdata.attrs['value']

# *************�ύ���ձ�***********

postFormurl = "http://yiqing.ctgu.edu.cn/wx/health/saveApply.do"

header['Referer'] = "http://yiqing.ctgu.edu.cn/wx/health/toApply.do"

responseRes = yiqingSession.post(postFormurl, data=postData, headers=header)

print(responseRes.text)
