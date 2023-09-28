#!/usr/bin/env python
# coding: utf-8
import time
import requests
from tqdm import tqdm
import os
import json
from random import uniform
from concurrent.futures import ThreadPoolExecutor
import threading

dir_name = "APP"
current_path = os.getcwd()
directory_path = os.path.join(current_path, dir_name)

DATA_DIRECTORY = "./data/"
TATGET_PATH = "./APP/"

# URL1 = 'https://d.apkpure.com/b/XAPK/'
URL2 = 'https://d.apkpure.com/b/APK/'
VERSION = '?version=latest'
HEADERS = {
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

LOOP_CTRL = 10
# IP_POOL = "Active_Proxy.txt"
SLEEP_TIME = 3
MAX_THREAD = 1

STOP_THRESHOLD = 100 * (1024**1)  # e.g., 10 MB
stop_script = False

def monitor_space():
    global stop_script
    while not stop_script:
        used_space = get_directory_size(TATGET_PATH)
        print(f"Used space: {used_space} bytes")
        if used_space > STOP_THRESHOLD:
            print("Space exceeded. Stopping script!")
            stop_script = True
        time.sleep(10)  # Check every 10 seconds
def get_directory_size(path='./APP/'):
    """Return the total size of the directory in bytes."""
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_directory_size(entry.path)
    return total

def json_walker(data_directory):
    json_files = []
    # Walk through the directory
    for dirpath, dirnames, filenames in os.walk(data_directory):
        for filename in filenames:
            # Check if the file has a .json extension
            if filename.endswith('.json'):
                full_path = os.path.join(dirpath, filename)
                json_files.append(full_path)

    return json_files

def assessment(file_path):  # evaluate valid app's numbers
    app_count = 0
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            #   get all valid apps' number
            valid_n = int(data.get("count", {}).get("valid"))
            app_count = app_count + valid_n
    except Exception as e:
        print(f"Error reading JSON file {file_path}: {e}")
    return app_count


def read_each_json(file_path):

    """
    Extract item names  both valid_apps.

    Parameters:
    - data: Dictionary containing the JSON data

    Returns:
    - A list of tuples with item's key and its name field
    """

    results = []
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

            for key, value in data['valid_apps'].items():
                # only donwload free apks 
                # if value['price']==0 :
                #     results.append((key, value['name']))
                results.append((key, value['name']))
            return results
    except Exception as e:
        print(f"Error reading JSON file {file_path}: {e}")


def download(id,target_path):
    url = URL2 + id + VERSION
    print('Downloading from: ' + url)
    r = requests.get(url, headers=HEADERS,proxies=PROXIES,stream=True)
    r.raise_for_status()

    total_size = int(r.headers.get('content-length', 0))
    chunk_size = 1024  # 1 KB

    file_path = os.path.join(target_path, id + '.apk')

    # Download the file and save it chunk by chunk
    with open(file_path, 'wb') as f:
        for chunk in tqdm(r.iter_content(chunk_size), total=total_size // chunk_size, unit='KB'):
            if chunk:  # filter out keep-alive chunks
                f.write(chunk)
    # sleep for a while
    sleep_time = uniform(0, SLEEP_TIME)
    print("Sleeping for " + str(sleep_time) + " seconds")
    time.sleep(sleep_time)


def download_wrapper(m):
    try:
        print("Downloading "+str(m[0])+" ...")
        download(m[0],TATGET_PATH)
    except Exception as e :
        print("Downloading "+str(m[0])+" failed"+str(e))
        sleep_time = uniform(0, SLEEP_TIME)
        time.sleep(sleep_time)

"""
    For further work, an IP pool is neccessary, but for test stage, it's not that urgent
"""
# def switch_id(id_pool):
#     with open("id_pool.txt",'r') as f:

if __name__ == '__main__':
    json_paths = json_walker(DATA_DIRECTORY)
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
        print("Directory " , directory_path ,  " Created ")

    print("Total json files: "+str(len(json_paths)))
    # Evaluate workload
    for iter in range(LOOP_CTRL):
        cur_path = json_paths[iter]
        counts = assessment(cur_path)
    # Open each file and get all valid names
    monitor_thread = threading.Thread(target=monitor_space)
    monitor_thread.start()

    for i in tqdm(range(len(json_paths))):
         if stop_script:
            exit(0)
         jsonpath = json_paths[i]
         app_urls = read_each_json(jsonpath)
         for m in app_urls:
             with ThreadPoolExecutor(max_workers=MAX_THREAD) as executor:
                 executor.map(download_wrapper, app_urls)

    print("Download Completed!")