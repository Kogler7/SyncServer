import os
import time
import queue
from flask import Flask, request, send_file

app = Flask(__name__)

result_path = "./results"

sync_queue = queue.Queue()

used_file_name = ""

if not os.path.exists(result_path):
    os.makedirs(result_path)


@app.route('/sync_file', methods=['POST', 'GET'])
def sync_file():
    if request.method == 'GET':
        if sync_queue.empty():
            print("\33[31m[Sync File] Queue is Empty\33[0m")
            return 'None'
        else:
            file_name: str = sync_queue.get()
            global used_file_name
            if used_file_name != "":
                os.remove(f"{result_path}/{used_file_name}")
            used_file_name = file_name
            print(f"\33[33m[Sync File] Get Succeeded ({file_name})\33[0m")
            return send_file(
                f"{result_path}/{file_name}.png",
                as_attachment=True,
                mimetype='image/png'
            )
    else:
        file = request.files['image']
        timeStr = time.strftime("%H%M%S")
        file.save(f"{result_path}/{timeStr}.png")
        sync_queue.put(timeStr)
        print(f"\33[32m[Sync File] Post Succeeded ({timeStr})\33[0m")
        return 'Success'


@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['image']
    timeStr = time.strftime("%H%M%S")
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    file.save(f"{result_path}{timeStr}.png")
    print("success", timeStr)
    return 'Success'


@app.route('/download_file', methods=['GET'])
def download_file():
    file_name = request.form['file_name']
    return send_file(f"./results/{file_name}", as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
