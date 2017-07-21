from scipy.integrate import quad

def integrand(x,a,b):
    return a*x**2 + b

a = 2
b = 1
I = quad(integrand, 0, 1, args=(a,b)) #ax제곱 + b 함수를 0~1 구간으로 정적분
print(I)
