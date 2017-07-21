import torch
import torchvision
import torchvision.datasets as dset
import torchvision.transforms as transforms
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool  = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1   = nn.Linear(4*4*16, 120)
        self.fc2   = nn.Linear(120, 84)
        self.fc3   = nn.Linear(84, 10)
        self.criterion = nn.CrossEntropyLoss()
    def forward(self, x,target):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        #print(x.size())
        x = x.view(-1, 4*4*16)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        loss = self.criterion(x,target)
        return x,loss
    def name(self):
        return 'LeNet-5'

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.1307,), (0.3081,))])

batch_size = 128
kwargs = {'num_workers': 1, 'pin_memory': True}
trainset = dset.MNIST(root='MNIST', train=True, transform=transform, download=True)
train_loader = torch.utils.data.DataLoader(trainset, batch_size = batch_size, shuffle=True, **kwargs)

testset = dset.MNIST(root='MNIST', train=False, transform=transform)
test_loader = torch.utils.data.DataLoader(testset, batch_size=batch_size,shuffle=False, **kwargs)

print ('==>>> total training batch number: {}'.format(len(train_loader)))
print ('==>>> total testing batch number: {}'.format(len(test_loader)))
model = LeNet()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

for epoch in range(10):  # loop over the dataset multiple times
    #training
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        data, target = Variable(data), Variable(target)
        _,loss = model(data, target)
        loss.backward()
        optimizer.step()
        if batch_idx % 100 == 0:
                print ('==>>> epoch: {}, batch index: {}, train loss: {:.6f}'.format(epoch, batch_idx, loss.data[0]))
    #testing
    correct_cnt, ave_loss = 0,0
    for batch_idx, (data,target) in enumerate(test_loader):
        x,target = Variable(data),Variable(target)
        score,loss = model(x,target)
        _,pred_label = torch.max(score.data,1)
        correct_cnt += (pred_label == target.data).sum()
        ave_loss += loss.data[0]
    accuracy = correct_cnt*1.0/len(test_loader)/batch_size
    ave_loss /= len(test_loader)
    print ('==>>> epoch: {}, test loss: {:.6f}, accuracy: {:.4f}'.format(epoch, ave_loss, accuracy))

torch.save(model.state_dict(), model.name())
