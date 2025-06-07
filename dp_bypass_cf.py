import os, time
from DrissionPage import Chromium, ChromiumOptions
from pyvirtualdisplay import Display


display = Display(size=(1920, 1080))
display.start()

def create_extension(plugin_path=None):
    # 创建Chrome插件的manifest.json文件内容
    manifest_json = """
{
    "manifest_version": 3,
    "name": "Turnstile Patcher",
    "version": "2.1",
    "content_scripts": [
        {
            "js": [
                "./script.js"
            ],
            "matches": [
                "<all_urls>"
            ],
            "run_at": "document_start",
            "all_frames": true,
            "world": "MAIN"
        }
    ]
}
    """

    # 创建Chrome插件的script.js文件内容
    script_js = """
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// old method wouldn't work on 4k screens

let screenX = getRandomInt(800, 1200);
let screenY = getRandomInt(400, 600);

Object.defineProperty(MouseEvent.prototype, 'screenX', { value: screenX });

Object.defineProperty(MouseEvent.prototype, 'screenY', { value: screenY });
    """

    # 创建插件目录并写入manifest.json和script.js文件
    os.makedirs(plugin_path, exist_ok=True)
    with open(os.path.join(plugin_path, "manifest.json"), "w+") as f:
        f.write(manifest_json)
    with open(os.path.join(plugin_path, "script.js"), "w+") as f:
        f.write(script_js)

    return os.path.join(plugin_path)


co = ChromiumOptions().set_browser_path(r"/usr/bin/google-chrome-stable")
co.auto_port()
co.set_timeouts(base=2)
# 加载插件
turnstilePatch = create_extension(plugin_path="turnstilePatch")
co.add_extension(path=turnstilePatch)

co.set_argument('--disable-blink-features=AutomationControlled')
co.set_argument('--disable-infobars')
co.set_argument('--no-sandbox')
co.set_argument('--disable-gpu')

browser = Chromium(co)
page = browser.get_tabs()[-1]
page.get("https://ping0.cc/geo")
print(page.ele('tag:body').text)
# page.get("https://tls.browserleaks.com/json")
# print(page.json)
# page.get("https://turnstile.zeroclover.io/")
page.get("https://linux.do/login")


def getTurnstileToken():
    page.run_js("try { turnstile.reset() } catch(e) { }")

    turnstileResponse = None
    for i in range(0, 10):
        try:
            turnstileResponse = page.run_js("try { return turnstile.getResponse() } catch(e) { return null }")
            if turnstileResponse:
                return turnstileResponse

            challengeSolution = page.ele("@name=cf-turnstile-response")
            challengeWrapper = challengeSolution.parent()
            challengeIframe = challengeWrapper.shadow_root.ele("tag:iframe")
            challengeIframeBody = challengeIframe.ele("tag:body").shadow_root
            challengeButton = challengeIframeBody.ele("tag:input")
            challengeButton.click()
            # time.sleep(5)
            # page.get_screenshot(path='tmp', name='pic.jpg', full_page=True)
        except Exception as e:
            print(f"处理 Turnstile 时出错: {str(e)}")
        time.sleep(1)
    page.refresh()
    # raise Exception("failed to solve turnstile")

print(getTurnstileToken())
