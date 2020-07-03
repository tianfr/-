#coding:utf-8
'''
file:server.py
date:2020/7/1 12:43
author:calmcat
email:747458467@qq.com
platform:win7.x86_64 pycharm python3
desc:p2p communication serverside
'''
import socketserver,json
import subprocess, socket

user_name = "a"
pwd = "a123"
conn_mode = None


connLst = []
##  连接列表，用来保存一个连接的信息（代号 地址和端口 连接对象）
class Connector(object):#连接对象类
    def __init__(self,account,password,addrPort,conObj):
        self.account = account
        self.password = password
        self.addrPort = addrPort
        self.conObj = conObj



class TCPServer(socketserver.BaseRequestHandler):

    def handle(self):
        print("got connection from",self.client_address)
        register = False
        while True:
            conn = self.request
            data = conn.recv(1024)
            if not data:
                continue
            dataobj = json.loads(data.decode('utf-8'))
            #如果连接客户端发送过来的信息格式是一个列表且注册标识为False时进行用户注册
            if type(dataobj) == list and not register:
                account = dataobj[0]
                password = dataobj[1]
                conObj = Connector(account,password,self.client_address,self.request)
                print(self.client_address,self.request)
                connLst.append(conObj)
                register = True
                continue
            print(connLst)
            #如果目标客户端在发送数据给目标客服端
            print("dataType", type(data))
            if len(connLst) > 0 and type(dataobj) == dict:

                if dataobj["mode"] == "1":
                    if dataobj["name"] == user_name and dataobj["keyword"] == pwd: data = {"froms": "server", "msg":"用户名密码验证正确"}
                    else: data = {"froms": "server", "msg":"用户名密码验证错误"}
                    data = json.dumps(data).encode("utf-8")
                    for obj in connLst:
                        if dataobj['froms'] == obj.account:

                            print(obj.account)
                            print("sendDataType", type(data))
                            obj.conObj.sendall(data)
                            sendok = True
                    continue

                sendok = False
                for obj in connLst:
                    if dataobj['to'] == obj.account:
                        obj.conObj.sendall(data)
                        sendok = True
                if sendok == False:
                    print('no target valid!')
            else:
                conn.sendall('nobody recevied!'.encode('utf-8'))
                continue
class UDPServer(socketserver.BaseRequestHandler):
    def handle(self):
        print("got connection from",self.client_address)
        register = False
        udp_socket_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        conn = self.request
        data, addr = conn
        # print(data)
        # data = conn.recvfrom(1024)
        if not data:
            return
        dataobj = json.loads(data.decode('utf-8'))
        #如果连接客户端发送过来的信息格式是一个列表且注册标识为False时进行用户注册
        if type(dataobj) == list and not register:
            account = dataobj[0]
            password = dataobj[1]
            conObj = Connector(account,password,self.client_address,self.request)
            print(self.client_address,self.request)
            connLst.append(conObj)
            register = True
            return
        # print("Register:",register)
        #如果目标客户端在发送数据给目标客服端
        # print("dataobjType:", type(dataobj))
        if len(connLst) > 0 and type(dataobj) == dict:

            if dataobj["mode"] == "1":
                if dataobj["name"] == user_name and dataobj["keyword"] == pwd: data = {"froms": "server", "msg":"用户名密码验证正确"}
                else: data = {"froms": "server", "msg":"用户名密码验证错误"}
                data = json.dumps(data).encode("utf-8")
                for obj in connLst:
                    if dataobj['froms'] == obj.account:

                        print(obj.addrPort)
                        # print("sendDataType", type(data))
                        # udp_socket_recv.connect(obj.addrPort)
                        # udp_socket_recv.send(data)
                        # obj.conObj.sendall(data)
                        udp_socket_recv.sendto(data,obj.addrPort)
                        sendok = True
                return

            sendok = False
            for obj in connLst:
                if dataobj['to'] == obj.account:
                    print(obj.addrPort)
                    udp_socket_recv.connect(obj.addrPort)
                    udp_socket_recv.sendto(data,obj.addrPort)
                    # obj.conObj.sendall(data)
                    sendok = True
            if sendok == False:
                print('no target valid!')
        else:
            conn.sendall('nobody recevied!'.encode('utf-8'))
            return
if __name__ == '__main__':

    while conn_mode not in ["1", "2"]: conn_mode = input("select mode: 1-tcp, 2-udp")
    if conn_mode == "1": 
        server = socketserver.ThreadingTCPServer(('127.0.0.1',8022),TCPServer)
        print('waiting for TCPconnection...')
    else:
        server = socketserver.ThreadingUDPServer(("127.0.0.1",8022),UDPServer)
        print('waiting for UDPconnection...')
    server.serve_forever()