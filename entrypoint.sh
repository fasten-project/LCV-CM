#!/bin/sh -l

cd /github/workspace/src/LCV
python3 LCVServer.py &
newman run https://www.getpostman.com/collections/3b2724fe658897b87a57
