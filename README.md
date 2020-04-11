### proxy_pool(自用)
Proxy IP pool for Python3 

Github上其实已经有很多IP代理池了，但为何还要多造这个轮子呢？
1. 爬取的网站资源比较少，需要自己写扩展才能获取更多的资源；
2. 很多都是通用性代理IP，需要自己二次校验；
3. 满足自己个性化需求，想怎么扩展就怎么扩展；
4. 总的来说就是Github上面的都不好用，用着很是不爽，看我来造个差劲更难用的！

当前爬取的网站主要如下：
1. 云代理 www.ip3366.net
2. 旗云代理 http://www.qydaili.com/
3. unknown http://www.goubanjia.com
4. 快代理 http://www.kuaidaili.com/free/inha/
5. 89免费代理 http://www.89ip.cn/index_1.html
6. IP海代理 http://www.iphai.com/free/ng
7. 极速代理 http://www.superfastip.com/welcome/freeip/1
8. 西刺代理  https://www.xicidaili.com/nn/
9. 西拉免费代理IP  http://www.xiladaili.com/https/1/  可用率比较高有反爬限制
10. http://www.nimadaili.com/gaoni/  可用率比较高有反爬限制
11. http://ip.kxdaili.com/ipList/1.html#ip
12. http://31f.cn/
13. http://www.shenjidaili.com/shareip/    http代理(处理方式不一致, 未处理)
14. http://www.66ip.cn/areaindex_19/1.html   有反爬限制，js动态加载
15. http://feilongip.com/
16. http://www.dlnyys.com/free/

环境要求：
```
Python3.6+
```
环境准备：
```
pip install requests faker redis
```
开始爬取：
1. 按自个情况修改 ProxyPool.py __init__() 参数
2. 启动爬虫：python3 ProxyPool.py

使用demo：
```
# 结合ProxyPool 中的 get_proxy_ip 方法使用
import requests
from ProxyPool import ProxyPool

proxy_ip = ProxyPool().get_proxy_ip()

proxies = {
    'http': 'http://' + proxy_ip,
    'https': 'https://' + proxy_ip
}
res = requests.get('https://baidu.com/', proxies=proxies, timeout=5)
```
