#!/usr/bin/env python3

import validators
from urllib.parse import urlparse
import sys
import re

# axis 
axis_rtsp_1 = "rtsp://root:pass@192.168.2.140/axis-media/media.amp?videocodec=h264"
axis_rtsp_2 = "rtsp://root:root@192.168.1.82/axis-media/media.amp?camera=4"

# avtech
avtech_rtsp = "rtsp://admin:admin@192.168.2.17/live/video_audio/profile1"

# unv
unv_rtsp = "rtsp://admin:Admin@12345@192.168.2.152:554/media/video1"


def validate(path):
    check_url = validators.url(path)
    
    return check_url


def check_rtsp(num, path):
    check = urlparse(path)
    
    return {"camera_num": num,
            "scheme": check.scheme,
            "netloc": check.netloc,
            "path": check.path,
            "username": check.username,
            "password": check.password,
            "hostname": check.hostname,
            "port": check.port}


def rtsp_regular_expression(path):
    axis_pattern = "^rtsp:\/\/[a-zA-Z0-9]*:[a-zA-Z0-9]*@192\.168\.[0-9]{1,3}\.[0-9]{1,3}/axis\-media/media\.amp\?(camera=[1-4]{1}|videocodec=h264)"
    avtech_pattern = "^rtsp:\/\/[a-zA-Z0-9]*:[a-zA-Z0-9]*@192\.168\.[0-9]{1,3}\.[0-9]{1,3}/live/video\_audio/profile1"

    if re.match(axis_pattern, path):
        print(f"axis: {path} --> correct\n")

    elif re.match(avtech_pattern, path):
        print(f"avtech: {path} --> correct\n")

    else:
        print(f"{path} --> incorrect\n")



if __name__ == "__main__":

    for i, line in enumerate(sys.stdin.readlines(), start=1):
        rtsp = line.rstrip()
        if len(rtsp) == 0:
            continue

        #print(check_rtsp(i, rtsp))
        #print(f"camera's rtsp: {i} --> {validate(rtsp)}\n")

        rtsp_regular_expression(rtsp)




