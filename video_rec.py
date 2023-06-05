import numpy as np
import os
import cv2
import pyrealsense2 as rs
from datetime import datetime
import time

"""
CONFIG
"""
CAMERA_DEVISE = 1

IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720
FPS = 30.0

FILEPATH = "./" + datetime.now().strftime("%Y-%m-%d") + "/"
DEPTHPATH = FILEPATH + "depth/"

"""
"""


def main():
    print("撮影開始")
    print("tを押して撮影時間を記録,depthの撮影")
    print("qを押して終了")
    capture()
    print("撮影完了")

def capture():
    num = 0
    start_time = time.time()

    laps_date = np.zeros(500, dtype=object)
    laps_time = np.zeros(500, dtype=object)

    cap = cv2.VideoCapture(CAMERA_DEVISE+cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")  # 動画のコーデックを指定
    filename = datetime.now().strftime("%Y-%m-%d_") +".mp4"
    if not os.path.exists(FILEPATH):
        os.makedirs(FILEPATH)
    if not os.path.exists(DEPTHPATH):
        os.makedirs(DEPTHPATH)
    out = cv2.VideoWriter(FILEPATH + filename, fourcc, FPS, (IMAGE_WIDTH, IMAGE_HEIGHT))  # 出力ファイル名、コーデック、フレームレート、フレームサイズを指定

    # RealSenseパイプラインの設定
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    

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
            laps_date = date_rap(laps_date, num)
            laps_time = time_rap(start_time, laps_time, num)
            depth = capture_depth(pipeline, config)
            np.save(DEPTHPATH + datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".npy", depth)
            num = num + 1
            print(str(num) + "回目")

        # 'q'キーを押して終了する
        if key == ord('q'):
            laps = np.stack([laps_date, laps_time])
            np.save(FILEPATH + datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".npy", laps)
            break

    cap.release()  # カメラキャプチャを解放
    out.release()  # 動画ファイルを閉じる
    cv2.destroyAllWindows()  # ウィンドウを閉じる


def date_rap(laps, num):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)
    laps[num] = now
    return laps 

def time_rap(start_time, laps, num):
    now = time.time()
    now_time = now - start_time
    laps[num] = now_time
    return laps

def capture_depth(pipeline, config):
    # パイプラインを開始
    pipeline.start(config)
    try:
        # フレームを待機
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        # DepthデータをNumPy配列に変換
        depth_image = np.asanyarray(depth_frame.get_data())

    finally:
        # パイプラインを停止
        pipeline.stop()

    return depth_image


if __name__ == "__main__":
    main()