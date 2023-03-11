# python detect_blur_for_all.py -i ./images
import argparse

# import numpy as np
import os
import shutil

import cv2
from imutils import paths

ap = argparse.ArgumentParser()
ap.add_argument(
    "-i", "--images", required=True, help="path to input directory of images"
)
ap.add_argument(
    "-t",
    "--threshold",
    type=float,
    default=100.0,
    help="focus measures that fall below this value will be considered ‘blurry’",
)
ap.add_argument(
    "-d",
    "--delete",
    type=bool,
    required=False,
    default=False,
    help="clean up images in directory of images before running the process",
)
args = vars(ap.parse_args())

# test内のreport folderとblurimage を削除する


def delete_past_imagefolder(file_path, sub_dir="/report"):
    # file pathを取得
    dir_file = os.path.split(file_path)
    dir = dir_file[0]
    file_name = dir_file[1]
    # imageフォルダ
    image_path = dir + "/" + file_name
    # reportフォルダ
    report_path = dir + "/" + sub_dir
    shutil.rmtree(image_path)
    shutil.rmtree(report_path)


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F)


def report_image(image, laplacian, text):
    cv2.putText(
        image,
        "{}: {:.2f}".format(text, laplacian.var()),
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 0),
        3,
    )


def write_image(file_path, image, sub_dir="/report"):
    dir_file = os.path.split(file_path)
    dir = dir_file[0]
    file_name = dir_file[1]
    report_dir = dir + sub_dir
    os.makedirs(report_dir, exist_ok=True)
    cv2.imwrite(report_dir + "/" + file_name, image)


# deleteフラグを指定していたらimageを削除
if args["delete"]:
    for image_path in paths.list_images(args["images"]):
        delete_past_imagefolder(image_path, "/blurimage")
        delete_past_imagefolder(image_path, "/notblurimage")
        delete_past_imagefolder(
            image_path,
        )


# フォーカスの合ってないものを除去する
for image_path in paths.list_images(args["images"]):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = variance_of_laplacian(gray)
    text = "Not Blurry"
    if laplacian.var() < args["threshold"]:
        text = "Blurry"
        report_image(image, laplacian, text)
        write_image(image_path, laplacian)
        write_image(image_path, image, "/blurimage")
    else:
        write_image(image_path, laplacian)
        write_image(image_path, image, "/notblurimage")
