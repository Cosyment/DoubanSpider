import random
import requests
import lxml.etree
from time import sleep
import json
import Headers
import ProxyValidator
from enum import Enum
from db.dao import CrawlRecordDao, HotMovieDao, BestMovieDao, MovieDao
from selenium import webdriver


class InsertType(Enum):
    HOT_MOVIE = 0  # 最新热门电影
    BEST_MOVIE = 1  # 豆瓣250榜单电影
    ALL_MOVIE = 2  # 全部电影


# ---------分 --割 --线 -------------------
# 豆瓣爬虫类
# 豆瓣网 [url=https://movie.douban.com/]https://movie.douban.com/[/url]
# 豆瓣TOP250电影榜 [url=https://movie.douban.com/top250?start=0&filter=]https://movie.douban.com/top250?start=0&filter=[/url]
class Spider:
    proxies = []
    path = ""  # 文件下载路径
    insert_enabled = True  # 是否将数据插入数据库
    download_enabled = True  # 是否下载预告片
    pageSize = 20  # 默认每页大小

    # 构造函数 设置预告片存储路径 是否下载预告片？ 是否插入数据表？
    def __init__(self, path, download_enabled, insert_enabled):
        self.path = path
        self.download_enabled = download_enabled
        self.insert_enabled = insert_enabled
        self.get_proxies_ip()

    # 遍历页面
    def foreach(self):
        print()
        print("豆瓣电影TOP250榜电影")
        i = 0
        while i < 10:
            # 遍历
            # flag 为获取当前页电影链接返回的值 如果为1则遍历下一页 不为1继续遍历本页
            flag = self.foreachPageUrl(i)
            if flag == 1:
                i += 1
            elif flag == 0:
                print("重新访问当前页")
            else:
                print("服务器拒绝，爬虫终止")
                break

    # 豆瓣250 获取当前页电影链接
    def foreachPageUrl(self, page):
        url = "https://movie.douban.com/top250?start={}&filter=".format(page * 25)
        header = dict()
        header["user-agent"] = Headers.get_header()
        r = None
        try:
            # 通过requests.get()方法 获取网页信息
            r = requests.get(url, headers=header)
            r.raise_for_status()  # 网页状态码 200 2开头表示正常 4或5开头的抛出异常
            # 使用lxml将网页的源码转换成xml，然后使用xpath（）进行xml解析
            xml = lxml.etree.HTML(r.text)
            # 获取xml下类名为hd的div标签下的所有a标签的href属性  href装着电影链接url
            a = xml.xpath("//div[@class='hd']/a/@href")
            i = 0
            count = page * 25 + 1
            while i < (len(a)):
                print("TOP {}".format(count))
                # 遍历当前页面的所有电影链接
                self.random_delay("准备获取电影详情 {}")
                flag = self.getMovieDetail(count, a[i], InsertType.BEST_MOVIE)
                sleep(3)  # 休息两秒 应付反爬
                if flag == 1:
                    i += 1
                    count += 1
                    print("")
                elif flag == 0:
                    print("重新获取电影详细信息")
                else:
                    print("服务器拒绝，爬虫终止")
                    break
            return 1
        except Exception as ex:
            print("爬取异常 {}".format(ex))
            if r.status_code == 403:
                return -1
            else:
                return 0

    # 获取分类下全部影片(网页版)
    def getAllMoviesByHtml(self):
        chrome_path = '/usr/local/bin/chromedriver'
        # os.environ['webdriver.chrome.driver'] = chrome_path#设置系统环境变量
        drive = webdriver.Chrome(chrome_path)  # 打开谷歌浏览器
        # 打开一个网址
        # drive.get('https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start='.format(page))
        # drive.get('https://movie.douban.com/tag/#/'.format(page))
        drive.get('https://movie.douban.com/tag/#/?sort=U&range=0,20&tags=电影')
        try:
            # 通过xpath查找网页标签
            drive.implicitly_wait(self.random_delay("准备爬取网页信息"))  # 等待5秒
            a = drive.find_elements_by_class_name("item")
            i = 0
            while i < 9999999:
                print("------------------------第{}条数据，已加载{}条数据------------------------".format((i + 1), len(a)))
                url = a[i].get_attribute("href")
                print()
                self.random_delay("准备获取电影详情 {}")
                self.getMovieDetail(0, url, 1)
                if i == len(a) - 18:
                    self.random_delay("准备爬取下一页 {}")
                    # 页面滚动到底部，解决查看更多不可见时点击无效问题
                    drive.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    more = drive.find_element_by_class_name("more")
                    more.click()

                    drive.implicitly_wait(5)
                    b = drive.find_elements_by_class_name("item")
                    # b = drive.find_element_by_xpath("//div[@class='list-wp']")

                    print("加载更多 {}".format(b[0].text))
                    # sleep(self.randomDelay())
                i += 1
        except Exception as ex:
            print(ex)
            return 0

    # 获取分类下全部影片(api版)
    def getAllMoviesByApi(self):
        print()
        print("开始爬取豆瓣全部电影")
        url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=电影&start={}"
        header = dict()
        start_page = 0  # 豆瓣api开始页
        is_reject = False  # 服务器是否拒绝访问
        header["user-agent"] = Headers.get_header()
        try:
            count = 1  # 当前已爬取总条数
            # 查询是否有失败记录
            record = CrawlRecordDao.query()
            if record is not None:
                start_page = record.page
                count += start_page

            while True:  # 爬取一页数据
                if is_reject:
                    break
                print("----------------------加载第{}页,start_page {}----------------------".format(
                    int(count / self.pageSize) + 1,
                    start_page))
                r = requests.get(url.format(start_page), headers=header, proxies={'http': self.random_proxies_ip()})
                r.raise_for_status()
                result = json.loads(r.content.decode('utf-8'))
                # 判断结果是否包含data 数组
                if 'data' in result:
                    datas = result['data']
                else:
                    print("爬取异常中止 result {}".format(result))
                    CrawlRecordDao.insert(0, start_page, '')
                    break

                if len(datas) == 0:
                    print("加载完毕")
                    break
                size = len(datas)
                for i in range(size):  # 爬取每页数据中的详情
                    print()
                    print("------------------------第{}条数据------------------------".format(count))
                    data = datas[i]
                    name = data['title']
                    self.random_delay("准备获取《" + name + "》电影详情 {}")
                    flag = 1
                    proxies_count = len(self.proxies)  # 获取代理ip数量
                    if proxies_count == 0:
                        proxies_count = 1
                    for _ in range(proxies_count):  # 获取电影详情数据，失败重试3次
                        flag = self.getMovieDetail(data['url'], InsertType.ALL_MOVIE)
                        if flag == 1:  # 详情页抓取成功
                            break
                        else:
                            if proxies_count > 1:  # 服务器拒绝抓取失败时，重新更换ip抓取
                                print()
                                print("重新抓取详情数据")
                            else:
                                CrawlRecordDao.insert(i, start_page, name)
                                break

                    if flag == -1:
                        CrawlRecordDao.insert(i, start_page, name)
                        print("服务器拒绝，爬虫终止")
                        is_reject = True
                        break
                    if i == size - 1:
                        print()
                        self.random_delay("准备爬取下一页 {}")
                        page = int(count / self.pageSize)
                        start_page = int(self.pageSize * page)
                    count += 1
        except Exception as ex:
            print("爬取异常 {}".format(ex))
            return 0

    # 搜索豆瓣电影
    def searchMovie(self, name):
        chrome_path = '/usr/local/bin/chromedriver'
        # os.environ['webdriver.chrome.driver'] = chrome_path#设置系统环境变量
        drive = webdriver.Chrome(chrome_path)  # 打开谷歌浏览器
        # 打开一个网址
        drive.get('https://movie.douban.com/subject_search?search_text={}&cat=1002'.format(name))
        try:
            # 通过xpath查找网页标签
            drive.implicitly_wait(3)  # 等待3秒
            a = drive.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/a')
            url = a.get_attribute('href')
            a.click()  # 点击连接
            # 获取电影详细信息
            self.getMovieDetail(url, InsertType.HOT_MOVIE)
            drive.implicitly_wait(5)  # 等待5秒
        except Exception as ex:
            print(ex)
            # drive.close()  # 关闭页面

    # 最新上映电影
    def getLatestReleases(self):
        chrome_path = '/usr/local/bin/chromedriver'
        # os.environ['webdriver.chrome.driver'] = chrome_path#设置系统环境变量
        drive = webdriver.Chrome(chrome_path)  # 打开谷歌浏览器
        drive.get('https://movie.douban.com/')  # 打开一个网址
        try:
            # 等待3秒  给予时间给浏览器加载javascript
            drive.implicitly_wait(3)
            # 通过xpath查找网页标签
            a = drive.find_elements_by_xpath('//*[@id="screening"]/div[2]/ul/li/ul/li[1]/a')
            # 定义一个集合 用来存储最新上映电影链接地址
            s = set()
            for i in a:
                s.add(i.get_attribute("href"))
            print("最新上映的电影有{}个".format(len(s)))
            l = list(s)  # set转为list
            drive.implicitly_wait(3)  # 等待3秒
            for i in range(len(l)):
                print()
                print("第{}个".format(i + 1))
                # 获取电影详细信息
                self.getMovieDetail(l[i], 1)
                print()
        except Exception as ex:
            print(ex)
        # drive.close()#关闭页面

    # 最近热门电影
    def getHots(self):
        chrome_path = '/usr/local/bin/chromedriver'
        # os.environ['webdriver.chrome.driver'] = chrome_path#设置系统环境变量
        drive = webdriver.Chrome(chrome_path)  # 打开谷歌浏览器
        drive.get('https://movie.douban.com/')  # 打开一个网址
        try:
            # 等待3秒  给予时间给浏览器加载javascript
            drive.implicitly_wait(3)
            # 通过xpath查找网页标签
            a = drive.find_elements_by_xpath('//*[@id="content"]/div/div[2]/div[4]/div[3]/div/div[1]/div/div//a')
            # 定义一个集合 用来存储最近热门电影链接地址
            s = set()
            for i in a:
                s.add(i.get_attribute("href"))
            l = list(s)  # set转为list
            print("最近热门电影有{}个".format(len(l)))
            for i in range(len(l)):
                print()
                print("第{}个".format(i + 1))
                # 获取电影详细信息
                self.getMovieDetail(l[i], InsertType.HOT_MOVIE)
                print()
            drive.implicitly_wait(3)  # 等待3秒
        except Exception as ex:
            print(ex)
            # drive.close()#关闭浏览器

    # 获取电影详细信息
    def getMovieDetail(self, url, insertType):  # insert_flag 0 热门电影，1 豆瓣250电影，2 全部电影
        print("豆瓣电影链接:{}".format(url))
        header = dict()
        # 获取请求头的user-agent字典，应付反爬处理
        header["user-agent"] = Headers.get_header()
        director = ''  # 导演
        writer = ''  # 编剧
        actors = ''  # 主演
        type = ''  # 类型
        release_date = ''  # 上映日期
        duration = ''  # 时长
        IMDb = ''  # IMDb链接
        text = ''  # 简介
        trailer = ''  # 预告片
        r = None
        try:
            # 通过requests.get获取url链接
            r = requests.get(url, headers=header, proxies={'http': self.random_proxies_ip()})
            r.raise_for_status()  # 网页状态码 200
            xml = lxml.etree.HTML(r.text)  # 将网页源码转为xml 用lxml库进行解析
            # 获取电影名
            n = xml.xpath("//div[@id='content']/h1/span")  # 通过xpath获取网页标签
            name = str(n[0].text)
            print("片名:{}".format(name))
            year = str(n[1].text).replace("(", "").replace(")", "")
            print("年份:{}".format(year))
            rating = xml.xpath("//strong[@class='ll rating_num']/text()")[0]
            print("评分:{}".format(rating))
            cover = xml.xpath("//div[@id='mainpic']/a/img/@src")[0]
            print("海报:{}".format(cover))
            div1 = xml.xpath("//div[@id='info']//span[@class='attrs']")
            for i in range(len(div1)):
                if i == 0:
                    # 获取电影导演
                    x1 = div1[0].xpath("a")
                    for i in x1:
                        director += i.text + " "
                elif i == 1:
                    # 获取电影编剧
                    x2 = div1[1].xpath("a")
                    for i in range(3):
                        if i >= len(x2):
                            break
                        writer += x2[i].text + " "
                elif i == 2:
                    # 获取电影的前几个主演
                    x3 = div1[2].xpath("a")
                    for i in range(5):
                        if i >= len(x3):
                            break
                        actors += x3[i].text + " "
            # 以上这么写原因：有些电影无编剧 无主演 健壮代码
            print("导演:{}".format(director))
            print("编剧:{}".format(writer))
            print("主演:{}".format(actors))
            # 获取电视;类型
            x4 = xml.xpath("//span[@property='v:genre']")
            for i in x4:
                type += i.text + " "
            print("类型:{}".format(type))
            # 获取电视上映日期
            x5 = xml.xpath("//span[@property='v:initialReleaseDate']")
            for i in x5:
                release_date += i.text + " "
            print("上映日期:{}".format(release_date))
            # 获取电影片长
            x6 = xml.xpath("//span[@property='v:runtime']")
            for i in x6:
                duration += i.text + ' '
            print("片长:{}".format(duration))
            # 获取电影的IMDb链接
            div2 = xml.xpath("//div[@id='info']/a/@href")
            if len(div2) != 0:
                IMDb = div2[0]
            print("IMDb链接:{}".format(IMDb))
            # 获取电影简介
            x7 = xml.xpath("//span[@property='v:summary']/text()")
            for i in range(len(x7)):
                text += "  " + x7[i].strip()
                if i < len(x7) - 1:
                    text += '\n'
            print("简介:\n{}".format(text))
            # 获取预告片链接
            video = xml.xpath("//a[@title='预告片']/@href")
            if len(video) >= 1:
                trailer = video[0]
                print("预告片链接:{}".format(trailer))
                if self.download_enabled:
                    for _ in range(3):  # 预告片下载失败时，重试3次
                        # 前往预告片链接页面，获取预告片的播放地址，实现下载预告片功能
                        if self.getMovieTrailer(name, video):
                            break
                        else:
                            print("重新获取电影预告片")
            else:
                # 有些电影没有预告片，数据库插入数据
                # 根据mysql来决定是否将数据插入数据表中
                print("该电影找不到预告片")

            if self.insert_enabled:
                if insertType == InsertType.HOT_MOVIE:
                    MovieDao.insert(name, cover, rating, year, director, writer, actors, type, release_date, duration,
                                    text, trailer)
                elif insertType == InsertType.BEST_MOVIE:
                    BestMovieDao.insert(name, cover, rating, year, director, writer, actors, type, release_date,
                                        duration, text, trailer)
                else:
                    MovieDao.insert(name, cover, rating, year, director, writer, actors, type, release_date, duration,
                                    text, trailer)
                return 1
        except Exception as ex:
            print("无法访问电影详细信息 {}".format(ex))
            if r.status_code == 403:
                return -1
            else:
                return 0

    # 获取电影预告片
    def getMovieTrailer(self, name, url):
        header = dict()
        header['user-agent'] = Headers.get_header()
        try:
            r = requests.get(url, headers=header)
            xml = lxml.etree.HTML(r.text)
            # 预告片页面使用了javascript特性，预告片url地址藏在了<script></script>内
            # 获取到指定的script标签后，对script标签下代码转换成字符串后进行字符串处理
            # 处理后便可以获取到预告片的实际播放地址url
            # 获取url后便可以进行下载操作，获取不到返回0表示该电影没有预告片
            script = xml.xpath("//script[@type='application/ld+json']/text()")
            str1 = str(script)
            start = str1.find("http://vt1")
            end = str1.find(".mp4")
            result = str1[start:end + 4]
            # 根据download_enabled开关来决定是否下载预告片
            if self.download_enabled:
                self.random_delay("准备下载预告片 {}")
                # 下载预告片
                if self.download(name, result):
                    return True
                else:
                    print("下载失败，重新下载")
            else:
                return False
        except Exception as ex:
            print("无法获取电影预告片 {}".format(ex))
            return False

    # 下载预告片
    def download(self, name, url):
        header = dict()
        header['user-agent'] = Headers.get_header()
        try:
            r = requests.get(url, headers=header, timeout=30)
            # 处理一下文件名 有些电影名中带 /\*:"?<>| ，windows中的文件名是不能有这些字符
            NAME = ''
            for i in range(len(name)):
                if name[i] not in '/\*:"?<>|':
                    NAME += name[i]
                else:
                    NAME += ""
            filename = self.path + '\\' + NAME + ".mp4"  # 预告片路径
            print("保存路径:{}".format(filename))
            # 通过二进制写入文件
            with open(filename, 'wb') as f:
                f.write(r.content)
                f.close()  # 关闭流
            print("下载成功")
            return True
        except:
            print("下载电影预告片失败")
            return False

    # 处理爬虫默认2-15s随机延迟
    def random_delay(self, str):
        delay = random.randint(2, 15)
        while True:
            if delay == 0:
                # 清除倒计时提示
                print("\r", end="", flush=True)
                break
            else:
                delay -= 1
                # 开始倒计时提示 覆盖打印 清空end 默认"\n"
                print("\r" + str.format(delay), end="", flush=True)
                sleep(1)

    # 从ip列表中随机取一个ip
    def random_proxies_ip(self):
        while True:
            if len(self.proxies) == 0:
                break
            ip = str(random.choice(self.proxies)).strip()
            # if ip.startswith("http://"):
            if ip.startswith("https://") and ProxyValidator.validate(ip):
                # if ip.startswith("https://"):
                print("有效代理ip {}".format(ip))
                return ip

            # 处理已失效ip
            else:
                original_ip = ip + "\n"
                self.proxies.remove(original_ip)  # 删除内存中proxies中的ip
                if len(self.proxies) <= 5:
                    self.get_proxies_ip()
                self.del_proxies_ip(original_ip)  # 删除文件中ip

    # 读取本地文件中的ip
    def get_proxies_ip(self):
        with open("ip.txt", "r") as file:
            self.proxies = file.readlines()
            file.close()

    # 根据ip删除ip.txt中数据
    def del_proxies_ip(self, text):
        with open("ip.txt", "r") as file:
            lines = file.readlines()
            file.close()
        with open('ip.txt', 'w') as file:
            for line in lines:
                if text == line:
                    continue
                file.write(line)
            file.close()

    def testProxy(self):
        url = "http://httpbin.org/ip"
        header = dict()
        header["user-agent"] = Headers.get_header()
        proxies_ip = random.choice(self.proxies)
        print("random ip {}".format(proxies_ip))
        proxies = {'http': proxies_ip, 'https': proxies_ip}
        r = requests.get(url, headers=header, proxies=proxies)
        # r = requests.get(url, headers=header)
        r.raise_for_status()
        print(r.text)


# ---------------------------

# ----------------分割线-----------
# 菜单函数
def menu():
    print("""------------------主-----菜-----单--------------------------
         1 豆瓣TOP250榜电影
         2 豆瓣全部电影
         3 豆瓣最新上映电影
         4 豆瓣最近热门电影
         5 豆瓣动态搜索电影
         6 查询数据库中电影
         0   退-出-爬-虫
    """)
    try:
        i = int(input("输入操作（0-6）："))
        if i < 0 or i > 6:
            print("操作有误，重新操作")
            # Spider("", False, False).testProxy()
            return 1
        if i == 0:
            return 0
        if i == 6:
            return sql_menu()  # 次级带单2
        s = child_menu()  # 次级菜单1
        if s != 0:
            if i == 1:
                s.foreach()  # 执行豆瓣电影TOP250榜遍历函数
            elif i == 2:
                # s.getAllMoviesByHtml()
                s.getAllMoviesByApi()
            elif i == 3:
                s.getLatestReleases()  # 获取豆瓣最新上映电影
            elif i == 4:
                s.getHots()  # 获取豆瓣最近热门电影
            elif i == 5:
                s.searchMovie(input("输入电影关键词："))  # 豆瓣搜索电影
        else:
            print("操作有误，重新操作")
            return 1
        return 1
    except:
        print("输入有误，请按规定输入数字")


# 二级菜单1 获取spider爬虫类对象
def child_menu():
    print("""------------------次---级---菜---单-----------------------
        1 不下载电影预告片，数据库不存储电影信息
        2 下载电影预告片，数据库存储电影信息
        3 数据库只存储电影信息
        4 只下载电影预告片
        """)
    try:
        i = int(input("输入操作（1-4）："))
        if i == 1:
            return Spider("", False, False)  # 返回一个spider类对象
        elif i == 2:
            return Spider(input("输入预告片存储路径："), True, True)  # 返回一个spider类对象
        elif i == 3:
            return Spider("", False, True)
        elif i == 4:
            return Spider(input("输入预告片存储路径："), True, False)  # 返回一个spider类对象
        else:
            print("操作有误，返回上一级")
            return 0
    except:
        print("输入有误，请按规定输入数字")
        return 0


# 二级菜单2  查询数据库电影信息
def sql_menu():
    print("""------------------次---级---菜---单-----------------------
        1 电影名查询
        2 类型查询
    """)
    try:
        i = int(input("输入操作（1-2）："))
    except:
        print("输入有误，请按规定输入数字")
        return 0
    try:
        if i == 1:
            MovieDao.searchByName(input("输入查询电影名关键字："))
        elif i == 2:
            MovieDao.searchByType(input("输入查询电影类型关键字："))
        else:
            print("操作有误，返回上次菜单")
        return 1
    except:
        print("查询异常")
        return 0


# ----------------分----割----线-----------
# 主函数
if __name__ == '__main__':
    while True:
        print()
        flag = menu()  #
        if flag == 0:
            break
        sleep(3)
