import random
import math
import string
import numpy as np
from PIL import Image
import SQLTools as st
from modulusCal import modulusCalc

# If there are same numbers, why not replacing it when one is calculated?
# Resolve issue when calculating large number modulus like a*=M
# Using a compression algorithm to reduce the file size?

class ImgEnc:
    lowPrimes =  [2,3,5,7,11,13,17,19,23,29,31,37,41]

    def __init__(self, bitNum, fileLen, path, pwd):
        self.__p = self.genLargePrime(bitNum)
        self.__q = self.genLargePrime(bitNum)
        self.modulusCalc = modulusCalc
        self.getRandomString(fileLen)
        self.__n = self.__p * self.__q
        phi = (self.__p - 1) * (self.__q - 1)
        self.__publicKey = self.getCoprime(phi)
        self.__privateKey = self.intSols(self.__publicKey, phi)
        self.__path = path
        self.__pwd = pwd

    def encImg(self):
        logger = st.sqlInterpreter(self.__pwd)
        imageArr = np.asarray(Image.open(self.__path))
        arr = np.empty([imageArr.shape[0], imageArr.shape[1], imageArr.shape[2]], dtype=np.int64)

        for row in range(imageArr.shape[0]):
            for col in range(imageArr.shape[1]):
                R = self.encNum(imageArr[row][col][0], self.__publicKey, self.__p, self.__q, self.__n)
                G = self.encNum(imageArr[row][col][1], self.__publicKey, self.__p, self.__q, self.__n)
                B = self.encNum(imageArr[row][col][2], self.__publicKey, self.__p, self.__q, self.__n)
                arr[row][col] = [R, G, B]

        np.save("./encArrays/" + self.__fileName, arr)
        logger.logInfo(self.__fileName, self.__n, self.__privateKey)
        return self.__fileName

    def getRandomString(self, length):
        # With combination of lower and upper case
        result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
        self.__fileName = result_str

    def rabinMiller(self, n):
        if n&1 == 0:
            return False
        s = n-1
        for i in self.lowPrimes:
            while s&1 == 0:
                s /= 2
                s = int(s)
                v = pow(i,s,n)
                if s&1 == 1 and v != 1:
                    return False
                elif s&1 == 0 and v != -1:
                    return False
            
        return True

    def genLargePrime(self, k):
        #k is the desired bit length
        r=100*(math.log(k,2)+1) #number of attempts max
        r_ = r
        while r>0:
            #randrange is mersenne twister and is completely deterministic
            #unusable for serious crypto purposes
            n = random.randrange(2**(k-1),2**(k))
            r-=1
            if self.rabinMiller(n) == True:
                return n
        return "Failure after "+str(r_) + " tries."

    def getCoprime(self, num):
        while True:
            coprime = random.randint(2, num)
            if math.gcd(coprime, num) == 1:
                return coprime
            
    def intSols(self, a, b):
        x_1 = 1
        y_1 = 0

        x_2 = 0
        y_2 = 1
        d = math.gcd(a, b)
        temp = b
        while b != 0:
            q = math.floor(a/b)
            r = a%b
            a = b
            b = r
            x_temp = x_1 - x_2*q
            y_temp = y_1 - y_2*q
            x_1 = x_2
            y_1 = y_2

            x_2 = x_temp
            y_2 = y_temp
        
        while x_1 < 0:
            x_1 += int(temp/d)
        return x_1

    def FLT(self, e, p):
        if not self.rabinMiller(p):
            return -1
        exp = p - 1
        return e%exp

    def getCipher(self, p, q, n, enc_p, enc_q):
        if p > q:
            cipher = (self.intSols(p, q)*(enc_q - enc_p)*p+enc_p)
        else:
            cipher = self.intSols(q, p)*(enc_p - enc_q)*q + enc_q
        return self.getPositiveCipher(cipher, n)
            

    def getPositiveCipher(self, cipher, n):
        while cipher < 0 or cipher > n:
            if cipher > n:
                cipher -= n
            if cipher < 0:
                cipher += n
        return cipher

    def encNum(self, num, publicKey, p, q, n):
        exp_p = self.FLT(publicKey, p)
        enc_p = self.modulusCalc(num, exp_p, p)
        exp_q = self.FLT(publicKey, q)
        enc_q = self.modulusCalc(num, exp_q, q)
        cipher = self.getCipher(p, q, n, enc_p, enc_q)
        cipher = self.modulusCalc(num, publicKey, n)
        return cipher