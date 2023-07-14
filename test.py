#!/usr/bin/python3
# -*- coding: utf8 -*-

import base64
import time, subprocess
from playwright.sync_api import sync_playwright

# 打开本地浏览器[最大化无头模式]
command = r"/usr/bin/google-chrome-stable --remote-debugging-port=9222 --no-first-run --disable-component-update --disable-crash-reporter --disable-breakpad --disable-background-networking --disable-logging --no-report-upload --start-maximized --headless --no-sandbox"
subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(5)

playwright = sync_playwright().start()
# 连接已打开浏览器，找好端口
browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")
context = browser.new_context()
page = context.new_page()
page.goto("https://bot.sannysoft.com/")
t = page.locator("#webdriver-result").inner_text()
print(t) # 如果出现"missing (passed)"则未被检测到
# page.pause()

# 关闭浏览器
page.close()
