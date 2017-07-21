import numpy as np

#2*3 array 생성 data type은 int32
x = np.array([[1,2,3], [4,5,6]], np.int32)
print(type(x)) #<class 'numpy.ndarray'>
print(x.shape) #(2,3)
print(x.dtype) #dtype('int32')
print(x[1,2]) #6

y = x[:,1]
print(y) #[2 5]
y[0] = 9
print(y) #[9 5]
print(x) #[[1 9 3]  [4 5 6]]

x = np.ndarray(shape=(2,2), dtype=float, order='C') #2*2 float 타입행렬 생성
print(x)

y = np.ndarray((2,), buffer=np.array([1,2,3]),offset=np.int_().itemsize,
dtype=int)
print(y)