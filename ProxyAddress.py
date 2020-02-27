import requests
import random
import lxml.etree

headerlist = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;  Trident/5.0)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B100 Safari/602.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0']


class ProxyAddress:

    # 获取西刺免费代理IP列表
    def getProxyByXiCi(self):
        url = "https://www.xicidaili.com/nn/{}"
        header = dict()
        header["user-agent"] = random.choice(headerlist)

        page = 1
        while True:
            r = requests.get(url.format(page), headers=header)
            r.raise_for_status()
            xml = lxml.etree.HTML(r.text)
            results = xml.xpath("//table[@id='ip_list']//tr")
            if len(results) <= 1:
                print("已爬取西刺所有代理IP列表")
                break
            for i in range(len(results)):
                if i > 0:
                    data = results[i]
                    ip = str(data.xpath("td[2]/text()")[0]).strip()
                    port = str(data.xpath("td[3]/text()")[0]).strip()
                    protocol = str(data.xpath("td[6]/text()")[0]).lower()
                    print()
                    if self.checkAvailable(protocol, ip, port):
                        self.inputFile(protocol + "://" + ip + ":" + port)
            page += 1

    # 获取89代理IP列表
    def getProxyBy89(self):
        url = "http://www.89ip.cn/index_{}.html"
        header = dict()
        header["user-agent"] = random.choice(headerlist)
        page = 1
        while True:
            r = requests.get(url.format(page), headers=header)
            r.raise_for_status()
            xml = lxml.etree.HTML(r.text)
            results = xml.xpath("//table[@class='layui-table']//tr")
            if len(results) <= 1:
                print("已爬取89所有代理IP列表")
                break
            for i in range(len(results)):
                if i > 0:
                    ip = str(results[i].xpath("td[1]/text()")[0]).strip()
                    port = str(results[i].xpath("td[2]/text()")[0]).strip()
                    print()
                    if self.checkAvailable("http", ip, port):
                        self.inputFile("http://" + ip + ":" + port)
            page += 1

    def getProxyByFreeIP(self):
        url = "https://www.freeip.top/?page={}"
        header = dict()
        header["user-agent"] = random.choice(headerlist)
        page = 1
        while True:
            r = requests.get(url.format(page), headers=header)
            r.raise_for_status()
            xml = lxml.etree.HTML(r.text)
            results = xml.xpath("//table[@class='layui-table']//tr")
            if len(results) <= 1:
                print("已爬取所有IP列表")
                break
            for i in range(len(results)):
                if i > 0:
                    ip = str(results[i].xpath("td[1]/text()")[0]).strip()
                    port = str(results[i].xpath("td[2]/text()")[0]).strip()
                    protocol = str(results[i].xpath("td[4]/text()")[0]).lower().strip()
                    if self.checkAvailable(protocol, ip, port):
                        self.inputFile(protocol + "://" + ip + ":" + port)
            page += 1

    # 验证ip有效性
    def checkAvailable(self, protocol, ip, port):
        print()
        print("-------------------开始检测IP是否可用-------------------")
        url = ip + ":" + port
        print("{}://{}".format(protocol, url))
        # check_url = "https://www.ip.cn"
        check_url = "http://www.baidu.com"
        header = dict()
        header["user-agent"] = random.choice(headerlist)
        proxies = {'http': 'http://' + url, 'https': 'https://' + url}
        try:
            r = requests.get(check_url, headers=header, proxies=proxies, timeout=10)
            if r.status_code == 200:
                print("IP地址可用")
                return True
            else:
                print("无效IP地址")
                return False
        except Exception as ex:
            print("无效IP地址")
            print(ex)
            return False

    def inputFile(self, ip):
        with open("ip.txt", "a") as file:
            print("写入文件")
            file.write(ip + "\n")


def menu():
    print()
    print("--------------------手动检测IP有效性--------------------")

    try:
        ip = str(input("请输入IP地址:"))
        if ip == '':
            print("请输入有效ip")
            return 1
        port = str(input("请输入端口号:"))
        if port == '':
            print("请输入有效端口号")
            return 1
        ProxyAddress().checkAvailable(ip, port)
    except:
        print("出错")
        return 1


if __name__ == "__main__":
    # ProxyAddress().getProxyByXiCi()
    # ProxyAddress().getProxyBy89()
    ProxyAddress().getProxyByFreeIP()
    # while True:
    #     menu()
