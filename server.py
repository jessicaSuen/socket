#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py

import socket               # 导入 socket 模块
import threading
import time

# 服务端
class Server(object):
	"""docstring for Server"""

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # 创建 socket 对象
	host = socket.gethostname()  # 获取本地主机名
	ip_port = ('127.0.0.1',9999)

	bufsize = 1024 # 数据缓存大小

	clientnum = 0  # 与服务端连接的客户端数目

	num = 1
	datanum = 0    # 服务端收到数据的数目
	dataall = []       # 服务端收到的所有数据

	updateflag = -1
	updatedata = 0


	def __init__(self, max_clientnum, method):
		super(Server, self).__init__()
		self.max_clientnum = max_clientnum   # 最大客户端数量
		self.method = method    # 同步异步方法，同步为0，异步为1
		self.lock = threading.Lock()

	def run(self):
		self.server.bind(self.ip_port)        # 绑定端口

		self.server.listen(5)

		# 开启服务器数据监听
		if self.method == 0:
			# 同步方法
			print('sync:')
			t=threading.Thread(target=self.sync_update,args=()) 
			t.start()
		elif self.method == 1:
			# 异步方法
			print('async:')
		else:
			print('method error!')
			return

		# 循环判断是否有新连接
		while True:
			# 接受客户端的socket对象和客户端ip,端口信息,
			# accept()方法返回的是一个元组,直接进行解包

			#1.等待客户端 会返回链接的标记位conn，与连接的地址
			#2.客户端同过conn,addr进行通话
			#3.conn就是客户端连接过来而在服务器端为其生成的一个连接实例
			conn,clientaddress=self.server.accept()
			print('connect from:',clientaddress)

			self.clientnum+=1
			print('clientnum:',self.clientnum)

			if self.clientnum <= self.max_clientnum:
				# 为新的TCP连接创建线程
				t=threading.Thread(target=self.connection,args=(conn,clientaddress)) 
				t.start()

		self.server.close()                # 关闭连接


	# 一个TCP连接
	def connection(self, conn, addr):

		while True:
		    # 使用TCP协议进行数据传输
			# 查看标记位与IP地址
			# print(conn,addr)

			# 循环处理客户端请求

			# 收到client发送的数据
			data = conn.recv(self.bufsize)


			
			if len(data) == 0:
				break
			else:
				# 收到有效数据
				# 将数据进行更新

				# 同步更新
				if self.method ==0:
					self.lock.acquire()
					self.datanum += 1
					self.dataall.append(float(bytes.decode(data)))
					self.lock.release()

					temp = float(bytes.decode(data))
					# print(temp)

					# 将更新好的数据发送回client
					while True:
						if self.updateflag != self.clientnum and self.updateflag != -1:
							conn.send(self.updatedata)
							self.lock.acquire()
							self.updateflag += 1
							self.lock.release()
							break

				# 异步更新
				else:
					result = self.async_update(float(bytes.decode(data)))
					conn.send(result)


		self.clientnum -= 1


	# 同步更新数据
	def sync_update(self):
		
		# 检测收到CLIENTNUM个client的数据
		while True:
			# 循环检测是否收到了所有的数据
			num = 0
			if self.datanum == self.max_clientnum and (self.updateflag == self.clientnum or self.updateflag == -1):

				for i in range(0,len(self.dataall)):
					num = num + self.dataall[i]
				# num = num/len(self.dataall)
				# 对值进行更新
				self.updatedata = str.encode(str(num))
				self.updateflag = 0

				self.datanum = 0
				self.dataall = []
		

		# 返回更新后的值

	# 异步更新数据
	def async_update(self, data):

		# 循环检测服务端有没有解锁
		self.lock.acquire()
		print('before',data,self.num)
		self.num = (data+self.num)
		self.updatedata = str.encode(str(self.num))
		print('after',self.updatedata,self.num)
		result = self.updatedata
		self.lock.release()

		return result

			


if __name__ == '__main__':
	num = input('client num:')
	method = input('method(0 for sync, 1 for async):')
	s = Server(int(num),int(method))
	s.run()
			
