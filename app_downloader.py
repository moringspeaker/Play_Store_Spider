#!/usr/bin/env python
# coding: utf-8
import time
import requests
from tqdm import tqdm
import os
import json
from random import uniform
from concurrent.futures import ThreadPoolExecutor

DATA_DIRECTORY = "./data/"
TATGET_PATH = "./APP/"

URL = 'https://d.apkpure.com/b/XAPK/'
VERSION = '?version=latest'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

LOOP_CTRL = 10
# IP_POOL = "Active_Proxy.txt"
SLEEP_TIME = 3
MAX_THREAD = 5
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
    url = URL + id + VERSION
    print('Downloading from: ' + url)
    r = requests.get(url, headers=HEADERS,stream=True)
    r.raise_for_status()

    total_size = int(r.headers.get('content-length', 0))
    chunk_size = 1024  # 1 KB

    if not os.path.exists(target_path):
        # If not, create the directory
        os.makedirs(target_path)
    file_path = os.path.join(target_path, id + '.xapk')

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
    except:
        print("Downloading "+str(m[0])+" failed")


"""
    For further work, an IP pool is neccessary, but for test stage, it's not that urgent
"""
# def switch_id(id_pool):
#     with open("id_pool.txt",'r') as f:

if __name__ == '__main__':
    json_paths = json_walker(DATA_DIRECTORY)
    print("Total json files: "+str(len(json_paths)))
    # Evaluate workload
    for iter in range(LOOP_CTRL):
        cur_path = json_paths[iter]
        counts = assessment(cur_path)
    # Open each file and get all valid names
    for i in tqdm(range(len(json_paths))):
         jsonpath = json_paths[i]
         app_urls = read_each_json(jsonpath)
         for m in app_urls:
             with ThreadPoolExecutor(max_workers=MAX_THREAD) as executor:
                 executor.map(download_wrapper, app_urls)

    print("Download Completed!")