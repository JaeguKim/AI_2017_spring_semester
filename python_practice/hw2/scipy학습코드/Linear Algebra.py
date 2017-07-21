import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt

#numpy.matrix vs 2D numpy.ndarray
A = np.mat('[1 2;3 4]')
print(A)
print(A.I) #A의 역행렬 출력

b = np.mat('[5 6]')
print(b.T) #B의 transpose 행렬
print(A*b.T)

A = np.array([[1,2], [3,4]])
print(A)
print(linalg.inv(A)) #scipy모듈로 역행렬 구하기

b = np.array([[5,6]]) #2D array

#finding inverse
A = np.array([[1,3,5], [2,5,1], [2,3,8]])
print(A)
print(linalg.inv(A))

print(A.dot(linalg.inv(A)))

#solving linear system
A = np.array([[1, 2], [3, 4]]) #x+2y = 5 와 3x+4y = 6 연립방정식 해구하기
b = np.array([[5], [6]])
linalg.inv(A).dot(b)
A.dot(linalg.inv(A).dot(b)) - b #0이 되는지 확인
np.linalg.solve(A, b) #해를 구하는 더 빠른 방법
A.dot(np.linalg.solve(A, b)) - b

#Finding Determinant
A = np.array([[1,2],[-3,4]])
linalg.det(A) #determinant 구하기

#computing norms
A=np.array([[1,2],[3,4]])
linalg.norm(A)

#Solving linear least-squares problems and pseudo-inverses
c1, c2 = 5.0, 2.0
i = np.r_[1:11]
xi = 0.1*i
yi = c1*np.exp(-xi) + c2*xi
zi = yi + 0.05 * np.max(yi) * np.random.randn(len(yi))
A = np.c_[np.exp(-xi)[:, np.newaxis], xi[:, np.newaxis]]
c, resid, rank, sigma = linalg.lstsq(A, zi)

xi2 = np.r_[0.1:1.0:100j]
yi2 = c[0]*np.exp(-xi2) + c[1]*xi2
plt.plot(xi,zi,'x',xi2,yi2)
plt.axis([0,1.1,3.0,5.5])
plt.xlabel('$x_i$')
plt.title('Data fitting with linalg.lstsq')
plt.show()