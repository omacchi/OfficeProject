# 実行するコマンド
COM1="/home/pi/python-venv/kanai/bin/python /home/pi/server.py"
COM2="/home/pi/.nodebrew/current/bin/node /home/pi/TrafficWebApp/app/app.js"

CMDNAME=`basename $0`
# 実行時に指定された引数の数が1でなければエラーを出力して終了
if [ $# -ne 1 ]; then
    # 標準出力を標準エラー出力にマージする
    echo "Usage: $CMDNAME [--start or --stop]" 1>&2
    exit 1
fi

# プロセスを実行
if [ "$1" = '--start' -o "$1" = '-s' ]; then
    # 一度終了処理を実行
    sudo pkill -e -f -9 "$COM1"
    sudo pkill -e -f -9 "$COM2"
    echo "`date '+%Y/%m/%d %H:%M:%S'` プログラムの実行開始"
    sudo ${COM1} >> /dev/null &
    sudo ${COM2} >> /dev/null
    echo "`date '+%Y/%m/%d %H:%M:%S'` プログラムの実行終了"
    exit 0
fi

# プロセスを終了
if [ "$1" = '--stop' -o "$1" = '-t' ]; then
    sudo pkill -e -f -9 "$COM1"
    sudo pkill -e -f -9 "$COM2"
    exit 0
fi

exit 0
