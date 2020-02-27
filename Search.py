#!/usr/bin/env python
import requests
import lxml.etree
import time
from selenium import webdriver

sourselist = [
    "http://www.zuidazy2.net/index.php?m=vod-search"
]

class search:

    # 搜索电影
    def fetch(self, type, name):
        url = sourselist[0]
        try:
            if type == 1:
                self.openBrowser(name)
            else:
                print("搜索电影《{}》".format(name))
                r = requests.get("{}&wd={}".format(url, name))
                r.raise_for_status()
                xml = lxml.etree.HTML(r.text)
                results = xml.xpath("//span[@class='xing_vb4']")
                count = len(results)
                if count > 0:
                    print("搜索到《{}》共{}条数据".format(name, count))
                else:
                    print("没有找到任何有关《{}》的结果".format(name))
                    return 1
                for data in results:
                    print()
                    print("《{}》".format(data.xpath("a/text()")[0]))
                    url = data.xpath("a/@href")[0]
                    self.getMovieDetail("http://www.zuidazy2.net/index.php{}".format(url))
        except Exception as ex:
            print(ex)
            return 0

    # 打开浏览器搜索电影
    def openBrowser(self, name):
        chrome_path = '/usr/local/bin/chromedriver'
        drive = webdriver.Chrome(chrome_path)  # 打开谷歌浏览器
        drive.get(sourselist[0])  # 打开一个网址
        try:
            # 等待3秒  给予时间给浏览器加载javascript
            drive.implicitly_wait(3)
            # 通过xpath查找网页标签
            input_text = drive.find_element_by_class_name('search-text')
            # 设置搜索关键字
            input_text.send_keys(name)
            submit = drive.find_element_by_class_name('search-btn')
            # 执行搜索
            submit.click()
            results = drive.find_elements_by_class_name("xing_vb4")
            count = len(results)
            if count > 0:
                print("搜索到《{}》共{}条数据".format(name, count))
            else:
                print("没有找到任何有关《{}》的结果".format(name))
                return 1
            for i in range(count):
                print()
                result = results[i]
                print("《{}》".format(result.text))
                # 获取第一个子元素 a标签下href
                url = result.find_element_by_xpath("./*").get_property("href")
                time.sleep(2)
                self.getMovieDetail(url)

        except Exception as ex:
            print("搜索出错 {}".format(ex))

    def getMovieDetail(self, link):
        r = requests.get(link)
        r.raise_for_status()
        xml = lxml.etree.HTML(r.text)
        elements = xml.xpath("//div[contains(@id,'play_')]")
        for i in range(len(elements)):
            print("-----------------------播放地址{}-----------------------".format(i + 1))
            e = elements[i]
            play_urls = e.xpath("ul/li/input/@value")
            for url in play_urls:
                print("{}".format(url))

        print("-----------------------下载地址-----------------------")
        download_elements = xml.xpath("//div[contains(@id,'down_')]")
        for e in download_elements:
            download_urls = e.xpath("ul/li/input/@value")
            for url in download_urls:
                print("{}".format(url))


def menu():
    print()
    print("""----------------------电影搜索程序----------------------
1.默认搜索
2.浏览器搜索
0.--退出--
             """)
    try:
        type = int(input("请输入搜索类型（0-2）:"))
        if type < 0 or type > 2:
            print("输入有误，请重新输入（0-2）")
            return 1
        elif type == 1:
            return default()
        elif type == 2:
            return browser()
        else:
            return 0
    except:
        print("输入有误，请重新输入 (0-2)")
        return 1


def browser():
    text = str(input("请输入电影名称："))
    if text == '':
        print("请输入电影名称")
        return 1
    else:
        search().fetch(1, text)
        return 1


def default():
    text = input("请输入电影名称：")
    if text == '':
        print("请输入电影名称")
        return 1
    else:
        search().fetch(0, text)
        return 1


if __name__ == '__main__':
    while True:
        type = menu()
        if type == 0:
            break
