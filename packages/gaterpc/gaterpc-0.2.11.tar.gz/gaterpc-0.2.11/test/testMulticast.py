# -*- coding: utf-8 -*-
# Author      : ShiFan
# Created Date: 2024/9/18 09:44
"""The Module Has Been Build for..."""
import socket
import struct
import sys
import time

MCAST_GRP = '239.0.0.7'  # 多播组地址
MCAST_PORT = 5004         # 多播端口
BCAST_ADDR = ("255.255.255.255", 5005)  # 广播地址和端口
BCAST_PORT = 5005
MESSAGE = b"Hello, Broadcast!"


def multicast_send():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    while True:
        message = b"Hello, Multicast!"
        sock.sendto(message, (MCAST_GRP, MCAST_PORT))
        print(f"Message sent: {message}")
        time.sleep(1)


def multicast_recv():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(('', MCAST_PORT))

    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        data, addr = sock.recvfrom(1024)
        print(
            f"Received message: {data}<{type(data)}> from {addr}<{type(addr)}>"
        )


def broadcast_send():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    while True:
        sock.sendto(MESSAGE, BCAST_ADDR)
        print(f"Broadcast message sent: {MESSAGE}")
        time.sleep(1)


def broadcast_recv():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(("", BCAST_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        print(
            f"Received message: {data}<{type(data)}> from {addr}<{type(addr)}>"
        )


if __name__ == '__main__':
    if sys.argv[1] == "send":
        multicast_send()
    elif sys.argv[1] == "recv": 
        multicast_recv()
    elif sys.argv[1] == "bcast_send":
        broadcast_send()
    elif sys.argv[1] == "bcast_recv":
        broadcast_recv()
