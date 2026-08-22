import time, subprocess
import requests

# 打开本地浏览器[最大化无头模式]
command = r"/usr/bin/google-chrome-stable --remote-debugging-port=9222 --no-first-run --disable-component-update --disable-crash-reporter --disable-breakpad --disable-background-networking --disable-logging --no-report-upload --start-maximized --headless --no-sandbox"
subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(5)

# 检查是否监听成功
try:
    r = requests.get("http://127.0.0.1:9222/json")
    if r.status_code == 200:
        print("🎉 Chrome 已成功在 9222 端口监听调试协议。")
    else:
        print("⚠️ Chrome 启动后未能访问 9222 端口。")
except Exception as e:
    print(f"❌ 无法访问 Chrome 调试端口: {e}")

# process 变量是 Chrome 进程，你可以选择不退出，保持进程运行
