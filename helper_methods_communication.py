import socket


def receive(conn):
    data = conn.recv(4096).decode('utf-8')
    return data


def send(conn, mess):
    try:
        conn.sendall(str.encode(mess))
    except socket.error as e:
        print(e)

