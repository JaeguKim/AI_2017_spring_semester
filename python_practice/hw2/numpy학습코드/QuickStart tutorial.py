import numpy as np
#Printing Arrays
a = np.arange(6) #일차원 배열
b = np.arange(12).reshape(4,3) #2차원배열
c = np.arange(24).reshape(2,3,4) #3차원배열
A = np.array( [[1,1], [0,1]] )
B = np.array( [[2,0], [3,4]] )
print(A*B) #elementwise product
A.dot(B) #matrix product
np.dot(A, B) #another matrix product
a = np.random.random((2,3))
print(a)
print(a.min())
print(a.max())
b = np.arange(12).reshape(3,4)
print(b.sum(axis=0)) #sum of each column
b.min(axis=1) #min of each row
b.cumsum(axis=1)  #cumulative sum along each row

#Universal Function
B = np.arange(3)
np.exp(B)
np.sqrt(B)
C = np.array([2., -1., 4.])
D = np.add(B, C)

#Indexing, Slicing and Iterating
a = np.arange(10)**3 #원소들값 3제곱

#Multidimensional
def f(x,y):
    return 10*x+y

b = np.fromfunction(f,(5,4),dtype=int)
b[0:5, 1] # each row in the second column of
b[ : ,1]
b[1:3, : ] # each column in the second and third row of b

for row in b:
     print(row)

for element in b.flat: #한원소씩 접근
    print(element)

#Stacking together different arrays
a = np.floor(10*np.random.random((2,2)))
print(a)
b = np.floor(10*np.random.random((2,2)))
np.vstack((a,b))
np.hstack((a,b))
np.column_stack((a,b))

#Splitting one array into several smaller ones
a = np.floor(10*np.random.random((2,12)))
np.hsplit(a,3) #split a into 3
np.hsplit(a,(3,4))   # Split a after the third and the fourth column

#Copies and Views
a = np.arange(12)
b = a
b.shape = 3,4
a.shape

#View or Shallow Copy
c = a.view()
c is a #true
c.base is a
#deep copy
d = a.copy()
d is a #false

#Linear Algebra
#Simple Array Operations
a = np.array([[1.0, 2.0], [3.0, 4.0]])
a.transpose()
u = np.eye(2) # unit 2x2 단위 matrix 생성
np.dot (j, j) # matrix product

