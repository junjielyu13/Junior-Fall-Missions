import socket
from threading import Thread
import time


class Manager:
    def __init__(self, socket, addr, username):
        self.ip = addr[0]
        self.port = addr[1]
        self.username = username
        self.socket = socket

    def getId(self):
        return f"{self.ip}-{self.port}"

    def getTime(self):
        return str(time.strftime("%Y-%m-%d %H:%M:%S"))

    def sendMsg(self, msg, username):
        self.socket.send((f"{self.getTime()} {username}: {msg} \n").encode('utf-8'))

    def recvMsg(self, bufsize=1024):
        try:
            data = self.socket.recv(bufsize).decode('utf-8')
            if data == "quit" or not data:
                for c in clients.values():
                    c.sendMsg(f"{self.username} ({self.port}) is disconnected\n", self.username)
                return False
            return data
        except:
            return False

    def close(self):
        try:
            self.socket.close()
        except:
            return False


    def new_client(client):
        try:
            print(f"({client.ip}, {client.port}) try to connect")

            data = client.recvMsg()

            if not data:
                return

            client.username = data

            print(f"{client.username} ({client.port}) is connected \n")
            iports[client.username] = client.getId()

            for c in clients.values():
                c.sendMsg(f"{client.username} ({client.port}) is connected\n", client.username)

            while True:
                data = client.recvMsg()
                if not data:
                    break

                print(f"{client.getTime()} : User {client.username} ({client.port}) send > {data}")

                for c in clients.values():
                    c.sendMsg(data, client.username)

        except:
            print("Connection error")

        finally:
            print(f"{client.username}: ({client.ip}, {client.port}) disconnected")
            client.close()
            clients.pop(client.getId())


if __name__ == '__main__':
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432
    clients = {}
    iports = {}

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen(10)
    print(f"listening on {server.getsockname()}")

    try:
        while True:
            conn, addr = server.accept()

            client = Manager(conn, addr, "")

            clients[client.getId()] = client
            thead = Thread(target=Manager.new_client, args=(client,))
            thead.start()

    except:
        client.close()

    finally:
        print("Server is closing")
