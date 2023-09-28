from SQLTools import sqlInterpreter as st
import numpy as np
from PIL import Image
from modulusCal import modulusCalc

class ImgDec:
    
    def __init__(self, fileName, pwd):
        self.__fileName = fileName
        self.__myInterp = st(pwd)
        self.__privateKey, self.__n = self.__myInterp.getPrivateKeyPair(fileName)
        self.__imgArr = np.load("./encArrays/"+fileName+".npy")

    def decryptImg(self):
        encArr = self.__imgArr
        arr = np.empty([encArr.shape[0], encArr.shape[1], encArr.shape[2]], dtype=np.int8)
        for row in range(encArr.shape[0]):
            for col in range(encArr.shape[1]):
                R = modulusCalc(encArr[row][col][0], self.__privateKey, self.__n)
                G = modulusCalc(encArr[row][col][1], self.__privateKey, self.__n)
                B = modulusCalc(encArr[row][col][2], self.__privateKey, self.__n)
                arr[row][col] = [R, G, B]
        img = Image.fromarray(arr.astype(np.uint8))
        img.save(self.__fileName + '.jpg')
