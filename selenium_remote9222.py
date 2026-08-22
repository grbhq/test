import time, subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 不输出信息结束chrome进程
subprocess.call(["pkill", "-f", "chrome"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# 打开本地浏览器[最大化无头模式]
command = r"/usr/bin/google-chrome-stable --remote-debugging-port=9222 --no-first-run --disable-component-update --disable-crash-reporter --disable-breakpad --disable-background-networking --disable-logging --no-report-upload --start-maximized --headless --no-sandbox"
subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(5)

options = Options()
# 连接已打开浏览器，找好端口
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
b = webdriver.Chrome(service=Service(executable_path=r'/usr/bin/chromedriver'), options=options)

# 规避Webdriver检测[加载本地stealth.min.js文件]  #源仓库  https://github.com/requireCool/stealth.min.js
with open('./stealth.min.js') as f:
    js = f.read()
b.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": js
})

b.get("https://bot.sannysoft.com/")
t = b.find_element(By.ID, 'webdriver-result').text
print(t)  # 出现"missing (passed)"则未被检测到
