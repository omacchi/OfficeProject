#!/bin/sh

sudo systemctl stop check_video.service
sudo systemctl stop stream.service
sudo systemctl stop record.service
sleep 1
