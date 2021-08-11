import time
import json
import re

from selenium import webdriver
from lxml import html



# 获取cookies和token
class C_ookie:
    # 初始化
    def __init__(self):
        self.html = ''

    # 获取cookie
    def get_cookie(self):
        cooki  = {}
        url = 'https://mp.weixin.qq.com'
        Browner = webdriver.Chrome()
        Browner.get(url)
        time.sleep(10)
        # 获取账号输入框
        ID = Browner.find_element_by_name('account')
        # 获取密码输入框
        PW = Browner.find_element_by_name('password')
        # 输入账号
        id = '1192301911@qq.com'
        pw = 'jay139432685050.'
        # id = input('请输入账号:')
        # pw = input('请输入密码:')
        ID.send_keys(id)
        PW.send_keys(pw)
        # 获取登录button，点击登录
        Browner.find_element_by_class_name('btn_login').click()
        # 等待扫二维码
        time.sleep(10)
        cks = Browner.get_cookies()
        for ck in cks:
            cooki[ck['name']] = ck['value']
        ck1 = json.dumps(cooki)
        print(ck1)
        with open('ck.txt','w') as f :
            f.write(ck1)
            f.close()
        self.html = Browner.page_source

	# 获取token，在页面中提取
    def Token(self):
      #等待页面加载
        time.sleep(5)
        etree = html.etree
        h = etree.HTML(self.html)
        url = h.xpath('//a[@title="首页"]/@href')[0]
        print(url)
        token = re.findall('\d+',url)
        tokentxt = json.dumps(token)
        print(tokentxt)
        with open('token.txt', 'w') as f:
            f.write(tokentxt)
            f.close()


C = C_ookie()
C.get_cookie()
C.Token()