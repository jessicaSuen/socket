#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：client.py

import socket               # 导入 socket 模块
import threading
import time

# 客户端
class Client(object):
	"""docstring for Client"""

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostname()     # 获取本地主机名
	ip_port = ('127.0.0.1',9999)    # 设置端口

	bufsize = 1024

	def __init__(self):
		super(Client, self).__init__()
		# self.clientnum = clientnum

	def run(self):
		self.client.connect(self.ip_port)

		# 客户端
		i = 1
		while i < 10000:
			# 使用TCP协议进行数据传输
			# client端将数据发送给server
			num = i
			data = str.encode(str(num)) # 获取要发送给客户端的信息
			# 将信息进行编码以后使用send方法进行发送,
			# 在python2中信息可以不用进行编码就可以发送
			print(data)
			self.client.send(data)

			# 当发送信息为空时，断开与服务器的连接

			
			# 收到server更新后的数据
			data = self.client.recv(self.bufsize)

			time.sleep(1)
			i = float(bytes.decode(data))
			print(i)


		self.client.close()


def auto_generate(clientnum):
	print('client num:',clientnum)
	for i in range(0,clientnum):
		#循环生成客户端线程
		s = Client()
		t=threading.Thread(target=s.run,args=()) 
		t.start()

if __name__ == '__main__':
	s = Client()
	s.run()
			
