#polynomials
import numpy as np
from numpy import poly1d

p = poly1d([3,4,5]) #3x+4x+5
print(p)

print(p*p) #9x + 24x + 46x + 40x + 25

#Vectorizing functions

def addsubtract(a,b):
    if a > b:
        return a-b
    else:
        return a+b


vec_addsubtract = np.vectorize(addsubtract)
print(vec_addsubtract([0,3,6,9], [1,3,5,7]))

#Type handling
print(np.cast['f'](np.pi)) #3.1415927410125732

#Other useful functions
x = np.r_[-2:3]
print(x)
print(np.select([x > 3, x >= 0], [0,x+2]))



