#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socketserver


class Myserver(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data, '我是self.clinet_address', self.client_address)
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 9999

    # 设置allow_reuse_address允许服务器重用地址
    socketserver.TCPServer.allow_reuse_address = True
    # 创建一个server, 将服务地址绑定到127.0.0.1:9999
    server = socketserver.TCPServer((HOST, PORT), Myserver)
    # 让server永远运行下去，除非强制停止程序
    server.serve_forever()
