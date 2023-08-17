import os
from DrissionPage import SessionPage
import httpx
from lxml import etree

# 设置默认输出格式为txt
form = "txt"
# 标题变量,用来存储小说名称
title = ""
page = SessionPage()

# 爬取页面内容的函数
def interview(url, pg):
    global title, form

    # 获取页面内容
    # response = httpx.get(url)
    page.get(url)
    # 将页面解析为HTML结构
    # root = etree.HTML(response.text)

    # 从页面中提取标题
    # pg_title = root.xpath("/html/body/div[2]/div[2]/div/div/div[2]/h1/text()")[0]
    pg_title = page.ele('xpath:/html/body/div[2]/div[2]/div/div/div[2]/h1/text()')
    # 打印爬取的章节名称和页数
    print("{}完成 (第{}页)".format(pg_title, pg))

    # 将标题和内容写入文件
    with open(
        "./{}/{}.{}".format(title, pg_title.strip(), form), "a", encoding="utf-8"
    ) as f:
        f.write(pg_title + "\n")

    # 提取正文内容
    # content = root.xpath('//*[@id="content"]/p/text()')
    content = page.eles('xpath://*[@id="content"]/p/text()')
    t = ""
    for i in content:
        t += "  " + i.strip() + "\n"

    # 将正文内容写入文件
    with open(
        "./{}/{}.{}".format(title, pg_title.strip(), form), "a", encoding="utf-8"
    ) as f:
        f.write(t)


# 计算小说章节数的函数
def count_pg(url):
    global title
    page.get(url)
    # 获取主页内容
    # response = httpx.get(url)
    # root = etree.HTML(response.text)

    # 提取小说书名作为目录名
    # title = root.xpath("/html/body/div[2]/div[2]/div[1]/div/div[2]/h1/text()")[
    #     0
    # ].strip()
    title = page.ele('xpath:/html/body/div[2]/div[2]/div[1]/div/div[2]/h1/text()').strip()
    print("开始爬取", title)

    # 创建书名目录
    if not os.path.exists("./{}".format(title)):
        os.makedirs("./{}".format(title))

    # 提取所有章节链接
    # result = root.xpath("//*[@id='booklist']/li/a/@href")
    result = page.eles('xpath://*[@id="booklist"]/li/a/@href')
    print("一共", len(result), "页")
    return result


def start():
    global form
    # 用户输入输出格式
    flag = input("输出格式(默认txt,回车跳过):")
    if flag != "":
        form = flag

    # 用户输入小说网址
    url = input("请输入网址: ")
    pg_url_list = count_pg(url)

    # 遍历所有章节链接
    index = 1
    for i in pg_url_list:
        interview(i, str(index))
        index += 1



start()
