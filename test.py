import requests
from tqdm import tqdm
headers = {
    'Host': 'd.apkpure.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,fr;q=0.6',
    'Cookie': '_apk_uid=Ez4mbacZW364ctxFP3MRJF3Ac6MCf89w; _user_tag=j%3A%7B%22language%22%3A%22en%22%2C%22source_language%22%3A%22en-US%22%2C%22country%22%3A%22US%22%7D; apkpure__lang=en; apkpure__country=US; _qimei=attabCssnHMpfCBkfxXcmZPWZ1GQ5DzF; apkpure__policy_review=20180525; g_state={"i_p":1694725888128,"i_l":1}; apkpure__sample=0.2574366447269034; _dt_sample=0.98051251492111; _dt_referrer_fix=0.5161414180404527; _tag_sample=0.037033851418904806; _home_article_entry_sample=0.06621880720403395; _related_recommend=0.1378872668213047; _download_detail_sample=0.0022168397817023955; _f_sp=1010271661; _gid=GA1.2.1926060329.1695929186; m1=19629; m2=1f0bb65136aa6447805f92823e77e48c; download_id=no_1406001684941259; _client_id=GA1.1.1848787690.1694717925; _apk_sid=1.1.1695929184941.3.9.1695930646853.-480; _ga=GA1.1.1848787690.1694717925; _ga_NT1VQC8HKJ=GS1.1.1695929186.4.1.1695930649.58.0.0',
    'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}
PROXIES = {
    "http": "http://172.67.27.160:80",
}

response = requests.get('https://d.apkpure.com/b/APK/com.theuptimes?version=latest',proxies=PROXIES, headers=headers)
total_size = int(response.headers.get('content-length', 0))
chunk_size = 1024  # 1 KB

file_path = './test.apk'

# Download the file and save it chunk by chunk
with open(file_path, 'wb') as f:
    for chunk in tqdm(response.iter_content(chunk_size),
                      total=total_size // chunk_size, unit='KB'):
        if chunk:  # filter out keep-alive chunks
            f.write(chunk)
