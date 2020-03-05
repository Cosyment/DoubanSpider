import requests
import lxml.etree
import threading
import Headers
import time
import ProxyValidator


class ProxySpider:

    # 获取西刺免费代理IP列表
    def getProxyByXiCi(self):
        print()
        print("开始抓取 西刺免费代理IP 网站ip列表")
        url = "https://www.xicidaili.com/wt/{}"
        header = dict()
        header["user-agent"] = Headers.get_header()

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
                    url = protocol + "://" + ip + ":" + port
                    if ProxyValidator.validate(protocol=protocol, ip=url):
                        self.inputFile(url)
            page += 1

    # 获取89代理IP列表
    def getProxyBy89(self):
        print()
        print("开始抓取 89IP 网站ip列表")
        url = "http://www.89ip.cn/index_{}.html"
        header = dict()
        header["user-agent"] = Headers.get_header()
        page = 1
        while True:
            r = requests.get(url.format(page), headers=header)
            r.raise_for_status()
            xml = lxml.etree.HTML(r.text)
            results = xml.xpath("//table[@class='layui-table']//tr")
            if len(results) <= 1:
                print("已爬取89所有代理IP列表")
                self.getProxyByXiCi()
                break
            for i in range(len(results)):
                if i > 0:
                    ip = str(results[i].xpath("td[1]/text()")[0]).strip()
                    port = str(results[i].xpath("td[2]/text()")[0]).strip()
                    print()
                    url = "http://" + ip + ":" + port
                    if ProxyValidator.validate(ip=url):
                        self.inputFile(url)
            page += 1

    def getProxyByFreeIP(self):
        print()
        print("开始抓取 FreeIP 网站ip列表")
        url = "https://www.freeip.top/?page={}"
        header = dict()
        header["user-agent"] = Headers.get_header()
        page = 1
        while True:
            r = requests.get(url.format(page), headers=header)
            r.raise_for_status()
            xml = lxml.etree.HTML(r.text)
            results = xml.xpath("//table[@class='layui-table']//tr")
            if len(results) <= 1:
                print("已爬取所有IP列表")
                self.getProxyBy89()
                break
            for i in range(len(results)):
                if i > 0:
                    ip = str(results[i].xpath("td[1]/text()")[0]).strip()
                    port = str(results[i].xpath("td[2]/text()")[0]).strip()
                    protocol = str(results[i].xpath("td[4]/text()")[0]).lower().strip()
                    url = protocol + "://" + ip + ":" + port
                    if ProxyValidator.validate(protocol=protocol, ip=url):
                        self.inputFile(url)
            page += 1

    def inputFile(self, ip):
        with open("ip.txt", "a") as file:
            print("写入文件")
            file.write(ip + "\n")

    def testThread(self, text):
        print(text)
        time.sleep(2)


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
        ProxyValidator.validate("http://" + ip + ":" + port)
    except:
        print("出错")
        return 1


if __name__ == "__main__":
    try:
        proxy = ProxySpider()
        threads = []
        t1 = threading.Thread(target=proxy.getProxyByXiCi())
        threads.append(t1)
        t2 = threading.Thread(target=proxy.getProxyByFreeIP())
        threads.append(t2)
        t3 = threading.Thread(target=proxy.getProxyBy89())
        threads.append(t3)

        for t in threads:
            t.setDaemon(True)
            t.start()
        # while True:
        #     menu()
    except Exception as ex:
        print(ex)
