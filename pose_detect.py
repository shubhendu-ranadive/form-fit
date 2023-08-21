from ultralytics import YOLO
import numpy as np
import os
import cv2

# ポーズを抽出するためのモデルを呼ぶ
model = YOLO('yolov8n-pose.pt')

# カメラを開いて、フレームを読み込む
cam = cv2.VideoCapture(0)
while True:
    ret, image = cam.read()
    if ret is False:
        cv2.waitKey(3000)
        cam.release()
        break

    # ポーズを抽出する
    results = model.track(image, persist=True)

    # 抽出したポーズを画像の上に描く
    annotated_image = results[0].plot()

    # ポーズを描いた画像を表示する
    cv2.imshow("Frame", annotated_image)

    # 「Q」キーを押したらプログラムを終了する
    key = cv2.waitKey(5)
    if key == ord('q') & 0xFF:
        break

# カメラを閉じて、表示画面を削除する
cam.release()
cv2.destroyAllWindows()
