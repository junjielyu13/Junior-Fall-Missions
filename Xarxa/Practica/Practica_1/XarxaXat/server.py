import socket
from threading import Thread
import time

class Administrator:
    """
    Class of Adiministrator of server
    ...
    Attributes:
    -----------
    socket :  socket
    ip :      ip address
    port :    port number
    username: username     

    Methods:
    --------
    - getId() -> str:
        get id of client

    - getTime() -> str:
        get current time

    - sendMsg(msg:str, username:str) -> none:
        server sends message to client

    - recvMsg(bufsize:int) -> none:
        server receive message from client

    - closeClient() -> none:
        close client 
    """
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

    def closeClient(self):
        try:
            self.socket.close()
        except:
            return False


def new_client(client):
    '''
    Serve each client as a server
    
    @param client --> Administrator

    @return --> none
    '''

    try:
        print(f"({client.ip}, {client.port}) try to connect")

        # Set the username of the client
        data = client.recvMsg()
        if not data:
            return
        client.username = data
        print(f"{client.username} ({client.port}) is connected \n")

        for c in clients.values():
            c.sendMsg(f"{client.username} ({client.port}) is connected\n", client.username)

        while True:
            # waiting for client activity
            data = client.recvMsg()
            if not data:
                break

            print(f"{client.getTime()} : User {client.username} ({client.port}) send > {data}")

            # forward to other clients
            for c in clients.values():
                c.sendMsg(data, client.username)

    except:
        print("Connection error")

    finally:
        print(f"{client.username}: ({client.ip}, {client.port}) disconnected")
        client.closeClient()
        clients.pop(client.getId())



if __name__ == '__main__':
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432
    clients = {}

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen(10)
    print(f"listening on {server.getsockname()}")

    try:
        while True:
            conn, addr = server.accept()

            client = Administrator(conn, addr, "")

            clients[client.getId()] = client
            thead = Thread(target=new_client, args=(client,))
            thead.start()

    except:
        print('Server error')

    finally:
        print("Server is closing")
        client.close()