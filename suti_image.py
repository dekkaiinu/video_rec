import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

import NHdata2pkl

""
LOADPATH = "D:\\ueno_zoo\\penguin\\20230607\\20230607\\set7\\Scan(s100x5,g100,9.88ms,350-1100)_20230607_150837.nh9"
SAVEPATH = "./suti_images/a/"

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

    band_image = band_image_array(array, 50)
    cv.imwrite(SAVEPATH + "50.png", sutiration(band_image))
    cv.waitKey(0)

    band_image = band_image_array(array, 10)
    cv.imwrite(SAVEPATH + "10.png", sutiration(band_image))
    cv.waitKey(0)
    band_image = band_image_array(array, 90)
    cv.imwrite(SAVEPATH + "90.png", sutiration(band_image))
    cv.waitKey(0)

def band_image_array(array, band):
    band_array = array[:, :, band]
    return band_array

def sutiration(array):
    image = np.zeros((VER, HOR, 3))
    image[:, :, 0] = array
    image[:, :, 1] = array
    image[:, :, 2] = array

    for v in range(VER):
        for h in range(HOR):
            if array[v, h] >= 250:
                image[v, h, 0] = 0
                image[v, h, 1] = 0
            if array[v, h] <= 10:
                image[v, h, 1] = 0
                image[v, h, 2] = 0
    
    return image

if __name__=="__main__":
    main()