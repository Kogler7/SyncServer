import os
import time
import pickle
import argparse
import requests
from PIL import ImageGrab

# 服务端URL
server_url = 'http://www.hereforus.cn:8080/sync_file'

# 工作模式，GET为从服务端获取文件，POST为向服务端发送文件
# 解析命令参数
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", type=str, default="GET")
args = parser.parse_args()

work_mode = args.mode

result_path = "./results"

while True:
    try:
        if work_mode == "GET":
            # 通过get请求获取服务端返回的文件，如果没有文件则返回None
            r = requests.get(server_url)
            if r.text == "None":
                print("None")
            else:
                if not os.path.exists(result_path):
                    os.makedirs(result_path)
                # r.headers['Content-Disposition']
                file_name = r.headers['Content-Disposition'].split('=')[1]
                with open(f"{result_path}/{file_name}.png", "wb") as f:
                    f.write(r.content)
                print("ok")
        else:
            img = ImageGrab.grab()
            img.save("temp.png")
            # 读取图片temp.png并通过post发送
            with open("temp.png", "rb") as f:
                requests.post(server_url, files={'image': f})
            print("ok")
    except Exception as e:
        print("retry", e)
    time.sleep(3)
