from socket import *

# 创建socket
tcp_client_socket = socket(AF_INET, SOCK_STREAM)

# 目的信息
server_ip = '192.168.50.17'
server_port = 11222

# 链接服务器
tcp_client_socket.connect((server_ip, server_port))

# 提示用户输入数据
while True:
    # 首先发送选择的网络信息
    send_data = input("请输入要发送的数据：")

    tcp_client_socket.send(send_data.encode("utf-8"))

    # 接收对方发送过来的数据，最大接收1024个字节
    recvData = tcp_client_socket.recv(1024)
    print('接收到的数据为:', recvData.decode('utf-8'))

    # 接下来发送某个图片过去
    file_name = input("请输入要发送的图片路径：")
    files = open(file_name, "rb")
    mes = files.read()
    
    # 这里发送的是图片流
    tcp_client_socket.send(str(len(mes)).encode('utf-8'))
    recvData = tcp_client_socket.recv(1024)
    print('接收到的数据为:', recvData.decode('utf-8'))

    tcp_client_socket.send(mes)


    # 接收对方发送过来的数据，最大接收1024个字节
    recvData = tcp_client_socket.recv(1024)
    print('接收到的数据为:', recvData.decode('utf-8'))

    recvData = tcp_client_socket.recv(1024)
    print('接收到的数据为:', recvData.decode('utf-8'))

# 关闭套接字
tcp_client_socket.close()

'''
————————————————
版权声明：本文为CSDN博主「Junieson」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/i6223671/article/details/100052423
'''