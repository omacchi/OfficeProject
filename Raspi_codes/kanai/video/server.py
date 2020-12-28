from flask import Flask, request, render_template, jsonify
import json
from flask_cors import CORS, cross_origin
import subprocess, shlex
import time

app = Flask(__name__)
CORS(app)


@app.after_request
def afterRequest(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# 現在のFPS, 録画時間, 解像度を取得
@app.route('/get_current_params')
def getCurrentParams():
    try:
        # 設定ファイルの読み込み
        with open('/home/pi/setting.json', 'r') as f:
            setting = json.load(f)
            fps = setting['fps']
            recordingTime = setting['recordingTime']
            resolution = setting['resolution']
    except Exception as e:
        print(e)
        return jsonify({'result': 'NG'})
    else:
        print('Setting Parameters:', setting)
        response = setting
        response['result'] = 'OK'
        print(response)

        return jsonify(response)


# FPSを変更
@app.route('/set_fps', methods=['POST'])
def setFps():
    data = json.loads(request.get_data().decode())
    fps = int(data['fps'])
    # 設定ファイルを更新
    try:
        # 設定ファイルの読み書き
        with open('/home/pi/setting.json', 'r') as f:
            setting = json.load(f)
            setting['fps'] = fps
        with open('/home/pi/setting.json', 'w') as f:
            f.write(json.dumps(setting))
    except Exception as e:
        print(e)
        return jsonify({'result': 'NG'})
    else:
        print('Set FPS:', fps)

        return jsonify({'result': 'OK'})


# 録画時間を変更
@app.route('/set_recordingTime', methods=['POST'])
def setRecordingTime():
    data = json.loads(request.get_data().decode())
    recordingTime = int(data['recordingTime'])

    # 設定ファイルを更新
    try:
        # 設定ファイルの読み書き
        with open('/home/pi/setting.json', 'r') as f:
            setting = json.load(f)
            setting['recordingTime'] = recordingTime
        with open('/home/pi/setting.json', 'w') as f:
            f.write(json.dumps(setting))
    except Exception as e:
        print(e)
        return jsonify({'result': 'NG'})
    else:
        print('Set Recording Time:', recordingTime)

        return jsonify({'result': 'OK'})


# 解像度を変更
@app.route('/set_resolution', methods=['POST'])
def setResolution():
    data = json.loads(request.get_data().decode())
    resolution = int(data['resolution'])

    # 設定ファイルを更新
    try:
        # 設定ファイルの読み書き
        with open('/home/pi/setting.json', 'r') as f:
            setting = json.load(f)
            setting['resolution'] = resolution
        with open('/home/pi/setting.json', 'w') as f:
            f.write(json.dumps(setting))
    except Exception as e:
        print(e)
        return jsonify({'result': 'NG'})
    else:
        print('Set resolution:', resolution)

        return jsonify({'result': 'OK'})


def checkServiceStatus(service):
    ret = subprocess.run(shlex.split(f'sudo systemctl is-active {service}'), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    status = ret.stdout.decode('utf-8').strip('\n')
    return status


@app.route('/start_record')
def startRecord():
    subprocess.call(shlex.split('/home/pi/stop_service.sh'))
    subprocess.call(shlex.split('sudo systemctl start stream.service'))
    subprocess.call(shlex.split('sudo systemctl start record.service'))

    time.sleep(1)

    if checkServiceStatus('stream.service') == 'active' and checkServiceStatus('record.service') == 'active':
        return jsonify({'result': 'OK'})
    else:
        return jsonify({'result': 'NG'})


@app.route('/stop_record')
def stopRecord():
    subprocess.call(shlex.split('/home/pi/stop_service.sh'))
    return jsonify({'result': 'OK'})


@app.route('/reload_video')
def reloadVideo():
    subprocess.call(shlex.split('/home/pi/stop_service.sh'))
    subprocess.call(shlex.split('sudo systemctl start check_video.service'))

    time.sleep(1)

    if checkServiceStatus('check_video.service') == 'active':
        return jsonify({'result': 'OK'})
    else:
        return jsonify({'result': 'NG'})


def main():
    app.run(host='0.0.0.0', port=60080)


if __name__ == '__main__':
    main()
