import requests
import Headers


def validate(protocol=None, ip=None):
    if ip is None:
        print("请输入有效ip地址 {} ".format(ip))
        return False
    if protocol is None:
        protocol = 'http'
    print()
    print("-------------------开始检测IP是否可用-------------------")
    print("验证ip {} ".format(ip))
    header = dict()
    header["user-agent"] = Headers.get_header()
    proxies = {'http': ip, 'https': ip}
    try:
        r = requests.get(protocol + "://www.baidu.com", headers=header, proxies=proxies, timeout=5)
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
