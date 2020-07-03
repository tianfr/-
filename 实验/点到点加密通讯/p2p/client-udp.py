#导入模块
import socket
#创建socket
skt  = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#创建发送消息和发送目标
msg = b'Hello world'
addr = ('127.0.0.1',9090)
skt.sendto(msg,addr)
#接受回复
rst = skt.recvfrom(1024)
print(rst)
print('client done')
#关闭链接
skt.close()