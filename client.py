import os
import time
import argparse
import requests
from PIL import ImageGrab

server_url = 'http://www.hereforus.cn:8080/sync_file'

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", type=str, default="GET")
args = parser.parse_args()

work_mode = args.mode

get_interval = 2
post_interval = 10
post_count = 0

result_path = "./results"

if not os.path.exists(result_path):
    os.makedirs(result_path)

while True:
    try:
        if work_mode == "GET":
            r = requests.get(server_url)
            if r.text == "None":
                print("\33[31m[Sync File] Queue is Empty\33[0m")
            else:
                file_name = r.headers['Content-Disposition'].split('=')[1]
                with open(f"{result_path}/{file_name}", "wb") as f:
                    f.write(r.content)
                print(f"\33[33m[Sync File] Get Succeeded ({file_name})\33[0m")
            time.sleep(get_interval)
        else:
            post_count += 1
            img = ImageGrab.grab()
            img.save("sync.png")
            with open("sync.png", "rb") as f:
                requests.post(server_url, files={'image': f})
            print(f"\33[32m[Sync File] Post Succeeded ({post_count})\33[0m")
            time.sleep(post_interval)
    except Exception as e:
        print(f"\33[31m[Sync Failed] Retrying... \33[0m")
        print(e)
        time.sleep(get_interval)
