import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

import NHdata2pkl

""
LOADPATH = "C:\\Users\\youta\\dataset\\Img-d_frozen_length120_height2_white(s20,g50,49.88ms,350-1100)_20230424_145859.nh9"
WITEPATH = "./a.png"
COLORS = ["indigo", "blueviolet", "dodgerblue", "lawngreen", "yellow", "orange", "red", "darkred", "maroon","saddlebrown","black","gray","silver","lightgray","gainsboro"]
LABELS = ["1~10", "11~20", "21~30", "31~40", "41~50", "51~60", "61~70", "71~80", "81~90","91~100","101~110","111~120","121~130","131~140","141~150"]

HOR = 2048
VER = 1080
SPECDIM = 151

THRESHOLD = 5 #飽和状態を決定する画素値の閾値(上下の)
SATURATION_RATIO = 0.01 #飽和認定する画素値の比率
# 2048 * 1080 = 2,211,840  を256(画素値)で割ると1つのビンあたり8640
""

def main():
    array = NHdata2pkl.load_data(LOADPATH, HOR, VER, SPECDIM)
    array = ((array / 4095) * 255).astype(np.uint8)
    count = 0
    rates = []
    for i in range(151):
        band_array = band_image_array(array, i)
        rate, frag = saturation_detect(band_array)

        rate = round(rate, 2)
        rate_pr = str(i + 1) + " :" + str(rate)
        rates.append(rate_pr)

        if frag == True:
            count += 1
    
    np.savetxt('saturation_pixel_rate.csv', rates ,delimiter=',', fmt='%s')
    print("飽和バンド率：", end="")
    print("{:.2f}".format(count / i))
    plot_hist(array)
    #指定したバンドのヒストグラムとグレースケール画像を出力
    #cv.imshow("band image", band_image_array(array, 41))
    #select_plot_hist(band_image_array(array, 41))


def load_data(name):
    data = np.load(name, allow_pickle=True)
    return data

def band_image_array(array, band):
    band_array = array[:, :, band]
    return band_array

def saturation_detect(band_array):
    frag = False
    threshold = THRESHOLD
    saturated_pixels = np.count_nonzero((band_array <= threshold) | (band_array >= 255 - threshold))
    saturated_ratio = saturated_pixels / band_array.size
    if saturated_ratio >= SATURATION_RATIO:
        frag = True
    return saturated_ratio, frag


def select_plot_hist(band_array):
    histgram = cv.calcHist([band_array], [0], None, [256], [0, 256])
    plt.figure(figsize=(8, 6))
    plt.plot(histgram.flatten(), color="gray", alpha=0.5)
    plt.xlim(-5, 256)
    plt.ylim(0, 50000)
    plt.show()

def plot_hist(array):
    tate, yoko, takasa = np.shape(array)
    shape = (tate, yoko, 15)
    hist_array = np.zeros(shape, dtype=np.uint8)
    for i in range(15):
        start = i * 10
        end = start + 9
        sliced_array = array[:, :, start:end]
        mean_array = np.mean(sliced_array, axis=2)
        mean_array = np.round(mean_array).astype(np.uint8)
        hist_array[:, :, i] = mean_array
    
    fig, axes = plt.subplots(3, 5, figsize=(10, 5))
    for i, ax in enumerate(axes.flatten()):
        histgram = cv.calcHist([hist_array[:, :, i]], [0], None, [256], [0, 256])
        ax.plot(histgram, color=COLORS[i], alpha=0.8)
        ax.set_title(LABELS[i])
        ax.set_xlim(-5, 256)
        ax.set_ylim(0, 50000)
    
    plt.tight_layout()
    plt.savefig("./hist.png")
    plt.show()

    

if __name__=="__main__":
    main()