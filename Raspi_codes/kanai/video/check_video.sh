result=$(/home/pi/python-venv/kanai/bin/python /home/pi/load_setting.py)
ARR=(${result//,/ })
FPS=${ARR[0]}  # FPS
SIZE=${2:-"640x480"}  # 解像度 (固定)

PORT="8080" #ポート番号
ID="kanai" #ID
PW="kanaipass" #パスワード

export LD_LIBRARY_PATH=/usr/local/lib

/home/pi/mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer \
    -i "/home/pi/mjpg-streamer/mjpg-streamer-experimental/input_uvc.so -f $FPS -r $SIZE -d /dev/video0 -y -n" \
    -o "/home/pi/mjpg-streamer/mjpg-streamer-experimental/output_http.so -w /usr/local/www -p $PORT"
