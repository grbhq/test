import os, time
from datetime import datetime
from loguru import logger
import functools
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


# # co = ChromiumOptions().set_browser_path(r"/usr/bin/google-chrome-stable")
# co = ChromiumOptions()
# co.auto_port()
# co.set_timeouts(base=2)
# # 加载插件
# turnstilePatch = create_extension(plugin_path="turnstilePatch")
# co.add_extension(path=turnstilePatch)

# co.set_argument('--disable-blink-features=AutomationControlled')
# co.set_argument('--disable-infobars')
# co.set_argument('--no-sandbox')
# co.set_argument('--disable-gpu')

# browser = Chromium(co)
# # page = browser.get_tabs()[-1]
# page = browser.new_tab()
# # page.get("https://ping0.cc/geo")
# # print(page.ele('tag:body').text)
# # page.get("https://tls.browserleaks.com/json")
# # print(page.json)
# # page.get("https://turnstile.zeroclover.io/")
# page.get("https://linux.do/login")
# time.sleep(2)

def retry_decorator(retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(
                        f"函数 {func.__name__} 第 {attempt + 1}/{retries} 次尝试失败: {str(e)}"
                    )
                    if attempt == retries - 1:  # 最后一次尝试
                        logger.error(f"函数 {func.__name__} 最终执行失败: {str(e)}")
                    time.sleep(1)
            return None

        return wrapper

    return decorator

# @retry_decorator()
# def getTurnstileToken():
#     page.run_js("try { turnstile.reset() } catch(e) { }")

#     turnstileResponse = None
#     timeout = 20  ## 验证时间不能超过20s
#     start = datetime.now()
#     while (datetime.now() - start).total_seconds() < timeout:
#         try:
#             turnstile_response = page.run_js("try { return turnstile.getResponse() } catch(e) { return null }")
#             if turnstile_response:
#                 return turnstile_response
#             challenge_solution = page.ele("@name=cf-turnstile-response")
#             if not challenge_solution:
#                 logger.warning("未找到 cf-turnstile-response 元素，可能 Turnstile 尚未加载完成")
#                 continue
#             challenge_wrapper = challenge_solution.parent()
#             iframe = challenge_wrapper.shadow_root.ele("tag:iframe")
#             iframe_doc = iframe.ele("tag:body")
#             if iframe_doc.shadow_root:
#                 button = iframe_doc.shadow_root.ele("tag:input")
#                 if button:
#                     button.click()
#                     logger.info("已点击 Turnstile 验证按钮")
#         except Exception as e:
#             logger.warning(f"处理 Turnstile 时出错: {type(e).__name__}: {e}")
#         time.sleep(2)
#     # page.refresh()
#     raise Exception("处理 Turnstile 验证超时")


class LinuxDoBrowser:
    def __init__(self) -> None:
        # co = ChromiumOptions().set_browser_path(r"/usr/bin/google-chrome-stable")
        co = ChromiumOptions()
        co.auto_port()
        co.set_timeouts(base=2)
        turnstilePatch = create_extension(plugin_path="turnstilePatch")
        co.add_extension(path=turnstilePatch)
        co.set_argument('--disable-blink-features=AutomationControlled')
        co.set_argument('--disable-infobars')
        co.set_argument('--no-sandbox')
        co.set_argument('--disable-gpu')
        
        self.browser = Chromium(co)
        self.page = self.browser.new_tab()

    @retry_decorator()
    def getTurnstileToken(self):
        self.page.run_js("try { turnstile.reset() } catch(e) { }")

        turnstileResponse = None
        timeout = 15  ## 验证时间不能超过15s
        start = datetime.now()
        logger.info(f"验证计时开始：{start}")
        while (datetime.now() - start).total_seconds() < timeout:
            try:
                turnstileResponse = self.page.run_js("try { return turnstile.getResponse() } catch(e) { return null }")
                if turnstileResponse:
                    return turnstileResponse
                challengeSolution = self.page.ele("@name=cf-turnstile-response")
                if not challengeSolution:
                    logger.warning("未找到 cf-turnstile-response 元素，可能 Turnstile 尚未加载完成")
                    continue
                challengeWrapper = challengeSolution.parent()
                challengeIframe = challengeWrapper.shadow_root.ele("tag:iframe")
                challengeIframeBody = challengeIframe.ele("tag:body").shadow_root
                if challengeIframeBody:
                    challengeButton = challengeIframeBody.ele("tag:input")
                    if challengeButton:
                        challengeButton.click()
                        logger.info("已点击 Turnstile 验证按钮")
            except Exception as e:
                logger.warning(f"处理 Turnstile 时出错: {str(e)}")
            time.sleep(1)
        # self.page.refresh()
        raise Exception("处理 Turnstile 验证超时")

    def login(self):
        logger.info("开始登录")
        self.page.get("https://linux.do/login")
        time.sleep(2)
        turnstile_token = self.getTurnstileToken()
        logger.info(f"turnstile_token: {turnstile_token}")

start = LinuxDoBrowser()
start.login()
