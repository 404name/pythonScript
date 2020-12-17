from pip._vendor import requests
import re
import time
import json

def get_info():
    headers = {
        'Host': 'api.bilibili.com',
        'Referer': 'https://www.bilibili.com/video/av77413543',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    info = 'https://api.bilibili.com/x/web-interface/archive/stat?aid=' + av
    info_rsp = requests.get(url=info, headers=headers)
    info_json = info_rsp.json()

    with open(av + '_info.txt', 'w', encoding='utf-8') as fp:
        if info_json['code'] == 0:
            fp.write('播放量: {}\n'.format(info_json['data']['view']))
            fp.write('弹幕量: {}\n'.format(info_json['data']['danmaku']))
            fp.write('收藏数: {}\n'.format(info_json['data']['favorite']))
            fp.write('硬币数: {}\n'.format(info_json['data']['coin']))
            fp.write('分享数: {}\n'.format(info_json['data']['share']))
            fp.write('点赞数: {}\n'.format(info_json['data']['like']))

            print('播放量:', info_json['data']['view'])
            print('弹幕量:', info_json['data']['danmaku'])
            print('点赞数:', info_json['data']['like'])
            print('收藏数:', info_json['data']['favorite'])
            print('硬币数:', info_json['data']['coin'])
            print('转发数:', info_json['data']['share'])
        fp.write('\n')
        comment_url = 'https://api.bilibili.com/x/v2/reply'
        page = 1
        while True:
            now_time = int(time.time() * 1000)
            param = {
                'callback': 'jQuery17205146934182044087_' + str(now_time),
                'jsonp': 'jsonp',
                'pn': page,
                'type': '1',
                'oid': av,
                'sort': '2',
                '_': now_time
            }
            rsp = requests.get(url=comment_url, headers=headers, params=param)
            rsp_str = rsp.text.replace('jQuery17205146934182044087_' + str(now_time) + "(", '').strip(')')
            com_json = json.loads(rsp_str)
            print()
            if com_json['code'] == 0:
                try:
                    replies = com_json['data']['replies']
                    print('当前{}页'.format(page))
                    for replie in replies:
                        # print(replie)
                        print('{}\n{}\n'.format('昵称: ' + replie['member']['uname'],
                                                '评论内容：' + replie['content']['message']))
                        fp.write('{}\n{}\n'.format('昵称: ' + replie['member']['uname'],
                                                   '评论内容：' + replie['content']['message']))
                    page += 1
                    time.sleep(1)
                except Exception as e:
                    break
# av = '77413543'
av = input('请输入av号：')
get_info()
