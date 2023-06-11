import numpy as np
import matplotlib.pyplot as plt

# NumPy配列から深度画像を作成
def convert_depth_array_to_image(depth_array):
    # 深度値の範囲を設定
    min_depth = np.min(depth_array)
    max_depth = np.max(depth_array)
    inverted_depth = max_depth - depth_array

    # 深度値を0-255の範囲に正規化
    normalized_depth = ((inverted_depth - min_depth) / (max_depth - min_depth)) * 255

    # 深度画像を作成
    depth_image = normalized_depth.astype(np.uint8)
    return depth_image

# NumPy配列から深度画像を作成
depth_array = np.load("D:\\ueno_zoo\\penguin\\video&depth\\2023-06-11\\depth\\DepthImage_2023-06-11_14-20-53.npy")
depth_image = convert_depth_array_to_image(depth_array)

# 深度画像を表示
plt.imshow(depth_image, cmap="gray")
plt.colorbar()
plt.show()
