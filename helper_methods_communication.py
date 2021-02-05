import socket
from time import sleep


def receive(conn):
    data = conn.recv(2048).decode('utf-8')
    return data


def send(conn, mess):
    # sleep(0.02)
    try:
        conn.send(str.encode(mess))
    except socket.error as e:
        print(e)

