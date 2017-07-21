file = open("input.txt",'r')
file2 = open("data_set.txt",'w')
file3 = open("test_set.txt",'w')
file4 = open("validation_set.txt",'w')

for i in range(5000):
    file2.write(file.readline())

for i in range(500):
    file4.write(file.readline())

for i in range(2624):
    file3.write(file.readline())
