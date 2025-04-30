#!/bin/bash

PYTHON=/home/pi/Desktop/MidtermProject/venv/bin/python

pushd /home/pi/Desktop/MidtermProject

echo "\nRunning Flask Server\n"
python test_sensor.py &

sleep 70

echo "\nRunning Cloudflare Tunnel\n"
rm -f temp_files/cloudflared.log
cloudflared tunnel --url http://127.0.0.1:5000 >> temp_files/cloudflared.log 2>&1 &
sleep 10

echo "\nUploading Tunnel URL\n"
$PYTHON parse_url.py

popd
