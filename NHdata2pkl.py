import pickle
import numpy as np
from glob import glob

"""ハイパーパラメータ"""
FILENAME = "./*.nh9"
#filename = "C:\\Users\\youta\\dataset\\Img-d_frozen_length120_height2_white(s20,g50,49.88ms,350-1100)_20230424_145859.nh9"
HOR = 2048
VER = 1080
SPECDIM = 151
"""-----------------"""

def load_data(name,hor,ver,SpectDim):
        with open(name,'rb') as f:
                img = np.fromfile(f,np.uint16,-1)
                img = np.reshape(img,(ver,SpectDim,hor))
                img = np.transpose(img,(0,2,1))
        return img

def change_data():
        for fn in glob(FILENAME):
                Str = fn.split('_')
                saveName = Str[0] + "_" + Str[1] + ".pkl"
                data = load_data(fn,HOR,VER,SPECDIM)
                with open(saveName,'wb') as f:
                        pickle.dump(data,f)

if __name__=="__main__":
        change_data()