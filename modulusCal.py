import math

def modulusCalc(M, e, p):
        
        if M == 0:
            return 0

        if M == 1 or e == 0:
            return 1
        a = 1
        exp = 0
        while a <= p:
            if e == exp:
                return a%p
            a *= M
            exp += 1
            
        a %= p
        q = math.floor(e / exp)
        r = e % exp
        myNum = ((M**r)%p)
        return (modulusCalc(a, q, p)*myNum)%p