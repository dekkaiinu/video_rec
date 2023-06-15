import pyrealsense2 as rs
import numpy as np
import matplotlib.pyplot as plt

# RealSenseパイプラインの初期化
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)

# パイプラインを開始
pipeline.start(config)

try:
    # フレームを待機
    frames = pipeline.wait_for_frames()

    # 深度フレームを取得
    depth_frame = frames.get_depth_frame()

    # フレームの幅と高さを取得
    width = depth_frame.get_width()
    height = depth_frame.get_height()

    # フレームをNumPy配列に変換
    depth_image = np.asanyarray(depth_frame.get_data())

    # 深度情報の表示（例: 画素 (100, 200) の深度値）
    depth_value = depth_image[200, 100]
    print("Depth value at pixel (100, 200):", depth_value)

finally:
    # パイプラインを停止してリソースを解放
    pipeline.stop()

plt.imshow(depth_image, cmap="gray")
plt.colorbar()
plt.show()
