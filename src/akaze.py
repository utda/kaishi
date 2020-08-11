# -*- coding: utf-8 -*-
import cv2
import math
import glob
import os
import csv
import json

from IPython.display import display, Image

def display_cv_image(image, format='.png'):
    decoded_bytes = cv2.imencode(format, image)[1].tobytes()
    display(Image(data=decoded_bytes))

# 画像読込
img1 = cv2.imread("data/main.jpg")
img2 = cv2.imread("data/target1.jpg")

# A-KAZE検出器の生成
detector = cv2.AKAZE_create()

# 特徴量の検出と特徴量ベクトルの計算
kp1, des1 = detector.detectAndCompute(img1, None)
kp2, des2 = detector.detectAndCompute(img2, None)

# Brute-Force Matcherの生成
bf = cv2.BFMatcher()

# 特徴量ベクトル同士をBrute-Force＆KNNでマッチング
matches = bf.knnMatch(des1, des2, k=2)

# データを間引く
ratio = 0.2
good = []
for m, n in matches:
    if m.distance < ratio * n.distance:
        good.append([m])

# 特徴量をマッチング状況に応じてソート
good = sorted(matches, key = lambda x : x[1].distance)

# 対応する特徴点同士を描画
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good[:3], None, flags=2)

cv2.imwrite("data/shift_result.png", img3)