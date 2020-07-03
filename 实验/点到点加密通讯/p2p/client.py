#coding:utf-8
'''
file:client.py.py
date:2020/7/1 11:01
author:calmcat
email:747458467@qq.com
platform:win7.x86_64 pycharm python3
desc:p2p communication clientside
'''
from socket import *
import threading,sys,json,re

HOST = '127.0.0.1'  ##
PORT=8022
BUFSIZ = 102400  ##缓冲区大小  1K
ADDR = (HOST,PORT)
MYPORT = 53825
MYADDR = ("127.0.0.1", 53825)
conn_mode = None





userAccount = None
def register():
    myre = r"^[_a-zA-Z]\w{0,}"
    #正则验证用户名是否合乎规范
    accout = input('Please input your account: ')
    if not re.findall(myre, accout):
        print('Account illegal!')
        return None
    password1  = input('Please input your password: ')
    password2 = input('Please confirm your password: ')
    if not (password1 and password1 == password2):
        print('Password not illegal!')
        return None
    global userAccount
    userAccount = accout
    return (accout,password1)

class inputdata(threading.Thread):
    def run(self):
        while True:
            mode = input("Please select mode: 1 - validation; 2 - messageSender")
            if mode == "1":
                valid_name = input("Please input username:")
                valid_keyword = input("Please input keyword:")
                dataObj = {"mode": mode, "name": valid_name, "keyword": valid_keyword, "froms": userAccount}
                datastr = json.dumps(dataObj)
                tcpCliSock.sendto(datastr.encode('utf-8'),ADDR)
            elif mode == "2":
                sendto = input('to>>:')
                msg = input('msg>>:')
                dataObj = {"mode": mode,'to':sendto,'msg':msg,'froms':userAccount}
                datastr = json.dumps(dataObj)
                tcpCliSock.sendto(datastr.encode('utf-8'),ADDR)
            else: continue
            


class getdata(threading.Thread):
    def run(self):
        while True:
            if conn_mode == "1": data = tcpCliSock.recv(BUFSIZ)
            else: data, addr = tcpCliSock.recvfrom(BUFSIZ)
                
            dataObj = json.loads(data.decode('utf-8'))
            print('{} -> {}'.format(dataObj['froms'],dataObj['msg']))


def main():
    global conn_mode,tcpCliSock,MYADDR,MYPORT

    while conn_mode not in ["1","2"]: conn_mode = input("select mode: 1-tcp, 2-udp")
    if conn_mode == "1":
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
    else:

        tcpCliSock = socket(AF_INET,SOCK_DGRAM)
        # tcpCliSock.bind(MYADDR)

    while True:
        regInfo = register()
        if  regInfo:
            datastr = json.dumps(regInfo)
            if conn_mode == "1": tcpCliSock.send(datastr.encode('utf-8'))
            else: tcpCliSock.sendto(datastr.encode('utf-8'),ADDR)
            break
    myinputd = inputdata()
    mygetdata = getdata()
    myinputd.start()
    mygetdata.start()
    myinputd.join()

    mygetdata.join()






if __name__ == '__main__':
    main()