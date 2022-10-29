import datetime
import os
import time
from time import sleep

import cv2
import numpy as np
import picamera
import picamera.array

import tkinter_1


def white_balance(bright):
    print("auto white balancing...")
    camera.awb_mode = "auto"
    wb = camera.awb_gains
    camera.awb_mode = "off"
    camera.awb_gains = wb
    bright = 0
    return bright


def sleep_mode(camera, wake):
    dark = 0
    print("sleep mode ON")
    cv2.destroyAllWindows()
    with picamera.array.PiRGBArray(camera) as stream:
        while True:
            for j in range(iteration):
                camera.resolution = sleep_resolution
                camera.capture(stream, "bgr", use_video_port=True)
                k = cv2.waitKey(waitkey_sleep)
                sleep(1)
                stream.seek(0)
                stream.truncate()
                if k == 27:
                    break
                elif np.average(stream.array) > brightbreak:
                    wake = 1
                    break
            if wake == 1:
                print("break sleep. ave pix value:", np.average(stream.array))
                wake = 0
                break
            else:
                print("sleep mode. ave pix value:", np.average(stream.array))
    camera.resolution = resolution
    return dark


def stream(dark, bright, camera, wake, pixvalue):

    camera.resolution = resolution
    a = camera.framerate

    with picamera.array.PiRGBArray(camera) as stream:
        time.sleep(2)
        while True:
            for i in range(iteration):
                camera.capture(stream, "bgr", use_video_port=True)
                if record:
                    date_time = datetime.datetime.now()
                    cv2.imwrite(
                        destdir
                        + str(date_time.hour)
                        + str(date_time.minute)
                        + str(date_time.microsecond)
                        + ".jpg",
                        stream.array,
                    )
                    cv2.putText(
                        stream.array,
                        "REC",
                        testinfo1,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        3.0,
                        (50, 50, 150),
                        thickness=4,
                    )
                if dark > dark_count:
                    cv2.putText(
                        stream.array,
                        "Going to sleep..." + emoji[dark - dark_count - 1],
                        infocood,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (50, 50, 50),
                        thickness=2,
                    )
                if test:
                    cv2.putText(
                        stream.array,
                        "Pix value: " + str(pixvalue),
                        testinfo1,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (50, 50, 50),
                        thickness=2,
                    )
                    cv2.putText(
                        stream.array,
                        "bright: " + str(bright),
                        testinfo2,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (50, 50, 50),
                        thickness=2,
                    )
                    cv2.putText(
                        stream.array,
                        "dark: " + str(dark),
                        testinfo3,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (50, 50, 50),
                        thickness=2,
                    )
                    cv2.rectangle(
                        stream.array,
                        (array_w1, array_h1),
                        (array_w2, array_h2),
                        (100, 100, 100),
                    )
                cv2.imshow("camera", stream.array)

                k = cv2.waitKey(waitkey)
                if k == 27:
                    break
                stream.seek(0)
                stream.truncate()
            # pixvalue = np.average(stream.array)
            pixvalue = np.count_nonzero(
                stream.array[array_h1:array_h2, array_w1:array_w2] < pixthresh
            )
            # print(pixvalue)
            if pixvalue < bright_thresh:
                bright += 1
                dark = 0
                if bright > 5:
                    bright = white_balance(bright)
                    print("white balance performed.")
            elif dark_thresh > pixvalue > bright_thresh:
                bright, dark = 0, 0
            elif pixvalue > dark_thresh:
                dark += 1
            if dark > 10:
                dark = sleep_mode(camera, wake)

        cv2.destroyAllWindows()


def init_pi_camera(dir_name):
    global destdir, dir, iteration, waitkey, waitkey_sleep, sleeprate, resolution, array_h1, array_h2, array_w1, array_w2, sleep_resolution, pixthresh, dark, pixvalue, bright, wake, dark_thresh, dark_count, bright_thresh, brightbreak, auto_wb, infocood, testinfo1, testinfo2, testinfo3, test, emoji

    if os.path.exists("ここに外部ボリュームパス"):
        destdir = "ここに外部ボリュームパス" + dir_name + "/"
        if not os.path.isdir(destdir):
            os.mkdir(destdir)
        print("recording mode")
        global record
        record = True
    else:
        print("normal mode")
        record = False
    dir = "/home/pi/camera"
    iteration = 20
    waitkey = 5
    waitkey_sleep = 2000
    sleeprate = 2000
    width, height = 2560, 1440  # 1920, 1088
    # width, height = 800, 608
    resolution = (width, height)
    array_h1, array_h2, array_w1, array_w2 = (
        int((height / 2) - (height / 8)),
        int((height / 2) + (height / 8)),
        int((width / 2) - (width / 8)),
        int((width / 2) + (width / 8)),
    )

    sleep_resolution = (160, 128)
    pixthresh = 100
    dark, pixvalue, bright, wake = 0, 0, 0, 0
    dark_thresh = 0.1 * width * width
    dark_count = 5
    bright_thresh = 0.003 * width * width
    brightbreak = 50
    auto_wb = 190
    infocood = (array_w1, array_h1 - 30)
    testinfo1 = (10, 100)
    testinfo2 = (10, 130)
    testinfo3 = (10, 160)
    test = False
    emoji = ["(=_=)~~", "(=o=)~~~", "(*O*)~~~~", "(-o-)~~~~~", "(-_-. o O"]

    with picamera.PiCamera() as camera:
        camera.vflip = False
        camera.hflip = False
        stream(dark, bright, camera, wake, pixvalue)


tkinter_1.init_tkinter(init_pi_camera)
