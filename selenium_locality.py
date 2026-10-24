#!/usr/bin/python3
# -*- coding: utf8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


s = Service(executable_path=ChromeDriverManager().install())  # 自动下载安装对应版本chromedriver
options = Options()
# 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
options.add_argument('--headless')  # 无头模式
options.add_argument('--no-sandbox')  # 关闭沙盒模式
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# options.add_experimental_option('detach', True)  # 不自动关闭浏览器
# options.binary_location = "/usr/bin/google-chrome-stable"  # 指定chromium浏览器路径

b = webdriver.Chrome(service=s, options=options)

# 规避Webdriver检测[加载本地stealth.min.js文件]  #源仓库  https://github.com/requireCool/stealth.min.js
with open('./stealth.min.js') as f:
    js = f.read()
b.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": js
})

b.get("https://bot.sannysoft.com/")
t = b.find_element(By.ID, 'webdriver-result').text
print(t)  # 出现"missing (passed)"则未被检测到
