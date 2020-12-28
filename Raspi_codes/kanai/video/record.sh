
result=$(/home/pi/python-venv/kanai/bin/python /home/pi/load_setting.py)
ARR=(${result//,/ })
FPS=${ARR[0]}  # FPS
TIME=${ARR[1]}
TIME=$((TIME * 60))  # 録画時間 (秒)
SIZE=${2:-"640x480"}  # 解像度 (固定)

ffmpeg -i http://localhost:8080/?action=stream -r $FPS -s $SIZE\
	-an -vcodec h264_omx \
	-f segment -segment_time $TIME \
	-segment_format_options movflags=+faststart -reset_timestamps 1 \
	-strftime 1 "/home/pi/ssd/video_data/%Y-%m-%d_%H-%M-%S.mp4"
