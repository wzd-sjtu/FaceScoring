from pic_process import pic_process
import socket
import base64
import os

net_dict = {"alexnet":1, "resnet18":2}

if __name__ == '__main__':
    # 这里1代表alexnet 2代表resnet
    net_choice = 1
    pic_choice = "lyf.jpg"
    pic = pic_process()

    pic.initial_net(net_choice)
    # 需要在这里写一些多进程的内容
    # 稍微有点忘了socket通信的写法

    # 这里的路径应当是用socket传过来的才对
    # net_choice也应该是的
    # pic.calculate_scores("lyf.jpg")
    # scores = pic.calculate_scores(pic_choice)
    # scores_matrix = scores.numpy()
    # 演值打分应当是满分为10分从而比较合理的
    # print(scores_matrix[0][0]*2)

    # 定义一小部分基础信息
    # 这里最好使用ip地址，这个是基本上的最优解

    # 以下是网络连接的部分
    host = '192.168.1.108'
    port = 11222

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
     # char* data = "alexnet"
    # 在while循环里面，应当实现一个简易的状态机
    state_IDEL = 0
    state_GET_NET_CHOICE = 1
    state_GET_PIC_SCORES = 2
    state_CHANGE_NET_CHOICE = 3
    state_EXIT = 4
    state_WAIT_FOR_MESSAGE = 5
    # 这里给出了状态机的状态定义，暂时还不清楚有什么meaning
    state = state_IDEL

    clientsock, clientaddr = None, None
    # 目标是和服务器连接起来

    # 以下是一个比较简单的tcp客户端，拥有比较复杂的通信机制
    # 在某种程度上，我自己创造了协议
    while 1:
        # 这里一直处于一种循环之中

        if state == state_IDEL:
            # 这里正处于accept阻塞状态的
            clientsock, clientaddr = s.accept()
            # 这一句话现在还没有出现，我直接裂开了
            print("successfully connect!")
            # 发现成功和目标完成了连接，非常高兴地
            # print(clientsock)
            # print(clientaddr)
            # 之后就可以获取对应的connection了
            # 后面的客户端可以使用c语言写网络进程
            recv_data = clientsock.recv(1024)  # 接收1024个字节
            print('接收到的数据为:', recv_data.decode('utf-8'))

            # 去除掉对应的内容哦
            recv_data = recv_data.decode('utf-8')
            recv_data.strip()
            print("recvived data is " + recv_data)
            if recv_data == "alexnet" or recv_data == "resnet18":
                state = state_GET_NET_CHOICE
                net_choice = net_dict[recv_data]
                clientsock.send("okay with net choice \n please send an image".encode('utf-8'))
            else:
                clientsock.send("please resend net choice".encode('utf-8'))

        elif state == state_GET_NET_CHOICE:
            pic.initial_net(net_choice)

            recv_data = None
            # for i in range(10):
            #    recv_data = recv_data + clientsock.recv(1024)
            # 这里别人用的是复杂的算法，我不妨使用重复recv的做法，提高efficiency
            # 稍微有点复杂的

            file_name = "test.jpg"
            new_file = open(file_name, "wb")

            time = 0
            length_of_pic = int((clientsock.recv(1024)).decode('utf-8'))
            print(length_of_pic)
            clientsock.send(("the size of pic is " + str(length_of_pic)).encode('utf-8'))
            while True:
                mes = clientsock.recv(4096)
                if mes:
                    new_file.write(mes)
                    time += len(mes)
                    # print(time)
                if time >= length_of_pic:
                    new_file.close()
                    break
            # 进入下一个状态
            state = state_GET_PIC_SCORES
            pic_choice = file_name
            clientsock.send("we have got the picture of face".encode('utf-8'))


        elif state == state_GET_PIC_SCORES:
            scores = pic.calculate_scores(pic_choice)
            scores_matrix = scores.numpy()
            # 将打分转发过去
            # scores = pic.calculate_scores(pic_choice)

            # 演值打分应当是满分为10分从而比较合理的
            # print(scores_matrix[0][0]*2)

            clientsock.send(("the score of your face is " + str(scores_matrix[0][0]*2)).encode('utf-8'))

            state = state_WAIT_FOR_MESSAGE

        elif state == state_CHANGE_NET_CHOICE:
            break
        elif state == state_WAIT_FOR_MESSAGE:
            clientsock, clientaddr = s.accept()
            # 之后就可以获取对应的connection了
            # 后面的客户端可以使用c语言写网络进程
            recv_data = clientsock.recv(1024)  # 接收1024个字节
            print('接收到的数据为:', recv_data.decode('utf-8'))

        elif state == state_EXIT:
            clientsock.close()

