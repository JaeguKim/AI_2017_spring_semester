import numpy as np

x = np.array([(1,2.,'Hello'), (2,3.,"world")],dtype = [('foo', 'i4'),('bar', 'f4'), ('baz', 'S10')])
print(x[1])
y = x['bar']
print(y)
y[:] = 2*y
print(y) #4,6
print(x) #(1,  4., b'Hello') (2,  6., b'world')
x[1] = (-1,-1., "Master")
print(x)

x = np.zeros(3, dtype='3int8, float32, (2,3)float64')
print(x)


