import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

""
LOADPATH = "C:/Users/youta/HsRawData2pickle/img02_Img-d(s35,g20,28.45ms,350-1100).pkl"
WITEPATH = "./a.png"

""

def main():
    array = load_data(LOADPATH)
    array = np.clip(array, 0, 255).astype(np.uint8)
    for i in range(151):
        band_array = band_image_array(array, i)
        print(i + 1 , end=": ")
        print(saturation_detect(band_array))
    plt.imshow(band_array)
    cv.imwrite(WITEPATH, band_array)
    band_image_hist(band_array)

def load_data(name):
    data = np.load(name, allow_pickle=True)
    return data

def band_image_array(array, band):
    band_array = array[:, :, band]
    return band_array

def band_image_hist(band_array):
    histgram = cv.calcHist([band_array], [0], None, [256], [0, 256])
    plt.figure(figsize=(8, 6))
    plt.plot(histgram.flatten(), color='red', alpha=0.5)
    plt.show()

def saturation_detect(band_array):
    frag = False
    threshold = 5
    saturated_pixels = np.count_nonzero((band_array <= threshold) | (band_array >= 255 - threshold))
    saturated_ratio = saturated_pixels / band_array.size
    if saturated_ratio >= 0.1:
        frag = True
        print(saturated_ratio)
    return frag



if __name__=="__main__":
    main()