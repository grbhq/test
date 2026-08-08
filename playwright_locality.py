#!/usr/bin/python3
# -*- coding: utf8 -*-

from playwright.sync_api import sync_playwright


playwright = sync_playwright().start()
browser = playwright.chromium.launch(
    channel="chromium",
    headless=True,  # 无头模式
    args=['--start-maximized'],
    slow_mo=1000
)

context = browser.new_context()
page = context.new_page()

# 规避Webdriver检测[加载本地stealth.min.js文件]  #源仓库  https://github.com/requireCool/stealth.min.js
with open('./stealth.min.js') as f:
    js = f.read()
page.add_init_script(js)

page.goto("https://bot.sannysoft.com/")
t = page.locator("#webdriver-result").inner_text()
print(t) # 如果出现"missing (passed)"则未被检测到
