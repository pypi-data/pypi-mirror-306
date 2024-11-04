# -*- coding: utf-8 -*-
# Author      : ShiFan
# Created Date: 2024/9/25 17:29
import sys

import zmq
import time

def server():
    context = zmq.Context()

    # 创建一个 REP (reply) socket
    socket = context.socket(zmq.REP)
    socket.set(zmq.constants.SocketOption.IPV6, 1)

    # 使用 bind 方法和 IPv6 地址绑定到端口
    socket.bind("tcp://[::]:5555")  # 注意 IPv6 地址需要放在方括号内

    while True:
        # 接收消息
        message = socket.recv_string()
        print(f"Received request: {message}")

        # 发送回复
        socket.send_string("World")


def client():
    context = zmq.Context()

    # 创建一个 REQ (request) socket
    socket = context.socket(zmq.REQ)
    socket.set(zmq.constants.SocketOption.IPV6, 1)

    # 使用 connect 方法和 IPv6 地址连接到服务器
    socket.connect("tcp://[::]:5555")  # 注意 IPv6 地址需要放在方括号内

    for _ in range(10):
        # 发送请求
        print("Sending request ...")
        socket.send_string("Hello")

        # 接收回复
        message = socket.recv_string()
        print(f"Received reply: {message}")

        time.sleep(1)


if __name__ == "__main__":
    if sys.argv[1] == "client":
        client()
    elif sys.argv[1] == "server":
        server()