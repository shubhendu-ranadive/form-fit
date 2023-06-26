import mediapipe as mp
import numpy as np
import os
import cv2

# ポーズを抽出するためにオブジェクトを作る
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5)

# 抽出したポーズを画像の上に描くためにオブジェクトを作る
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


# カメラを開いて、フレームを読み込む
cam = cv2.VideoCapture(0)
while True:
    ret, image = cam.read()
    if ret is False:
        cv2.waitKey(3000)
        cam.release()
        break


    # ポーズを抽出する
    results = pose.process(image)

    # もしポーズが抽出出来なかったら、次のフレームに進む
    if not results.pose_landmarks:
        continue

    # 抽出したポーズを画像の上に描く
    annotated_image = image.copy()
    mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks,
                              mp_pose.POSE_CONNECTIONS,
                              landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    # ポーズを描いた画像を表示する
    cv2.imshow("Frame", annotated_image)

    # 「Q」キーを押したらプログラムを終了する
    key = cv2.waitKey(5)
    if key == ord('q') & 0xFF:
        break

# カメラを閉じて、表示画面を削除する
cam.release()
cv2.destroyAllWindows()
