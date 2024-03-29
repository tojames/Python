## 今日内容

ARP协议：

- 地址解析协议
- 通过ip地址获取其MAC地址

## 

### 1. TCP协议

- **应用场景**：文件上传下载（邮件、网盘、缓存电影）

- **特点**（3）：可靠、传输效率较低、全双工，重传机制、发送的每一帧都有确认回复
- **三次握手**：请求(SYN)—> 确认(ACK)+请求—>确认
  - 通信：建立在全双工连接的基础上
- **长连接**：会一直占用双方port
- I/O：相对于**内存**来说
  - write 是 send
  - read 是 recv

- **四次挥手**：请求(FIN)—> 确认—>请求—>确认
  - 断开：四次

![TCP](/Users/henry/Documents/截图/Py截图/TCP.png)

### 2. UDP协议

- **场景**：即时通讯（qq，wechat）
- **特点**：无连接、速度快，可能会丢帧
- UDP 是User Datagram Protocol的简称， 中文名是用户数据报协议

#### Note(2)

- TCP传输数据几乎没有限制，UDP能够传递数据长度是有限的，是根据数据传递设备的设置有关
- Tcp可靠有连接，udp不可靠无连接

### 3. OSI(Open System Interconnection)

1. 应用层
2. 表示层
3. 会话层
4. 传输层
5. 网络层
6. 数据链路层
7. 物理层

OSI**五层**协议(简化)

1. 应用层：代码
2. 传输层：tcp/udp 端口号，**四层路由器、四层交换机**
3. 网络层：ipv4/ipv6，**三层路由器、三层交换机**
4. 数据链路层：mac地址，arp协议，**(二层)交换机**
5. 物理层：二进制流

TCP/IP(**arp在tcp/ip中属于网络层**)

1. 应用层
2. 传输层
3. 网络层
4. 链路层

#### Note

- 家用路由器集成了交换功能
- 网际层协议:IP协议、ICMP协议、ARP协议、RARP协议。 
- 传输层协议:TCP协议、UDP协议。 
- 应用层协议:FTP、Telnet、SMTP、HTTP、RIP、NFS、DNS

### 4. socekt(套接字)

- 工作在应用层和传输层之间的抽象层
- 帮助我们完成所有信息的组织和拼接
- socket历史：
  - 同一机器上的两个服务之间的通信(基于文件)
  - **基于网络**的多台机器之间的多个服务通信

## 4. Socket模块

### 2.1 tcp

```python
type = SOCK_STRESM  # 表示tcp协议
sk.listen(n)        # n 表示允许多少个客户端等待，3.7之后无限制
sk.accept()         # 阻塞
# 服务端需要一直监听，不能关闭
```

需求：

1. server和client连接后，知道是哪一个好友
2. 不同好友的聊天颜色不同
3. 多个人能互相聊

### 2.2 UDP

```python
# server
import socket
sk = socket.socket(type = socket.SOCK_DGRAM)
sk.bind(('127.0.0.1', 9000))

msg, client_addr = sk.recvfrom(1024)
print(msg)
sk.sendto(b'received', client_addr)
sk.close()

# client
import socket
sk = socket.socket(type = socket.SOCK_DGRAM)

sk.sendto(b'hello', ('127.0.0.1', 9000))
ret = sk.recv(1024)
print(ret)
sk.close()
```

需求：

- 实现一个人和多个人聊天
- 每个人标识