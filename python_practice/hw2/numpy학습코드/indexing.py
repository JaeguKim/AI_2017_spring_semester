import numpy as np
x = np.arange(10) #size가 10인 배열생성
print(x[2]) #2
print(x[-2]) #8
x.shape = (2,5) #이제 x는 2치원배열이됨
print(x[1,3]) #8
print(x[1,-1]) #9
print(x[0])

x = np.arange(10) #size 10인 배열생성
print(x[2:5]) #2,3,4
print(x[1:7:2]) #1,3,5
y = np.arange(35).reshape(5,7)
print(y[1:5:2, ::3]) #1,3행에 3열 간격으로 선택하여 배열 구성 => [ [ 7 10 13 ] [ 21 24 27 ] ]

x = np.arange(10,1,-1)
print(x) #array([10,  9,  8,  7,  6,  5,  4,  3,  2])
temp = x[np.array([3, 3, 1, 8])]
print(temp) #array([7, 7, 9, 2])

x[np.array([3,3,-3,8])] #array([7, 7, 4, 2])

temp = y[np.array([0,2,4]), np.array([0,1,2])]
print(temp) # y[0,2], y[2,1], y[4,2]

temp = y[np.array([0,2,4]),1]
print(temp) # y[0,1], y[2,1], y[4,1]

temp = y[np.array([0,2,4])]
print(temp) # 0행,2행,4행 원소들 출력

#Bollean or "mask" index arrays
b = y>20
temp = y[b]
print(temp) #20보다 큰 원소들 모두 출력

x = np.arange(30).reshape(2,3,5) #0~29까지의 원소로 3차원 행렬 생성
print(x)
b = np.array([[True,True,False], [False,True, True]])
print(x[b]) #[x[0][0].x[0][1],x[1][1],x[1][2] 원소출력

#Structural indexing tools
print(y.shape) # (5,7)
temp = y[:,np.newaxis,:].shape
print(temp) #(5,1,7)

x = np.arange(10)
x[2:7] = 1
print(x)
x[2:7] = np.arange(5)

x = np.arange(0,50,10) #0,10,20,30,40
x[np.array([1,1,3,1])] += 1
print(x) # 0,11,20,31,40 =>1은 한번만 가산됨


