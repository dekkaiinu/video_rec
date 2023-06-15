import pyrealsense2 as rs
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

UPPATH = "./depth/"
if not os.path.exists(UPPATH):
    os.makedirs(UPPATH)

# RealSenseパイプラインの初期化
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)

# パイプラインを開始
pipeline.start(config)

i = 0
try:
    while True:
        # フレームを待機
        frames = pipeline.wait_for_frames()

        # 深度フレームを取得
        depth_frame = frames.get_depth_frame()

        # フレームの幅と高さを取得
        width = depth_frame.get_width()
        height = depth_frame.get_height()

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
            i+=1
            np.save(UPPATH + str(i) + "depth.npy", depth_image)
            print("Depth " + str(i) + "saved.")

        # "q"キーを押した場合、パイプラインを停止してループを終了
        if key == ord('q'):
            break


finally:
    # パイプラインを停止してリソースを解放
    pipeline.stop()

# ウィンドウを閉じる
cv2.destroyAllWindows()

