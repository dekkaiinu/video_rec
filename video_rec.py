import numpy as np
import os
import cv2
from datetime import datetime

"""
CONFIG
"""
CAMERA_DEVISE = 1

IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720
FPS = 30.0

FILEPATH = "./" + datetime.now().strftime("%Y-%m-%d") + "/"

"""
"""


def main():
    set = input("何セット目ですか？:")
    print("撮影開始")
    print("tを押して撮影時間を記録")
    print("qを押して終了")
    capture(set)
    print("撮影完了")

def capture(set):
    num = 0
    raps = np.zeros(5, dtype=object)
    cap = cv2.VideoCapture(CAMERA_DEVISE+cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")  # 動画のコーデックを指定
    filename = datetime.now().strftime("%Y-%m-%d_") + "SET" + str(set) +".mp4"
    if not os.path.exists(FILEPATH):
        os.makedirs(FILEPATH)
    out = cv2.VideoWriter(FILEPATH + filename, fourcc, FPS, (IMAGE_WIDTH, IMAGE_HEIGHT))  # 出力ファイル名、コーデック、フレームレート、フレームサイズを指定

    while cap.isOpened():
        ret, frame = cap.read()  # フレームを取得

        if not ret:
            break

        # フレームを表示する
        cv2.imshow('Frame', frame)
        # フレームを動画ファイルに書き込む
        out.write(frame)

        key = cv2.waitKey(1) & 0xFF
        # 時間を記録する
        if key == ord('t'):
            raps = rap(raps, num)
            num = num + 1
            print(str(num) + "回目")

        # 'q'キーを押して終了する
        if key == ord('q'):
            print(raps)
            break

    cap.release()  # カメラキャプチャを解放
    out.release()  # 動画ファイルを閉じる
    cv2.destroyAllWindows()  # ウィンドウを閉じる

            

def rap(raps, num):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)
    raps[num] = now
    return raps 



if __name__ == "__main__":
    main()