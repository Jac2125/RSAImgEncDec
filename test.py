from Encrypt import ImgEnc
from Decrypt import ImgDec

a = ImgEnc(bitNum=13, fileLen=5, path="./images/Python.jpg",pwd="418825")

fileName = a.encImg()

b = ImgDec(fileName, 418825)
b.decryptImg()