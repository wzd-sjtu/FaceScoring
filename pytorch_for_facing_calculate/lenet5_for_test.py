import torch
import torch.nn as nn
import torch.nn.functional as F

# 下面我们稍微对着官方教程，实现一个比较简单的神经网络
# 也就是lenet-5网络，卷积神经网络的鼻祖


# 首先定义神经网络的结构
class Net(nn.Module):
    def __init__(self):
        # 固有的数据结构
        super(Net, self).__init__()
        # 输入1个，输出6个，5*5卷积核
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)

        # 第一个全连接层函数
        self.fc1 = nn.Linear(16*5*5, 120)
        # 第二个全连接层函数
        # 最终输出10个参数，是合理的吗？不知道
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
    def forward(self, x):
        # 池化的尺寸是2*2
        # 这里是把整个网络连接起来的操作，是合理的
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2, 2))
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    def num_flat_features(self, x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features
net = Net()
print(net)

params = list(net.parameters())
print(len(params))

# 下面对网络进行随机的输入
input = torch.randn(1, 1, 32, 32)
out = net(input)
print(out)

target = torch.randn(10)
target = target.view(1, -1)
criterion = nn.MSELoss # 这个是某一个损失函数，值得记忆的代码段
loss = criterion(out, target) # 这二者的意义是明确的


# 下面是网络的自动反向传播的操作
net.zero_grad()
# 这里的backward反向传播参数的meaning是什么呢？意义明显不够明确
out.backward(torch.randn(1, 10))

# 这里生成的都是pytorch专用的变量，名字叫张量

# 当反向传播完成以后，就可以更新神经网络对应的参数
# 不妨使用简易的随机梯度下降方法

learning_rate = 0.01
# 可以认为，这里的网络写法是非常easy的
for f in net.parameters():
    f.data.sub_(f.grad.data*learning_rate)

# 不妨先使用lenet5对颜值适当打分，从而获取对应的内容
# 这个是可以的，先写一个简单版本的，再去写alexnet的内容
# pytorch确实算是比较好入门的，需要把代码对着敲一遍，理解即可

