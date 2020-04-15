import re
import time
from multiprocessing.dummy import Pool
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

import requests
from faker import Faker
from bs4 import BeautifulSoup

# 避免被禁IP，一个站点一个线程 检测ip有效性时可以并发
# 全局记录域名是否有跑过 (list) 程序结束随Python进程结束再释放
# 函数内记录 url 是否有跑过 (list) 每跑完一个站点就清空

urls = list()
domains = list()
search_depth = 3

# 匹配proxy ip正则式
pattern_tags = re.compile(r'<[^>]+>', re.S)
pattern_blank = re.compile(r'\s+', re.S)
pattern_colon = re.compile(r' ', re.S)
pattern_ip = re.compile(r'(?:\d+\.){3}\d+:\d+')


def extract_proxy_ip(html):
    """
    匹配任意html页面的代理IP
    :param html:
    :return:
    """
    # 删除所有html标签
    text = pattern_tags.sub(' ', html)
    # 将空白符替换成空格
    text = pattern_blank.sub(' ', text)
    # 两数字之前的空格替换成冒号
    text = pattern_colon.sub(':', text)
    # 提取代理ip
    proxy_ip_lst = pattern_ip.findall(text)

    return proxy_ip_lst


def is_valid_proxy(ip, url=None, timeout=5):
    """
    校验代理ip是否能访问指定url（代理ip是否有效）
    :param ip: 127.0.0.1:8888
    :param url: https://www.baidu.com/
    :param timeout: 超时时间
    """
    url = url or 'https://www.baidu.com/'

    proxies = {
        'http': 'http://' + ip,
        'https': 'https://' + ip
    }

    try:
        ret = requests.get(url, proxies=proxies, timeout=timeout)
    except Exception as e:
        return False

    if 200 <= ret.status_code < 300:
        return ip


def webpage_opt(start_url, depth=0):
    domain = urlparse(start_url).netloc

    try:
        text = requests.get(start_url, headers={'User-Agent': Faker().user_agent()}).text
    except Exception as e:
        print(e)
        return domain, [], []

    links = [urljoin(start_url, line.get('href')) for line in BeautifulSoup(text).select('a')]
    ip_lst = extract_proxy_ip(text)

    # check proxy ip
    p = Pool(10)
    ret = p.map(is_valid_proxy, ip_lst)
    proxy_ips = [i for i in ret if i]

    print(start_url, f'{len(proxy_ips)} / {len(ip_lst)}')

    if depth <= search_depth:
        depth += 1
        for link in links:
            if link in urls or urlparse(link).netloc != domain:
                # 跑过的link 和 站外的link 都过滤
                continue
            urls.append(link)
            d, a, b = webpage_opt(link, depth)
            ip_lst += a
            proxy_ips += b

    return domain, ip_lst, proxy_ips


def catch():
    s = '代理 ip'
    page_count = 1

    pool = ThreadPoolExecutor(max_workers=5)
    # url = f'https://www.baidu.com/s?wd={s}&pn=10'

    ret = []

    for p in range(page_count):
        url = f'https://cn.bing.com/search?q={s}&first={p}1'  # 1，11，21，31，41，51
        res = requests.get(url, headers={'User-Agent': Faker().user_agent()})
        res.raise_for_status()

        bs = BeautifulSoup(res.text)
        links = [line.get('href') for line in bs.select('h2 a')]
        for link in links:
            domain = urlparse(link).netloc
            if domain in domains:
                continue
            domains.append(domain)
            ret.append(pool.submit(webpage_opt, link))
            break
        time.sleep(3)

    for r in ret:
        print('-' * 20)
        print(r.result())


if __name__ == '__main__':
    catch()
