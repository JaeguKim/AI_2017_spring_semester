import numpy as np

a = np.array([1.0,2.0,3.0])
b = np.array([2.0,2.0,2.0])
print(a*b)

a = np.array([1.0,2.0,3.0])
b= 2.0
print(a*b)

#General Boradcasting Rules
x = np.arange(4)
xx = x.reshape(4,1)
y = np.ones(5) #1 다섯개로 이루어진 1D 배열
print(y)
z = np.ones((3,4))

print(xx + y) # 4X5행렬 생성
a = np.array([0.0,10.0,20.0,30.0])
b = np.array([1.0,2.0,3.0])
temp = a[:,np.newaxis] + b
print(temp.shape) #4X3 행렬생성
print(temp)

