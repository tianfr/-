import os

from .chatWindow import Ui_MainWindow
from object.client import Client
from object.message import Message
from mysql.connectMysql import ConnetMysql
from object import myRSA
from PyQt5 import QtWidgets, QtGui
import datetime
import base64

class Chat(QtWidgets.QWidget, Ui_MainWindow):

    def __init__(self):
        super(Chat, self).__init__()
        self.setupUi(self)
        self.db = ConnetMysql()
        self.id = None
        self.client = None
        self.chat_record = []
        self.saved_record_row = 0
        self.pushButton.clicked.connect(self._send)
        self.pushButton_2.clicked.connect(self._save_chat_record)
        self.pushButton_3.clicked.connect(self._send_file)
        self.pushButton_4.clicked.connect(self._choose_directory)

    def login(self, id):
        self.id = id
        result = self.db.search("select id from users where alive = 1 and id != '%s'"%(self.id))
        print(result)
        if result != []:
            users_alive = list(zip(*result))[0]
            self.listWidget.addItems(users_alive)
        self.client = Client(self)
        self._init_browser()

    def _send(self):
        msg = self.textEdit.toPlainText()

        users = self._get_users()
        if users == []:
            QtWidgets.QMessageBox.information(self, "警告", "请在右栏选择发送对象")
            return
        if msg == "":
            QtWidgets.QMessageBox.information(self, "警告", "输入栏为空")
            return
        for user in users:
            self._from_id_RSA_dic = myRSA.generate_RSAkey_with_sig(2048, self.id)
            self._to_id_RSA_dic = myRSA.generate_RSAkey_with_sig(2048, user)
            self._from_id = self.id
            self._to_id = user
            self._value = msg
            # 先拿自己私钥加密增加签名，再拿对方公钥加密保护数据
            print("Start Encryption")
            # print("before encrypt", type(self._value))
            self._sign = myRSA.to_sign_with_private_key(self._value, self._from_id_RSA_dic["pri_key"])
            # print("Finish signature.")
            init_value = self._value
            self._value = myRSA.encrypt_with_rsa(self._value, self._to_id_RSA_dic["pub_key"])
            decode_value = myRSA.decrypt_with_rsa(self._value, self._to_id_RSA_dic["pri_key"])
            print("tesst", decode_value == init_value)
            # print("after encrypt", type(self._value))
            # self._value = self._value.decode('utf-8', 'ignore')
            print("value")
            print(self._value)
            print("sign")
            print(self._sign)
            self._value = base64.b64encode(self._value).decode("utf-8")
            # print("before sign", self._sign)
            # self._sign = self._sign.decode('utf-8', 'ignore')
            before_sign = self._sign
            self._sign = base64.b64encode(self._sign).decode("utf-8")
            # print(self._sign == self._sign.decode("utf-8").encode("utf-8"))

            # tmp = self._sign.encode('utf-8')
            # tmp = base64.b64decode(self._sign)
            # print("after sign", tmp==before_sign)
            print("Encryption Completes")

            byte_msg = Message("transmit", self.id, user, self._value, sign=self._sign).content_bytes
            print("complete message")
            self.client.socket.send(byte_msg)
            print("Transmit complete")
            browser_msg = "({} to {}): {}".format(datetime.datetime.now(), user, msg).rstrip()
            self.textBrowser.append(browser_msg + "\n")
            self.chat_record.append(browser_msg)
        self.textEdit.clear()

    def _send_file(self):
        file_path= self.lineEdit.text()
        if not os.path.isfile(file_path):
            QtWidgets.QMessageBox.information(self, "错误", "文件不存在，请检查文件路径是否正确")
            return
        file_name = file_path.split("/")[-1]
        file_size = os.path.getsize(file_path)
        users = self._get_users()
        if users == []:
            QtWidgets.QMessageBox.information(self, "警告", "请在右栏选择发送对象")
            return
        f = open(file_path, "rb")
        content = f.read()
        f.close()
        for user in users:
            byte_file_header = Message("file", self.id, user, file_size, file_name).content_bytes
            self.client.socket.send(byte_file_header)
            self.client.socket.sendall(content)

    def _get_file_path_and_name(self):
        return "/home/agwave/PycharmProjects/socket/debug/libserver.py", "libserver.py"

    def _choose_directory(self):
        get_directory_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                              "选取文件所在文件夹",
                                                              "/home/agwave/PycharmProjects/socket")
        if str(get_directory_path) != "":
            self.lineEdit.setText(str(get_directory_path))
            QtWidgets.QMessageBox.information(self, "提示", "文件夹地址已输入，请继续输入文件名")

    def _sign_out(self):
        self.client.sign_out()
        self.close()

    def _save_chat_record(self):
        if len(self.chat_record) == self.saved_record_row:
            QtWidgets.QMessageBox.information(self, "警告", "当前保存记录已是最新")
        else:
            self.saved_record_row = self.db.save_chat_record(self.chat_record, self.saved_record_row, self.id)
            QtWidgets.QMessageBox.information(self, "信息", "已成功保存聊天记录")

    def _init_browser(self):
        self.textBrowser.append("---------过往聊天记录---------")
        sql = "select record from {} order by 'date', 'time'".format(self.id+"_record")
        record = self.db.search(sql)
        for r in record:
            self.textBrowser.append(r[0])
        self.textBrowser.append("----------------------------")

    def _get_users(self):
        users = []
        items = self.listWidget.selectedItems()
        for item in items:
            users.append(item.text())
        return users

    def closeEvent(self, QCloseEvent):
        reply = QtWidgets.QMessageBox.question(self,
                                               '退出',
                                               "是否要退出系统？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self._sign_out()
        else:
            QCloseEvent.ignore()

