import time
import json
import random
import csv

from selenium import webdriver
from lxml import html
import requests
import re
from http import cookiejar


# 获取文章
class getEssay:

    def __init__(self):
        # 获取cookies
        with open('ck.txt', 'r') as f:
            cookie = f.read()
            f.close()
        self.cookie = json.loads(cookie)

        # 获取token
        self.header = {
            "HOST": "mp.weixin.qq.com",
            "User-Agent": 'Mozilla / 5.0(WindowsNT6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 74.0.3729.131Safari / 537.36'
        }
        m_url = 'https://mp.weixin.qq.com'
        response = requests.get(url=m_url, cookies=self.cookie)
        print(response)
        self.token = 969637498  ## 填入token.txt保存的token信息。
        print(self.token)
        # fakeid与name
        self.fakeid = []

    # 获取公众号信息
    def getGname(self):
        # 请求头
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'mp.weixin.qq.com',
            'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=%d&lang=zh_CN' % int(
                self.token),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        # 地址
        url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
        # query = input('请输入要搜索的公众号关键字:')
        # begin = int(input('请输入开始的页数:'))
        query = 'Tableau社区'
        begin = 0
        begin *= 5
        # 请求参数
        data = {
            'action': 'search_biz',
            'token': self.token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': ' 1',
            'random': random.random(),
            'query': query,
            'begin': begin,
            'count': '1'
        }
        # 请求页面，获取数据
        res = requests.get(url=url, cookies=self.cookie, headers=headers, params=data)
        print(res.text)
        name_js = res.text
        name_js = json.loads(name_js)
        list = name_js['list']
        for i in list:
            time.sleep(1)
            fakeid = i['fakeid']
            nickname = i['nickname']
            print(nickname, fakeid)
            self.fakeid.append((nickname, fakeid))

    # 获取文章url
    def getEurl(self, begin):

        url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'mp.weixin.qq.com',
            'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=%d&lang=zh_CN' % int(
                self.token),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # 遍历fakeid，访问获取文章链接
        for i in self.fakeid:
            time.sleep(1)
            fake = i[1]
            data = {
                'token': self.token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': begin,
                'count': 5,
                'fakeid': fake,
                'type': 9
            }
            res = requests.get(url, cookies=self.cookie, headers=headers, params=data)
            js = res.text
            print(js)
            link_l = json.loads(js)
            self.parJson(link_l)

    # 解析提取url
    def parJson(self, link_l):
        l = link_l['app_msg_list']
        for i in l:
            link = i['link']
            link = self.getVideo(link)
            name = i['title']
            self.saveData(name, link)

    # 保存数据进csv中
    def saveData(self, name, link):
        with open('link.csv', 'a', encoding='utf8') as f:
            w = csv.writer(f)
            w.writerow((name, link))
            print('ok')

    def getVideo(self, url):
        # 请求要下载的url地址
        html = requests.get(url)
        # content返回的是bytes型也就是二进制的数据。
        # 我用的是正则，也可以使用xpath
        jsonRes = html.text  # 匹配:wxv_1105179750743556096
        dirRe = r"wxv_.{19}"
        result = re.search(dirRe, jsonRes)
        if result:
            wxv = result.group(0)

            print(wxv)
            print(html)

            # 页面播放形式
            video_url = "https://mp.weixin.qq.com/mp/readtemplate?t=pages/video_player_tmpl&auto=0&vid=" + wxv
            print("video_url", video_url)

            # 页面可下载形式
            video_url_temp = "https://mp.weixin.qq.com/mp/videoplayer?action=get_mp_video_play_url&preview=0&__biz=MzU1MTg5NTQxNA==&mid=2247485507&idx=4&vid=" + wxv
            response = requests.get(video_url_temp)
            content = response.content.decode()
            content = json.loads(content)
            print(content)
            url_info = content.get("url_info")
            if url_info:
                video_url2 = url_info[0].get("url")
                print(video_url2)
                return video_url2
            else:
                return ""

        else:
            return ""


if __name__ == '__main__':
    G = getEssay()
    G.getGname()
    for num in range(0, 20):
        time.sleep(1)
        G.getEurl(num * 5)
