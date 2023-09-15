# coding=utf-8
# ！/usr/bin/env python
import json
import threading
import time
import requests as rq

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br"
}
testUrl = ' https://ipinfo.ipidea.io'

Active_Proxy = []
TIME_SLEEP = 5

# core function
def testPost(host, port):
    proxies = {
        'http': 'http://{}:{}'.format(host, port),
        'https': 'http://{}:{}'.format(host, port),
    }
    res = ""

    while True:
        try:
            res = rq.get(testUrl, proxies=proxies, timeout=5)
            # print(res.status_code)
            print(res.status_code, "***", res.text)
            if res.status_code == 200:
                Active_Proxy.append((host, port))
            break
        except Exception as e:
            print(e)
            break

    return


class ThreadFactory(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port

    def run(self):
        testPost(self.host, self.port)


#  extract poxy link from json
def getProxy():
    tiqu = 'extract Link (account and password)'

    while True:
        # Extract the 10 proxy link from the json and put them into the thread pool
        resp = rq.get(url=tiqu, timeout=5)
        try:
            if resp.status_code == 200:
                dataBean = json.loads(resp.text)
            else:
                print("Failed to get proxy")
                time.sleep(1)
                continue
        except ValueError:
            print("Failed to get proxy")
            time.sleep(1)
            continue
        else:
            # Parsing json arrays
            print("code=", dataBean["code"])
            code = dataBean["code"]
            if code == 0:
                threads = []
                for proxy in dataBean["data"]:
                    threads.append(ThreadFactory(proxy["ip"], proxy["port"]))
                for t in threads:  # Open thread
                    t.start()
                    time.sleep(0.01)
                for t in threads:  # Jam thread
                    t.join()
        with open('Active_Proxy.txt','w') as f:
            f.write(str(Active_Proxy),'w')  # write available proxies to proxy.txt and overwrite this file during each loop

        # break
        time.sleep(TIME_SLEEP)

