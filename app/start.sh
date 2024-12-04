#!/bin/bash


echo "Starting Uvicorn"
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

echo "Starting SpiderFoot"
python /home/spiderfoot/sf.py -l 0.0.0.0:5001
