#导入socket模块
import socket
#创建socket
skt = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#绑定地址和端口
skt.bind(('127.0.0.1',9090))
#循环
while True:
    #调用接受消息
    data,addr = skt.recvfrom(1024)
    print(data)
    #接受成功回复消息
    rst = b'I am fine'
    skt.sendto(rst,addr)
    print('server Done')
    #关闭链接
    # skt.close()