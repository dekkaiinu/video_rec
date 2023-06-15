import numpy as np
import os
import cv2
import pyrealsense2 as rs
from datetime import datetime
import time
import math
import sys

""

IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 768
FPS = 30

#FILEPATH = "./ueno_zoo/penguin/" + datetime.now().strftime("%Y-%m-%d") + "/set" + sys.argv[1] + "/"
FILEPATH = "D:/ueno_zoo/penguin/" + datetime.now().strftime("%Y-%m-%d") + "/set" + sys.argv[1] + "/"
DEPTHPATH = FILEPATH + "depth/"

""


def main():
    print("撮影開始")
    print("tを押して撮影時間を記録,depthの撮影")
    print("qを押して終了")
    capture()
    print("撮影完了")

def capture():
    laps_date = np.zeros(500, dtype=object)
    laps_time = np.zeros(500, dtype=object)

    if not os.path.exists(FILEPATH):
        os.makedirs(FILEPATH)
    if not os.path.exists(DEPTHPATH):
        os.makedirs(DEPTHPATH)
    # パイプラインを開始 RealSenseパイプラインの初期化
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, IMAGE_WIDTH, IMAGE_HEIGHT, rs.format.z16, FPS)
    pipeline.start(config)

    i = 0
    start_time = time.time()
    try:
        while True:
            
            # フレームを待機
            frames = pipeline.wait_for_frames()

            # 深度フレームを取得
            depth_frame = frames.get_depth_frame()

            # フレームをNumPy配列に変換
            depth_image = np.asanyarray(depth_frame.get_data())
            depth_image_normalized = (depth_image / 65535 * 255).astype(np.uint8)

            heatmap = cv2.applyColorMap(depth_image_normalized, cv2.COLORMAP_JET)
            # 深度画像を表示
            cv2.imshow("Depth Image", heatmap)
            # キーボードの入力を監視
            key = cv2.waitKey(1)

            # "t"キーを押した場合、深度画像を保存
            if key == ord('t'):
                laps_date = date_rap(laps_date, i)
                laps_time = time_rap(start_time, laps_time, i)
                i+=1
                np.save(DEPTHPATH + "DepthImage_"+ datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".npy", depth_image)
                print("Depth " + str(i) + "saved.")

            # "q"キーを押した場合、パイプラインを停止してループを終了
            if key == ord('q'):
                laps = np.stack([laps_date, laps_time])
                np.save(FILEPATH + "time_" +datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".npy", laps)
                break


    finally:
        # パイプラインを停止してリソースを解放
        pipeline.stop()

    # ウィンドウを閉じる
    cv2.destroyAllWindows()


def date_rap(laps, num):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)
    laps[num] = now
    return laps 

def time_rap(start_time, laps, num):
    now = time.time()
    now_time = now - start_time
    now_time = math.floor(now_time)
    print(now_time)
    laps[num] = now_time
    return laps

if __name__ == "__main__":
    main()