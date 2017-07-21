training_data = open('xxx.data.txt','r')

for line in training_data:
    temp1 = line.split(',')
    if (temp1[22].strip('\n') == 'p' or temp1[22].strip('\n') == 'u'):
        print(temp1)
print('없음')

