import pickle
import numpy as np
from glob import glob

"""ハイパーパラメータ"""
filename = "./*.nh9"
hor = 2048
ver = 1080
SpectDim = 151
"""-----------------"""

def load_data(name,hor,ver,SpectDim):
        with open(name,'rb') as f:
                img = np.fromfile(f,np.uint16,-1)
                img = np.reshape(img,(ver,SpectDim,hor))
                img = np.transpose(img,(0,2,1))
        return img

def change_data():
        for fn in glob(filename):
                Str = fn.split('_')
                saveName = Str[0] + "_" + Str[1] + ".pkl"
                data = load_data(fn,hor,ver,SpectDim)
                with open(saveName,'wb') as f:
                        pickle.dump(data,f)

if __name__=="__main__":
        change_data()