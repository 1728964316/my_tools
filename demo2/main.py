# 导入所需的模块
import os
from time import sleep

from DrissionPage import ChromiumPage  # 浏览器自动化模块
from cnocr import CnOcr  # OCR文字识别模块

# 创建浏览器页面对象
page = ChromiumPage()


# 爬虫入口函数
def start():
    global page

    # 输入爬取的书籍链接
    url = input("输入链接:")

    # 打开书籍链接
    page.get(url)

    # 如果图片保存路径不存在,则创建
    if not os.path.exists("./img"):
        os.makedirs("./img")

    # 点击"免费试读"按钮
    page.ele(
        'xpath://*[@id="routerView"]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/button[2]'
    ).click(by_js=None)

    # 检查是否已登录,未登录则重新登录
    while not page.ele(
        'xpath://*[@id="routerView"]/div[1]/div[2]/div[2]/div/div/img', timeout=0.5
    ):
        print("登录失败,重新登录")
        try:
            login()
        except:
            pass

    print("登录成功")

    # 获取书籍总页数
    pg_list_len = len(page.eles('xpath://*[@id="routerView"]/div[5]/div[2]/ul/li'))

    # 翻页截图
    for i in range(pg_list_len):
        change_pg(i)
        sleep(2.5)

    # OCR文字识别
    start_ocr(pg_list_len)


# 翻页函数
def change_pg(i):
    global page

    # 定位到当前页元素
    current_pg = page.ele(
        'xpath://*[@id="routerView"]/div[5]/div[2]/ul/li[{}]/div/span'.format(i + 1)
    )
    print(i)

    # 如果不是第一页,则截图保存
    if i > 0:
        page.get_screenshot(path="./img/{}.png".format(i), full_page=True)
        print(page.ele('xpath://*[@id="routerView"]/div[1]/div[2]/span/span[2]/text()'))

    # 点击"下一页"按钮
    page.ele('xpath://*[@id="routerView"]/div[2]/button[1]').click(by_js=None)

    # 点击当前页元素
    current_pg.click(by_js=None)


# 登录函数
def login():
    global page

    # 定位并点击"登录"按钮
    lg = page.ele('xpath://*[@id="routerView"]/div[1]/div[2]/div[2]/button')
    lg.click(by_js=None)
    lg.wait.not_covered()


# OCR识别函数
def start_ocr(pg):
    global page

    # 获取书名
    title = page.ele(
        'xpath://*[@id="routerView"]/div[1]/div[2]/span/span[1]/text()'
    )

    # 创建保存书名的目录
    if not os.path.exists("./{}".format(title)):
        os.makedirs("./{}".format(title))

    # 逐页进行OCR识别
    for i in range(1, pg):
        ocr = CnOcr(det_model_name="naive_det")
        res = ocr.ocr("./img/{}.png".format(i))
        content = ""
        for con in res:
            print(con["text"])
            content += con["text"]
        print(content)

        # 保存文字内容到文件
        with open("./{}/{}.doc".format(title, i), "w") as f:
            f.write(content)


if __name__ == "__main__":
    start()
