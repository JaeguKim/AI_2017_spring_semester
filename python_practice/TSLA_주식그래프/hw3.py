#TSLA 회사의 주식데이터(2010-2014)를 가져와서 화면에 그래프로 변화를 그려주는 프로그램입니다.

import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt

#CSV 파일 열기
my_data = genfromtxt('TSLA_stockprice2.csv', delimiter=',' ,names=True)
fname = open('TSLA_stockprice2.csv','r')
#0번째에서 6번째 칼럼을 대상으로 각각의 그래프 생성
plt.plotfile(fname, (0, 1, 2, 3, 4, 5, 6))

#Open,High,Low,Close 각각의 최대값을 받아옴
max_open = np.max(my_data['Open'])
max_high = np.max(my_data['High'])
max_low = np.max(my_data['Low'])
max_close = np.max(my_data['Close'])

#분석결과를 콘솔창에 출력
print('***** TSLA_stockprice 분석 결과값 *****')
print('open의 최대값 : '+str(max_open))
print('high의 최대값 : '+str(max_high))
print('low의 최대값 : '+str(max_low))
print('close의 최대값 : '+str(max_close))

#최종적인 결과를 화면에 출력하기
plt.suptitle('TSLA_stockprice',fontsize = 20) #그래프 제목설정
plt.show()
