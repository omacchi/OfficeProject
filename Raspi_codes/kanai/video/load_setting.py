import sys
import json


def main():
    with open('/home/pi/setting.json', 'r') as f:
        setting = json.load(f)
        fps = setting['fps']
        recordingTime = setting['recordingTime']
        resolution = setting['resolution']

    sys.stdout.write(f'{fps}, {recordingTime}, {resolution}')


if __name__ == '__main__':
    main()
