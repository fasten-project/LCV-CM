#!/bin/sh -l

cd /github/workspace/src/LCV
python3 LCVServer.py &
newman run https://www.getpostman.com/collections/12cd4d55bac01c3e06e0
