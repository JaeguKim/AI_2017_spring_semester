import numpy as np
x = np.float32(1.0)
print(x)
y = np.int_([1,2,4])
print(y)
z = np.arange(3, dtype=np.uint8)
print(z)

temp = np.array([1,2,3], dtype = 'f')
print(temp)

temp = z.astype(float) #uint8 datatype을 float로 변경
print(temp)

temp = np.int8(z)
print(temp)

temp = z.dtype
print(temp)

d = np.dtype(int)
print(d)

temp = np.issubdtype(d, int) #d가 int타입이면 true 아니면 false를 반환
print(temp) # true

temp = np.issubdtype(d, float) #d가 float타입이면 true 아니면 false를 반환
print(temp) #false
